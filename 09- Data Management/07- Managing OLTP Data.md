---
title: "Managing Relational (OLTP) Data in AnyLog"
description: "OLTP data"
layout: page
---
<!---
### 📜 Change Log
- 2026-08-04 | Ori Shadmon | OLTP data processing 
- 2026-08-11 | Ori Shadmon | extended support from Moshe - including an example 
- 2026-08-11 | Ori Shadmon | split concept from worked example; added metadata vs. OLTP vs. time-series distinction

Note: this should stay the last conceptual document in Data Management. It is immediately followed by 
"Creating and Managing a Non-Time-Series Table," which walks through a full worked example.
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
logical database (for example, PostgresSQL or SQLite). This allows the database engine to enforce relational constraints 
while AnyLog continues to provide access to the data through its metadata layer and query framework.

The recommended design is to let the relational database manage relational behavior (constraints, keys, indexes, and 
transactions) while AnyLog provides metadata management, distributed discovery, querying, and optional ingestion.

This approach also keeps the lifecycle of the two data types independent. Time-series sensor data can continue to 
leverage partitioning and retention policies, while relational tables remain permanent, non-partitioned datasets that 
are managed using standard database practices.

## Where OLTP Fits: Metadata vs. OLTP vs. Time-Series

AnyLog data generally falls into three layers, each suited to a different kind of question:

- **Blockchain metadata** describes the identity and organization of assets—information that's useful for 
discovering, organizing, and understanding data across the network. It's a shared, verifiable record across nodes, 
which makes it a natural fit for device/sensor identity, factory structure, and other longer-lived records (e.g. 
purchase history or maintenance logs) where a consistent, trusted record across the network has value.
- **OLTP data** describes how a particular deployment operates—configuration that is typically deployment-specific 
rather than something that needs to be discoverable or compared network-wide.
- **Time-series data** describes observations over time—the continuously growing sensor readings AnyLog is built 
and optimized for.

Whether a given piece of information belongs on the blockchain, in an OLTP table, or isn't tracked at all depends on 
whether it needs to be discoverable/comparable network-wide (blockchain) or is operational detail specific to a 
given line or device (OLTP). This is a use-case decision rather than something AnyLog prescribes—some deployments 
track purchase/maintenance history on the blockchain, others just want fast access to raw data and don't use that 
layer at all.

**Example hierarchy:**

```
Factory A
├── Production Line 1
│   └── Pump P-101
│       └── Temperature Sensor TS-17
│
├── Production Line 2
│   └── Pump P-102
│       └── Temperature Sensor TS-18
│
└── Production Line 3
    └── Pump P-103
        └── Temperature Sensor TS-19
```

**Device Type Metadata** describes the type of device and is common regardless of where it's installed—this belongs 
on the blockchain because it describes capabilities and meaning that are useful across the network.

```
Device Type:
    Name: Temperature Sensor X100
    Manufacturer: Acme Sensors
    Supported Measurement: Temperature
    Protocol: BLE
    Engineering Unit: Celsius
```

**Device Instance Metadata** describes a specific physical asset—still metadata, because it describes the identity 
and location of an asset.

```
Device Instance:
    Device Type: Temperature Sensor X100
    Device Name: TS-17
    UID: A123456
    Purchase Date: 2025-01-15
    Firmware Version: 2.1.7
    Location: Factory A / Production Line 1
    Geolocation: 37.123,-121.456
```

**Operational Configuration (OLTP)** is where the distinction matters. Operating parameters are typically 
deployment-specific—two identical sensors may have different acceptable operating ranges depending on where they're 
installed:

```sql
CREATE TABLE device_range (
    device_uid VARCHAR PRIMARY KEY,
    device_name VARCHAR NOT NULL,
    min_value FLOAT NOT NULL,
    max_value FLOAT NOT NULL
);

INSERT INTO device_range VALUES
('A123456', 'TS-17', 0, 100);

INSERT INTO device_range VALUES
('B789012', 'TS-18', 10, 120);
```

A scheduler running at the edge can read this local configuration and evaluate incoming sensor values. If TS-17 
reports a value of 105, the scheduler knows it exceeded the configured limit for that specific installation and can 
generate an anomaly. This is a scheduler pattern, not a database constraint: (1) data is inserted, (2) a scheduler 
process checks incoming values against the OLTP range table, (3) if out of range, a message is sent—the table-policy 
tooling described in the companion example document isn't involved in this flow.

**Time-series data** remains the actual sensor observations:

```sql
CREATE TABLE TS_17 (
    timestamp TIMESTAMP,
    value FLOAT
);
```

```
2026-08-06 10:00:01, 27.4
2026-08-06 10:00:02, 27.5
2026-08-06 10:00:03, 27.6
```

**As a rule of thumb:**
- Blockchain metadata describes the identity and organization of assets.
- OLTP data describes how a particular deployment operates.
- Time-series data describes observations over time.

> AnyLog automatically creates an index for columns defined with the `TIMESTAMP` data type. Additional constraints 
> and indexes are typically needed on non-timestamp columns instead (e.g. sensor ID, username, or other lookup 
> fields)—see [Creating and Managing a Non-Time-Series Table](./07-1%20Creating%20and%20Managing%20a%20Non-Time-Series%20Table.md) 
> for how to define those.

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

**Typical use cases include:**
1. Static or slowly changing OLTP data, such as users, devices, assets, equipment metadata, and configuration records.
2. Historical [aggregation tables](./02-2%20Data%20Aggregations.md) (hourly, daily, weekly, etc.) that are maintained independently of the raw time-series data and are intended to be retained indefinitely.

## Two Ways to Register a Table

1. **Standard / autogenerated (default):** If the table has no custom schema requirements (no UNIQUE constraints, 
specific column types, or other manipulation of the `CREATE TABLE` statement beyond AnyLog's defaults), just push 
JSON data to the node. AnyLog automatically generates the table schema, creates the corresponding table and cluster 
policies, and executes the `CREATE TABLE` statement based on the data itself.
2. **Custom / manual:** If the table needs constraints, keys, or indexes other than AnyLog's default timestamp-based 
ones, define the `CREATE TABLE` statement yourself and register it—either by hand-writing the table policy, or by 
using a script to generate it from your SQL file. This path also requires disabling partitioning, since static 
relational tables shouldn't be subject to time-based retention.

See [Creating and Managing a Non-Time-Series Table](./07-1%20Creating%20and%20Managing%20a%20Non-Time-Series%20Table.md) 
for a full worked example of the custom/manual path.

## Dropping a Table

AnyLog has a built-in command for deleting the local table:

```anylog
drop table users where dbms=my_db
```

This drops the table from the local logical database and removes any associated partitions, if they exist. It does 
**not** remove the table policy from the blockchain, nor does it remove the table/data from other operators in the 
cluster. Removing the table definition from the blockchain is a separate operation, since it requires locating and 
removing the corresponding policy and then reloading/synchronizing the metadata.