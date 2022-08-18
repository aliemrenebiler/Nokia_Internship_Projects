
import sys
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from netmiko import ConnectHandler


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# SCP with Paramiko
def scp_with_paramiko(hostname, username, password, source, destination):

    try:
        print("Connecting with SSH by Paramiko...")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        print("Connected!")

        print("Copying with SCP...")
        scp = SCPClient(client.get_transport())
        scp.put("config_files/" + source, remote_path = destination)
        print("Copied!")

        scp.close()
        client.close()
        return True

    except Exception as e:
        print(bcolors.FAIL + "(!) PARAMIKO ERROR: " + str(e) + bcolors.ENDC)
        return False


# Config with Netmiko
def config_with_netmiko(type, hostname, username, password, config_file):

    device = {
        "device_type": type,
        "host": hostname,
        "username": username,
        "password": password,
    }

    try:
        print("Connecting with SSH by Netmiko...")
        client = ConnectHandler(**device)
        client.find_prompt()
        print("Connected!")

        print("Configuration started...")
        output = client.send_multiline_timing(
            ["enter candidate", "source " + config_file , "commit validate"],
            delay_factor=1,
        )
        print("Configuration ended!")

        error_occured = False
        for item in output.split("\n"):
            if "error" in item or "Error" in item:
                print(bcolors.FAIL + "(!) CONFIG ERROR: " + item.strip() + bcolors.ENDC)
                error_occured = True
        if (not error_occured):
            print("Config is valid.")

        client.disconnect()
        
    except Exception as e:
        print(bcolors.FAIL + "(!) NETMIKO ERROR: %s" + str(e) + bcolors.ENDC)


# Main Code
if(len(sys.argv) != 2):
    print(bcolors.FAIL + "(!) ARGS ERROR: There should be one argument which will be the name of config file." + bcolors.ENDC)
else:
    config_file = sys.argv[1]
    print("Config file name: " + config_file)
    copied = scp_with_paramiko("172.20.20.2", "admin", "admin", config_file, "/home/admin/")

    if(copied):
        config_with_netmiko("nokia_srl", "172.20.20.2", "admin", "admin", config_file)

print("Program was ended!")


'''
IMPORTANT
This issue was fixed but this note might be helpful in the future.

If you connected to a container before and reconfigured it later, this error might happen:
(!) PARAMIKO ERROR: Host key for server '172.20.20.2' does not match: got '...', expected '...'

This is because there was a saved ssh key for that IP, but that key was changed with reconfiguration.

Use this command to delete previous ssh key:
ssh-keygen -f "/home/USER/.ssh/known_hosts" -R "HOSTNAME"
'''