#!/usr/bin/env bash
# Generate a small CA chain for DNP3 TLS lab tests (AnyLog master ↔ outstation).
#
# Usage:
#   cd certs/ca_chain
#   bash create_certificates.sh
#
# AnyLog master (TLS client):  anylogDNP3ca.cert, master1.cert, master1.key
# Outstation (TLS server):     anylogDNP3ca.cert, outstation1.cert, outstation1.key
#
set -euo pipefail
cd "$(dirname "$0")"

CA_CERT=anylogDNP3ca.cert
CA_KEY=anylogDNP3ca.key

echo "=== CA ==="
openssl req -x509 -new -nodes -newkey rsa:2048 \
  -keyout "${CA_KEY}" -sha256 -days 3600 -out "${CA_CERT}" \
  -subj "/C=US/ST=OR/L=Bend/O=AnyLog Certificate Corp"

echo "=== CSRs ==="
openssl req -newkey rsa:2048 -nodes -keyout master1.key -out master1.csr \
  -subj "/C=US/ST=OR/O=AnyLogDNP3/CN=master1"
openssl req -newkey rsa:2048 -nodes -keyout outstation1.key -out outstation1.csr \
  -subj "/C=US/ST=OR/O=AnyLogDNP3/CN=outstation1"
openssl req -newkey rsa:2048 -nodes -keyout outstation2.key -out outstation2.csr \
  -subj "/C=US/ST=OR/O=AnyLogDNP3/CN=outstation2"

echo "=== Signed certs ==="
openssl x509 -req -in master1.csr -CA "${CA_CERT}" -CAkey "${CA_KEY}" -CAcreateserial \
  -out master1.cert -days 3600 -sha256
openssl x509 -req -in outstation1.csr -CA "${CA_CERT}" -CAkey "${CA_KEY}" -CAcreateserial \
  -out outstation1.cert -days 3600 -sha256
openssl x509 -req -in outstation2.csr -CA "${CA_CERT}" -CAkey "${CA_KEY}" -CAcreateserial \
  -out outstation2.cert -days 3600 -sha256

rm -f master1.csr outstation1.csr outstation2.csr

echo "=== Verify chain ==="
openssl verify -CAfile "${CA_CERT}" master1.cert outstation1.cert outstation2.cert

echo "OK: certificates in $(pwd)"
