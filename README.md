# Quality Assurance for Infrastructure Orchestrators 

> Placeholder for contents related to the infrastructure orchestrator project. Contents will soon be updated. 

### Organization

- Branches: `master (active)`, `smith (inactive)`, `lamia (inactive)`

### Usage
* output YAML files by default are to be saved to `{{ PROJECT_ROOT }}/data/generated_yaml/<timestamp>/lv{{ LEVEL }}`
  * corresponding dataset is saved to `{{ PROJECT_ROOT }}/data/generated_yaml/<timestamp>`

# Code Installation
* create a virtual environment for python version **3.10** and activate it
* in `<project root>` run `pip install -e .` 

Now you can run the program by calling `cftools` in your terminal

# Docker Infrastructure Setup
1. install docker
2. change directory to `{{ PROJECT_ROOT }}/files/docker_scripts`
3. build the images by running `./build all`
  * these images are used to deploy our ansible hosts for testing
4. deploy the infrastructure by running `./run`
  * this just executes the docker command that utilizes the `docker-compose.yml` file in the same directory
5. change directory to `{{ PROJECT_ROOT }}/files/docker_scripts/ssh`
6. run `./add_to_personal` to import the ssh key and config file required to connect to the docker hosts without a password
  * **NOTE** this script should only be executed once. If there was a mistake and you need to execute it again, you will have to read the script and manually find the commands you need to re-execute.
  * optionally you can just follow the commands that are listed in the contents of `add_to_personal` so you can see what gets changed
7. if all goes well, you should now be able to ssh into your docker hosts. try the following commands:
  * `ssh ubuntu1`
  * `ssh alpine1`
  * `ssh centos1`
  * `ssh redhat1`
8. if you can connect to your docker hosts then you are done.
