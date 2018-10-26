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
    -p 80:80 \
    -p 443:443 \
    --network pratki-net \
    -v $SRC/nginx/nginx.conf:/etc/nginx/conf.d/default.conf \
    -v $SRC/nginx/ssl/pratki-heroku.crt:/etc/nginx/pratki-heroku.crt \
    -v $SRC/nginx/ssl/pratki-heroku.key:/etc/nginx/pratki-heroku.key \
    -v $SRC/nginx/html/502.html:/usr/share/nginx/html/502.html \
    -d nginx:stable-alpine sh -c "while true; do nginx -g 'daemon off;'; sleep 1; done"

docker start -a -i pratki-heroku

docker rm -f pratki-nginx

DANGLING=$(docker images -f "dangling=true" -q)
if [ "x""$DANGLING" != "x" ]; then
    docker rmi $DANGLING
fi
docker volume ls -qf dangling=true | xargs -r docker volume rm

echo "Successfuly destroyed all containers"
exit 0
