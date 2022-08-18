# Nokia SR Linux - Config Validation

This project is the final project of my internship.

## What is validation?

On Nokia SR Linux devices, you can configure the device with a config file. These files are mostly have .cfg extention and have a format of a JSON-like format. While configuring the device, the config file is checked by the device itself if it has any mistake inside it (like a syntax error or such...).

To validate a config file, these steps should be followed:
- Copy the file to the device (with SCP or another way)
- Connect with SSH to the device
- Use these commands to validate and configure:
```
enter candidate
source <file-name>
commit validate
```

If the file is valid, the device also get configured.

If not, it shows errors as output.

## Why we need such a project?

Let's assume we just want to see if any config file is valid or not.

Following these steps for one config file is easy. But for multiple config files (think about fifty of them) it is too many commands to write.

This projects main goal is to connect to an SR Linux device with simple inputs and validate multiple config files with a single start.

## Usage

The "srl_cfg_python" folder is the Python project for the development of the image, you can check the code there.

The "srl_cfg_image" folder is the Docker image project for simple use, ypu can run it without any installation. Just read its README file and learn.

More details inside folders.