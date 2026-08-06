---
title: "Blockchain: Full Circle"
description: "The complete loop of using AnyLog's metadata layer — connect, sync, check, define, publish, query — shown side by side for a Master/Metadata node and a real blockchain platform."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | New page — walks the full connect → sync → check → define → publish → query loop, based on the real deployment scripts in AnyLog-co/deployment-scripts. Confirms `blockchain wait for !policy` (not `blockchain wait where`) is the correct syntax per the actual `publish_policy.al` source and the upstream blockchain-commands.md — resolving that open question from the Blockchain Commands doc. | |
--->

# Blockchain: Full Circle

As covered in the previous sections, the process by which nodes communicate with a an actual blockchain ledger versus a
metadata / master node differs only by the connectivity process itself.

This page walks the full loop once, start to finish, showing the Master/Metadata node path and the real blockchain 
platform path side by side at each step, using the actual logic from AnyLog's [deployment-scripts](https://github.com/AnyLog-co/deployment-scripts) repo
(`node-deployment/`), trimmed down for readability. The full scripts handle considerably more edge-case branching
(DNS, overlay networks, auth) than shown here — follow the links at each step for the complete version.

## Which ledger?

"Real blockchain platform" itself splits into two setups depending on who runs the node you connect to. All three
options plug into the same loop below — only the connection details in step 1 change.

| | Master / Metadata Manager node | Self-hosted blockchain | Hosted blockchain platform |
|---|---|---|---|
| **What it is** | AnyLog's built-in metadata ledger — no external blockchain software involved | You run your own blockchain client (e.g. a local Ethereum/Optimism node) | A managed RPC provider (e.g. Infura, Alchemy) gives access to a public chain without running a node yourself |
| **Setup complexity** | Low — no contract deployment | Highest — install, sync, and maintain your own blockchain client | Moderate — deploy the AnyLog contract; node infrastructure is managed for you |
| **Decentralization** | None — single point of failure (an HA pair mitigates this) | Full — you control the node, decentralization of the chain itself still applies | Full chain decentralization, but node *access* depends on the provider's uptime |
| **Where the ledger lives** | Local `blockchain` database + local JSON file | On your own blockchain node's storage | On the public chain, reached through the provider's endpoint |
| **Connect via** (step 1) | `connect dbms blockchain where ...` | `blockchain connect to ethereum where provider=http://<your-node-ip>:<port>` | `blockchain connect to ethereum where provider=https://sepolia.infura.io/v3/[INFURA_PROJECT_ID]` |
| **Best for** | Dev/test and small deployments that want to avoid blockchain complexity entirely | Deployments with compliance/control requirements, or that want no dependency on a third-party RPC provider | The fastest way onto a real chain without operating any infrastructure |

1. [Connect to the ledger](#1-connect-to-the-ledger)
2. [Sync](#2-sync)
3. [Check if the policy already exists](#3-check-if-the-policy-already-exists)
4. [Define the policy](#4-define-the-policy)
5. [Publish the policy](#5-publish-the-policy)
6. [Query](#6-query)
7. [One node or two?](#7-one-node-or-two)

---

## 1. Connect to the ledger

Both paths start by making sure the node has somewhere to store metadata.

**Master / Metadata node** — create the local `blockchain` database and `ledger` table:
```anylog
<if !db_type == psql then connect dbms blockchain where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port>
else connect dbms blockchain  where type=!db_type

create table ledger where dbms=blockchain
```

**Real blockchain platform** — connect to the platform and (if needed) deploy the AnyLog contract, per blockchain 
connectivity.
```anylog
blockchain connect to ethereum where provider=https://sepolia.infura.io/v3/[INFURA_PROJECT_ID]

<blockchain set account info where
    platform = !blockchain_source and
    private_key = !blockchain_private_key and
    public_key = !blockchain_public_key and
    chain_id = !chain_id>
    
blockchain deploy contract where platform = !blockchain_source and public_key = !blockchain_public_key
```

## 2. Sync

Every node keeps its local metadata copy current via `run blockchain sync`. Master / metadata node is the only one that 
keeps 2 copies - both a JSON file and the actual connection the the blockchain logical databaase. 

```anylog
# Master
run blockchain sync where source = master and time = 60 seconds and dest = file and connection = !ledger_conn

# Real blockchain platform
run blockchain sync where source = blockchain and time = !sync_time and dest = file and platform = ethereum
```

## 3. Check if the policy already exists

Before creating a new policy, check whether one already matches this node — by company, IP, and port.
```anylog
<is_policy = blockchain get !node_type where
    company = !company_name and
    ip = !ip and
    port = !anylog_server_port bring.first>
```

This same check runs identically whether the local copy came from a master node sync or a real blockchain sync — the
query only ever hits the **local copy**. If `!is_policy` comes back non-empty, the node already has a policy and
skips straight to step 6; if it's empty, move on to step 4.

The real script branches this same check four different ways depending on DNS/overlay-network/bind configuration
(`ip = !external_dns`, `local_ip = !overlay_ip`, etc.) — see the full script for those variants.

---

## 4. Define the policy

If no policy exists yet, build one field by field. 

```anylog
new_policy = ""
set policy new_policy [!node_type] = {}
set policy new_policy [!node_type][name] = !node_name
set policy new_policy [!node_type][company] = !company_name
set policy new_policy [!node_type][ip] = !external_ip
set policy new_policy [!node_type][port] = !anylog_server_port.int
set policy new_policy [!node_type][rest_port] = !anylog_rest_port.int
```

This part is identical regardless of master vs. real blockchain — the policy JSON doesn't know or care which ledger
it'll be published to; that only matters at the publish step.

For an `operator` node specifically, the script also has to attach cluster membership, and decide whether this
operator is the primary or a backup for that cluster (by checking whether a primary already exists):

```anylog
set policy new_policy [!node_type][cluster] = !cluster_id

if not !is_main then is_primary = blockchain get operator where cluster = !cluster_id
if not !is_main and !is_primary then
do set is_main = false
do node_name = !node_name + "-bkup"
do set policy new_policy [!node_type][name] = !node_name
else if not !is_main and not !is_primary then set is_main = true
set policy new_policy [!node_type][main] = !is_main.bool
```

## 5. Publish the policy

Once built, the policy gets signed (if auth is enabled), prepared (assigned an `id`/`date`), and inserted. 

```anylog
if !enable_auth == true then new_policy = id sign !new_policy where key = !node_private_key and password = !node_password

blockchain prepare policy !new_policy

policy_type = from !new_policy bring [*]
if !policy_type == config or !master_configs == true then
do blockchain insert where policy=!new_policy and local=true
else blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

Then confirm it landed:
```anylog
is_updated = blockchain wait for !new_policy
```


## 6. Query

Once policies exist — whichever ledger backed the publish — querying is identical:

```anylog
blockchain get *
```

See [Blockchain Commands](03-%20Blockchain%20Commands.md#query-the-blockchain) for filtering, `bring`, join/merge, etc.