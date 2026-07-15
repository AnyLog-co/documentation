---
title: "DNP3 Mapping Policies — Reusing a Schema Across Connections"
description: Storing a DNP3 point map once as a blockchain policy and reusing it across multiple connections, instead of repeating the map JSON inline
layout: page
source_path: "DNP3-Mapping-Policies.md"
---

<!--
## Changelog
- 2026-07-14 | Created document — extends DNP3.md, which documents `map` only as a literal inline JSON array, to
              cover the policy-based reuse pattern used in production deployment scripts
-->

# DNP3 Mapping Policies — Reusing a Schema Across Connections

[DNP3](DNP3.md) documents `map` as a JSON array supplied directly in the `get plc values` / `run plc client`
command — every example on that page writes the point list out in full, inline. That's the right approach for a
single connection, or for testing. For a deployment with several outstations that share the same, or nearly the
same, point layout — several substations of the same model, for instance — repeating an identical `map` array in
every connection command means the same schema has to be kept in sync by hand in multiple places.

The alternative: declare the point map once as a policy on the blockchain, and have each connection look it up
by name instead of restating it.

## The `dnp3` policy type

The policy has one required shape:

```json
{
    "dnp3": {
        "namespace": "FACTORY4/DNP3/SUBSTATION",
        "name": "plant1",
        "schema": [
            {"name":"analog_0","type":"Analog","index":0},
            {"name":"binary_0","type":"Binary","index":0},
            {"name":"analog_output_status_0","type":"AnalogOutputStatus","index":0},
            {"name":"binary_output_status_0","type":"BinaryOutputStatus","index":0}
        ]
    }
}
```

- `namespace` + `name` together identify the policy — this pair is the lookup key, and not coincidentally, it's
  the same `namespace`/`name` pair used when registering the connection in the UNS (see
  [DNP3 — Dynamic ingest with UNS](DNP3.md#dynamic-ingest-with-uns-namespace--master_node)). Using the same
  values for both isn't required by the platform, but it keeps one connection's identity, UNS registration, and
  mapping policy all pointing at the same pair of values instead of three independently-tracked names.
- `schema` is exactly the same array documented as `map` in
  [DNP3 — Connection and map](DNP3.md#connection-and-map) — the same `name`/`type`/`index` (or
  `group`/`variation`) objects, just stored as policy data instead of typed inline.

## Looking up an existing policy

```anylog
is_dnp3 = blockchain get dnp3 where namespace = !base_namespace and name = !dnp_name
dnp_schema = from !is_dnp3 bring [*][schema]
```

`!dnp_schema` now holds the same JSON array that `map` expects, pulled from whichever policy already matches this
`namespace`/`name` pair — whether that policy was published by this exact connection previously, or by an
earlier, identical outstation deployment reusing the same namespace/name convention.

## Publishing a new policy

If no matching policy exists yet, build one and insert it — following the same
[sign → insert](../../05-%20Networking%20&%20Security/Built-in%20Authentication/Authentication.md#signing-a-policy)
pattern used for any other policy type:

```anylog
<new_policy={
    "dnp3": {
        "namespace": !base_namespace,
        "name": !dnp_name,
        "schema": [
          {"name":"analog_0","type":"Analog","index":0},
          {"name":"binary_0","type":"Binary","index":0}
        ]
    }
}>
blockchain insert where policy = !new_policy and local = true and master = !ledger_conn
```

(A full deployment script wraps this with signing and error handling — see
[Deploying a DNP3 Connector via Script](Deploying%20a%20DNP3%20Connector%20via%20Script.md#prep-policy--build-a-new-mapping-policy)
for the complete pattern, including the check-then-create flow that avoids republishing an identical policy on
every run.)

## Using the resolved schema

Whether `!dnp_schema` came from an existing policy or was just published, it's used exactly where `map` appears
in the standard `run plc client` command:

```anylog
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
    map = !dnp_schema
>
```

This is identical to every other `run plc client` example in [DNP3](DNP3.md) — the only difference is that `map`
is populated from a variable resolved via a policy lookup, rather than written out as a literal array in the
command itself.

## How this differs from a "mapping policy"

AnyLog also has a generic **mapping policy** type, covered in
[Mapping data to tables](../southbound-overview.md#mapping-policy), used for REST/MQTT ingestion — those policies
describe a `bring`-based extraction schema (`{"type": "float", "bring": "[reading]"}`) for pulling fields out of
an arbitrary incoming JSON payload. The `dnp3` policy type here is a different, protocol-specific shape: it
describes DNP3 point addresses (`type`/`index`, or `group`/`variation`) on an outstation, not a JSON-payload
extraction rule. The two aren't interchangeable, and a `dnp3` policy isn't referenced via the generic `mapping`
keyword — it's looked up directly with `blockchain get dnp3 where ...`, as shown above.

## Why bother — the actual benefit

With several outstations sharing a `dnp3` policy (by using the same `namespace`/`name` convention across
deployments of otherwise-identical equipment):

- The point schema is edited in exactly one place — updating the policy — rather than in every deployment
  script that connects to a matching outstation.
- New deployments of the same equipment type look the schema up instead of needing it re-specified, reducing the
  chance of a typo or drift between two supposedly-identical connections.
- The schema itself becomes queryable and auditable via the blockchain, the same as any other policy, rather
  than living only inside script files.

The tradeoff is a layer of indirection: reading a deployment script alone (without also checking the published
policy) won't tell you the actual point map in use. For a one-off connection or a quick test, the inline `map`
array shown throughout [DNP3](DNP3.md) remains simpler.

## See also

- [DNP3](DNP3.md) — the underlying `get plc values`/`run plc client` command reference
- [Deploying a DNP3 Connector via Script](Deploying%20a%20DNP3%20Connector%20via%20Script.md) — a full deployment
  script using this pattern, with TLS branching and error handling