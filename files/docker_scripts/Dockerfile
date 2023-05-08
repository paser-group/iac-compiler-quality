# use ubuntu:latest as base
FROM ubuntu:latest

# set root password
RUN echo "root:bdi_lab!" | chpasswd
RUN 

# update
RUN apt update && apt upgrade -y

# install stuff
RUN apt install -y openssh-client openssh-server
RUN apt install -y iputils-ping
RUN apt install -y vim

# create normal user
RUN useradd -m ubuntu -s /bin/bash
RUN echo "ubuntu:bdi_lab!" | chpasswd

# copy ssh keys to ubuntu user
RUN mkdir /home/ubuntu/.ssh
COPY ssh/cf-key /home/ubuntu/.ssh/
COPY ssh/cf-key.pub /home/ubuntu/.ssh/
COPY ssh/config /home/ubuntu/.ssh/
WORKDIR /home/ubuntu/.ssh/
RUN cat cf-key.pub >> authorized_keys
RUN chmod 600 authorized_keys
RUN chown -R ubuntu *
RUN chgrp -R ubuntu *

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
CMD ["/usr/sbin/sshd","-D"]
RUN service ssh start

WORKDIR /root/
