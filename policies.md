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

New policies are added to the ledger, and when a new policy is added, it updates the global metadata layer (the global copy).
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
   4. tcp_threads - the number of threads supporting the service (the default number is 6).
      
    If a local_ip is not provided, the service binds to the ip address. if both attributes are provided
    (ip and local_ip), the service would be listening to all messages (regardless of the IP) on the service port.
    To avoid binding, without a dedicated local_ip, assign the IP value to the 2 attributes (ip and local_ip). 
   

2. **REST Service** - The REST service communicates with applications and data generators (like sensors). It is equivalent 
   to configure the node using the command [run rest server](background%20processes.md#rest-requests).   
   Attributes required:  
   1. rest_ip – (optional) an IP that provides a dedicated address for the REST services.
   2. rest_port - the service port.
   3. rest_threads - the number of threads supporting the service (the default number is 5).
      
    Note that if an IP is provided, the node binds to the IP, otherwise it will receive all REST based requests on the specified port.

3. **Broker Service** - These services communicate with data generators (like sensors) using Publish-Subscribe functionalities.
   It is equivalent to configure the node using the command [run messsage broker](background%20processes.md#message-broker).   
   Attributes required:  
   1. broker_ip – (optional) an IP that provides a dedicated address for the broker services.
   2. broker_port -the service port.
   3. msg_threads - the number of threads supporting the service (the default number is 6).
      
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

## Policies based Configuration

AnyLog commands can be added to policies and replace or co-exist with configuration scripts.    
Commands in policies are listed with attribute named **script**.  
The command ```config from policy ``` configures the network based services (if detailed) and 
afterwards executes the commands listed in the **script** attribute.

The following policy includes both - the networking services and script commands:

```anylog
<config_policy = {"config" : {
    "name"  : "default_config",
    "ip" : !external_ip,
    "local_ip" : !ip,
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

# Creating policies

Policies are JSON structures that represent logical and physical objects which are stored on the shared metadata.   
Their only structural requirement is that the root of the JSON is with a single key.
For example, members of the network, security rules, table definitions are represented as policies.  
Users and processes can create policies and using a simple API, the policies can be written to the shared metadata layer
or retrieved from the shared metadata layer. 
The (single) root key in a policy is the 'policy type', it allows identifying and classifying policies by their type and facilitates
search where query and filtering processes are assigned to a group of policies identified by their type.

Adding and retrieving policies from the shared metadata layer is described in the [Blockchain Commands](blockchain%20commands.md#blockchain-commands) section.
 
## Declaring a policy using a code block

Using a code block, users can describe a policy on the [AnyLog Command Line (CLI)](getting%20started.md#anylog-command-line-interface).  
The code block assigns a policy to a key, is contained between less than and greater than signs and can be copied to the AnyLog CLI.  
When the copy is done, the key is assigned with the policy and maintained in the [local dictionary](getting%20started.md#the-node-dictionary).

Using the code block example [above](#policies-based-configuration), when the code block is copied to the CLI, the policy is assigned to the key ```config_policy```.
This process updates the node's dictionary with the key and value such that the value (policy) can be referenced using the key (see the examples below).

Note that some attribute names in the policy are associated with dictionary values. For example, the attribute name
```ip``` is assigned with ```!external_ip``` as its value. When the policy is written to the metadata, the dictionary keys
are replaced with their assigned values.

## Creating policies using the Create Policy command

The **create policy** command provides a command option to declare policies and include default attributes and values 
that are required in the policy.  
Usage:
```anylog
create policy [policy type] [with defaults] where [key value pairs]
```
**policy type** - The type of the policy created (i.e.: master, operator, query, publisher).  
**with defaults** - Optional keywords to include the default attributes (if not specified in the list of key values pairs).  
**key value pairs** - A list of key (equals) value pairs, separated with the _"and"_ keyword.

Example:

```anylog
create policy operator with defaults where name = operator_name and company = my_company and city = "San Francisco" and country = "USA" and cluster = !cluster_id
```
The command above returns the following policy:
```anylog
     {'operator' : {'company' : 'my_company',
               'city' : 'San Francisco',
               'country' : 'USA',
               'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a',
               'name' : 'my_company-operator-1',
               'ip' : '73.202.142.172',
               'internal_ip' : '10.0.0.78',
               'port' : 32148,
               'rest_port' : 32149,
               'member' : 175}}
```
A complete process may have the following sequence:
1. Retrieve the IP and Port of the Master node.
2. Retrieve the ID of the data cluster that is assigned to the new Operator.
3. Create the new Operator policy.
4. Add the policy to the metadata.

An example of a process that creates and adds the policy to the metadata is as follows:
```anylog
master_node = blockchain get master bring.ip_port
cluster_id = blockchain get cluster where name = cluster_1 bring.first [cluster][id]
new_policy = create policy operator with defaults where company = my_company and city = "San Francisco" and country = "USA" and cluster = !cluster_id
blockchain insert where policy = !new_policy and local = true and master = !master_node 
```

## Retrieving policies from the dictionary

The value assigned to a key in the dictionary is retrieved by providing the attribute name prefixed with exclamation point 
or optionally using the command ```get```.     
Each of the following 2 commands on the CLI return the value assigned to the key ```config_policy```:

```anylog
!config_policy
get !config_policy
```

The command ```json``` followed by the key (prefixed with exclamation point) does the following:
1. It replaces the keys in the policy with their associated values.
2. It validates that the policy is formatted correctly (orherwise an empty string is returned).

Example:
```anylog
json !config_policy
```
Returns:
```anylog
{'config' : {'name' : 'default_config',
             'ip' : '73.222.38.83',
             'local_ip' : '10.0.0.78',
             'port' : 7848,
             'rest_port' : 7849,
             'broker_port' : 7850,
             'script' : ['set authentication off',
                         'set echo queue on',
                         'set anylog home D:/Node']}}

```
Note that the value assigned to the key ```ip``` is set to be 73.222.38.83 which is the dictionary value assigned 
to the key ```external_ip```.

The **json** command is detailed in the section [Transforming JSON representatives to JSON Objects](json%20data%20transformation.md#transforming-json-representatives-to-json-objects).

## Retrieving and formatting attributes from policies

Using the **from** command it is possible to retrieve and format attributes of a policy or of multiple policies.  
The following example retrieves the name, IPs and Port from the config policy to a table format.

```anylog
from !config_policy bring.table [config][name] [config][ip] [config][local_ip] [config][port]
```

The **from** command is detailed in the section [The 'From JSON Object Bring' command](json%20data%20transformation.md#the-from-json-object-bring-command).

## Declaring a policy using set commands

The **set policy** command creates and updates a policy dynamically.  

Usage:
```anylog
set policy [policy name] [one or more key value pairs]
```

The policy name represents the key in the dictionary, and the key value pairs assign values to policy.

The example below dynamically defines a policy identical to the code block example [above](#policies-based-configuration).   

```anylog
set policy config_policy [config] = {} and [config][name] = default_config 
set policy config_policy [config][ip] = !external_ip and [config][local_ip] = !ip 
set policy config_policy [config][port] = 7848 and [config][restport] = 7849 and [config][broker_port] = 7850
set policy config_policy [config][script] = []
set policy config_policy [config][script] + 'set authentication off' and [config][script] + 'set echo queue on' and [config][script] + 'set anylog home D:/Node'
```

Notes:
1. The policy attribute values can be assigned in a single command or using multiple **set policy** commands
that reference the same policy name (```config_policy``` in the example above). This property allows to condition the 
assignment with **if** conditions (details are available in the [conditional execution](anylog%20commands.md#conditional-execution) section.
2. A dictionary is assigned to a key using the signs: {}
3. A list is assigned to a key using the sign: [] and entries are added to the list using the plus (+) sign as in the example above.
4. Removing entries from the local dictionary is by assigning a null string to the key in the dictionary. The example below 
   removes the policy from the local dictionary:
   ```anylog
   config_policy = ""
   ```


## ANMP Policy
The AnyLog Network Management Policy (ANMP) are used to modify existing policies. 

The key is a policy ID, the value are attribute names and values that are modified.

**Example**: Map Hostname to IP by modifying the policy
0. Declare Operator - this step is already done as part of the deployment 
```anylog
cluster_id = blockchain get cluster where name = cluster_1 bring.first [cluster][id]

<operator_policy={'operator': {
   'hostname' : !hostname,
   'name' : !node_name',
   'ip': !ip,
   'company':  !company_name,
   'port': !anylog_server_port.int,
   'rest_port': !anylog_rest_port.int,
   'cluster': !cluster_id
}}>


blockchain insert where policy = !operator_policy and local = true and master = !ledger_conn 
```

1. Get the policy ID of the Operator policy
```anylog 
policy_id = blockchain get operator where name=my_operator and company=AnyLog bring [operator][id]
```

2. Replace update the node to include **both** public and private IP addresses. 
```anylog 
<anmp = {"anmp" : {
   !policy_id : {
      "ip" : !external_ip,
      "local_ip": !ip      
   }
}}>

blockchain insert where policy = !anmp and local = true and master = !master_node
```

## Compare Policies

Policies can be compared to determine the different attribute and values.  
The following command returns a report indicating the differences between the two policies, or between lists of policies.  
Usage:
```anylog 
get policies diff [object 1] [object 2]
``` 
Object 1 and Object 2 are policies or lists of policies to compare. 
When lists are compared, the number of policies in the lists needs to be equal with one exception: 
If a policy is compared to a list with a single policy, the policy is assumed to be in a list, and the comparison is allowed.  
Example:
```anylog 
get policies diff !policy1 !policy2
```

