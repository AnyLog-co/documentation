# Deployment Process
The following provides insight into the work being done in the background to deploy the Master node. 
In the example, the node is part of a [nebula overlay network](../Networking%20&%20Security/nebula.md), with the TCP 
connection set to bind. 

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
AL anylog-master > company_name=$COMPANY_NAME
AL anylog-master > anylog_server_port=$ANYLOG_SERVER_PORT
...
```

2. Declare (optional) configurations and master policies - the polices are built based on parameters
```anylog
AL anylog-master > <new_policy = {'config' : {
   'name' : 'master-overlay-configs',
   'company' : 'New Company',
   'port' : '!anylog_server_port.int',
   'external_ip' : '!external_ip',
   'ip' : '!overlay_ip',
   'rest_port' : '!anylog_rest_port.int'
}}>
AL anylog-master > blockchain prepare policy !new_policy
AL anylog-master > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

AL anylog-master > <new_policy = {'master' : {
   'name' : 'anylog-master',
   'company' : 'New Company',
   'hostname' : 'nebula-node1',
   'loc' : '51.5085,-0.1257',
   'country' : 'GB',
   'state' : 'England',
   'city' : 'London',
   'port' : 32048,
   'external_ip' : '212.71.244.21',
   'ip' : '10.0.0.2',
   'rest_port' : 32049
}}>
AL anylog-master > blockchain prepare policy !new_policy
AL anylog-master > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

3. Connect to [network](../../network%20configuration.md) - either based on a configuration or node policy ID. In this case, 
the node is using the configuration policy ID
```anylog  
AL anylog-master > config from policy where id = !policy_id
```

4. Connect to `blockchain` logical database and create `ledger` table
```anylog
# connect to logical database 
AL anylog-master > connect dbms blockchain where type=!db_type and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port

create table ledger where dbms=blockchain
```
5. If set, connect to `system_query` logical database 
```anylog
AL anylog-master > connect dbms system_query where type=sqlite and memory=!memory
```

6. Run [scheduler processes](../../background%20processes.md#scheduler-process) and [blockchain sync](../../background%20processes.md#blockchain-synchronizer)
```anylog
run scheduler 1
run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn
```

**Expected Behavior**: The _basic_ deployment for the given master node is something like this: 
```anylog
AL anylog-master +> get connections 

Type      External Address Internal Address Bind Address   
---------|----------------|----------------|--------------|
TCP      |10.0.0.2:32048  |10.0.0.2:32048  |10.0.0.2:32048|
REST     |10.0.0.2:32049  |10.0.0.2:32049  |0.0.0.0:32049 |
Messaging|Not declared    |Not declared    |Not declared  |

AL anylog-master +> get processes 

    Process         Status       Details                                                                
    ---------------|------------|----------------------------------------------------------------------|
    TCP            |Running     |Listening on: 10.0.0.2:32048, Threads Pool: 6                         |
    REST           |Running     |Listening on: 10.0.0.2:32049, Threads Pool: 5, Timeout: 20, SSL: False|
    Operator       |Not declared|                                                                      |
    Publisher      |Not declared|                                                                      |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 10.0.0.2:32048               |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                        |
    Distributor    |Not declared|                                                                      |
    Blobs Archiver |Not declared|                                                                      |
    Consumer       |Not declared|                                                                      |
    MQTT           |Not declared|                                                                      |
    Message Broker |Not declared|No active connection                                                  |
    SMTP           |Not declared|                                                                      |
    Streamer       |Not declared|                                                                      |
    Query Pool     |Running     |Threads Pool: 3                                                       |
    Kafka Consumer |Not declared|                                                                      |
```

