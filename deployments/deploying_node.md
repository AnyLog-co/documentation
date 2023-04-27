# Deploying a Node

The AnyLog instances are using the same code base and differ by the services they provide. 
The services offered by a node are determined by the configuration applied to the node. 
For convenience, we named 4 types of nodes which are configured differently to provide different functionalities
(_Master_, _Operator_, _Query_ and _Publisher_), as-well-as a _Generic_ instance configured with commonly used
services and can be deployed "out-of-the-box" to support many of the edge use cases. 

In the examples below, users define **system variables** by assigning values to keys. These keys  
are referenced in the node configuration process to apply a configuration option, or a configuration value.


## Configuration Based Deployment
AnyLog's [deployment scripts](https://github.com/AnyLog-co/deployments) provides users with a series of questions to assist
with deployment of an AnyLog instance of either _Docker_ or _Kubernetes_. For a _Docker_ instance the deployment script 
updates the correlating `.env` file of the node. 

**Disclaimer**: The deployment scripts do not [deploy physical database](database_configuration.md). Make sure your
non-SQLite database(s) is deployed prior to starting your AnyLog instance.   

### Requirements
**Docker**
* [Docker and docker-compose](https://docs.docker.com/engine/install/)
* Python3
  * [dotenv](https://pypi.org/project/python-dotenv/) - Python3 package utilized in the deployment scripts

**Kubernetes**
* [Kubernetes Orchestrator](https://kubernetes.io/docs/tasks/tools/)  
    * [Helm](https://helm.sh/docs/)
    * Python3
      * [yaml](https://pypi.org/project/PyYAML/) - Python3 package utilized in the deployment scripts

For testing purposes we use and _minikube_ and _microk8s_ IaaS; however, other [IaaS](https://kubernetes.io/docs/tasks/tools/)
should work just as well.   

### Deployment
1. Download [deployment scripts](https://github.com/AnyLog-co/deployments)
```shell
cd $HOME
git clone https://github.com/AnyLog-co/deployments
cd $HOME/deployments/
```

2. Log into AnyLog's Dockerhub - [contact us](mailto:info@anylog.co) if you do not have login credentials

**Docker**
```shell
bash $HOME/deployments/installations/docker_credentials.sh ${YOUR_ANYLOG_DOCKER_CREDENTIALS}
```

**Kubernetes**
```shell
bash $HOME/deployments/installations/kube_credentials.sh ${YOUR_ANYLOG_DOCKER_CREDENTIALS}
```

3. Deploy AnyLog 
```shell
bash $HOME/deployments/deployment_scripts/deploy_node.sh
```

If a user already has a configuration file and does not want to go through the questionnaire, they can utilize the basic
`docker-compose` or `helm` deployment commands.  

**Docker Deployment**
```shell
cd $HOME/deployments/docker-compose/anylog-${NODE_TYPE}

# start a node in detached mode
docker-compose up -d 

# to attach
docker attach --detach-keys=ctrl-d anylog-${NODE_NAME} 
```
**Kubernetes Deployment**
```shell
# install volumes 
helm install $HOME/deployments/helm/packages/anylog-node-volume-1.22.3.tgz \
  --name-template ${NODE_NAME}-volume
  --values $HOME/deployments/helm/sample-configurations/anylog_${NODE_TYPE}.yaml \

# install node 
helm install $HOME/deployments/helm/packages/anylog-node-1.22.3.tgz \
  --name-template ${NODE_NAME}-volume
  --values $HOME/deployments/helm/sample-configurations/anylog_${NODE_TYPE}.yaml \
  
# to attach
kubectel get pod # get pod name 
kubectl attach -it pod/${POD_NAME}

# to detach ctrl-p + ctrl-pq
```

### Sample Questionare 
Below is a sample questionnaire for a _Generic_ node. The node will set the environment variables as 
well as enable the TCP and REST services. Information regarding `Kubernetes Metadata` will not appear when deploying a _Docker_ 
installation of AnyLog. 

```editorconfig
anylog@anylog-builder:~$ bash $HOME/deployments/deployment_scripts/deploy_node.sh 
Node Type [default: rest | options: rest, master, operator, publisher, query, info]: rest
Deployment Type [default: docker | options: docker, kubernetes]: docker
Deploy Existing Configs [y / n]: n
AnyLog Build Version [default: predevelop | options: develop, predevelop, test]: predevelop

Section: General
        License Key:
        Node Name [default: anylog-node]: 
        Company Name [default: New Company]: 
        Location [default: 0.0, 0.0]: 
        Country [default: Unknown]: 
        State [default: Unknown]: 
        City [default: Unknown]: 


Section: Authentication
        Enable Basic REST Authentication [default: false | options: true, false]: 


Section: Networking
        Connect to Networking based on Blockchain Policy [default: false | options: true, false]: true
        Configuration Policy [default: true | options: true, false]: 
        Config Policy Name: 
        Overlay IP: 
        Proxy IP: 
        TCP Port [default: 32548 | range: 30000-32767]: 
        REST Port [default: 32549 | range: 30000-32767]: 
        Local Broker Port [range: 30000-32767]: 
        Bind TCP Connection [default: true | options: true, false]: 
        Bind REST Connection [default: false | options: true, false]: 
        Bind Message Broker Connection [default: false | options: true, false]: 


Section: Database
        Database Type [default: sqlite | options: sqlite, psql]: psql
        Database User: admin
        Database Password: passwd
        Database IP Address [default: 127.0.0.1]: 
        Database Port [default: 5432]: 
        Enable Autocommit [default: false | options: true, false]: 
        Enable System Query Database [default: false | options: true, false]: true
        Set System Query in-memory [default: true | options: true, false]: 
        Enable NoSQL Database [default: false | options: true, false]: true
        Database Type [default: mongo | options: mongo]: 
        Database User: admin
        Database Password: passwd
        Database IP Address [default: 127.0.0.1]: 
        Database Port [default: 27017]: 
        Blobs DBMS [default: true | options: true, false]: 
        Blobs Folder [default: true | options: true, false]: 
        Compress Blobs [default: false | options: true, false]: 
        Reuse Blobs [default: true | options: true, false]: 


Section: Blockchain
        Master Node TCP Connection [default: 127.0.0.1:32548]: 
        Sync Time [default: 30 second | options: second, minute, hour, day]: 
        Blockchain Source [default: master | options: master, blockchain]: 
        Blockchain Destination [default: file | options: file, dbms]: 


Section: Operator
        Cluster Name [default: new-company-cluster]: 
        Database Name [default: test]: 
        Enable HA [default: false | options: true, false]: 
        Enable Partitions [default: false | options: true, false]: 
        Track JSON Files [default: true | options: true, false]: 
        Archive Files [default: true | options: true, false]: 
        Compress Files [default: true | options: true, false]: 
        Operator Threads [default: 1]: 


Section: Publisher
        DB File Location [default: 0]: 
        Table File Location [default: 1]: 
        Compress Files [default: true | options: true, false]: 


Section: MQTT
        Enable MQTT [default: false | options: true, false]: true
        Enable MQTT Logging [default: false | options: true, false]: 
        Broker [default: driver.cloudmqtt.com]: 
        Port [default: 18785]: 
        MQTT User [default: ibglowct]: 
        MQTT Password [default: MSY4e009J7ts]: 
        Topic [default: anylogedgex]: 
        Database Name [default: test]: 
        Table Name [default: rand_data]: 
        Timestamp Column [default: now]: 
        Value Column [default: bring [readings][][value]]: 
        Value type [default: float | options: str, int, float, timestamp, bool]: 


Section: Advanced Settings
        Enable Local Script [default: false | options: true, false]: 
        Write Data Immediate [default: true | options: true, false]: 
        Threshold Time [default: 60 seconds | options: second, minute, hour, day]: 
        Threshold Volume [default: 10KB | options: KB, MB, GB]:

--- Kubernetes Metadata Configurations ---
Section: Metadata
        Namespace [default: default]: 
        Kubernetes pod hostname [default: anylog-node]: 
        App Name [default: anylog-node-app]: 
        Pod Name [default: anylog-node-pod]: 
        Deployment Name [default: anylog-node-deployment]: 
        Service Name [default: anylog-node-service]: 
        Configuration Name [default: anylog-node-configmap]: 
        Node Selector: 
        Replicas [default: 1]: 
Section: Image
        Secret Name [default: imagepullsecret]: 
        Repository [default: anylogco/anylog-network]: 
        Deployment Version [default: predevelop | options: develop, predevelop, test]: 
        Pull Policy [default: IfNotPresent | options: Always, IfNotPresent, Never]: 
Section: Volume
        Enable Volumes [default: true | options: true, false]: 
        --> Volume: anylog_volume
        Name [default: anylog-rest-anylog-data]: 
        Path [default: /app/AnyLog-Network/anylog]: 
        Access Mode [default: ReadWriteOnce | options: ReadWriteOnce, ReadWriteMany, ReadOnlyMany, ReadWriteOncePod]: 
        Storage Size [default: 1Gi]: 
        --> Volume: blockchain_volume
        Name [default: anylog-rest-blockchain-data]: 
        Path [default: /app/AnyLog-Network/blockchain]: 
        Access Mode [default: ReadWriteOnce | options: ReadWriteOnce, ReadWriteMany, ReadOnlyMany, ReadWriteOncePod]: 
        Storage Size [default: 1Gi]: 
        --> Volume: data_volume
        Name [default: anylog-rest-data-data]: 
        Path [default: /app/AnyLog-Network/data]: 
        Access Mode [default: ReadWriteOnce | options: ReadWriteOnce, ReadWriteMany, ReadOnlyMany, ReadWriteOncePod]: 
        Storage Size [default: 1Gi]: 
```
