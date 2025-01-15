# Blobs by Example 

AnyLog / EdgeLake enables storage of both SQL and non-SQL data, such as images, videos, and other file formats. For 
non-SQL data, storage options include file-based systems or NoSQL databases like MongoDB.

This document provides step-by-step instructions for deploying and managing blob data. For a detailed architectural 
explanation of blob management, refer to the [image mapping document](../image%20mapping.md).

**What are blobs**: Binary Large Objects (BLOBs) are collections of binary data stored as single entities. Examples 
include PDFs, images, and videos. Due to their size and format, blobs cannot be effectively stored in standard SQL 
databases. Instead, they are managed using NoSQL solutions (e.g., MongoDB) or file-based storage systems.


## Node Setup 
The following directions are automatically done using user provided configurations when deploying via docker-compose. 

1. Blob data will be sent into AnyLog/EdgeLake via either REST or Message Broker service 
```anylog
# Sample connection to REST service
<run rest server where
    external_ip=!ip and external_port=!anylog_rest_port and
    internal_ip=!overlay_ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

 # Sample connection to Message Broker service
 <run message broker where
    external_ip=!ip and external_port=!anylog_broker_port and
    internal_ip=!!overlay_ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>
```

2. Connect to both SQL and NoSQL databases 
```anylog
# SQL database 
<connect dbms !default_dbms where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port
>

# NoSQL database 
<connect dbms !default_dbms where
    type=!nosql_type and
    ip=!nosql_ip and
    port=!nosql_port and
    user=!nosql_user and
    password=!nosql_passwd
>
```

**Output**: Notice that while both NoSQL and SQl use `!default_dbms` as the database name for both SQL and NoSQL, 
AnyLog/EdgeLake is smart enough to rename NoSQL with `blob_` at the start of the database name.   
```shell
Logical DBMS Database Type Owner  IP:Port         Configuration                                Storage                                       
------------|-------------|------|---------------|--------------------------------------------|---------------------------------------------|
blobs_edgex |mongo        |user  |127.0.0.1:27017|                                            |Blobs Persistent                             |
edgex       |sqlite       |user  |Local          |Autocommit On, Fsync full (after each write)|/app/AnyLog-Network/data/dbms/edgex.dbms     |
```

3. Enable blobs archiving service
```anylog 
<run blobs archiver where
    dbms=true and
    folder=false and
    compress=true and
    reuse_blobs=true
>
```


## Accept data 
The process of accepting data is combined of two parts, data mapping and subscribing to the policy. 

From this point, the directions will utilize the logic for getting image data from 
<a href="https://github.com/AnyLog-co/Sample-Data-Generator" target="_blank">Sample Data Generator</a>. 
Mapping for other data-sets can be found in 
<a href="https://github.com/AnyLog-co/deployment-scripts/tree/main/demo-scripts" target="_blank">deployment-scripts/demo-scripts</a>. 
