# use redhat/ubi8:latest as base
FROM redhat/ubi8:latest

# set root password
RUN echo "root:bdi_lab!" | chpasswd

# update
RUN yum update -y

RUN yum install \
    openssh \
    openssh-server \
    openssh-clients \
    vim \
    sudo \
    bind-utils \
    python2 \
    python3 \
    -y

# create normal user and add to sudo
RUN useradd -m ansible -s /bin/bash
RUN echo "ansible:bdi_lab!" | chpasswd

# add sudoers
RUN echo "ansible ALL=(ALL) ALL" > /etc/sudoers.d/ansible && chmod 0440 /etc/sudoers.d/ansible

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
RUN mkdir /etc/ssh/sshd_config.d
EXPOSE 22
RUN ssh-keygen -A

CMD ["/usr/sbin/sshd", "-D"]

WORKDIR /root/
