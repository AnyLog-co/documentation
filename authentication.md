# Users Authentication

A set of authentication commands (described in this document) provides the mechanisms to authenticate users and nodes 
within a framework that determines access and permissions to the processes of the network and data maintained by nodes of the network.

Each node in the network is assigned with a public and a private key. 
The public key serves as an identification of the node and can be associated with a permission group.    
A permission group sets a list of permitted operations (such as querying specific databases). 
When a public key is associated with the permission group, the node is assigned with the group permissions.  
The private key signs messages sends from the nodes to peers in the network such that when a message needs to be processed,
the processing node can validate the authentication of the message and determine the authorization assigned by the relevant permission group.

When an external user or application connects to a node in the network, the node validates the user name and passowrd
against a local list and if validated, the user inherits the permissions provided to the node.


# Creating a private and public key for a node

These keys are kept on the node. The public key serves to uniquely identify a node and the private key serves to sign messages send from the node.

Command:
<pre>
id create keys for node where password = [password]
</pre> 

The command creates a public and private key for the node.
The public key serves as an identifier of the node and can be retrieved using the command:
<pre>
get node id
</pre> 
Keys for each node needs to be created only once. Once the keys were created, a new call to ```id create keys for node``` returns an error.


# Creating a private and public key for a user

These keys are provided to a user and managed by the user. 
The public key uniquely identifies the user and the private key allows to sign policies added to the the blockchain by the user.  
When a policy is added to the blockchain, the public key is added to the policy.    
When a policy is processed, these keys allow to validate the following:
1. That the policy was signed by the user associated with the public key.
2. That the user associated with the public key is authorized to sign the policy.



