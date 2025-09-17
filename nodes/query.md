# Query Node

The Query Node is an AnyLog / EdgeLake agent that's specifically used for querying data.

The node requires 2 major components: 
1. a logical database called `system_query`
2. a copy of the metadata, in specific clusters and operators, in order to know where to send the request


Since a "Query node" is a node that simply has a copy of the blockchain metadata and a `system_query` logical database 
any AnyLog / EdgeLake agent can run as a query node. When deploying via containers, it's a simple True/False parameter 
in the configurations.

## Configuring a Query Node

1. Declare `system_query` - when memory or unlogged is set to **True**, then the results of the query are not guaranteed 
if the database crashes. However, having the logical database in memory performance is much faster as the data isn't 
commited.

```anylog
# connect to system_query using sqlite 
connect dbms system_query where type=sqlite and memory=true 

# connect to system_query using PostgresSQL 
<connect dbms system_query where 
    type=psql and 
    ip=127.0.0.1 and 
    port=5432 and 
    user=[DB User] and 
    password=[DB password] and 
    unlog=true>
```

2. Run a regular blockchain sync to regularly get a copy of the data 

```anylog
<run blockchain sync where 
    source=master and 
    time="30 seconds" and 
    dest=file and 
    connection=!ledger_conn>
```
`!ledger_conn` is the TCP service IP and Port for the master node. Directions for using the blockchain can be found [here]().


3. (Optional) Create & publish a policy with information about the query node 
* **Step 1**: Create policy 
```anylog
<new_policy = create policy query where 
    name=query-node and 
    company="My Company" and 
    ip=!ip and 
    port=!anylog_server_port and
    ret_port=!anylog_rest_port>
```

* **Step 2**: Publish policy
```anylog
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

## Basic Query Setup

Executing a SQL request consists of 3 parts:
1. Node(s) to get data from - `run client`
2. Logical database and result formatting - `sql [db_name] format=[table | json] and includ=([other tables]) and extend=([other information])`
3. Actual `SELECT` statement 

**Example**: 
```anylog
run client () sql new_company "SELECT * FROM rand_data WHERE timestamp >= NOW() - 10 minutes;"
```

Inside the parentheses of the `run client ()` users can specify which nodes to send the request against. If the 
parentheses remain empty then the system automatically knows where to send requests via information provided by the 
blockchain. 

For more advanced query functionality, checkout [querying ddata]() document. 
