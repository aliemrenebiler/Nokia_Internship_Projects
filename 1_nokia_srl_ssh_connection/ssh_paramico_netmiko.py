
from netmiko import ConnectHandler
from paramiko import SSHClient, AutoAddPolicy


# Netmiko
def connect_with_netmiko(type, hostname, username, password):

    device = {
        "device_type": type,
        "host": hostname,
        "username": username,
        "password": password,
    }

    try:
        netmiko_connect = ConnectHandler(**device)
        netmiko_connect.find_prompt()
        
        config_commands = ["help"]
        output = netmiko_connect.send_config_set(config_commands, delay_factor=0.2)
        netmiko_connect.disconnect()
        print(output)

    except Exception as e:
        print("(!) NETMIKO ERROR: %s" % (e,))


# Paramiko
def connect_with_paramiko(hostname, username, password):

    try:
        client = SSHClient()

        client.load_system_host_keys()
        client.load_host_keys("/home/alemre/.ssh/known_hosts")
        client.set_missing_host_key_policy(AutoAddPolicy())

        client.connect(hostname, username=username, password=password)

        stdin, stdout, stderr = client.exec_command("help")
        print(stdout.read().decode("utf-8"))

        client.close()

    except Exception as e:
        print("(!) PARAMIKO ERROR: %s" % (e,))


# Main Code

print("\n=== NETMIKO ===\n")
connect_with_netmiko("nokia_srl", "172.20.20.2", "admin", "admin")

print("\n")

print("\n=== PARAMIKO ===\n")
connect_with_paramiko("172.20.20.2", "admin", "admin")


'''
IMPORTANT

If this error happens:
(!) PARAMIKO ERROR: Host key for server '172.20.20.2' does not match: got '...', expected '...'

Use this command on terminal, then start run the code again:
ssh-keygen -f "/home/alemre/.ssh/known_hosts" -R "172.20.20.2"

Then start this code again.
'''