# Deployment Process
The following provides insight the work being done in the background to deploy the Operator node. 

For directions to start a master node please visit the [operator node](operator_node.md) document.

## Steps
1. Set parameters such as:
   * hostname
   * Local & External IPs (backend of AnyLog if not preset in configuration)
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

# If declare connect to message broker 
run message broker !external_ip !anylog_broker_port !ip !anylog_broker_port
```

3. Connect to databases almgm and create tsd_info table 
```anylog
connect dbms almgm where type=!db_type and ip=!db_ip and port=!db_port and user=!db_user and password=!db_passwd
create table tsd_info where dbms=almgm
```
<p style="color: gray; size: 90%">`almgm.tsd_info` contains all metadata information about files injested. Other tables 
in almgm contain information regarding data ingested in peer  nodes in the same  cluster.</p>

4. Connect to the operator database - this is where device data is ultimately stored
```anylog
connect dbms connect dbms !default_dbms where type=!db_type and ip=!db_ip and port=!db_port and user=!db_user and password=!db_passwd

# if MongoDB is enabled start MongoDB database 
connect dbms connect dbms !default_dbms where type=!nosql_type and ip=!nosql_ip and port=!nosql_port and user=!nosql_user and password=!nosql_passwd
```

5. (Optional) Connect to `system_query`
```anylog
connect dbms system_query where type=sqlite and memory=true  
```

6. Set scheduler 1 & blockchain sync 
```anylog 
run scheduler 1
run blockchain sync where source=blockchain_source and time=!sync_time and dest=blockchain_destination and connection=!ledger_conn
```

7. Check if cluster policy exists & if not create it
```anylog 
policy = blockchain get cluster where name=!cluster_name and company=!company_name bring.first

<new_policy={"cluster": {
    "company": !company_name, 
    "dbms": !default_dbms, 
    "name": !cluster_name, 
    "master": !ledger_conn
}}> 

if not !policy then 
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

8. Declare Operator Node on the metadata layer 
```anylog
# get cluster ID 
cluster_id = blockchain get cluster where name=!cluster_name bring.first [cluster][id]
<new_policy={"operator": {
    "hostname": !hostname, 
    "name": !node_name, 
    "company": !company_name, 
    "local_ip": !ip, 
    "ip": !external_ip, 
    "port" : !anylog_server_port.int, 
    "rest_port": !anylog_rest_port.int, 
    "loc": !loc, 
    "cluster": !cluster_id
}}> 

policy = blockchain get operator where name=!node_name and company=!company_name and cluster=!cluster_id 
if not !policy then 
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

9. Set partitioning of the data & schedule to drop old partitions once a day
```anylog
partition !default_dbms !table_name using !partition_column by !partition_interval

schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep
```
10. Run MQTT   
```anylog
<run mqtt client where broker=!broker and port=!port and log=!mqtt_log and topic=(
   name=!mqtt_topic_name and 
   dbms=!mqtt_topic_dbms and 
   table=!mqtt_topic_table and 
   column.timestamp.timestamp=!mqtt_column_timestamp and
   column.value=(value=!mqtt_column_value and type=!mqtt_column_value_type)
)>
```
11. If NoSQL is enabled, then set blobs archiver configurations -- [configure accepting NoSQL](setting_up_mongodb.md)
```anylog
<run blobs archiver where
    dbms=!blobs_dbms and
    folder=!blobs_folder and
    compress=!blobs_compress and
    reuse_blobs=!blobs_reuse
>```

12. Start Operator - There are 3 steps need to start the operator process:
    * `set buffer threshold` –  By setting the threshold to immediate, data (new) coming in will be stored within the operator database with no delay, whereas when disabled it takes up to 60 seconds for new data to be stored in the database. 
    * `run data distributor` – The distributor tells the node to share its data with other operator instances connected to the same cluster (if  HA  is enabled). In the case of this demo, each of the (two) operators deployed is correlated to a different cluster without HA.
    * `run operator` – This is the only required step, as it informs the node that it needs to host data. 

```anylog
operator_id = blockchain get operator where name=!node_name and company=!company_name and local_ip=!ip and port=!anylog_server_port bring [operator][id]

run data distributor
run data consumer where start_date = !ha_start_date

<run operator where
    create_table=!create_table and
    update_tsd_info=!update_tsd_info and
    compress_json=!compress_file and
    compress_sql = !compress_file and archive=!archive and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads = !operator_threads
>
```

13. (Manually) Validate processes are running
```anylog
AL anylog-operator +> get processes 

    Process         Status       Details                                                                    
    ---------------|------------|--------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 139.162.56.87:32148, Threads Pool: 6                        |
    REST           |Running     |Listening on: 139.162.56.87:32149, Threads Pool: 5, Timeout: 20, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 45.79.74.39:32048, Threads Pool: 1    |
    Publisher      |Not declared|                                                                          |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                            |
    Distributor    |Running     |                                                                          |
    Blobs Archiver |Running     |                                                                          |
    Consumer       |Running     |No peer Operators supporting the cluster                                  |
    MQTT           |Running     |                                                                          |
    Message Broker |Not declared|                                                                          |
    SMTP           |Not declared|                                                                          |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes              |
    Query Pool     |Running     |Threads Pool: 3                                                           |
    Kafka Consumer |Not declared|                                                                          |
```