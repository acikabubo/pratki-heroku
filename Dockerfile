FROM python:3.7

LABEL Aleksandar Krsteski "krsteski_aleksandar@hotmail.com"

ENV LANG=C.UTF-8

ARG USER=acika

# Update system and install tmux
RUN apt-get update -qq  && \
    apt-get upgrade -yqq && \
    apt-get install sudo tmux -yqq && \
    apt-get autoremove -y

# Set git aliases
RUN git config --global alias.s status && \
    git config --global alias.c checkout && \
    git config --global alias.b branch

ADD requirements.in /tmp/requirements.in

# Install necessary packages
RUN pip3 install -U setuptools
RUN pip3 install --upgrade pip
RUN pip3 install pip-tools pip-review pipdeptree

# Make requirements file and put in tmp folder
RUN pip-compile /tmp/requirements.in
ADD requirements.txt /tmp/requirements.txt

# Install requirements
# RUN pip3 install r /tmp/requirements.txt

# Sync packages
RUN pip-sync /tmp/requirements.txt

# Remove tmp files
RUN rm -rf /tmp/requirements.in /tmp/requirements.txt

# Set necessary env vars
ENV DRPB_ACCESS_TOKEN k3RJ3XBM0RsAAAAAAAADi5DeRos9Wo6mqAe5QX1URifVxBo5JJY2LijhD1-U_Y_t
ENV FILE_PATH /pratki.txt

# Add user to sudo group
RUN useradd -m $USER && echo "$USER:$USER" | chpasswd && adduser $USER sudo && \
    echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER

# USER $USER

ADD . /home/$USER/pratki-heroku
WORKDIR /home/$USER/pratki-heroku

# Shell form of ENTRYPOINT ignores any CMD
# or docker run command line arguments
# ENTRYPOINT tmux new -s server bash
