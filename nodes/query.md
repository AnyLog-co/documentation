# Query Node

The Query Node is an AnyLog / EdgeLake agent that's specifically used for querying data.

The node requires 2 major components: 
1. a logical database called `system_query`
2. a copy of the metadata, in specific clusters and operators, in order to know where to send the request

## Configuring a Query Node

1. Declare `system_query` - when memory or unlogged is set to **True**, then the results of the query are not guaranteed 
if the database crashes. However, having the logical database in memory performance is much faster as the data isn't 
commited.

```anylog
# connect to system_query using sqlite 
connect dbms system_query where type=sqlite and memory=true 

# connect to system_query using PostgresSQL 
connect dbms system_query where type=psql and ip=127.0.0.1 and port=5432 and user=[DB User] and password=[DB password] and unlog=true
```

2. Run a regular blockchain sync to regularly get a copy of the data 

```anylog
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=[Master Node IP and port]
```

## Basic Query Setup

Executing a SQL request consists of 3 parts:
1. Node(s) to get data from - `run client`
2. Logical database and result formatting - `sql [db_name] format=[table | json] and includ=([other tables]) and extend=([other information])`
3. Actual `SELECT` statement 

Example: 
```anylog
run client () sql new_company format=table and extend=(+node_name) "SELECT * FROM rand_data WHERE timestamp >= NOW() - 10 minutes;"
```

Users can specify 
