#!/usr/bin/env bash
docker run --rm -it --network host hivemq/mqtt-cli \
  sub -h localhost -p 1883 -t 'sensors/#' -T