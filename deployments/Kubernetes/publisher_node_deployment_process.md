# Deployment Process
The following provides insight the work being done in the background to deploy the Operator node. 

For directions to start a master node please visit the [publisher node](publisher_node.md) document.

## Steps
1. Set parameters such as:
   * hostname
   * Internal & External IPs (backend of AnyLog if not preset in configuration)
   * `ENV` parameters from configuration into AnyLog parameters  
```anylog
hostname = get hostname
node_name=$NODE_NAME
company_name=$COMPANY_NAME
anylog_server_port=$ANYLOG_SERVER_PORT
...
```

2. Connect to TCP & REST 
```anylog
run tcp server !external_ip !anylog_server_port !ip !anylog_server_port
run rest server !ip !anylog_rest_port

# If declared run message broker 
run message broker !external_ip !anylog_broker_port !ip !anylog_broker_port
```

3. Connect to databases almgm and create tsd_info table 
```anylog
connect dbms almgm where type=!db_type and ip=!db_ip and port=!db_port and user=!db_user and password=!db_passwd
create table tsd_info where dbms=almgm
```
<p style="color: gray; size: 90%">`almgm.tsd_info` contains all metadata information about files injested. Other tables 
in almgm contain information regarding data ingested in peer  nodes in the same  cluster.</p>

5. (Optional) Connect to `system_query`
```anylog
connect dbms system_query where type=sqlite and memory=true  
```

6. Set scheduler 1 & blockchain sync 
```anylog 
run scheduler 1
run blockchain sync where source=blockchain_source and time=!sync_time and dest=blockchain_destination and connection=!ledger_conn
```

8. Declare Publisher Node on the metadata layer 
```anylog
<new_policy = {"master": {
    "hostname": !hostname,
    "name": !node_name,
    "ip" : !external_ip,
    "local_ip": !ip,
    "company": !company_name,
    "port" : !anylog_server_port.int,
    "rest_port": !anylog_rest_port.int,
    "loc": !loc,
    "country": !country,
    "state": !state, 
    "city": !city
}}>

do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```


10. Run MQTT (if set)   
```anylog
<run mqtt client where broker=!broker and port=!port and log=!mqtt_log and topic=(
   name=!mqtt_topic_name and 
   dbms=!mqtt_topic_dbms and 
   table=!mqtt_topic_table and 
   column.timestamp.timestamp=!mqtt_column_timestamp and
   column.value=(value=!mqtt_column_value and type=!mqtt_column_value_type)
)>
```
11. (Optional) Send data to specific operator nodes -- needs to be configured manually 
    * when using `data distribution`, the table value can be set to be specific or all (`*`) tables in a given database 
    * data coming from a publisher node can be distributed to multiple operators with `and dest ...` added. 
```anylog 
set data distribution where dbms={DB_NAME} and table={TABLE_NAME} and dest={DESTINATION_IP}:{DESTINATION_PORT} 
```

12. Deploy publisher 
```anylog
<run publisher where
    compress_json=!compress_file and
    compress_sql=!publisher_compress_file and
    master_node=!ledger_conn and
    dbms_name=!dbms_file_location and
    table_name=!table_file_location
>
```

 

13. (Manually) Validate processes are running
```anylog
AL anylog-publisher +> get processes

    Process         Status       Details                                                                      
    ---------------|------------|----------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.104.180.110:32248, Threads Pool: 6                        |
    REST           |Running     |Listening on: 172.104.180.110:32249, Threads Pool: 5, Timeout: 20, SSL: None|
    Operator       |Not declared|                                                                            |
    Publisher      |Running     |                                                                            |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                  |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                              |
    Distributor    |Not declared|                                                                            |
    Blobs Archiver |Not declared|                                                                            |
    Consumer       |Not declared|                                                                            |
    MQTT           |Running     |                                                                            |
    Message Broker |Running     |Listening on: 172.104.180.110:32250, Threads Pool: 4                        |
    SMTP           |Not declared|                                                                            |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes                |
    Query Pool     |Running     |Threads Pool: 3                                                             |
    Kafka Consumer |Not declared|                                                                            |
```
