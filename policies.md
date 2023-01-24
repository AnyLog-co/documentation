# Policies based Metadata

AnyLog maintains the metadata in a ledger. The metadata is organized as a collection of objects, called policies. A 
policy is a JSON structure with a single key at the root. The root key is called the Policy Type.

Example of policy types: database, table, operator, device. The following Policy describes an Operator (an Operator is a 
node that hosts data):

```json
{"operator": {
    "cluster": "7a00b26006a6ab7b8af4c400a5c47f2a",
    "ip": "24.23.250.144",
    "local_ip": "10.0.0.78",
    "port": 32148,
    "rest_port": 32149,
    "loc": "37.77986, -122.42905",
    "country": "USA",
    "city": "San Francisco",
    "id": "f3a3c56fcfb78aecc110eb911f35851c",
    "date": "2021-12-28T04:10:14.210574Z",
    "member": 91,
    "ledger": "global"
  }
}
```


Policies are written to the ledger and are available to all the members of the network. The ledger can be hosted on a 
blockchain platform (like Ethereum) or contained in a master node. Regardless of where the blockchain is hosted, every 
node maintains a local copy of the ledger such that when the node needs metadata - it can be satisfied from the local 
copy with no dependency on network connectivity or the blockchain latency. The local copy on a node is organized in a 
json file, The path to the file is represented by the `blockchain_file` variable. Use the following command to see the value 
assigned to the variable: `!blockchain_file`. Optionally, the local ledger can be hosted in a local database. If a 
master node is used, the master node is configured such that the ledger is stored on a local database.

When new policies are added to the ledger, they need to update the global metadata layer (the global copy).
As every node continuously synchronizes the local copy with the global copy, evey update will appear on the local copy 
of every member node. Synchronization is enabled with the `run blockchain sync` command. 
Details are available [here](background%20processes.md#blockchain-synchronizer).  

## The Policy ID
When a Policy is added to the metadata, one of the fields describing the object is an ID field.  
The ID value can be provided by the user or generated dynamically when the policy is added to the ledger.  
Users can specify a unique ID to their policies or, if the value is auto-generated, it is based on the MD5 Hash value of the object.


# Configuration Policies

The AnyLog nodes are configured to provides services to applications and peer members of the network. These services include
data storage, query functionality, integration, security and more.
To provide the services, the nodes in the network can be configured in 2 ways:
1. Using scripts that are assigned to nodes and executed when the nodes are initiated. The configuration options are 
detailed throughout the documentation. 
2. Using configuration policies that are assigned to nodes when nodes are initiated.

This chapter explains Policies based Configuration.

## Assigning a configuration policy to a node 

One or more configuration policies can be assigned to a node as detailed below:     
Usage:
```anylog
config from policy where id = [policy id]
```
Note that any type of policy can be used to configure a node as long as the node is structured as needed.  

## Monitor policies used to configure a node
The following command, executed on a node in the network, returns the list of policies used to configure the node with 
indication if the configuration completed successfully:  
Usage:
```anylog
get config policies
```

## The configuration policy structure

Any type of policy can serve as a configuration policy. This property allows to extend the functionality of existing 
policies by configuration instructions.
For example, as an Operator Policy (an Operator is a node that hosts data) is required to publish IP and Port that
can be used to message the node, it is convenient to leverage the Operator policy as a configuration policy.

To be considered as a configuration policy, the policy needs to include one or two sections which are the following:
1.  A section that details connection information for the networking related services.
2.  A section that details other configuration instructions.

### Configuration of network related services

Configuring the TCP, REST and Message Broker services can be done by specifying the services IPs and Ports in 
the policy.   
Below are the needed attributes for the networking services.

1. **TCP service** - The TCP service makes a node a member of the network. It is equivalent to configure the node using
the command [run tcp server](background%20processes.md#the-tcp-server-process).  
   Attributes required:  
   1. ip – the IP address allowing peer nodes to communicate with the service.
   2. port - the service port.
   3. local_ip – a second IP which can be used to communicate with node (i.e. an IP that identifies the service on a local network). 
      
    If a local_ip is not provided, the service binds to the ip address. if both attributes are provided
    (ip and local_ip), the service would be listening to all messages (regardless of the IP) on the service port.
    To avoid binding, without a dedicated local_ip, assign the IP value to the 2 attributes (ip and local_ip). 
   

2. **REST Service** - The REST service communicates with applications and data generators (like sensors). It is equivalent 
   to configure the node using the command [run rest server](background%20processes.md#rest-requests).   
   Attributes required:  
   1. rest_ip – (optional) an IP that provides a dedicated address for the REST services.
   2. rest_port - the service port.
      
    Note that if an IP is provided, the node binds to the IP, otherwise it will receive all REST based requests on the specified port.

3. **Broker Service** - These services communicate with data generators (like sensors) using Publish-Subscribe functionalities.
   It is equivalent to configure the node using the command [run messsage broker](background%20processes.md#message-broker).   
   Attributes required:  
   1. broker_ip – (optional) an IP that provides a dedicated address for the broker services.
   2. broker_port -the service port.
      
    Note that if an IP is provided, the node binds to the IP, otherwise it will receive all Publish requests on the specified port.

### Example:
The example below defines an Operator policy including the networking services (info contained within greater than and less than signs 
is a code block that can be coppied to the AnyLog CLI).
The insert command adds the policy to the shared metadata layer. When the policy is added, it is updated with a unique ID.

```anylog
<member = {"operator" : {
    "name"  : "operator_2",
    'company' : 'New Company',
    'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2b',
    "ip" : !external_ip,
    "local_ip" : !ip,
    "port" : 7848,
    "rest_port" : 7849,
    "broker_port" :7850
    }
}>

blockchain insert where policy = !member and local = true  and master = !master_node
```
The commands below retrieve the assigned ID and configure the node using **config from policy** command. 

```anylog
policy_id =  blockchain get operator where name = operator2 and ip = !external_ip bring [operator][id]

config from policy where id = !policy_id
```

## Policies Configuration

AnyLog commands can be added to policies and replace or co-exist with configuration scripts.    
Commands in policies are listed with attribute named **script**.  
The command ```config from policy ``` configures the network based services (if detailed) and 
afterwards executes the commands listed in the **script** attribute.

The following policy includes both - the networking services and script commands:

```anylog
<config = {"config" : {
    "name"  : "default_config",
    "ip" : "!external_ip",
    "local_ip" : "!ip",
    "port" : 7848,
    "rest_port" : 7849,
    "broker_port" :7850,
    "script" : [
      "set authentication off",
      "set echo queue on",
      "set anylog home D:/Node"
    ]
    }
}>
```
