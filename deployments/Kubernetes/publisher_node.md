# Publisher Node
A node that supports distribution of data from device(s) to operator nodes. In the example we have a running 
message broker, however the MQTT client is running against the local REST node for a sample data set  

To understand the steps taken to deploy a query node, please review the [deployment process](publisher_node_deployment_process.md). 

## Deployment Steps
1. In [deployments/helm/sample-configurations/anylog_publisher.yml](https://github.com/AnyLog-co/deployments/blob/master/helm/sample-configurations/anylog_publisher.yaml) 
update configurations. Please note, the `LEDGER_CONN` value is configured against our testnet / demo master node.  
```YAML
#----------------------------------------------------------------------------------------------------------------------
# The following are the general values used to deploy an AnyLog instance of type: Publisher | AnyLog version: develop
#----------------------------------------------------------------------------------------------------------------------
general:
  namespace: default
  app_name: anylog
  deployment_name: anylog-publisher-app
  service_name: anylog-publisher-svs
  configmap_name: anylog-publisher-configs
  # nodeSelector - Allows running Kubernetes remotely. If commented out, code will ignore it
  #nodeSelector: ""
  replicas: 1
  
image:
  secretName: imagepullsecret
  repository: anylogco/anylog-network
  tag: predevelop
  pullPolicy: Always

configs:
  basic:
    node_type: publisher
    node_name: anylog-publisher-node
    company_name: Company Name
    # if location is not set, will use `https://ipinfo.io/json` to get coordinates
    location: ""
    country: ""
    state: ""
    city: ""

  networking:
    server: 32248
    rest: 32249
    # Optional broker port
    broker: 32250
    # master node is not needed for REST node
    # Optional external & local IP instead of the default values
    external_ip: ""
    local_ip: ""
    # Proxy IP used by Nginx or other loadbalancer
    k8s_proxy_ip: 172.104.180.110

  authentication:
    enable: false
    type: ""
    user: ""
    password: ""

  blockchain:
    ledger_conn: 45.79.74.39:32048
    sync_time: 30 seconds
    source: master
    destination: file

  database:
    type: sqlite
    #ip: postgres-svs
    #port: 5432
    #user: admin
    #password: demo
    # whether to have the node support system_query (ie querying data).
    deploy_system_query: false
    # whether to have system_publisher database to run against memory directly
    memory: true

  publisher:
    compress: true
    move: true
    db_location: file_name[0]
    table_location: file_name[1]

  mqtt:
    enable: true
    broker: rest
    port: 32249
#    user: ibglowct
#    password: MSY4e009J7ts
    log: false
    topic:
      name: anylogrest
      db_name: "bring [dbms]"
      table: "bring [table]"
      timestamp: "bring [timestamp]"
      value_type: float
      value: "bring [value]"

  settings:
    # whether to deploy a local script that extends the default startup script
    deploy_local_script: "false"
    # An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port.
    tcp_thread_pool: 6
    # Amount of time (in seconds) until REST timeout
    rest_timeout: 30
    # The number of concurrent threads supporting HTTP requests.
    rest_threads: 5
    # Sets the number of threads supporting queries (the default is 3).
    publisher_pool: 3
    write_immediate: true
    threshold_time : 60 seconds
    threshold_volume: 10KB
```
2. Deploy AnyLog Publisher 
```shell
helm install ~/deployments/helm/packages/anylog-node-1.22.3.tgz --values ~/deployments/helm/sample-configurations/anylog_publisher.yaml --name-template anylog-publisher
```

3. Attaching to node 
```shell
# get pod name 
kubectl get pod

<< comment 
NAME                                   READY   STATUS    RESTARTS   AGE
anylog-publisher-app-788549f88d-krp9kr     1/1     Running   0      11m

>>

# attach to node 
kubectl attach -it anylog-publisher-app-788549f88d-krp9kr

# to detach: ctrl-p + ctrl-q
```



### Validate Node 
* Get Status
```shell
curl -X GET ${PUBLISHER_NODE_IP}:${PUBLISHER_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${PUBLISHER_NODE_IP}:${PUBLISHER_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23" 
    Process         Status       Details                                                                      
    ---------------|------------|----------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.104.180.110:32248, Threads Pool: 6                        |
    REST           |Running     |Listening on: 172.104.180.110:32249, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                            |
    Publisher      |Running     |                                                                            |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                  |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                              |
    Distributor    |Not declared|                                                                            |
    Consumer       |Not declared|                                                                            |
    MQTT           |Running     |                                                                            |
    Message Broker |Running     |Listening on: 172.104.180.110:32250, Threads Pool: 4                        |
    SMTP           |Not declared|                                                                            |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes                |
    Query Pool     |Running     |Threads Pool: 3                                                             |
    Kafka Consumer |Not declared|                                                                            |
```

* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-publisher-node

# to detach press: ctrl-d
```
