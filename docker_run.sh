#!/usr/bin/env bash

docker run \
  --env DISPLAY=$DISPLAY \
  --env PROFILE=breathing-rate \
  --volume /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --name radar-frame-collector-qt \
  --privileged \
  --detach \
  radar-frame-collector-qt:latest