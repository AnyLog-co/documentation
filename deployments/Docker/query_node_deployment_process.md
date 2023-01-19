# Deployment Process
The following provides insight the work being done in the background to deploy the Master node. 

For directions to start a master node please visit the [query node](deploying_node.md) document.

## Steps
1. Set parameters such as:
   * hostname
   * Internal & External IPs (backend of AnyLog if not preset in configuration)
   * `ENV` parameters from configuration into AnyLog parameters  
```anylog
AL > hostname = get hostname
AL > node_name=$NODE_NAME
company_name=$COMPANY_NAME
anylog_server_port=$ANYLOG_SERVER_PORT
...
```

2. Connect to TCP & REST 
```anylog
run tcp server !external_ip !anylog_server_port !ip !anylog_server_port
run rest server !ip !anylog_rest_port
```

3. Connect to system_query 
```anylog
connect dbms system_query where type=!db_type and memory=!memory
```

4. Set scheduler 1 & blockchain sync 
```anylog
run scheduler 1
run blockchain sync where source=blockchain_source and time=!sync_time and dest=blockchain_destination and connection=!ledger_conn
```

5. Declare the Master in the metadata (Master Node Policy)
```anylog
<new_policy = {"query": {
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

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

6. (Manually) Validate processes are running
```anylog
AL anylog-query-node +> get processes 

    Process         Status       Details                                                                    
    ---------------|------------|--------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 23.239.12.151:32348, Threads Pool: 6                        |
    REST           |Running     |Listening on: 23.239.12.151:32349, Threads Pool: 5, Timeout: 20, SSL: None|
    Operator       |Not declared|                                                                          |
    Publisher      |Not declared|                                                                          |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                            |
    Distributor    |Not declared|                                                                          |
    Blobs Archiver |Not declared|                                                                          |
    Consumer       |Not declared|                                                                          |
    MQTT           |Not declared|                                                                          |
    Message Broker |Not declared|No active connection                                                      |
    SMTP           |Not declared|                                                                          |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes              |
    Query Pool     |Running     |Threads Pool: 3                                                           |
    Kafka Consumer |Not declared|                                                                          |
```
