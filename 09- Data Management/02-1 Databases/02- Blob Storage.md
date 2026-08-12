---
title: "Blob Storage"
description: "Storing media content (images, video, ML models) within AnyLog's data management layer — the blobs archiver service, and querying blob data alongside SQL results."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Fixed table/command mismatches: `blob_dir` → `blobs_dir` (table didn't match its own Default column or the actual command); the command template used `file` where the table and worked example both use `folder` — templates now agree with both. Added the missing opening quote to both query examples in "Querying Blobs" (same fix already applied to the source query in Databases.md). Added frontmatter/H1/changelog (missing entirely). Typo fixes | |
--->

# Blob Storage

Blob storage is the ability to store media content (ex. images, videos and machine learning models) within AnyLog's
data management layer.

## Blobs Archiver

The data archiver is a process that manages blob data by pushing the blobs (like image, video and sound) to a
dedicated blobs database or to a dedicated folder (or both).

By default, the default deployment process enables the blobs archiver against filesystem storage unless specified
otherwise in the configurations. That way the service is guaranteed to exist when attempting to publish blob data
before trying services like MongoDB or S3 buckets.

* Define Blobs Archiver

| parameter | Details                                                                                                  | Default                             |
| ------------- |----------------------------------------------------------------------------------------------------------|-------------------------------------|
| bwatch_dir | A directory where the JSON data files with reference to the blobs data are placed as it's being buffered | The value assigned to `!bwatch_dir` |
| blobs_dir | A directory where blobs data is placed to be archived if `folder=true`                                    | The value assigned to `!blobs_dir`  |
| dbms | A boolean value to determine if blobs database is used                                                   | true                                |
| folder | A boolean value to determine if file is saved in a folder as f(date)                                     | false                               |
| compress | A boolean value to determine if compression is applied                                                   | false                               |
| reuse | A boolean value to determine whether to reuse blob files rather than keeping duplicates (based ob file hash)| false                               | 

```anylog
<run blobs archiver where 
    bwatch_dir = [data directory location] and 
    blobs_dir = [data directory location] and 
    dbms = [true/false] and 
    folder = [true/false] and 
    compress = [true/false]>
    
# Example     
run blobs archiver where dbms = true and folder = true and compress = false
```

* Check blobs archiver status

```anylog
get blobs archiver
```

## Querying Blobs

When blob data gets queried as part of the SQL request — example in
[02- Databases.md](../02-%20Databases.md#example-an-object-detection-models-output) — the SQL content gets
aggregated from across the network into a unified table within `system_query`, but the actual blobs can either
remain locally at the edge **or** get copied over into the query.

**Copying the content Over**:
```anylog
<run client () sql edgex 
    extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format=json and timezone=Europe/Dublin 
    "SELECT 
        timestamp, file, class, bbox, score, status 
    FROM 
        images 
    WHERE timestamp >= now() - 1 hour AND timestamp <= NOW() 
    ORDER BY timestamp desc  --> 
        selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file) -->  
        description (columns: bbox as shape.rect and score)">
```

**Keeping at the Edge**:
```anylog
<run client () sql edgex 
    info = (dest_type = rest) and extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format=json and timezone=Europe/Dublin 
    "SELECT 
        timestamp, file, class, bbox, score, status 
    FROM 
        images 
    WHERE timestamp >= now() - 1 hour AND timestamp <= NOW() 
    ORDER BY timestamp desc  --> 
        selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file) -->  
        description (columns: bbox as shape.rect and score)">
```

Notice that in the second example the request has `info = (dest_type = rest)`, which means forward the content live
but do not copy it from the edge to the query.