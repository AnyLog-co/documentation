# Deployment Process
The following provides insight into the work being done in the background to deploy the Query node. 
In the example, the physical machine part a [nebula overlay network](../Networking%20&%20Security/nebula.md); however, 
connectivity is based on the default local IP address with TCP bind disabled. 

For directions to start a Query node please visit the [deployment process](deploying_node.md) document.
configurations used for this deployment can be found [here](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-query-remote-cli/anylog_configs.env)   

**Reminder** - By default, when using the [deployment scripts](https://github.com/AnyLog-co/deployments), [Remote-CLI](../Support/Remote-CLI.md)
will be deployed with your node. 

## Steps
1. Set parameters such as:
   * hostname
   * Internal & External IPs (backend of AnyLog if not preset in configuration)
   *  If overlay_network is configured by setting the OVERLAY_NETWORK to true and OVERLAY_IP, INTERNAL_IP will be set to the OVERLAY_IP
   * `ENV` parameters from configuration into AnyLog parameters  
```anylog
AL > hostname = get hostname
AL > node_name=$NODE_NAME
AL anylog-query > company_name=$COMPANY_NAME
AL anylog-query > anylog_server_port=$ANYLOG_SERVER_PORT
...
```

2. Declare (optional) configurations and master policies - the polices are built based on parameters
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
run scheduler 1
run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn
```

**Expected Behavior**: The _basic_ deployment for the given query node is something like this: 
```anylog
AL anylog-query > get connections 

Type      External Address    Internal Address    Bind Address  
---------|-------------------|-------------------|-------------|
TCP      |74.207.231.88:32348|74.207.231.88:32348|0.0.0.0:32348|
REST     |74.207.231.88:32349|74.207.231.88:32349|0.0.0.0:32349|
Messaging|Not declared       |Not declared       |Not declared |

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
```

