#!/bin/bash

IMIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$(dirname "$IMIN")"

docker network create pratki-net

docker build --force-rm -t pratki-heroku \
    --build-arg USER=$USER \
    --build-arg UID=`id -u $USER` \
    --build-arg GID=`id -g $GROUP` \
    $SRC
    
docker create --rm -it \
    --name pratki-heroku \
    -v $SRC:/pratki-heroku \
    --hostname server \
    --network pratki-net \
    -p 5000:5000 \
    pratki-heroku tmux new -s server bash

docker run \
    --name pratki-nginx \
    -v $SRC/nginx/nginx.conf:/etc/nginx/conf.d/default.conf \
    --network pratki-net \
    -p 80:80 \
    nginx:stable-alpine

docker start -a -i pratki-heroku

DANGLING=$(docker images -f "dangling=true" -q)
if [ "x""$DANGLING" != "x" ]; then
    docker rmi $DANGLING
fi
docker volume ls -qf dangling=true | xargs -r docker volume rm

docker rm -f pratki-nginx

echo "Successfuly destroyed all containers"
exit 0
