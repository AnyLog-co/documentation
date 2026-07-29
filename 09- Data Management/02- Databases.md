---
title: "Databases"
description: "The database and storage backends AnyLog can connect to — SQL, NoSQL, blob/object storage, and vector search."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Split "NoSQL / Blob storage" into two separate categories (NoSQL document DB vs. object/blob storage — different technology categories); restructured the S3-compatible bullets so AWS S3/MinIO/Akave are siblings rather than MinIO/Akave nested under AWS S3; fixed "PostgresSQL" → "PostgreSQL"; added a brief note on what Akave actually is; added frontmatter/H1 (missing entirely); typo/grammar fixes | |
--->

# Databases

AnyLog can connect to an array of databases that store data both as SQL and blob-based storage.

Blob storage refers to storing files (e.g. videos, images, AI models) as objects rather than structured rows, in
object storage systems designed for exactly that.

Having an array of database types readily accessible via a unified platform and language allows DBAs and IT teams
to easily manage different types of data. This also enhances AI / ML capabilities such as federated learning and
real-time decision making, since there's no need to gather information from different sources — AnyLog does that
for you automatically.

### Supported SQL databases

| DB Type | Usage | Examples | 
|:---:|:---:|:---:|
| SQL-based | Store time-series data | SQLite and PostgresSQL |
| Blob Storage | FIle storage | MongoDB and S3-compatible file stoe | 
| Vector Databases | Support for Indexing and searching content stored on the AynLog network  | Milvus |


## How SQL and Blob Storage Connect

Sensor/device data and blob files (images, video, model output, etc.) live in fundamentally different kinds of
storage, so AnyLog uses a **mapping policy** to keep them connected. When blob data comes in, the actual file goes
into the underlying object/blob store, while the SQL row AnyLog creates keeps a lightweight reference to that file
(a hash, filename, and path) alongside whatever structured data arrived with it.

When a user later queries the SQL table — ideally from a GUI rather than the raw CLI — the returned row already
contains everything needed to also fetch and display the associated file: the query result points directly at
which blob to open, without the user needing to separately search the blob store.

### Example: an object-detection model's output

The following example shows a cellular component with a defective region detected.

The `file_content` is an image (base64d encoded) with the error.

While `detection` is the region where the issue resides. 
* `bbox` - the coordinates of each corner within the square where the issue resides 
* `score` - precent of accuracy of the bbox. 

Since the data is dealing with both complex data formatting (`detection`) and blob storage (`file_content`), AnyLog 
needs to utilize mapping and `run msg client` in order to match between the JSON and where/how to store the data.  

The example is a good illustration of `"root": true` param for mapping, as the content coming in data that's critical 
for storage both inside a sub-JSON list (ie `detection`) and outside of it - `file_content` and `status`.  


**Process**: 

1. User defines a mapping policy + run msg client to match between the content and how to store it on the database. 
```json
{
  "mapping": {
      "id": "!policy_id",
      "dbms": "bring [dbms]",
      "table": "bring [table]",
      "readings": "detection",
      "schema": {
          "timestamp": {
              "type": "timestamp",
              "default": "now()"
          },
          "file": {
              "root" : true,
              "blob" : true,
              "bring" : "[file_content]",
              "extension" : "jpeg",
              "apply" : "base64decoding",
              "hash" : "md5",
              "type" : "varchar"
          },
          "class": {
              "type": "string",
              "bring": "[class]",
              "default": ""
          },
          "bbox": {
              "type": "string",
              "bring": "[bbox]",
              "default": ""
          },
          "score": {
              "type": "float",
              "bring": "[score]",
              "default": -1
          },
          "status": {
              "root": true,
              "type": "string",
              "bring": "[status]",
              "default": ""
          }
      }
  }
}
```

2. Device generates data 
```json
{
    "id": "f85b2ddc-761d-88da-c524-12283fbb0f21",
    "dbms": "ntt",
    "table": "deeptector",
    "file_name": "20200306202533614.jpeg",
    "file_type": "image/jpeg",
    "file_content": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD",
    "detection": [
            {"class": "kizu", "bbox": [666, 275, 682, 291], "score": 0.83249},
            {"class": "kizu", "bbox": [669, 262, 684, 277], "score": 0.83249},
            {"class": "kizu", "bbox": [688, 261, 706, 276], "score": 0.72732},
            {"class": "kizu", "bbox": [698, 277, 713, 292], "score": 0.72659}
    ],
    "status": "ok"
}
```


3. Once the the buffer is full, usually much faster with blob storage than just sensor data, query the results from 
the [Edge Data Manager](../10-%20EDM%20tool%20(Edge%20Data%20Manager)) or other third party apps.  

```anylog
<run client () sql edgex 
    extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format=json and timezone=Europe/Dublin 
    SELECT 
        timestamp, file, class, bbox, score, status 
    FROM 
        images 
    WHERE timestamp >= now() - 1 hour AND timestamp <= NOW() 
    ORDER BY timestamp desc  --> 
        selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file) -->  
        description (columns: bbox as shape.rect and score)">
```

> The `-->` in the query is a pointer between the SQL database and the blob storage layer so that the aggregated results 
> in the query node is able to match file (copied from operator) with row corresponding SQL row.  