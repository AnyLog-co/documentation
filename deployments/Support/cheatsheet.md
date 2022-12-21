# Cheat Sheet 
## Basic Commands
### Docker
* Starting a container 
```shell 
docker run --network host -it --detach-keys="ctrl-d" --name anylog-node --rm anylogco/anylog-network:develop 

# using docker-compose
cd $HOME/deployments/docker-compose/anylog-rest/ 
docker-compose up -d 
```
* Viewing all containers
```shell
docker ps -a
```
* View volumes
```shell
docker volume ls 
```
* View images 
```shell
docker image ls 
```
* Attaching to a container & Detaching from a container
```shell
# to detach: ctrl-d
docker attach --detach-keys=ctrl-d anylog-node  
```
* Accessing a volume
```shell
# inspect volume to get Mountpoint
docker volume inspect anylog-node_anylog-node-local-scripts 
"""
[
    {
        "CreatedAt": "2022-11-28T17:50:50Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "anylog-operator",
            "com.docker.compose.version": "1.29.2",
            "com.docker.compose.volume": "anylog-operator-node-local-scripts"
        },
        "Mountpoint": "/var/lib/docker/volumes/anylog-node_anylog-node-node-local-scripts/_data",
        "Name": "anylog-operator_anylog-operator-node-local-scripts",
        "Options": null,
        "Scope": "local"
    }
]
"""
 
 # access MountPont - sudo permissions required   
 cd  /var/lib/docker/volumes/anylog-node_anylog-node-node-local-scripts/_data
 
 # view directories / files to changes 
 ls -l 
 
```
* Stopping a container 
```shell
docker stop anylog-node 
```
* Removing an Image
```shell
docker rm anylog-node 
```
* Removing a volume
```shell
docker volume rm anylog-node_anylog-node-local-scripts

# to remove all volumes
echo y | docker volume prune 
```

* A node that was deployed with docker-compose cna be removed using docker-compose as well 
```shell
cd $HOME/deployments/docker-compose/anylog-rest/

# -v will remove volumes associated with the docker-compose
# --rmi all will remove image(s) associated with the docker-compose  
docker-compose down -v --rmi all 
```
### Kubernetes / Helm 
* Starting a container
```shell
git clone https://github.com/AnyLog-co/deployments 
# deploy volume for container 
helm install $HOME/helm/packages/anylog-node-volume-1.22.3.tgz --name-template anylog-node-volume 

# deploy container 
helm install $HOME/helm/packages/anylog-node-1.22.3.tgz --name-template anylog-node
```
* Viewing all services
```shell
# viewing all helm packages deployed 
helm list 

# viewing all Kubernetes instance on default namespace 
kubectl get all 

# viewing all Kubernetes instance
kubectl get all -A 
```
* Attaching to a AnyLog CLI & Detaching from a AnyLog CLI
```shell
# attach to AnyLog CLI -- to detach ctrl-p + ctrl-q
kubecttl attach -it ${POD_NAME}

# attach to docker bash for kubernetes instance 
kubecttl exec -it ${POD_NAME} bash  
```

* Stopping a service - note as long as you don't remove the volume installation data would stay persistent 
```shell
helm delete anylog-node 
```

## Basic AnyLog Commands 
### Validate node is running & check (internal) network communication
* check connections
```anylog
AL anylog-node > get connections
Type      External Address     Local Address        
---------|--------------------|--------------------|
TCP      |139.162.200.15:32048|139.162.200.15:32048|
REST     |139.162.200.15:32049|139.162.200.15:32049|
Messaging|Not declared        |Not declared        | 
```
* view processes
```anylog
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
* view database open against the given node 
```anylog
AL anylog-node > get databases 
List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
blockchain           psql          127.0.0.1:5432                 Persistent
system_query         sqlite        Local                          MEMORY

```
* check local communication
```anylog
AL anylog-node > test node  
```
* check network communication - node should have access to the blockchain
```anylog
AL anylog-node > test network 
```
### Blockchain 
* view all policies on blockchain
```anylog
AL anylog-node > blockchain get * 
```
* get list of all query nodes on blockchain 
```anylog 
AL anylog-node > blockchain get query 
[{'query' : {'hostname' : 'anylog-query',
             'name' : 'anylog-query-node',
             'ip' : '23.239.12.151',
             'local_ip' : '23.239.12.151',
             'company' : 'AnyLog',
             'port' : 32348,
             'rest_port' : 32349,
             'loc' : '40.8223,-74.4569',
             'country' : 'US',
             'state' : 'New Jersey',
             'city' : 'Morris Plains',
             'id' : '83fd249bef7dc7ce6d876b0bd879b686',
             'date' : '2022-08-01T02:09:37.947008Z',
             'ledger' : 'global'}},
 {'query' : {'hostname' : 'anylog-query-node2',
             'name' : 'query-node2',
             'ip' : '45.79.18.179',
             'local_ip' : '45.79.18.179',
             'company' : 'AnyLog',
             'port' : 32348,
             'rest_port' : 32349,
             'loc' : '32.9482,-96.7297',
             'country' : 'US',
             'state' : 'Texas',
             'city' : 'Richardson',
             'id' : 'ebba19b10c2483e1afd71c6f0355fa06',
             'date' : '2022-08-04T20:37:43.958960Z',
             'ledger' : 'global'}}]

```
* view information regarding data nodes (operators)
```anylog 
AL anylog-node > get data nodes 

Company         DBMS          Table                Cluster ID                       Cluster Status Node Name                Member ID External IP/Port      Local IP/Port         Node Status 
---------------|-------------|--------------------|--------------------------------|--------------|------------------------|---------|---------------------|---------------------|-----------|
AFG            |afg          |battery             |56ff4fdcca9d65c5c418cdb62ba35779|active        |afg-cluster3-operator1  |      151|172.105.60.50:32148  |172.105.60.50:32148  |active     |
               |             |                    |bde201429a660306df45d03593d9abb1|active        |afg-cluster1-operator1  |      186|69.164.203.68:32148  |69.164.203.68:32148  |active     |
               |             |                    |07b9b4ca2955299adb44e82ef679c7f6|active        |afg-cluster2-operator1  |       73|172.105.6.90:32148   |172.105.6.90:32148   |active     |
AFG            |afg          |inverter            |56ff4fdcca9d65c5c418cdb62ba35779|active        |afg-cluster3-operator1  |      151|172.105.60.50:32148  |172.105.60.50:32148  |active     |
               |             |                    |07b9b4ca2955299adb44e82ef679c7f6|active        |afg-cluster2-operator1  |       73|172.105.6.90:32148   |172.105.6.90:32148   |active     |
               |             |                    |bde201429a660306df45d03593d9abb1|active        |afg-cluster1-operator1  |      186|69.164.203.68:32148  |69.164.203.68:32148  |active     |
AFG            |afg          |eswitch             |56ff4fdcca9d65c5c418cdb62ba35779|active        |afg-cluster3-operator1  |      151|172.105.60.50:32148  |172.105.60.50:32148  |active     |
               |             |                    |07b9b4ca2955299adb44e82ef679c7f6|active        |afg-cluster2-operator1  |       73|172.105.6.90:32148   |172.105.6.90:32148   |active     |
               |             |                    |bde201429a660306df45d03593d9abb1|active        |afg-cluster1-operator1  |      186|69.164.203.68:32148  |69.164.203.68:32148  |active     |
AFG            |afg          |solar               |56ff4fdcca9d65c5c418cdb62ba35779|active        |afg-cluster3-operator1  |      151|172.105.60.50:32148  |172.105.60.50:32148  |active     |
               |             |                    |bde201429a660306df45d03593d9abb1|active        |afg-cluster1-operator1  |      186|69.164.203.68:32148  |69.164.203.68:32148  |active     |
               |             |                    |07b9b4ca2955299adb44e82ef679c7f6|active        |afg-cluster2-operator1  |       73|172.105.6.90:32148   |172.105.6.90:32148   |active     |
AFG            |afg          |pmu                 |56ff4fdcca9d65c5c418cdb62ba35779|active        |afg-cluster3-operator1  |      151|172.105.60.50:32148  |172.105.60.50:32148  |active     |
               |             |                    |bde201429a660306df45d03593d9abb1|active        |afg-cluster1-operator1  |      186|69.164.203.68:32148  |69.164.203.68:32148  |active     |
               |             |                    |07b9b4ca2955299adb44e82ef679c7f6|active        |afg-cluster2-operator1  |       73|172.105.6.90:32148   |172.105.6.90:32148   |active     |
AFG            |afg          |synchrophasor       |07b9b4ca2955299adb44e82ef679c7f6|active        |afg-cluster2-operator1  |       73|172.105.6.90:32148   |172.105.6.90:32148   |active     |
               |             |                    |bde201429a660306df45d03593d9abb1|active        |afg-cluster1-operator1  |      186|69.164.203.68:32148  |69.164.203.68:32148  |active     |
Lit San Leandro|litsanleandro|ping_sensor         |efb22a109434b64244fc01fea01e711b|active        |lsl-cluster2-operator2  |      169|172.105.112.207:32148|172.105.112.207:32148|active     |
               |             |                    |                                |active        |lsl-cluster2-operator1  |       25|139.162.164.95:32148 |139.162.164.95:32148 |active     |
               |             |                    |091ced55d3ff918bbe440e20251b30cd|active        |lsl-cluster3-operator1  |       33|172.105.13.202:32148 |172.105.13.202:32148 |active     |
               |             |                    |                                |active        |lsl-cluster3-operator2  |      243|50.116.61.153:32148  |50.116.61.153:32148  |active     |
               |             |                    |0015392622f3eaac70eafa4311fc2338|active        |lsl-cluster1-operator1  |       76|139.162.126.241:32148|139.162.126.241:32148|active     |
               |             |                    |                                |active        |lsl-cluster1-operator2  |       77|139.177.192.209:32148|139.177.192.209:32148|active     |
Lit San Leandro|litsanleandro|percentagecpu_sensor|efb22a109434b64244fc01fea01e711b|active        |lsl-cluster2-operator2  |      169|172.105.112.207:32148|172.105.112.207:32148|active     |
               |             |                    |                                |active        |lsl-cluster2-operator1  |       25|139.162.164.95:32148 |139.162.164.95:32148 |active     |
               |             |                    |0015392622f3eaac70eafa4311fc2338|active        |lsl-cluster1-operator1  |       76|139.162.126.241:32148|139.162.126.241:32148|active     |
               |             |                    |                                |active        |lsl-cluster1-operator2  |       77|139.177.192.209:32148|139.177.192.209:32148|active     |
               |             |                    |091ced55d3ff918bbe440e20251b30cd|active        |lsl-cluster3-operator1  |       33|172.105.13.202:32148 |172.105.13.202:32148 |active     |
               |             |                    |                                |active        |lsl-cluster3-operator2  |      243|50.116.61.153:32148  |50.116.61.153:32148  |active     |
NTT            |ntt          |deeptector          |f0a62fce8bff170fc0d72f4adc35d0a8|active        |ntt-operator-node-remote|       55|176.58.126.170:32148 |176.58.126.170:32148 |active     |
IOTech System  |edgex        |rand_data           |8dbb1fdab6d1b0c181e630ff4bb74e3a|active        |edgex-cluster1-operator1|      180|172.105.86.168:32148 |172.105.86.168:32148 |active     |
               |             |                    |0172634946c53e4c9bbede925182aa18|active        |edgex-cluster2-operator1|      188|139.162.56.87:32148  |139.162.56.87:32148  |active     |
IOTech System  |edgex        |videos              |8dbb1fdab6d1b0c181e630ff4bb74e3a|active        |edgex-cluster1-operator1|      180|172.105.86.168:32148 |172.105.86.168:32148 |active     |
               |             |                    |0172634946c53e4c9bbede925182aa18|active        |edgex-cluster2-operator1|      188|139.162.56.87:32148  |139.162.56.87:32148  |active     |

```

### Other Commands
* list of tables in blockchain 
```shell
# using blockchain command 
blockchain get table bring [table][name] separator=\n

# using get function 
get tables where dbms=*
Database      Table name                             Local DBMS Blockchain 
-------------|--------------------------------------|----------|----------|
afg          |battery                               | -        | V        |
             |eswitch                               | -        | V        |
             |inverter                              | -        | V        |
             |pmu                                   | -        | V        |
             |solar                                 | -        | V        |
             |synchrophasor                         | -        | V        |
edgex        |par_rand_data_2022_11_02_d07_timestamp| V        | -        |
             |par_rand_data_2022_11_03_d07_timestamp| V        | -        |
             |par_rand_data_2022_11_04_d07_timestamp| V        | -        |
             |par_rand_data_2022_12_00_d07_timestamp| V        | -        |
             |par_rand_data_2022_12_01_d07_timestamp| V        | -        |
             |par_rand_data_2022_12_02_d07_timestamp| V        | -        |
             |par_videos_2022_11_01_d07_timestamp   | V        | -        |
             |par_videos_2022_11_02_d07_timestamp   | V        | -        |
             |par_videos_2022_11_03_d07_timestamp   | V        | -        |
             |par_videos_2022_11_04_d07_timestamp   | V        | -        |
             |par_videos_2022_12_00_d07_timestamp   | V        | -        |
             |par_videos_2022_12_01_d07_timestamp   | V        | -        |
             |rand_data                             | V        | V        |
             |videos                                | V        | V        |
             |plc_device                            | -        | V        |
             |traffic_data                          | -        | V        |
fledge       |openweathermap                        | -        | V        |
             |random                                | -        | V        |
litsanleandro|percentagecpu_sensor                  | -        | V        |
             |ping_sensor                           | -        | V        |
ntt          |deeptector                            | -        | V        |
```

* View statistics on the streaming processes
```anylog 
AL anylog-node > get streaming 
Flush Thresholds
Threshold         Value  Streamer 
-----------------|------|--------|
Default Time     |    60|Running |
Default Volume   |10,240|        |
Default Immediate|True  |        |
Buffered Rows    |    82|        |
Flushed Rows     |     0|        |


Statistics
             Put    Put     Streaming Streaming Cached Counter    Threshold   Buffer   Threshold  Time Left Last Process 
DBMS-Table   files  Rows    Calls     Rows      Rows   Immediate  Volume(KB)  Fill(%)  Time(sec)  (Sec)     HH:MM:SS     
------------|------|-----|-|---------|---------|------|----------|-----------|--------|----------|---------|------------|
edgex.videos|    82|   82| |        0|        0|     0|         0|          0|       0|         0|        0|939:51:52   |

```

* view data coming in on Operator node 
```anylog 
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

* view data coming in on Publisher node 
```anylog 
AL anylog-node > get publisher
Publisher process is running
Configuration:

Key               Value
---------------   -----
compress_json   : [True]
compress_sql    : [True]
master_node     : ['45.79.74.39:32048']
dbms_name       : [0]
table_name      : [0]
watch_dir       : ['/app/AnyLog-Network/data/watch/']
err_dir         : ['/app/AnyLog-Network/data/error/']
bkup_dir        : ['/app/AnyLog-Network/data/bkup/']
archive_dir     : ['/app/AnyLog-Network/data/archive/']
blockchain_file : ['/app/AnyLog-Network/blockchain/blockchain.json']
file_type       : ['json', 'sql']


Statistics:
DBMS                   TABLE                  FILES      LAST TRANSFER       DESTINATION
---------------------- ---------------------- ---------- ------------------- -------------------
litsanleandro          percentagecpu_sensor        52184 2022-12-21 02:57:19 172.105.13.202:32148
edgex                  rand_data                   60348 2022-12-21 02:58:25 172.105.86.168:32148
litsanleandro          ping_sensor                 26701 2022-12-21 02:56:12 172.105.112.207:32148
afg                    solar                       44676 2022-12-21 02:57:59 172.105.6.90:32148
afg                    battery                     44609 2022-12-21 02:58:04 69.164.203.68:32148
afg                    inverter                    44664 2022-12-21 02:58:09 69.164.203.68:32148
afg                    eswitch                     44610 2022-12-21 02:58:14 172.105.60.50:32148
afg                    pmu                         44655 2022-12-21 02:58:20 172.105.60.50:32148
afg                    synchrophasor               44604 2022-12-21 02:58:25 69.164.203.68:32148

Files moved to error dir:   1322
```

* view data coming in via `run mqtt client`
```
run mqtt client
```
* query data 
```anylog
AL anylog-node > run client () sql test format=table "select * from rand_data"
row_id insert_timestamp           tsd_name tsd_id timestamp                  value        
------ -------------------------- -------- ------ -------------------------- ------------ 
     1 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:00.682831 1890264146.0 
     2 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:00.899964       3505.0 
     3 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:00.900518        109.0 
     4 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:20.668691      17140.0 
     5 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:20.885815        -29.0 
     6 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:20.886417 -426977856.0 
     7 2022-11-21 00:00:45.718601      180  51559 2022-11-21 00:00:40.671727      23954.0 
     8 2022-11-21 00:02:45.847600      180  51560 2022-11-21 00:01:40.889366 -404033083.0 
     9 2022-11-21 00:02:45.847600      180  51560 2022-11-21 00:01:40.893219         48.0 
    10 2022-11-21 00:02:45.847600      180  51560 2022-11-21 00:02:00.673841      -7192.0 
...
```

* Get the status of the last executed queries
```anylog 
AL anylog-node > query status
AL anylog-query-node +> query status

Job  ID Output Run Time Operator             Par Status    Blocks Rows Command                          
----|--|------|--------|--------------------|---|---------|------|----|--------------------------------|
0061|62|stdout|00:00:01|All                 |---|Completed|    37| 370|select * from rand_data limit 10|
    |  |      |00:00:00|172.105.86.168:32148|  0|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  1|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  2|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  3|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  4|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  5|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  6|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  7|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  8|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  9|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 10|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 11|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 12|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 13|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 14|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 15|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 16|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 17|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 18|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 19|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 20|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 21|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 22|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 23|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 24|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 25|Completed|     1|  10|                                |
    |  |      |00:00:00|                    | 26|Completed|     1|  10|                                |
    |  |      |00:00:01|                    | 27|Completed|     1|  10|                                |
    |  |      |00:00:01|                    | 28|Completed|     1|  10|                                |
    |  |      |00:00:01|                    | 29|Completed|     1|  10|                                |
    |  |      |00:00:01|                    | 30|Completed|     1|  10|                                |
    |  |      |00:00:00|139.162.56.87:32148 |  0|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  1|Completed|     1|  10|                                |
    |  |      |00:00:00|                    |  2|Completed|     1|  10|                                |
    |  |      |00:00:01|                    |  3|Completed|     1|  10|                                |
    |  |      |00:00:01|                    |  4|Completed|     1|  10|                                |
    |  |      |00:00:01|                    |  5|Completed|     1|  10|                                |
```
* Sample cURL commands
```shell  
# run command against the "local" node 
curl -X GET ${IP}:${REST_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"

# run query against the entire network 
curl -X GET ${IP}:${REST_PORT} -H 'command: run test format=table "select * from rand_data;"' -H "User-Agent: AnyLog/1.23" -H "destination: network" 

# run query against a specific node
curl -X GET ${IP}:${REST_PORT} -H 'command: run test format=table "select * from rand_data;"' -H "User-Agent: AnyLog/1.23" -H "destination: ${OPERATOR_IP}:${OPERATOR_TCP_PORT}" 
```


All AnyLog commands can be run via either the AnyLog CLI and REST.  
