# SR Linux Config Validation

This project is for Nokia SR Linux devices.

You can validate multiple config files with a single start.

## How To Use?

You can use it with an virtual SR Linux device by installing Docker or ContainerLab. See more on their documentations.

You should copy all your config files inside "config_files" folder.

If there is no "config_files" folder, create one at the same directory with srl-cfg-validation.tar.gz file.

## Commands

These commands should be used at the same directory with this file.

- To do all and clean (recommended for the first use):
```
make all
```

- To load the image
```
make load
```

- To run the container
```
make run
```

- To clean the previously created container
```
make clean
```
