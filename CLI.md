# AnyLog CLI

Each AnyLog / EdgeLake agent includes a built-in Command Line Interface (CLI), enabling users to interact with the system 
directly through a terminal command prompt. This text-based interface supports a wide range of commands, allowing users 
to execute operations on the local node or communicate with peer nodes in the network. Through the CLI, users can manage 
configurations, query data, monitor activity, and control node behavior efficiently without the need for a graphical 
interface.

* [Introduction to The CLI](#introduction-to-the-cli)
* [`help`, `dictionary` and Other Basic Commands](#help-dictionary-and-other-basic-commands)
  * [`help` command](#help-command)
  * [`get` command](#get-command)
  * [`dictionary` command](#dictionary-command)
  * [`print` command](#print-command)
  * [`echo` Command](#echo-command)
* [Executing Scripts with the CLI](#executing-scripts-with-the-cli)
  * [Setting & Using Variables](#setting--using-variables)
  * [Running Scripts](#running-scripts)

--- 

## Introduction to the CLI

When a node starts, it provides the AnyLog Command Line Interface (AnyLog CLI) 
```anylog 
AL >
```

Users can then change the name of the agent using the command `set node name`.  The node name extends the CLI prompt 
name.
```anylog
AL >  set node name Operator_3
AL Operator_3 >
```

`AL` stands for _AnyLog_, and **Operator_3** is the assigned name of the agent. 
> When using EdgeLake, the CLI would look like this: `EL Operator_3 >`

--- 

## `help`, `dictionary` and Other Basic Commands

### `help` Command

Due to our vast amount of options and commands, AnyLog / EdgeLake has a built-in `help` function to help users better 
understand what different commands do and how / when to use them.

* Getting help based on a key word would provide a list of options to be used with said key word - for example `help run`
```anylog
AL Operator_3 > help run
    Maybe: etherip struct
    Maybe: json file struct
    Maybe: msg rules
    Maybe: opcua struct
    Maybe: msg rule
    Maybe: run blobs archiver where blobs_dir = [data directory location] and archive_dir = [archive directory location] and dbms = [true/false] and file = [true/false] and compress = [true/false]
    Maybe: run blockchain sync [options]
    Maybe: run client (IPs and Ports) [AnyLog command]
    Maybe: run data consumer where start_date = [date] and end_date = [date] and mode = [mode of operation]
    Maybe: run data distributor where distr_dir = [data directory location] and archive_dir = [archive directory location]
    Maybe: run grpc client where name = [unique name] and ip = [IP] and port = [port] and policy = [policy id]
    Maybe: run kafka consumer where ip = [ip] and port = [port]] and reset = [latest/earliest] and topic = [topic and mapping instructions]
    Maybe: run message broker where external_ip = [ip] and external_port = [port] and internal_ip = [local_ip] and internal_port = [local_port] and bind = [true/false] and threads = [threads count]
    Maybe: run msg client where broker = [url] and port = [port] and user = [user] and password = [password] and topic = (name = [topic name] and dbms = [dbms name] and table = [table name] and [participating columns info])
    Maybe: run opcua client where url = [connect string] and frequency = [frequency] and dbms = [dbms name] and table = [table name] and node = [node id]]
    Maybe: run operator where [option] = [value] and [option] = [value] ...
    Maybe: run plc client where type = [connector type] and url = [connect string] and frequency = [frequency] and dbms = [dbms name] and table = [table name] and node = [node id]]
    Maybe: run publisher [options]
    Maybe: run rest server where external_ip = [external_ip ip] and external_port = [external port] and internal_ip = [internal ip] and internal_port = [internal port] and timeout = [timeout] and ssl = [true/false] and bind = [true/false]
    Maybe: run scheduled pull where name = [unique name] and type = [log type] and source = [localhost or IP] and frequency = [in seconds] and dbms = [dbms name] and table = [table name]
    Maybe: run scheduler
    Maybe: run smtp client where host = [host name] and port = [port] and email = [email address] and password = [email password] and ssl = [true/false]
    Maybe: run streamer
    Maybe: run tcp server where external_ip = [ip] and external_port = [port] and internal_ip = [local_ip] and internal_port = [local_port] and bind = [true/false] and threads = [threads count]
```

* Commands are also grouped to different indexes. This allows users dealing with a specific type of issue, such as security, 
more easily locate the relevant commands

**List of Index Options**:
```anylog
AL Operator_3 > help index 
    aggregations
    api
    background processes
    blockchain
    cli
    config
    configuration
    control
    data
    dbms
    debug
    enterprise
    file
    frequency
    help
    high availability
    ingestion
    internal
    json
    log
    metadata
    monitor
    network
    node info
    profile
    profiling
    query
    schedule
    script
    secure network
    streaming
    test suite
    unstructured data
```

**Specific commands related to network security**: 
```anylog 
AL Operator_3 > help index secure network
secure network
     get authentication
     get encryption
     get member permissions
     get node id
     get permissions
     get private
     get public
     get signatory
     get users
     id add user
     id authenticate
     id create keys
     id create keys for node
     id decrypt
     id encrypt
     id generate certificate authority
     id generate certificate request
     id remove user
     id sign
     id sign certificate request
     id update user password
     id validate
     reset signatory
     set authentication
     set encryption
     set local password
     set node authentication
     set private password
     set signatory
     set user authentication
```

* Ofcourse, assuming the user knows which command they want to work with, but doesn't remember how to use it or for what, 
the `help` function helps with that as well. 
```anylog 
AL Operator_3 > help blockchain get 
Usage:
        blockchain get [policy type] [where] [attribute name value pairs] [bring] [bring command variables]
Explanation:
        Get the policies or information from the policies that satisfy the search criteria.
Examples:
        blockchain get *
        blockchain get operator where dbms = lsl_demo
        blockchain get cluster where table[dbms] = purpleair and table[name] = air_data bring [cluster][id] separator = ,
        blockchain get operator bring.table [*] [*][name] [*][ip] [*][port]
        blockchain get * bring.table.unique [*]
Index:
        ['blockchain']
Link: https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#query-policies
Link: https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md
```

### `get` Command
`get` is a prefix-command that provides information on hardware state, (service) status, files, resources and security 
of the AnyLog / EdgeLake agent.

#### Basic `get` Commands
| Option  | Information provided |
|:-------:| :---: | 
| [get node name](#get-node-name)                                                                                                       | Return the name assigned to the node including the IP and Port identifying the node.                                                                                                                          |
| [get event log](logging%20events.md#the-event-log)                                                                                    | Records the Last commands processed by the node.                                                                                                                                                              | 
| [get error log](logging%20events.md#the-error-log)                                                                                    | Records the last commands that returned an error. Adding a list of keywords narrows the output to error events containing the keywords.                                                                       |
| [get file log](#get-logged-instances)                                                                                                 | Records the last data files processed by the node.                                                                                                                                                            |
| [get rest log](#get-logged-instances)                                                                                                 | Records the REST calls returning an error. Can record all REST calls by setting "set rest log on"                                                                                                             |
| [get query log](logging%20events.md#the-query-log)                                                                                    | The last queries processed by the node. Enable this log using the ***set query log*** command                                                                                                                 |
| [get processes](®#the-get-processes-command)                                                                                          | The list of background processes. More details are available in [background processes](background%20processes.md).                                                                                            |
| get members status                                                                                                                    | Get status of members nodes that are messaged by this node.                                                                                                                                                   |
| get synchronizer                                                                                                                      | Information on the blockchain synchronize process.                                                                                                                                                            |
| [get operator](monitoring%20calls.md#get-operator)                                                                                    | Information on the Operator processes.                                                                                                                                                                        |
| [get blobs archiver](background%20processes.md#the-blobs-archiver)                                                                    | Information on the Blobs Archiving processes.                                                                                                                                                                 |
| get publisher                                                                                                                         | Information on the Publisher processes.                                                                                                                                                                       |
| get distributor                                                                                                                       | With HA enabled, information on the distributions of source files to cluster members.                                                                                                                         |
| get consumer                                                                                                                          | With HA enabled, information on pulling source files from cluster members.                                                                                                                                    |
| [get streaming](monitoring%20calls.md#get-streaming)                                                                                  | Information on streaming data from REST and MQTT calls.                                                                                                                                                       |
| get cluster info                                                                                                                      | Information on the cluster supported by the node including Cluster ID, Member ID and Operators supporting the cluster.                                                                                        |
| get tsd info [table name]                                                                                                             | Information on the synchronization status between the cluster members.                                                                                                                                        |
| [get rest calls](monitoring%20calls.md#get-rest-calls)                                                                                | Statistical information on the REST calls.                                                                                                                                                                    |
| [get rest server info](monitoring%20calls.md#rest-server-configuration)                                                               | Information on the REST server configuration.                                                                                                                                                                 |
| [get msg clients](monitoring%20calls.md#get-msg-clients)                                                                              | Information on clients subscribed to topics.                                                                                                                                                                  |
| get msg brokers                                                                                                                       | Information on message brokers and the topics subscribed with each broker.                                                                                                                                    |
| get local broker                                                                                                                      | Information on the Message Broker.                                                                                                                                                                            |
| [get status](monitoring%20nodes.md#the-get-status-command)                                                                            | Replies with the string 'running' if the node is active. Can be extended to include additional status information                                                                                             | 
| get connections                                                                                                                       | The list of TCP and REST connections supported by the node.                                                                                                                                                   |
| get machine connections                                                                                                               | The system-wide socket connection. Users can detail specific port: ```get machine connections where port = [port]```                                                                                          |
| get platforms                                                                                                                         | The list connected blockchain platforms.                                                                                                                                                                      |
| [get dictionary](../monitoring%20nodes.md#the-get-dictionary-command)                                                                 | The list of the variable names and their assigned values.                                                                                                                                                     |
| [get env var](../monitoring%20nodes.md#the-get-env-var-command)                                                                       | The environment variables keys and values.                                                                                                                                                                    |
| get databases                                                                                                                         | The list of databases managed on the local node.                                                                                                                                                              |
| get partitions                                                                                                                        | Information on how data is partitioned on the local databases.                                                                                                                                                |
| get partitions where dbms = [dbms_name] and table = [table name]                                                                      | Partition details on a specific table.                                                                                                                                                                        |
| get query mode                                                                                                                        | The query param variables assigned by the command ***set query mode***.                                                                                                                                       |
| [get query pool](#get-pool-info)                                                                                                      | Details the status of query workers assigned by the command ***set threads pool [n]***. The value 0 means thread in rest and 1 processing data.                                                               |
| [get tcp pool](#get-pool-info)                                                                                                        | Details the number TCP workers thread that execute peer command. The number of threads is set by the command ***run tcp server***.                                                                            |
| [get rest pool](#get-pool-info)                                                                                                       | Details the number REST workers thread that execute REST calls. The number of threads is set by the command ***run rest server***.                                                                            |
| [get msg pool](#get-pool-info)                                                                                                        | Details the number Message Broker workers thread that execute REST calls. The number of threads is set by the command ***run message broker***.                                                               |
| [get operator pool](#get-pool-info)                                                                                                   | Details the number of operator threads. The number of threads is set by the command ***run operator***.                                                                                                       |
| get threads                                                                                                                           | The list of the threads executing users scripts.                                                                                                                                                              |
| get scheduler [n]                                                                                                                     | Information on the scheduled tasks. [n] - an optional ID for the scheduler, the default value is 1, 0 is the system scheduler.                                                                                |
| get hostname                                                                                                                          | The name assigned to the node.                                                                                                                                                                                | 
| [get dns name](#get-dns-name)                                                                                                         | return the DNS name.           |
| get version                                                                                                                           | The code version.                                                                                                                                                                                             |
| get git [version/info] [path to github root]                                                                                          | ***git version*** returns the first 5 digits of the commit used, ***git info*** provides additional information. If path is not specified, the dictionary variable ***!anylog_path*** is used to identify the ***AnyLog-Network*** directory. |
| get queries time                                                                                                                      | Statistics on queries execution time. The statistics is configurable by the command ***set query log profile [n] seconds***                                                                                   |
| get watch directories                                                                                                                 | The list of the Watch directories on the node.                                                                                                                                                                |
| get metadata info                                                                                                                     | Returns summary info on the metadata including version and time since last update .                                                                                                                           |
| get database size [database name]                                                                                                     | The size of the named database in bytes.                                                                                                                                                                      |
| get node id                                                                                                                           | Returns a unique identifier of the node.                                                                                                                                                                      |
| get hardware id                                                                                                                       | Returns a unique identfier of the hardware.                                                                                                                                                                   |
| [get servers](#get-servers)                                                                                                           | Retrurn info on the the servers supporting the table.                                                                                                                                                         |
| get tables for dbms [dbms name]                                                                                                       | The list of tables of the named database and where the table is declared (local database and/or blockchain)                                                                                                   |
| get table [exist status/local status/blockchain status/rows count/complete status] where name = table_name and dbms = dbms_name       | Returns information on the specified table                                                                                                                                                                    |
| get views for dbms [dbms name]                                                                                                        | The list of views of the named database.                                                                                                                                                                      |
| get files in [dir name] where type = [file type] and hash = [hash value]                                                              | The list of files in the specified dir that satisfy the optional filter criteria.                                                                                                                             |
| get file timestamp [file path and name]                                                                                               | Get the file's timestamp.                                                                                                                                                                                     |
| get error [error number]                                                                                                              | Get the error text for the error number.                                                                                                                                                                      |
| get echo queue                                                                                                                        | Get the queue with the ***echo*** commands and messages.                                                                                                                                                      |
| get files [directory path]                                                                                                            | Details the files in the specified directory.                                                                                                                                                                 |
| get directories [directory path]                                                                                                      | Details the sub-directories in the specified directory.                                                                                                                                                       |
| get json file structure                                                                                                               | Details the convention for JSON file name.                                                                                                                                                                    |
| get users                                                                                                                             | The list of users declared using the command ```id add user ...```.                                                                                                                                           |
| get reply ip                                                                                                                          | Retrieve the IP address for reply messages.                                                                                                                                                                   |
| get archived files [YYYY-MM-DD]                                                                                                       | List the files archived on the provided date.                                                                                                                                                                 |
| get size [dir name] [YYYY-MM-DD]                                                                                                      | List the size of a directory including sub-directories.                                                                                                                                                       |
| get access [path and file name or directory name]                                                                                     | Get the access rights to the provided file or directory.                                                                                                                                                      |
| get data nodes                                                                                                                        | Details the Operators that host each table's data.                                                                                                                                                            |
| [get rows count](monitoring%20nodes.md#monitoring-data-commands)                                                                      | Details the number of rows in all or specified tables.                                                                                                                                                        |
| [get files count](../dat%20manaement/image%20mapping.md#get-files-count)                                                              | Details the number of files stored in all or specified tables.                                                                                                                                                |
| [get query execution](profiling%20and%20monitoring%20queries.md#retrieving-the-status-of-queries-being-processed-on-an-operator-node) | Provides the status of queries being executed on an Operator node.                                                                                                                                            |
| get timezone info                                                                                                                     | Get the timezone on the local machine.                                                                                                                                                                        |
| get datetime [date-time function](queries.md#get-datetime-command)                                                                    | Translate a date-time function to the date-time string.                                                                                                                                                       |
| [get streaming conditions](streaming%20conditions.md#condition-declaration)                                                           | List the conditions assigned to streaming data.                                                                                                                                                               |
| [get nics list](network%20configuration.md#get-the-list-of-nics)                                                                      | List the conditions assigned to streaming data.                                                                                                                                                               |

#### Monitoring node status options
| Option  | Information provided |
|:-------:| :---: | 
| get disk [usage/total/used/free] [path]  | Disk statistics about the provided path.                                                                                                                                              |
| get platform info | Info on the type and version of the OS, node name and type of processor.                                                                                                              |
| get memory info | Info on the memory of the current node. The function depends on psutil installed.                                                                                                     |
| get cpu info | Info on the CPU of the current node.  The function depends on psutil installed.                                                                                                       |
| get cpu usage | Info on current usage of each CPU.  The function depends on psutil installed.                                                                                                         |
| get ip list | The list of IP addresses available on the node.                                                                                                                                       |
| get cpu temperature | The CPU temperature.                                                                                                                                                                  |
| get os process [options] | Different statistics on the OS processes. Details are available [here](../monitoring%20nodes.md#the-get-os-process-command).                                                          |
| get node info [options] | Different statistics on the node. Details are available [here](../monitoring%20nodes.md#the-get-node-info-command).                                                                   |
| get monitored | Retrieve the list of topics monitored by an aggregator node. Details are available [here](monitoring%20nodes.md#organizing-nodes-status-in-an-aggregator-node).         |
| get monitored [topic] | Retrieve monitored info on a specific topic from an aggregator node. Details are available [here](monitoring%20nodes.md#organizing-nodes-status-in-an-aggregator-node). |

Additional information is available at [monitoring nodes](monitoring%20nodes.md#monitoring-nodes).

#### Security and encryption related options
| Option  | Information provided |
|:-------:| :---: | 
| get public key  | The node\'s public key. | 
| get public key using keys_file = [file name] | Retrieves the public key from the specified file. |
| get permissions | Provide the permissions for the current node using the node public key. |
| get permissions for member [member id] | The permissions for the member identified by its public key. |
| get authentication | Returns ON or OFF depending on the current status. |
| get encryption | Returns ON or OFF depending on the current status. |
| get compression | Returns ON or OFF depending on the current status. |


### `dictionary` Command

The local dictionary allows hardware abstraction by associating configuration values (that are specific to the hardware used) to generic keys that are shared across all deployments. The configuration process, the queries and AnyLog commands that are issued to each node reference the shared keys which are translated to the specific values which may be different on each node.
For example: IPs and Ports, paths to files and directories are referenced by their assigned key names and translated on each node to the appropriate value.
Some entries in the dictionary represent default setups and configurations, and users can add or modify entries in the dictionary as needed.
For example, all the directories in the default folders structure can be referenced by their keys, whereas in each deployment the physical location of the folders may be different. Using this example, users can reference the path to the archive directory using the key !archive_dir, the path to the blobs directory using the key !blobs_dir etc. allowing a shared configuration process whereas the physical path to each folder can be different on each node.

Users can include in the dictionary any key value pair that is needed to support a process, for example, maintain values generated by data ingestion or represent a node state. For example, a user can declare a key called "disk_usage" and configure the scheduler to update the value with percentage of free space every 15 seconds and include the value (by referencing the name) in the processes monitoring the node state.

In addition, the dictionary is used to construct, maintain and update policies before their persistent storage in the shared metadata.


### `print` Command

Print output to the console, words starting with exclamation point are replaced with dictionary values and words starting 
with environment variables are replaced with system params. A words or multiple words inside a single quotation are not 
modified.

**Sample Command & Output**: 
```anylog 
print hello !node_name

'hello Operator_3'
```

### `echo` Command
Within AnyLog / EdgeLake, `echo` is similar to a `print` in that it allows for the user to generate statements using 
dictionary and environment variables. Unlike `print`, when enabled, `echo` has a built-in queue process that keeps a 
record of the `echo` messages coming into the node, as opposed to printing them directly on the CLI. 

* Enable / disable the echo queue. With echo queue, messages from peer nodes are stored in a queue rather than send to 
stdout.
```anylog
set echo [on/off]
```

A prompt extended by a plus (+) sign indicates a message in the buffer queue. For example:
```anylog 
AL Operator_3 +>
```

* Get the echo commands from the current nodes and peer nodes.
```anylog
AL Operator_3 +> get echo queue       
Message Queue:
Counter Time                       Message                                                                                              
-------|--------------------------|----------------------------------------------------------------------------------------------------|
     66|2025-07-16 02:04:48.006195|hello Operator_3                                                                                    |
```


--- 

## Executing Scripts with the CLI

### Setting & Using Variables

### Running Scripts
