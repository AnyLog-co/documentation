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

### `dictionary` Command

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
stdtout.
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
