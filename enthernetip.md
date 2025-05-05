# EtherNet/IP

## Overview
EtherNet/IP (Ethernet Industrial Protocol) is an industrial network protocol that enables communication between automation 
devices such as PLCs, sensors, actuators, and control systems over standard Ethernet networks.     
It builds on the Common Industrial Protocol (CIP), which defines a unified architecture for messaging and real-time I/O, 
allowing devices from different vendors to interoperate.

## The EtherNet/IP Structure

EtherNet/IP organizes industrial automation data through a set of well-defined CIP (Common Industrial Protocol) objects, 
which represent device attributes, configurations, and runtime data. Unlike OPC UA's tree-based model, EtherNet/IP uses a flat, 
object-oriented structure where each device exposes standard or vendor-specific classes, instances, and attributes. T
hese are accessed using CIP messaging over Ethernet.

Each class (such as Identity Object, Assembly Object, or Connection Object) may contain multiple instances, and each instance 
can expose multiple attributes, forming a structured view of the device's capabilities and status. 
While the structure is not hierarchical like OPC UA, it provides a standardized way to navigate and interact with device data.

The `get etherip struct` command explores the structure by querying supported classes and retrieving their instances and attributes. 
This provides insight into the connected PLC or device, including program tags and system-level data.

The EtherNet/IP structure is explored with the following command:


```anylog
get etherip struct where url = [connect string] and user = [username] and password = [password] and ...
```
This command enables users to query both system-level and user-defined tags, making it easier to explore and interact with a PLC’s data structure over EtherNet/IP.

### Command Variables

| Keyword     | Details                                                                                                                                |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `url`       | The IP address of the target PLC or EtherNet/IP device.                                                                                |
| `slot`      | The slot number of the target controller (used in multi-slot chassis).                                                                 |
| `user`      | Username, if the PLC requires authentication.                                                                                          |
| `password`  | Password for authentication.                                                                                                           |
| `limit`     | Limit the number of tags or objects returned in the response.                                                                          |
| `prefix`    | Limit the tags to a path that satisfies the prefix string.                                                                             |
| `output`    | The target for the output stream (stdout or a file name).                                                                              |
| `format`    | The format of the output (see details below).                                                                                          |
| `target`    | The variables in the 'blockchain insert commands'. This option is used with 'format = policy' to generate 'blockchain insert' commands |
| `schema`    | A boolean value. If set to True, output includes, for each tag, the table's schema.                                                    |
| `frequency` | Specifying the reading frequency in Hz, with **format = run_client**.                                                                  |
| `name`      | Specifying a process name when with **format = run_client** option.                                                                    |

Format options:
* tree - the OPC-UA tree structure (default).
* policy - generating a policy representing the tag. If target is specified, output is "blockchain insert" command for every policy.
* get_value - generating a [get plc value](#the-get-plc-values-command) command with the tags visited in the **get plc struct** command.
* run_client - generating a [run plc client](#the-run-plc-client-command) command with the tags visited in the **get plc struct** command.

Examples:

The following example outputs the PLC tags and their current value:
```anylog
get etherip struct where url = 127.0.0.1 and read = true
```
The following example outputs a **get plc values** command (see details [below](#the-get-plc-values-command)):
```anylog
get etherip struct where url = 127.0.0.1 and format = get_value 
```
The following example outputs a **run plc client** command (see details [below](#the-run-plc-client-command)):
```anylog
get etherip struct where url = 127.0.0.1 and format = run_client and frequency = 1 and name = etherip_reads and dbms = my_dbms
```
The following example outputs tag policies and tables policies to enable streaming of the PLC data to local databases 
```anylog
get etherip struct where url = 127.0.0.1 and format = policy  and schema = true and dbms = my_dbms and target = "local = true and master = !master_node" and output = !tmp_dir/my_file.out
```

## The Get PLC Values Command
Tag values are retrieved with the following command:

```anylog
get plc values where type = [connector type] and url = [connect string] and user = [username] and password = [password] and node = [node id]
```

Details:

[connect string] - The url specifies the endpoint of the OPC UA server.
[user] - The username required by the OPC UA server for access.
[password] - The password associated with the username.
[node] - One or multiple node IDs.
[nodes] - Providing a list of nodes, separated by comma, within square brackets.

Examples:

```anylog
get plc values where type = etherip and url = 127.0.0.1 and node = CombinedChlorinatorAI.PV and node = STRUCT.Status

get plc values where type = etherip and url = 127.0.0.1 and nodes = ["CombinedChlorinatorAI.PV", "STRUCT.Status"]
```

## The Run PLC Client Command

The command **run plc client*** pulls data from the PLC continuously and streams the data into a database on the local node:
```anylog
run opcua client where name = [unique name] and url = [connect string] and frequency = [frequency] and dbms = [dbms name] and table = [table name] and node = [node id]]
```
 
The following tables summarizes the command variables:

| keyword   | Details                                                                                      |
|-----------|----------------------------------------------------------------------------------------------| 
| name      | A unique connection name.                                                                    |
| url       | The url specifies the endpoint of the OPC UA server.                                         |
| user      | the username required by the OPC UA server for access.                                       |
| password  | the password associated with the username.                                                   |
| frequency | Read frequency in seconds or a fraction of seconds using hz (i.e.: 10 hz).                   |
| node      | ID of one or multiple nodes that their value is retrieved.                                   |
| nodes     | Providing a list of nodes, separated by comma, within square brackets.                       |
| policy    | If nodes are not specified on the CLI, the policy determines the nodes and the table to use. |
| dbms      | The database to host the data (if not specified in a policy).                                |
| table     | The table to host the data (if not specified in a policy).                                   |
| topic     | If data is processed through the local broker.                                               |


Example 1 - listing individual tags:
```anylog
run plc client where type = etherip and name = etherip_reads and url = 127.0.0.1 and frequency = 1 and dbms = my_dbms and node = FreeChlorinatorAI.PV and node = CombinedChlorinatorAI.PV
```
Example 2 - providing a list of tags:
```anylog
<run plc client where type = etherip and name = etherip_reads and url = 127.0.0.1 and frequency = 1 and dbms = my_dbms and nodes =
["BOOL","SINT","INT","DINT","REAL","STRING","STRUCT.Temp","STRUCT.Status","ARRAY_INT","ARRAY_BOOL","ARRAY_STRING","TIMER.ACC"
,"TIMER.PRE","COUNTER.ACC","COUNTER.PRE","DATE_TIME","ATSNormalRdyDI","CombinedChlorinatorAI.PV","FreeChlorinatorAI.PV"]>
```

Notes: 
1. Multiple clients can be declared on the same node.
2. Each row is added with 2 columns:
   * Timestamp - representing the earliest source_timestamp of the values considered (if source_timestamp is missing, the server_timestamp is considered).
   * Duration - the number of milliseconds between the earliest timestamp and the latest timestamp that were considered in the values that were retrieved from the OPCUA.


## Example - Creating Policies from EtherNet/IP and pulling data

The first step is to create policies that represent the tags to be managed. 
These policies define the structure and semantics of the tags, including their names, data types, and relationships.   
Once defined, the policies are published to the blockchain. They serve as a mapping between table names and tag information, and vice versa.    
This enables the system to automatically interpret and organize incoming data from OPC UA or other sources, aligning it 
with the defined structure for seamless querying, validation, and distribution across the network.

### Generate the policies
```anylog
get etherip struct where url = 127.0.0.1 and format = policy  and schema = true and dbms = my_dbms and target = "local = true and master = !master_node" and output = !tmp_dir/my_file.out
```
These tag policies are stored in a file: **!tmp_dir/my_file.out** and the format is like the example below:
```anylog
 {'tag' : {'protocol' : 'etherip',
           'ns' : 0,
           'dbms' : 'my_dbms',
           'table' : 't101',
           'datatype' : 'boolean',
           'node_sid' : 'BOOL',
           'id' : '0e17856bdb914cdfe338eff3485ef366',
           'date' : '2025-05-04T18:07:54.695893Z',
           'ledger' : 'local'}}]
```
If **schema** is set to **true**, the output includes, for every tag, the table's schema associated with the tag.  
Example:
```anylog
{"table": {"name": "t109", 
           "dbms": "my_dbms", 
              "create": "CREATE TABLE IF NOT EXISTS t109(row_id SERIAL PRIMARY KEY,  insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
              tsd_name CHAR(3),  tsd_id INT,  timestamp timestamp not null default now(),  value varchar ); 
              CREATE INDEX t109_timestamp_index ON t109(timestamp); CREATE INDEX t109_insert_timestamp_index ON t109(insert_timestamp);", 
              "source": "ETHERIP Interface"}}
```

### Load the file to the metadata
```anylog
process !tmp_dir/my_file.out
```
### Generate the command to read the tags data
```anylog
get etherip struct where url = 127.0.0.1 and format = run_client and frequency = 1 and name = etherip_reads and dbms = nov
```
Notes:
* The [run opcua client](#pulling-data-from-opcua-continuously) command is stored in a file: **!tmp_dir/my_file.out**.
* The **table** name is not specified as it will be derived from the policies (based on the namespace and node id).

### Execute the command
```anylog
process !tmp_dir/my_run_cmd.out 
```

This process pulls the data using OPCUA and assigns the data to the tables according to the info in the policies.

