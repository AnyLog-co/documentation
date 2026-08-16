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
 | 2026-08-15 | Moshe Shadmon    | Updated Page. | |

--->
---
title: Blockchain Commands
description: Insert, query, and remove AnyLog metadata policies using the blockchain ledger.
layout: page
source_path: blockchain commands.md
---

# Blockchain Commands

AnyLog uses a distributed ledger to maintain the metadata that describes the network: where data resides, which nodes 
and services are available, how data is organized, and which policies control access and operation.

The metadata ledger can be maintained using a blockchain platform, or alternatively using AnyLog's blockchain emulator,
referred to as a master node.

Most blockchain commands are compatible with both implementations, allowing users to switch between a blockchain platform and a master node with minimal changes to their applications or workflows.
The metadata is stored as **policies**. A policy is a JSON object with a single root key, called the **policy type**. 
Examples of policy types include `operator`, `cluster`, `publisher`, and `uns`.

For normal operation, most users interact with the metadata layer through three commands:

```anylog
blockchain insert
blockchain get
blockchain update
blockchain drop
```

| Command | Purpose |
|---|---|
| `blockchain insert` | Add a policy to the metadata ledger |
| `blockchain get` | Query policies from the local metadata view |
| `blockchain update` | Update an existing policy while preserving its policy ID |
| `blockchain drop` | Remove or invalidate an existing policy |

These commands provide a consistent interface whether the global metadata ledger is maintained by a **master / metadata node** or by a blockchain platform such as Ethereum.

> **Note:** Every AnyLog node maintains a local view of the metadata it needs. Queries are executed against this local view, so `blockchain get` does not depend on the availability or latency of the global ledger.

---

## Metadata Storage Model

AnyLog metadata is managed by the blockchain platform or master node, which serves as the shared metadata ledger for the network.

Nodes in the network periodically synchronize with this ledger to maintain a local copy of the metadata. The local copy can be maintained as a JSON file, in a local database, or both.

AnyLog commands and services use this local copy during normal operation, allowing each node to access the metadata it needs without requiring continuous access to the blockchain or master node.

A node operates in the same manner regardless of how the global ledger is implemented. The configuration determines whether updates are sent to a master node or to a blockchain platform.

When a policy is inserted into the local ledger before it is confirmed by the global ledger, AnyLog marks it with:

```json
"ledger": "local"
```

After synchronization confirms the policy on the global ledger, the value changes to:

```json
"ledger": "global"
```

---

# `blockchain insert`

`blockchain insert` adds a policy to the metadata ledger.

It is the primary command for publishing metadata because it can update the local ledger and the configured global ledger in one operation.

## Syntax

```anylog
blockchain insert where
    policy = [policy]
    and local = [true|false]
    and master = [IP:Port]
    and blockchain = [platform]
```
The `local`, `master`, and `blockchain` parameters identify the **destination(s) for the policy**. Only the destinations that apply to the deployment need to be specified.

| Parameter | Policy Destination |
|---|---|
| `local` | The node's local metadata copy |
| `master` | The AnyLog master node / blockchain emulator |
| `blockchain` | The configured blockchain platform, such as Ethereum |

A policy can be written to one or multiple destinations in the same command.

For example, to insert a policy locally and into the master node:

```anylog
blockchain insert where policy = !policy and local = true and master = !master_node
```
## Parameters

| Parameter | Description |
|---|---|
| `policy` | JSON policy to insert |
| `local` | If `true`, update the local JSON ledger. Default: `true` |
| `master` | IP and port of the master / metadata node |
| `blockchain` | Connected blockchain platform, for example `ethereum` |

A typical deployment writes to the local ledger and to **one** global ledger:

- local ledger + master node, or
- local ledger + blockchain platform.

## Insert using a master node

```anylog
blockchain insert where
    policy = !policy
    and local = true
    and master = !master_node
```

## Insert using a blockchain platform

```anylog
blockchain insert where
    policy = !policy
    and local = true
    and blockchain = ethereum
```

## Policy ID and date

When a policy is inserted, AnyLog validates the policy and associates metadata such as its unique ID and update date.

A policy ID can be provided explicitly, but in most cases AnyLog should generate the ID automatically from the policy content.

If a policy needs a short, stable identifier because it will be referenced manually and frequently, a user-defined ID may be appropriate.

### Prepare a policy before insertion

```anylog
blockchain prepare policy !operator
```

If the policy `id` or `date` is not provided by the user, `blockchain prepare policy` adds the `id` and `date` attributes before the policy is published.

## Lower-level insert commands

`blockchain insert` is the recommended general command. The following lower-level commands target a specific storage layer.

| Command | Target |
|---|---|
| `blockchain add [policy]` | Local JSON ledger only |
| `blockchain push [policy]` | Local metadata database only |
| `blockchain commit [policy]` | Blockchain platform only |

Examples:

```anylog
blockchain add !policy
blockchain push !policy
blockchain commit !policy
```

Use these commands when working directly with a specific ledger layer. For normal application workflows, prefer `blockchain insert`.

---

# `blockchain get`

`blockchain get` queries metadata policies.

Queries are processed against the **local metadata view** maintained by the node. This allows applications and commands to use metadata without waiting for a remote blockchain platform or master node.

## Syntax

```anylog
blockchain get [policy-type] [where ...] [bring ...]
```

The command has three main parts:

1. **Policy type** — selects the type of policy.
2. **`where`** — optionally filters the policies.
3. **`bring`** — optionally extracts and formats values from the returned policies.

---

## Select policies by type

Return all operator policies:

```anylog
blockchain get operator
```

Return multiple policy types:

```anylog
blockchain get (operator, publisher)
```

Return all policies:

```anylog
blockchain get *
```

---

## Filter policies with `where`

A simple condition uses attribute/value pairs:

```anylog
blockchain get operator where dbms = my_data
```

Multiple conditions can be combined with `and`:

```anylog
blockchain get operator where
    dbms = my_data
    and ip = 24.23.250.144
```

Another example:

```anylog
blockchain get cluster where company = my-company
```

### Conditional expressions

Square-bracket paths can be used when more complex Boolean logic is needed.

```anylog
blockchain get operator where
    [name] == operator1
    or [name] == operator2
```

```anylog
blockchain get operator where
    [country] == US
    and ([city] == "San Francisco" or [city] == "San Jose")
```

A path can identify nested values inside a policy. For example:

```text
[operator][name]
```

The root element may be omitted when the policy type is already known:

```text
[name]
```

---

## Path matching

Metadata paths can be filtered using path operators.

### `startwith`

Return paths beginning with the specified value:

```anylog
blockchain get tag where
    [path] startwith 'Root/Objects/DeviceSet'
```

### `childfrom`

Return child paths below the specified path:

```anylog
blockchain get tag where
    [path] childfrom 'Root/Objects/DeviceSet'
```

---

# Formatting results with `bring`

By default, `blockchain get` returns matching policy objects. `bring` can extract specific fields or transform the result.

A detailed explanation of the ```bring``` option is available in the [05- JSON Data Transformation.md](../07-%20CLI/05-%20JSON%20Data%20Transformation.md#the-bring-keyword) section.

## Return a single field

```anylog
blockchain get operator bring [name]
```

## Combine fields

```anylog
blockchain get operator bring [name] [ip]:[port]
```

## Return IP:Port values

```anylog
blockchain get operator bring.ip_port
```

## Table output

```anylog
blockchain get operator bring.table
```

## JSON output

```anylog
blockchain get operator bring.json
```

## Sorted table

```anylog
blockchain get operator bring.table.sort [operator][name]
```

---

## Query examples

### Find operators supporting a table

```anylog
blockchain get operator where
    dbms = my_data
    and table = ping_sensor
    bring [name] [ip]:[port]
```

### Get operator addresses by country

```anylog
blockchain get operator where
    [country] == US
    or [country] == UK
    bring.ip_port
```

### Get the cluster ID for a table

```anylog
blockchain get cluster where
    table[dbms] = my_data
    and table[name] = ping_sensor
    bring [cluster][id] separator = ,
```

---

# Save results and apply `bring` later

The result of `blockchain get` can be assigned to a variable and processed separately.

```anylog
operators = blockchain get operator
```

Then:

```anylog
from !operators bring [name] [ip]:[port]
```

This is useful when the same set of policies is reused for multiple operations or output formats.

---

# Use metadata to determine command destinations

A common AnyLog pattern is to query metadata and use the result as the destination of another command.

For example:

```anylog
destinations = blockchain get (operator, query) where
    [country] == US
    or [country] == IL
    bring [*][ip]:[*][port] separator = ,
```

Then:

```anylog
run client (!destinations) get node info net_io_counters
```

The query can also be embedded directly:

```anylog
run client (
    blockchain get (operator, query) where
        [country] == US
        or [country] == IL
        bring [*][ip]:[*][port] separator = ,
) get node info net_io_counters
```

This allows policies to dynamically define which AnyLog nodes receive a command.

---

# Join and Merge Policy Queries

`blockchain get` can combine metadata from related policies using `join` or `merge`.

## `join`

`join` preserves both policy objects as separate objects in the result.

```anylog
blockchain get bucket where
    name = my_bucket
    join (
        blockchain get operator where
            name = [bucket][operator]
    )
```

Example result:

```json
[
  {
    "bucket": {
      "name": "my_bucket",
      "operator": "operator1"
    },
    "operator": {
      "name": "operator1",
      "ip": "24.5.219.50",
      "port": 7848
    }
  }
]
```

Behavior:

- the left-hand and right-hand policies remain separate;
- values from the left-hand policy can be referenced in the right-hand query;
- if the right-hand query has no match, the record is omitted.

### Format joined results

```anylog
blockchain get bucket where
    name = my_bucket
    join (
        blockchain get operator where
            name = [bucket][operator]
    )
    bring.table
        [bucket][name]
        [operator][ip]
        [operator][port]
```

---

## `merge`

`merge` adds fields returned by the second query directly into the first policy object.

```anylog
blockchain get bucket where
    name = my_bucket
    merge (
        blockchain get operator where
            name = [bucket][operator]
    )
```

Example result:

```json
[
  {
    "bucket": {
      "name": "my_bucket",
      "operator": "operator1",
      "ip": "24.5.219.50",
      "port": 7848
    }
  }
]
```

Behavior:

- fields from the right-hand result are added to the left-hand object;
- the left-hand policy wins if both objects contain the same key;
- if no right-hand policy matches, the left-hand policy is returned unchanged.

---

# Root and Child Policies

AnyLog policies can form a hierarchy. This is used, among other things, to represent Unified Namespace (UNS) structures.

A **root policy** does not contain a `parent` attribute.

A **child policy** references another policy through its `parent` attribute.

Return root policies:

```anylog
blockchain get root policies
```

Example:

```json
[
  {
    "uns": {
      "name": "Enterprise_A",
      "namespace": "Enterprise_A",
      "id": "00ddf..."
    }
  },
  {
    "uns": {
      "name": "Sensors",
      "namespace": "Enterprise_A/Sensors",
      "parent": "00ddf...",
      "dbms": "my_data",
      "table": "ping_sensor"
    }
  }
]
```

In this example, `Enterprise_A` is a root policy and `Sensors` is a child policy.

## Include selected root policy types

```anylog
blockchain get root policies include cluster uns
```

## Exclude selected root policy types

```anylog
blockchain get root policies exclude cluster
```

---

# `blockchain get` vs. `blockchain read`

For normal metadata queries, use:

```anylog
blockchain get
```

`blockchain get` returns the node's operational view of the policies after AnyLog has applied runtime and dynamic updates.

`blockchain read` returns the policies as they were received from the global ledger, before those dynamic updates.

```anylog
blockchain read operator
```

Use `blockchain read` primarily for troubleshooting or for examining the source representation of a policy.

---

# `blockchain drop`

`blockchain drop` removes or invalidates metadata policies.

The exact behavior depends on the type of global ledger.

## Drop by policy ID

```anylog
blockchain drop policy where
    id = 4a0c16ff565c6dfc05eb5a1aca4bf825
```

A variable can also be used:

```anylog
blockchain drop policy where id = !policy_id
```

## Drop using a policy object

```anylog
blockchain drop policy !operator
```

---

## Master node vs. immutable blockchain

The meaning of "drop" is important because a blockchain ledger is immutable.

### Master / metadata node

When the global ledger is maintained by a master / metadata node, the matching policy can be removed from the master's local metadata database.

### Blockchain platform

When the global ledger is an immutable blockchain platform, the original ledger entry cannot be physically deleted.

Instead, AnyLog records metadata that identifies the policy as dropped so that the network ignores the policy.

From the application's point of view, the policy is no longer active even though the historical blockchain record remains immutable.

---

## Drop policies associated with a host

A master metadata database can remove policies associated with a particular host:

```anylog
blockchain drop by host
```

This is a lower-level administrative operation and should be used when cleaning metadata associated with a node or host rather than removing an individual policy.

---

# Securing Policies

Policies can be signed to verify the identity of the party writing metadata.

## Sign using the configured key

```anylog
id sign !json_script where
    password = !my_password
```

## Sign using a specified private key

```anylog
id sign !json_script where
    key = !my_key
    and password = !my_password
```

The signature information is added to the JSON policy and can be used to validate the source of metadata written to the ledger.

---

# Connecting and Synchronizing the Ledger

Most application users only need `blockchain insert`, `blockchain get`, and `blockchain drop`.

The commands in this section are primarily used when configuring or administering the metadata infrastructure.

---

## Seed a node from another AnyLog node

When a new node joins an existing network, it can retrieve an initial metadata copy from another node:

```anylog
blockchain seed from 73.202.142.172:7848
```

General form:

```anylog
blockchain seed from [IP:Port]
```

This operation is commonly used during startup. Ongoing updates should normally be handled by blockchain synchronization.

---

# Blockchain Synchronization

`run blockchain sync` continuously refreshes the local metadata representation.

## Synchronize from a master node

```anylog
run blockchain sync where
    source = master
    and time = 60 seconds
    and dest = file
    and dest = dbms
    and connection = !ip_port
```

## Synchronize from a blockchain platform

```anylog
run blockchain sync where
    source = blockchain
    and time = !sync_time
    and dest = file
    and platform = ethereum
```

## Synchronization options

| Option | Description |
|---|---|
| `source` | Metadata source: `master` or `blockchain` |
| `dest` | Destination to update: `file` and/or `dbms` |
| `connection` | Connection information for a master node |
| `platform` | Blockchain platform when `source = blockchain` |
| `time` | Synchronization frequency |

Every node that depends on changing metadata should maintain an appropriate synchronization process. The required frequency may vary by node role.

---

# Master / Metadata Node Administration

A master / metadata node maintains a complete metadata ledger in a local database.

## Create the ledger table

```anylog
blockchain create table
```

The ledger is stored in:

```text
blockchain.ledger
```

## Export the ledger as JSON

```anylog
blockchain pull to json [output-file]
```

## Export the ledger as SQL

```anylog
blockchain pull to sql [output-file]
```

## Print the ledger

```anylog
blockchain pull to stdout
```

## Load a ledger file into the local database

```anylog
blockchain update dbms [file]
```

## Query the master ledger directly

```anylog
sql blockchain "select * from ledger"
```

Direct SQL access is primarily an administrative and troubleshooting capability. Application logic should normally query metadata using `blockchain get`.

---

# Copy Metadata from a Master Node

A node can explicitly retrieve the ledger from a master node.

```anylog
master_node = 127.45.35.12:32048
```

Retrieve the ledger:

```anylog
run client (!master_node) blockchain pull to json
```

Copy the generated file:

```anylog
run client (!master_node) file get !!blockchain_file !blockchain_file
```

If automatic synchronization is not running, force AnyLog to reload the updated local metadata:

```anylog
blockchain load metadata
```

---

# Blockchain Platform Setup

When the global ledger is maintained on a blockchain platform, the platform must be configured before policies can be published.

## Configure account information

```anylog
blockchain set account info where
    platform = ethereum
    and private_key = !private_key
    and public_key = !public_key
    and chain_id = 11155111
```

## Deploy the AnyLog contract

```anylog
blockchain deploy contract where
    platform = ethereum
    and public_key = !public_key
```

A master / metadata node does not require blockchain account or smart-contract configuration because its global ledger is maintained in the local metadata database.

---

# Update an Existing Policy

An existing policy can be updated while preserving its policy ID.

The ID must already exist on the target ledger, and the ID in the policy must match the ID supplied to the update command.

Example for Ethereum:

```anylog
blockchain update to ethereum !policy_id !policy
```

An update should be used when the policy represents the same logical object. Use `blockchain insert` when publishing a new policy.

---

# Compare Policies

Policies can be compared to identify differences in attributes and values.

## Syntax

```anylog
get policies diff [object-1] [object-2]
```

Example:

```anylog
get policies diff !policy1 !policy2
```

The objects can be individual policies or lists of policies.

When two lists are compared, the lists normally need to contain the same number of policies. A single policy may also be compared with a list containing one policy.

---

# Additional Blockchain Commands

The following commands are useful for validation, troubleshooting, administration, or direct manipulation of a specific metadata layer.

| Command | Description |
|---|---|
| `blockchain test` | Validate the local blockchain JSON file and its structure |
| `blockchain test id` | Test whether a policy ID exists locally |
| `blockchain get id [json]` | Return the hash / ID associated with a JSON structure |
| `blockchain prepare policy [json]` | Add an ID and date to a policy |
| `blockchain checkout` | Retrieve the latest ledger data from a blockchain platform |
| `blockchain update file [path]` | Replace the local blockchain file and preserve the prior version as `.old` |
| `blockchain delete local file` | Delete the local JSON ledger file |
| `blockchain query metadata` | Display a diagram view of the local metadata structure |
| `blockchain test cluster` | Analyze cluster policies |
| `blockchain state where platform = [name]` | Return the state of the active blockchain contract |

---

# Recommended Usage

For most AnyLog applications and integrations, the primary blockchain commands are `insert`, `get`, `update`, and `drop`:

```anylog
# Publish metadata
blockchain insert where policy = !policy and local = true and master = !master_node

# Query metadata
blockchain get operator where dbms = my_data bring [name] [ip]:[port]

# Update existing metadata
blockchain update to ethereum !policy_id !policy

# Remove metadata
blockchain drop policy where id = !policy_id
```

The remaining blockchain commands support deployment configuration, synchronization, administration, debugging, or direct access to an individual ledger layer.
