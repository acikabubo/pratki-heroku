#!/bin/bash

IMIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$(dirname "$IMIN")"

docker build --force-rm -t pratki-heroku \
    --build-arg user=$USER \
    --build-arg uid=`id -u $USER` \
    --build-arg gid=`id -g $GROUP` \
    $SRC

DANGLING=$(docker images -f "dangling=true" -q)
if [ "x""$DANGLING" != "x" ]; then
    docker rmi $DANGLING
fi

docker volume ls -qf dangling=true | xargs -r docker volume rm