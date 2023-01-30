# Deployment Process
The following provides insight into the work being done in the background to deploy the Operator node. 
In the example, the node is part of a [nebula overlay network](../Networking%20&%20Security/nebula.md), with the TCP 
connection set to bind. 

For directions to start a Operator node please visit the [deployment process](deploying_node.md) document.
configurations used for this deployment can be found [here](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-operator/anylog_configs.env)

Note, the sample configurations use _SQLite_ so that users can take it run. However, we recommnad utilizing Relational 
databases, such as _PostgreSQL_, for large scale projects when/if possible.       

## Steps
1. Set parameters such as:
   * hostname
   * Local & External IPs (backend of AnyLog if not preset in configuration)
   * `ENV` parameters from configuration into AnyLog parameters  
```anylog
AL > hostname = get hostname
AL > node_name=$NODE_NAME
AL anylog-operator > company_name=$COMPANY_NAME
AL anylog-operator > anylog_server_port=$ANYLOG_SERVER_PORT
...
```

2. Declare (optional) configurations, cluster and operator policies - the polices are built based on parameters
```anylog
AL anylog-operator > <new_policy = {'config' : {
   'name' : !config_policy_name,
   'company' : !company_name,
   'port' : '!anylog_server_port.int',
   'external_ip' : '!external_ip',
   'ip' : '!overlay_ip',
   'rest_port' : '!anylog_rest_port.int'
}}>
AL anylog-operator > blockchain prepare policy !new_policy
AL anylog-operator > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

AL anylog-operator > <new_policy = {"cluster": {
    "company": !company_name,
    "name": !cluster_name,
    "dbms": !default_dbms
}}>
AL anylog-operator > blockchain prepare policy !new_policy
AL anylog-operator > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

AL anylog-operator > <new_policy = {'operator' : {
   'name' : !node_name,
   'company' : !company_name,
   'hostname' : !hostname,
   'loc' : !loc,
   'country' : !country,
   'state' : !state,
   'city' : !city,
   'port' : !anylog_server_port.int,
   'external_ip' : !external_ip,
   'ip' : !overlay_ip,
   'rest_port' : !anylog_rest_port.int,
   'cluster': !cluster_id
}}>
AL anylog-operator > blockchain prepare policy !new_policy
AL anylog-operator > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

3. Connect to [network](../../network%20configuration.md) - either based on a configuration or node policy ID. In this case, 
the node is using the configuration policy ID
```anylog  
AL anylog-operator > config from policy where id = !policy_id
```

4. Connect to the logical databases that data will be stored in  
```anylog
# connect to logical database 
AL anylog-operator > connect dbms !default_dbms where type=!db_type and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port

# connect to a database that keeps record of data comming in and created assoicated table
AL anylog-operator > connect dbms almgm where type=!db_type and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port
AL anylog-operator > create table tsd_info where dbms=almgm
```
5. If set, connect to `system_query` logical database 
```anylog
AL anylog-operator > connect dbms system_query where type=sqlite and memory=!memory
```

6. Run [scheduler processes](../../background%20processes.md#scheduler-process) and [blockchain sync](../../background%20processes.md#blockchain-synchronizer)
```anylog
AL anylog-operator > run scheduler 1
AL anylog-operator > run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn
```

7. If set, enable partitioning & a scheduled process to remove older partitioned tables 
```anylog 
AL anylog-operator > partition !default_dbms !table_name using !partition_column by !partition_interval
AL anylog-operator > schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep
```

**Expected Behavior**: Validate the node is running properly
* `get processes` - show the background & connection information
* `get databases` - show which database(s) the node is connected to  
* `get msg client` - view data coming into the node
```anylog
AL anylog-operator +> get processes 

    Process         Status       Details                                                                
    ---------------|------------|----------------------------------------------------------------------|
    TCP            |Running     |Listening on: 10.0.0.3:32148, Threads Pool: 6                         |
    REST           |Running     |Listening on: 10.0.0.3:32149, Threads Pool: 5, Timeout: 20, SSL: False|
    Operator       |Running     |Cluster Member: False, Using Master: 10.0.0.2:32048, Threads Pool: 1  |
    Publisher      |Not declared|                                                                      |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 10.0.0.2:32048               |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                        |
    Distributor    |Not declared|                                                                      |
    Blobs Archiver |Not declared|                                                                      |
    Consumer       |Not declared|                                                                      |
    MQTT           |Running     |                                                                      |
    Message Broker |Not declared|No active connection                                                  |
    SMTP           |Not declared|                                                                      |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes          |
    Query Pool     |Running     |Threads Pool: 3                                                       |
    Kafka Consumer |Not declared|                                                                      |
        
AL anylog-operator +> get databases  

List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
almgm                sqlite        Local                          /app/AnyLog-Network/data/dbms/almgm.dbms
test                 sqlite        Local                          /app/AnyLog-Network/data/dbms/test.dbms

AL anylog-operator +> get msg client 

Subscription ID: 0001
User:         ibglowct
Broker:       driver.cloudmqtt.com:18785
Connection:   Connected

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
             40          40           0  2023-01-30 05:01:43
     
     Subscribed Topics:
     Topic       QOS DBMS Table     Column name Column Type Mapping Function        Optional Policies 
     -----------|---|----|---------|-----------|-----------|-----------------------|--------|--------|
     anylogedgex|  0|test|rand_data|timestamp  |timestamp  |now()                  |False   |        |
                |   |    |         |value      |float      |['[readings][][value]']|False   |        |
```

