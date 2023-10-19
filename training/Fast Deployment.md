# Fast Deployment of the Test Network

This document lists the deployment steps to bring a network of 4 nodes (master, query and 2 operators nodes) and a remote CLI.    
A detailed description of every step is available in the [Session II](Session%20II%20(Deployment).md) Deployment document.

## The setup
This deployment will be using 2 physical machines.
* Machine A - deployed with Master, Query, Operator and a remote CLI.
* Machine B - deployed with the second Operator. 

## Clone AnyLog
```shell 
git clone https://github.com/AnyLog-co/deployments  
```

## Register docker credentials 
```shell
bash $HOME/deployments/installations/docker_credentials.sh [DOCKER_ACCESS_CODE]
```

## Deploy the Master node

#### Update the configs

In the folder ```deployments/training/anylog-master``` update the ```anylog_configs.env``` file as follows:
* LICENSE_KEY with the AnyLog License Key (if different than the default).
* NODE_NAME is set to anylog-master
* COMPANY_NAME with your company name.

#### Start the node

```docker-compose up -d```

#### Attach & test

```docker attach --detach-keys=ctrl-d anylog-master``` (and hit the Enter key)

* Test the network by issuing the command: **test network** on the AnyLog CLI (One node - the Master, is identified).

* Copy the Network ID (the IP and Port of the master) - use the command: ```get connections``` to view the IP and Port info.
    This network ID is added to the configuration of the member nodes to make them members of the network associated with this master.  
    Example:
    ```
    AL anylog-master +> get connections
    
    Type      External Address    Internal Address    Bind Address  
    ---------|-------------------|-------------------|-------------|
    TCP      |198.74.50.131:32048|198.74.50.131:32048|0.0.0.0:32048|
    REST     |198.74.50.131:32049|198.74.50.131:32049|0.0.0.0:32049|
    Messaging|Not declared       |Not declared       |Not declared |
    ```
    The Network ID in the example above is identified by TCP/External-Address and is: ```198.74.50.131:32048```.  
    This ID is added to each participating node to make it a member of the same network.

#### Detach

Using the keys: **ctrl+d**

## Deploy the Query node

#### Update the configs

In the folder ```cd deployments/training/anylog-query``` update the ```anylog_configs.env``` file as follows:
* LICENSE_KEY with the AnyLog License Key (if different than the default).
* NODE_NAME is set to anylog-query
* COMPANY_NAME with your company name.
* LEDGER_CONN with the Network ID - the IP and Port of the Master Node (for example: LEDGER_CONN=198.74.50.131:32048).

#### Start the node

```docker-compose up -d```

#### Attach & test

```docker attach --detach-keys=ctrl-d anylog-query``` (and hit the Enter key)

Test the network by issuing the command: **test network** on the AnyLog CLI (Two nodes - a Master and a Query node are identified).

#### Detach

Using the keys: **ctrl+d**

## Deploy the Operator nodes (one node on each physical machine)

In the folder ```cd deployments/training/anylog-operator``` update the ```anylog_configs.env``` file as follows:
* LICENSE_KEY with the AnyLog License Key (if different than the default).
* COMPANY_NAME with your company name.
* LEDGER_CONN with the Network ID - the IP and Port of the Master Node (for example: LEDGER_CONN=198.74.50.131:32048).
* NODE_NAME - currently showing **anylog-operator**, change to be unique (and anylog can be replaced with your company name):
    - for operator 1: **anylog-operator_1**
    - for operator 2: **anylog-operator_2**
* CLUSTER_NAME - currently showing **new-company-cluster**. change to your company name (the example below is 
using anylog for new-company) and a unique prefix like the example below:
    - for operator 1: **anylog-cluster_1**
    - for operator 2: **anylog-cluster_2**
DEFAULT_DBMS - a logical database name for test data. Use the same name on both operators (or use the default name - **test**).    
        
#### Start the node

```docker-compose up -d```

#### Attach & test

```docker attach --detach-keys=ctrl-d anylog-operator```  (and hit the Enter key)

Test the network by issuing the command: **test network** on the AnyLog CLI.  
* With the first Master - Three nodes (a Master, a Query and an Operator node) are identified).
* With the second Master - Four nodes (a Master, a Query and 2 Operators) are identified.

Note: In this training session, the operators are configured to pull data from a 3rd party broker. Issue the command 
```get streaming``` to see the data stream to the node (from the external broker). 

#### Detach

Using the keys: **ctrl+d**

## Example commands and queries on the Query Node

#### View the list of tables

```get virtual tables```

#### View columns in a table

```get columns where dbms = test and table = lightout1 ```

#### Example queries

```shell
run client () sql test format=table "select count(*) from lightout1"
run client () sql test format=table "select timestamp, value from lightout1 limit 20"
```

#### View data distribution (for each table)

```get data nodes```

## Deploy the remote CLI

#### Enter the Remote CLI folder
 ```shell
cd deployments/training/remote-cli
```
#### Start the Remote CLI
```shell
docker-compose up -d
```

#### Open a browser with the following URL
```
http://[The IP of the Node]:31800
```
for example:
```
http://198.74.50.131:31800
```
