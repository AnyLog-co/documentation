# AnyLog Authentication 

The following provides insight into utilizing authentication. For a detailed explanation of how authentication works, 
visit [authentication](../../authentication.md) document.  

## Basic Authentication

The basic authentication requires a username and password when accessing a node via _REST_. It has no influence regarding 
communication between AnyLog nodes (via _TCP_) on a given network. 

To deploy automatically, a user needs to enable the following parameters in configurations, under _Authentication_ section:
* set `ENABLE_REST_AUTH` to **true**
* set `NODE_PASSWORD`
* set `USER_NAME`
* set `USER_PASSWORD`
* set `USER_TYPE` to either **admin** or **user** 

**Basic Authentication Process**:
1. set params
```anylog 
enable_rest_auth = $ENABLE_REST_AUTH
node_password = $NODE_PASSWORD 
user_name = $USER_NAME
user_password = $USER_PASSWORD
user_type = $USER_TYPE 
```

2. Set the password of the node 
```anylog
set local password = !node_passwd
```

3. Enable Authentication for _User_
```anylog
set user authentication on
```

4. Grant user permissions to access node 
```anylog 
id add user where name=!user_name and password=!user_password and type=!user_type
```

Once a user has been added _cURL_ commands require username and password credentials to execute. 

```shell
# Without Authentication: 
curl -X GET 10.0.0.1:32048 -H "command: get status" -H "User-Agent: AnyLog/1.23"
# With Authentication: 
curl -X GET 10.0.0.1:32048 -U user:password -H "command: get status" -H "User-Agent: AnyLog/1.23"
```

## Certificate Based Authentication 
Using certificate based authentication cannot be done via configurations at this time. Instead, this needs to be done once
the node is already running.
 
Certificate based authentication, can be set for a _node_ or _user_. In addition, there should be a _root_ account that's
responsible for managing access for all other members. 

**Disclaimer**: We do not recommend setting up the `root` account on the master node

### Root Authentication & Preset Permissions
Root user grants permissions to members (nodes and users) - this should be done only on a single AnyLog instance.

1. [AnyLog-Network/scripts/authentication/set_params.al](https://github.com/AnyLog-co/AnyLog-Network/blob/develop/scripts/authentication/enable_authentication.al)
presets the configurations values used to configure certificate based authentication. Directions for updating configuration 
values in [Docker](../Docker/docker_volumes.md) | [Kubernetes](../Kubernetes/volumes.md).

**Relevant Params for creating a _root_ user**: 
* root_name 
* root_password 

```anylog
process !local_scripts/authentication/set_params.al 
``` 

2. Generate keys for the Root User - if keys already exists, the script stores the private key as a
variable called `!private_key`.
```anylog
process !local_scripts/authentication/root_keys.al
```

3. Create root user policy & store in blockchain.  
```anylog
process !local_scripts/authentication/declare_root_member.al
```

**Sample Root Policy**: 
```json
{"member": {
  "type": "root", 
  "name": "admin", 
  "company": "New Company",
  "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzrKmV/mf0oA1WvkqJ5F+SxAz/"
                "mpJfoJPTkKUwbVNZmC+CCHGMnvbw3eN+EKM6rTosN/HUrzUIi2m6K4ZVv+MfKWYY"
                "VPVewGsDXXK0Endbou/01dljVyM6p7aqrTtutGJb8hJUZDxn+MxxKOASHgXb5kgK"
                "bJHGcCaa5uJEBTwBfQIDAQAB", 
  "id": "16ec124e46d5792dc28fc1b5dedd4b02", 
  "date": "2023-01-10T19:55:40.247276Z", 
  "signature": "48ac358d526f3e2306818b7eff22d061dd2930dee91669f6797c046baebb88d8"
               "5033d167e98df1fb36c82feb6a17892e0ad69841fe4e1d4189e25b8e0875e400"
               "a4916886f432206200c9c877cc233ac8eb2f1d77ac59f66bf31e186322be7365"
               "9e4eca91d3d8a6cc268f4d5fa7c7cd2dedb6011d35c251dab194eeea2d980b5f",
  "ledger": "global"
}}
```

At this point the node which declared the has the keys `root` can be used to declare other member in the network, as well
as their permissions. We recommend having a [node member](#declare-non-root-member) for the node as well.

### Declare non-Root Member
Except for `root` member policy, all other members must be associated with a subset of permissions of what their
respective keys can and cannot do. The default scripts provide examples for permissions with [no restrictions](https://github.com/AnyLog-co/AnyLog-Network/blob/develop/scripts/authentication/no_restrictions_permissions.al) 
and with [limited permissions](https://github.com/AnyLog-co/AnyLog-Network/blob/develop/scripts/authentication/limited_permissions.al).
The limited permissions allows commands such as: _get_, _sql_ and _blockchain_.

1. Declare no restrictions permissions policy 
```anylog
process !local_scripts/authentication/no_restrictions_permissions.al
```

2. Declare limited permissions policy
```anylog
process !local_scripts/authentication/limited_permissions.al 
```

**Sample Permission Policy**: 
```json
{"permissions": {
  "name": "no_restrictions", 
  "databases": ["*"], 
  "enable": ["*"], 
  "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzrKmV/mf0oA1WvkqJ5F+SxAz/"
                "mpJfoJPTkKUwbVNZmC+CCHGMnvbw3eN+EKM6rTosN/HUrzUIi2m6K4ZVv+MfKWYY"
                "VPVewGsDXXK0Endbou/01dljVyM6p7aqrTtutGJb8hJUZDxn+MxxKOASHgXb5kgK"
                "bJHGcCaa5uJEBTwBfQIDAQAB", 
  "id": "b3e415fd3479a3dc2329391e6f7441d5", 
  "date": "2023-01-10T19:55:47.371616Z", 
  "signature": "567a6408ada95e05878214d0f0cf7add65822080039a8fc1758760ea31fbefe2"
               "d91a83bbb82b261b47c625a857c403a94817d4f159bca8a3a2907350d75b69d0"
               "6f83766d0f0745ea9375b04a16a278d15fa50c6db6c40b03fd5a463f0439cf1a"
               "ad7b81f4a6f4125d6f32ee937a867090793a013cb8f78a0f4e14da0868d4872d", 
  "ledger": "global"
}}
```

#### Node Authentication
The node authentication requires access to **both** the new AnyLog node (_new node_), as-well-as a node with permissions that allows 
adding a new AnyLog instance to the network (_root node_). If you do not have access to such a node, please work with your administrator
to connect your node to the network. 

1. [AnyLog-Network/scripts/authentication/set_params.al](https://github.com/AnyLog-co/AnyLog-Network/blob/develop/scripts/authentication/enable_authentication.al)
presets the configurations values used to configure certificate based authentication; this step needs to be done on **both**
the _root node_, as-well-as the _new node_ being added to the network. Directions for updating configuration 
values in [Docker](../Docker/docker_volumes.md) | [Kubernetes](../Kubernetes/volumes.md).

**Relevant Params on New Node**: 
* `node_password` - node password for when creating node_keys -- used for both private and local password in enable_authentication.al

**Relevant Params on Root Node**: 
* `remote_node_conn` - IP:PORT information for _new node_ that"ll be added to network 
* `remote_node_name` - set the name for the _new node_ you want to add to the network
* `remote_node_company` - set the company associated with the _new node_

```anylog
process !local_scripts/authentication/set_params.al 
```

2. On the _new node_ create a private and public key - if keys already exists, the script stores the private key as a
variable called `!private_key_node`.
```anylog
process !local_scripts/authentication/node_keys.al
```

3. On the _root node_ declare a member policy that"ll be associated with the _new node_
```anylog
process !local_scripts/authentication/declare_node_member.al
```

**Sample Member Policy**
```json     
{"member": {
  "type": "node", 
  "name": "anylog-query", 
  "company": "New Company", 
  "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt8v4YVlHr5Mr/pzyXE1mowy3i"
                "oFWp1MyrjLVoM9Qu0Mo0JwVL8wqFMdGM9ZRwskx5iMlgeCiP3MsMB9Obb8xxUU+I"
                "B9Pu2xeiYh5czkW1ztjqE5quHW1Tn0FM+iDMYBN9sh5kyYcFgZ2xMHZdpNP40xiC"
                "5ZP3VaaVct4VsiET6wIDAQAB", 
  "id": "76158fbea9b5542289c20e550b37931c", 
  "date": "2023-01-10T19:56:19.318761Z", 
  "ledger": "global"}}
```

4. Once a member policy is declared for a node, the _root node_ needs to give this member permissions. The scripts provided
currently give (new) node members full access. However, administrators may choose to set different permissions for different
nodes. Directions for updating configuration values in [Docker](../Docker/docker_volumes.md) | [Kubernetes](../Kubernetes/volumes.md).
```anylog
process !local_scripts/authentication/assign_node_privileges.al
```

**Sample Assignment Policy**
```json
{"assignment": {
  "name": "anylog-query", 
  "company": "New Company", 
  "permissions": "b3e415fd3479a3dc2329391e6f7441d5", 
  "members": ["MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt8v4YVlHr5Mr/pzyXE1mowy3i"
              "oFWp1MyrjLVoM9Qu0Mo0JwVL8wqFMdGM9ZRwskx5iMlgeCiP3MsMB9Obb8xxUU+I"
              "B9Pu2xeiYh5czkW1ztjqE5quHW1Tn0FM+iDMYBN9sh5kyYcFgZ2xMHZdpNP40xiC"
              "5ZP3VaaVct4VsiET6wIDAQAB"], 
  "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzrKmV/mf0oA1WvkqJ5F+SxAz/"
                "mpJfoJPTkKUwbVNZmC+CCHGMnvbw3eN+EKM6rTosN/HUrzUIi2m6K4ZVv+MfKWYY"
                "VPVewGsDXXK0Endbou/01dljVyM6p7aqrTtutGJb8hJUZDxn+MxxKOASHgXb5kgK"
                "bJHGcCaa5uJEBTwBfQIDAQAB", 
  "id": "10a97e525386b26a90e4f03ff986e2b5", 
  "date": "2023-01-10T19:56:26.698297Z", 
  "signature": "50082415da17346c077418d02a8a51370600440bafd13e37f24af3ca5efc8fab"
               "59e260eb3ed3a35410ea81b65c13a93ef447aa852d6978be965636586a716292"
               "af358f7f4d9dd0bf11f22b0335d737b0f9718f5166688c5e4719d64dbe4368b4"
               "bdc84f1f78ae3235e307661b4e3b62b9e5bf79b168fb5d350fa9dd07e891575b", 
  "ledger": "global"
}}
```

5. Once a member policy (and it's permissions) are declared, then the _new node_ can enable authentication. The script 
also configures [password security](../../authentication.md#passwords) for the private key using `node_password` as the 
default password value. 
```anylog
process !local_scripts/authentication/enable_authentication.al 
```

At this point the _new node_, has the correct privileges to communicate with the network, and act as is expected of it.
If the _new node_ is configured as _REST_, then users can **either** deploy the process(es) for the desired node type
**or** execute `blockchain sync` in view its privileges, and access other nodes in the network. 

```anylog 
# blockchain sync
run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn

# deploy a desired node type on the node - the example is for an Operator Node 
process !local_scripts/run_scripts/start_operator.al 
```

