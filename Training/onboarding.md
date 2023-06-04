# Onboarding Training

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

## Review events 
    Multiple logs that track events - logs examples: event log, error log, rest log, query log (needs to be enabled).
  
     Examples:
    ```anylog 
    get event log
    get error log
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
  
## Connecting to a network
    
    3 types of connections:  
    - TCP - to communicate between nodes which are members of the network.
    - REST - to communicate between 3rd parties apps to a node in the network (examples: the Remote CLI, Grafana).
    - Messaging broker - push data from a data source.
    
    View existing connections:
     ```anylog 
    get connections
  
    run tcp server where internal_ip = !ip and internal_port = 20048 and external_ip = !external_ip and external_port = 20048 and bind = false and threads = 6
    run rest server where internal_ip = !ip and internal_port = 20049 and external_ip = !external_ip and external_port = 20049 and bind = false

    get connections
    ```   
  
    Disable authentication:
    ```anylog 
    set authentication off
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

## The remote CLI:
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
    and [Blockchain Commands](../blockchain%20commands.md#blockchain-commands)
  
    If the file was retrieved using copy (vs. sync), restart he node or call reload:
    ```anylog 
    blockchain reload metadata
    ```   
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

    Use the TCP connection to communicate with peers 
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
    - [Monitoring Calls](..r/monitoring%20calls.md#monitoring-calls-from-external-applications)


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
  
* Data setup:
      Examples: 
     ```anylog 
    get virtual tables
    get tables where dbms = litsanleandro
    get columns where table = ping_sensor and dbms = litsanleandro
    
    get data nodes

    ```
  
* Data Query 
      
     Details are in the [query section](../queries.md).
     Examples: 
     ```anylog 
    run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor WHERE timestamp > NOW() - 1 day limit 100"
    run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
    
    query status
    
    run client () sql edgex format=table "select increments(minute, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value,  count(*) as row_count from rand_data where timestamp >= NOW() - 1 hour;"
    
    run client () sql edgex format=table "select timestamp, value FROM rand_data WHERE period(minute, 5, NOW(), timestamp) ORDER BY timestamp"
    ```
  
    