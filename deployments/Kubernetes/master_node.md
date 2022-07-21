# Master Node
A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).

To understand the steps taken to deploy a master node, please review the [deployment process](master_node_deployment_process.md). 

## Deployment Steps 
0. The sample deployment uses [PostgreSQL](Postgres.md). Please make sure  PostgreSQL is installed.

2. In [deployments/anylog-node/envs/anylog_master.env]() update configurations
```YAML
#-----------------------------------------------------------------------------------------------------------------------
# The following are the general values used to deploy an AnyLog instance of type: Master | AnyLog version: predevelop
#-----------------------------------------------------------------------------------------------------------------------
general:
 namespace: default
 app_name: anylog
 # pod name is used as a hostname for the pod
 pod_name: anylog-master-pod
 deployment_name: anylog-master-app
 service_name: anylog-master-svs
 configmap_name: anylog-master-configs
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
   node_type: ledger
   node_name: anylog-master-node
   company_name: New Company
   # if location is not set, will use `https://ipinfo.io/json` to get coordinates
   location: ""
   country: ""
   state: ""
   city: ""

 networking:
   server: 32048
   rest: 32049
   # Optional broker port
   broker: ""
   # master node is not needed for REST node
   # Optional external & local IP instead of the default values
   external_ip: ""
   local_ip: ""
   # Proxy IP used by Nginx or other loadbalancer. We've tested with Nginx, setting the value to the local IP of the machine
   K8s_proxy_ip: 45.79.74.39

 authentication:
   enable: false
   type: ""
   user: ""
   password: ""

 blockchain:
   ledger_conn: 127.0.0.1:32048
   sync_time: 30 seconds
   source: master
   destination: file

 database:
   type: psql
   ip: postgres-svs
   port: 5432
   user: admin
   password: demo
   # whether to have the node support system_query (ie querying data).
   deploy_system_query: false
   # whether to have system_query database to run against memory directly
   memory: true

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
   query_pool: 3
   write_immediate: true
   threshold_time : 60 seconds
   threshold_volume: 10KB
```

2. Deploy AnyLog Master
```shell
helm install ~/deployments/packages/anylog-node-1.22.3.tgz --values ~/deployments/configurations/helm/anylog_master.yaml --name-template anylog-master
```

3. Attaching to Pod
```shell

# get pod name 
kubectl get pod

<< comment 
NAME                                   READY   STATUS    RESTARTS   AGE
anylog-master-app-768549f86d-2vpkr     1/1     Running   0          11m
>>

# attach to node 
kubectl attach -it anylog-master-app-768549f86d-2vpkr

# to detach: ctrl-p + ctrl-q
```

### Validate Node 
* Get Status
```shell
curl -X GET ${MASTER_NODE_IP}:${MASTER_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${MASTER_NODE_IP}:${MASTER_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23"  #| jq 

    Process         Status       Details                                                                  
    ---------------|------------|------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 45.79.74.39:32048, Threads Pool: 6                        |
    REST           |Running     |Listening on: 45.79.74.39:32049, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                        |
    Publisher      |Not declared|                                                                        |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 127.0.0.1:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                          |
    Distributor    |Not declared|                                                                        |
    Consumer       |Not declared|                                                                        |
    MQTT           |Not declared|                                                                        |
    Message Broker |Not declared|No active connection                                                    |
    SMTP           |Not declared|                                                                        |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes            |
    Query Pool     |Running     |Threads Pool: 3                                                         |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-master-node

# to detach press: ctrl-d
```
