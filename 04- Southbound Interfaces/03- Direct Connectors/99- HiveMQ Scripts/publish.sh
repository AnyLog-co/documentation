#!/bin/sh
# hivemq_publisher.sh - publish random sensor readings to an MQTT broker (HiveMQ)
# Message: {"device_name":"sensor-1","timestamp":"2026-10-22T18:00:00Z","value":42.17}
#
# Usage:   ./hivemq_publisher.sh
# Options: BROKER=10.0.0.5 TOPIC=plant/line1 INTERVAL=5 ./hivemq_publisher.sh
#
# If mosquitto_pub is not installed locally, the script re-runs itself inside the
# eclipse-mosquitto Docker image (requires Docker).

if ! command -v mosquitto_pub >/dev/null 2>&1; then
  echo "mosquitto_pub not found locally - running inside eclipse-mosquitto container"
  # strip CRLF so the script also works when saved with Windows line endings
  tr -d '\r' < "$0" | exec docker run --rm -i --init --network host \
    -e BROKER -e PORT -e TOPIC -e INTERVAL -e DEVICES \
    eclipse-mosquitto:2 sh -s
fi

BROKER=${BROKER:-localhost}
PORT=${PORT:-1883}
TOPIC=${TOPIC:-sensors/data}
INTERVAL=${INTERVAL:-5}
DEVICES=${DEVICES:-"sensor-1 sensor-2 sensor-3"}

echo "Publishing to ${BROKER}:${PORT} topic '${TOPIC}' every ${INTERVAL}s (Ctrl+C to stop)"

while true; do
  for DEVICE in $DEVICES; do
    TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    R=$(( $(od -An -N2 -tu2 /dev/urandom) % 10000 ))
    PAYLOAD=$(printf '{"device_name":"%s","timestamp":"%s","value":%d.%02d}' "$DEVICE" "$TS" $((R / 100)) $((R % 100)))
    mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" -q 1 -m "$PAYLOAD" && echo "$TOPIC $PAYLOAD"
  done
  sleep "$INTERVAL"
done