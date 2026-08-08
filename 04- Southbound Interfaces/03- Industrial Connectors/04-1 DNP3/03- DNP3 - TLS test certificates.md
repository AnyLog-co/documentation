---
title: "DNP3 TLS Test Certificates"
description: Generating a local CA chain for mutual TLS between an AnyLog DNP3 master and an outstation, for testing only
layout: page
source_path: "DNP3-tls-test-certificates.md"
---

<!--
## Changelog
- (original) Lived as ca_chain/README.md under 06- Networking & Security/C- DNP3 certificates/, alongside
              committed .cert/.key files (including private keys) and create_certificates.sh
- 2026-07-14 | Rewritten as a standalone document for 04- Southbound Interfaces, alongside DNP3.md. The
              generation script is now embedded here directly, so nothing needs to be committed to the repo —
              readers generate their own CA chain locally, in a directory outside version control. The prior
              06- Networking & Security/C- DNP3 certificates/ directory (committed certs, keys, and .gitignore)
              can be removed once this replaces it.
-->

# DNP3 TLS Test Certificates

This page generates a small, local CA chain for mutual TLS between an AnyLog DNP3 **master** and an
**outstation** — for example, [opendnp3](https://github.com/dnp3/opendnp3)'s `outstation-demo`, configured for
TLS. It produces a root CA plus one client certificate (the AnyLog master) and two server certificates
(outstations), all signed by that CA.

**For testing only.** These are self-signed, lab-only credentials — do not reuse them in production, and do not
commit the generated `.cert`/`.key` files to any repository. Run the script below in a working directory of your
own, outside of version control, and regenerate a fresh chain whenever you need one.

## Generating the chain

Save the following as `create_certificates.sh` in an empty working directory, then run `bash
create_certificates.sh`. It has no dependencies beyond `openssl`.

```bash
#!/usr/bin/env bash
# Generate a small CA chain for DNP3 TLS lab tests (AnyLog master <-> outstation).
#
# Usage:
#   mkdir -p ~/dnp3-tls-test && cd ~/dnp3-tls-test
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

rm -f master1.csr outstation1.csr outstation2.csr *.srl

echo "=== Verify chain ==="
openssl verify -CAfile "${CA_CERT}" master1.cert outstation1.cert outstation2.cert

echo "OK: certificates in $(pwd)"
```

This produces 8 files in your working directory:

| File | Role |
|---|---|
| `anylogDNP3ca.cert` / `anylogDNP3ca.key` | Root CA |
| `master1.cert` / `master1.key` | AnyLog master (TLS client) |
| `outstation1.cert` / `outstation1.key` | Primary test outstation (TLS server) |
| `outstation2.cert` / `outstation2.key` | Second outstation (optional) |

The script's own cleanup (`rm -f ... *.srl`) already removes the intermediate CSRs and OpenSSL's serial file —
so nothing but the certs and keys above is left behind, and there's no separate `.gitignore` to maintain. If you
do generate the chain inside a version-controlled directory for convenience, add `*.cert`, `*.key`, `*.csr`, and
`*.srl` to that repo's `.gitignore` before running the script.

## Configuring the AnyLog master

Point the master's TLS settings at your generated files (use the actual path to your working directory):

| Keyword | Path |
|---|---|
| `tls_ca` | `/path/to/your/working/dir/anylogDNP3ca.cert` |
| `tls_cert` | `/path/to/your/working/dir/master1.cert` |
| `tls_key` | `/path/to/your/working/dir/master1.key` |

## Configuring the outstation (TLS server)

| Setting | File |
|---|---|
| Peer / CA | `anylogDNP3ca.cert` |
| Local certificate | `outstation1.cert` |
| Private key | `outstation1.key` |

With `opendnp3` built at `~/opendnp3/build`, after generating the chain:

```bash
cd ~/opendnp3/build
./outstation-tls-demo \
  /path/to/your/working/dir/anylogDNP3ca.cert \
  /path/to/your/working/dir/outstation1.cert \
  /path/to/your/working/dir/outstation1.key
```

Plain TCP, no TLS: run `./outstation-demo` instead, from the same directory.

## See also

- [DNP3](../04-%20DNP3.md#dnp3-out-station-testing) —
  the main DNP3 connector doc; this page is referenced from its outstation-testing section.