---
title: "AnyLog Release notes"
description: ""
layout: page
source_path: "release/notes.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 |            |                |                  |          |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-08-0X | Ori Shadmon    | Updated URLs     | 2.0.2606 |   
--->

# AnyLog Release notes

AnyLog Version: 2.0.2606 (ms-dev - 4bd615 [2026-07-06 00:02:19])
1. Add ```is declared``` and ```not declared``` to blockchain get
2. New command to get a unique id (in the config process).

AnyLog Version: 1.5.2605 [2026-06-30 18:35:19]
### New Features
1. Using ```for loop``` in scripts and pulling attribute values from the dictionary - see <a href="../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/02-%20dictionary.md#referencing-values-in-a-list-of-dictionaries" target="_blank">details</a>.

AnyLog Version: 1.5.2605 [2026-06-12 18:37:39]
### New Features
1. New commands: ```get global tables``` and ```get local tables``` See details under <a href="../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/03-%20sql%20setup.md#the-metadata" target="_blank">The metadata</a> 
2. Add **include** and **exclude** options to the command ```blockchain get root policies``` - See details <a href="../08-%20Blockchain%20%26%20Metadata/03-%20Blockchain%20Commands.md" target="_blank">here</a>

AnyLog Version: 1.4.2510-beta3 [e0d9e1] [2026-03-08 17:52:24]
### New Features
1. New options for issuing AnyLog commands via REST: 
    * <a href="../06-%20Networking%20%26%20Security/04-%20Using%20REST.md" target="_blank">Specifying commands in the message URL</a>
    * <a href="../06-%20Networking%20%26%20Security/04-%20Using%20REST.md" target="_blank">Specifying commands in the message body</a>

AnyLog Version: 1.4.2510-beta3 [8ca403] [2026-02-02 16:13:21] <a href="../08-%20Blockchain%20%26%20Metadata/03-%20Blockchain%20Commands.md" target="_blank">Details</a>
### New Features
1. New command option: **blockchain get root policies**  
2. ```set mcp client config``` command - Configure an active MCP connection to automatically disconnect after a specified period of inactivity. The default timeout is one hour.
3. Adding UNS policies generation. <a href="../06-%20Networking%20&%20Security/05-%20Message%20Broker.md#generating-uns-policies" target="_blank">Details</a>

AnyLog Version: 1.4.2510-beta3 [845952] [2025-11-30 18:01:37]
### New Features
1. MCP Server functionalities
2. Connector to Akave
### New Commands
1. ```get mcp status``` - Returns information on the MCP clients connected to the node.
2. ```get node resources``` - Returns info on the resources available to the node.
### New Features
1.  Add timezone to query casting options. <a href="../07-%20CLI/04-%20SQL.md" target="_blank">Details</a>

## AnyLog Version: 1.4.2509-beta1 [2a53f6] [2025-10-18 17:07:29]
1. New options to merge and join policies dynamicaly, in a ```blockchain get``` command. <a href="../08-%20Blockchain%20%26%20Metadata/03-%20Blockchain%20Commands.md" target="_blank">Details</a>

## AnyLog Version: 1.3.2504-beta22 [fb9340] [2025-09-24 19:54:29]
1. New command: ```file from``` - Return a file via REST. [Details]()

## AnyLog Version: 1.3.2504-beta22 [69bf12] [2025-08-16 19:18:49]
1. New option for where condition to retrieve immediate child ```childfrom``` command. <a href="../07-%20CLI/08-%20Conditional%20Execution%20and%20Control%20Flow.md" target="_blank">Details</a>

## AnyLog Version: 1.3.2504-beta22 [77ce52] [2025-08-04 16:59:25]
1. (AE) New options for ```get columns``` command. <a href="../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/03-%20sql%20setup.md#The-get-columns-command" target="_blank">Details</a>

## AnyLog Version: 1.3.2504-beta22 [cc7a3b] [2025-07-26 14:24:20]
### New Commands
1. (A) The command ```run helpers``` initiates AnyLog helper processes. <a href="../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/04-%20helpers.md" target="_blank">Details</a>
2. (AE) The command ```get dynamic stats``` provides info on internal processes. <a href="../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/04-%20helpers.md#Dynamic-monitoring-of-internal-processes" target="_blank">Details</a>

## AnyLog Version: 1.3.2504-beta22 [318361] [2025-07-11 20:49:13]
### New Command
1. (AE) The command "flush buffers" forces streaming data to be pushed to the database ignoring the buffer fill and time thresholds.

## AnyLog Version: 1.3.2504-beta9 [1c2753] [2025-06-07 19:14:56]
### New features
1. (AE) Manage Windows Event Log. Detaile <a href="../04-%20Southbound%20Interfaces/05-%20Monitoring" target="_blank">Run Scheduled Pull</a>

## AnyLog Version: 1.3.2504-beta7 [009f60] [2025-05-15 21:02:36]
### New features
1. (AE) Debug Method Using the ```trace method``` Command:
    Use the following format to enable or disable tracing of specific methods:  
    ```trace method [on/off] [method name]```  
    Examples:  
    * Enable trace of TCP messages sent from the node: ```trace method on tcp out```
    * Disable trace of TCP messages sent from the node: ```trace method off tcp out```
    * Enable trace of TCP messages received by the node: ```trace method on tcp in```
    * Disable trace of TCP messages received by the node: ```trace method off tcp in```
2. (AE) New command: **get nics list** - Retrieves and displays a list of all network interfaces (NICs). [Details](../06-%20Networking%20&%20Security/02-%20Network%20Processing.md#nic_type--which-interface-identifies-this-agent).
3. (AE) New command: **set internal ip with [nic name]**. [details](../06-%20Networking%20&%20Security/02-%20Network%20Processing.md#nic_type--which-interface-identifies-this-agent)

## AnyLog Version: 1.3.2504-beta4 [168405] [2025-05-12 21:13:37]
### New features
1. (AE) Adding an option to return a list of objects from the metadata. Example: blockchain get tag bring.list [tag][dbms] . [tag][table]
## AnyLog Version: 1.3.2504-beta1 [d483ae] [2025-05-05 10:35:06]
### New features
1. (AE) Adding EtherNet/IP connector. See details in [EtherNet/IP](../04-%20Southbound%20Interfaces/04-%20Industrial%20Connectors/04-%20EtherIP.md)
### Updates
1. (AE) Making the OPCUA call consistent with EtherNet/IP - [OPC-UA](../04-%20Southbound%20Interfaces/04-%20Industrial%20Connectors/03-%20OPC-UA.md)

## AnyLog Version: 1.3.2504 [673f50] [2025-04-27 20:15:35]
### New features
1. (AE) Adding **extend** and **include** options to the Grafana payload. See details in [example 2 in Using Grafana documentation](../05-%20Northbound%20Connectors/03-%20Grafana.md).

### Bugs Fixed
1. (AE) Rejecting tag policies (with OPC-UA) with duplicate String ID or Int ID. 

## AnyLog Version:  1.3.2501-beta3 [3fd820] [2025-04-12 17:47:39]
### New Features:
1. (AE) Optimized increments function. Details: [Increments Optimized Version](../07-%20CLI/04-%20SQL.md#increments)  
2. (AE) A new AnyLog command: **get increments params**. Details: [get-increments-params-command](../07-%20CLI/04-%20SQL.md#increments)
3. (AE) A new option to optimize data points returned in Grafana. Details: [Using the Time-Series Data Visualization](../05-%20Northbound%20Connectors/03-%20Grafana.md ).

## AnyLog Version: 1.3.2501-beta3 [7ec215] [2025-03-30 16:52:26]
### New Features:
1. (AE) New command to configure output table width: set output table width 250
2. (AE) New Functionality for String Substring Operations. Details: [Special Bring Values](../07-%20CLI/05-%20JSON%20Data%20Transformation.md#special-bring-values)
3. (AE) Severe error messages (boxed) are now printed on the node in RED.

## AnyLog Version: 1.3.2401 [d9321d] [2025-03-07 18:19:06]
### New Features:
1. (AE) Using DNS names. Details: [Get DNS Name](../06-%20Networking%20&%20Security/02-%20Network%20Processing.md)

## AnyLog Version: 1.3.2401 [d6c050] [2025-02-16 13:59:47]
### New Features:
1. (A) Aggregations over user data. Details: [Aggregations](../09-%20Data%20Management/02-2%20Data%20Aggregations.md)
2. (AE) New AnyLog command: **subprocess** to run shell scripts.

## AnyLog Version: 1.3.2401 [6665e9] [2025-01-26 14:14:09]
### New Features:
1. (AE) wait for a blockchain sync. Details: [AnyLog Commands](../07-%20CLI/08-%20Conditional%20Execution%20and%20Control%20Flow.md#the-wait-command)

## **Version** [139b43] [2025-01-04 14:23:39]
### New Features:
1. (A) Add **license** policy.    
Usage example:  
Creating the policy:  
```
license_number_key = "af043d39675e85e5c9d74999dfd123de2e54e6ed4f1fe9bed04b8ce7754826c89aa1adfb562b18d49f7c4a336ecedadb3c3ca43f88a7d3f4644b6424c5f6ba9217bede0bbcdc94094af9f6e213aa247ccb3ed5f77b794f68df07a62552ac0c6d9c67e406fe6213d6145d7c3d2c127e99906dffebd1c34c12b259719d80e6fcb3"
policy = create policy license where company = AnyLogCo. and expiration = 2025-03-01 and type = beta and activation_key = !license_number_key   # create the policy to a variable called "policy"
```
Updating the policy:
```
blockchain insert where policy = !policy and local = true and master = !master_node
```
Retrieving the License:
```
blockchain get license bring.last [license][activation_key] "{'company':'"  [license][company] "','expiration':'"  [license][expiration] "','type':'" [license][type] "'}"
```
2. Extending string operations
(AE) Supporting: !param_name[from_offset:to_offset]  
(A) Example to create a poiicy from a license key:
```
license_key = "af043d39675e85e5c9d74999dfd123de2e54e6ed4f1fe9bed04b8ce7754826c89aa1adfb562b18d49f7c4a336ecedadb3c3ca43f88a7d3f4644b6424c5f6ba9217bede0bbcdc94094af9f6e213aa247ccb3ed5f77b794f68df07a62552ac0c6d9c67e406fe6213d6145d7c3d2c127e99906dffebd1c34c12b259719d80e6fcb3{'c
ompany':'AnyLogCo.','expiration':'2025-03-01','type':'beta'}"       # Note: maintain the quotations to avoid formatting of the string

key_part = !license_key[:256]       # Extract the key from the license
info_part = !license_key[256:]      # Extract the JSON part from the license

json !info_part     # Print the json part

company = from !info_part bring [company]       # Extract the company name
expiration = from !info_part bring [expiration]    # Extract the expiration date
type = from !info_part bring [type]          # Extract the license type

policy = create policy license where company = !company. and expiration = !expiration and type = !type and activation_key = !license_key   # create the policy to a variable called "policy"

```
### Changes
1. (AE) Modify the command **exit mqtt** to **exit msg client [n/all]** - Details are in: [Processing messages and terminating a subscription](../04-%20Southbound%20Interfaces/03-%20Direct%20Connectors/02-%20Message%20Broker.md).

## **Version** [c03b82] [2025-01-02 12:30:17]
### New Features:
1. (AE) OPCUA support. Details: [OPC-UA](../04-%20Southbound%20Interfaces/04-%20Industrial%20Connectors/03-%20OPC-UA.md) 

## **Version**: [024a85] [2024-12-21 13:31:31]
### New Features:
1. (AE) A new command: **file to** - write a file to a specified directory, using CLI or via REST. 
   Details are in [Copy a file to a folder](../07-%20CLI/09-%20File%20Commands.md#copy-a-file-to-a-folder) section.  
   This command can be used to remotely copy configurations to a node. An example is available in the [using rest](../06-%20Networking%20%26%20Security/04-%20Using%20REST.md#examples) section.
2. The command **process** is supported using REST PUT.
### Changes
1. (AE) The required structure for the file name in the **file store** command is optional. 
   See details in the [Insert a file to a local database](../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/05-image%20mapping.md#insert-a-file-to-a-local-database) section. 

## **Version**: [a4924f] [2024-12-07 16:49:46] /
### New Features:
1. (AE) HTTP Commands - specifying commands and output format using http requests. Details in [http commands](../04-%20Southbound%20Interfaces/03-%20Direct%20Connectors/01-%20REST.md). 

## **Version**: [be71d3] [2024-08-29 15:18:04] |
### New Features:
1. (AE) New Casting features in SQL: function, lstrip, rstrip, timediff. Details in [CAST Data](../07-%20CLI/04-%20SQL.md#cast-data--formatting-options)
2. (AE) Increment function without specifying the time range - the time intervals would be provided dynamically.  
3. (AE) Configuring the number of threads when a message to peers is send. See details [here]().
4. (AE) Monitor inserts using the command: **trace level = 1 insert 10000** 10,000 is the threshold to print stats on inserts

## **Version**: 1.4 | 
### Changes
1. (AE) Create EdgeLake branch.
2. Update **blockchain set account info** call to include the Chain ID. 
3. (AE) Add options to create HTML documents from a query.
4. (AE) Add option **unlog** to PSQL declaration. Details in [Connecting to a local database](../09-%20Data%20Management/02-1%20Databases/01-%20SQL%20Storage.md).

### New Features:
1. (AE) New command: **get policies diff** detailed in [Compare Policies](../08-%20Blockchain%20&%20Metadata/03-%20Blockchain%20Commands.md#compare-policies-).

## **Version**: 1.3.240112 | 

### New Features
1. (AE) Adding support to gRPC [Using gRPC](../04-%20Southbound%20Interfaces/06-%20RPC%20&%20Media%20Streaming/01-%20gRPC.md)
2. (AE) Deprecated: "run mqtt client" --> Replaced by: "run msg client" 
3. (AE) **delete archive** command. Details: [Operator data archival](../07-%20CLI/02-%20Background%20Processes.md). 
4. (AE) Adding support to syslog [Using SysLog](../04-%20Southbound%20Interfaces/05-%20Monitoring/02-%20Syslog.md)

## **Version**: 1.3.23110 | **Release Date**: Oct.  12 2023 (Official)

### New Features
1. (AE) Adding sort by columns to **blockchain get** command. Details: [the bring command](../07-%20CLI/05-%20JSON%20Data%20Transformation.md#the-bring-keyword)
2. (AE) Adding sort by columns to **get data nodes** command. Details: [View the distribution of data to clusters](../09-%20Data%20Management/03-%20High%20Availability.md)

## **Version**: 1.3.2309 | **Release Date**: Oct.  2 2023 (Official)

### New Features:
1.  (AE) pip Install. Details: [pip Install](../02-%20Installation%20%26%20Deployment/02-%20Virtualization/99-06-%20Pip%20Install.md)
2.  (AE) Deploy AnyLog node as a background process. Details: [Deploy AnyLog as a background process](../02-%20Installation%20&%20Deployment/02-%20Virtualization/99-05-%20AnyLog%20as%20a%20Service.md).
3.  (AE) Map a local CLI to a peer node. Details: [Assigning a CLI to a peer node](../06-%20Networking%20&%20Security/02-%20Network%20Processing.md).
4.  (AE) Start a new node with a seed from a peer node. Details: [Retrieving the metadata from a source node](../08-%20Blockchain%20%26%20Metadata/03-%20Blockchain%20Commands.md)
5.  (AE) [Associating peer replies to a key in the dictionary]().    
6.  (AE) wait command - pauses execution by time and condition. Details: [The Wait Command](../07-%20CLI/08-%20Conditional%20Execution%20and%20Control%20Flow.md#the-wait-command)
7.  (AE) Create policy command - a command option to declare policies and include default attributes. Details:
    [Creating policies using the Create Policy command](../08-%20Blockchain%20&%20Metadata/02-%20Policy%20&%20Metadata.md)
8.  (AE) REST requests without a command assume get status. Example: `curl 10.0.0.78:7849` returns: **AnyLog@73.202.142.172:7848 running** 

### Changes:

1.  (AE) The command: **run blockchain sync where source = master**, if connection info is not provided, connection info is
    retrieved from the policy of the Master Node. Details: [Blockchain Synchronizer](../07-%20CLI/02-%20Background%20Processes.md).
    
2. (AE) If echo queue is set to True - all stdout messages which are not the result of the user keyboard input on the CLI are directed to the echo queue.

3. (AE) If license key is not provided - the **get status** command returns a warning on the missing license key.    

4. (AE) Option for **min** and **max** values in the ```bring command```: Details: [The bring keyword](../07-%20CLI/05-%20JSON%20Data%20Transformation.md#the-bring-keyword)

### Bugs fixed:

1. (AE) The command **get inserts** ignored data inserted in immediate mode.