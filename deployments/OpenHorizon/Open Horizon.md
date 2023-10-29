# Open Horizon 

Open Horizon is a platform for managing the service software lifecycle of containerized workloads and related machine 
learning assets. It enables autonomous management of applications deployed to distributed web scale fleets of edge 
computing nodes and devices without requiring on-premise administrators.

Open Horizon can be used to easily manage and deploy AnyLog node(s) through their interface.
* [Open Horizon Website](https://www.lfedge.org/projects/openhorizon/)
* [IBM Documentation for Open Horizon](https://developer.ibm.com/components/open-horizon/)
* [Open Source Documentation](https://open-horizon.github.io/)
* [AnyLog Documentation](https://github.com/AnyLog-co/documentation)
* [AnyLog Website](https://anylog.co)

## Requirements 
* A physical / virtual machine for each node, as OpenHorizon is unable to deploy more than 1 instance per node 
* [Machine requirements](https://www.ibm.com/docs/en/eam/4.0?topic=devices-preparing-edge-devicehttps://www.ibm.com/docs/en/eam/4.0?topic=devices-preparing-edge-device)
**For 64-bit Intel or AMD device or virtual machine:**
* 64-bit Intel or AMD device or virtual machine
* An internet connection for your device (wired or wifi)

**For Linux on ARM (32-bit):**
* Hardware requirements - Raspberry Pi 3A+, 3B, 3B+, or 4 (preferred), but also supports  A+, B+, 2B, Zero-W, or Zero-WH
* MicroSD flash card (32 GB preferred)
* An Internet connection for your device (wired or wifi). Note: Some devices can require extra hardware for supporting wifi.

## Associating Machine to Open Horizon
The following steps will associate a new machine with the Open Horizon management platform. The process will complete the 
following:  
* [Create an API key](https://www.ibm.com/docs/en/eam/4.3?topic=installation-creating-your-api-key) 
* [Install Horizon CLI](https://www.ibm.com/docs/en/eam/4.1?topic=cli-installing-hzn) 
* [Install Docker](https://docs.docker.com/engine/install/) 
* Validate Open Horizon is working by deploying an _Hello World_ package

1. On the node Update / Upgrade Node
```shell
for CMD in update upgrade ; do sudo apt-get -y ${CMD} ; done
```

2. Create an Open Horizon [API Key](https://www.ibm.com/docs/en/eam/4.3?topic=installation-creating-your-api-key)

3. Update Environment variables
   * In `~/.bashrc` (or `~/.profile` for Alpine) add the following variables
```shell
export HZN_ORG_ID=<COMPANY_NAME> 
export HZN_EXCHANGE_USER_AUTH="iamapikey:<API_KEY>"
export HZN_EXCHANGE_URL=<HZN_EXCHANGE_URL>
export HZN_FSS_CSSURL=<HZN_FSS_CSSURL> 
```
   * Set Environment variables
```shell
# For non-Alpine operating systems 
source ~/.bashrc 

# For Alpine operating systems 
source ~/.profile 
```

4. Install agent and provide admin privileges
```shell
curl -u "${HZN_ORG_ID}/${HZN_EXCHANGE_USER_AUTH}" -k -o agent-install.sh ${HZN_FSS_CSSURL}/api/v1/objects/IBM/agent_files/agent-install.sh/data

chmod +x agent-install.sh

sudo -s -E ./agent-install.sh -i 'css:' -p IBM/pattern-ibm.helloworld -w '*' -T 120
```

5. Validate helloworld sample edge service is running
```shell
hzn eventlog list -f

<<COMMENT  
"2022-06-13 21:27:13:   Workload service containers for IBM/ibm.helloworld are up and running."
<<COMMENT
```

To unregister an edge service: 
```shell
hzn unregister -f 
```

6. Docker is already installed via HZN, however needs permissions to use not as root
```shell
USER=`whoami` 
sudo groupadd docker 
sudo usermod -aG docker ${USER} 
newgrp docker
```

At the end of the process, OpenHorizon should show a new active node
![OpenHorizon_node_state.png](imgs%2FOpenHorizon_node_state.png)

## Associate AnyLog Deployment with OpenHorizon

@Troy - needs to explain how he associated AnyLog with OpenHorizon  

## Create AnyLog node as a Service on Open Horizon
The following provides directions for deploying an AnyLog Operator & Query via OpenHorizon. 

IBM has deployed a _Master_ node which will be used against `132.177.125.232:32048` (REST communication - `132.177.125.232:32049`). 

1. via [AnyLog Downloads](https://anylog.co/download-anylog) request access to our _Docker_ repository a 3-month license

2. Update `service.definition.json` configuration file  ([Operator Node](deployments/operator/service.definition.json) | [Query Node](deployments/query/service.definition.json)) with the following: 
* License Key 
* Node Name (optional)
* Company Name 
* For Operator Node - Cluster Name (optional)
* For Operator Node - Default DBMS (optional)
* If you're deploying your own Master node, make sure to update `LEDGER_CONN` value in other node configurations 

3. Deploy Node - Note, `hzn` is not able to deploy more than a single instance on a given machine 
```shell
# Operator Node 
cd deployments/operator
hzn register --pattern anylog-node --policy privileged_node_policy.json

# Query Node 
cd deployments/query
hzn register --pattern anylog-node --policy privileged_node_policy.json
```

4. Validate node is running  
      