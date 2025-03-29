

# Using OPC-UA

## Overview

OPC Unified Architecture (OPC UA) is a robust, platform-independent communication protocol widely used in industrial automation 
for secure and reliable data exchange between devices, systems, and applications. 
Designed as an evolution of the OPC Classic standard, OPC UA provides cross-platform compatibility and supports 
advanced features like real-time data access, historical data retrieval, and event notifications. 
Its architecture emphasizes security with built-in encryption, authentication, and access control, making it ideal for modern i
ndustrial IoT and Industry 4.0 environments. By enabling seamless interoperability across diverse hardware and software,
OPC UA simplifies the integration and scalability of complex industrial systems.

Users can issue requests and configure their nodes to act as clients, pulling data from an OPC-UA interface.

## The OPCUA Namespace

In OPC UA, namespaces are used to organize and uniquely identify nodes in the address space of a server.    
Each namespace is assigned a unique index (e.g., ns=0, ns=1, ns=2), which is used in Node IDs.  
Example Node ID: ns=1;s=TemperatureSensor.

Retrieving the namespaces is with the following command:
```anylog
get opcua namespace where url = [connect string] and user = [username] and password = [password]
```
Details:
* [connect string] - The url specifies the endpoint of the OPC UA server.
* [username] - the username required by the OPC UA server for access.
* [password] - the password associated with the username.

Example:
```anylog
get opcua namespace where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer
```

## The OPCUA Structure

The OPC UA tree structure organizes the server's address space into a hierarchical model resembling a file system, 
making it intuitive to navigate and interact with data. At the root level, predefined folders like 
**Objects**, **Types**, and **Views** provide entry points to different parts of the address space.  
The Objects folder contains application-specific nodes, such as devices, sensors, or systems, 
while the Types folder defines the structure and behavior of nodes, including ObjectTypes, VariableTypes, and DataTypes.     
Each node in the tree can have child nodes, creating a parent-child relationship that represents connections or logical groupings.

The **get opcua struct** command navigates in the tree and provides different types of outputs (based on the command line variables).  
The navigation starts from the root of the tree, unless the user specifies a node to serve as a root.

The Tree structure is explored with the following command:
```anylog
get opcua struct where url = [connect string] and user = [username] and password = [password] and ...
```
  
The following tables summarizes the command variables:

| keyword    | Details                                                                                        |
|------------|------------------------------------------------------------------------------------------------| 
| url        | The url specifies the endpoint of the OPC UA server.                                           |
| username   | the username required by the OPC UA server for access.                                         |
| password   | the password associated with the username.                                                     |
| node       | Define a different root by providing the node id: examples: 'ns=0;i= i=84 or s=MyVariable      |
| type       | Type of nodes to consider: Object, Variable etc. If not specified, all types are visited.      |
| attributes | Attribute names to consider or * for all                                                       |
| limit      | Limit the Tree traversal by the number of nodes to visit                                       |
| depth      | Limit the Tree traversal by the depth.                                                         |
| class      | Filter the Tree traversal to show only nodes in the listed class.                              |
| output     | The target for the output stream (stdout or a file name).                                      |
| format     | The format of the output (see details below).                                                  |
| frequency  | If output generates "run_client" - the frequency of the "run client" command                   |
| dbms       | If output generates "run_client" - the table name of the "run client" command                  |
| table      | If output generates "run_client" - the dbms name of the "run client" command                   |
| validate   | A boolean value. If set to True, the value from each visited node is read (see details below). |

**Format options:**
* **tree** - the OPC-UA tree structure (default)
* **stats** - statistics counting the number of entries in each class.
* **get_value** - generating a [get opcua value command](#the-get-opcua-values-command) with the tree visited in the **get opcua struct** command.   
* **run_client** - generating a [run opcua client command](#pulling-data-from-opcua-continuously) with the tree visited in the **get opcua struct** command.

**The validate option:**  
* The default value is **false**. 
* If value is set to **true**, the value of each considered node is read during the traversal.
* If the read fails:
  * if **format** is set to **get_value** or **run_client** the node is not considered.
  * In other cases, the output includes a **validate** attributes which is assigned with the value **success** or **failure**.
  * The summary chart includes a counter for the number of nodes that failed to generate a value.

**Examples:**
1. Traversal from the root and limit by 10 nodes:
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and limit = 10
    ```
2. Traversal from the root, output is directed to a file:
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = !prep_dir/opcua_tree.txt and limit = 10
    ```
3. Traversal from the root and limit by depth:
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and depth = 4
    ```
4. Traversal from a new root (from node "ns=6;s=MyObjectsFolder"):
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and node="ns=6;s=MyObjectsFolder"
    ```
5. Traversal from a new root (from node "ns=6;s=MyObjectsFolder") including attribute info:
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and node="ns=6;s=MyObjectsFolder" and attributes = *
    ```
6. Traversal from the root, limit by depth 4 and filter by classes "variable" and "object"
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and depth = 4 and class = variable and class = object
    ```
7. Traversal from a new root (from node "ns=6;s=MyObjectsFolder"), considering only variables, and output the visited nodes to a **get opcua value** command.
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node="ns=6;s=MyObjectsFolder" and class = variable and format = get_value
    ```
8. Traversal from a new root (from node "ns=6;s=MyObjectsFolder"), considering only variables, and output the visited nodes to a **run opcua client** command.
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node="ns=6;s=MyObjectsFolder" and class = variable and format = run_client and dbms = nov and table = sensor and frequency = 10 and limit = 10
    ```
      
## The Get OPCUA Values Command

Node values are retrieved with the following command:
```anylog
get opcua values where url = [connect string] and user = [username] and password = [password] and node = [node id]
```
Details:
* [connect string] - The url specifies the endpoint of the OPC UA server.
* [username] - The username required by the OPC UA server for access.
* [password] - The password associated with the username.
* [include] - Additional attributes that are returned with the value.
* [node] - One or multiple node IDs.
* [nodes] - Providing a list of nodes, separated by comma, within square brackets.
* [method] - 2 optional values:
  * **collection** - The default, a single read pulls the values of all the listed nodes.
  * **individual** - Each value is read individually, this option is used to identify the ID of the node causing the failures.
* [failures] - A boolean value to determine the data collected. This option requires **method** to be set as **individual**.
  * **false** - The default value - data from successful and failed reads are collected.
  * **true** - Only failed reads are collected.

The include options:
* id - the id of the attribute
* name - The attribute name
* source_timestamp - The timestamp of the value as determined by the data source (e.g., a sensor or device).
* server_timestamp - The timestamp assigned by the OPC UA server when the data value was received or processed.
* status_code - The status of the value (e.g., Good, Bad, Uncertain).

Note: if **include** is assigned with the keyword **all**, all attributes are included in the output.

Example 1:
```anylog
get opcua values where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node = "ns=0;i=2257" and node = "ns=0;i=2258" and include = all
```
Example 2, using a comma seperated list of nodes:
```anylog
get opcua values where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and nodes = ["ns=4;s=AirConditioner_1.StateCondition.EventType","ns=4;s=AirConditioner_1.StateCondition.SourceNode"]
```
Example 3, identifying failed reads:
```anylog
get opcua values where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and method = individual and failures = true and nodes = ["ns=4;s=AirConditioner_1.StateCondition.EventType","ns=4;s=AirConditioner_1.StateCondition.SourceNode"]
```
## Pulling data from OPCUA continuously

The command **run opcua client*** pulls data from OPCUA continuously and streams the data into a database on the local node:
```anylog
run opcua client where url = [connect string] and frequency = [frequency] and dbms = [dbms name] and table = [table name] and node = [node id]]
```
 
The following tables summarizes the command variables:

| keyword   | Details                                                                                      |
|-----------|----------------------------------------------------------------------------------------------| 
| url       | The url specifies the endpoint of the OPC UA server.                                         |
| username  | the username required by the OPC UA server for access.                                       |
| password  | the password associated with the username.                                                   |
| frequency | Read frequency in seconds or a fraction of seconds using hz (i.e.: 10 hz).                   |
| node      | ID of one or multiple nodes that their value is retrieved.                                   |
| nodes     | Providing a list of nodes, separated by comma, within square brackets.                       |
| policy    | If nodes are not specified on the CLI, the policy determines the nodes and the table to use. |
| dbms      | The database to host the data (if not specified in a policy).                                |
| table     | The table to host the data (if not specified in a policy).                                   |
| topic     | If data is processed through the local broker.                                               |


Example 1:
```anylog
run opcua client where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and frequency = 10 and dbms = nov and table = sensor and node = "ns=0;i=2257" and node = "ns=0;i=2258"
```
Example 2:
```anylog
run opcua client where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and frequency = 10 and dbms = nov and table = sensor and nodes = ["ns=0;i=2257","ns=0;i=2258"]
```

Notes: 
1. Multiple OPCUA client can be declared on the same node.
2. Each row is added with 2 columns:
   * Timestamp - representing the earliest source_timestamp of the values considered (if source_timestamp is missing, the server_timestamp is considered).
   * Duration - the number of milliseconds between the earliest timestamp and the latest timestamp that were considered in the values that were retrieved from the OPCUA.

## Client status

The following command provides the info on the OPCUA Client processes:
```anylog
get opcua client
```

## Exit OPCUA Client

The following command terminates a client process:
```anylog
exit opcua client [client name]
```
The client name is the policy ID or **[dbms name].[table name]**.  
If the client name is **all**, all clients are terminated.
Examples:
```anylog
exit opcua all
exit opua nov.rig8
```

## Example - Declaring OPC UA with aggregations

Aggregation functions summarize streaming data over a time interval. See details in the [Aggregation](aggregations.md) section.

The following are the needed configuration steps:

### Identify the time and value attribute names

To apply aggregation on the OPC UA, users need to identify the names of the time attribute and the value attribute retrieved from the OPC UA connector.      
If the AnyLog OPC UA service is used, the time attribute name is **timestamp** and users can retrieve the value attribute name using the ```get 
opcua values``` command with **include = all** or **include = name**.

Example:
```anylog
get opcua values where url = opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer and node = "ns=3;i=1002" and include = name

OPCUA Nodes values
name   value
------|----------|
random|-0.5909728|
```
The call above shows that the column name for "ns=3;i=1002" is **random**.

### Apply aggregation on the OPC UA columns and assign a database and table

```anylog
set aggregations where dbms = nov and table = table_2 and time_column = timestamp and value_column = random
```

### Declare the aggregation menthod (optional)
The following example will replace the OPC UA source data with an aggregation function:
```anylog
set aggregations encoding where dbms = nov and table = table_2 and encoding = bounds
```

### Validate the aggregation declarations
```anylog
get aggregations
get aggregations config
```

### Start the OPC UA service
```anylog
<run opcua client where 
   url=opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer and 
   node = "ns=3;i=1002" and 
   frequency=25 and 
   dbms=nov and 
   table=table_2> 
```

### Validate processing
```anylog
get opcua client
get aggregations
get aggregations where dbms = nov and table = table_2
get streaming
get operator
```

### Validate data
```anylog
run client () sql nov select timestamp, min, max, count, avg from bounds_table_2 order by timestamp desc limit 10  
```

run client () sql nov select * from bounds_table_2
