# Overlay Networks

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/). 

**Documentation**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs)
* [Defines' Website](https://www.defined.net/)

## Terminology 
_Nebula's_ overlay network requires a minimum of 2 nodes: _lighthouse_ and regular nodes, nicknamed _host_, as well as 
authentication certificates for the nodes to be associated with one another.  

* **Lighthouse**: A _Nebula_ host that is responsible for facilitating nodes discover each other by acting as a static 
reference point; helping them find each other within a Nebula ntwork. When data is sent from non-Lighthouse 1 (host1) to 
non-Lighthouse 2 (host2), the data does not go through the lighthouse. Instead, host1 obtains information needed to 
send a data to host2 from the lighthouse.
In order to eliminate the dependency on a single lighthouse, Nebula offers advanced configuration to support 
[multiple lighthouses](https://www.defined.net/blog/newsletter-admin-api-cert-rotation-multiple-lighthouses/#support-for-multiple-lighthouses).
We recommend either a generic or query node to act as the lighthouse. 


* **Host**: A _Nebula_ host is simply any single node in the network, e.g. a server, laptop, phone, tablet. Each host will 
have its own private key, which is used to validate the identity of that host when Nebula tunnels are created.


* **Certificate Authority**: Nebula Certificate Authority (CA) consists of two files, a CA certificate, and an associated 
private key. CA certificate is distributed to, and trusted by, every host on the network. The CA private key should not be 
distributed, and can be kept offline when not being used to add hosts to a Nebula network.

## Deploy Nebula via AnyLog

### Requirements

Nebula uses port 4242 (by default) as an entry point for communication between Nebula nodes. 

### Steps
**For Lighthouse**: 
1. In advanced configs, set the overlay IP address and update nebula configs as shown below. 
The CIDR_OVERLAY_ADDRESS should have the same IP value as the overlay IP address.
```dotenv
... 
#--- Networking ---
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=10.10.1.1
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
...
 
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=true
# whether node is type lighthouse
IS_LIGHTHOUSE=true
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24) 
CIDR_OVERLAY_ADDRESS=10.10.1.1/24 
# Nebula IP address for Lighthouse node (ex. 10.10.1.15) 
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP="" 
```

2. Start Node
```shell 
make up ANYLOG_TYPE=generic
```

3. Validate node is working with overlay  
```shell    
make test-node
<<COMMENT
root@localhost:~/docker-compose# make test-node
REST Connection Info for testing (Example: 127.0.0.1:32149):
10.10.1.1:32549
Node State against 10.10.1.1:32549
anylog-node@172.232.20.156:32548 running

Test                                    Status                                                               
---------------------------------------|--------------------------------------------------------------------|
Metadata Version                       |                                                                   0|
Metadata Test                          |Failed                                                              |
TCP test using 10.10.1.1:32548         |[From Node 10.10.1.1:32548] anylog-node@172.232.20.156:32548 running|
REST test using http://10.10.1.1:32549 |anylog-node@172.232.20.156:32548 running                            |


    Process         Status       Details                                                                                          
    ---------------|------------|------------------------------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.232.20.156:32548 and 10.10.1.1:32548, Threads Pool: 6                         |
    REST           |Running     |Listening on: 172.232.20.156:32549 and 10.10.1.1:32549, Threads Pool: 6, Timeout: 30, SSL: False|
    Operator       |Not declared|                                                                                                |
    Blockchain Sync|Not declared|                                                                                                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)]                                                             |
    Blobs Archiver |Not declared|                                                                                                |
    MQTT           |Not declared|                                                                                                |
    Message Broker |Not declared|No active connection                                                                            |
    SMTP           |Not declared|                                                                                                |
    Streamer       |Not declared|                                                                                                |
    Query Pool     |Running     |Threads Pool: 3                                                                                 |
    Kafka Consumer |Not declared|                                                                                                |
    gRPC           |Not declared|                                                                                                |
    Publisher      |Not declared|                                                                                                |
    Distributor    |Not declared|                                                                                                |
    Consumer       |Not declared|                                                                                                |
<<     
```

4. Update advanced configs to disable generating new nebula keys. Otherwise, when the node restarts, the overlay network would 
use different keys than before. 
```dotenv
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=true
# whether node is type lighthouse
IS_LIGHTHOUSE=true
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24) 
CIDR_OVERLAY_ADDRESS=10.10.1.1/24 
# Nebula IP address for Lighthouse node (ex. 10.10.1.15) 
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP="" 
```

**Copy Keys**: Steps are all done via the lighthouse node
1. For each new node, generate private key and certificate on the lighthouse node 
```shell
make exec ANYLOG_TYPE=generic
cd $ANYLOG_PATH/nebula
./nebula-cert sign -name "new-node" -ip "${CIDR_OVERLAY_ADDRESS}"
```

2. Locate path for nebula volume
```shell        
docker volume inspect docker-makefile_nebula-overlay 
<<COMMENT
[
    {
        "CreatedAt": "2024-10-04T21:12:45Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "docker-makefile",
            "com.docker.compose.version": "2.29.7",
            "com.docker.compose.volume": "nebula-overlay"
        },
        "Mountpoint": "/var/lib/docker/volumes/docker-makefile_nebula-overlay/_data", # <-- this is the path we'll want
        "Name": "docker-makefile_nebula-overlay",
        "Options": null,
        "Scope": "local"
    }
] 
<< 
```

3. Locate ca.crt in nebula volume
```shell
sudo ls -l  /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data
<<COMMENT
total 39688
drwxr-xr-x 2 root root     4096 Oct  4 21:12 archive_certs
-rw------- 1 root root      243 Oct  4 21:12 ca.crt # <-- public key, should be shared among all nodes in (nebula) network
-rw------- 1 root root      174 Oct  4 21:12 ca.key # <-- private key
-rw-r--r-- 1 root root     5585 Oct  1 19:28 config_nebula.py
-rw-r--r-- 1 root root    16518 Oct  1 03:07 config.yml
-rw-r--r-- 1 root root     2416 Oct  4 20:27 deploy_nebula.sh
-rw-r--r-- 1 root root       38 Aug 30 06:11 export_nebula.sh
-rw------- 1 root root      292 Oct  4 21:12 host.crt # <-- public key specifically by the node used to identify the lighthouse in the network and for encryption purposes.
-rw------- 1 root root      127 Oct  4 21:12 host.key # <-- private key specifically for the node used by the lighthouse for its own identity and secure communication
-rwxr-xr-x 1 1001  127 18986052 Jan  8  2024 nebula
-rwxr-xr-x 1 1001  127  7675668 Jan  8  2024 nebula-cert
-rw-r--r-- 1 root root     1589 Oct  4 21:12 nebula.log
-rw-r--r-- 1 root root 13906330 Jan  8  2024 nebula.tar.gz
-rw------- 1 root root      300 Oct  5 00:48 new-node.crt # <-- public key generated for new node in step 1
-rw------- 1 root root      127 Oct  5 00:48 new-node.key # <-- public key generated for new node in step 1
-rw-r--r-- 1 root root      843 Oct  4 21:12 node.yml
```

4. scp `ca.crt` and node key and certificate for new node. Notice _node_ key and certification are renamed to _host_. 
```shell 
sudo scp /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data/node.crt [user_name]@[ip]:~/host.crt
sudo scp /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data/node.key [user_name]@[ip]:~/host.key  
sudo scp /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data/ca.crt [user_name]@[ip]:~/
```

When deploying other AnyLog nodes on the same physical machine there is not need to repeat this step as the nebula volume is the 
same for all containers.   

**For Hosts**: 
The following will cover how to add a new AnyLog node to the overlay network. In the example we'll be using the Query 
node, but the same logic can be applied to Operator, Publisher and Master nodes.

1. When deploying a new AnyLog node, that seats on a host machine without Nebula preset, make sure `ca.crt` exists on 
the machine. See _Copy Keys_ above for directions on how to obtain `ca.crt` file. 

2. Update `.env` configuration files (docker-compose/docker-makefile/.env) to deploy a _bash_ based interface of the   
docker container in order to copy the certificate into the new AnyLog container. 
```dotenv
# AnyLog init type
# -> prod: run AnyLog instance
# -> bash: run shell interface with AnyLog installed and params set
INIT_TYPE=bash

# AnyLog immage
IMAGE=anylogco/anylog-network

# params for Remote-CLI
CONN_IP=0.0.0.0
CLI_PORT=31800
```

3. In advanced configs, set the overlay IP address and update nebula configs as shown below. 
The CIDR_OVERLAY_ADDRESS should be the same as the CIDR value set in the lighthouse node (AnyLog Generic). 
```dotenv
... 
#--- Networking ---
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=10.10.1.31
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
...
 
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=true
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24) 
CIDR_OVERLAY_ADDRESS=10.10.1.1/24 
# Nebula IP address for Lighthouse node (ex. 10.10.1.15) 
LIGHTHOUSE_IP=10.10.1.1
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=172.232.20.156
```
To get `LIGHTHOUSE_NODE_IP` attach to the AnyLog container associated with the lighthouse and simpy request `!external_ip`. 

4. Bring up the AnyLog container 
```shell
make up ANYLOG_TYPE=queryy
```

5. Locate where nebula volume path, in order to copy the `ca.crt` file to  
```shell
docker volume inspect docker-makefile_nebula-overlay 
<<COMMENT
[
    {
        "CreatedAt": "2024-10-04T21:12:45Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "docker-makefile",
            "com.docker.compose.version": "2.29.7",
            "com.docker.compose.volume": "nebula-overlay"
        },
        "Mountpoint": "/var/lib/docker/volumes/docker-makefile_nebula-overlay/_data", # <-- this is the path we'll want
        "Name": "docker-makefile_nebula-overlay",
        "Options": null,
        "Scope": "local"
    }
] 
<< 
```

6. Copy `ca.crt` into nebula volume 
```shell
sudo cp $HOME/ca.crt /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data
sudo cp $HOME/host.key /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data
sudo cp $HOME/host.crt /var/lib/docker/volumes/docker-makefile_nebula-overlay/_data
```

7. Update `.env` configuration files (docker-compose/docker-makefile/.env) to deploy AnyLog 
```dotenv
# AnyLog init type
# -> prod: run AnyLog instance
# -> bash: run shell interface with AnyLog installed and params set
INIT_TYPE=prod

# AnyLog immage
IMAGE=anylogco/anylog-network

# params for Remote-CLI
CONN_IP=0.0.0.0
CLI_PORT=31800
```

8. Update advanced configs to disable generating new nebula keys. Otherwise, when the node restarts, the overlay network would 
remove the certificates used to communicate with the lighthouse
```dotenv
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=false
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24) 
CIDR_OVERLAY_ADDRESS=10.10.1.1/24 
# Nebula IP address for Lighthouse node (ex. 10.10.1.15) 
LIGHTHOUSE_IP=10.10.1.1
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=172.232.20.156
```

9. Restart AnyLog container with correct certification 
```shell
make down ANYLOG_TYPE=query
make up ANYLOG_TYPE=query
```

10. Test Node

**Multiple Nodes on one Machine**: 
When deploying additional AnyLog containers on the same machine, they'll all use the same OVERLAY IP address. 
1. In advanced configs, set the overlay IP address and update nebula configs as shown below. In general, it is the same
as the pre-existing configurations of the other AnyLog nodes, but makes sure `NEBULA_NEW_KEYS` is set to _false_. 
* When seating on the same machine as the lighthouse node

```dotenv
#--- Networking ---
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=10.10.1.1
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
...
 
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=false
# whether node is type lighthouse
IS_LIGHTHOUSE=true
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24) 
CIDR_OVERLAY_ADDRESS=10.10.1.1/24 
# Nebula IP address for Lighthouse node (ex. 10.10.1.15) 
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=""
```

* When seating on the same machine as another non-lighthouuse node
```dotenv
#--- Networking ---
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=10.10.1.31
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
...
 
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=false
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24) 
CIDR_OVERLAY_ADDRESS=10.10.1.1/24 
# Nebula IP address for Lighthouse node (ex. 10.10.1.15) 
LIGHTHOUSE_IP=10.10.1.1
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=172.232.20.156```
```

2. Deploy AnyLog container
```shell
make up ANYLOG_TYPE=[NODE_TYPE]
```

3. Test node

