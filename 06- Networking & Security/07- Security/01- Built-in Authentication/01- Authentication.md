---
title: "Users and Nodes Authentication — Implementation"
description: How to implement AnyLog's built-in authentication options — node/key-based authentication, user authentication, and certificate-based (SSL) authentication
layout: page
source_path: "01- Authentication.md"
---

<!--
## Changelog
- (original) Created as "Users and nodes Authentication, making the data secure" under
              03- Installation & Deployment/01- Authentication.md
- 2026-07-14 | Moved to 06- Networking & Security/Built-in Authentication/01- Authentication.md, alongside a new
              worked-example sub-file (Policy-Based Users and Keys — Example.md). Updated cross-references
              accordingly. For a general overview of all of AnyLog's security options (this document plus TPM
              and overlay networking), see Securing the Network.
-  2026-07-31 | Massimiliano | remote sign via certificate_authority (Master/Operator) | 2.0.2606 |
-->

# Users and Nodes Authentication — Implementation

This document covers how to implement each of AnyLog's built-in authentication options: the commands, their
options, and what each one does. For a general overview of how this fits alongside TPM and overlay networking,
see [Securing the Network](../../03-%20Securing%20the%20Network.md). For a full
worked example — assigning keys, building permission and assignment policies, and running a 2-operator demo end
to end — see [Policy-Based Users and Keys — Example](02-%20Authentication-policies.md).

The commands in this document facilitate a framework that provides the following:

* Authenticates messages sent from nodes to peer nodes.
* Authenticates messages sent from nodes to peers with privileges assigned to users.
* Determines permissions for network processes and the data maintained by nodes in the network.
* Validates policies by authenticating their authors and their assigned permissions (see
   [Adding policies to the blockchain](#adding-policies-to-the-blockchain) below).
* Encrypts and decrypts commands and data transferred in the network.

The network provides two layers of authentication:

1) **Node Authentication** — processes that authenticate users and processes delivering messages from one node
   to another, and that authenticate policies registered on the blockchain. These messages are authenticated
   using the TCP server processes and related calls (see the
   [TCP Server process](../../../07-%20CLI/02-%20Background%20Processes.md#the-tcp-server-process) section).
   Message authentication is based on issuing a private key and a public key to nodes and users. Messages are
   signed by the private key of the sender (a user or a node), and the destination node validates the sender
   using their public key and the policies that describe the sender's authorized functionality. Policies
   themselves are authenticated by validating the author's permission to create them.

2) **User Authentication** — processes that authenticate users and applications that are *not* members of the
   network (for example, a Grafana dashboard or a cURL request issuing a REST request to a node). See
   [REST requests](../../../07-%20CLI/02-%20Background%20Processes.md#rest-requests) for details on REST
   handling. Authentication here is based on one of:
   - Usernames and passwords kept on the destination node — see [below](#users-authentication).
   - Client certificates validated against policies that define authorized functionality — see
     [below](#using-ssl-certificates).

Enabling and disabling authentication (both node and user authentication together) is done with:

```anylog
set authentication [on/off]
```

Notes:
- Node authentication can optionally be enabled on its own using `set node authentication`, detailed
  [below](#node-authentication).
- User authentication can optionally be enabled on its own using `set user authentication`, detailed
  [below](#add-users).

The following command determines how the node is currently configured:

```anylog
get authentication
```

## Encrypting network messages

AnyLog provides mechanisms to encrypt messages transferred over the network. Messages are encrypted using the
public key of the receiver and decrypted by the receiver with their private key. These processes are detailed
[below](#encrypt-and-decrypt-messages).

# Passwords

Private keys and other sensitive information can be kept outside the node and supplied when needed, or protected
with a password so they can be kept on the node itself. Each node can be assigned two types of passwords:

1. A **local password** — enables encryption and decryption of sensitive data stored on the local file system.
2. The **private key password** — enables use of the private key to sign policies and authenticate as a member.

## The local password

Used to encrypt the node's sensitive information saved in local files, using a random salt key. Set with
`set local password`; the password itself is not stored on disk, so it must be re-provided whenever the node
starts, and is validated against the original whenever it's re-provided.

Usage:

```anylog
set local password = [password]
```

## The private password

Protects the node's private key. Set with `set private password`, and can optionally be stored in a local file,
itself protected by the node's [local password](#the-local-password).

Usage:

```anylog
set private password = [password] [in file]
```

`in file` is optional. If provided, the password protecting the node's private key is stored locally and the
private key becomes available to all processes that need it (assuming the node's local password is available).
If specified, the password only needs to be provided once; otherwise, `set private password` must be called
again every time the node starts.

# Node Authentication

Members participating in the network are assigned a public and a private key. The public key uniquely identifies
the member and its privileges; the private key signs outgoing messages so the sender can be authenticated by the
receiving node.

Enable/disable node authentication:

```anylog
set node authentication on
set node authentication off
```

## Creating private and public keys

A private key and a public key are issued for each node that is a member of the network. The public key is
assigned privileges (see [Permission Group](#permission-group) below) that determine whether a command sent from
the node to a peer can be executed on that peer. Users can also be issued their own private/public key pair —
this lets an individual user's privileges (rather than the node's) determine whether their commands are
processed on a peer, which is useful for an administrator who needs elevated access beyond what the node itself
is permitted.

### Creating keys for a node in the network

```anylog
id create keys for node where password = [password]
```

Creates a private and a public key; the private key is encrypted using the given password and kept on the node.
The public key uniquely identifies the node; the private key signs messages sent from it. Retrieve the public
key with:

```anylog
get node id
```

Policies added to the blockchain include the author's public key and a signature. Before executing a policy, a
node validates that the policy was signed with the private key of the holder of the public key it contains, and
that the author has permission to create that policy.

Notes:
- Keys for a given node only need to be created once — a second call to `id create keys for node` returns an
  error.
- Both the public key and the encrypted private key are stored in a file called `node_id.pem`.

### Creating keys for users in the network

Users issuing commands on the AnyLog CLI can be assigned their own private/public key pair, letting them:

a) Send messages to nodes in the network.
b) Sign policies they add to the blockchain.

Command:

```anylog
id create keys for node where password = [password] and keys_file = [file path and name]
```

`keys_file` is optional. Examples:

```anylog
id create keys for node where password = my_password
id create keys for node where password = my_password and keys_file = !usb_path/my_keys
```

If a file name is given, the keys are stored there (which can be on removable media, letting the user physically
secure them). If not given, the keys are printed to the screen and the user is responsible for storing them
securely. If only a file name (no path) is given, the file is written to the AnyLog keys directory — find its
location with `!id_dir`.

### Retrieving the keys

```anylog
get private key
get public key
```

Without headers/newlines:

```anylog
get private string
get public string
```

From a specific PEM file:

```anylog
get private key where keys_file = [path and file name]
get public key where keys_file = [path and file name]
```

Notes:
- If no path is given, `!id_dir` is assumed.
- If no file type is given, `.pem` is assumed and appended to the file name.

Examples:

```anylog
get private key where keys_file = roy
get public key where keys_file = !pem_dir/server-acme-inc-public-key
```

Without headers/newlines, from a file:

```anylog
get private string where keys_file = [path and file name]
get public string where keys_file = [path and file name]
```

## Adding policies to the blockchain

When a policy is added to the blockchain, the author's public key is attached to it. When the policy is
processed, this allows validation of:

1. That the policy was signed by the user associated with the public key.
2. That the user associated with the public key is authorized to sign that policy.

## Permission Group

A node or user's public key can be associated with a permission group, declared via a permission policy that
sets a list of permitted operations (e.g. which databases can be queried). Show one or more permission policies:

```anylog
get permissions where [attribute name] = [attribute value]
```

Examples:

```anylog
get permissions
get permissions where name = "application basic permissions"
```

When a message needs processing, the receiving node authenticates the sender via their public key, then
determines the authorization granted by whatever permission group that public key is assigned to.

`get member permissions` returns the permissions of a specific member (node or user). Without a `where`
condition, it returns permissions for the current node.

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
- The `where` condition is applied against the member policy; the permissions returned are whatever's assigned
  to that member via an assignment policy.
- If a [signatory](#setting-the-signatory) is assigned to the node, `get member permissions` (no `where`)
  returns the signatory's permissions instead of the node's own.

## Signing a policy

If authentication is enabled, policies published by users and nodes are signed with `id sign`, which updates the
policy with the publisher's public key and signature so the publisher can be authenticated and their
authorization validated.

```anylog
id sign [JSON Policy] where key = [private key] and password = [password]
id sign [JSON Policy] where password = [password]
```

If assigned to a variable, that variable holds the signed policy; otherwise the source variable is updated in
place.

Examples:

```anylog
id sign !json_script where key = !my_key and password = my_password
id sign !json_script where password = my_password
```

## Authenticate signature

Validate that a policy was signed using the private key associated with its public key:

```anylog
id authenticate [JSON Policy]
```

Example:

```anylog
id authenticate !json_script
```

# Validate permitted command

When a node receives a command from a peer, it uses the peer's public key to validate authorization against
`permissions` policies — confirming the public key is represented in a permission policy signed by an authorized
member.

```anylog
id validate where key = [public_key] and command = [command text] and table = [table name] and dbms = [dbms name]
```

`table` and `dbms` are optional and used with SQL commands.

Examples:

```anylog
id validate where key = !public_key and command = copy
id validate where key = !public_key and command = sql and dbms = lsl_demo and table = ping_sensor
```

# Setting the signatory

If node authentication is enabled, messages and policies are signed with the node's private key and identified
by its public key. Users can substitute a different private key to sign as themselves instead — useful for
letting a higher-privileged user leverage their own permissions on a node.

## Assign a signatory

```anylog
set signatory where key = [private key] and password = [password] and name = [signatory name]
```

`key` — the encrypted private key of the signatory. `password` — the private key's password. `name` — any
string except `node` (reserved for the node's own signatory identity).

## Revert to the node as the signatory

```anylog
reset signatory
```

## Get the signatory name

```anylog
get signatory name
```

Returns `"node"` if the node itself is the signatory, or the message "No signatory assigned" if none is set.

# Encrypt and Decrypt messages

Senders can encrypt a message with the receiver's public key; the receiver decrypts it with their private key.

## Encrypting a message

```anylog
id encrypt !message !public_key
```

## Decrypting a message

```anylog
id decrypt [message text] where key = [private key] and password = [password]
```

If `key` is omitted, the node's own private key is used.

Examples:

```anylog
id decrypt !message where key = !private_key and password = !my_password
id decrypt !message where password = !my_password
```

# Users Authentication

## Add users

When an external user or application connects to a node with user authentication enabled, the node validates
the username/password against a local list; on success, the user inherits the node's permissions.

```anylog
set user authentication on
set user authentication off
get authentication
```

Note: node authentication is detailed [above](#node-authentication).

Users and passwords are added per node, and `id add user` can specify an expiration after which the user's
access is revoked:

```anylog
id add user where name = [user name] and type = [user type] and password = [password] and expiration = [duration]
```

| Option | Explanation |
|---|---|
| user name | A unique identifier for the user. |
| user type | e.g. `admin`; defaults to `user`. |
| password | Any character string. |
| expiration | Time limit after which the user's access is revoked (seconds/minutes/hours/days). If omitted, access doesn't expire on its own — use `remove user` instead. |

Example:

```anylog
id add user where name = ori and password = 123 and expiration = 2 minutes
```

## Remove users

```anylog
id remove user where name = [user name]
```

Example:

```anylog
id remove user where name = john
```

## Update password

```anylog
id update user password where name = [user name] and old = [old password] and new = [new password]
```

Example:

```anylog
id update user password where name = ori and old = 123456 and new = iugsek88ekA
```

## Authenticating HTTP requests

### Enabling Basic Authentication on a node

1. On the AnyLog node:
   a. Provide the [local password](#the-local-password), if not already set: `set local password = [password]`
   b. Enable user authentication: `set user authentication on`
   c. Add permitted users: [id add user](#add-users)
2. On the REST call, include in the header:
   - key: `Authorization`
   - value: Base64-encoded `username:password`

#### Enabling Basic Authentication in Grafana

On the Data Source connection page:
1. In the *Auth* section, enable *Basic Auth*.
2. In the *Basic Auth Details* section, add the username and password.

#### Enabling Basic Authentication in Postman

In the Authorization tab: select *Basic Auth*, then update username and password.

# Using SSL Certificates

Nodes that aren't network members ("servers" below) can be authenticated using certificates. An example is
Grafana using a [Client Certificate](https://grafana.com/docs/grafana/latest/administration/configuration/#client_cert_path)
delivered with its query requests. Network member nodes can also be issued Signed Certificate Requests, so a
non-member server can authenticate them using the Certificate Authority's public key.

The process follows the [X.509](https://en.wikipedia.org/wiki/X.509#Structure_of_a_certificate) standard:
- The root user (or a designated user) acts as the Certificate Authority (CA).
- A server (non-member node) is issued a Certificate Request (CR).
- The AnyLog CA validates the server's identity and, if valid, signs the CR — giving the server a signed
  certificate and a private key to sign messages sent to the AnyLog node.

Notes:
1. Certificate commands write their output files to the location assigned to `pem_dir` (by default
   `AnyLog-Network/data/pem`). View it with `!pem_dir` on the CLI.
2. `[org]` in generated file names is derived from the `org` value passed to the command, with spaces replaced
   by hyphens.

## Setup the CA

The root user creates the CA's private key and public certificate, used to authenticate requests and encrypt
REST traffic:

```anylog
id generate certificate authority where [command options]
```

| Option | Explanation |
|---|---|
| password | Protects the CA private key. |
| country | [Two-letter ISO code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) for the organization's country. |
| locality | Province, region, county, or state. |
| state | Town, city, village. |
| org | Organization name. |
| hostname | The URL representing the CA. |

Example:

```anylog
id generate certificate authority where country = US and state = CA and locality = "Redwood City" and org = AnyLog and hostname =  anylog.co
```

Generates two files:


| Type        | Name  | Explanation |
| ------------- | ------------| ---- |
| .key  | ca-[org]-private_key | The Private Key for the CA |
| .crt  | ca-[org]-public_key | The Public Key for the CA. It will be provided to every AnyLog node that authenticates non-member nodes with CR signed by the AnyLog CA |



## Generating a certificate request

A non-member server is represented by a Certificate Request (CR) and a private key:

```anylog
id generate certificate request where [command options]
```

| Option | Explanation |
|---|---|
| password | Protects the generated private key. |
| country | Two-letter ISO country code. |
| locality | Province, region, county, or state. |
| state | Town, city, village. |
| org | Organization name. |
| alt_name | One or more IPs — additional host names for a single SSL certificate. |
| hostname | The URL of the node issuing the CR. |
| ip | The IP of the node issuing the CR. |

Example:

```anylog
id generate certificate request where country = US and state = CA and locality = "Redwood City" and org = "Acme Inc" and alt_name =  24.5.219.50 and hostname =  acme.co and ip = "192.56.76.4"
```

Generates three files:

| Type        | Name  | Explanation |
| ------------- | ------------| ---- |
| .key  | server-[org]-private_key | The Private Key for the requesting server. |
| .csr  | server-[org]-csr | A CR representing the server. |
| .pem  | server-[org]-public_key | The Public Key for the requesting server. This key is updated in the shared metadata layer to determine permissions.|

## Signing a certificate request

The CA signs the CR so an AnyLog node can authenticate the server:

```anylog
id sign certificate request where [command options]
```

| Option | Explanation |
|---|---|
| ca_org | The CA's organization name. |
| server_org | The organization name of the server associated with the CR. |

Example:

```anylog
id sign certificate request where ca_org = AnyLog and server_org = "Acme Inc"
```

Generates one file:

| Type | Name | Explanation |
|---|---|---|
| .crt  | server-[org]-public-key | The Signed Certificate Request. |

## Generating and signing a certificate request for the AnyLog node itself

```anylog
id generate certificate request where country = US and state = CA and locality = "Palo Alto" and org = "Node 128" and alt_name = 10.0.0.78 and hostname = anylog.co and ip = "192.38.78.8"
```

```anylog
id sign certificate request where ca_org = AnyLog and server_org = "Node 128"
```

## Summary of files from the examples above

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

Deploy with SSL enabled:

```anylog
run rest server where internal_ip = !ip and internal_port = 7849 and timeout = 0 and threads = 6 and ssl = true and ca_org = AnyLog and server_org = "Node 128"
```

Check the REST server configuration:

```anylog
get rest server info
```

### Setup the Server (Client Side)

Configure the client with:
The client is configured using the following files:
1) The Public Key of the CA: ca-[org]-public_key.crt (using the example files: ca-anylog-public-key.crt)
2) The Private Key of the server: server-[org]-csr.csr  (using the example files: server-acme-inc-private-key.key)
3) The Signed CR of the server: server-[org]-public-key.crt  (using the example files: server-acme-inc-public-key.crt)

An example Postman configuration is available at [Using Postman](../../../05-%20Northbound%20Connectors/02-%20Postman%20Integration.md#sending-queries-and-commands-to-the-anylog-network-with-postman).

## Examples using HTTPS

### Generating certificates

```anylog
id generate certificate authority where country = US and state = CA and locality = "Redwood City" and org = AnyLog and hostname =  anylog.co

id generate certificate request where country = US and state = CA and locality = "Redwood City" and org = "Acme Inc" and alt_name = 10.0.0.78 and hostname =  acme.co and ip = "10.0.0.78"

id sign certificate request where ca_org = AnyLog and server_org = "Acme Inc"

id generate certificate request where country = US and state = CA and locality = "Palo Alto" and org = "Node 128" and alt_name = 10.0.0.78 and alt_name = 24.5.219.50 and hostname =  anylog.co and ip = "10.0.0.78"

id sign certificate request where ca_org = AnyLog and server_org = "Node 128"
```

### cURL command using a certificate

```shell
curl --location --request GET https://10.0.0.78:7849 \
  --header "User-Agent: AnyLog/1.23" \
  --header "command: get status where format = json" \
  --cert "/mnt/d/Node/AnyLog-Network/data/pem/server-acme-inc-public-key.crt" \
  --key "/mnt/d/Node/AnyLog-Network/data/pem/server-acme-inc-private-key.key" \
  --cacert "/mnt/d/Node/AnyLog-Network/data/pem/ca-anylog-public-key.crt" \
  --max-time 30 -w "\n"
```

### Python calls using HTTPS

```python
import requests
url = "https://10.0.0.78:7849"

headers = {
    "User-Agent": "AnyLog/1.23",
    "command": "get status where format = json"
}

response = requests.get(
    url,
    headers=headers,
    cert=(
        "D:/Node/AnyLog-Network/data/pem/server-acme-inc-public-key.crt",
        "D:/Node/AnyLog-Network/data/pem/server-acme-inc-private-key.key"
    ),
    verify="D:/Node/AnyLog-Network/data/pem/ca-anylog-public-key.crt",
    timeout=30
)

print("Status Code:", response.status_code)
print("Response Body:")
print(response.text)
```

---

For a full worked example that ties keys, permission policies, and assignment policies together in a running
2-operator demo — including certificate-based permissions for a 3rd-party application — see
[Policy-Based Users and Keys — Example](02-%20Authentication-policies.md).