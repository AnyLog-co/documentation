#!/usr/bin/env bash

docker run --name hivemq \
  -p 8080:8080 \
  -p 1883:1883 \
  --pull=always \
  -e HIVEMQ_LICENSE_KEY='P5JL36-0C9C7700-6DB5-467B-ADEA-CE3889F6822C' \
  -e HIVEMQ_LOG_BASED_CLUSTERING_ENABLED=true \
  --rm -d hivemq/hivemq4:latest