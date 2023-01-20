# Deployment Process
The following provides insight into the work being done in the background to deploy the Master node. 

For directions to start a Master node please visit the [deployment process](deploying_node.md) document.
configurations used for this deployment can be found [here](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-master/anylog_configs.env)   


## Steps
1. Set parameters such as:
   * hostname
   * Internal & External IPs (backend of AnyLog if not preset in configuration)
   *  If overlay_network is configured by setting the OVERLAY_NETWORK to true and OVERLAY_IP, INTERNAL_IP will be set to the OVERLAY_IP
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
if (overlay_network is true {
  run tcp server where external_ip = !external_ip and external_port = !anylog_server_port and internal_ip = !internal_ip 
  and internal_port = !anylog_server_port and bind = true 
  run rest server where external_ip = !external_ip and external_port = !anylog_server_port and internal_ip = !internal_ip 
  and internal_port = !anylog_server_port and bind = false 
  } else {
   run tcp server where external_ip = !external_ip and external_port = !anylog_server_port and internal_ip = !internal_ip 
   and internal_port = !anylog_server_port and bind = false
   run rest server where external_ip = !external_ip and external_port = !anylog_server_port and internal_ip = !internal_ip 
   and internal_port = !anylog_server_port and bind = false 
  }
```

3. Connect to blockchain database & create ledger table 
```anylog
connect dbms blockchain where type=psql and ip=!db_ip and port=!db_port and user=!db_user and password=!db_passwd
create table ledger where dbms=blockchain
```
<p style="color: gray; size: 90%">Note: `blockchain.ledger` contains the metadata policies. For example, the different node 
types connected to the network  data tables associated with each node. </p>

4. Set scheduler 1 & blockchain sync 
```anylog
run scheduler 1
run blockchain sync where source=blockchain_source and time=!sync_time and dest=blockchain_destination and connection=!ledger_conn
```

5. Declare the Master in the metadata (Master Node Policy)
```anylog
If (overlay_network is true) {
<new_policy = {"master": {
    "hostname": !hostname,
    "name": !node_name,
    "internal_ip": !internal_ip,
    "company": !company_name,
    "port" : !anylog_server_port.int,
    "rest_port": !anylog_rest_port.int,
    "loc": !loc,
    "country": !country,
    "state": !state, 
    "city": !city
}}>
} else {
<new_policy = {"master": {
    "hostname": !hostname,
    "name": !node_name,
    "external_ip" : !external_ip,
    "internal_ip": !internal_ip,
    "company": !company_name,
    "port" : !anylog_server_port.int,
    "rest_port": !anylog_rest_port.int,
    "loc": !loc,
    "country": !country,
    "state": !state, 
    "city": !city
}}>
}

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

6. (Manually) Validate processes are running
```anylog
AL anylog-master +> get processes 

    Process         Status       Details                                                                  
    ---------------|------------|------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 45.79.74.39:32048, Threads Pool: 6                        |
    REST           |Running     |Listening on: 45.79.74.39:32049, Threads Pool: 5, Timeout: 20, SSL: None|
    Operator       |Not declared|                                                                        |
    Publisher      |Not declared|                                                                        |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 127.0.0.1:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                          |
    Distributor    |Not declared|                                                                        |
    Blobs Archiver |Not declared|                                                                        |
    Consumer       |Not declared|                                                                        |
    MQTT           |Not declared|                                                                        |
    Message Broker |Not declared|No active connection                                                    |
    SMTP           |Not declared|                                                                        |
    Streamer       |Not declared|                                                                        |
    Query Pool     |Running     |Threads Pool: 3                                                         |
    Kafka Consumer |Not declared|                                                                        |
```
