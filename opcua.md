

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

Retieving the namespaces is with the following command:
```anylog
get opcua namespace where url = [connect string] and user = [username] and password = [password]
```
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
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and user = [username] and password = [password] and ...
```
  
The following tables summarizes the command variables:

| keyword    | Details                                                                                   |
|------------|-------------------------------------------------------------------------------------------| 
| url        | The url specifies the endpoint of the OPC UA server.                                      |
| username   | the username required by the OPC UA server for access.                                    |
| password   | the password associated with the username.                                                |
| node       | Define a different root by providing the node id: examples: 'ns=0;i= i=84 or s=MyVariable |
| type       | Type of nodes to consider: Object, Variable etc. If not specified, all types are visited. |
| attributes | Attribute names to consider or * for all                                                  |
| limit      | Limit the Tree traversal by the number of nodes to visit                                  |
| depth      | Limit the Tree traversal by the depth                                                     |

Examples:
1. Traversal from the root and limit by 10 nodes:
    ```anylog
    get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and limit = 10
    ```
2. Traversal from the root and limit by depth:
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