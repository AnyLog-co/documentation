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
 | 2026-08-29 | Moshe Shadmon    | Update | |
--->
# Blockchain: Full Circle

This section walks through the command-by-command logic used to configure access to the metadata ledger, synchronize metadata, define policies, and publish them.

The examples are based on AnyLog's `deployment-scripts` repository under `node-deployment/`, with some configuration and edge-case branches removed for readability.

The same policy structure and APIs are used whether the metadata backend is an AnyLog **Master Node** or a **blockchain platform**. The examples below use a Master Node.

The basic flow is:

1. Connect to the ledger (configuration)
2. Synchronize metadata (configuration)
3. Define a policy
4. Publish the policy

---

## 1. Connect to the Ledger

When using a Master Node, the metadata is stored in the local `blockchain` database.

The database connection is part of the Master Node configuration and must be established whenever the Master Node starts or restarts.

The value of `!db_type` determines which database implementation is used:

- `psql` for PostgreSQL
- `sqlite` for SQLite

The same configuration handles both:

~~~anylog
<if !db_type == psql then connect dbms blockchain where
    type=!db_type and
    user=!db_user and
    password=!db_passwd and
    ip=!db_ip and
    port=!db_port>
else connect dbms blockchain where type=!db_type
~~~

For example, when using PostgreSQL:

~~~text
db_type = psql
db_user = admin
db_passwd = passwd
db_ip = 127.0.0.1
db_port = 5432
~~~

When using SQLite:

~~~text
db_type = sqlite
~~~

The logical database name is `blockchain` in both cases.

The `ledger` table needs to be created **once** when the Master Node is initially configured:

~~~anylog
create table ledger where dbms=blockchain
~~~

Once created, the table remains in the database and does not need to be recreated when the Master Node restarts.

---

## 2. Synchronize Metadata

Each AnyLog node maintains a local metadata file.

Metadata synchronization is part of the node configuration and runs automatically according to the configured synchronization interval.

When using a Master Node:

~~~anylog
run blockchain sync where
    source=master and
    time=60 seconds and
    dest=file and
    connection=!ledger_conn
~~~

The `time` value determines how frequently the node synchronizes its local metadata file with the metadata maintained by the Master Node.

For example, `time=60 seconds` causes the node to synchronize its metadata every 60 seconds.

Once configured, the synchronization process runs continuously in the background.

---

## 3. Define a Policy

A policy can be constructed locally before it is published.

For example, assume the following values:

~~~text
node_type = operator
node_name = operator-1
company_name = AnyLog
external_ip = 10.0.0.10
anylog_server_port = 32148
anylog_rest_port = 32149
~~~

The policy can be constructed using:

~~~anylog
new_policy = {}

set policy new_policy [!node_type] = {}
set policy new_policy [!node_type][name] = !node_name
set policy new_policy [!node_type][company] = !company_name
set policy new_policy [!node_type][ip] = !external_ip
set policy new_policy [!node_type][port] = !anylog_server_port.int
set policy new_policy [!node_type][rest_port] = !anylog_rest_port.int
~~~

With the values above, `!new_policy` contains:

~~~json
{
  "operator": {
    "name": "operator-1",
    "company": "AnyLog",
    "ip": "10.0.0.10",
    "port": 32148,
    "rest_port": 32149
  }
}
~~~

---

## 4. Publish the Policy

The policy is published to the Master Node using `blockchain insert`:

~~~anylog
blockchain insert where
    policy=!new_policy and
    local=true and
    master=!ledger_conn
~~~

This command performs two updates:

1. The policy is published to the Master Node and added to the shared metadata.
2. Because `local=true` is specified, the policy is also added immediately to the node's local metadata file.

The policy therefore becomes immediately available locally without waiting for the next synchronization cycle.

If `local=true` is omitted:

~~~anylog
blockchain insert where
    policy=!new_policy and
    master=!ledger_conn
~~~

the policy is published to the Master Node, but the node's local metadata file is not updated immediately. The policy will become available locally during the next synchronization cycle.

In other words:

~~~text
With local=true:

Policy
  ├──► Master Node
  └──► Local metadata file
~~~

Without `local=true`:

~~~text
Policy
  └──► Master Node
          │
          │ next synchronization
          ▼
       Local metadata file
~~~

### Preparing a Policy

A policy can optionally be prepared before it is inserted:

~~~anylog
blockchain prepare policy !new_policy
~~~

This adds system-managed attributes such as the policy `id` and `date`.

However, explicitly preparing the policy is **not required**. If `blockchain prepare policy` is not called, the required system-managed attributes are added dynamically as part of the `blockchain insert` process.

Therefore, the normal flow can simply be:

~~~anylog
new_policy = {}

set policy new_policy [operator] = {}
set policy new_policy [operator][name] = operator-1
set policy new_policy [operator][company] = AnyLog

blockchain insert where
    policy=!new_policy and
    local=true and
    master=!ledger_conn
~~~