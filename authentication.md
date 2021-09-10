# Users Authentication

A set of authentication commands (described in this document) provides the mechanisms to authenticate users and nodes 
within a framework that determines access and permissions to the processes of the network and data maintained by nodes of the network.

Each node in the network is assigned with a public and a private key. 
The public key serves as an identification of the node and can be associated with a permission group.    
A permission group sets a list of permitted operations (such as querying specific databases). 
When a public key is associated with the permission group, the node is assigned with the group permissions.  
The private key signs messages sends from the nodes to peers in the network such that when a message needs to be processed,
the processing node can validate the authentication of the message and determine the authorization assigned by the relevant permission group.

When an external user or application connects to a node in the network, and user authentication is enabled, the node validates the user name and password
against a local list and if validated, the user inherits the permissions provided to the node.  

Use the following command to enable user authentication:
<pre>
set user authentication on
</pre>
Use the following command to disable user authentication:
<pre>
set user authentication off
</pre>
Use the following command to determine if user authentication is enabled:
<pre>
get authentication
</pre>

# Creating a private and a public key for a node in the network

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

# Creating a private and a public key for a user

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
  
  
# Authenticate signature

Authenticate the policy by validating that the policy was signed using the private key associated with the public key on the policy.  
Command:
<pre>
id authenticate [JSON Policy]
</pre> 

Example:
<pre>
id authenticate !json_script
</pre>

# Encrypt and Decrypt messages

When a message is send, the sender can encrypt the message using the public key of the receiver.  
When the message arrives at the receiver, the receiver is able to decrypt the message using his private key.

## Encrypting a message
Command:
<pre>
id encrypt !message !public_key
</pre> 

Example:
<pre>
id encrypt !message !public_key
</pre>


## Decrypting a message
Command:
<pre>
id decrypt [message text] where key = [private key] and password = [password]
</pre> 
If key is not provided, the decryption will apply the private key of the node.

Exampls:
<pre>
id decript !message where key = !private_key and password = !my_password
id decript !message where password = !my_password
</pre>

# Validate permitted command

When a node receives a command from a peer node, the receiving node is using the public key of the peer to validate the authorization of the peer to issue the command.  
Authorization is validated against ***permissions*** policies.  
The receiving node considers the permissions policy to determine that the public key of the peer is represented in a permission policy which is signed by an authorized member.  

Command:
<pre>
id validate where key = [public_key] and command = [command text] and table = [table name] and dbms = [dbms name]
</pre>   
Table and dbms are optional and are used with SQL command.

Example:
<pre>
id validate where key = !public_key and command = copy
id validate where key = !public_key and command = sql and dbms = lsl_demo and table = ping_sensor
</pre>   

# Add users

Users names and passwords are added to each node to only allow connections with permitted users.  
The ***id add user*** command can specify a time frame (expiration) that determines if the user permission is terminated after a period of time.  
Command:
<pre>
id add user where name = [user name] and type = [user type] and password = [password] and expiration = [duration]
</pre>  

Command variables:
| Option        | Explanation  |
| ------------- | ------------| 
| user name  | A unique name to identify the user. |
| user type  | The type of user, i.e. ***admin***. The default value is ***user***. |
| password  | Any character string. |
| expiration  | A time limit that terminates permissions for the user.|
 
If expiration time is specified, the user permission to connect to the node is revoked after the time interval.  
Duration can be specified in seconds, minutes, hours and days.
If expiration is not specified, the user permissions are not limited by time. User can be removed using the ```remove user``` command.

Example:
<pre>
id add user where name = ori and password = 123 and expiration = 2 minutes
</pre>  

# Remove users

A user can be removed with the following command:
<pre>
id remove user where name = [user name]
</pre>   

Example:
<pre>
id remove user where name = john
</pre>  

# Update password

A user can modify his password using the following command:
<pre>
id update user password where name = [user name] and old = [old password] and new = [new password]
</pre>   

Example:
<pre>
id update user password where name = ori and old = 123456 and new = iugsek88ekA
</pre>  

# Authenticating HTTP requests

Nodes in the network can be configured to enable authentication of HTTP REST requests.

## Enabling Basic Authentication in a node in the network

Basic authentication is enabled using the following procedure:

1. On the AnyLog node:  
    a. Provide the [local passoword](#The-local-password) (if was not yet provided) usinf the command: ```set local password = [the local passoword]```   
    b. Enable user authentication using the command: ```set user authentication on```.          
    c. Update the list of permitted users using the command: [id add user](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#add-users).  
2. When the REST call is send, include the following key-value pair to the header:
<pre>
key - "Authorization"  
value - Base64 encoded string of the user name and password separated by a colon.
</pre>

Examples of basic authentication setup on 3rd parties tools:

#### Enabling Basic Authentication in Grafana

On the Data Source connection page:
1. In the ***Auth*** section: Enable ***Basic Auth***.
2. In the ***Basic Auth Details*** section: Add the user name and password.

#### Enabling Basic Authentication in Postman

In the Authorization Tab:  
1, select: ***Basic Auth***.  
2. Update user name and password.


# Using passwords

For authentication of users, members and message encryption, nodes operate with 2 secret passwords:  
1. A local password - enables to encrypt and decrypt sensitive data that is stored on the local file system.  
2. The private key password - enables the usage of the private key to sign policies and authenticate members.   
 
### The local password
The local password is provided using the command:
<pre>
set local password = [password]
</pre>
If a local password was provided to a node, restarting the node requires to re-provide the same password. 
When the password is re-provided, it is validated to determine that it is identical to the initial password.


### The private key password
The private key password is provided using the command:
<pre>
set private password = [password] [in file]
</pre>
[in file] - An optional command text to store the password in an encrypted file protected by the ***local password***.  
If the ***in file*** option is added to the command but the ***local password*** is not set, the ***set private password*** command returns an error.    
If the private password is available, the encrypted password (of the private key) is written to the local file system.

# SSL
To enable SSL connections, you need to determine if you are the designated trusted user (i.e the root user of the network or certificate authority) or a user of AnyLog (i.e. client or server). 

### Setup root user
The root user is responsible for creating and distributing certificates and private key pairs, which will be used to authenticate requests and encrypt messages at REST. 
To create the private key and public certificate of the root user (or certificate authority), run the following command on the AnyLog CLI:
<pre>
id generate certificate authority
</pre>

To generate a public certificate and private key pair, run the following command on the AnyLog CLI:
<pre>
id generate certificate request
id sign certificate request
</pre>

### Setup AnyLog user
Request a certificate and private key pair from the certificate authority.
Deploy AnyLog node with SSL enabled with the following command: 
<pre>
run rest server !ip 2049 where timeout = 0 and threads = 6 and ssl = true
</pre>
