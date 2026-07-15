---
title: "Policy-Based Users and Keys — Example"
description: A full worked example of key-based authentication — assigning keys to nodes and users, building permission and assignment policies, and running a 2-operator demo end to end
layout: page
source_path: "Policy-Based Users and Keys — Example.md"
---

<!--
## Changelog
- (original) This walkthrough previously lived inside 03- Installation & Deployment/Securing the Network.md,
              alongside general overlay-network and authentication overview content.
- 2026-07-14 | Split out into its own standalone example file, as the sample logic for policy-based users/keys
              referenced from Securing the Network (overview) and Authentication (implementation reference).
              Internal links updated to match the new location alongside Authentication.md.
-->

# Policy-Based Users and Keys — Example

This page demonstrates an end-to-end pattern for AnyLog's key-based authentication: assigning keys to nodes and
users, defining the policies that determine permissions, and assigning nodes/users to those policies. For the
concepts and individual commands used here, see [Authentication](Authentication.md). For where this fits
alongside TPM and overlay networking, see
[Securing the Network](../../03-%20Installation%20&%20Deployment/Securing%20the%20Network.md).

## Definitions

- **Member policy** — provides information on a member node or a user, including the public key assigned to
  that member.
- **Permission policy** — lists permitted/restricted commands and permitted/restricted database tables.
- **Assignment policy** — lists one or more members and a permission policy; the assignment determines the
  permitted operations for the listed members.
- **Keys directory** (`!id_dir`) — directory holding keys assigned to different members, saved on the node.
- **PEM directory** (`!pem_dir`) — directory holding certificates and their associated keys.

## Prerequisites and reset

- A network with 2 operators.
- A setup using either a blockchain or a master node.
- No existing permission or assignment policies.
- No existing keys assigned to nodes or users.

This example configures a network using a master node; if a blockchain is used instead, the master node
configuration steps are simply ignored.

Configure each operator node:

```anylog
set authentication off
master_node = 10.0.0.25:2048        # Replace with the proper address
```

Configure the master node:

```anylog
set authentication off
connect dbms blockchain where type = sqlite and user = !db_user and port = !db_port
```

On an operator node, delete all policies on the master node:

```anylog
run client !master_node "drop table ledger where dbms = blockchain"
run client !master_node "create table ledger where dbms = blockchain"
run client !master_node "blockchain delete local file"
```

Delete the local blockchain file on each operator node:

```anylog
blockchain delete local file
```

Delete existing issued keys on each node:

```anylog
system del !id_dir/*.* /q      # Windows
system rm !id_dir/*.*          # Linux
```

## Validating policy structure

Policies are JSON structures whose root has exactly one attribute — the **policy type**. When a variable is
assigned a policy, prefixing the variable name with `!` (e.g. `!member`) displays the policy on the CLI. The
`json` command confirms the structure is valid JSON:

```anylog
json !member
```

Adding `test` returns `true`/`false` instead of printing the policy:

```anylog
json !member test
```

## Required attributes in each policy

| Policy Type | Role | Attribute | Required | Comments |
|---|---|---|---|---|
| member | Declares a member node or a user | type | Yes | Only one policy may have the value `root`. Multiple members can have `node` or `user`. |
| | | public_key | Yes | Unique — no two member policies may share a public key. |
| Permissions | Determines commands and databases allowed | name | Yes | A unique name for the permissions policy. |
| | | enable | Yes | A list of allowed commands; `*` = all commands. |
| | | disable | No | Optional list of disallowed commands. |
| | | databases | No | Optional list of allowed databases. |
| | | tables | No | Optional list of allowed tables. |
| Assignment | Associates a permissions policy with one or more member policies | permissions | Yes | The ID of the permissions policy. |
| | | members | Yes | A list of the public keys of the assigned members. |
| | | public_key | Yes | The public key of the node/user creating the assignment. |
| | | signature | Yes | The signature of the node/user creating the assignment. |

### Conventions used below

This demo runs on the CLI of the two operators:
- Commands on operator 1 are marked `CLI(opr.1)`.
- Commands on operator 2 are marked `CLI(opr.2)`.
- Commands on both are marked `CLI(opr.1.2)`.

## The demo steps

The demo uses 2 operator nodes and 2 users (a root user and a non-root user). Each node and user is assigned
keys and a member policy; each member policy is assigned a permission policy via an assignment policy, so
senders can be authenticated and their permissions determined. If a master node is used, its configuration is
detailed [below](#master-node-configuration).

| Step | Node | Process | Details |
|---|---|---|---|
| 1 | CLI(opr.1) | Root user keys | Generate keys for the root user |
| 2 | CLI(opr.1) | Root user policy | Create a policy for the root user, who grants permissions to other members |
| 3 | CLI(opr.1.2) | Node keys | Generate keys for the operator nodes |
| 4 | CLI(opr.1.2) | Node member policy | Create member policies representing the operator nodes |
| 5 | CLI(opr.1) | User keys | Generate keys for a user who is not a node |
| 6 | CLI(opr.1) | User policy | Create a member policy for the user |
| 7 | CLI(opr.1) | Permission policy | Create a permission policy with no restrictions |
| 8 | CLI(opr.1) | Assign permissions to a user | Root user grants all privileges to a user |
| 9 | CLI(opr.1) | Permission policy | Generate a permission policy with limited privileges |
| 10 | CLI(opr.1) | Assign permissions to a node | A privileged user grants limited privileges to a node |
| 11 | CLI(opr.1.2) | Set a local password | Protects local data; provided to the node every time it restarts |
| 12 | CLI(opr.1.2) | Save the node's private key | Stored locally, protected by the local password |
| 13 | CLI(opr.1.2) | Enable authentication | Enables authentication of messages from users and nodes |

### Step 1 — Generate keys for the root user

```anylog
id create keys where password = abc and keys_file = root_keys
```

Creates a file (`root_keys`) with the public key and encrypted private key of the root user, in the keys
directory (`!key_dir`).

Note: if no file name is given, the keys are printed to the screen and the user must store/protect them
themselves.

### Step 2 — Root user policy

The only required attributes are `type = "root"` and `public_key` (added automatically when the policy is
signed). A `name` attribute is optional but useful for referencing the policy later.

```anylog
<member = {"member" : {
    "type" : "root",
    "name"  : "rachel"
    }
}>
private_key = get private key where keys_file = root_keys
member = id sign !member where key = !private_key and password = abc
json !member    # View the policy including the signature and public key
blockchain insert where policy = !member and local = true and master = !master_node
```

### Step 3 — Generate keys for the operator nodes

CLI(opr.1):

```anylog
id create keys for node where password = demo1
```

CLI(opr.2):

```anylog
id create keys for node where password = demo2
```

### Step 4 — Create member policies for the operator nodes

CLI(opr.1):

```anylog
<member = {"member" : {
    "id"   : "node_001",
    "type" : "node",
    "company"  : "Northern Light",
    "name" : "member north"
    }
}>
member = id sign !member where password = demo1
json !member
blockchain insert where policy = !member and local = true and master = !master_node
```

CLI(opr.2):

```anylog
<member = {"member" : {
    "id"   : "node_002",
    "type" : "node",
    "company"  : "Northern Light",
    "name" : "member south"
    }
}>
member = id sign !member where password = demo2
json !member
blockchain insert where policy = !member and local = true and master = !master_node
```

### Step 5 — Generate keys for a user

CLI(opr.1), generating keys for a user named Roy, stored in the keys directory:

```anylog
id create keys where password = 123 and keys_file = roy
```

### Step 6 — Create a member policy for the user

CLI(opr.1). Notes:
1. The policy type is `user`, distinguishing it from `root`.
2. The public key is added when the policy is signed — no two member policies may share a public key.

```anylog
<member = {"member" : {
    "id"   : "user_001",
    "type" : "user",
    "name"  : "roy"
    }
}>
private_key = get private key where keys_file = roy
member = id sign !member where key = !private_key and password = 123
json !member
blockchain insert where policy = !member and local = true and master = !master_node
```

### Step 7 — Create a permission policy with no restrictions

CLI(opr.1). This policy enables all commands and all databases, and must be signed by the root user.

```anylog
<permissions = {"permissions" : {
    "name" : "no restrictions",
    "databases" : ["*"],
    "enable" : ["*"]
    }
}>
private_key = get private key where keys_file = root_keys
permissions = id sign !permissions where key = !private_key and password = abc
json !permissions
blockchain insert where policy = !permissions and local = true and master = !master_node
```

### Step 8 — Assign privileges to a user

CLI(opr.1). The root user grants Roy all privileges by associating the "no restrictions" policy with Roy's
member policy:

```anylog
permission_id = blockchain get permissions where name = "no restrictions" bring ['permissions']['id']
member_user = blockchain get member where name = roy bring ['member']['public_key']

<assignment = {"assignment" : {
        "name" : "assignment to no restrictions",
        "permissions"  : !permission_id,
        "members"  : [!member_user]
        }
}>
private_key = get private key where keys_file = root_keys
assignment = id sign !assignment where key = !private_key and password = abc
json !assignment
blockchain insert where policy = !assignment and local = true and master = !master_node
```

Notes:
1. The assignment policy must be signed by the root user or a user with permission to sign assignment policies.
2. After this assignment, since Roy has no-restrictions permissions, Roy is himself permitted to sign
   assignment policies.

### Step 9 — Create a permission policy with limited privileges

CLI(opr.1):

```anylog
<permissions = {"permissions" : {
    "name" : "node basic permissions",
    "databases" : ["*", "-lsl_demo"],
    "tables" : ["lsl_demo.temperature_sensor", "lsl_demo.ping_sensor"],
    "enable" : [ "file", "get", "reset", "sql", "echo", "print", "blockchain", "event"],
    "disable" : ["get node id"]
    }
}>
private_key = get private key where keys_file = roy
permissions = id sign !permissions where key = !private_key and password = 123
!permissions
blockchain insert where policy = !permissions and local = true and master = !master_node
```

Notes:
1. Permits operating on all databases except `lsl_demo`.
2. `tables` permits exactly `temperature_sensor` and `ping_sensor` within `lsl_demo`.
3. Net effect: all databases are allowed, but only those two tables are allowed within `lsl_demo`.
4. `enable` lists permitted commands; `disable` lists commands that are explicitly not allowed.

### Step 10 — Assign limited privileges to the operator nodes

CLI(opr.1). Roy (who now has full privileges) assigns the "node basic permissions" policy to both operator
nodes:

```anylog
member_node1 = blockchain get member where id = node_001 bring ['member']['public_key']
member_node2 = blockchain get member where id = node_002 bring ['member']['public_key']

permission_id = blockchain get permissions where name = "node basic permissions" bring ['permissions']['id']

<assignment = {"assignment" : {
        "permissions"  : !permission_id,
        "members"  : [!member_node1, !member_node2]
        }
}>
private_key = get private key where keys_file = roy
assignment = id sign !assignment where key = !private_key and password = 123
json !assignment
blockchain insert where policy = !assignment and local = true and master = !master_node
```

### Step 11 — Provide the local password

Protects sensitive local information; provided every time a node restarts. In this example, operator 1 uses
`123` and operator 2 uses `456`.

CLI(opr.1):

```anylog
set local password = 123
```

CLI(opr.2):

```anylog
set local password = 456
```

Notes:
- If a local password is set and a node restarts with the wrong password, an error is returned.
- If the local password is lost, all files in the keys directory need to be deleted, and the node must be
  assigned new keys and a new assignment policy.

### Step 12 — Save the node's private key

CLI(opr.1):

```anylog
set private password = demo1 in file
```

CLI(opr.2):

```anylog
set private password = demo2 in file
```

Note: stored in a file called `auth.id` in the keys directory.

### Step 13 — Enable authentication

Enables authentication of message senders and determination of their authorization. On receiving a message, a
node first authenticates the sender via their public key, then checks permission policies to determine
authorization — granted directly by the root user, or via a chain of permitted authorizations derived from the
root user.

CLI(opr.1.2):

```anylog
set node authentication on
```

Note: if a master node is used, enable authentication on the operators only after the
[master node setup](#master-node-configuration) below.

## Adding members to an existing network

A newly initiated node has no permissions and can't publish its own member policy. A permitted peer node must
add it on the new node's behalf:

1. The new node generates its public/private keys — see
   [Creating keys for a node in the network](Authentication.md#creating-keys-for-a-node-in-the-network).
2. A peer node with proper permissions retrieves the new node's public key:
   ```anylog
   peer_key = run client IP:Port get node id
   ```
3. The peer node creates the new node's member policy.
4. The peer node assigns permissions to the new node.
5. Since the new node has no metadata yet, it can't process messages from other network members, so a peer must
   provide it a valid copy of the metadata:
   1. On the new node — disable local authentication: `set authentication off`
   2. On the peer node — copy the metadata to the new node, e.g.:
      `run client 10.0.0.78:3048 file copy !blockchain_file !!blockchain_file`
   3. On the new node — provide the local password and re-enable authentication:
      `set local password = 456`, then `set authentication on`

The new node is now an active member of the network.

## Master Node Configuration

Optional — only needed if a master node is used. `CLI(master)` designates the master node's command line.

### Generate keys for the master node

CLI(master):

```anylog
id create keys for node where password = masterpswd
```

### Master node policy

CLI(master):

```anylog
<member = {"member" : {
    "type" : "node",
    "name"  : "master_node"
    }
}>
private_key = get private key
member = id sign !member where key = !private_key and password = masterpswd
json !member    # View the policy including the signature and public key
blockchain insert where policy = !member and local = true and master = !master_node
```

### Create a permission policy for the master node

CLI(opr.1):

```anylog
<permissions = {"permissions" : {
    "name" : "master node permissions",
    "enable" : [ "file", "event", "echo", "print"]
    }
}>
private_key = get private key where keys_file = roy
permissions = id sign !permissions where key = !private_key and password = 123
json !permissions
blockchain insert where policy = !permissions and local = true and master = !master_node
```

### Assign privileges to the master node

CLI(opr.1):

```anylog
permission_id = blockchain get permissions where name = "master node permissions" bring ['permissions']['id']
member_node = blockchain get member where name = master_node bring ['member']['public_key']

<assignment = {"assignment" : {
        "name" : "master assignment",
        "permissions"  : !permission_id,
        "members"  : [!member_node]
        }
}>
private_key = get private key where keys_file = roy
assignment = id sign !assignment where key = !private_key and password = 123
json !assignment
blockchain insert where policy = !assignment and local = true and master = !master_node
```

### Provide the local password

CLI(master):

```anylog
set local password = masterlocpsswd
```

### Save the master node's private key

CLI(master):

```anylog
set private password = masterpswd in file
```

### Enable authentication

CLI(master):

```anylog
set node authentication on
```

## Demo: authorized and non-authorized commands

Get the address of each operator:

CLI(opr.1):

```text
AL +> get connections
Type      External Address  Local Address
---------|-----------------|--------------|
TCP      |73.222.38.13:7848|10.0.0.78:7848|
REST     |10.0.0.78:7849   |10.0.0.78:7849|
Messaging|73.222.38.13:7850|10.0.0.78:7850|
```

CLI(opr.2):

```text
AL +> get connections
Type      External Address  Local Address
---------|-----------------|--------------|
TCP      |73.222.38.13:3048|10.0.0.78:3048|
REST     |10.0.0.78:3049   |10.0.0.78:3049|
Messaging|73.222.38.13:7855|10.0.0.78:7855|
```

### Examples of permitted messages

CLI(opr.1):

```anylog
run client 10.0.0.78:3048 get status
run client 10.0.0.78:3048 echo 'hello world'
run client 10.0.0.78:3048 get status
run client 10.0.0.78:3048 get databases
```

CLI(opr.2):

```anylog
run client 10.0.0.78:7848 get status
run client 10.0.0.78:7848 echo 'hello world'
run client 10.0.0.78:7848 get status
run client 10.0.0.78:7848 show databases
```

### Examples of denied messages

CLI(opr.1):

```anylog
run client 10.0.0.78:3048 system ls
run client 10.0.0.78:3048 set authentication off
```

CLI(opr.2):

```anylog
run client 10.0.0.78:7848 system ls
run client 10.0.0.78:7848 set authentication off
```

## Messaging using the private key of a user

A user may want to send messages under their own authorization — for example, an administrator logged into a
node who needs to issue a command the node's own permission policy doesn't allow. The user can leverage their
own assigned permissions instead:

```anylog
private_key = get private key where keys_file = roy
set signatory where key = !private_key and password = 123 and name = roy
get signatory   # Validate the signatory changed from the node to the user
run client 10.0.0.78:3048 system ls     # Roy has no restrictions, so this executes
```

## Using certificates

This section extends the policy-based pattern above to 3rd-party applications that aren't network members at
all — see [Using SSL Certificates](Authentication.md#using-ssl-certificates) for the underlying commands. In
this model, AnyLog acts as a Certificate Authority issuing Client Certificates to 3rd-party applications. Client
certificates work like this:

- Only clients holding a certificate can communicate with network nodes.
- A message from a certificate holder includes a public key, treated like any other network member:
  - The certificate holder is represented by a member policy (with `type = certificate`).
  - An assignment policy associates that member policy with a permission policy.
  - A message from the 3rd party is processed if the sender is authenticated and holds the right permissions.

This setup enables SSL between the AnyLog node (server) and the 3rd-party application (client). Example REST
server configuration to allow SSL certificates:

```anylog
run rest server !ip !rest_port where timeout = 0 and threads = 6 and ssl = true and ca_org = AnyLog and server_org = "Node 128"
```

Check the configuration:

```anylog
get rest server info
```

### Example

Assumes the example certificates from [Using SSL Certificates](Authentication.md#using-ssl-certificates) are
available in the pem directory (`!pem_dir`).

#### Generate a member policy representing the issued certificate

Not signed, since the member is outside the network:

```anylog
public_key = get public string where keys_file = !pem_dir/server-acme-inc-public-key

<member = {"member" : {
    "type" : "certificate",
    "name"  : "acme",
    "public_key" : !public_key
    }
}>
json !member
blockchain insert where policy = !member and local = true and master = !master_node
```

#### Generate a permission policy for 3rd-party applications

```anylog
<permissions = {"permissions" : {
    "name" : "application basic permissions",
    "tables" : ["lsl_demo.temperature_sensor", "lsl_demo.ping_sensor"],
    "enable" : [ "file", "get", "reset", "sql", "echo", "print", "blockchain", "event", "run client"]
    }
}>
private_key = get private key where keys_file = roy
permissions = id sign !permissions where key = !private_key and password = 123
json !permissions
blockchain insert where policy = !permissions and local = true and master = !master_node
```

#### Assign the permission policy to the member policy

```anylog
member_certificate = blockchain get member where type = certificate and name = acme bring ['member']['public_key']

permission_id = blockchain get permissions where name = "application basic permissions" bring [permissions][id]

<assignment = {"assignment" : {
        "name" : "application assignment",
        "permissions"  : !permission_id,
        "members"  : [!member_certificate]
        }
}>
private_key = get private key where keys_file = roy
assignment = id sign !assignment where key = !private_key and password = 123
json !assignment
blockchain insert where policy = !assignment and local = true and master = !master_node
```

#### Query member policies

```anylog
blockchain get member       # The entire policies
blockchain get member bring.table [] [*][name] [*][type] [*][public_key]      # Selected attributes from each policy
```

#### Query permissions for members

See [Permission Group](Authentication.md#permission-group) for `get permissions`.

```anylog
public_key = get public key where keys_file = !pem_dir/server-acme-inc-public-key
get permissions where public_key = !public_key
get permissions where name = roy
```

### Example: 3rd-party application via cURL

```anylog
curl --location --request GET https://10.0.0.78:7849 --header "User-Agent: AnyLog/1.23" --header "command: get status" --cert "server-acme-inc-private-key.crt" --key "server-acme-inc-private-key.key"
```

### Example: 3rd-party application via AnyLog Remote CLI

In the Settings tab:
- Enable CA Certificate.
- Set the PEM file to: `ca-anylog-public-key.crt`
- Set the CRT file to: `server-acme-inc-public-key.crt`
- Set the KEY file to: `server-acme-inc-private-key.key`

### Example: 3rd-party application via Grafana

Configuring Grafana in general is covered in
[Using Grafana](../../08-%20Northbound%20Connectors/Using%20Grafana.md). To use a certificate specifically,
update the Grafana JSON data source page:
- Set the AnyLog URL to use HTTPS.
- Set *TLS Client Auth* to ON.
- Set *Skip TLS Verify* to ON.
- In *TLS/SSL Auth Details*:
  - Set *Client Cert* to the contents of `server-acme-inc-public-key.crt`.
  - Set *Client Key* to the contents of `server-acme-inc-private-key.key`.

With this setup, *Save & Test* should return a green "Data Source is working" message.