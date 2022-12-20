# Operator Node
A node that hosts the data. This operator will receive data directly from EdgeX via MQTT. 

To understand the steps taken to deploy a operator node, please review the [deployment process](operator_node_deployment_process.md). 

Directions for configuring EdgeX send data to a local AnyLog broker can be found [here](../Other%20Tools/EdgeX.md).

## Deployment Steps 
0. The sample deployment uses [PostgreSQL](Postgres.md). Please make sure  PostgreSQL is installed.


1. In [deployments/helm/sample-configurations/anylog_operator.yaml](https://github.com/AnyLog-co/deployments/blob/master/helm/sample-configurations/anylog_operator.yml) 
update configurations. Please note, the `LEDGER_CONN` value is configured against our testnet / demo master node.  
```YAML
#-----------------------------------------------------------------------------------------------------------------------
# The following are the general values used to deploy an AnyLog instance of type: Operator | AnyLog version: predevelop
#-----------------------------------------------------------------------------------------------------------------------
general:
 namespace: default
 app_name: anylog
 pod_name: anylog-operator-pod
 deployment_name: anylog-operator-app
 service_name: anylog-operator-svs
 configmap_name: anylog-operator-configs
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
   node_name: anylog-operator-node
   company_name: New Company
   # if location is not set, will use `https://ipinfo.io/json` to get coordinates
   location: ""
   country: ""
   state: ""
   city: ""

 networking:
   server: 32148
   rest: 32149
   # Optional broker port
   broker: 32150
   # master node is not needed for REST node
   # Optional external & local IP instead of the default values
   external_ip: ""
   local_ip: ""
   # Proxy IP used by Nginx or other loadbalancer
   proxy_ip: 139.162.56.87

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
   type: psql
   ip: postgres-svs
   port: 5432
   user: admin
   password: demo
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
       interval: 14 days
       keep: 6
       sync: 1 day

# MQTT configured against CloudMQTT broker to get random data from generated using EdgeX. 
 mqtt:
   enable: true
   broker: driver.cloudmqtt.com
   port: 32150
#   user: ibglowct
#   password: MSY4e009J7ts
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
helm install ~/deployments/helm/packages/anylog-node-1.22.3.tgz --values ~/deployments/helm/sample-configurations/anylog_operator.yml --name-template anylog-operator1
```

3. Updating [nginx](../Networking/nginx.md) files to support REST & MQTT communication remotely & restart the service

   i. To Support TCP - add following content in `/etc/nginx/nginx.conf`
   
   ```editorconfig
   stream {
       # AnyLog TCP Connection - repeat the next two steps for each node
       upstream anylog_operator1_tcp {
           server ${KUBE_APISERVER_IP}:32148;
       }
       server {
           listen 32148 so_keepalive=on;
           proxy_pass anylog_operator1_tcp;
       }
       # AnyLog Broker Connection - repeat the next two steps for broker ports
       upstream anylog_operator1_broker {
           server ${KUBE_APISERVER_IP}:32150;
       }
       server {
           listen 32150 so_keepalive=on;
           proxy_pass anylog_operator1_broker;
       }   
   }
   ```
   ii. To support REST - add the following content in `/etc/nginx/sites-enabled/anylog.conf`
   ```editorconfig
   server {
     listen 32149;
     server_name _;
     location / {
       proxy_set_header Host            $host;
       proxy_set_header X-Forwarded-For $remote_addr;
       proxy_pass http://192.168.49.2:32149;
     }
   }
   ```
   iii. Restart nginx service
   ```shell
   sudo service nginx reload
   sudo service nginx restart 
   ```

4. Attaching to node 
```shell
# get pod name 
kubectl get pod

<< comment 
NAME                                   READY   STATUS    RESTARTS   AGE
anylog-operator-app-784549f88d-pkr     1/1     Running   0          11m

>>

# attach to node 
kubectl attach -it anylog-operator-app-784549f88d-pkr

# to detach: ctrl-p + ctrl-q
```

### Validate Node 
* Get Status
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23"  
    Process         Status       Details                                                                    
    ---------------|------------|--------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 139.162.56.87:32148, Threads Pool: 6                        |
    REST           |Running     |Listening on: 139.162.56.87:32149, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 45.79.74.39:32048                     |
    Publisher      |Not declared|                                                                          |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                            |
    Distributor    |Running     |                                                                          |
    Consumer       |Not declared|                                                                          |
    MQTT           |Running     |                                                                          |
    Message Broker |Running     |Listening on: 139.162.56.87:32150, Threads Pool: 4                        |
    SMTP           |Not declared|                                                                          |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes              |
    Query Pool     |Running     |Threads Pool: 3                                                           |
    Kafka Consumer |Not declared|                                                                          |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-operator-node1

# to detach press: ctrl-d
```
