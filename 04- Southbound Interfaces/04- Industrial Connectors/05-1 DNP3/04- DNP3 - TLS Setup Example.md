---
title: "DNP3 TLS Setup Example"
description: Full DNP3 mutual TLS walkthrough with AnyLog certificate commands — local CA, Operator client certs, outstation server certs, external org files, and optional Master/Operator remote signing.
layout: page
source_path: "DNP3-tls-setup-example.md"
---

<!---
### Change Log
 **Date**   | **Name** | **Change** | **Version** |
 |------------|--|------------|----------|
 | 2026-08-14 | Massimiliano | DNP3 TLS setup example aligned with MQTT Broker TLS Example; Master/Operator remote-sign scenario. | |
--->

# Configure DNP3 TLS

Full worked example for securing AnyLog as a **DNP3 master (TLS client)** against an **outstation (TLS server)** using AnyLog `id generate` / `id sign` commands.

For OpenSSL-only lab files and `opendnp3` demos, see [DNP3 TLS Test Certificates](./03-%20DNP3%20-%20TLS%20test%20certificates.md). For the connector reference, see [DNP3](../05-%20DNP3.md).

**Roles (do not confuse):**

| Role | Meaning |
|------|---------|
| AnyLog **Master node** | Network master — optional holder of the CA private key for remote signing |
| AnyLog **Operator** | Runs `run plc client` / `get dnp3 values` as the DNP3 **master** (TLS client) |
| **Outstation** | DNP3 device or demo (TLS server) |

Local signing (CA key on the same node that signs) is enough for a single-node lab. Remote signing is **optional** — see [Scenario: Master node + Operator with remote signing](#scenario-master-node--operator-with-remote-signing).

## Create CA Authority for self-signed TLS certificates

```anylog
<id generate certificate authority where country = US and
  state = CA and locality = "Redwood City" and
  org = AnyLogDNP3CA and
  output_name = "AnyLogDNP3CA" and
  expiration_days = 3650
>
```

Writes under `!pem_dir`: `AnyLogDNP3CA.crt` / `AnyLogDNP3CA.key`.

## Create certificate request — AnyLog DNP3 master (TLS client)

On the Operator that will poll the outstation:

```anylog
<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "AnyLog DNP3 master"
  and hostname = master1
  and alt_name = 192.168.1.60
  and ip = 192.168.1.60 and
  output_name = "master1"
>
```

## Sign certificate with above CA (local)

```anylog
<id sign certificate request where ca_org = AnyLogDNP3CA and ca_output_name = "AnyLogDNP3CA"
  and server_org = "AnyLog DNP3 master" and output_name = "master1"
  and expiration_days = 3650
>
```

Writes under `!pem_dir`: `master1.csr` / `.key` / `.pem`, then `master1.crt`.

## Create and sign outstation certificates (TLS servers)

```anylog
<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "AnyLog DNP3 outstation"
  and hostname = outstation1
  and alt_name = 192.168.1.70
  and ip = 192.168.1.70 and
  output_name = "outstation1"
>

<id sign certificate request where ca_org = AnyLogDNP3CA and ca_output_name = "AnyLogDNP3CA"
  and server_org = "AnyLog DNP3 outstation" and output_name = "outstation1"
  and expiration_days = 3650
>

<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "AnyLog DNP3 outstation"
  and hostname = outstation2
  and alt_name = 192.168.1.71
  and ip = 192.168.1.71 and
  output_name = "outstation2"
>

<id sign certificate request where ca_org = AnyLogDNP3CA and ca_output_name = "AnyLogDNP3CA"
  and server_org = "AnyLog DNP3 outstation" and output_name = "outstation2"
  and expiration_days = 3650
>
```

Ship to each device owner (same CA public cert for both):

| Outstation | Ship |
|------------|------|
| `outstation1` | `outstation1.crt`, `outstation1.key`, `AnyLogDNP3CA.crt` |
| `outstation2` | `outstation2.crt`, `outstation2.key`, `AnyLogDNP3CA.crt` |

Do not ship `AnyLogDNP3CA.key`.

## Connect AnyLog with the written certificates

Use the certificate files under `!pem_dir` (typically `./data/pem`):

```anylog
<get dnp3 values where
    hostname = 192.168.1.70 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    enable_tls = true and
    tls_ca = !pem_dir/AnyLogDNP3CA.crt and
    tls_cert = !pem_dir/master1.crt and
    tls_key = !pem_dir/master1.key and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

Continuous ingest:

```anylog
<run plc client where type = dnp3 and
    hostname = 192.168.1.70 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    enable_tls = true and
    tls_ca = !pem_dir/AnyLogDNP3CA.crt and
    tls_cert = !pem_dir/master1.crt and
    tls_key = !pem_dir/master1.key and
    dbms = dnp3_db and
    table = dnp3_points and
    map = [{"name":"analog_0","type":"Analog","index":0},
           {"name":"binary_0","type":"Binary","index":0}]
>
```

All three of `tls_ca`, `tls_cert`, and `tls_key` are required when `enable_tls = true`.

## Make use of existing certificate files, coming from an outside organization

If an outside organization already provides the DNP3 TLS material, place those files under `!pem_dir` (or another path). Use distinct names (for example an `ext_` prefix) so they are not confused with certificates generated in the sections above:

| Role | Example files |
|------|----------------|
| Peer / CA | `ext_dnp3_ca.crt` |
| AnyLog DNP3 master (client) cert / key | `ext_master1.crt` / `ext_master1.key` |
| Outstation (server) cert / key | `ext_outstation1.crt` / `ext_outstation1.key` (and optionally `ext_outstation2.*`) |

```anylog
<get dnp3 values where
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    enable_tls = true and
    tls_ca = !pem_dir/ext_dnp3_ca.crt and
    tls_cert = !pem_dir/ext_master1.crt and
    tls_key = !pem_dir/ext_master1.key and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

To generate OpenSSL-only lab files for `opendnp3`, see [DNP3 TLS Test Certificates](./03-%20DNP3%20-%20TLS%20test%20certificates.md).

## Scenario: Master node + Operator with remote signing

Remote signing is **optional**. Use it when the CA private key must stay on the AnyLog **Master node**. Background:
[Optional: remote signing with a master](../../../06-%20Networking%20%26%20Security/07-%20Security/01-%20Built-in%20Authentication/01-%20Authentication.md#optional-remote-signing-with-a-master-certificate_authority).

**Operators do not get the CA private key** (`AnyLogDNP3CA.key`). Copy the CA **public** cert from the Master for `tls_ca`.

| Who | Gets |
|-----|------|
| Master | Keeps `AnyLogDNP3CA.key`; creates CA and signs CSRs |
| Operator | `master1.crt` / `master1.key` (remote sign) + copy of `AnyLogDNP3CA.crt` from Master |
| Device owner | `outstation*.crt` / `.key` and `AnyLogDNP3CA.crt` |

### Topology

| Node | IP:port (example) | Holds | Does |
|------|-------------------|--------|------|
| Master | `192.168.1.88:32048` | `AnyLogDNP3CA.key` | Creates CA; signs CSRs |
| Operator `op1` | `192.168.1.60` | `master1.key` | Creates CSR; remote-signs; runs DNP3 client |
| Outstation `outstation1` | `192.168.1.70:20001` | `outstation1.key` | TLS server for DNP3 |
| Outstation `outstation2` | `192.168.1.71:20001` | `outstation2.key` | Second TLS outstation (same CA) |

### On the Master — create CA once

```anylog
<id generate certificate authority where country = US and
  state = CA and locality = "Redwood City" and
  org = AnyLogDNP3CA and
  output_name = "AnyLogDNP3CA" and
  expiration_days = 3650
>
```

Keep `AnyLogDNP3CA.key` on the Master only.

Create and sign the outstation certificates on the Master (local sign) — required when you use this CA for DNP3 TLS — then ship to each **device owner**: `outstation*.crt` / `.key` and `AnyLogDNP3CA.crt`. Do not ship `AnyLogDNP3CA.key`.

```anylog
<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "AnyLog DNP3 outstation"
  and hostname = outstation1
  and alt_name = 192.168.1.70
  and ip = 192.168.1.70 and
  output_name = "outstation1"
>

<id sign certificate request where ca_org = AnyLogDNP3CA and ca_output_name = "AnyLogDNP3CA"
  and server_org = "AnyLog DNP3 outstation" and output_name = "outstation1"
  and expiration_days = 3650
>

<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "AnyLog DNP3 outstation"
  and hostname = outstation2
  and alt_name = 192.168.1.71
  and ip = 192.168.1.71 and
  output_name = "outstation2"
>

<id sign certificate request where ca_org = AnyLogDNP3CA and ca_output_name = "AnyLogDNP3CA"
  and server_org = "AnyLog DNP3 outstation" and output_name = "outstation2"
  and expiration_days = 3650
>
```

### On the Operator — CSR + remote sign

```anylog
set master_node = 192.168.1.88:32048

<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "AnyLog DNP3 master"
  and hostname = master1
  and alt_name = 192.168.1.60
  and ip = 192.168.1.60 and
  output_name = "master1"
>

<id sign certificate request where ca_org = AnyLogDNP3CA and ca_output_name = "AnyLogDNP3CA"
  and server_org = "AnyLog DNP3 master" and output_name = "master1"
  and expiration_days = 3650
  and certificate_authority = !master_node
>
```

Result on the Operator: `master1.crt` under `!pem_dir` (with `.csr` / `.key` / `.pem`). The Operator never receives `AnyLogDNP3CA.key`.

### On the Operator — copy CA public cert from Master

Copy `AnyLogDNP3CA.crt` from the Master's `!pem_dir` into the Operator's `!pem_dir` (for `tls_ca`). Do not copy `AnyLogDNP3CA.key`.

### On the Operator — run DNP3 over TLS

```anylog
<run plc client where type = dnp3 and
    hostname = 192.168.1.70 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    enable_tls = true and
    tls_ca = !pem_dir/AnyLogDNP3CA.crt and
    tls_cert = !pem_dir/master1.crt and
    tls_key = !pem_dir/master1.key and
    dbms = dnp3_db and
    table = dnp3_points and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

Additional Operators repeat the CSR + remote-sign steps with their own `output_name` (for example `master2`) and IP in `alt_name` / `ip`, and copy `AnyLogDNP3CA.crt` from the Master the same way.

## Related

* [DNP3](../05-%20DNP3.md)
* [DNP3 TLS Test Certificates](./03-%20DNP3%20-%20TLS%20test%20certificates.md) — OpenSSL lab chain for `opendnp3`
* [Authentication — optional remote master signing](../../../06-%20Networking%20%26%20Security/07-%20Security/01-%20Built-in%20Authentication/01-%20Authentication.md#optional-remote-signing-with-a-master-certificate_authority)
* [Broker Setup TLS Example](../../../06-%20Networking%20%26%20Security/05-3%20Broker%20Setup%20TLS%20Example.md) — same certificate patterns for MQTT
