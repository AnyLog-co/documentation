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