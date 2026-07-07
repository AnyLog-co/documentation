---
layout: default
title: KubeArmor / gRPC
parent: Southbound
nav_order: 5
---
# KubeArmor / gRPC Integrations

gRPC (Google Remote Procedure Calls) is an open-source framework developed by Google. 
It is designed to be efficient, scalable, and interoperable across different programming languages.
gRPC is used in distributed systems, microservices architectures, and client-server applications to enable efficient 
communication between components. Detailed gRPC documentation is available [here](https://grpc.io/docs/what-is-grpc/introduction/#overview).

EdgeLake can connect as a gRPC client to a gRPC Server to receive the data streams. Using EdgeLake policies, streams 
are mapped to a target schema, and the data is hosted on the local EdgeLakee node.

EdgeLake comes pre-configured with the gRPC protocol files for KubeArmor

* [KubeArmor](https://kubernetes.io/docs/setup/)
* [Integration Architecture (with OpenHorizon)](https://wiki.lfedge.org/display/OH/EdgeLake+-+KubeArmor+Integration)

## KubeArmor and EdgeLake

KubeArmor analyzes telemetry data to understand application behavior for container/node forensics. With thousands of 
nodes deployed (using Open Horizon), sending events streams to a centralized node is not a viable option. 

The EdgeLake instances form a decentralized network of nodes that service the distributed edge data as a unified collection 
of data (whereas the physical data remains distributed at the edge).

By sending KubeArmor data into EdgeLake (via *gRPC*), users and applications are able to query the distributed data. 
This approach distributes each query to the edge nodes with relevant data and aggregates the individual replies to form 
a unified and complete result set equivalent to a reply from a cloud based database. A more detailed information on how 
EdgeLake  Operates is available in [Value Proposition article](https://medium.com/anylog-network/anylog-value-proposition-7746f04fd0a3).

Users deploying EdgeLake to manage the KubeArmor's event data are able to extract real time insight from their data, 
enable real-time alerts and monitoring and service the data to analysis and AI applications, all of that without cloud 
contracts and costs.

## Prepare EdgeLake and KubeArmor
<ol start="1">
<li>Setup <a href="https://github.com/EdgeLake/docker-compose" target="_blank">EdgeLake</a> and <a href="https://docs.kubearmor.io/kubearmor/quick-links/deployment_guide">KubeArmor</a></li>
</ol>

### On KubeArmor Side 
<ol start="2"><li>If EdgeLake is not deployed through <i>Kubernetes</i>, then KubeArmor must be accessible through some kind of proxy service.
<pre class="code-frame"><code class="language-shell"># proxy command 
kubectl port-forward --address ${INTERNAL_IP} service/kubearmor 32769:32767 -n kubearmor
</code></pre></li></ol>

### On EdgeLake Side
<ol start="3"><li>Locate the EdgeLake volume for local-scripts
<pre class="code-frame"><code class="language-shell">moshe@anylog-gcp-publisher:~$ docker volume ls 
DRIVER    VOLUME NAME
local     edgelake-operator_edgelake-operator-anylog
local     edgelake-operator_edgelake-operator-blockchain
local     edgelake-operator_edgelake-operator-data
local     edgelake-operator_edgelake-operator-local-scripts
local     minikube
moshe@anylog-gcp-publisher:~$ docker inspect edgelake-operator_edgelake-operator-local-scripts
[
    {
        "CreatedAt": "2024-01-19T23:11:12Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "edgelake-publisher",
            "com.docker.compose.version": "2.17.2",
            "com.docker.compose.volume": "edgelake-publisher-local-scripts"
        },
        "Mountpoint": "/var/snap/docker/common/var-lib-docker/volumes/edgelake-operator_edgelake-operator-local-scripts/_data",
        "Name": "edgelake-operator_edgelake-operator-local-scripts",
        "Options": null,
        "Scope": "local"
    }
]</code></pre></li>
<br>
<li>Locate <i>gRPC file(s)</i>
<pre class="code-frame"><code class="language-shell">moshe@anylog-gcp-publisher:~$ sudo ls -l /var/snap/docker/common/var-lib-docker/volumes/edgelake-operator_edgelake-operator-local-scripts/_data/grpc/
total 20
-rw-r--r-- 1 root root 1576 Jan 19 04:58 README.md
-rw-r--r-- 1 root root  920 Jan 19 04:58 compile.py
-rw-r--r-- 1 root root 5289 Jan 19 04:58 dummy_kube_server.py
drwxr-xr-x 2 root root 4096 Jan 21 01:34 kubearmor
moshe@anylog-gcp-publisher:~$ sudo ls -l /var/snap/docker/common/var-lib-docker/volumes/edgelake-operator_edgelake-operator-local-scripts/_data/grpc/kubearmor
total 48
-rw-r--r-- 1 root root     0 Jan 19 04:58 __init__.py
-rw-r--r-- 1 root root  1083 Jan 19 04:58 deploy_kubearmor_healthcheck.al
-rw-r--r-- 1 root root  1354 Jan 21 01:34 deploy_kubearmor_system.al
-rw-r--r-- 1 root root  1519 Jan 19 04:58 grpc_client.al
-rw-r--r-- 1 root root  2566 Jan 19 04:58 kubearmor.proto
-rw-r--r-- 1 root root  6356 Jan 19 04:58 kubearmor_system_policy.al
</code></pre></li>
<br>
<li>Compile protocol file
<pre class="code-frame"><code class="language-shell">sudo python3 /var/snap/docker/common/var-lib-docker/volumes/anylog-publisher_edgelake-publisher-local-scripts/_data/grpc/compile.py /var/snap/docker/common/var-lib-docker/volumes/anylog-publisher_edgelake-publisher-local-scripts/_data/grpc/kubearmor/kubearmor.proto</code></pre>
</li>
<br>
<li>Update <code class="language-shell">deploy_kubearmor_system.al</code> file
<pre class="code-frame"><code class="language-anylog">#-----------------------------------------------------------------------------------------------------------------------
# Deploy process to accept data from KubeArmor
# Steps:
#   1. Compile proto file
#   2. Set params
#   3. Declare Policy
#   4. gRPC client
#-----------------------------------------------------------------------------------------------------------------------
# process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/deploy_kubearmor_system.al
# Compile proto file
#:compile-proto:
# on error goto compile-error
# compile proto where protocol_file=$EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/kubearmor/kubearmor.proto

# Set Params
:set-params:

grpc_client_ip = kubearmor.kubearmor.svc.cluster.local
grpc_client_port = 32767
grpc_dir = $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/
grpc_proto = kubearmor
grpc_value = (Filter = all)
grpc_limit = 0
set grpc_ingest = true
set grpc_debug = false

grpc_service = LogService
grpc_request = RequestMessage

set alert_flag_1 = false
set alert_level = 0
ingestion_alerts = ''
table_name = bring [Operation]

set default_dbms = kubearmor # <-- update to your default database name 
set company_name = kubearmor # <-- update to your company name 

:run-grpc-client:
grpc_name = kubearmor-message
grpc_function = WatchMessages
grpc_response = Message

process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/kubearmor_message.al
process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/grpc_client.al

grpc_name = kubearmor-alert
grpc_function = WatchAlerts
grpc_response = Alert

process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/kubearmor_alert.al
process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/grpc_client.al

grpc_name = kubearmor-logs
grpc_function = WatchLogs
grpc_response = Logs
process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/kubearmor_log.al
process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/grpc_client.al
</code></pre></li>
</ol>

## Deploy KubeArmor Connector in EdgeLake
<ol start="1">
<li>Attach to EdgeLake operator node
<pre class="code-frame"><code class="language-shell"># ctrl-d to detach 
cd servvice-edgelake 
make attach operator</code></pre></li>
<li>Execute <code>deploy_kubearmor_system.al</code> process
<pre class="code-frame"><code class="language-anylog">process $EDGELAKE_PATH/deployment-scripts/grpc/kubearmor/deploy_kubearmor_system.al</code></pre>
</li>
<li>Validate gRPC is Runnig
<pre class="code-frame"><code class="language-anylog">get grpc client</code></pre>
<b>Expected Output:</b>
<pre class="code-frame"><code class="language-anylog">EL edgelake-operator +> get grpc client 

Name (ID)         Status Connection                                  Proto Name Request Msg    Policy Type Policy Name       Policy ID         Data Msgs Timeouts Error 
-----------------|------|-------------------------------------------|----------|--------------|-----------|-----------------|-----------------|---------|--------|-----|
kubearmor-alert  |Active|kubearmor.kubearmor.svc.cluster.local:32767|kubearmor |RequestMessage|mapping    |kubearmor-alert  |kubearmor-alert  |     2846|    4883|     |
kubearmor-message|Active|kubearmor.kubearmor.svc.cluster.local:32767|kubearmor |RequestMessage|mapping    |kubearmor-message|kubearmor-message|        0|    4891|     |
kubearmor-logs   |Active|kubearmor.kubearmor.svc.cluster.local:32767|kubearmor |RequestMessage|mapping    |kubearmor-logs   |kubearmor-logs   |    87496|    4885|     |
</code></pre>
</li>
<li>Detach from Operator node - <code code="language-shell">ctrl-d</code></li>
</ol> 

## Querying Data 
<ol start="1">
<li>Attach to EdgeLake query node
<pre class="code-frame"><code class="language-shell"># ctrl-d to detach 
cd docker-compose 
make attach EDGELAKE_TYPE=query
</code></pre></li>
<li>Query Data - make sure to set logical database name correctly
<pre class="code-frame"><code class="language-anylog"># Get row count 
run client () sql kubearmor format=table "select count(*) from logs;"
run client () sql kubearmor format=table "select count(*) from alert;"

# Query log table using increment function 
run client () sql kubearmor format=table "select increments(hour, 1, updated_timestamp), result, min(updated_timestamp) as min_ts, max(updated_timestamp) as max_ts, count(*) as row_count from logs where operation='File' group by result ORDER by min_ts;"

# Query alert table using period function
run client () sql kubearmor format=table "select updated_timestamp as timestamp, cluster_name, namespace, pod_name as pod, severity, policy_name as policy, message, action, result, tag, resource, source from alert where period(day, 1, now(), timestamp)"
</code></pre></li>
</ol>

Directions for importing pre-built Grafana Dashboards for KubeArmor can be found as part of our <a href="https://github.com/open-horizon-services/service-edgelake/blob/main/Documentation/Import_Grafana_Dashboards.md" target="_blang">OpenHorizon Deployment</a>