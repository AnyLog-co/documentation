# Securing the Network

## Overview

The network is secured using 3 mechanisms:
1) Using a 3rd party Overlay Network. An example of an overlay network is [Nebula](https://nebula.defined.net/docs/).
2) Securing the messages transferred between AnyLog nodes using Key-Based Authentication (Public Key Authentication).
3) Securing messages transferred between 3rd parties applications and AnyLog nodes using certificates and passwords.

## Deploying a 3rd party overlay network

The overlay network allows for:
a) Authorize the nodes allowed to participate in the network.
b) Identify the members of the network by unique IP and Port.
c) Resolve network routing issues.
d) Encrypted messaging between the member nodes.

Refer to the 3rd party vendor manual for instalation and configuration instructions.

## Key-Based Authentication

These processes are based on the following processes:  
* Each node is assigned with a private key and a public key^.
* A message from a node to a peer is signed by the private key.
* The peer receiving th message authenticates the sender using the public key.
* If the sender is authenticated, the sender permissions are validated using the relevant policies. 
* If the sender is authenticated, and the message request is permitted, the message will be processed.

^Note: A private key and a public key can be assigned to users - it allows for administrators to operate on the node's CLI
using their assigned permissions which may be less restrictive compared to the permissions assigned to the node.

The relevant AnyLog commands are detailed in the section [Node Authentication](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#node-authentication).  


## Key-Based-Authentication deployment example

The example below demonstrates the following:
a) Assigning keys to nodes and users as needed.
b) Defining the policies that determine user permissions.
c) Assigning nodes and users to the policy that determine their permissions.

### Definitions

Policies
* A member policy - a policy that provides information on a member node or a user. The policy includes the public key assigned to the member.
* A permission policy - a policy that lists permitted and restricted commands and permitted and restricted database tables.
* An assignment policy - a policy that lists one or more members and a permission policy. The assignment determines the permitted operations to the listed members. 
Directories
* keys directory (!id_dir) - a directory that contains keys assigned to different members and are saved on the node.


### Prerequisites and reset

* A network with 2 operators and a master node.  
* No existing permissions and assignment policies.   
* No existing keys assigned to nodes and users.  

Use the following commands to set up each operator node:
<pre> 
set authentication off
master_node = 10.0.0.25:2048        # Replace with the proper address
</pre>

Use the following commands to set up the master node:
<pre> 
set authentication off
connect dbms sqlite !db_user !db_port blockchain
</pre>

Use the following commands to delete all policies on a master node:
<pre> 
run client !master_node "drop table ledger where dbms = blockchain"
run client !master_node "create table ledger where dbms = blockchain"
run client !master_node "blockchain delete local file"
</pre>

Use the following command to delete the local blockchain file on each operator node:
<pre> 
blockchain delete local file
</pre>

Use the following commands to delete existing issued keys on each node:
<pre> 
system del !id_dir/*.* /q      # Windows
system rm !id_dir/*.*          # linux
</pre>

### Validate policy structure
Policies are represented in JSON structure.  
When a variable name is assigned with a policy, the policy info is presented on the CLI when the variable name is prefixed with  
exclamation point (like: ***!member*** when "member" is the variable name).  
The command ***json*** presents the policy on the CLI only if the policy is in correct JSON structure.  
For example:
<pre> 
json !member
</pre>
Adding the keyword test, returns ***true*** if the structure is correct, otherwise ***false*** is returned.
<pre> 
json !member test
</pre>

### Comments
This demo is executed on the CLI of the 2 operators.  
* When a command is executed on operator 1 it is designated by CLI(opr.1).
* When a command is executed on operator 2 it is designated by CLI(opr.2).
* When a command is executed on operator 1 and 2 it is designated by CLI(opr.1.2).


## The demo steps
The demo is using 2 operator nodes and 2 users (root user and a non-root user). Each node and user is assigned with keys.
Each node and user are associated with member policies. Each member policy is assigned with permission policy such that 
each node and member are associated with permissions. Relevant policies are signed such that it is possible to authenticate
the senders of messages and determine the permissions.

The following chart details the processes demonstrated:  

| Step | Node         | Process         | Details       |
| -----| ------------ | --------------- | ------------- |
| 1    | CLI(opr.1)   |Root user keys   | Generate keys for the root user  |
| 2    | CLI(opr.1)   |Root user policy  | Create a policy for a root user, this policy provides the permissions to all members (nodes and users)  |
| 3    | CLI(opr.1.2) |Node Keys  | Generate keys to the operator nodes  |
| 4    | CLI(opr.1.2) |Node member policy  | Create member policies to the operator nodes  |
| 5    | CLI(opr.1)   |User keys  | Generate keys to a user which is not a node  |

### Step 1 - Generate keys for the Root User

<pre> 
id create keys where password = abc and keys_file = root_keys
</pre>
 
A file (name root keys) with the public and encrypted private key is created in the keys' directory (!key_dir).  
These are the keys of the root user. If a file name is not specified, the keys would be presented on the monitor, and the
user is responsible to store and protect the keys.

### Step 2 - Root user policy

This policy can include any information which is representative of the root user. The only required attributes are:
* type - with the value "root"
* public_key - with the public key of the root user. Note that the public key is added when the policy is signed (as in the example below).

In the example, we add a name (rachel) to the policy. It allows to reference the policy by the name, however, ***name*** is not a required attribute.
 
```<pre> 
<member = {"member" : {  
    "type" : "root",  
    "name"  : "rachel"  
    }  
}>  
private_key = get private key where keys_file = root_keys
member = id sign !member where key = !private_key and password = abc
json !member    # View the policy including the signature and public key
blockchain insert where policy = !member and local = true  and master = !master_node
```  

### Step 3 - Generate keys to nodes

Generate keys to the 2 operator nodes.  

Use CLI(oper.1) to generates keys to operator #1:
<pre> 
id create keys for node where password = opr001
</pre>

Use CLI(oper.2) to generates keys to operator #2:
<pre> 
id create keys for node where password = opr002
</pre>

### Step 4 - Create member policies to the operator nodes

Create a member policy to the 2 operator nodes.

Use CLI(oper.1) to create the member policy of operator #1:
```
<member = {"member" : {
    "id"   : "node_001",
    "type" : "node",
    "company"  : "Northern Light",
    "name" : "server south"
    }
}>
member = id sign !member where password = opr001
!member
blockchain insert where policy = !member and local = true  and master = !master_node
```
Use CLI(oper.2) to create the member policy of operator #2:
```
<member = {"member" : {
    "id"   : "node_002",
    "type" : "node",
    "company"  : "Northern Light",
    "name" : "server north"
    }
}>
member = id sign !member where password = opr002
!member
blockchain insert where policy = !member and local = true  and master = !master_node
```