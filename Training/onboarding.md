# Onboarding Training

## Onboarding demo commands

The basic AnyLog commands demonstrated in the Onboarding session:

* Help commands - see details in [the help command section](#../getting%20started.md#the-help-command).  
    Examples:
    ```anylog 
    help
    help index
    help index streaming
    help run kafka consumer
    ``` 

* Review events - 
    Multiple logs that track events - logs examples: event log, error log, rest log, query log (needs to be enabled).
  
     Examples:
    ```anylog 
    get event log
    get error log
    ```   
  
* The local dictionary - maps local values (like paths names and IPs) to unified names that can be shared across nodes.
  
    Details are in [the local dictionary section](#../dictionary.md#the-local-dictionary).

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
    Details are in [the local directory structure](#../getting%20started.md#local-directory-structure).
  
* Connecting to a network
    
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
  
* Connecting to a DBMS
    Supported databases: PostgreSQL for larger nodes and SQLite for smaller nodes or data in RAM.

    2 system databases:    
        - system_query - orchestrate query results
        - almgm - tracks data ingestion and Manage HA
  
    Connect to a dbms:
    ```anylog 
    connect dbms system_query where type = sqlite and memory = true # Used for local processing
    get databases
    ```   

* Commands can be issued on the remote CLI:

    ```anylog 
    get status
    get dictionary
    get databases
    ```   
