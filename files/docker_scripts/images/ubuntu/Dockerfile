# use ubuntu:latest as base
FROM ubuntu:latest

# set root password
RUN echo "root:bdi_lab!" | chpasswd

# update
RUN apt update && apt upgrade -y

# install stuff
RUN apt install -y openssh-client openssh-server
RUN apt install -y iputils-ping
RUN apt install -y vim
RUN apt install -y sudo
RUN apt install -y dnsutils

# install python executables
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update

RUN apt install -y python2.7
RUN apt install -y python3.7
RUN apt install python-is-python3

# create normal user and add to sudo
RUN useradd -m ansible -s /bin/bash
RUN echo "ansible:bdi_lab!" | chpasswd

# add sudoers
RUN usermod -aG sudo ansible
RUN usermod -aG sudo root

# copy ssh keys to ubuntu user
RUN mkdir /home/ansible/.ssh
COPY ssh/cf-key /home/ansible/.ssh/
COPY ssh/cf-key.pub /home/ansible/.ssh/
COPY ssh/config /home/ansible/.ssh/
WORKDIR /home/ansible/.ssh/
RUN cat cf-key.pub >> authorized_keys
RUN chmod 600 authorized_keys
RUN chmod 600 cf-key
RUN chmod 600 config
WORKDIR /home/ansible/
RUN chown -R ansible .ssh
RUN chgrp -R ansible .ssh

# copy ssh keys to root
RUN mkdir /root/.ssh
COPY ssh/cf-key /root/.ssh/cf-key
COPY ssh/cf-key.pub /root/.ssh/cf-key.pub
COPY ssh/config /root/.ssh/
WORKDIR /root/.ssh/
RUN cat cf-key.pub >> authorized_keys
RUN chmod 600 authorized_keys

# set up ssh server
COPY ssh/sshd_config /etc/ssh/sshd_config
EXPOSE 22
RUN service ssh start
CMD ["/usr/sbin/sshd","-D"]

WORKDIR /root/
