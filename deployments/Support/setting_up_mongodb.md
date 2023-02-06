# Accessing MongoDB via AnyLog
The following is based on the example in `!local_scripts/sample_code/mongodb_process.al`, within AnyLog, to demonstrate 
accepting videos into AnyLog and storing them in MongoDB (and/or local folder). Directions to install MongoDB can be 
found [here](../database_configuration.md#mongodb). 

1. Connect to MongoDB  
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


3. Declare Policy (based on data coming from EdgeX) 
```anylog
policy_id = image-data 
default_dbms = test 
table_name=edgex_data
 
<mapping_policy = {
    "mapping": {
        "id": !policy_id,
        "dbms": !default_dbms,
        "table": !table_name,
        "source": {
            "bring": "[deviceName]",
            "default": "12"
        },
        "readings": "readings",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "default": "now"
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

4. Set blobs archiver configurations 

```anylog
<run blobs archiver where
    dbms=!blobs_dbms and
    folder=!blobs_folder and
    compress=!blobs_compress and
    reuse_blobs=!blobs_reuse
>
```

5. Initiate `mqtt client` process with local broker 

```anylog
<run mqtt client where  broker=local and port=!anylog_broker_port and log=false and topic=(
  name=anylogedgex-images and 
  policy=!policy_id
)>
```
