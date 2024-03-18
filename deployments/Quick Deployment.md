## Quick Deployment 

Using the [deployment scripts](https://github.com/AnyLog-co/deployment-scripts), users are able to configure their node 
with their desired configurations. This includes things like specifying port values, naming conventions for policies, 
and even more advanced options like enabling / disabling MQTT and how long to wait with (user) data until it's pushed 
into the database. Since this can be confusing for some, there's the docker image also provides an option to quickly 
deploy more generic nodes, using very limited environment configurations. 

**Other Deployments**: 
* [Training](../training) - Standard training used for explaining how to use AnyLog
* [Configuration Based](../deployments/deploying_node.md) - Deploy AnyLog using configuration file with environment variables
* [Empty Node](deploying_node.md) - Manually deploy an AnyLog node 

## Deployment 
The following provides directions to deploy a network without too much configuration on a single node. If nodes are not
on the same physical machine, make sure to update the `LEDGER_CONN` environment variable when deploying nodes. When 
deploying, users can include other [environment variable](Support/sample_config_file.env), but are not required to.  

Please [contact us](mailto:info@anylog.co) if you do not have access to our Docker hub and/or an active license key. 

1. Log into AnyLog user
```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```

2. Start Master node 
   * if AnyLog nodes are on different machines, view TCP connection information via `get connections` 
```shell
docker run -it --detach-keys=ctrl-d --network host \
  -e LICENSE_KEY=${ANYLOG_LICENSE_KEY} \
  -e NODE_TYPE=master  \
  -v anylog-master-anylog:/app/AnyLog-Network/anylog \
  -v anylog-master-blockchain:/app/AnyLog-Network/blockchain \
  -v anylog-master-data:/app/AnyLog-Network/data \
  -v anylog-master-scripts:/app/deployment-scripts/scripts \
  -v anylog-master-test:/app/deployment-scripts/tests \
--name anylog-master --rm anylogco/anylog-network:latest
```
detach from master node using **ctrl-d** command

3. Start Query Node 
   * if the node is on different machine from the master node, add the following environment variable `-e LEDGER_CONN=${MASTER_NODE_TCP_CONN_INFO}`
```shell
docker run -it --detach-keys=ctrl-d --network host \
  -e LICENSE_KEY=${ANYLOG_LICENSE_KEY} \
  -e NODE_TYPE=query  \
  -v anylog-query-anylog:/app/AnyLog-Network/anylog \
  -v anylog-query-blockchain:/app/AnyLog-Network/blockchain \
  -v anylog-query-data:/app/AnyLog-Network/data \
  -v anylog-query-scripts:/app/deployment-scripts/scripts \
  -v anylog-query-test:/app/deployment-scripts/tests \
--name anylog-query --rm anylogco/anylog-network:latest
```
detach from query node using **ctrl-d** command

4. Start Operator Node 1 - 
   * if the node is on different machine from the master node, add the following environment variable `-e LEDGER_CONN=${MASTER_NODE_TCP_CONN_INFO}`
   * To automatically populate the node with data, enable MQTT using the following environment variable `-e ENABLE_MQTT=true`
```shell
docker run -it --detach-keys=ctrl-d --network host \
  -e LICENSE_KEY=${ANYLOG_LICENSE_KEY} \
  -e NODE_TYPE=operator  \
  -v anylog-operator-anylog:/app/AnyLog-Network/anylog \
  -v anylog-operator-blockchain:/app/AnyLog-Network/blockchain \
  -v anylog-operator-data:/app/AnyLog-Network/data \
  -v anylog-operator-scripts:/app/deployment-scripts/scripts \
  -v anylog-operator-test:/app/deployment-scripts/tests \
--name anylog-operator --rm anylogco/anylog-network:latest
```
detach from operator 1 node using **ctrl-d** command

5. Start Operator Node 2
   * if the node is on different machine from the master node, add the following environment variable `-e LEDGER_CONN=${MASTER_NODE_TCP_CONN_INFO}`
   * To automatically populate the node with data, enable MQTT using the following environment variable `-e ENABLE_MQTT=true`
   * Change node name and cluster name in the environment variables 
   * If both operators are on the same machine (as in this example), make sure the TCP and REST ports are updated 
```shell
docker run -it --detach-keys=ctrl-d --network host \
  -e LICENSE_KEY=${ANYLOG_LICENSE_KEY} \
  -e NODE_TYPE=operator  \
  -e NODE_NAME=operator2 \
  -e CLUSTER_NAME=cluster2 \
  -e ANYLOG_SERVER_PORT=32158 \
  -e ANYLOG_REST_PORT=32159 \
  -v anylog-operator-anylog2:/app/AnyLog-Network/anylog \
  -v anylog-operator-blockchain2:/app/AnyLog-Network/blockchain \
  -v anylog-operator-data2:/app/AnyLog-Network/data \
  -v anylog-operator-scripts2:/app/deployment-scripts/scripts \
  -v anylog-operator-test2:/app/deployment-scripts/tests \
--name anylog-operator2 --rm anylogco/anylog-network:latest
```
detach from operator 2 node using **ctrl-d** command

