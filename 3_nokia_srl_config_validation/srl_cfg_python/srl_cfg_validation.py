"""
The main code of SR Linux config file validation.
"""


from os.path import join
from sys import stdout
from json import loads, dump
from loguru import logger
from scp import SCPClient
from netmiko import ConnectHandler
from paramiko import SSHClient, AutoAddPolicy
import utils


logger.remove(0)
logger_config = {
    "handlers": [
        {
            "sink": stdout,
            "colorize": True,
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | <lvl>{level}: {message}</lvl>",
        },
        {
            "sink": join(
                "log_files", "config-validation_{time:YYYY-MM-DD_HH:mm:ss}.log"
            ),
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level}: {message}",
        },
    ],
}
logger.configure(**logger_config)


def connect_with_ssh_paramiko(hostname, username, password):
    """Connect with SSH using the paramiko library"""
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname,
            username=username,
            password=password,
        )
        return client
    except Exception as error:  # pylint: disable=broad-except
        logger.error("[SSH ERROR]: " + str(error))
        return None


def connect_with_ssh_netmiko(device_type, hostname, username, password):
    """Connect with SSH using the netmiko library"""
    device = {
        "device_type": device_type,
        "host": hostname,
        "username": username,
        "password": password,
    }
    try:
        client = ConnectHandler(**device)
        client.find_prompt()
        return client
    except Exception as error:  # pylint: disable=broad-except
        logger.error("[SSH ERROR]: " + str(error))
        return None


def copy_file_with_scp_paramiko(config_name, path, destination, client):
    """Copy files to SR Linux device with SCP by usinh paramiko's SSH connection"""
    copied = False
    try:
        if client is not None:
            scp = SCPClient(client.get_transport())
            try:
                scp.put(join(path, config_name), remote_path=destination)
                copied = True
            except Exception as error:  # pylint: disable=broad-except
                logger.error('"' + config_name + '" [SCP ERROR]: ' + str(error))
            scp.close()
    except Exception as error:  # pylint: disable=broad-except
        logger.error('"' + config_name + '" [SCP ERROR]: ' + str(error))
    return copied


def end_netmiko_ssh_connection(client):
    """End any SSH connection (netmiko)"""
    if client is not None:
        try:
            client.disconnect()
        except Exception as error:  # pylint: disable=broad-except
            logger.error("[SSH ERROR]: " + str(error))


def end_paramiko_ssh_connection(client):
    """End any SSH connection (paramiko)"""
    if client is not None:
        try:
            client.close()
        except Exception as error:  # pylint: disable=broad-except
            logger.error("[SSH ERROR]: " + str(error))


def reset_configuration(client):
    """Discard any configuration on SR Linux"""
    try:
        if client is not None:
            client.send_multiline_timing(
                [
                    "exit all",
                    "enter candidate",
                    "discard now",
                    "exit all",
                ],
                delay_factor=1,
            )
    except Exception as error:  # pylint: disable=broad-except
        logger.error("[RESET ERROR]: " + str(error))


def validate_config_file(config_name, client):
    """Validate the given SR Linux config file"""
    try:
        if client is not None:
            logger.info('Validating "' + config_name + '"...')
            valid_config = True

            # Check source errors
            source_output = client.send_multiline_timing(
                [
                    "enter candidate",
                    "source " + config_name,
                ],
                delay_factor=1,
            )
            valid_config = utils.check_for_errors(source_output)

            # Check commit errors
            if valid_config:
                commit_output = client.send_multiline_timing(
                    [
                        "commit validate",
                        "exit all",
                    ],
                    delay_factor=1,
                )
                valid_config = utils.check_for_errors(commit_output)

            return valid_config
    except Exception as error:  # pylint: disable=broad-except
        logger.error('"' + config_name + '" [VALIDATION ERROR]: ' + str(error))
        return None


def save_config_as_json(config_name, path, client):
    """Save the valid configuration as JSON file on the device"""
    try:
        if client is not None:
            # Change extention from .cfg to .json
            json_file = utils.change_file_extention(config_name, "json")
            info_text = client.send_multiline_timing(
                ["info | as json"],
                delay_factor=1,
            )
            info_text = info_text.split("\n", 1)[1]  # Deletes first row
            info_text = info_text.rsplit("\n", 2)[0]  # Deletes last two rows
            # Convert to json and write to file
            json_data = loads(info_text)
            with open(join(path, json_file), "w", encoding="utf-8") as json:
                dump(json_data, json)
    except Exception as error:  # pylint: disable=broad-except
        logger.error("[SAVING ERROR]: " + str(error))


def delete_config_file(config_name, client):
    """Delete the config file after validation"""
    try:
        if client is not None:
            client.send_multiline_timing(
                ["bash", "rm -r " + config_name, "exit all"],
                delay_factor=1,
            )
    except Exception as error:  # pylint: disable=broad-except
        logger.error("[CLEAR ERROR]: " + str(error))


# Main Code
all_files = utils.get_file_names("config_files")
config_files = utils.get_config_files(all_files)

if len(config_files) == 0:
    logger.warning("Could not find any config file!")
else:
    logger.info("Found " + str(len(config_files)) + " config file(s)!")
    srl_ip, srl_username, srl_password = utils.get_ip_username_password()

for config_file in config_files:
    logger.info('File Name: "' + config_file + '"')

    ssh = connect_with_ssh_paramiko(srl_ip, srl_username, srl_password)
    FILES_ARE_COPIED = copy_file_with_scp_paramiko(
        config_file, "config_files", "/home/admin", ssh
    )
    end_paramiko_ssh_connection(ssh)

    if FILES_ARE_COPIED:
        ssh = connect_with_ssh_netmiko("nokia_srl", srl_ip, srl_username, srl_password)
        reset_configuration(ssh)
        is_valid = validate_config_file(config_file, ssh)

        if is_valid:
            utils.check_and_create_the_folder("output_files")
            save_config_as_json(config_file, "output_files", ssh)
            delete_config_file(config_file, ssh)
            logger.success('"' + config_file + '": All changes are valid!')

        reset_configuration(ssh)
        end_netmiko_ssh_connection(ssh)

logger.info("Program was ended.")
