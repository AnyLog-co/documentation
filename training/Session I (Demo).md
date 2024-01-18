# Session I - The Basic Guided Tour

Prerequisite: See details [here](prerequisite.md).

# Basic AnyLog commands

The basic AnyLog commands demonstrated in the Onboarding session:

## Help commands 
See details in [the help command section](../getting%20started.md#the-help-command).  
Examples:
```anylog 
help
help index
help index streaming
help run kafka consumer
``` 

## The logged events
Multiple logs that track events - logs examples: event log, error log, rest log, query log (needs to be enabled).

 Examples:
```anylog 
get event log
get error log
```   

## The node name
The name on the CLI prompt can be set by the user to identify the node when multiple CLIs are used.
```anylog 
node_name = generic
```   
The assignment above makes the CLI prompt appear as:
```
AL generic > 
```   
  
## The local dictionary
The local dictionary maps local values (like paths names and IPs) to unified names that can be shared across nodes.

Details are in [the local dictionary section](../dictionary.md#the-local-dictionary).

 Examples:
```anylog 
get dictionary
abc = 123
!abc

!blockchain_file

get env var
$HOME
```   

Use the local dictionary to see the local folders' setup:

```anylog 
get dictionary _dir
```   
Details are in [the local directory structure](../getting%20started.md#local-directory-structure).
  
## The communication services
Each node can offer 3 types of communication services:  

| Service Name   | Service Type |
| ------------- | ------------- |
| TCP  | A service allowing the node to send and receive messages from peer nodes using the AnyLog Network Protocol |
| REST  | A service allowing the node communicate with 3rd parties applications and data sources using REST |
| Messaging  | A message broker service allowing data sources and 3rd parties applications to publish data on the node |

Enable the TCP and REST services and view existing connections:
 ```anylog 
get connections   # command returns no connection

run tcp server where internal_ip = !ip and internal_port = 20048 and external_ip = !external_ip and external_port = 20048 and bind = false and threads = 6
run rest server where internal_ip = !ip and internal_port = 20049 and external_ip = !external_ip and external_port = 20049 and bind = false

get connections     # command returns the details of each communication service
```   

Disable authentication:
```anylog 
set authentication off      # The training ignors authentication of users, nodes and their permissions
```   

Enable message queue:
  ```anylog 
set echo queue on

echo this is a test message
get echo queue
```  
  
## Connecting to a DBMS
Supported databases: PostgreSQL for larger nodes and SQLite for smaller nodes or data in RAM.

2 system databases:    
    - system_query - orchestrate query results
    - almgm - tracks data ingestion and Manage HA

Connect to a dbms:
```anylog 
connect dbms system_query where type = sqlite and memory = true # Used for local processing
get databases
```   

## The remote CLI (Demonstrating 3rd party application interacting with the network):
Connection via the REST protocol.  
Most commands can be issued on the Remote CLI.    
Examples:
```anylog 
get status
get dictionary
get databases
```   

## The Metadata
Details are available in [Managing Metadata](../metadata%20management.md#managing-metadata)
and [Blockchain Commands](../blockchain%20commands.md#blockchain-commands).

Example blockchain commands:
```anylog 
blockchain get *
blockchain get operator

blockchain get operator bring.table [operator][name] [operator][city] [operator][ip]  [operator][port] 
blockchain get operator where [city] = toronto  bring.table [operator][name] [operator][city] [operator][ip]  [operator][port] 

blockchain get operator where [city] = toronto  bring [operator][ip] : [operator][port] separator = ,

blockchain get operator where [city] = toronto  bring.ip_port
```   

## Execute commands on a peer node
Use the TCP connection to communicate with peers.  
- With a single peer:   run client ip:port
- With multiple peers:  run client (ip:port, ip:port, ip:port ...)  
 Examples: 
 ```anylog 
run client 23.239.12.151:32348 get status
run client 23.239.12.151:32348 get disk usage .
run client 23.239.12.151:32348 get cpu usage
```   

Copy the metadata from a peer node - the correct way to do it is to sync with the metadata
```anylog 
run client 23.239.12.151:32348 file get !!blockchain_file !blockchain_file
```
  
## Monitoring commands:
Additional info is in the following sections:  
- [Monitoring nodes](../monitoring%20nodes.md#monitoring-nodes)
- [Alerts and Monitoring](../alerts%20and%20monitoring.md#alerts-and-monitoring)
- [Monitoring Data](../monitoring%20data.md#monitoring-data)
- [Monitoring Calls](../monitoring%20calls.md#monitoring-calls-from-external-applications)


Examples: 
 ```anylog 
run client (blockchain get operator where [city] = toronto  bring.ip_port) get status

run client (blockchain get operator where [city] = toronto  bring.ip_port) get disk usage .

destination = blockchain get operator where [city] = toronto  bring.ip_port

!destination

run client (!destination) get status
run client (!destination) get disk usage .
run client (!destination) get memory info

run client (!destination) get processes

run client (!destination) get databases

help continuous
continuous cpu  
```
  
## Data setup:
  Examples: 
 ```anylog 
get virtual tables
get tables where dbms = litsanleandro
get columns where table = ping_sensor and dbms = litsanleandro

get data nodes

```
  
## Data Query 
Details are in the [query section](../queries.md).

 Examples: 
 ```anylog 
run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor WHERE timestamp > NOW() - 1 day limit 100"
run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"

query status

run client () sql edgex format=table "select increments(minute, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value,  count(*) as row_count from rand_data where timestamp >= NOW() - 1 hour;"

run client () sql edgex format=table "select timestamp, value FROM rand_data WHERE period(minute, 5, NOW(), timestamp) ORDER BY timestamp"
```

