---
title: "File Processing"
description: ""
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | descriptor on file processing | |
--->

# File Processing

## Intro

AnyLog hosts data on nodes configured as **Operator** nodes. Any connected node can act as an Operator as long as it's connected to the right logical databases and has the `run operator` process active.

Data reaches the network either through a <a href="../04-%20Southbound%20Interfaces" target="_blank">southbound service</a> or by writing directly to the `!watch_dir`. This document covers how a file moves from ingestion to storage, and the commands used to manage files along the way.

## Operator vs Publisher

- **Operator** — an agent that stores data directly. When a query node needs data, it queries the Operator(s) that hold it.
- **Publisher** — an agent that distributes incoming data across multiple Operators. Used for large-scale, fast-paced data that a single Operator can't process quickly enough.

> Publisher is an enterprise feature, same as <a href="./03-%20High%20Availability.md" target="_blank">High-Availability and Data Resilience</a>. 
> See <a href="../07-%20CLI/02-1%20Nodes.md" target="_blank">nodes.md</a> for more detail.

## Tree Structure

Deploying a node builds a directory tree with `create work directories`:

```anylog
set anylog home /app
create work directories
```

```tree
/app/AnyLog-Network/
├── anylog
│   └── node_id.pem
├── blockchain
│   ├── blockchain.json
│   ├── blockchain.new
│   └── blockchain.old
└── data
    ├── archive
    │   └── 26
    │       └── 07
    │           └── 10
    │               ├── monitoring.node_insight.0.035b63b3bdd2a0d6769cb1cb7bfea8d9.0.216.22.260710225015.json.gz
    │               └── monitoring.node_insight.0.039b978a8cb346472ee6b52eea9a17de.0.216.44.260710230146.json.gz
    ├── bkup
    │   └── monitoring.node_insight.2026_07_10_01_h12_insert_timestamp.0.869cd2c7862a7c04ccbbc2e4a88fcd84.0.216.1.260710223953.1783723193.insert.sql.1783723194.gz
    ├── blobs
    ├── bwatch
    ├── dbms
    │   ├── almgm.dbms
    │   ├── blockchain.dbms
    │   ├── monitoring.dbms
    │   └── persistence.dbms
    ├── distr
    ├── error
    ├── pem
    ├── prep
    ├── tmp
    └── watch
```

| Path | Variable | Description |
|---|---|---|
| `/app/AnyLog-Network/anylog/` | `!anylog_dir` | Keys (private and public) |
| `/app/AnyLog-Network/blockchain/` | `!blockchain_dir` | Blockchain file(s) |
| `/app/AnyLog-Network/blockchain/blockchain.json` | `!blockchain_file` | Latest copy of the blockchain (from `blockchain sync`) |
| `/app/AnyLog-Network/data/prep/` | `!prep_dir` | Manual content prep / decompressed files for analysis |
| `/app/AnyLog-Network/data/watch/` | `!watch_dir` | Files (SQL or JSON) awaiting processing into AnyLog |
| `/app/AnyLog-Network/data/archive/` | `!archive_dir` | Archived files |
| `/app/AnyLog-Network/data/error/` | `!err_dir` | Files that failed to process |
| `/app/AnyLog-Network/data/backup/` | `!bkup_dir` | Files backed up but not archived |
| `/app/AnyLog-Network/data/bwatch/` | `!bwatch_dir` | Watch directory for blobs |
| `/app/AnyLog-Network/data/blobs/` | `!blobs_dir` | Archive directory for blobs (when `file=true`) |

### File Structure (naming convention)

File names/paths can use dictionary keys: `!key` resolves against the **local** node's dictionary, `!!key` against the **remote** node's.

```commandline
[dbms name].[table name].[data source].[hash value].[instructions].[TSD member].[TSD ID].[TSD date].[file type]

# example:
monitoring.syslog.0.fc1524ad102f035b83a6b7b01aeac3f5.0.165.311239.260726140705.json.gz
```

| Section | Meaning |
|---|---|
| dbms name | Target database |
| table name | Target table |
| data source | ID of the data source generating the data |
| hash value | Hash of the file |
| instructions | ID of the policy mapping the file to a table structure (`0` if none) |
| TSD member | Member ID, if sent by a cluster member |
| TSD ID | ID of the file in the TSD table |
| TSD date | 12-byte `YYMMDDHHMMSS` timestamp of when the file was processed |
| file type | `json` or `sql` |

## File Commands

Files land in `!watch_dir` (dropped by a southbound service or manually) and Operators process them automatically: read 
the file, derive the DB/table/mapping from its name, create the table if needed, and load the data. The commands below 
are the ones you'll reach for most often when managing files by hand.

### Copy a file (local)

```anylog
file copy !err_dir/data.json !prep_dir/json.data
```

### Copy a file to/from a remote node

```anylog
# local -> remote
run client (132.148.12.32:2048) file copy !source_dir/data.json !!prep_dir/json.data

# remote -> local
run client (10.0.0.78:2048) file get !!blockchain_file !blockchain_file
```
`!key` resolves on the local node, `!!key` on the remote node. Wildcards (`*`) work for copying multiple files to a directory, e.g. `file copy !prep_dir/* !!temp_dir/`.

### Move a file

```anylog
file move !prep_dir/my_file !watch_dir
```

### Delete a file

```anylog
file delete !prep_dir/my_file
```

### Test if a file exists

```anylog
file test !prep_dir/my_file
```
Returns `True` or `False`.

### Compress / decompress a file

```anylog
file compress source_file.dat new_file.gz
file decompress new_file.gz source_file.dat
```
Target name is optional (defaults to source name + `.gz` or `.dat`). Use `*` to compress/decompress all matching files in a directory.

### List files / subdirectories

```anylog
get files !err_dir
get directories !archive_dir

# on a remote node
run client (10.0.0.78:2048) get files !!err_dir
```