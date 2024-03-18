# Nebula Through AnyLog

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/). 

_Nebula_ is a mutually authenticated peer-to-peer overlay network, based on [Noise Protocol Framework](https://noiseprotocol.org/). 
This means that Nebula's overlay network uses certificates to assert a node's IP address, name, and membership within 
user-defined groups. 

By default, AnyLog is provided with pre-set certification. This allows the user to just declare Nebula configuration file 
and configure the desired `OVERLAY_IP` value in order to deploy AnyLog with Nebula. Please note, using this tactic means 
your nodes can be accessed by people using the pre-set certifications.

In order to resolve the issue mentioned above, users can do 2 things:  
* [Personalize Nebula](nebula.md) & [Updating Docker for Nebula](#personalized-nebula)  
* Directions to secure your network with AnyLog can be found [here](../../secure%20network.md)

**Documentation**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs)
* [Defines' Website](https://www.defined.net/)
* [Configuring Overlay with AnyLog](Configuring%20Overlay%20with%20AnyLog.md)

## Deploying with pre-set Nebula 

1. In [advanced_configs.env](https://github.com/AnyLog-co/deployments/blob/main/docker-compose/anylog-master/advance_configs.env), 
update the **NEBULA** section as well as the `OVERLAY_IP` value in **Networking** section
* configurations for a lighthouse node 
```dotenv
#--- Networking ---
...
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=192.168.100.100
...

#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# whether node is type lighthouse
IS_LIGHTHOUSE=true
# Nebula IP address for Lighthouse node
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP="" 
```
* configurations for non-lighthouse node
```dotenv
#--- Networking ---
...
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=192.168.100.101
...

#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula IP address for Lighthouse node
LIGHTHOUSE_IP=192.168.100.100
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=172.105.4.105
```

2. Enable [TUN/TAP driver](https://docs.kernel.org/networking/tuntap.html) to provide packet reception and transmission 
for user space programs. 
```shell
sudo modprobe tun
```

3. Deploy AnyLog 
```shell
bash deployments/run.sh docker master up
```

## Personalized Certification keys
Since security is critical, can use their own Nebula keys for certifying nodes

0. Make a directory called `nebula` - which will be used for all necessary files, unless stated otherwise 
```shell
cd $HOME
mkdir nebula 
cd $HOME/nebula
```

1. Downloading Nebula & Untar the Nebula software - the example below uses the latest version of Nebula (for Linux amd64), other version can be found [here](https://github.com/slackhq/nebula/releases)   
```shell
wget https://github.com/slackhq/nebula/releases/download/v1.7.2/nebula-linux-amd64.tar.gz
tar -xzvf nebula-linux-amd64.tar.gz 

<< COMMENT
root@anylog-master:~/nebula# ls -l 
total 39360
-rwxr-xr-x 1 1001  123 18811965 Jun  1 15:21 nebula
-rwxr-xr-x 1 1001  123  7664823 Jun  1 15:21 nebula-cert
-rw-r--r-- 1 root root 13820988 Jun  1 15:29 nebula-linux-amd64.tar.gz
<< COMMENT
```

2. Creating your certificate authority - certificate authority is used to create credentials that prove a host should be trusted by your organization
```shell
./nebula-cert ca -name "New Company"

<< COMMENT
root@anylog-master:~/nebula# ls -l 
total 39368
-rw------- 1 root root      243 Aug  3 01:36 ca.crt # <-- new file 
-rw------- 1 root root      174 Aug  3 01:36 ca.key # <-- new file 
-rwxr-xr-x 1 1001  123 18811965 Jun  1 15:21 nebula
-rwxr-xr-x 1 1001  123  7664823 Jun  1 15:21 nebula-cert
-rw-r--r-- 1 root root 13820988 Jun  1 15:29 nebula-linux-amd64.tar.gz
<< COMMENT
```

3. Copy certification keys (`ca.crt` and `ca.key`) to all nodes that are part of the Nebula / AnyLog network.

The following steps should be done on all machines with AnyLog node(s) being deployed 

4. Update Dockerfile to have association with key certificates - update `/home/username/nebula/` to correct full path of 
nebula directory
```yaml
version: "3"
services:
  anylog-master:
    image: anylogco/anylog-network:${TAG}
    privileged: true
    restart: always
    env_file:
      - anylog_configs.env
      - advance_configs.env
    container_name: ${CONTAINER_NAME}
    stdin_open: true
    tty: true
    network_mode: host
    environment:
      - INIT_TYPE=${INIT_TYPE}
    volumes:
      - anylog-master-anylog:/app/AnyLog-Network/anylog
      - anylog-master-blockchain:/app/AnyLog-Network/blockchain
      - anylog-master-data:/app/AnyLog-Network/data
      - anylog-master-local-scripts:/app/deployment-scripts
      - nebula-configs:${ANYLOG_PATH}/nebula/
      - /home/username/nebula/ca.crt:${ANYLOG_PATH}/nebula/ca.crt
      - /home/username/nebula/ca.key:${ANYLOG_PATH}/nebula/ca.key
volumes:
  anylog-master-anylog:
  anylog-master-blockchain:
  anylog-master-data:
  anylog-master-local-scripts:
  nebula-configs:
```

5. In [advanced_configs.env](https://github.com/AnyLog-co/deployments/blob/main/docker-compose/anylog-master/advance_configs.env), 
update the **NEBULA** section as well as the `OVERLAY_IP` value in **Networking** section
* configurations for a lighthouse node 
```dotenv
#--- Networking ---
...
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=192.168.100.100
...

#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# whether node is type lighthouse
IS_LIGHTHOUSE=true
# Nebula IP address for Lighthouse node
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP="" 
```
* configurations for non-lighthouse node
```dotenv
#--- Networking ---
...
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=192.168.100.101
...

#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula IP address for Lighthouse node
LIGHTHOUSE_IP=192.168.100.100
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=172.105.4.105
```

6. Enable [TUN/TAP driver](https://docs.kernel.org/networking/tuntap.html) to provide packet reception and transmission 
for user space programs. 
```shell
sudo modprobe tun
```

7. Deploy AnyLog 
```shell
bash deployments/run.sh docker master up
```