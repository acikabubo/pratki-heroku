#!/bin/bash

docker build --force-rm -t pratki-heroku .

DANGLING=$(docker images -f "dangling=true" -q)
if [ "x""$DANGLING" != "x" ]; then
    docker rmi $DANGLING
fi

docker volume ls -qf dangling=true | xargs -r docker volume rm