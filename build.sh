#!/usr/bin/env bash
set -e

docker build -t experiment-builder .
docker run experiment-builder | \
  docker build -t geowa4/python-pex-rxpy-asyncio-experiment  -
docker push geowa4/python-pex-rxpy-asyncio-experiment

