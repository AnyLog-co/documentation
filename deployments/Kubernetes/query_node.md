# Query Node
A node that coordinates the query process. This node is ideal for communicating with [North Bound](../../northbound%20connectors) 
connectors, as heavy in terms of I/O against other nodes, unless requested by a user or application. 

To understand the steps taken to deploy a query node, please review the [deployment process](query_node_deployment_process.md). 

## Deployment Steps
1. In [deployments/helm/sample-configurations/anylog_query.yaml](https://github.com/AnyLog-co/deployments/blob/master/helm/sample-configurations/anylog_query.yml) 
update configurations. Please note, the `LEDGER_CONN` value is configured against our testnet / demo master node.  
```yaml
#-----------------------------------------------------------------------------------------------------------------------
# The following are the general values used to deploy an AnyLog instance of type: Query | AnyLog version: predevelop
#-----------------------------------------------------------------------------------------------------------------------
general:
 namespace: default
 app_name: anylog
 pod_name: anylog-query-pod
 deployment_name: anylog-query-app
 service_name: anylog-query-svs
 configmap_name: anylog-query-configs
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
   node_type: query
   node_name: anylog-query-node
   company_name: "Company Name"
   # if location is not set, will use `https://ipinfo.io/json` to get coordinates
   location: ""

 networking:
   server: 32348
   rest: 32349
   # Optional broker port
   broker: ""
   # master node is not needed for REST node
   # Optional external & local IP instead of the default values
   external_ip: ""
   local_ip: ""
   # Proxy IP used by Nginx or other loadbalancer
   proxy_ip: 23.239.12.151

 authentication:
   enable: false
   type: ""
   user: ""
   # if location is not set, will use `https://ipinfo.io/json` to get coordinates
   location: ""
   country: ""
   state: ""
   city: ""


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

2. Deploy AnyLog Query 
```shell
helm install ~/deployments/helm/packages/anylog-node-1.22.3.tgz --values ~/deployments/helm/sample-configurations/anylog_query.yaml --name-template anylog-query
```

3. Updating [nginx](../Networking/nginx.md) files to support REST & MQTT communication remotely & restart the service

   i. To Support TCP - add following content in `/etc/nginx/nginx.conf`
   
   ```editorconfig
   stream {
       # AnyLog TCP Connection - repeat the next two steps for each node
       upstream anylog_query {
           server ${KUBE_APISERVER_IP}:32348;
       }
       server {
           listen 32348 so_keepalive=on;
           proxy_pass anylog_query;
       }
   }
   ```
   ii. To support REST - add the following content in `/etc/nginx/sites-enabled/anylog.conf`
   ```editorconfig
   server {
     listen 32349;
     server_name _;
     location / {
       proxy_set_header Host            $host;
       proxy_set_header X-Forwarded-For $remote_addr;
       proxy_pass http://192.168.49.2:32349;
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
anylog-query-app-784549f88d-arp9kr     1/1     Running   0          11m

>>

# attach to node 
kubectl attach -it anylog-query-app-784549f88d-arp9kr

# to detach: ctrl-p + ctrl-q
```

### Validate Node 
* Get Status
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23" 
    Process         Status       Details                                                                    
    ---------------|------------|--------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 23.239.12.151:32348, Threads Pool: 6                        |
    REST           |Running     |Listening on: 23.239.12.151:32349, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                          |
    Publisher      |Not declared|                                                                          |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                            |
    Distributor    |Not declared|                                                                          |
    Consumer       |Not declared|                                                                          |
    MQTT           |Not declared|                                                                          |
    Message Broker |Not declared|No active connection                                                      |
    SMTP           |Not declared|                                                                          |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes              |
    Query Pool     |Running     |Threads Pool: 3                                                           |
    Kafka Consumer |Not declared|                                                                          |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-query-node

# to detach press: ctrl-d
```
