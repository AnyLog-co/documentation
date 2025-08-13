# Kubernetes 

This document demonstrate a deployment of an AnyLog node as a Kubernetes instance with Minikube and Helm.
The deployment makes AnyLog scripts persistent (using PersistentVolumeClaim). In a customer deployment, it is recommended 
to predefine the services for each Pod.

* [Requirements](#requirements)
  * [Validate Connectivity](third-party/kubernetes_network_validation)
* [Deploying AnyLog](#deploy-anylog)
  * [`make` Commands](#make-commands)
* [Advanced](#advanced)
  * [Networking](#networking)
  * [Volumes](#volumes)

--- 

## Requirements
* [Kubernetes Cluster manager](https://kubernetes.io/docs/tasks/tools/) - deploy Minikube with [Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/) 
* [helm](https://helm.sh/)
* [kubectl](https://kubernetes.io/docs/reference/kubectl/)
* Hardware Requirements - based on [official documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin)


|                                               |                                                               Requirements                                                               | 
|:---------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------:| 
|                      RAM                      |                                                               2 GB or more                                                               | 
|                      CPU                      |                                                                2 or more                                                                 |
|                  Networking                   |             Network connectivity between machines in cluster<br/><br/>Unique hostname / MAC address for every physical node              | 
| Other | <a href="https://www.geeksforgeeks.org/linux-unix/how-to-permanently-disable-swap-in-linux/" target="_blank">Disable swap on machine</a> |  


When using multiple nodes on different machines, validate connectivity between machines in the network. Directions for 
testing Kubernetes can be found [here](third-party/kubernetes_network_validation)

---

## Deploying AnyLog 
1. Request a trial license via <a href="https://anylog.network/download" target="_blank">Download Page</a>

2. Clone <a href="https://github.com/AnyLog-co/deployment-k8s" target="_blank">docker-compose</a> repository
```shell
cd $HOME
git clone https://github.com/AnyLog-co/deployment-k8s 
```

3. Log into AnyLog docker repository
```shell
cd $HOME/deployment-k8s
bash secret.sh [DOCKER_LOGIN]
```

4. Update Configurations - Sample configurations file can be found in [Quick Start](quick_start.md#configuration)

> Kubernetes uses a YAML based configuration file, as opposed to dotenv configuration file. However, the configurations 
(from AnyLog/EdgeLake) perspective are the same

> In the configurations, the value of `LEDGER_CONN` needs to be the  TCP connection information that can reach the master node.
 

|                                                  Node Type                                                  |                                                	Role                                                 | |                                                                                                                               | 
|:-----------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:| :---: |:-----------------------------------------------------------------------------------------------------------------------------:|  
|                                                  Operator                                                   |                          	A node that hosts the data and satisfies queries.                          | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/base_configs.env) |   [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/advance_configs.env)    | 
|                               Query	|                              A node that orchestrates a query process.                               | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/query-configs/base_configs.env) |   [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/query-configs/advance_configs.env)    |
| Master	| A node that hosts the metadata on a ledger and serves the metadata to the peer nodes in the network. | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/base_configs.env) |    [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/advance_configs.env)     |
| Publisher	| A node that receives data from a data source (i.e. devices, applications) and distributes the data to Operators. | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/publisher-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/publisher-configs/advance_configs.env)  |

5. Deploy Agent - this is a 2 step process
    * Package for _Helm_ deployment
    * Deploy agent
```shell
make package ANYLOG_TYPE=[NODE_TYPE]
make up ANYLOG_TYPE=[NODE_TYPE]
```

6. Using Node
* Attach to AnyLog CLI   
```shell
# to detach ctrl-p-q
make attach ANYLOG_TYPE=[NODE_TYPE]
```

* Attach to the shell interface of the node  
```shell
# to detach ctrl-p-q
make exec ANYLOG_TYPE=[NODE_TYPE]
```

### `make` Commands

The Kubernetes repository uses the `make` functionality in order to remove the need for users to manually execute 
`docker` related commands. This allows for ease of use and consistency.

```shell
Usage: make [target] [VARIABLE=value]

Available targets:
  login                 log into the docker hub for AnyLog - use `ANYLOG_TYPE` as the placeholder for password
  build                 pull image from the docker hub repository
  dry-run               create docker-compose.yaml file based on the .env configuration file(s)
  up                    start AnyLog instance
  down                  Stop AnyLog instance
  clean-vols            Stop AnyLog instance and remove associated volumes
  clean                 Stop AnyLog instance and remove associated volumes & image
  attach                Attach to docker / podman container (use ctrl-d to detach)
  exec                  Attach to the shell executable for the container
  logs                  View container logs
  test-node             Test a node via REST interface
  test-network          Test the network via REST interface
  check-vars            Show all environment variable values

Common variables you can override:
  IS_MANUAL           Use manual deployment (true/false) - required to overwrite
  ANYLOG_TYPE         Type of node to deploy (e.g., master, operator)
  TAG                 Docker image tag to use
  NODE_NAME           Custom name for the container
  CLUSTER_NAME           Cluster Operator node is associted with
  ANYLOG_SERVER_PORT  Port for server communication
  ANYLOG_REST_PORT    Port for REST API
  ANYLOG_BROKER_PORT  Optional broker port
  LEDGER_CONN         Master node IP and port
  LICENSE_KEY         AnyLog License Key
  TEST_CONN           REST connection information for testing network connectivity
```

--- 



---

## Advanced

### Networking

AnyLog uses [dynamic ClusterIP](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/) as it's preferred setup. This means a unique IP address is automatically assigned 
to the services as they are created and ensures load balancing across the pods in the service.

#### Configuring the network services on the AnyLog node

Since dynamic ClusterIP generates a new IP whenever a pod is deployed, this causes a issue with AnyLog's metadata 
(hosted in a blockchain or a master node) as each new IP will generate a new policy.  
To resolve this issue, and avoid policy updates, specify the host's internal IP as the `OVERLAY_IP` value. 

The following chart summarizes the setup:

|   Connection Type    | External IP | Internal IP |    Config Command    | 
|:--------------------:| :---: | :---: |:--------------------:| 
|         TCP          | External IP | Overlay IP |   `run tcp server`   | 
|         REST         | External IP | Overlay IP |   `run REST server`  |
| Message Broker (TCP) | External IP | Overlay IP | `run message broker` |

Additional information on the network configuration are in the [networking section](https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md).

#### Enable P2P messaging between the AnyLog Nodes 

The second part is in AnyLog's networking configuration is the need for nodes to communicate between one another; to 
accomplish this recommend using [port-forwarding](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/).

The process for port-forwarding is configured to run automatically.

> **Note**: When using Kubernetes, makes sure ports are open and accessible across your network.   

#### Sample Node Policy for Kubernetes

The following provides a basic example of both the configuration policy, as-well-as a (master) node policy.

Values in the configuration policy are relatively set, that way when a deployment is restarted a new policy will not be declared for the node due to the changing virtual IP. As for the local IP in the (master) node policy, we assume the service name will not change.

The sample JSON for (master) node policy is set to have communication between AnyLog nodes to be set to binding. When the communication is set to not-binding, the external IP (73.222.38.13) will be set to ip key in the policy, and the Kubernetes service IP (anylog-master-service) will be set to local_ip.
```json
{"config" : {
  "name" : "master-configs",
  "company" : "New Company",
  "port" : "!anylog_server_port.int",
  "external_ip" : "!external_ip",
  "ip" : "!ip",
  "rest_port" : "!anylog_rest_port.int"
}},
{"master" : {
  "name" : "anylog-master",
  "company" : "New Company",
  "hostname" : "anylog-master-pod", 
  "loc" : "0.0, 0.0",
  "country" : "Unknown",
  "state" : "Unknown",
  "city" : "Unknown",
  "port" : 32048,
  "external_ip" : "73.222.38.13",
  "ip" : "anylog-master-service",
  "proxy_ip" : "10.0.0.183",
}}
```

### Volumes
The base deployment has the same general volumes as a docker deployment, and uses [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) - _data_, 
_blockchain_, _anylog_ and _local-scripts (deployments)_.

While _data_, _blockchain_ and _anylog_ are autogenerated and populated, _local-scripts_ gets downloaded as part of the 
container image. Therefore, we utilize an `if/else` process to make this data persistent. 

At deployment, a copy the deployment-scripts is stored persistently after the associated pod is initialized. 

Once a node is up and running, users can change content in _local-scripts_ using `kubectl exec ${POD_NAME} -- /bin/bash`.

Volumes are deployed automatically as part of [deploy_node.sh](deploy_node.sh), and remain persistent as long as PersistentVolumeClaims
are not removed. 


#### Docker versus Kubernetes Volumes 
Docker volumes are a set of directories that seats on the physical machine and are associated with docker instance(s). 
Kubernetes' volumes, are more of an abstract idea as persistent data can be stored either on the machine or cloud (ex. AWS S3).

AnyLog "requires" storing certain content generated throughout the usage (locally) in order to have a backup for when a 
node (physically) resets, or when migrating data from one machine to another. These include:

* `anylog` directory - which contains authentication keys
* `blockchain` directory - which contains a copy of the blockchain (as JSON file)
* `data` directory - which contains data coming in, as well as the files SQLite database(s) [if created].
* `local-scripts` directory - which contains AnyLog scripts used to configure and deploy an AnyLog / EdgeLake agent. 

#### Personalized Script on Kubernetes
1. Access the Kubernetes deployment bash interface
```shell
exec -it pod/${DEPLOYMENT_POD_NAME} bash
```

2. `cd` into scripts directory - this is the !loca_scripts variable in AnyLog
```shell
cd AnyLog-Network/scripts/
```

3. Either create a new script, or utilize the existing local_script.al file to write your personalized script. When 
setting the Enable Local Script configuration to **true**, the default deployment process will automatically run 
`local_script.al` when starting.
```shell
# install - apt-get -y install vim
vim deployment_scripts/local_scripts.al 
```

4. Once the personalized script has been created, detach from the bash interface and reattach to the AnyLog console
```shell
# detach: ctrl-p +ctrl-pq 
kubectl attach -it pod/${DEPLOYMENT_POD_NAME}
```

5. Once the personalized script has been created, you can manually run it by executing process command.
```shell
AL anylog-node > process !local_scripts/deployment_scripts/local_script.al
```

