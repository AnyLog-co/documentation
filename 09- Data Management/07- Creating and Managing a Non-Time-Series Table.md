---
title: "Creating and Managing a Non-Time-Series Table"
description: "Worked example: registering a non-time-series table with the AnyLog metadata layer"
layout: page
---
<!---
### 📜 Change Log
- 2026-08-11 | Ori Shadmon | Non-time-series table creation, registration, and worked example

Note: companion document to "Managing Relational (OLTP) Data in AnyLog" — read that document first for the 
concepts behind this workflow.
--> 

# Creating and Managing a Non-Time-Series Table

AnyLog is optimized for managing and querying time-series data. However, there are cases where users need to include 
non-time-series tables—such as asset information, user records, configuration data, reference data, or 
application-specific tables—in the AnyLog environment. By registering these tables with the AnyLog metadata layer, 
they become discoverable across the network. A query submitted to any AnyLog node can use the metadata to identify 
where the requested table is hosted, route the query to the appropriate node, and return the results to the 
requesting application. This allows non-time-series data to participate in the same distributed data environment as 
time-series data, without requiring the data to be centralized.

This document walks through the custom/manual path described in 
<a href="./07%20OLTP%20Data.md" target="_blank">Managing Relational (OLTP) Data in AnyLog</a>: defining your own `CREATE TABLE` statement and 
registering it with the AnyLog metadata layer, so the table remains discoverable and queryable from any node in the 
network.

> Use this workflow when the table needs constraints, keys, or indexes other than AnyLog's default timestamp-based 
> ones. If the default is sufficient, just push data to the node—AnyLog will generate the schema and policies 
> automatically.

## Example Environment

The example below uses a small three-node network—one **master**, one **operator**, and one **query** node—started 
and validated before the table is created.

```anylog
# start nodes 
make up ANYLOG_TYPE=master 
make up ANYLOG_TYPE=operator 
make up ANYLOG_TYPE=query 

# validate they can communicate 
AL d486935679d6-acme-query1 +> test network 
Test Network
[****************************************************************]

Address          Node Type Node Name                       Status
----------------|---------|-------------------------------|------|
172.27.0.2:32048|master   |8f06476c3312-my_company-master1|  +   |
172.27.0.4:32348|query    |d486935679d6-acme-query1       |  +   |
172.27.0.3:32148|operator |f0fb02d5d873-anylog-operator1  |  +   |
```

## 1. Create the Table

The table structure is defined by the user using a standard SQL `CREATE TABLE` statement. This statement isn't run 
against the database directly—it's passed to AnyLog in the next step so the corresponding metadata policy can be 
generated. The table is ultimately created on the AnyLog node that will host the data.

**Example:**

```sql
-- sample_file.sql
CREATE TABLE IF NOT EXISTS users(
    username char(5),
    password char(7),
    role char(5),
    email char(4),
    associds char(4),
    CONSTRAINT users_username_unique UNIQUE (username)
);
```

## 2. Register the Table with the Metadata Layer

The table definition needs to be represented by a policy in the AnyLog metadata layer. The policy describes the 
table name, database, and schema, allowing AnyLog to discover it across the network.

If you want data to be inserted and managed *through* AnyLog (as shown in Step 3), your `CREATE TABLE` statement 
needs to include AnyLog's system columns before you register it:

| Column | Definition | Purpose |
|---|---|---|
| `row_id` | `SERIAL PRIMARY KEY` | unique row identifier |
| `insert_timestamp` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | when the row was inserted |
| `tsd_name` | `CHAR(3)` | replication/HA-DR bookkeeping |
| `tsd_id` | `INT` | replication/HA-DR bookkeeping |

along with two supporting indexes:

```sql
CREATE INDEX <table>_tsd_index ON <table>(tsd_name, tsd_id);
CREATE INDEX <table>_insert_timestamp_index ON <table>(insert_timestamp);
```

> Use `CURRENT_TIMESTAMP` rather than PostgreSQL's `NOW()` for the default—SQLite (one of AnyLog's supported 
> backends) doesn't support `NOW()`. If the table will only ever be managed directly through the underlying 
> database rather than through AnyLog, these columns and indexes aren't required.

**Example—extending Step 1's `sample_file.sql` with the required columns and indexes:**

```sql
CREATE TABLE IF NOT EXISTS users (
    row_id SERIAL PRIMARY KEY,
    insert_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tsd_name CHAR(3),
    tsd_id INT,

    username char(5),
    password char(7),
    role char(5),
    email char(4),
    associds char(4),
    CONSTRAINT users_username_unique UNIQUE (username)
);

CREATE INDEX users_tsd_index ON users(tsd_name, tsd_id);
CREATE INDEX users_insert_timestamp_index ON users(insert_timestamp);
```

Before registering, confirm there's no existing _table_ or _cluster_ policy with the same database/table name—if 
either already exists, it can't be reused:

```anylog
blockchain get table where name=users and dbms=mydb

blockchain get cluster where table[name] = users and table[dbms] = mydb
```

Wrap the `CREATE` statement in a `table` policy and publish it to the blockchain:

```anylog
<new_policy = {
  "table": {
    "dbms": "mydb",
    "name": "users",
    "create": "CREATE TABLE IF NOT EXISTS users (row_id SERIAL PRIMARY KEY, insert_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, tsd_name CHAR(3), tsd_id INT, username char(5), password char(7), role char(5), email char(4), associds char(4), CONSTRAINT users_username_unique UNIQUE (username));CREATE INDEX users_tsd_index ON users(tsd_name, tsd_id);CREATE INDEX users_insert_timestamp_index ON users(insert_timestamp);"
  }
}>

blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

Confirm the policy was registered:

```anylog
AL f0fb02d5d873-anylog-operator1 +> blockchain get table where dbms=mydb
[{"table" : {"dbms" : "mydb",
             "name" : "users",
             "create" : "CREATE TABLE IF NOT EXISTS users (row_id SERIAL PRIMARY KEY, insert_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, tsd_name CHAR(3), tsd_id INT, username char(5), password char(7), role char(5), email char(4), associds char(4), CONSTRAINT users_username_unique UNIQUE (username));CREATE INDEX users_tsd_index ON users(tsd_name, tsd_id);CREATE INDEX users_insert_timestamp_index ON users(insert_timestamp);",
             "id" : "c5e55bfc1cf20f4312cd27083ee3ae08",
             "date" : "2026-08-11T18:51:17.392505Z",
             "ledger" : "global"}}]
```

**Before running this against a table that's already deployed:** if a table policy already exists for this 
database/table name with a different `create` value, publishing will conflict and downstream inserts will fail with 
"no such table" until the mismatch is resolved. Also make sure your SQL uses syntax valid across every SQL backend 
you're deploying to (AnyLog supports SQLite and PostgreSQL)—dialect-specific syntax with no equivalent on the other 
engine (e.g. PostgreSQL's `SERIAL`) isn't caught automatically.

> **Note:** There's a limitation in the manual `CREATE` above—it hardcodes column types and constraints **before** 
> seeing any data, whereas the standard AnyLog-generated table policy defines the `create` statement **based on the 
> data** once it arrives. Use the manual path only when you need constraints or indexes beyond AnyLog's 
> defaults.

## 3. Add or Update Data

Data is initially added by pushing a JSON stream containing the data to the table. The first JSON data pushed to the 
node triggers AnyLog to:
1. Create the table and its schema in the local database assigned to the table.
2. Register the node in the AnyLog metadata layer as a node that hosts data for this table.
3. Insert the JSON data into the local table.

Therefore, pushing JSON data to the table at least once initializes the local table and makes its location 
discoverable through the AnyLog metadata layer.

After the table has been initialized, data can be added or updated in either of two ways:
- **Through AnyLog:** JSON data can continue to be pushed to the node hosting the table and inserted into the table.
- **Directly by an application:** An application can connect directly to the local database and modify the table 
using standard SQL operations such as `INSERT`, `UPDATE`, and `DELETE`.

Because the node hosting the table has already been registered with the AnyLog metadata layer, applications can 
subsequently manage the data directly in the local database without affecting the table's discoverability across 
the AnyLog network.

**Example:**

```shell
curl.exe -X PUT "http://172.23.160.85:32149/" \
  -H "type: json" \
  -H "dbms: mydb" \
  -H "table: users" \
  -H "mode: streaming" \
  -H "Content-Type: application/json" \
  -d '[{"username":"oshad","password":"1234567","role":"admin","email":"osha","associds":"uid1"}]'

curl.exe -X PUT "http://172.23.160.85:32149/" \
  -H "type: json" \
  -H "dbms: mydb" \
  -H "table: users" \
  -H "mode: streaming" \
  -H "Content-Type: application/json" \
  -d '[{"username":"nwarn","password":"7543216","role":"user","email":"nsha","associds":"uid12"}]'
```

### Constraint Enforcement

Because this sample workflow defines the schema with constraints like the `UNIQUE (username)` constraint from Step 1 
are enforced at the database layer on every insert—including inserts pushed through AnyLog. If a row violates the 
constraint, AnyLog does not silently drop, duplicate, or retry it; the row is rejected and the failure is recorded 
in the node's error log.

For example, resubmitting a `username` that already exists:

```shell
curl.exe -X PUT "http://172.23.160.85:32149/" \
  -H "type: json" \
  -H "dbms: mydb" \
  -H "table: users" \
  -H "mode: streaming" \
  -H "Content-Type: application/json" \
  -d '[{"username":"oshad","password":"1234567","role":"user","email":"osha","associds":"uid1"}]'
```

Check the error log on the operator that processed the insert:

```anylog
AL 38797aba3631-anylog-operator1 +> get error log 

ID  Count Thread     Time                     Type  Text
---|-----|----------|------------------------|-----|----------------------------------------------------------------------------------------------------|
822|    1|rest_0    |Tue Aug 11 21:05:48 2026|Error|Error executing SQL: INSERT INTO par_users_2026_08_00_d14_insert_timestamp (row_id, insert_timestamp|
   |     |          |                        |     |, tsd_name, tsd_id, username, password, role, email, associds) VALUES (NULL, '2026-08-11T21:05:48.91|
   |     |          |                        |     |4348Z', 0, 7, 'oshad', '1234567', 'user', 'osha', 'uid1'); UNIQUE constraint failed: par_users_2026_|
   |     |          |                        |     |08_00_d14_insert_timestamp.username                                                                 |
823|    1|rest_0    |Tue Aug 11 21:05:48 2026|Error|Failed to INSERT streaming data to local table with immediate flag: mydb.users                      |
825|    1|operator_0|Tue Aug 11 21:06:04 2026|Error|Error executing SQL: INSERT INTO par_users_2026_08_00_d14_insert_timestamp (row_id, insert_timestamp|
   |     |          |                        |     |, tsd_name, tsd_id, username, password, role, email, associds) VALUES (NULL, '2026-08-11T21:06:04.01|
   |     |          |                        |     |5412Z', 45, 8, 'oshad', '1234567', 'user', 'osha', 'uid1'); UNIQUE constraint failed: par_users_2026|
   |     |          |                        |     |_08_00_d14_insert_timestamp.username                                                                |
828|    1|operator_1|Tue Aug 11 21:06:09 2026|Error|Error executing SQL: INSERT INTO par_users_2026_08_00_d14_insert_timestamp (row_id, insert_timestamp|
   |     |          |                        |     |, tsd_name, tsd_id, username, password, role, email, associds) VALUES (NULL, '2026-08-11T21:06:04.01|
   |     |          |                        |     |5412Z', 45, 8, 'oshad', '1234567', 'user', 'osha', 'uid1'); UNIQUE constraint failed: par_users_2026|
   |     |          |                        |     |_08_00_d14_insert_timestamp.username                                                                |
829|    1|operator_1|Tue Aug 11 21:06:09 2026|Error|Error executing SQL from file: /app/AnyLog-Network/data/watch/mydb.users.2026_08_00_d14_insert_times|
   |     |          |                        |     |tamp.0.00ac17473055b70d6f49cda1f974b262.0.45.8.260811210603.1786482364.insert.sql                   |
830|    1|operator_1|Tue Aug 11 21:06:09 2026|Error|Failed to process SQL from file: /app/AnyLog-Network/data/watch/mydb.users.2026_08_00_d14_insert_tim|
   |     |          |                        |     |estamp.0.00ac17473055b70d6f49cda1f974b262.0.45.8.260811210603.1786482364.insert.sql                 |
```

> The rejection shows up at every stage the row passes through: the initial REST-facing failure 
> ("Failed to INSERT streaming data...") on `rest_0`, and the same `UNIQUE constraint failed` error again on 
> `operator_0` and `operator_1` as the cluster's watch-folder mechanism processes the insert file. Use 
> `get error log` to confirm a constraint is actually being enforced, and to diagnose rejected inserts in general.

## 4. Query the Table from Any Node

Applications do not need to know which physical node hosts the table. A query can be submitted to any AnyLog node in 
the network. The metadata layer identifies the node or nodes hosting the requested table and directs the query to the 
appropriate location. The query is executed where the data resides, and the results are returned to the requesting node.
This provides a single logical view of the data while allowing the table and its data to remain distributed.

**Example:**

```anylog
AL a4ee723b4064-acme-query1 +> run client () sql mydb format=table select username, password, role, email, associds from users
[4]

username password role  email associds
-------- -------- ----- ----- --------
oshad     1234567 admin osha  uid1
nwarn     7543216 user  nsha  uid12
{"Statistics":[{"Count": 2,
                "Time":"00:00:00",
                "Nodes": 1}]}
```