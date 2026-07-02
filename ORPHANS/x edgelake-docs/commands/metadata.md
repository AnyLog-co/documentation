---
layout: default
title: Metadata 
parent: Commands
nav_order: 3
---
# Metadata commands

The metadata commands are agnostic to the metadata platform used. When an EdgeLake network is deployed, users can 
select a blockchain platform or a master node as their metadata storage, The metadata commands operate indistinguishably 
on the platform used.

Notes: 
* The metadata commands start with the keyword blockchain, regardless of the metadata platform used (blockchain or master node).
* Run **help blockchain** on the EdgeLake CLI for a complete list of the blockchain commands.

## Blockchain Seed
The **blockchain seed** command pulls a copy of the metadata from a peer node. When a node is properly configured,
the [run synchronizer](backgound_services.md#run-blockchain-sync) command pulls the updated version of the metadata continuously.  
The **blockchain seed** command is used to support a node that is not configured with the synchronizer process.  

**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain seed from [ip:port]</code></pre>

**Explanation**:  Pull the metadata from a source node.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain seed from 73.202.142.172:7848</code></pre>

**Details**: [Retrieve the Metadata from a source node](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#retrieving-the-metadata-from-a-source-node)

## Add a policy to the metadata

**Usage**:
<pre class="code-frame"><code class="language-anylog">&lt;blockchain insert where 
    policy = [policy] and 
    blockchain = [platform] and 
    local = [true/false] and 
    master = [IP:Port]&gt;
</code></pre>

Identify the metadata platform by including one of these 2 values: 
* blockchain - the blockchain platform to use
* master - the ip and port of the master node.

**Explanation**:  Add a JSON policy to the specified blockchain platform.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain insert where policy = !policy and local = true and master = !master_node
blockchain insert where policy = !policy and local = true and blockchain = ethereum
</code></pre>

**Details**: [Blockchain Insert Command](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-blockchain-insert-command)

## Delete a policy from the metadata

**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain delete policy where id = [policy id] and master = [IP:Port] and local =[true/false] and blockchain = [platform]
</code></pre>

Identify the metadata platform by including one of these 2 values: 
* blockchain - the blockchain platform to use
* master - the ip and port of the master node.

**Explanation**:  Delete a policy from the ledger.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain delete policy where id = 64283dba96a4c818074d564c6be20d5c and master = !master_node
blockchain delete policy where id = 64283dba96a4c818074d564c6be20d5c and local = true and blockchain = ethereum
</code></pre>

**Details**: [The blockchain delete policy command](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-blockchain-delete-policy-command)

## Connect to a blockchain platform
The **blockchain connect** and **blockchain set account info** commands are used to connect to the blockchain platform. 
Ignore these commands if a master node is used.

### Blockchain Connect
**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain connect to [platform] where provider = [provider] and [connection params]</code></pre>

**Explanation**: Connect to the blockchain platform using the connection params.

**Examples**:
<pre class="code-frame"><code class="language-anylog">&lt;blockchain connect to ethereum where 
    provider = https://rinkeby.infura.io/v3/... and 
    contract = 0x3899bED... and 
    private_key = a4caa21209188 ... and 
    public_key = 0x982AF5e15... and 
    gas_read = 3000000 and 
    gas_write = 4000000&gt;</code></pre>

**Details**: [Using Ethereum as a Global Metadata Platform](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md#using-ethereum-as-a-global-metadata-platform).

### Blockchain set Account Info

**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain set account info where platform = [platform name] and [platform parameters]</code></pre>

**Explanation**: Associate account parameters with the blockchain platform.

**Examples**:
<pre class="code-frame"><code class="language-anylog">&lt;blockchain set account info where 
    platform = ethereum and 
    private_key = !private_key and 
    public_key = !public_key and 
    chain_id = 11155111&gt;
</code></pre>

**Details**: [Using Ethereum as a Global Metadata Platform](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md#using-ethereum-as-a-global-metadata-platform).

## Enable a master Node
If a master node is used, prepare a database table called **ledger** to host a local copy of the ledger using the 
**blockchain create table** command.  
If a master node failed, use the **blockchain update dbms** command to update a new master with an existing ledger file.

### blockchain create table

**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain create table</code></pre>

**Explanation**: Create the 'ledger' table on the local **blockchain** DBMS.    
Note: Associate a physical database (like PostgreSQL) to the logical DBMS (**blockchain**) prior to creating the 
ledger table. A physical database is associated to a logical database using the [connect dbms](data_management.md#associate-a-physical-database-to-a-logical-database) command.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain create table</code></pre>

### blockchain update dbms

**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain update dbms [path and file name]</code></pre>

**Explanation**:  Update the local DBMS with the policies in the named file. If file name is not provided, use the default **blockchain.json** file.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain update dbms</code></pre>

## Test that the local copy of the ledger is with correct format
**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain test</code></pre>

**Explanation**:  Validate the structure of the local copy of the ledger.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain test</code></pre>


## Delete a local copy of the ledger 
**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain delete local file</code></pre>

**Explanation**: Delete the local JSON file with the blockchain data.

**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain delete local file</code></pre>

## Retrieve metadata from the ledger

**Usage**:
<pre class="code-frame"><code class="language-anylog">blockchain get [policy type] [where] [attribute name value pairs] [bring] [bring command variables]</code></pre>

**Explanation**:  Get the metadata policies or information from the policies that satisfy the search criteria.


**Examples**:
<pre class="code-frame"><code class="language-anylog">blockchain get *
blockchain get operator where dbms = lsl_demo
blockchain get cluster where table[dbms] = purpleair and table[name] = air_data bring [cluster][id] separator = ,
blockchain get operator bring.table [*] [*][name] [*][ip] [*][port]
blockchain get * bring.table.unique [*]
</code></pre>

**Details**: [Query Policies](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#query-policies).

