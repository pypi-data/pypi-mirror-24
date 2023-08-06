###
# file: Dockerfile
#
# language: python3
# licence: GPL>=v3
# date begin: 20170514
# version: 4.
# author: bue
#
# run:
#    bugfixing and new realworld:
#    bue: can not start container with entrypoint  blender and cmd help
#    (Unable to open a display) or background (problem with sockets)
#    to be able to enter the container comment out entrypoint blender and cmd help
#    and enable cmd bash
#
#    docker build . -t zerogravity:latest
#
#    docker run zerogravity
#    docker run --rm zerogravity blender --help
#    docker run --rm -ti zerogravity /bin/bash
#    docker run --rm -v /host/directory:/container/directory zerogravity blender --help
#    docker run --rm -v /Users/buchere/src_gitlab/zerogravity:/mnt/host -ti zerogravity /bin/bash
#
#    old realworld:
#    bue: entrypoint blender and cmd help
#
#    docker build . -t zerogravity:latest
#
#    docker run --rm zerogravity
#    docker run --rm -v /host/directory:/container/directory zerogravity
#
# description:
#    dockerized blender software
###

FROM debian:sid
MAINTAINER elmar bucher <ulmusfagus zoho com>

RUN apt-get update && apt-get install -y \
  blender\
  libopenhmd0

COPY ./bplayer /usr/local/lib/bplayer
COPY ./bgectrlrmodule.py /usr/local/lib/zgravity/

RUN mkdir -p /mnt/host
VOLUME ["/mnt/host"]

#ENTRYPOINT ["/usr/bin/blender"]
#CMD ["--help"]
CMD ["/bin/bash"]
