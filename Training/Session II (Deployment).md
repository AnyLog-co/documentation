# Session II - Deployment of the test network

If you do not have Docker credentials, or an AnyLog license key please contact us at [info@anylog.co](mailto:info@anylog.co) 

## Starting an Empty Node 
An Empty node is a node doesn't contains any preset AnyLog services. 

1. Log into AnyLog Docker Hub
```
docker login -u anyloguser -p ${DOCKER_LOGIN]
```

2. Start an Empty Node
```
docker run -it --detach-keys=ctrl-d \
-e NODE_TYPE=none \
-e LICENSE_KEY=${ANYLOG_LICENSE_KEY} 
--net=host --rm anylogco/anylog-network
```


If for some reason, the License Key doesn't get enabled: 
```
AL > set license where activation_key = !license_key
```

## Sample Commmands

* _Help_ functions 
```
# general help 
help

# view help sections
help index

# list of commands associated with data streaming
help index streaming

# explanation of the command: run kafka consumer
help run kafka consumer
```

* _log_ commands
```
# view activity on the node 
get event log 

# view errors on the node 
get error log 

# for a node running a query, view the status of the query
query status [all]

# for operator and publisher nodes, view whether data is coming in 
get streaming
```

* _Local_ and _Environment_ variables
```
# view all local variables (in the AnyLog dictionary)
get dictionary 

# view Environment variables
get env vars 

# view a specific AnyLog variable  - in this case the TCP port value 
!anylog_server_port

# view a specific Environment variables
$HOME

# declare a new AnyLog variable & view it
abc = 123
!abc
```

* _Network_ Configuration 
```
# View connections 
get connections 

# connect to TCP / REST 
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=true and threads=3>

<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=false and threads=3 and timeout=30>

# validate the TCP connection, the REST connection and the local blockchain structure.
test node 
```

* Database  Configuration 
```
# connect to a logical database 
connect dbms test where  type=sqlite and memory=false 

# if you have PostgreSQL installed: 
connect dbms test where type=psql and ip=127.0.0.1 and port=5432 and user=[USERNAME] and password=[PASSWORD]

# view databases 
get databases
```
## Other Documents
* [Getting Started](../getting%20started.md)
* [Deployment Scripts](../deployments/deploying_node.md)
* [Cheatsheet](../deployments/Support/cheatsheet.md)
* Remote-CLI
  * [Deployment](../deployments/Support/Remote-CLI.md)
  * [Usage](../northbound%20connectors/remote_cli.md) 


