---
title: "Metadata"
description: "How AnyLog's metadata relates to policies — metadata as the network's collective knowledge, policies as its individual JSON records — plus a tour of the core policy types."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | Fixed invalid JSON in the `config` and `table` policy examples (Python-style multi-line string concatenation isn't valid JSON; also a stray quote splitting `"CREATE INDEX"` mid-word); fixed a literal `[...]` placeholder that isn't valid JSON; typo fixes (recored/gurantee/infromation/nodes's/wheelchair→hierarchical); completed a truncated sentence in the Mapping Policy bullet | |
 | 2026-07-27 | Ori Shadmon    | Created document distinguishing metadata (the concept) from policy (the JSON unit); fixed a misleading "metadata vs. policy" JSON example that implied policies exist in two different shapes (they don't — the root-key wrapper is the policy, same as every policy example elsewhere in these docs) | |
--->

# Metadata

Metadata is the actual content stored on the blockchain, whether it's the node definition, configuration policies or
the `CREATE` statements for the tables.

AnyLog maintains the metadata in a ledger. The metadata is organized as a collection of objects, called policies. A
policy is a JSON structure with a single key at the root. The root key is called the Policy Type.

## Policy vs. Metadata

_Metadata_ and _policy_ describe the same underlying thing at two different levels: _metadata_ is the conceptual,
collective idea — "what nodes exist" or "which operators are part of a specific cluster" — while a _policy_ is one
individual JSON record that makes up part of that metadata.

Put simply: metadata is the whole body of knowledge the network has about itself; a policy is a single entry in it.
A node's metadata is really just the set of every policy it currently knows about — for example, one `cluster` policy
and one `operator` policy that references it, together, are both individually policies and collectively part of the
network's metadata:

```json
{
  "cluster": {
    "company": "Bachelor Controls 2.0",
    "name": "cluster1",
    "id": "06f093559c851c6d4c3e950ebc9c5499",
    "date": "2026-07-20T18:40:12.114402Z",
    "status": "active",
    "ledger": "global"
  }
},
{
  "operator": {
    "name": "bachelor-operator1",
    "company": "Bachelor Controls 2.0",
    "hostname": "node3",
    "ip": "172.233.208.212",
    "port": 32148,
    "rest_port": 32149,
    "broker_port": 32150,
    "loc": "41.8500,-87.6500",
    "country": "US",
    "state": "Illinois",
    "city": "Chicago",
    "cluster": "06f093559c851c6d4c3e950ebc9c5499",
    "id": "c7df327826839d64ff23f5f9b52ebf1b",
    "date": "2026-07-20T18:38:31.925781Z",
    "ledger": "global"
  }
}
```

Each of the two JSON objects above is a policy (`cluster`, `operator`) — note the operator's `cluster` field pointing
at the cluster's `id`. Together with every other node/cluster/table/config policy the node has synced, they
collectively make up that node's metadata. There isn't a separate, unwrapped "metadata shape" that a policy turns
into — the root-key wrapper (`"cluster": {...}`, `"operator": {...}`) is the policy, full stop.

### Metadata storage

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


## Policy Types

Standard policies that most deployments would have:

* `config` - a configuration policy explaining how to deploy a node in terms of which services are needed, frequency of
_blockchain sync_ and logical databases the agent is connected to.

```json
{
  "config" : {
    "name" : "operator-smart_city-configs",
    "company": "Bachelor Controls 2.0",
    "node_type" : "operator",
    "ip" : "!ip",
    "port" : "!anylog_server_port.int",
    "tcp_threads" : "!tcp_threads.int",
    "tcp_bind" : "!tcp_bind.bool",
    "rest_port" : "!anylog_rest_port.int",
    "rest_threads" : "!rest_threads.int",
    "rest_timeout" : "!rest_timeout.int",
    "rest_bind" : "!rest_bind.bool",
    "broker_port" : "!anylog_broker_port.int",
    "broker_threads" : "!broker_threads.int",
    "broker_bind" : "!broker_bind",
    "script" : [
      "process !local_scripts/node-deployment/database/deploy_database.al",
      "process !local_scripts/node-deployment/connect_blockchain.al",
      "process !local_scripts/node-deployment/policies/cluster_policy.al",
      "process !local_scripts/node-deployment/policies/node_policy.al",
      "run scheduler 1",
      "set buffer threshold where time=!threshold_time and volume=!threshold_volume and write_immediate=!write_immediate",
      "run streamer",
      "if !enable_ha == true then run data distributor",
      "if !enable_ha == true then run data consumer where start_date=!start_date",
      "if !operator_id and !blockchain_source != master then run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and compress_json=!compress_file and compress_sql=!compress_sql and archive_json=!archive and archive_sql=!archive_sql and blockchain=!blockchain_source and policy=!operator_id and threads=!operator_threads",
      "if !operator_id and !blockchain_source == master then run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and compress_json=!compress_file and compress_sql=!compress_sql and archive_json=!archive and archive_sql=!archive_sql and master_node=!ledger_conn and policy=!operator_id and threads=!operator_threads",
      "...",
      "process !local_scripts/node-deployment/policies/license_policy.al"
    ],
    "id" : "56024db17faa4a7ec2673f0da8793722",
    "date" : "2026-06-02T00:05:42.964222Z",
    "ledger" : "global"
  }
}
```
> The `"..."` entry above is a placeholder for additional, omitted script lines — not literal script content.

> Notice that network configurations (the top half) does not use hardcoded values, thus the same configuration policy
> can be reused with multiple / all operator nodes.

* `cluster` - clusters are logical objects that define the grouping of operator nodes so that the network is aware
where data resides, and shared operators can seamlessly copy data from one another. A cluster policy is required in order to
define an operator node policy, but the (root) cluster itself can be defined in 3 ways:
  * as is without any dbms or tables - this would guarantee that any new information flowing into the operator would be recorded
  on the blockchain and thus is the **best** and simplest form of the cluster policies to be defined by the user.
  * Specify a logical database, and then only data associated with that specific database is recorded on the blockchain
  * specify both logical database and table

**Note:** sensor or device data is stored in the operator node, only the metadata information is stored on the blockchain.

```text
# No extra content cluster policy
{
  "cluster": {
    "company": "Bachelor Controls 2.0",
    "name": "cluster1",
    "id": "06f093559c851c6d4c3e950ebc9c5499",
    "date": "2026-07-20T18:40:12.114402Z",
    "status": "active",
    "ledger": "global"
  }
}

# a policy containing both dbms and table - this gets autogenerated when new data is inserted
{
  "cluster" : {
    "parent" : "06f093559c851c6d4c3e950ebc9c5499",
    "name" : "cluster1",
    "company" : "Bachelor Controls 2.0",
    "table" : [{
      "dbms" : "monitoring",
      "name" : "syslog",
      "status" : "active"
    }],
    "source" : "Node at 173.255.212.88:32148",
    "id" : "bb248db689a124329909cead98d2e5f5",
    "date" : "2026-07-24T10:27:35.559884Z",
    "status" : "active",
    "ledger" : "global"
}}

# a database specific cluster policy
{
  "cluster": {
    "company": "Bachelor Controls 2.0",
    "name": "cluster1",
    "dbms" : "monitoring",
    "id": "06f093559c851c6d4c3e950ebc9c5589",
    "date": "2026-07-20T18:40:12.114402Z",
    "status": "active",
    "ledger": "global"
  }
}
```

* **Node policy** - This provides information on how to interact with the node. With the exception of the _operator_
node, which requires a node policy, all other nodes' policies are optionally defined. The reason _operator_ is
required is because otherwise the network wouldn't know where the data is stored.

```json
{
  "operator": {
    "name": "bachelor-operator1",
    "company": "Bachelor Controls 2.0",
    "hostname": "node3",
    "ip": "172.233.208.212",
    "port": 32148,
    "rest_port": 32149,
    "broker_port": 32150,
    "loc": "41.8500,-87.6500",
    "country": "US",
    "state": "Illinois",
    "city": "Chicago",
    "cluster": "06f093559c851c6d4c3e950ebc9c5499",
    "id": "c7df327826839d64ff23f5f9b52ebf1b",
    "date": "2026-07-20T18:38:31.925781Z",
    "ledger": "global"
  }
}
```

* `table` - A metadata piece of information that shows how table(s) - in this case `monitoring.syslog`, are defined (i.e.
`CREATE` statement). This policy is often reused across nodes and partitioning in order to guarantee that the data is
organized in the same manner.

```json
{
  "table" : {
    "dbms" : "monitoring",
    "name" : "syslog",
    "create" : "CREATE TABLE IF NOT EXISTS syslog(row_id SERIAL PRIMARY KEY, insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(), tsd_name CHAR(3), tsd_id INT, source_ip cidr, priority int, timestamp timestamp not null default now(), hostname varchar, tag varchar, message varchar); CREATE INDEX syslog_timestamp_index ON syslog(timestamp); CREATE INDEX syslog_tsd_index ON syslog(tsd_name, tsd_id); CREATE INDEX syslog_insert_timestamp_index ON syslog(insert_timestamp); CREATE INDEX syslog_source_ip_index ON syslog(source_ip);",
    "id" : "011886bb90df2d265ab9a0854eddf07f",
    "date" : "2026-07-18T19:49:43.020405Z",
    "ledger" : "global"
  }
}
```

* [Mapping Policy](./04-%20Mapping%20Policy.md) - A mapping policy defines how incoming JSON data (arriving at an operator node) should be
organized — i.e., which keys/value pairs map to which column/value, for each row. This allows the same ingestion
logic to be reused consistently across every node handling that data source.

* [UNS](./05-%20Unitfied%20Namespace.md) - Unified namespace policies are a way to help the user view the data in a hierarchical format; similar to
OSISoft's PI System Asset Framework (AF). These policies can be **both** autogenerated using `dynamic=true` or manually
defined by the user. The hierarchy itself consists of 2 parts:
  * `parent` - same referencing logic as `cluster`, linking a policy to its parent in the hierarchy
  * `namespace` path

The policies mentioned above are either autogenerated (ex. table) or frequently used (ex. node connection info). However,
a user can define whatever policy they choose - it could be information about device / sensors, license key, permissions
and security, etc.