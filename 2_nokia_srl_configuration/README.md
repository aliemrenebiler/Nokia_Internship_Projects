# Nokia SR Linux - Configuration

This project is created for configuring an SR Linux device via SSH.

The code gets only one argument, which is config file's name. This config file should be located in the config_files folder.

The code simply connects to the device, sends the config file via SCP and validate it. If it is valid, that means the configuration is done.