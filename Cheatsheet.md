# Cheatsheet 

The following is intended as a "cheatsheet" or "FAQ" document containing some sample commands, showing basic functionality
to validate an _AnyLog_ node and/or _EdgeX_ is running. 

We recommend starting with [deployments](deployments) for detailed  explanation of how to deploy configure and AnyLog.

### Starting a Node
* How to start a node
```shell
# docker
anylog@new-node:~$ cd deployments/docker-compose/anylog-rest
anylog@new-node:~$ docker-compose up -d 
```
* How to attach to a node
```shell
# docker -- ctrl-d to detach 
docker attach --detach-keys="ctrl-d" anylog-node 
```
* validate node is running 
```shell
anylog@new-node:~$ curl -X GET ${IP}:${REST_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"
```

### Within AnyLog 
* get list of network connections
```commandline
AL anylog-node > get connections
Type      External Address     Local Address        
---------|--------------------|--------------------|
TCP      |139.162.200.15:32048|139.162.200.15:32048|
REST     |139.162.200.15:32049|139.162.200.15:32049|
Messaging|Not declared        |Not declared        | 
```
* view running processes
```commandline
AL anylog-node > get processes 

    Process         Status       Details                                                                     
    ---------------|------------|---------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 139.162.200.15:32048, Threads Pool: 6                        |
    REST           |Running     |Listening on: 139.162.200.15:32049, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                           |
    Publisher      |Not declared|                                                                           |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 127.0.0.1:32048                   |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                             |
    Distributor    |Not declared|                                                                           |
    Consumer       |Not declared|                                                                           |
    MQTT           |Not declared|                                                                           |
    Message Broker |Not declared|No active connection                                                       |
    SMTP           |Not declared|                                                                           |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes               |
    Query Pool     |Running     |Threads Pool: 3                                                            |
    Kafka Consumer |Not declared|                                                                           |
```
* get list of connected databases 
```commandline
AL anylog-node > get databases 

List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
blockchain           psql          127.0.0.1:5432                 Persistent
system_query         sqlite        Local                          MEMORY
```
* view data coming into Operator
```commandline
AL anylog-node > get operator 

Status:     Active
Time:       1:37:43 (H:M:S)
Policy:     29ebc0cf136de22b25c3036a32363f65
Cluster:    e9c30c8935f845a8976ff0f827378b92
Member:     113
Statistics JSON files:
DBMS                   TABLE                  FILES      IMMEDIATE  LAST PROCESS
---------------------- ---------------------- ---------- ---------- --------------------
test                  rand_data                       4         90 2022-07-29 00:34:07

Statistics SQL files:
DBMS                   TABLE                  FILES      IMMEDIATE  LAST PROCESS
---------------------- ---------------------- ---------- ---------- --------------------
test                  rand_data                       4          0 2022-07-29 00:01:05

Errors summary
Error Type           Counter DBMS Name Table Name Last Error Last Error Text 
--------------------|-------|---------|----------|----------|---------------|
Duplicate JSON Files|      0|         |          |         0|               |
JSON Files Errors   |      0|         |          |         0|               |
SQL Files Errors    |      0|         |          |         0|               |
```
* view data coming via [`run mqtt client`](message%20broker.md)
```commandline
AL anylog-node > get msg client 

Subscription: 0001
User:         unused
Broker:       local
Connection:   Not connected: MQTT_ERR_NO_CONN

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
            843         843           0  2022-07-29 00:34:24
     
     Subscribed Topics:
     Topic       QOS DBMS  Table     Column name Column Type Mapping Function        Optional Policies 
     -----------|---|-----|---------|-----------|-----------|-----------------------|--------|--------|
     anylogedgex|  0|test|rand_data|timestamp  |timestamp  |now()                  |False   |        |
                |   |     |         |value      |float      |['[readings][][value]']|False   |        |

     
     Directories Used:
     Directory Name Location                       
     --------------|------------------------------|
     Prep Dir      |/app/AnyLog-Network/data/prep |
     Watch Dir     |/app/AnyLog-Network/data/watch|
     Error Dir     |/app/AnyLog-Network/data/error|
```
### EdgeX
[Directions for EdgeX](deployments/Docker/EdgeX.md)
* Validate EdgeX is running
```shell
anylog@new-node:~$ docker ps -a | grep edgex 
root@edgex-operator2:~# docker ps -a | grep edgex
a13b169023b7   emqx/kuiper:1.1.1-alpine                                                   "/usr/bin/docker-ent…"   45 hours ago   Up 44 hours             127.0.0.1:20498->20498/tcp, 9081/tcp, 127.0.0.1:48075->48075/tcp                       edgex-kuiper
56a3482bdfc8   edgexfoundry/docker-sys-mgmt-agent-go:1.3.1                                "/sys-mgmt-agent -cp…"   45 hours ago   Up 44 hours             127.0.0.1:48090->48090/tcp                                                             edgex-sys-mgmt-agent
2740875f17a4   edgexfoundry/docker-app-service-configurable:1.3.1                         "/app-service-config…"   45 hours ago   Up 44 hours             48095/tcp, 127.0.0.1:48101->48101/tcp                                                  edgex-app-service-configurable-mqtt
32b749bbd104   edgexfoundry/docker-device-random-go:1.3.1                                 "/device-random --cp…"   45 hours ago   Up 44 hours             127.0.0.1:49988->49988/tcp                                                             edgex-device-random
e960f5ff00c5   edgexfoundry/docker-app-service-configurable:1.3.1                         "/app-service-config…"   45 hours ago   Up 44 hours             48095/tcp, 127.0.0.1:48100->48100/tcp                                                  edgex-app-service-configurable-rules
e50c8de4b879   edgexfoundry/docker-device-modbus-go:1.3.1                                 "/device-modbus --cp…"   45 hours ago   Up 44 hours             127.0.0.1:49991->49991/tcp                                                             edgex-device-modbus
e91cd4ad63fa   edgexfoundry/docker-core-command-go:1.3.1                                  "/core-command -cp=c…"   45 hours ago   Up 44 hours             127.0.0.1:48082->48082/tcp                                                             edgex-core-command
59464a3a976d   edgexfoundry/docker-core-data-go:1.3.1                                     "/core-data -cp=cons…"   45 hours ago   Up 44 hours             127.0.0.1:5563->5563/tcp, 127.0.0.1:48080->48080/tcp                                   edgex-core-data
b706d9584413   edgexfoundry/docker-core-metadata-go:1.3.1                                 "/core-metadata -cp=…"   45 hours ago   Up 44 hours             127.0.0.1:48081->48081/tcp                                                             edgex-core-metadata
13abb3559d2a   edgexfoundry/docker-support-notifications-go:1.3.1                         "/support-notificati…"   45 hours ago   Up 44 hours             127.0.0.1:48060->48060/tcp                                                             edgex-support-notifications
ff7d350ca3ba   edgexfoundry/docker-support-scheduler-go:1.3.1                             "/support-scheduler …"   45 hours ago   Up 44 hours             127.0.0.1:48085->48085/tcp                                                             edgex-support-scheduler
0346e264f6d6   edgexfoundry/docker-edgex-consul:1.3.0                                     "edgex-consul-entryp…"   45 hours ago   Up 44 hours             8300-8302/tcp, 8400/tcp, 8301-8302/udp, 8600/tcp, 8600/udp, 127.0.0.1:8500->8500/tcp   edgex-core-consul
fab7cbdcc29f   redis:6.0.9-alpine                                                         "docker-entrypoint.s…"   45 hours ago   Up 44 hours             127.0.0.1:6379->6379/tcp                                                               edgex-redis
f135b724626e   nexus3.edgexfoundry.org:10003/edgex-devops/edgex-modbus-simulator:latest   "/simulator"             45 hours ago   Up 44 hours             127.0.0.1:1502->1502/tcp                                                               edgex-modbus-simulator
```
* View Data coming in
```shell
anylog@new-node:~$ curl http://127.0.0.1:48080/api/v1/reading | jq 
[
  {
    "id": "000767a3-61bb-49e1-93ff-be4695eb5b43",
    "created": 1659412501505,
    "origin": 1659412501498780400,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int16",
    "value": "10380",
    "valueType": "Int16"
  },
  {
    "id": "000797b4-736b-48b9-bbe5-09594be7099f",
    "created": 1659403221133,
    "origin": 1659403221133020700,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int32",
    "value": "771919435",
    "valueType": "Int32"
  },
  {
    "id": "00079ae9-340a-4d70-9e0b-9a5a8b48e216",
    "created": 1659412541467,
    "origin": 1659412541463869400,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int8",
    "value": "27",
    "valueType": "Int8"
  },
  {
    "id": "0008d23e-7640-4974-aaeb-179e375566cb",
    "created": 1659425642023,
    "origin": 1659425642019472400,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int8",
    "value": "-87",
    "valueType": "Int8"
  },
  {
    "id": "000f547c-25b7-4d96-b862-67467345a74c",
    "created": 1659461623534,
    "origin": 1659461623530927000,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int8",
    "value": "-49",
    "valueType": "Int8"
  },
  ...
]
```