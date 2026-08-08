---
title: "Managing Relational (OLTP) Data in AnyLog"
description: "OLTP data"
layout: page
---
<!---
### 📜 Change Log
    - 2026-08-04 | Ori Shadmon | OLTP data processing 
--> 

# OLTP & Historical Data 

AnyLog is designed and optimized for real-time, time-series sensor data. Its core capabilities—including high-throughput 
ingestion, automatic schema generation, data partitioning, retention policies, and distributed querying—are built around 
continuously growing datasets where records are appended over time.

At the same time, AnyLog can also integrate with conventional relational (OLTP) data when users need to expose existing 
relational datasets or manage non-time-series tables alongside their sensor data. 
Examples include users, configuration records, assets, equipment metadata, and other reference information that changes 
infrequently and benefits from database constraints such as UNIQUE, primary keys, foreign keys, and indexes.

For these types of tables, the recommended approach is to create and manage the schema directly in the underlying 
logical database (for example, PostgreSQL or SQLite). This allows the database engine to enforce relational constraints 
while AnyLog continues to provide access to the data through its metadata layer and query framework.

The recommended design is to let the relational database manage relational behavior (constraints, keys, indexes, and 
transactions) while AnyLog provides metadata management, distributed discovery, querying, and optional ingestion.

This approach also keeps the lifecycle of the two data types independent. Time-series sensor data can continue to 
leverage partitioning and retention policies, while relational tables remain permanent, non-partitioned datasets that 
are managed using standard database practices.

The remainder of this document demonstrates this approach, including how to create a constrained relational table in the 
logical database, register it with AnyLog, and query it alongside time-series data.

**Typical use cases include:**
1. Static or slowly changing OLTP data, such as users, devices, assets, equipment metadata, and configuration records.
2. Historical [aggregation tables](./02-2%20Data%20Aggregations.md) (hourly, daily, weekly, etc.) that are maintained independently of the raw time-series data and are intended to be retained indefinitely.

## Considerations

This workflow is intended primarily for existing relational (OLTP) data that already exists in an underlying logical 
database and needs to be exposed through AnyLog.

Examples include:
- User/account information
- Asset metadata
- Configuration records
- Other application-managed relational data

In this scenario, the user is responsible for creating the SQL schema and defining the corresponding AnyLog table and 
cluster policies so that AnyLog can discover and query the data.

When creating new tables from scratch, the recommended approach is different. If the table is intended to be managed by 
AnyLog but should not follow time-series retention behavior (for example, aggregation or historical summary tables), 
create the table using the standard AnyLog workflow and disable partitioning.

## Processing 

The following creates a sample table called _users_. 

If this is a brand-new table with no custom schema requirements (e.g. no UNIQUE constraints, specific column types, or 
other manipulation of the `CREATE TABLE` statement beyond AnyLog's defaults), complete steps 1–2, then skip to step 7. 
AnyLog will automatically generate the table schema, create the corresponding table and cluster policies, and execute 
the `CREATE TABLE` statement when the first data batch arrives — steps 3–6 are only needed when you must define or 
register the schema yourself.

1. Make sure the logical database you want to use is actually connected to the operator node.

2. Disable partitioning for static table [issue-192]
```anylog
partition exclude [db name] [table name]
```
> Static relational tables should generally not be partitioned because they are not subject to time-based retention 
> policies. Partitioning is intended for continuously growing time-series datasets.

3. make sure there's no _table_ or _cluster_ logical policy with the same dbms and table name. If either one already 
exists then it cannot be used. Similarly, a _table_ policy is not used without a "child" _cluster_, and a child _cluster_ 
isn't used without a _table_ policy.
```anylog
blockchain get table where name=users and dbms=my_db

blockchain get cluster where table[name] = users and table[dbms] = my_db 
```

4. An AnyLog policy create table - the user needs to decide whether they want to publish data into the table via 
AnyLog or not. If data will be inserted through AnyLog (southbound interfaces or REST), include the AnyLog system columns 
(`row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`) required for replication and HA/DR. If the table will only be 
managed directly through the relational database, these columns and correlated keys are not needed. 

**The SQL**
```sql
CREATE TABLE IF NOT EXISTS users(
    row_id SERIAL PRIMARY KEY,  
    insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),  
    tsd_name CHAR(3),  
    tsd_id INT,
    
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'operator', 'viewer')),
    email TEXT,
    assoc_ids TEXT
);

CREATE INDEX users_tsd_index ON users(tsd_name, tsd_id); 
CREATE INDEX users_insert_timestamp_index ON users(insert_timestamp);
```

> Since AnyLog connects seamlessly to multiple SQL logical database, you need to make sure the SQL is supported by both 
> if using both, otherwise choose SQL syntax supported by all target database engines if the same table definition will 
> be deployed across multiple logical databases.

```anylog 
<new_policy = {
  "table": {
    "dbms": "my_db",
    "name": "users",
    "create": "CREATE TABLE IF NOT EXISTS users(row_id SERIAL PRIMARY KEY, insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(), tsd_name CHAR(3), tsd_id INT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT NOT NULL CHECK (role IN ('admin', 'operator', 'viewer')), email TEXT, assoc_ids TEXT\n);\n\nCREATE INDEX users_tsd_index ON users(tsd_name, tsd_id);\nCREATE INDEX users_insert_timestamp_index ON users(insert_timestamp);"
  }
}>

blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

# Optionally create table via AnyLog
create table users where dbms=my_db
```

5. Based on the operator node hosting the data, locate the parent cluster. 

```anylog
cluster_id = blockchain get operator where name = !node_name bring [*][cluster] 
cluster_name = blockchain get cluster where id = !cluster_id bring [*][name]
```

6. Associate the table with the appropriate cluster 

```anylog
<new_policy = {
    "cluster": {
      "parent": !cluster_id,
      "name": !cluster_name,
      "company": !company_name,
      "table": [        {
          "dbms": "my_db",
          "name": "users",
          "status": "active"
        }]
    }
}>

blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

7. Insert data. If the table includes the AnyLog HA/DR system columns (`row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`), 
data must be inserted through AnyLog via a [southbound source](../04-%20Southbound%20Interfaces) — inserting directly 
through the physical database's CLI will leave those columns unpopulated, since the database has no way to generate 
their values itself. If the table does not include those columns, insert data directly via the physical database's 
CLI.

**AnyLog Insertion**
```shell
curl -X PUT http://127.0.0.1:32149 \
  -H "type: json" \
  -H "dbms: my_db" \
  -H "table: users" \
  -H "mode: streaming" \
  -H "Content-Type: text/plain" \
  -d '{"username":"admin","password":"mog1234","role":"admin","email":"","assoc_ids":""}'
```

**SQL Insertion**:
```shell
psql -d my_db -c "INSERT INTO users (username, password, role, email, assoc_ids) VALUES ('admin', 'mog1234', 'admin', '', '');"
```