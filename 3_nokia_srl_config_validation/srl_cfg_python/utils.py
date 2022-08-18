"""
The other modules for file management and string search/modification
"""


from os import listdir, mkdir
from os.path import isfile, join
from loguru import logger


def get_file_names(path):
    """Get only the file names as a list, ignore folders"""
    # This code is short, can be used
    # return [f for f in listdir(path) if isfile(join(path, f))]
    logger.info("Getting config file names...")
    all_contents = listdir(path)
    files_list = []
    for content in all_contents:
        if not isfile(join(path, content)):
            logger.warning('"' + content + '"' + " is a folder, it won't be included.")
        else:
            files_list.append(content)
    return files_list


def get_config_files(files):
    """Get only the config files from all files"""
    config_files = []
    for file in files:
        # split with dot and get the last element (the extention)
        extention = file.rsplit(".", 1)[1]
        if extention != "cfg":
            logger.warning(
                '"' + file + '"' + " is not a config file, it won't be copied."
            )
        else:
            config_files.append(file)
    return config_files


def get_ip_username_password():
    """Get IP, username and password of SR Linux as input"""
    print("------------------------------------------------")
    print("Please enter the informations of SR Linux below.")
    ip = str(input("SRL IP: "))
    username = str(input("SRL Username: "))
    password = str(input("SRL Password: "))
    print("------------------------------------------------")
    logger.info("| IP: " + ip + " | Username: " + username + " | Password: " + password)
    return ip, username, password


def check_and_create_the_folder(folder):
    """Check the folder if it exists. If not, create it"""
    all_contents = listdir()
    file_exist = False
    if folder in all_contents:
        if not isfile(folder):
            file_exist = True

    if not file_exist:
        mkdir(folder)


def check_for_errors(output):
    """Check for the word 'error' inside a long string"""
    lines = output.split("\n")
    no_error = True
    line_index = 0
    while no_error and (line_index < len(lines)):
        if "error".casefold() in lines[line_index].casefold():
            no_error = False
            err_index = line_index
            err_msg = lines[err_index].strip()
            # if error has more lines, print these lines too
            while lines[err_index].strip()[-1] == ":" and err_index + 1 < len(lines):
                err_index += 1
                err_msg += " " + lines[err_index].strip()
            logger.warning(err_msg)
        line_index += 1
    return no_error


def change_file_extention(file_name, new_extention):
    """Change the given file's extention and return it"""
    return file_name.rsplit(".", 1)[0] + "." + new_extention
