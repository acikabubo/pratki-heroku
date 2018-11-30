FROM python:3.7

LABEL Aleksandar Krsteski "krsteski_aleksandar@hotmail.com"

ENV LANG=C.UTF-8

# Update system and install tmux
RUN apt-get update -qq  && \
    apt-get upgrade -yqq && \
    apt-get install sudo tmux supervisor -yqq && \
    apt-get autoremove -y

# Set git aliases
RUN git config --global alias.s status && \
    git config --global alias.co checkout && \
    git config --global alias.b branch

ARG USER=devel
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID $USER; exit 0  # do not crash on already existing GID
RUN useradd -ms /bin/bash -u $UID -g $GID $USER

# Install necessary packages
RUN pip3 install -U setuptools
RUN pip3 install --upgrade pip
RUN pip3 install pip-tools pip-review pipdeptree

# Make requirements file and put in tmp folder
# ADD requirements.in /tmp/requirements.in
# RUN pip-compile /tmp/requirements.in

# Sync packages
ADD requirements.txt /tmp/requirements.txt
RUN pip-sync /tmp/requirements.txt

# Remove tmp files
RUN rm -rf /tmp/requirements.in /tmp/requirements.txt

# Set necessary env vars
ENV DRPB_ACCESS_TOKEN k3RJ3XBM0RsAAAAAAAADi5DeRos9Wo6mqAe5QX1URifVxBo5JJY2LijhD1-U_Y_t
ENV FILE_PATH /pratki.txt
# Env vars for oauth credentials
# Facebook oauth credentials
ENV FB_ID 1982853558673321
ENV FB_SECRET ea3bb54866a4bc6667a78cabca0034be
# Google oauth credentials
ENV G_ID = 1073788361141-872fbem3o8mr9ol71730ltoppb21ansq.apps.googleusercontent.com
ENV G_SECRET Qy012SanPwRfj7oFCCj1UtAI

# It use for debug purposes and from flask debug toolbar
ENV FLASK_ENV development

RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER

USER $USER

ADD . /pratki-heroku
RUN chown -R $user:$gid /pratki-heroku

WORKDIR /pratki-heroku

# Shell form of ENTRYPOINT ignores any CMD
# or docker run command line arguments
# ENTRYPOINT tmux new -s server bash
