# Operator Node
A node that hosts the data. This operator will receive data directly from EdgeX via [third-party MQTT broker](https://www.cloudmqtt.com/). 

To understand the steps taken to deploy a operator node, please review the [deployment process](operator_node_deployment_process.md). 

## Deployment Steps
1. In [deployments/anylog-node/envs/anylog_operator2.env]() update configurations. Please note, the `LEDGER_CONN` value 
is configured against our testnet / demo master node.  
```yaml

#----------------------------------------------------------------------------------
# The following are the general values used to deploy an AnyLog instance of type: Operator | AnyLog version: predevelop
#----------------------------------------------------------------------------------
general:
 namespace: default
 app_name: anylog
 pod_name: anylog-operator-pod2
 deployment_name: anylog-operator-app2
 service_name: anylog-operator-svs2
 configmap_name: anylog-operator-configs2
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
   node_type: operator
   node_name: anylog-operator-node2
   company_name: New Company
   # if location is not set, will use `https://ipinfo.io/json` to get coordinates
   location: ""
   country: ""
   state: ""
   city: ""

 networking:
   server: 32158
   rest: 32159
   # Optional broker port
   broker: ""
   # master node is not needed for REST node
   # Optional external & local IP instead of the default values
   external_ip: ""
   local_ip: ""
   # Proxy IP used by Nginx or other loadbalancer
   k8s_proxy_ip: ""

 authentication:
   enable: false
   type: ""
   user: ""
   password: ""

 blockchain:
   # The ledger conn is right now configured against our test / demo network - please update to utilize against your own network. 
   ledger_conn: 45.79.74.39:32048
   sync_time: 30 seconds
   source: master
   destination: file

 database:
   type: sqlite
   # whether to have the node support system_query (ie querying data).
   deploy_system_query: true
   # whether to have system_query database to run against memory directly
   memory: true

 operator:
   # set member ID for operator - should only be used when readding operator to blockchain but keep (file) configs consistent
   member: ""
   cluster_name: new-cluster
   create_table: true
   update_tsd: true
   archive: true
   distributor: true
   db_name: test
   partition:
       enable: true
       table: "*"
       column: timestamp
       interval: 7 days
       keep: 5
       sync: 1 day

# MQTT configured against CloudMQTT broker to get random data from generated using EdgeX. 
 mqtt:
   enable: true
   broker: driver.cloudmqtt.com
   port: 18785
   user: ibglowct
   password: MSY4e009J7ts
   log: false
   topic:
     name: anylogedgex
     db_name: test
     table: plc_device
     timestamp: now
     value_type: float
     value: bring [readings][][value]

 settings:
   # whether to deploy a local script that extends the default startup script
   deploy_local_script: false
   # An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port.
   tcp_thread_pool: 6
   # Amount of time (in seconds) until REST timeout
   rest_timeout: 30
   # The number of concurrent threads supporting HTTP requests.
   rest_threads: 5
   # Sets the number of threads supporting queries (the default is 3).
   operator_pool: 3
   write_immediate: true
   threshold_time : 60 seconds
   threshold_volume: 10KB
```
2. Deploy AnyLog Operator
```shell
helm install ~/deployments/packages/anylog-node-1.22.3.tgz --values ~/deployments/configurations/helm/anylog_operator.yaml --name-template anylog-operator1
```

3. Attaching to node 
```shell
# get pod name 
kubectl get pod

<< comment 
NAME                                   READY   STATUS    RESTARTS   AGE
anylog-operator2-app-784549f88d-pkr     1/1     Running   0         11m

>>

# attach to node 
kubectl attach -it anylog-operator2-app-784549f88d-pkr

# to detach: ctrl-p + ctrl-q
```

### Validate Node 
* Get Status
```shell
curl -X GET ${OPERATOR_NODE2_IP}:${OPERATOR_NODE2_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${OPERATOR_NODE2_IP}:${OPERATOR_NODE2_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23"  
    Process         Status       Details                                                                     
    ---------------|------------|---------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.105.86.168:32148, Threads Pool: 6                        |
    REST           |Running     |Listening on: 172.105.86.168:32149, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 45.79.74.39:32048                      |
    Publisher      |Not declared|                                                                           |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                 |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                             |
    Distributor    |Running     |                                                                           |
    Consumer       |Not declared|                                                                           |
    MQTT           |Running     |                                                                           |
    Message Broker |Not declared|No active connection                                                       |
    SMTP           |Not declared|                                                                           |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes               |
    Query Pool     |Running     |Threads Pool: 3                                                            |
    Kafka Consumer |Not declared|                                                                           |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-operator-node2

# to detach press: ctrl-d
```
