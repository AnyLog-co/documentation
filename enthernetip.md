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

| Keyword    | Details                                                                |
|------------|------------------------------------------------------------------------|
| `url`      | The IP address of the target PLC or EtherNet/IP device.                |
| `slot`     | The slot number of the target controller (used in multi-slot chassis). |
| `user`     | Username, if the PLC requires authentication.                          |
| `password` | Password for authentication.                                           |
| `limit`    | Limit the number of tags or objects returned in the response.          |
| `prefix`   | Limit the tags to a path that satisfies the prefix string.            |



## The Get PLC Values Command
Tag values are retrieved with the following command:

```anylog
get plc values where type = etherip and url = [connect string] and user = [username] and password = [password] and node = [node id]
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
