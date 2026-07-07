---
title: Policies & Metadata
description: Understand AnyLog's policy-based metadata layer — how policies are structured, created, queried, and used to configure the network.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 


AnyLog uses a **policy-based metadata layer** stored on a blockchain or master node. Policies are JSON objects that describe nodes, clusters, data schemas, configuration rules, and more. Every node in the network maintains a local copy of the relevant policies and uses them to route data, resolve queries, and enforce configuration.

---

## What is a policy?

A policy is a JSON structure with a single root key — the **policy type**. The type determines how AnyLog interprets and uses the policy.

```json
{
  "operator": {
    "name": "my-operator",
    "ip": "172.233.208.212",
    "port": 32048,
    "rest_port": 32049,
    "company": "my-company",
    "cluster": "06f093559c851c6d4c3e950ebc9c5499",
    "id": "d93487bec012c8847bca734bcc31a3a6",
    "date": "2024-01-01T00:00:00Z",
    "ledger": "global"
  }
}
```

When a policy is published to the blockchain, AnyLog automatically adds:
- `id` — a unique identifier
- `date` — timestamp of creation
- `ledger` — scope (`global` or `local`)

---

## Core policy types

| Policy type | Purpose |
|---|---|
| `master` | Identifies a master node and its connection details |
| `operator` | Identifies an Operator node, its cluster membership, and ports |
| `publisher` | Identifies a Publisher node |
| `query` | Identifies a Query node |
| `cluster` | Groups Operators that host the same data (HA replication unit) |
| `table` | Associates a table with a cluster and defines its schema |
| `mapping` | Maps incoming JSON data fields to database table columns |
| `config` | Configuration policy — commands executed when a node starts |
| `distribution` | Routes data from specific Publishers to specific Operators |
| `schedule` | Defines a scheduled task to run on a node |

---

## Blockchain commands

### Add a policy

```anylog
blockchain insert where policy = [json-policy] and local = true and master = !master_node
```

Or using the two-step prepare/push flow:
```anylog
blockchain prepare policy !my_policy
run client (!master_node) blockchain push !my_policy
```

### Query policies

```anylog
blockchain get [policy-type]
blockchain get operator
blockchain get operator where [key] = [value]
blockchain get cluster where company = my-company
```

With formatting:
```anylog
blockchain get operator bring [name] [ip] [port]
blockchain get operator bring.table [name][ip][port]
blockchain get operator bring.json
```

### Delete a policy

```anylog
blockchain drop policy where id = [policy-id]
```

### Validate the local blockchain file

```anylog
blockchain test
```

### Sync with the network

```anylog
run blockchain sync                          # force immediate sync
get synchronizer                             # sync status
get metadata version                         # current metadata version ID
```

---

## Node policies

### Operator policy

An Operator policy identifies the node, its ports, and its cluster membership. Every Operator node must have a published policy to receive data and be discoverable.

```json
{
  "operator": {
    "hostname": "operator1",
    "name": "cluster1-operator1",
    "ip": "155.248.209.193",
    "local_ip": "10.0.0.173",
    "company": "my-company",
    "port": 32148,
    "rest_port": 32149,
    "cluster": "06f093559c851c6d4c3e950ebc9c5499",
    "country": "US",
    "state": "California",
    "city": "San Jose"
  }
}
```

### Cluster policy

Groups one or more Operators that replicate the same data. A cluster policy is referenced by the `cluster` key in Operator policies.

```json
{
  "cluster": {
    "company": "my-company",
    "dbms": "my_data",
    "name": "cluster1",
    "status": "active"
  }
}
```

---

## Configuration policies

A `config` policy stores a script of AnyLog commands that are executed when a node starts. This allows node configuration to be managed centrally on the blockchain rather than locally on each node.

```json
{
  "config": {
    "name": "operator-config",
    "node_name": "my-operator",
    "script": [
      "connect dbms my_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432",
      "run operator where policy = !operator_policy and create_table = true and update_tsd_info = true and threads = 3"
    ]
  }
}
```

Execute a configuration policy by ID:
```anylog
policy [policy-id]
```

---

## Mapping policies

Mapping policies define how incoming JSON data is transformed into database rows. They are referenced by the Operator when processing files in the watch directory.

```json
{
  "mapping": {
    "name": "sensor-mapping",
    "dbms": "my_data",
    "table": "ping_sensor",
    "schema": {
      "timestamp": {"type": "timestamp", "bring": "[timestamp]"},
      "device_name": {"type": "string", "bring": "[device]"},
      "value": {"type": "float", "bring": "[reading]"}
    }
  }
}
```

See 
<a href="{{ '/docs/Network-Services/Managing-Data-Southbound/data-ingestion/#Using-a-mapping-policy' | relative_url }}">Data Southbound — Mapping</a> 
for full mapping configuration.

---

## Metadata management

### Local blockchain file

Each node maintains a local JSON file containing the metadata relevant to its operation. The path is stored in the 
dictionary:

```anylog
get !blockchain_file        # path to local blockchain file
blockchain test             # validate structure of the local file
```

### Pull metadata from a peer

When a new node starts, it can sync the metadata from any existing network member:

```anylog
blockchain pull to json [ip:port]
```

### Copy the blockchain file

```anylog
file copy [source-path] !blockchain_file
```

---

## Querying metadata

### Find Operators supporting a table

```anylog
blockchain get operator bring.ip_port
blockchain get operator where [dbms] = my_data bring [name] [ip] [port]
```

### Find nodes by location

```anylog
blockchain get operator where [country] = US bring.ip_port
blockchain get operator where [city] = "San Jose" bring [name] [ip]
```

### Use metadata in commands

```anylog
run client (blockchain get operator bring.ip_port) get status
run client (operator where [country] contains US bring.ip_port, subset = true) get status
```

The `subset = true` flag allows the command to proceed even if some nodes are unresponsive.

---

## The bring directive

`bring` extracts specific fields from policy JSON to format command output or construct destination lists:

```anylog
blockchain get operator bring [name]             # returns just the name field
blockchain get operator bring [name] [ip]:[port] # concatenates name + ip:port
blockchain get operator bring.ip_port            # standard IP:Port list
blockchain get operator bring.table              # tabular output
blockchain get operator bring.json               # JSON output
```

The `from` command applies bring-style extraction to a variable:
```anylog
operators = blockchain get operator
from !operators bring [name] [ip]:[port]
```