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

Command:
<pre>
id create keys for node where password = [password] and keys_file = [file path and name]
</pre> 

Providing a key file is optional.
Examples:
<pre>
id create keys for node where password = my_password  
id create keys for node where password = my_password and keys_file = !usb_path/my_keys
</pre> 

The command creates a public and private key.      
If a file name is provided, the keys are stored in the file.        
The file location can be on a detached drive like a USB such that the user is able to physically secure the keys.    
If a file name is not provided, the keys are displayed on the screen and the user needs to copy and secure the keys.  
If only a file name is provided (without a path), the file is written to the AnyLog keys directory. The location of the directory can be found with the comand ```!id_dir```.

  
# Signing a policy

Users and nodes can publish policies on the blockchain.  
Using the ***id sign*** command, these policies are updated with the public key and the signature of the publisher such that the publisher can be authenticated and his authorization can be validated.    
If the private key is not provided, the policy would be signed by the private key assigned to the node.    

Command options:
<pre>
id sign [JSON Policy] where key = [private key] and password = [password]
id sign [JSON Policy] where password = [password]
</pre> 

If ***id sign*** assigns the results to a variable, the variable value is the signed message.  
If ***id sign*** does not assign the results to a variable, the value of the variable providing the policy changes.
Examples:
<pre>
id sign !json_script where key = !my_key and password = my_password
id sign !json_script where password = my_password
</pre>
  





