---
title: "Accessing MongoDB via AnyLog"
description: "Connect AnyLog to MongoDB for blob storage, using the same connect/create/drop workflow as a SQL database, plus a worked mapping-policy example for image/video data from EdgeX."
layout: page
source_path: "deployments/Support/02 configuring mongodb.md"
---

<!---

### 📜 Change Log

-  2026-07-28 | Ori Shadmon | Rewrote steps 6 and 7 entirely — they were using the unrelated kizu/object-detection payload and query from Databases.md, which doesn't match this doc's actual mapping policy (an EdgeX binary reading: `source`/`timestamp`/`file`/`file_type`, no `class`/`bbox`/`score`/`status`, and video not image). Built a payload matching the real schema (readings array with `deviceName`/`binaryValue`/`mediaType`) and updated the query's columns and `-->` annotation accordingly (dropped `description`, which was specific to drawing a bbox overlay that doesn't apply to plain video)
- 2026-07-28 | Ori Shadmon | Reconciled the dbms/table names across steps 3, 6, and 7 — they previously named three different targets (`test.edgex_data` from the mapping policy, `ntt.deeptector` in the published payload, `edgex.images` in the query), meaning the walkthrough as written would publish data to one place and query an empty one. Updated the payload and query to match the policy's fixed target (`test.edgex_data`), since that's the one actually enforced — flag if the intent was instead to make the policy dynamic (`bring [dbms]`/`bring [table]`) so the payload's own values would be the ones that matter. Noted new evidence on `User-Agent` vs `AnyLog-Agent` (now 2-of-3 examples across the doc set favor `AnyLog-Agent`)
- 2026-07-28 | Ori Shadmon | Fixed `!default_dbms` being used in step 2 before it's defined (moved the assignment earlier); quoted three unquoted dictionary-variable references in the mapping policy JSON (`id`/`dbms`/`table` — same bug fixed twice elsewhere this session); fixed `"default": "now"` → `"now()"` to match every other example's function-call convention; moved the `source` field into `schema` (it was a sibling of `schema` rather than a member of it, and the only field of its kind missing a `type`) — flag if `source` is meant to be a distinct top-level concept instead. Added a missing example for step 1 and typo/grammar fixes
- 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 

--->

MongoDB is a schema-less physical database that's intended for document-oriented data. The NoSQL logic stores data in
a flexible BSON (Binary JSON) format, allowing for dynamic schemas and easy adaptation to changing application needs.

> For most internal or application-embedded uses, you can use the Community Edition for free under SSPL without needing
> a commercial license, as long as you are not offering MongoDB itself as a hosted service.

## Using MongoDB

Unlike other blob storage options integrated with AnyLog, MongoDB has seamless compatibility with SQL databases due to
its nature. Object storage (S3, MinIO, Akave) holds opaque blobs with no internal structure to query, while MongoDB's
documents are already field-structured, mapping much more directly onto SQL's row/column model — making it a great
tool to demonstrate the relationship between data and blob storage.

> MongoDB has the same interaction commands with AnyLog as a [SQL database](01-%20SQL%20Storage.md) for dis/connecting
> and creating / dropping databases (collections in MongoDB) and tables.

1. Connect to SQL-based database

```anylog
default_dbms = test

connect dbms !default_dbms where type=psql and user=anylog and password=demo and ip=127.0.0.1 and port=5432
```

2. Connect to MongoDB

```anylog
mongo_db_ip = 127.0.0.1
mongo_db_port = 27017
mongo_db_user = admin
mongo_db_passwd = passwd

<connect dbms !default_dbms where 
    type=mongo and 
    ip=!mongo_db_ip and 
    port=!mongo_db_port and 
    user=!mongo_db_user and 
    password=!mongo_db_passwd
>
```
> Note that the logical "database" for blobs and SQL need to be the same. However, the blob database would be
> annotated with `blob_[db name]` when doing `get databases`.

3. Declare Policy (based on data coming from EdgeX)

```anylog
policy_id = image-data 
default_dbms = test 
table_name=edgex_data
 
<mapping_policy = {
    "mapping": {
        "id": "!policy_id",
        "dbms": "!default_dbms",
        "table": "!table_name",
        "readings": "readings",
        "schema": {
            "source": {
                "bring": "[deviceName]",
                "default": "12"
            },
            "timestamp": {
                "type": "timestamp",
                "default": "now()"
            },
            "file": {
                "blob": true,
                "bring": "[binaryValue]",
                "extension": "mp4",
                "apply": "base64decoding",
                "hash": "md5",
                "type": "varchar"
            },
            "file_type": {
                "bring": "[mediaType]",
                "type": "string"
            }
        }
    }
}>

blockchain prepare policy !mapping_policy
blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn
```

> Note this policy assigns `dbms`/`table` as fixed values (`!default_dbms`/`!table_name`) rather than pulling them
> from each incoming payload via `bring` — so every message ingested through this policy lands in `test.edgex_data`
> regardless of what `dbms`/`table` fields the payload itself contains.

4. Set blobs archiver configurations - The example specifies to store, compress and reuse (based on file hash) blob
data within the NoSQL database (MongoDB).

```anylog
<run blobs archiver where
    dbms=true and
    folder=false and
    compress=true and
    reuse_blobs=true
>
```

5. Initiate `msg client` process with REST (POST)

```anylog
<run msg client where broker=rest and user-agent=anylog and log=false and topic=(
  name=anylogedgex-images and 
  policy=!policy_id
)>
```

6. Begin publishing data into AnyLog agent

This mapping resolves `source`/`timestamp`/`file`/`file_type` relative to each element of the top-level `readings`
array (none of them are flagged `"root": true`, so none reach back up to the event's top level) — so the payload
needs an EdgeX-style event with each reading carrying its own `deviceName`, `binaryValue`, and `mediaType`:

```shell
curl -X POST http://{Operator IP}:{Operator Port} \
  -H "command: data" \
  -H "topic: anylogedgex-images" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '{
    "apiVersion": "v2",
    "id": "b91c1e0c-6e2e-4ee1-9f8b-7b2ed3e0a111",
    "deviceName": "factory-cam-03",
    "profileName": "SecurityCameraProfile",
    "sourceName": "ClipCapture",
    "origin": 1782500000000000000,
    "readings": [
        {
            "id": "6a2f9f5b-6e2e-4ee1-9f8b-7b2ed3e0a222",
            "deviceName": "factory-cam-03",
            "resourceName": "ClipCapture",
            "mediaType": "video/mp4",
            "binaryValue": "AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAAIZnJlZQAAB..."
        }
    ]
}'
```

7. Query data

With this policy, each row has `source`, `timestamp`, `file`, and `file_type` — no `class`/`bbox`/`score`/`status`,
since those belonged to the unrelated object-detection example. The `description` annotation (which drew a `bbox`
rectangle overlay) doesn't apply to a plain video file, so it's dropped here — only `selection` is needed, to
locate the file itself:

```anylog
<run client () sql test 
    extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format=json and timezone=Europe/Dublin 
    "SELECT 
        timestamp, file, file_type, source 
    FROM 
        edgex_data 
    WHERE timestamp >= now() - 1 hour AND timestamp <= NOW() 
    ORDER BY timestamp desc  --> 
        selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file)">
```

> Please review [Extracting blobs](../../10-%20Edge%20Data%20Manager/01-%20EDM.md) in Edge Data Manager section.