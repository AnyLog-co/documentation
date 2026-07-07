---
layout: default
parent: Training
title: Kubernetes
nav_order: 5
---
# Kubernetes

This document demonstrates a deployment of an EdgeLake node as a Kubernetes instance with Minikube and Helm.
The deployment makes EdgeLake scripts persistent (using PersistentVolumeClaim). In a customer deployment, it is recommended 
to predefine the services for each Pod.

* [Requirements](#requirements)
* [Deploying EdgeLake](#deploy-edgelake)
    * [Configuration file](#configuration-file)
    * [deploy_node.sh Explained](#deployment-script-explained)
* [Using Node](#using-node)
* [Network](advanced_kubernetes.md#networking)
  * [Configuring EdgeLake Node](advanced_kubernetes.md#configuring-the-network-services-on-the-edgelake-node)
  * [Peer-to-peer communication](advanced_kubernetes.md#peer-to-peer-communication)
* [Volumes](advanced_kubernetes.md#volumes)
* [Node Policy](advanced_kubernetes.md#sample-node-policy-for-kubernetes)

## Requirements
* <a href="https://kubernetes.io/docs/tasks/tools/" target="_blank">Kubernetes Cluster manager</a> - deploy Minikube with [Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/) 
* <a href="https://helm.sh/" target="_blank">helm</a>
* <a href="https://kubernetes.io/docs/reference/kubectl/" target="_blank">kubectl</a>
* Hardware Requirements - based on <a href="https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin" target="_blank">official documentation</a>

<table>
    <tr>
        <th>Requirements</th>
    </tr>
    <tr>
        <td>2 GB or more RAM</td>
    </tr>
    <tr>
        <td>2 or more CPUs</td>
    </tr>
    <tr>
        <td>Network connectivity between machines in cluster</td>
    </tr>
    <tr>
        <td>Unique hostname / MAC address for every physical node</td>
    </tr>
    <tr>
        <td>Disable swap on machine</td>
    </tr>
</table>

## Deploy EdgeLake
Steps to deploy an EdgeLake container using the <a href="https://github.com/EdgeLake/deployment-k8s/blob/main/deploy_node.sh" target="_blank">deployment script</a>
<ol start="1">
  <li>Clone deployment-k8s
    <pre class="code-frame"><code class="language-shell">git clone https://github.com/EdgeLake/deployment-k8s</code></pre>
  </li>
  <li>Update <a href="#configuration-file">Configurations</a> - located in <a href="https://github.com/EdgeLake/deployment-k8s/tree/main/configurations" target="_blank">deploymnet-k8s//configurations</a></li>
  <br/>
  <li>(Optional) build helm package - The Github repository already has a Helm package for both the node and volume.  
    <pre class="code-frame"><code class="language-shell">bash deploy_node.sh package deployment-k8s/configurations/edgelake_master.yaml</code></pre>
  </li>
  <li>Deploy Kubernetes volume and container for the EdgeLake Node - the deployment script enables port-forwarding with and optional specification of the IP that identifies the proxy. 
If an address is not set, then the port-forwarding is done against localhost (127.0.0.1).
    <pre class="code-frame"><code class="language-shell">bash deploy_node.sh start deployment-k8s/configurations/edgelake_master.yaml [--address={INTERNAL_IP}]</code></pre>
  </li>
  <li>(Optional) Stop deplyment and corresponding proxy process, this will not remove volumes
    <pre class="code-frame"><code class="language-shell">bash deploy_node.sh stop deployment-k8s/configurations/edgelake_master.yaml</code></pre>
  </li>
</ol>


## Configuration file

Since Kubernetes containers use a unique internal IP with each deployment, we recommend setting the machine's internal
IP address as the overlay IP value in the configurations; otherwise a new EdgeLake policy will be declared when the EdgeLake node reboots. 

The configuration is seprated into the 3 parts
<ul>
  <li><code>metadata</code> - Kubernetes information such as component names and network service type (ClusterIP)</li>
  <li><code>image</code> - EdgeLake docker image information</li>
  <li><code>node_configs</code> - Environment variables used by EdgeLake. The environment variables are broken up into relevant sections</li>
</ul>

<b>Sample Configuration file for Operator Node</b>
<pre class="code-frame"><code class="language-yaml">metadata:
  # Kubernetes Instance namespace
  namespace: default
  # hostname for deployment
  hostname: edgelake-operator
  # deployment application name / Name of the edgelake instance
  app_name: edgelake-operator
  service_name: edgelake-operator-service
  # Configuration file mapping name
  configmap_name: edgelake-operator-configmap
  # Allows running Kubernetes remotely. If commented out, code will ignore it
  node_selector: ""
  service_type: ClusterIP

image:
  # Image secret naming
  secret_name: imagepullsecret
  # (Docker Hub) Image Path
  repository: anylogco/edgelake-network
  # Image version
  tag: latest
  # Image pulling policy
  pull_policy: IfNotPresent

node_configs:
  general:
    # Information regarding which edgelake node configurations to enable. By default, even if everything is disabled, edgelake starts TCP and REST connection protocols
    NODE_TYPE: operator
    # Name of the edgelake instance
    NODE_NAME: edgelake-operator
    # Owner of the edgelake instance
    COMPANY_NAME: New Company

  networking:
    # Port address used by edgelake's TCP protocol to communicate with other nodes in the network
    ANYLOG_SERVER_PORT: 32148
    # Port address used by edgelake's REST protocol
    ANYLOG_REST_PORT: 32149
    # Port value to be used as an MQTT broker, or some other third-party broker
    ANYLOG_BROKER_PORT: 32150
    # Internal IP address of the machine the container is running on - if not set, then a unique IP will be used each time
    OVERLAY_IP: ""
    # A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
    TCP_BIND: false
    # A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
    REST_BIND: false
    # A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
    BROKER_BIND: false

  database:
    # Physical database type (sqlite or psql)
    DB_TYPE: sqlite
    # Username for SQL database connection
    DB_USER: ""
    # Password correlated to database user
    DB_PASSWD: ""
    # Database IP address
    DB_IP: 127.0.0.1
    # Database port number
    DB_PORT: 5432
    # Whether to set autocommit data
    AUTOCOMMIT: false
    # Whether to enable NoSQL logical database
    ENABLE_NOSQL: false

  blockchain:
    # TCP connection information for Master Node
    LEDGER_CONN: 127.0.0.1:32048

  operator:
    # Owner of the cluster
    CLUSTER_NAME: new-company-cluster1
    # Logical database name
    DEFAULT_DBMS: new_company

  mqtt:
    # Whether to enable the default MQTT process
    ENABLE_MQTT: false

    # IP address of MQTT broker
    MQTT_BROKER: 139.144.46.246
    # Port associated with MQTT broker
    MQTT_PORT: 1883
    # User associated with MQTT broker
    MQTT_USER: edgelakeuser
    # Password associated with MQTT user
    MQTT_PASSWD: mqtt4edgelake!
    # Whether to enable MQTT logging process
    MQTT_LOG: false

    # Topic to get data for
    MSG_TOPIC: edgelake-demo
    # Logical database name
    MSG_DBMS: new_company
    # Table where to store data
    MSG_TABLE: bring [table]
    # Timestamp column name
    MSG_TIMESTAMP_COLUMN: now
    # Value column name
    MSG_VALUE_COLUMN: bring [value]
    # Column value type
    MSG_VALUE_COLUMN_TYPE: float

  advanced:
    # Whether to automatically run a local (or personalized) script at the end of the process
    DEPLOY_LOCAL_SCRIPT: false
    # Whether to monitor the node or not
    MONITOR_NODES: false</code></pre>

## Deployment Script Explained

The <code>deploy_node.sh</code> script is a tool that allows to easily prepare and deploy a Kubernetes deployment based 
on user-defined configurations. The code has 3 basic options:

<ul>
  <li><i>package</i> - Package both the EdgeLake deployment and volume helm charts
    <pre class="code-frame"><code class="language-shell">helm package edgelake-node
helm package edgelake-node-volume</code></pre>
  </li>

  <li><i>start</i> - Deploy the Helm chart based on user-defined configuration file, then set up Kubernetes port-forwarding. 
The script will wait for the deployment to finish before setting up port-forwarding.
  <ul>
    <li>Install volume
      <pre class="code-frame"><code class="language-shell">helm install ./edgelake-node-volumes-0.0.0.tgz -f ${CONFIG_FILE} --name-template ${APP_NAME}-volume</code></pre>
    </li>
    <li>Install deployment
      <pre class="code-frame"><code class="language-shell">helm install ./edgelake-node-0.0.0.tgz -f ${CONFIG_FILE} --name-template ${APP_NAME}</code></pre>
    </li>
    <li>Declare port forwarding  -  the port(s) to open for port-forwarding depends on whether the port is 
trying to communicate with services outside the Kubernetes network. The deploy_node.sh script will open ports for the EdgeLake services: TCP, 
REST and Broker (if set).
  <pre class="code-frame"><code class="language-shell"># example without a specified IP address  
kubectl port-forward -n ${NAMESPACE} service/${SERVICE_NAME} ${ANYLOG_SERVER_PORT}:${ANYLOG_SERVER_PORT} > /dev/null 2>&1 &
<br>
# example with a specified IP address 
kubectl port-forward -n ${NAMESPACE} service/${SERVICE_NAME} ${ANYLOG_SERVER_PORT}:${ANYLOG_SERVER_PORT} --address=${INTERNAL_IP}  &gt /dev/null 2&gt&1 &</code></pre></li>
    </ul>
  </li>
  <li><i>stop</i> - Based on used-defined configurations, stop Kubernetes instance and kill port-forwarding process. It will not remove the Helm volumes used by Kubernetes. 
  <pre class="code-frame"><code class="language-shee">helm delete ${APP_NAME}
kill -15 `ps -ef | grep port-forward | grep ${ANYLOG_SERVER_PORT} | awk -F " " '{print $2}'`</code></pre></li>
</ul>

To remove a Helm/Kubernetes volume simply run:
<pre class="code-frame"><code class="language-shell">helm delete ${VOLUME_NAME}</code></pre>

## Using Node
<ul>
  <li>Attach to EdgeLake CLI   
<pre class="code-frame"><code class="language-shell"># to detach ctrl-p-q
kubectl attach -it pod/edgeLake-master-deployment-7b4ff75fb7-mnsxf</code></pre></li>
  <li>Attach to the shell interface of the node
<pre class="code-frame"><code class="language-shell"># to detach ctrl-p-q
kubectl attach -it pod/edgeLake-master-deployment-7b4ff75fb7-mnsxf</code></pre></li>
  <li>Sample Insert Data - <a href="https://github.com/EdgeLake/edgelake.github.io/tree/main/docs/examples/python_examples/data" target="_blank">Sample Python Code</a>
<pre class="code-frame"><code class="language-shell">curl -X PUT http://127.0.0.1:32149 \ 
   -H "type: json" -H "dbms: new_company" \
   -H "table: rand_data" \
   -H "mode: streaming" \
   -H "Content-Type: text/plain" \
   -H "User-Agent: AnyLog/1.23" \
   --data-raw "[{\"value\": 50, \"ts\": \"2019-10-14T17:22:13.051101Z\"}, {\"value\": 501, \"ts\": \"2019-10-14T17:22:13.050101Z\"}, {\"value\": 501, \"ts\": \"2019-10-14T17:22:13.050101Z\"}]"</code></pre></li>
  <li>Check Node Status
<pre class="code-frame"><code class="language-shell">curl -X GET http://127.0.0.1:32149</code></pre></li>
  <li>Check data coming in
<pre class="code-frame"><code class="language-shell"># data being processed
curl -X GET http://127.0.0.1:32149  -H "command: get streaming"
# validate data was stored 
curl -X GET http://127.0.0.1:32149  -H "command: get streaming"</code></pre></li>
  <li><a href="../commands/query_data.html">Query</a> — notice the request is running against the query node via REST
<pre class="code-frame"><code class="language-shell">curl -X GET http://127.0.0.1:32349 \
   -H "command: sql new_company select * from rand_data;" 
   -H "User-Agent: AnyLog/1.23"
   -H "destination: network"</code></pre></li>
</ul>