# Deployment Process
The following provides insight into the work being done in the background to deploy the Query node. 
In the example, the physical machine part a [nebula overlay network](../Networking%20&%20Security/nebula.md); however, 
connectivity is based on the default local IP address with TCP bind disabled. 

For directions to start a Query node please visit the [deployment process](../Docker/deploying_node.md) document.
configurations used for this deployment can be found [here](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-query-remote-cli/anylog_configs.env)   

Note, the sample configurations use _SQLite_ so that users can take it run. However, we recommend utilizing Relational 
databases, such as _PostgreSQL_, for large scale projects when/if possible.

**Reminder** - By default, when using the [deployment scripts](https://github.com/AnyLog-co/deployments), [Remote-CLI](../Support/Remote-CLI.md)
will be deployed with your node. 

## Steps
1. Set parameters such as:
   * hostname
   * Local & External IPs (backend of AnyLog if not preset in configuration)
   * `ENV` parameters from configuration into AnyLog parameters  
```anylog
AL > hostname = get hostname
AL > node_name=$NODE_NAME
AL anylog-query > company_name=$COMPANY_NAME
AL anylog-query > anylog_server_port=$ANYLOG_SERVER_PORT
...
```

2. Declare (optional) configurations and query policies - the polices are built based on parameters
```anylog
AL anylog-query > <new_policy = {'config' : {
   'name' : !config_policy_name,
   'company' : !company_name,
   'port' : '!anylog_server_port.int',
   'external_ip' : '!external_ip',
   'ip' : '!ip',
   'rest_port' : '!anylog_rest_port.int'
}}>
AL anylog-query > blockchain prepare policy !new_policy
AL anylog-query > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

AL anylog-query > <new_policy = {'query' : {
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
   'rest_port' : !anylog_rest_port.int
}}>
AL anylog-query > blockchain prepare policy !new_policy
AL anylog-query > blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

3. Connect to [network](../../network%20configuration.md) - either based on a configuration or node policy ID. In this case, 
the node is using the configuration policy ID
```anylog  
AL anylog-query > config from policy where id = !policy_id
```
 
4. Connect to `system_query` logical database 
```anylog
AL anylog-query > connect dbms system_query where type=sqlite and memory=!memory
```

5. Run [scheduler processes](../../background%20processes.md#scheduler-process) and [blockchain sync](../../background%20processes.md#blockchain-synchronizer)
```anylog
AL anylog-query > run scheduler 1
AL anylog-query > run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn
```

**Expected Behavior**: Validate the node is running properly
* `get processes` - will show the background & connection information
* `get databases` - will show which database the node is connected to
```anylog
AL anylog-query > get processes 

    Process         Status       Details                                                                     
    ---------------|------------|---------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 74.207.231.88:32348, Threads Pool: 6                         |
    REST           |Running     |Listening on: 74.207.231.88:32349, Threads Pool: 5, Timeout: 20, SSL: False|
    Operator       |Not declared|                                                                           |
    Publisher      |Not declared|                                                                           |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 10.0.0.2:32048                    |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                             |
    Distributor    |Not declared|                                                                           |
    Blobs Archiver |Not declared|                                                                           |
    Consumer       |Not declared|                                                                           |
    MQTT           |Not declared|                                                                           |
    Message Broker |Not declared|No active connection                                                       |
    SMTP           |Not declared|                                                                           |
    Streamer       |Not declared|                                                                           |
    Query Pool     |Running     |Threads Pool: 3                                                            |
    Kafka Consumer |Not declared|                                                                           |

AL anylog-query > get databases 

List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
system_query         sqlite        Local                          MEMORY
```

