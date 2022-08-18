
import sys
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


# Command with Netmiko
def exec_with_netmiko(type, hostname, username, password, command):

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
        output = client.send_multiline_timing(
            [command],
            delay_factor=1,
        )
        print("COMMAND: " + command)
        error_occured = False
        for item in output.split("\n"):
            if "error" in item:
                print(bcolors.FAIL + "(!) COMMAND ERROR: " + item.strip() + bcolors.ENDC)
                error_occured = True
        if (not error_occured):
            print("== OUTPUT ==")
            print(output)
        client.disconnect()
    except Exception as e:
        print(bcolors.FAIL + "(!) NETMIKO ERROR: " + str(e) + bcolors.ENDC)


# Main Code
if(len(sys.argv) != 2):
    print(bcolors.FAIL + "(!) ARGS ERROR: There should be one argument which will be the a command." + bcolors.ENDC)
else:
    command = sys.argv[1]
    exec_with_netmiko("nokia_srl", "172.20.20.2", "admin", "admin", command)

print("Program was ended!")