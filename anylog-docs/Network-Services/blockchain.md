---
title: Blockchain & Metadata
description: Use AnyLog's blockchain commands to manage the distributed metadata ledger — adding, querying, updating, and syncing policies.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks
--> 

AnyLog maintains a distributed metadata ledger using either a **master node** (a simple AnyLog node hosting the ledger in a local database) or a **blockchain platform** (e.g. Optimism, Ethereum). Every node maintains a local copy of the relevant metadata and uses it to route data, resolve queries, and enforce configuration — without depending on the availability of the global ledger at runtime.

The metadata is organized as **policies** — JSON objects with a single root key (the policy type). 
See <a href="{{ '/docs/Network-Services/policies-metadata/' | relative_url }}">Policies & Metadata</a> for policy types 
and structure.

---

## Metadata storage

Each node stores metadata in up to three locations:

| Location | Purpose |
|---|---|
| **Local JSON file** | Primary working copy used by the node at runtime |
| **Local database** | Optional; used by master nodes and for offline analysis |
| **Global ledger** | Blockchain platform or master node — the source of truth |

```anylog
get !blockchain_file          # path to the local JSON file
blockchain test               # validate the local file structure
```

---

## Master node vs blockchain platform

| | Master node | Blockchain platform |
|---|---|---|
| Setup complexity | Low | Higher (requires contract) |
| Decentralisation | No (single point) | Yes |
| Latency | Low | Higher (block confirmation) |
| Recommended for | Dev, small deployments | Production, multi-org |

A node operates identically regardless of which global ledger is used. The difference is only in the sync configuration.

---

## Connecting to a blockchain platform

Using a blockchain platform requires a deployed AnyLog contract. Connect to the platform before issuing any blockchain commands:

```anylog
<blockchain connect to ethereum where
  provider = "https://rinkeby.infura.io/v3/[your-key]" and
  contract = "[contract-address]" and
  private_key = "[your-private-key]" and
  public_key = "[your-public-key]" and
  gas_read = 2000000 and
  gas_write = 3000000>
```

Verify the connection:
```anylog
get platforms
```

---

## Blockchain sync

Every non-master node should run the blockchain sync service to keep its local copy up to date. See <a href="{{ '/docs/Network-Services/background-services/#blockchain-sync-service' | relative_url }}">Background Services — Blockchain sync</a> for full options.

### Sync with a master node
```anylog
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node
```

### Sync with a blockchain platform
```anylog
run blockchain sync where source = blockchain and platform = ethereum and time = 30 seconds and dest = file
```

### Force an immediate sync
```anylog
run blockchain sync
```

### Monitor sync status
```anylog
get synchronizer
get metadata version
```

### Switch master node at runtime
```anylog
blockchain switch network where master = [IP:Port]
```

---

## Seeding a new node

When a node starts for the first time, pull the current metadata from any existing network member:

```anylog
blockchain seed from [ip:port]
```

This syncs the local JSON file and makes the node immediately aware of all peers, clusters, and policies.

---

## Adding policies

### blockchain insert (recommended)

Updates both the local copy and the global ledger atomically. The policy is immediately available locally, and will be pushed to the global ledger when connectivity allows.

```anylog
blockchain insert where policy = [policy] and local = true and master = !master_node
blockchain insert where policy = [policy] and local = true and blockchain = ethereum
```

| Key | Description |
|---|---|
| `policy` | The JSON policy to add |
| `local` | `true` — also update the local JSON file |
| `master` | IP:Port of the master node |
| `blockchain` | Blockchain platform name (e.g. `ethereum`) |

When inserted locally, the policy gets `"ledger": "local"`. Once confirmed on the global ledger, it changes to `"ledger": "global"`.

### Two-step prepare / push

```anylog
blockchain prepare policy !my_policy          # add ID and date fields
run client (!master_node) blockchain push !my_policy
```

Wait for the update to be confirmed on the local copy:
```anylog
is_updated = blockchain wait for !my_policy
```

### Other insert commands

| Command | Target |
|---|---|
| `blockchain add [policy]` | Local JSON file only |
| `blockchain push [policy]` | Local database only |
| `blockchain commit [policy]` | Blockchain platform only |

---

## Querying policies

Queries run against the **local copy** and do not depend on global ledger availability.

### Basic get

```anylog
blockchain get [policy-type]
blockchain get operator
blockchain get (operator, publisher)       # multiple types
blockchain get *                           # all policies
```

### Where conditions

```anylog
blockchain get operator where dbms = my_data
blockchain get operator where dbms = my_data and ip = 24.23.250.144
blockchain get cluster where company = my-company
```

Using conditional expressions (square-bracket paths):
```anylog
blockchain get operator where [name] == operator1 or [name] == operator2
blockchain get operator where [country] == US and ([city] == "San Francisco" or [city] == "San Jose")
```

Special path operators:
```anylog
blockchain get tag where [path] startwith 'Root/Objects/DeviceSet'
blockchain get tag where [path] childfrom 'Root/Objects/DeviceSet'
```

### bring — format the output

```anylog
blockchain get operator bring [name]                        # single field
blockchain get operator bring [name] [ip]:[port]            # concatenate fields
blockchain get operator bring.ip_port                       # standard IP:Port list
blockchain get operator bring.table                         # tabular output
blockchain get operator bring.json                          # JSON output
blockchain get operator bring.table.sort [operator][name]   # sorted table
```

### from — apply bring to a variable

```anylog
operators = blockchain get operator
from !operators bring [name] [ip]:[port]
```

### Examples

```anylog
# All operators supporting a specific table
blockchain get operator where dbms = my_data and table = ping_sensor bring [name] [ip]:[port]

# Operators in specific countries
blockchain get operator where [country] == US or [country] == UK bring.ip_port

# Cluster ID for a specific table
blockchain get cluster where table[dbms] = my_data and table[name] = ping_sensor bring [cluster][id] separator = ,
```

---

## blockchain read vs blockchain get

| Command | Description |
|---|---|
| `blockchain get` | Returns policies after runtime dynamic updates (use this normally) |
| `blockchain read` | Returns policies exactly as received from the global ledger, without dynamic updates |

---

## Join and merge

Combine results from two policy queries.

### JOIN — keep both objects separate

```anylog
blockchain get bucket where name = my_bucket join (blockchain get operator where name = [bucket][operator])
```

Output:
```json
[{"bucket": {...}, "operator": {...}}]
```

- If no RHS match → record is omitted (inner join behaviour)
- Path interpolation: `[bucket][operator]` is resolved from the LHS record

### MERGE — flatten RHS into LHS

```anylog
blockchain get bucket where name = my_bucket merge (blockchain get operator where name = [bucket][operator])
```

Output:
```json
[{"bucket": {"name": "my_bucket", "operator": "op1", "ip": "24.5.219.50", "port": 7848}}]
```

- LHS wins on key conflicts
- If no RHS match → LHS returned unchanged (left merge behaviour)

### With bring formatting

```anylog
# Table output with join
blockchain get bucket where name = my_bucket join (blockchain get operator where name = [bucket][operator]) bring.table [bucket][name] [operator][ip] [operator][port]

# JSON output with merge
blockchain get bucket where name = my_bucket merge (blockchain get operator where name = [bucket][operator]) bring.json [bucket][name] [bucket][ip] [bucket][port]
```

---

## Root and child policies (UNS hierarchy)

Root policies have no `parent` attribute. Child policies reference a parent via the `parent` field, forming a hierarchy used by the Unified Namespace (UNS).

```anylog
blockchain get root policies
```

Example output:
```json
[
  {"uns": {"name": "Enterprise_A", "namespace": "Enterprise_A", "id": "00ddf..."}},
  {"uns": {"name": "Sensors", "namespace": "Enterprise_A/Sensors", "parent": "00ddf...", "dbms": "my_data", "table": "ping_sensor"}}
]
```

Child policies inherit structure from their parent and carry `dbms`/`table` attributes used by the query engine.

---

## Using policies as command destinations

A common pattern is to use a `blockchain get` result as the target of a `run client` command:

```anylog
run client (blockchain get operator bring.ip_port) get status

run client (blockchain get operator where [country] == US bring.ip_port, subset = true) get rows count

destinations = blockchain get (operator, query) where [country] == US or [country] == UK bring [*][ip]:[*][port] separator = ,
run client (!destinations) get node info cpu_percent
```

`subset = true` allows the command to proceed even if some nodes are unresponsive.

---

## Updating policies

```anylog
blockchain update where policy = [updated-policy] and id = [policy-id] and local = true and master = !master_node
blockchain update to ethereum [policy_id] [policy]
```

The policy ID must pre-exist. AnyLog validates structure and updates the timestamp.

---

## Deleting policies

```anylog
# By ID
blockchain delete policy where id = [policy-id] and master = !master_node
blockchain delete policy where id = b90b40ff46ea7244a49357a46901e114, 4a0c16ff565c6dfc05eb5a1aca4bf825

# Using a blockchain get to identify targets
blockchain delete policy where id = blockchain get operator where [company] == ibm bring [*][id] separator = ,

# By policy data
blockchain drop policy !my_operator

# From local database only
blockchain drop policy where id = [id]
blockchain drop by host [ip]
```

---

## Local database operations

Master nodes and optionally any node can maintain the ledger in a local database:

```anylog
blockchain create table                           # create the ledger table
blockchain pull to json [output-file]             # export to JSON file
blockchain pull to sql [output-file]              # export as INSERT statements
blockchain pull to stdout                         # print to console
blockchain update dbms [file]                     # load file into local DB
sql blockchain "select * from ledger"             # query directly with SQL
```

### Pull from a master node

```anylog
master_node = 127.45.35.12:32048
run client (!master_node) blockchain pull to json
run client (!master_node) file get !!blockchain_file !blockchain_file
blockchain load metadata                          # force node to use updated file
```

---

## Other blockchain commands

| Command | Description |
|---|---|
| `blockchain test` | Validate local JSON file structure |
| `blockchain test id` | Check if a policy ID exists locally |
| `blockchain get id [json]` | Return the hash of a JSON structure |
| `blockchain prepare policy [json]` | Add ID and date to a policy |
| `blockchain checkout` | Pull latest data from blockchain platform to local JSON |
| `blockchain update file [path]` | Replace local blockchain file (backs up `.old`) |
| `blockchain delete local file` | Delete the local JSON file |
| `blockchain query metadata` | Diagram view of the local metadata structure |
| `blockchain test cluster` | Analyse cluster policies |
| `blockchain state where platform = [name]` | State of the active contract |