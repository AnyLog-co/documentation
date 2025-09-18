# Using a Master Node

Nodes in an AnyLog network communicate by knowing each other’s access details — such as `ip:port`, access keys, and data 
locations — all over TCP. This information is usually stored on a shared ledger (a blockchain).

A blockchain ensures true decentralization since no single node holds the entire ledger. However, it also comes with 
costs: immutability, transaction fees for reads/writes, and deployment complexity at scale.

To simplify deployment, AnyLog supports a Master Node: a designated node that stores and shares metadata for the network, 
without requiring a full blockchain. Nodes still communicate directly with one another; the Master Node is only 
responsible for managing metadata.

In large-scale deployments, a Master Node can also act as a relay between the blockchain layer and subsets of nodes.

This document describes how to deploy a standalone Master Node instance for a pre-production network.

## Configuring a Master Node

Due to the service-based logic around AnyLog, nodes can act as multiple node types and require only a blockchain logical 
database and ledger table. In addition, other nodes should have permissions to access the master node. 

By default, these steps are done automatically when a node is deployed using [deployment-scripts](https://github.com/AnyLog-co/deployment-scripts)

When deploying a test network and / or an EdgeLake setup, then security processes are limited and not something to deal 
with. Please review our [security]() section for farther details.

1. Enable TCP service 
```anylog
<run tcp server where 
    external_ip=!external_ip and external_port=32048 and 
    internal_ip=!ip and internal_port=32048 and 
    bind=false and threads=3> 
```

2. Enable synchronization - this is a separate service that is to run on all nodes, allowing them to consistently get a 
copy of the blockchain ledger every X seconds.

```anylog
<run blockchain sync where 
    source=master and 
    time="30 seconds" and 
    dest=file and 
    connection=!ledger_conn>
```
> `!ledger_conn` is the TCP service IP and Port for the master node. Directions for using the blockchain can be found [here]().


3. Create a logical database called `blockchain`

**When using SQLite**:
```anylog 
connect dbms blockchain where type=sqlite
```

**Using using PostgresSQL**:
```anylog 
<connect dbms blockchain where 
    type=psql and 
    ip=127.0.0.1 and 
    port=5432 and 
    user=[db user] and 
    password=[db password]>
```

4. Create a table called `ledger` within `blockchain` database - the table definition is hardcoded within AnyLog / EdgeLake code. 
```anylog
create table ledger where dbms=blockchain
```

5. (Optional) Create & publish a policy with information about the master node 
* **Step 1**: Create policy 
```anylog
<new_policy = create policy master where 
    name=master-node and 
    company="My Company" and 
    ip=!external_ip and
    local_ip=!ip and
    port=32048 and 
    rest_port=32049>
```

If TCP bind is **True** then use the following policy
```anylog
<new_policy = create policy master where 
    name=master-node and 
    company="My Company" and 
    ip=!ip and
    port=32048 and 
    rest_port=32049>
```

* **Step 2**: Publish policy
```anylog
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
> `!ledger_conn` is the TCP service IP and Port for the master node. Directions for using the blockchain can be found [here]().

6. Enable synchronization - this is a separate service that is to run on all nodes, allowing them to consistently get a 
copy of the blockchain ledger every X seconds.
```anylog
<run blockchain sync where 
    source=master and 
    time="30 seconds" and 
    dest=file and
    connection=!ledger_conn>
```

## Synchronizing a local copy of the blockchain

Nodes maintain a local copy of the ledger in a JSON file. The file name and location is declared in the local
dictionary using `!blockchain_file`. A node can enable a synchronization process (shown in step 5) between the master or 
blockchain and the local agent. This process periodically pulls the policies from the blockchain source (master or 
blockchain) and stores it locally. 

The synchronization process is detailed at [blockchain synchronizer]().  
