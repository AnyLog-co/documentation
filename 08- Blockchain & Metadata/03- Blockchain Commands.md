---
title: "Blockchain Commands"
description: "Full command reference for managing AnyLog policies — connecting/syncing, publishing/dropping policies, and querying the blockchain."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | Removed a duplicated "help blockchain set account info" block; fixed `blockchain deploy contract` example to match its own Usage line; condensed `help` transcripts into command+description style; flagged several open questions between this reference and other docs (see inline notes): `run blockchain sync`'s `connection` vs `master_node` param, `dest` specified twice in one call, `blockchain wait for` vs `blockchain wait where`, and whether the `where`-style `blockchain update` form still exists; restored the narrower `add`/`push`/`commit` insert-variant table; typo fixes | |
 | 2026-07-27 | Ori Shadmon    | New page — split out of "03 Blockchain & Metadata.md". Moved the master-vs-blockchain-platform comparison and all connect/sync/seed commands to the new standalone Blockchain Connectivity doc, since those are about wiring a node to a ledger source rather than managing policies once connected. Fixed `master_npode` typo. | |
--->

In general the blockchain or metadata layer is the platform that informs all the nodes in the network where data resides
and which nodes have access to what. The [previous section](02-%20Policy%20&%20Metadata.md) discussed the different types
of policies and metadata content that can be stored in the blockchain. This section covers how to interact with the
blockchain layer.

* [Connect & Sync](#connect--sync)
* [Publish & Drop Policy](#publish--drop-policy)
* [Query the Blockchain](#query-the-blockchain)

## Connect & Sync

### Real Blockchain

`blockchain set account info where platform = [platform name] and [platform parameters]` - associate parameters
(private key, public key, chain ID, etc.) with a blockchain platform.

```anylog
<blockchain set account info where 
    platform = ethereum and 
    private_key = !private_key and 
    public_key = !public_key and 
    chain_id = 11155111>
```

`blockchain deploy contract where platform = [platform name] and public_key = [public key]` - deploy the AnyLog
contract on the blockchain platform.

```anylog
blockchain deploy contract where platform = ethereum and public_key = !public_key
```

> A metadata manager (i.e. master node) does not need to define the steps above. Instead, it creates a logical
> database and table (`blockchain.ledger`) and syncs the content against it.

### Master / Metadata Node Blockchain

Master nodes, and optionally any node, can maintain the ledger in a local database:

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

### Blockchain sync

`blockchain seed from [ip:port]` - pull the metadata from a source node (typically used once, on startup).

```anylog
blockchain seed from 73.202.142.172:7848
```

`run blockchain sync where [options]` - repeatedly update the local copy of the blockchain.

| Option | Description |
|---|---|
| `source` | The source of the metadata (`blockchain` or `master`) |
| `dest` | Destination for the blockchain data — `file` (local file) and/or `dbms` (local database) |
| `connection` | Connection info needed to retrieve the data — for a master, its IP:Port |
| `time` | Frequency of updates |

```anylog
run blockchain sync where source = master and time = 60 seconds and dest = file and dest = dbms and connection = !ip_port
run blockchain sync where source = blockchain and time = !sync_time and dest = file and platform = ethereum
```

> The sync logic should run on every node in the network (though frequency may differ based on node type).

---

## Publish & Drop Policy

`blockchain prepare policy [policy]` - add `id` and `date` attributes to a policy.

```anylog
blockchain prepare policy !operator
```

`blockchain insert where policy = [policy] and blockchain = [platform] and local = [true/false] and master = [IP:Port]` -
add a JSON policy to the specified destination(s).

```anylog
blockchain insert where policy = !policy and local = true and master = !ledger_conn
blockchain insert where policy = !policy and local = true and blockchain = ethereum
```

| Key | Description |
|---|---|
| `policy` | The JSON policy to add |
| `local` | `true` — also update the local JSON file |
| `master` | IP:Port of the master node |
| `blockchain` | Blockchain platform name (e.g. `ethereum`) |

When inserted locally, the policy gets `"ledger": "local"`. Once confirmed on the global ledger, it changes to `"ledger": "global"`.

### Narrower insert variants

| Command | Target |
|---|---|
| `blockchain add [policy]` | Local JSON file only |
| `blockchain push [policy]` | Local database only |
| `blockchain commit [policy]` | Blockchain platform only |

`blockchain wait where [condition]` - pause the process until the local copy of the blockchain is updated with the
policy. `[condition]` is specified as `[key] = [value]`.

```anylog
blockchain wait where policy = !operator
blockchain wait where id = [id]
blockchain wait where command = "blockchain get cluster where name = cluster_1"
```

`blockchain update to [blockchain name] [policy_id] [policy]` - update an existing JSON policy on the blockchain platform.

```anylog
blockchain update to ethereum !policy_id !policy
```

`blockchain drop policy where id = [policy id]` / `blockchain drop policy [policy]` - on the master node, delete the
provided policy (or policies) from the local blockchain database.

```anylog
blockchain drop policy where id = 4a0c16ff565c6dfc05eb5a1aca4bf825
blockchain drop policy !operator
```

Blockchain drop is interesting because the actual ledger is immutable - i.e. cannot be changed. So when a user executes
`blockchain drop policy` when using the master / metadata manager node, the policy / row is actually removed.
However, when using an actual blockchain, `blockchain drop policy` instead adds an annotation telling the network to
ignore the policy with the given ID.

Each policy has a unique ID, which can either be manually defined or automatically assigned based on a hash of the
policy's content. Since the id must be unique, we recommend letting AnyLog assign it automatically, unless the policy
is one you'll reference manually and often — where a short, readable ID is easier to work with than an auto-generated
hash (e.g. a schedule policy used to monitor nodes).

### Securing Policies

By default, each policy has a unique ID that's based on the hash of the policy, or is defined by the user (though
this is less recommended). The system is also intelligent enough to stop a user from registering multiple nodes of
the same type on the same IP and port.

Since the blockchain is intended as a tool for untrusted groups to view / share data (almost like an immutable
contract), it may also be worth validating who is writing to the blockchain, using public / private keys:

`id sign [JSON Policy] where key = [private key] and password = [password]` / `id sign [JSON Policy] where password = [password]` -
sign a policy, adding the public key and signature to it.

```anylog
id sign !json_script where password = !my_password
id sign !json_script where key = !my_key and password = !my_password
```

---

## Query the Blockchain

Queries run against the **local copy** and do not depend on global ledger availability.

| Command | Description |
|---|---|
| `blockchain get` | Returns policies after runtime dynamic updates (use this normally) |
| `blockchain read` | Returns policies exactly as received from the global ledger, without dynamic updates |

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

**Examples**

```anylog
# All operators supporting a specific table
blockchain get operator where dbms = my_data and table = ping_sensor bring [name] [ip]:[port]

# Operators in specific countries
blockchain get operator where [country] == US or [country] == UK bring.ip_port

# Cluster ID for a specific table
blockchain get cluster where table[dbms] = my_data and table[name] = ping_sensor bring [cluster][id] separator = ,
```

### JOIN — keep both objects separate

```anylog
blockchain get bucket where name = my_bucket join (blockchain get operator where name = [bucket][operator])
```

Output:
```json
[{"bucket": {...}, "operator": {...}}]
```

- If no RHS match → record is omitted (inner join behavior)
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
- If no RHS match → LHS returned unchanged (left merge behavior)

### With bring formatting

```anylog
# Table output with join
blockchain get bucket where name = my_bucket join (blockchain get operator where name = [bucket][operator]) bring.table [bucket][name] [operator][ip] [operator][port]

# JSON output with merge
blockchain get bucket where name = my_bucket merge (blockchain get operator where name = [bucket][operator]) bring.json [bucket][name] [bucket][ip] [bucket][port]
```

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

## Compare Policies 

Policies can be compared to determine the different attribute and values.  
The following command returns a report indicating the differences between the two policies, or between lists of policies.  
Usage:
```anylog 
get policies diff [object 1] [object 2]
``` 
Object 1 and Object 2 are policies or lists of policies to compare. 
When lists are compared, the number of policies in the lists needs to be equal with one exception: 
If a policy is compared to a list with a single policy, the policy is assumed to be in a list, and the comparison is allowed.  
Example:
```anylog 
get policies diff !policy1 !policy2
```

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