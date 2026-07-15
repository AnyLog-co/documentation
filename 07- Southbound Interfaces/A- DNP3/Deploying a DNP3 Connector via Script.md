---
title: "Deploying a DNP3 Connector via Script"
description: Walking through a production-style .al deployment script for a DNP3 southbound connection — parameters, policy reuse, TLS branching, and error handling
layout: page
source_path: "Deploying a DNP3 Connector via Script.md"
---

<!--
## Changelog
- 2026-07-14 | Created document, based on a sample deployment script (dnp3_connector.al)
-->

# Deploying a DNP3 Connector via Script

[DNP3](DNP3.md) documents the `get plc values` / `run plc client` commands directly — typed once on the CLI, or
pasted into a one-off script, with the point `map` written out as a literal JSON array each time. For a
production deployment, it's more common to run DNP3 connections from a standing `.al` script that a node
executes on startup (or on demand), with parameters set at the top and the point map itself stored once as a
reusable blockchain policy rather than duplicated in every script. This page walks through that pattern using a
sample script, `dnp3_connector.al`.

For the reusable-mapping-policy pattern itself (the `dnp3` policy type this script checks for and creates), see
[DNP3 Mapping Policies — Reusing a Schema Across Connections](DNP3-Mapping-Policies.md).

Run the script with:

```anylog
process !local_scripts/southbound-industrial/dnp3_connector.al
```

(adjust the path to wherever the script actually lives in your deployment).

---

## Script structure

The script is organized as a sequence of labels, executed with `goto`/fall-through, rather than top-to-bottom —
this lets it branch (e.g. TLS vs. plain TCP) and handle errors from a shared sub-script without duplicating
logic.

### `:set-params:` — connection and identity

```anylog
on error ignore
:set-params:
client_type=dnp3
dnp_ip = 192.168.1.88
dnp_port = 20001
dnp_master_id = 1
outstation_id  = 10
dnp_frequency = 20
dnp_name = plant1
base_namespace = "FACTORY4/DNP3/SUBSTATION"

# authentication configs
set enable_tls = false

# !anylog_dir is accessible as a volume and used to store certifications and access points.
# we can also store the public information on the blockchain so there's no need for persistence of content
tls_ca = !anylog_dir/dnp3_certs/factory_ca.cert
tls_cert = !anylog_dir/dnp3_certs/master1.cert
tls_key = !anylog_dir/dnp3_certs/master1.key
```

Everything a given deployment needs to change — target outstation, link IDs, poll frequency, the UNS namespace
this connection is registered under, and whether TLS is used — is set once here. `dnp_name` and
`base_namespace` together are also the key used to look up (or create) the reusable mapping policy in the next
step, so they double as the identity of this particular DNP3 connection, not just a display label.

Note on TLS paths: `!anylog_dir` is a volume mounted into the AnyLog container, used here to hold certificate
files locally on the node. The comment in the script also flags an alternative worth knowing about — the
*public* half of a certificate can instead be stored on the blockchain as part of a policy, avoiding the need to
persist certificate files on every node that needs them. This script uses the local-file approach; see
[DNP3 TLS Test Certificates](../../05-%20Networking%20&%20Security/DNP3-tls-test-certificates.md) for generating
a chain to use with `tls_ca`/`tls_cert`/`tls_key`.

### `:check-policy:` — look for an existing mapping policy

```anylog
:check-policy:
is_dnp3 = blockchain get dnp3 where namespace = !base_namespace and name=!dnp_name
if not !is_dnp3 then goto prep-policy

dnp_schema = from !is_dnp3 bring [*][schema]

goto declare-dnp3
```

If a `dnp3` policy already exists for this `namespace`/`name` pair, its `schema` (the point map) is pulled out
into `!dnp_schema` and the script jumps straight to declaring the connection. If not, it falls through to
`:prep-policy:` to create one.

### `:prep-policy:` — build a new mapping policy

```anylog
:prep-policy:
<new_policy={
    "dnp3": {
        "namespace": !base_namespace,
        "name": !dnp_name,
        "schema": [
          {"name":"analog_0","type":"Analog","index":0},
          {"name":"binary_0","type":"Binary","index":0},
          {"name":"analog_output_status_0","type":"AnalogOutputStatus","index":0},
          {"name":"binary_output_status_0","type":"BinaryOutputStatus","index":0}
        ]
    }
}>
```

This is the point map — the same shape documented as the `map` array in [DNP3](DNP3.md#connection-and-map) —
but declared once, as data, rather than repeated inline in every `run plc client` call.

### `:publish-policy:` — sign and insert the policy

```anylog
:publish-policy:
process !local_scripts/node-deployment/policies/publish_policy.al
if not !error_code.int then
do set create_policy = true
goto check-policy

if !error_code == 1 then goto sign-policy-error
else if !error_code == 2 then goto prepare-policy-error
else if !error_code == 3 then goto declare-policy-error
```

This delegates to a shared helper script (`publish_policy.al`) that signs `!new_policy` and inserts it onto the
blockchain — the same helper any connector's deployment script would call, not something DNP3-specific. On
success, the script loops back to `:check-policy:`, which will now find the freshly published policy and pick up
`!dnp_schema` from it. A nonzero `!error_code` routes to one of three error labels depending on which stage
failed (signing, preparing, or declaring the policy) — see [Error handling](#error-handling) below.

### `:declare-dnp3:` / `:declare-dnp3-tls:` — start the connection

```anylog
:declare-dnp3:
on error goto declare-dnp3-err
if !enable_tls == true goto declare-dnp3-tls
<run plc client where type = dnp3 and
    hostname = !dnp_ip and
    port = !dnp_port and
    master_id = !dnp_master_id and
    outstation_id = !outstation_id and
    frequency = !dnp_frequency and
    name = !dnp_name and
    dbms = !default_dbms and
    dynamic = true and
    namespace = !base_namespace and
    master_node = !ledger_conn and
    map =  !dnp_schema
>
goto end-script

:declare-dnp3-tls:
<run plc client where type = dnp3 and
    hostname = !dnp_ip and
    port = !dnp_port and
    master_id = !dnp_master_id and
    outstation_id = !outstation_id and
    frequency = !dnp_frequency and
    name = !dnp_name and
    dbms = !default_dbms and
    dynamic = true and
    namespace = !base_namespace and
    master_node = !ledger_conn and
    map =  !dnp_schema and
    enable_tls = true and
    tls_ca = !tls_ca and
    tls_cert = !tls_cert and
    tls_key = !tls_key
>
```

Both branches are the same `run plc client where type = dnp3 ...` call documented in
[DNP3 — Dynamic ingest with UNS](DNP3.md#dynamic-ingest-with-uns-namespace--master_node); the only difference is
whether the four `enable_tls`/`tls_*` keywords are included. `!dnp_schema` (from either `:check-policy:` or
`:prep-policy:` → `:publish-policy:` → `:check-policy:`) supplies `map`, and `!base_namespace` /
`!dnp_name` supply `namespace` — so the UNS registration and the policy lookup key are the same values,
by design.

### Error handling

```anylog
:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign mapping policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare mapping policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare mapping policy on blockchain"
goto terminate-scripts

:declare-dnp3-err:
print "Failed to define connection to DNP3 against" + !dnp_ip + ":" + !dnp_port
goto terminate-scripts
```

Each failure path prints a specific message identifying which stage failed (signing, preparing, or declaring the
policy; or establishing the DNP3 connection itself) before terminating the script — useful for diagnosing a
failed deployment from logs without needing to instrument the script further.

---

## Adapting this for your own deployment

At minimum, change in `:set-params:`:

- `dnp_ip`, `dnp_port`, `dnp_master_id`, `outstation_id` — to match your actual outstation.
- `dnp_name`, `base_namespace` — pick values that uniquely identify this connection; these double as the lookup
  key for the reusable mapping policy.
- The `schema` array in `:prep-policy:` — to match the actual points on your outstation (see
  [DNP3 — Connection and map](DNP3.md#connection-and-map) for the supported `type` values).
- `enable_tls` and the three `tls_*` paths, if using TLS.

If you're deploying several identical or near-identical outstations (for example, several substations with the
same point layout), give them the same `base_namespace`/`dnp_name` pattern deliberately, so later deployments hit
the `:check-policy:` fast path and reuse the schema already published by the first one, rather than re-declaring
it. See [DNP3 Mapping Policies](DNP3-Mapping-Policies.md) for more on this reuse pattern.