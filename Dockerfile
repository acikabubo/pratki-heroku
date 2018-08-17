FROM python:3.7

LABEL Aleksandar Krsteski "krsteski_aleksandar@hotmail.com"

ENV LANG=C.UTF-8

RUN apt-get update -qq  && \
    apt-get upgrade -yqq && \
    apt-get install tmux -yqq && \
    apt-get autoremove -y

RUN pip3 install -U setuptools
RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt

ENV DRPB_ACCESS_TOKEN k3RJ3XBM0RsAAAAAAAADi5DeRos9Wo6mqAe5QX1URifVxBo5JJY2LijhD1-U_Y_t
ENV FILE_PATH /pratki.txt

ADD . /pratki-heroku

WORKDIR /pratki-heroku
