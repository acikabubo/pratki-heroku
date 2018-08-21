#!/bin/bash

IMIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$(dirname "$IMIN")"

docker build --force-rm -t pratki-heroku \
    --build-arg USER=$USER \
    --build-arg UID=`id -u $USER` \
    --build-arg GID=`id -g $GROUP` \
    $SRC

docker create --rm -it \
    --name pratki-heroku \
    -v $SRC:/pratki-heroku \
    --hostname server \
    -p 5000:5000 \
    pratki-heroku tmux new -s server bash

docker start -a -i pratki-heroku

DANGLING=$(docker images -f "dangling=true" -q)
if [ "x""$DANGLING" != "x" ]; then
    docker rmi $DANGLING
fi
docker volume ls -qf dangling=true | xargs -r docker volume rm

echo "Successfuly destroyed all containers"
exit 0
