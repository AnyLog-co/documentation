# Users and nodes Authentication, making the data secure

A set of authentication commands (described in this document) provides the mechanisms to authenticate users, nodes, messages and policies.  
For a detailed demo setup of a secured network refer to the document [Securing the Network](examples/Secure%20Network.md).   
These commands detailed in this document facilitate a framework that provides the following functionality:  
a) Authenticates messages send from nodes to peer nodes.  
b) Authenticates messages which are sent from nodes to peers with privileges assigned to users.  
c) Determines permissions to the processes of the network and data maintained by nodes of the network.  
d) Validates policies by authenticating their authors and their assigned permissions (see section [adding policies to the blockchain](#adding-policies-to-the-blockchain) below.  
e) Encrypt and decrypt commands and data transferred in the network.  

The network provides 2 layers of authentications:
1) Node Authentications - These are processes to authenticate users and processes delivering messages from one node to another
   and authenticate policies registered on the blockchain.  
   The messages that are authenticated are using the TCP server processes and related calls. 
   Details on the TCP based processes are available in the [TCP Server process](background%20processes.md#the-tcp-server-process) section.
   Message Authentication is based on issuing a private key and a public key to nodes and users. Messages are signed by the private 
   key of the sender (a user or a node) and validating the senders, at the destination nodes, using their public key and 
   policies providing the authorized functionalities.
   Policies are authenticated by validating the policies authors' permissions to create the policies.
   
2) User Authentication - These are processes to authenticate users and processes delivering messages from external applications 
   and users that are not members of the network.  
   For example:
   * Grafana calls issuing a REST request to a node in the network.
   * cURL request to a node in the network.
   Details on REST requests are available in the [REST requests](background%20processes.md#rest-requests) section.
   Authentication is based on one of the following methods:
   * Usernames and passwords that are kept on the destination node.
     Details are available [below](#users-authentication)
   * Issuing client certificate and validating the signature with policies providing the authorized functionalities. 
    Details are available [below](#using-ssl-certificates).
    
Enabling and disabling authentication (both - node authentication and user authentication) is done using the following command:
```anylog
set authentication [on/off]
```
Note:
* Optionally, node authentication can be enabled using `set node authentication` detailed [below](#node-authentication).
* Optionally, user authentication can be enabled using `set user authentication` detailed [below](#add-users).

The following command determines how the node is configured:  
```anylog
get authentication
```

## Encrypting network messages   
AnyLog provides the mechanisms to encrypt messages transferred over the network.
The messages are encrypted using the public key of the receiver and decrypted by the receiver with the private key.
These processes are detailed [below](#encrypt-and-decrypt-messages).

# Passwords
Private keys and sensitive information can be kept outside the node and provided when needed.  
Or users can issue passwords to protect sensitive information that is kept on the node (like private keys and users' passwords).
Each node can be assigned 2 types of passwords:
1. A local password - enables the encryption and decryption of sensitive data that is stored on the local file system.  
2. The private key password - enables the usage of the private key to sign policies and authenticate members.   
 
## The local password
A password is used to encrypt the node's sensitive information. This password is used to encrypt data saved in files on the node.
This encryption is using a random salt key. This password is provided using the command `set local password`, and the 
password is not stored on a local file - it needs to be provided whenever the node starts. 
If a local password was provided to a node, restarting the node requires re-providing the same password. 
When the password is re-provided, it is validated to determine that it is identical to the initial password.
Usage:
```anylog
set local password = [password]
```
      
## The private password
A password protects the node's private key. This password is provided using the command `set private password` and 
can be optionally stored in a local file and protected by the node's [local password](#the-local-password).  
Usage:
```anylog
set private password = [password] [in file]
```
_in file_ are optional keywords. If provided, the password protecting the node's private key will be stored in 
a local file, and the private key will be available to all processes that need the private key 
(assuming that the node's local password is available).
If _in file_ is specified, the password is provided once and is available on the node afterwards. Otherwise,
users need to call `set private password` whenever the node is starting.    
Note: the key is protected using the [local password](#the-local-password).


# Node Authentication

Members participating in the network are assigned a public and a private key.  
The public key uniquely identifies the member and its privileges, and the private key signs the outgoing messages such
that the member can be authenticated by the node receiving the message.
 
The following examples enable and disable node authentication:
```anylog
set node authentication on
set node authentication off
```


## Creating private and public keys 

A private key and a public key are issued for each node that is a member of the network. The public key is assigned with 
privileges (see the [assignment policy](...) below) that determine if a command sent from the node to a peer can be executed on the peer node.
In addition, users can be issued with a private and a public key. Setting users with keys assigns privileges to individual 
users such that, when a user is issuing commands to peer nodes, the privileges granted to the user determine if a command is
processed, rather than the privileges granted to the node.  
For example, an administrator can issue a command and use the administrator privileges when the command is executed on a peer member
rather than being rejected if the node's privileges (the privileges of the node from which the command is executed) are not sufficient to allow processing.

### Creating keys for a node in the network

The command `id create keys for node` creates a private and a public key. These keys are kept on the node, 
and the private key is encrypted using the password. 

Command:
```anylog
id create keys for node where password = [password]
``` 

The public key serves to uniquely identify a node, and the private key serves to sign messages sent from the node.  
The public key can be retrieved using the command:
```anylog
get node id
```

In addition, policies added to the blockchain include the public key of the node and a signature. Prior to executing
a policy by a node in the network, the node executing the policy validates that the policy was signed using the 
private key of the holder of the public key contained in the policy. If the signature is validated, the node executing
the policy needs to determine that the author of the policy has the permissions to create the policy, and only afterwards,
the policy is considered by the node.

Notes:  
* Keys for each node need to be created only once. Once the keys were created, a new call to ```id create keys for node``` returns an error.
* Both the public key and the encrypted private key are stored in a file called _node_id.pem_.

### Creating keys for users in the network

Users issuing commands on the AnyLog CLI, can be assigned a private and public key, and the public key uniquely identifies the user.

Users can use their assigned keys to:   
a) Send messages to nodes in the network.
b) Sign policies added to the blockchain by the user.

**Command**:
```anylog
id create keys for node where password = [password] and keys_file = [file path and name]
```

Providing a key file is optional.
**Examples**:
```anylog
id create keys for node where password = my_password  
id create keys for node where password = my_password and keys_file = !usb_path/my_keys
```

The command creates a public and private key.      
If a file name is provided, the keys are stored in the file.        
The file location can be on a detached drive, like a USB, such that the user is able to physically secure the keys.    
If a file name is not provided, the keys are displayed on the screen, and the user needs to copy and secure the keys.  
If only a file name is provided (without a path), the file is written to the AnyLog keys directory. The location of the directory can be found with the command ```!id_dir```.

### Retrieving the keys

The following commands retrieve the private key and public key of the node:
```anylog
get private key  
get public key
```

Users can retrieve the keys without the headers and new lines using the following commands:

```anylog
get private string  
get public string
```

The following commands retrieve the private key and public key from a PEM file: 
```anylog
get private key where keys_file = [path and file name] 
get public key where keys_file = [path and file name]
```

**Note**:
* If the path is not specified, it is assumed to be !id_dir.
* If no file type is specified, it is assumed to be 'pem', and the file name is extended to include the type.  

**Examples**:
```anylog
get private key where keys_file = roy
get public key where keys_file = !pem_dir/server-acme-inc-public-key
```

users can retrieve the keys without the headers and new lines using the following commands:
```anylog
get private string where keys_file = [path and file name] 
get public string where keys_file = [path and file name]
```


## Adding policies to the blockchain
When a policy is added to the blockchain, the public key is added to the policy.    
When a policy is processed, these keys allow for validation of the following:
1. The policy was signed by the user associated with the public key.
2. The user associated with the public key is authorized to sign the policy.

## Permission Group
The public key serves as an identification of the node and can be associated with a permission group.    
A permission group is declared using a permission policy. The policy sets a list of permitted operations (such as querying specific databases).  
The ```get permissions``` commands show the details of one or more permission policies.  
Usage:
```anylog
get permissions where [attribute name] = [attribute value]
```
Examples:
```anylog
get permissions
get permissions where name = "application basic permissions"
```
Nodes and users are represented by their public key, when a public key is associated with the permission group, 
the node or user is assigned to a group permissions.  
The private key signs messages sent from the nodes to peers in the network, such that when a message needs to be processed,
the processing node can authenticate the message and determine the authorization assigned by the relevant permission group.  

The command ***get member permissions*** returns the permissions of a member (a node or a user).   
If the public key is not included in the where condition, the permissions assigned to the current node are returned.  
The where condition retrieves the Member Policy that satisfies the condition, and the permissions assigned to the policy are returned.     
Usage:
```anylog
get member permissions
get member permissions where [attribute name] = [attribute value]
```

Examples:
```anylog
get member permissions
get member permissions where public_key = !public_key
get member permissions where name = value
```
Notes: 
* The where conditions are applied on the member policy, and the permissions retrieved represent the permission policy assigned to the member.
* If a signatory is assigned to the node, the command **get member permissions** (without _where_ condition) returns the permissions of the signatory.

## Signing a policy

Users and nodes can publish policies on the blockchain.  
If authentication is enabled, the policies are signed by the ***id sign*** command, and the policies are updated with the public 
key and the signature of the publisher such that the publisher can be authenticated, and their authorization can be validated.    
 
**Command options**:
```anylog
id sign [JSON Policy] where key = [private key] and password = [password]
id sign [JSON Policy] where password = [password]
```

If _id sign_ assigns the results to a variable, the variable value is the signed message.  
If _id sign_ does not assign the results to a variable, the value of the variable is provided by the policy changes.
**Examples**:
```anylog
id sign !json_script where key = !my_key and password = my_password
id sign !json_script where password = my_password
```
  
  
## Authenticate signature

Authenticate the policy by validating that the policy was signed using the private key associated with the public key on the policy.  
**Command**:
```anylog
id authenticate [JSON Policy]
```

**Example**:
```anylog
id authenticate !json_script
```


# Validate permitted command

When a node receives a command from a peer node, the receiving node uses the public key of the peer to validate the authorization of the peer to issue the command.  
Authorization is validated against ***permissions*** policies.  
The receiving node considers the permissions policy to determine that the public key of the peer is represented in a permission policy that is signed by an authorized member.  

**Command**:
```anylog
id validate where key = [public_key] and command = [command text] and table = [table name] and dbms = [dbms name]
```

Table and dbms are optional and are used with SQL commands.

**Example**:
```anylog
id validate where key = !public_key and command = copy
id validate where key = !public_key and command = sql and dbms = lsl_demo and table = ping_sensor
```

# Setting the signatory
If node authentication is enabled, messages and policies are signed by the node's private key and identified by the node's public key.  
Users can use a different private key to sign messages and policies. In this case, the associated public key identifies the message and policy.  
This option is used to allow users with higher permissions, to leverage their assigned permissions when operating on a node.  
The following commands replace the signatory on a node, revert to allow the node to be the signatory, and validate the signatory name:  

## Assign a signatory
**Usage**:
```anylog
set signatory where key = [private key] and password = [password] and name = [signatory name]
```

**private key** is the encrypted private key of the signatory.      
**password** is the private key password.    
**name** is a name assigned to the signatory. The name can be any string, excluding "node", which is the signatory name when the node's keys are used.

## Revert to the node as the signatory
**Usage**:
```anylog
reset signatory
```

This command sets the node as the signatory such that messages and policies would be signed by the private key assigned to the node.

## Get the signatory name
Usage:
```anylog
get signatory name
```

Return the **signatory name**. If the node is the signatory, the string "node" is returned. If no signatory is assigned,
the message "No signatory assigned" is returned.


# Encrypt and Decrypt messages

When a message is sent, the sender can encrypt the message using the public key of the receiver.  
When the message arrives at the receiver, the receiver is able to decrypt the message using his private key.

## Encrypting a message
**Command**:
```anylog
id encrypt !message !public_key
```

Example:
```anylog
id encrypt !message !public_key
```


## Decrypting a message
**Command**:
```anylog
id decrypt [message text] where key = [private key] and password = [password]
```

If key is not provided, the decryption will apply the private key of the node.

**Examples**:
```anylog
id decript !message where key = !private_key and password = !my_password
id decript !message where password = !my_password
```

# Users Authentication

## Add users

When an external user or application connects to a node in the network, and user authentication is enabled, the node validates the username and password
against a local list and if validated, the user inherits the permissions provided to the node.  

Use the following command to enable user authentication:
```anylog
set user authentication on
```

Use the following command to disable user authentication:
```anylog
set user authentication off
```

Use the following command to determine if user authentication is enabled:
```anylog
get authentication
```
Note: Node authentication is detailed [above](#node-authentication).


Users' names and passwords are added to each node to only allow connections with permitted users.  
The **id add user** command can specify a time frame (expiration) that determines if the user's permission is terminated after a period of time.  
**Command**:
```anylog
id add user where name = [user name] and type = [user type] and password = [password] and expiration = [duration]
```

**Command Variables**:

| Option        | Explanation  |
| ------------- | ------------| 
| user name  | A unique name to identify the user. |
| user type  | The type of user, i.e. ***admin***. The default value is ***user***. |
| password  | Any character string. |
| expiration  | A time limit that terminates permissions for the user.|
 
If the expiration time is specified, the user's permission to connect to the node is revoked after the time interval.  
Duration can be specified in seconds, minutes, hours, and days.
If expiration is not specified, the user permissions are not limited by time. The user can be removed using the ```remove user `` command.

**Example**:
```anylog
id add user where name = ori and password = 123 and expiration = 2 minutes
```

## Remove users

A user can be removed with the following command:
```anylog
id remove user where name = [user name]
```

**Example**:
```anylog
id remove user where name = john
```

## Update password

A user can modify their password using the following command:
```anylog
id update user password where name = [user name] and old = [old password] and new = [new password]
```

**Example**:
```anylog
id update user password where name = ori and old = 123456 and new = iugsek88ekA
```

## Authenticating HTTP requests

Nodes in the network can be configured to enable authentication of HTTP REST requests.

### Enabling Basic Authentication in a node in the network

Basic authentication is enabled using the following procedure:

1. On the AnyLog node:  
    a. Provide the [local password](#The-local-password) (if it was not yet provided) using the command: ```set local password = [the local passoword]```   
    b. Enable user authentication using the command: ```set user authentication on```.          
    c. Update the list of permitted users using the command: [id add user](authentication.md#add-users).  
2. When the REST call is sent, include the following key-value pair in the header:
```anylog
key - "Authorization"  
value - Base64 encoded string of the user name and password separated by a colon.
```

Examples of basic authentication setup on 3rd parties tools:

#### Enabling Basic Authentication in Grafana

On the Data Source connection page:
1. In the _Auth_ section: Enable _Basic Auth_.
2. In the [_Basic Auth_ Details](#enabling-basic-authentication-in-a-node-in-the-network) section: Add the username and password.

#### Enabling Basic Authentication in Postman

In the Authorization Tab:  
1, select: _Basic Auth_.  
2. Update username and password.


# Using SSL Certificates

Nodes that are not members of the network (called servers in the description below) interacting with the network can be authenticated by the AnyLog nodes using _users_ certificates.  
An example is a Grafana node using [Client Certificate](https://grafana.com/docs/grafana/latest/administration/configuration/#client_cert_path)
which is delivered to the AnyLog node with the query requests.  
In addition, the participating AnyLog nodes are issued with Signed Certificate Requests such that a server that is not a member of the network
can authenticate the nodes using the Certificate Authority's public key.

### The process with SSL certificate is based on the [X.509](https://en.wikipedia.org/wiki/X.509#Structure_of_a_certificate) standard and is the following:  
* The root user of the network or a designated user is treated as a Certificate Authority (CA).
* A server (a node which is not a member of the network) is provided with a Certificate Request (CR).
* The AnyLog CA validates the identity of the server, and if validated, signs the CR. This process provides
  the server a signed certificate and a private key to sign messages delivered to the AnyLog Node.

Notes:  
    1) When the certificate commands are issued, different files are generated. These files are written to the location assigned to the `pem_dir` variable (by default to the `AnyLog-Network/data/pem` directory).
        To view the location assigned to the `pem_dir` variable, issue `!pem_dir` on the AnyLog CLI.   
    2) [org] in the file name is a key based on the organization name provided in the command line (value assigned to the key org whereas spaces are replaced with hyphen character).

## Setup the CA
The root user is responsible for creating and distributing certificates and private key pairs, which will be used to authenticate requests and encrypt messages at REST. 
To create the private key and public certificate of the root user (or Certificate Authority), run the following command on the AnyLog CLI:
```anylog
id generate certificate authority where [command options]
```

The command options:

| Option        | Explanation  |
| ------------- | ------------|
| password  | A password to protect the CA private key. |
| country  | The [two-letter ISO code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) for the country where your organization is located. |
| locality  | Province, region, county, or state (e.g. West Sussex, Normandy, New Jersey). |
| state  | Town, city, village. |
| org  | Organization name.|
| hostname  | The URL representing the CA.|

Example:
```anylog
id generate certificate authority where country = US and state = CA and locality = "Redwood City" and org = AnyLog and hostname =  anylog.co
```

When the command is issued 2 files are generated:  

| Type        | Name  | Explanation |
| ------------- | ------------| ---- |
| .key  | ca-[org]-private_key | The Private Key for the CA |
| .crt  | ca-[org]-public_key | The Public Key for the CA. It will be provided to every AnyLog node that authenticates non-member nodes with CR signed by the AnyLog CA |


## Generating a certificate request

A server that is not a member of the AnyLog network is represented by a Certificate Request (CR) and a Private Key.
Use the following command to generate a certificate request:
```anylog
id generate certificate request where [command options]
```

The command options:

| Option        | Explanation  |
| ------------- | ------------|
| password  | A password to protect the generated private key. |
| country  | The [two-letter ISO code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) for the country where your organization is located. |
| locality  | Province, region, county or state (e.g. West Sussex, Normandy, New Jersey). |
| state  | Town, city, village. |
| org  | Organization name.|
| alt_names  | An extension to the X.509 specification that allows specifying additional host names for a single SSL certificate.|
| hostname  | The URL representing the node that issues the CR.|
| ip  | The IP of the node that issues the CR.|

Example:
```anylog
id generate certificate request where country = US and state = CA and locality = "Redwood City" and org = "Acme Inc" and alt_names = 127.0.0.1 and hostname =  acme.co and ip = "192.56.76.4"
```

When the command is issued 2 files are generated:  

| Type        | Name  | Explanation |
| ------------- | ------------| ---- |
| .key  | server-[org]-private_key | The Private Key for the requesting server. |
| .csr  | server-[org]-csr | A CR representing the server. |
| .pem  | server-[org]-public_key | The Public Key for the requesting server. This key is updated in the shared metadata layer to determine permissions.|


## Signing a certificate request

To allow an AnyLog node to authenticate the server, the CA signs the CR using the following command:

```anylog
id sign certificate request where [command options]
```

The command options:

| Option        | Explanation  |
| ------------- | ------------|
| ca_org  | The organization name of the CA. |
| server_org  | The organization name of the server associated with the CR. |

Example:
```anylog
id sign certificate request where ca_org = AnyLog and server_org = "Acme Inc"
```

When the command is issued 1 file is generated:  

| Type        | Name  | Explanation |
| ------------- | ------------| ---- |
| .crt  | server-[org]-public-key | The Signed Certificate Request. |


## Generating and signing a certificate request to the AnyLog node

The following example generates generate certificate request for the AnyLog node.

```anylog
id generate certificate request where country = US and state = CA and locality = "Palo Alto" and org = "Node 128" and alt_names = 127.0.0.1 and hostname =  anylog.co and ip = "192.38.78.8"
```

Signing the CR using the CA private key:
```anylog
id sign certificate request where ca_org = AnyLog and server_org = "Node 128"
```

## Summary of the example files
With the examples described above, the following files were generated:


| File Name        | Explanation  |
| ------------- | ------------|
| ca-anylog-private-key.key  | The private key of the CA. |
| ca-anylog-public-key.crt  | The public key of the CA. |
| server-acme-inc-csr.csr  | The non-signed CR of the server (Acme Inc). |
| server-acme-inc-private-key.key  | The private key key of the server (Acme Inc). |
| server-acme-inc-public-key.crt  | The signed certificate request of the server (Acme Inc). |
| server-acme-inc-public-key.pem  | The public key of the server (Acme Inc). It is represented in the metadata to determine the permissions. |
| server-node-128-csr.csr  | The non-signed CR of the AnyLog node (Node 128). |
| server-node-128-private-key.key  | The private key key of the AnyLog node (Node 128). |
| server-node-128-public-key.pem  | The public key associated with the private key (Node 128). |
| server-node-128-public-key.crt  | The signed certificate request of the AnyLog node (Node 128). |


## Setup the AnyLog Node and the connecting Server

### Setup the AnyLog node

Make the following files available in the _pem_ directory:
1) The Public Key of the CA: ca-[org]-public_key.crt (using the example files: ca-anylog-public-key.crt)
2) The Private Key of the AnyLog Node: server-[org]-csr.csr  (using the example files: server-node-128-private-key.key)
3) The Signed CR of the AnyLog Node: server-[org]-public-key.crt  (using the example files: server-node-128-public-key.crt)


Deploy AnyLog with SSL enabled using the following command: 
```anylog
run rest server !ip !rest_port where timeout = 0 and threads = 6 and ssl = true and ca_org = AnyLog and server_org = "Node 128"
```

Use the following command to retrieve the REST server configuration:
```anylog
get rest server info
```


### Setup the Server (Client Side)

The client is configured using the following files:
1) The Public Key of the CA: ca-[org]-public_key.crt (using the example files: ca-anylog-public-key.crt)
2) The Private Key of the server: server-[org]-csr.csr  (using the example files: server-acme-inc-private-key.key)
3) The Signed CR of the server: server-[org]-public-key.crt  (using the example files: server-acme-inc-public-key.crt)

An example of Postman configuration is available at [using postman](using%20postman.md#how-too-use-postman-as-the-query-interface).
