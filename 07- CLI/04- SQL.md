---
title: "Databases"
description: "The database and storage backends AnyLog can connect to — SQL, NoSQL, blob/object storage, and vector search."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Correction: `-->` is confirmed real `sql` syntax, not GUI-behavior notation — my previous edit had wrongly stripped it out of the query. Restored it and documented the query's 3 parts (execution directions, the `SELECT` statement, and the `selection`/`description` annotation relating the SQL data to its associated blob file) per clarification | |
 | 2026-07-28 | Ori Shadmon | Resolved the `-->` question: since it isn't confirmed as real `sql` syntax, moved `selection`/`description` out of the query string entirely — the query now ends cleanly at `ORDER BY timestamp desc`, and what a GUI should do with the extended columns (locate/open the file, render the bbox overlay) is now stated as plain-English prose below it instead of embedded pseudo-syntax | |
 | 2026-07-28 | Ori Shadmon | Merged the `root: true` mechanism explanation with the new intro sentence instead of stacking both; fixed the query's missing opening quote (matching the convention used elsewhere in the doc set — every other multi-line `sql` example opens the quote right before `SELECT`); flagged that fixing the quote this way places the `--> selection/description` annotations *inside* the literal query string, which leans toward them being real syntax rather than GUI-behavior notation — still unconfirmed. Typo/clarity fixes ("base64d" → "base64", "precent" → reworded as a 0–1 confidence score, doubled "the the", bbox "each corner" → clarified as two corners, "cellular component" flagged) | |
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

## Supported SQL databases

* PostgreSQL
* SQLite

## Supported NoSQL databases

* MongoDB

## Supported blob / object storage

* Local Filesystem store
* S3-compatible object storage
  * AWS S3
  * MinIO
  * Akave (Filecoin-backed, S3-compatible object storage)

## Vector databases

In addition, we also support Milvus, a vector-based database used for embeddings and similarity search.

---

## How SQL and Blob Storage Connect

Sensor/device data and blob files (images, video, model output, etc.) live in fundamentally different kinds of
storage, so AnyLog uses a **mapping policy** to keep them connected. When blob data comes in, the actual file goes
into the underlying object/blob store, while the SQL row AnyLog creates keeps a lightweight reference to that file
(a hash, filename, and path) alongside whatever structured data arrived with it.

When a user later queries the SQL table — ideally from a GUI rather than the raw CLI — the returned row already
contains everything needed to also fetch and display the associated file: the query result points directly at
which blob to open, without the user needing to separately search the blob store.

### Example: an object-detection model's output

The following example shows a manufacturing component with a defective region detected (`kizu` is a common
surface-scratch defect class in this kind of inspection data).

The `file_content` is the image itself (base64 encoded), showing the defect. `detection` is a list — each entry is
one region where an issue was found:
* `bbox` — the bounding box marking where the issue resides, given as two corners: `[x1, y1, x2, y2]`
  (top-left, then bottom-right)
* `score` — the model's confidence in that detection, as a fraction from 0 to 1

Since this payload combines both nested/complex data (`detection`) and blob storage (`file_content`), AnyLog needs
to utilize mapping and `run msg client` in order to match between the JSON and where/how to store the data.

This is also a good illustration of what the `"root": true` mapping parameter actually does. `"readings":
"detection"` shifts every other `schema` field to resolve *relative to each element of the `detection` array* — so
`class`/`bbox`/`score` correctly pull from each detection. But `file_content` and `status` aren't inside
`detection` at all; they're siblings of it at the top level of the incoming JSON. `"root": true` on `file` and
`status` is what tells the mapping to reach back up to the top-level JSON for those two fields instead of trying
to find them inside each detection. Each detection becomes its own row, and every one of those rows carries the
same blob reference and status alongside its own `class`/`bbox`/`score` — since there was only one image here, all
four detection rows point at the same file.

**Process**:

1. User defines a mapping policy + `run msg client` to match between the content and how to store it on the database.
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

3. Once the buffer is full (which happens faster with blob data than with plain sensor data, since blob payloads
   are larger), query the results from the [Edge Data Manager](../10-%20EDM%20tool%20(Edge%20Data%20Manager)) or
   other third-party apps.

```anylog
<run client () sql edgex 
    extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format=json and timezone=Europe/Dublin 
    "SELECT 
        timestamp, file, class, bbox, score, status 
    FROM 
        images 
    WHERE 
        timestamp >= now() - 1 hour AND timestamp <= NOW() 
    ORDER BY timestamp desc  --> 
        selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file) -->  
        description (columns: bbox as shape.rect and score)">
```

This query breaks down into 3 parts.

**Section 1 — how to execute the query:**
```anylog
sql edgex extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format=json and timezone=Europe/Dublin
```
The `extend` parameter lets the query also return the source of each row's data — the node name, IP:port, and
database/table — alongside the actual data itself. This lets a user or program distinguish where each row came
from when analyzing the same type of data across multiple nodes.

**Section 2 — the actual `SELECT` statement:**
```sql
SELECT 
    timestamp, file, class, bbox, score, status 
FROM 
    images 
WHERE 
    timestamp >= now() - 1 hour AND timestamp <= NOW() 
ORDER BY timestamp desc
```

**Section 3 — the `-->` annotation:** since this data is split across two kinds of storage (SQL for the
time-series/detection data, blob storage for the actual image), `-->` tells the query node how the two relate —
which columns locate the file, and how to interpret the SQL columns describing what's in it:
```anylog
selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file) -->
description (columns: bbox as shape.rect and score)
```
* **`selection`** maps the `extend`-provided location columns (`@ip`, `@port`, `@dbms_name`, `@table_name`) plus
  `file` to the fields actually needed to locate and retrieve the associated blob.
* **`description`** tells the client how to render the SQL columns as an annotation over that blob: `bbox` as a
  rectangle shape (`shape.rect`) drawn on the image, alongside `score`.