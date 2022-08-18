.PHONY: all load_the_image run_the_image remove_the_container

all: load run clean

.SILENT:
load: srl-cfg-validation.tar.gz
	echo "Image is loading..."
	sudo docker load < $(shell pwd)/srl-cfg-validation.tar.gz

run:
	echo "Starting the image..."
	sudo docker run -i --net=host -v $(shell pwd)/config_files:/app/config_files --name srl-cfg srl-cfg-validation

clean:
	echo "Cleaning..."
	-sudo docker container stop srl-cfg
	-sudo docker container rm srl-cfg
