# use ubuntu:latest as base
FROM alpine:latest

# set root password
RUN echo "root:bdi_lab!" | chpasswd

# update
RUN apk update && apk upgrade

# apk installs
RUN apk add --update openssh
RUN apk add --update vim
RUN apk add --update sudo
RUN apk add --update iputils-ping
RUN apk add --update bind-tools
RUN apk add --update python3
RUN apk add --update openssh-server-pam

# create normal user and add to sudo
RUN adduser -g ansible ansible -D
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
EXPOSE 22
RUN apk update && apk upgrade
RUN ssh-keygen -A

CMD ["/usr/sbin/sshd", "-D"]


#ENTRYPOINT ["tail", "-f", "/dev/null"]

WORKDIR /root/
