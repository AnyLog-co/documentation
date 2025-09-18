# Publisher Node

Publisher node(s) are AnyLog only agents that allow distributing data across different operators. 

The main reason someone would use a Publisher as opposed to a (small) Operator node is when data needs to be broadcast 
to multiple operators that reside in different clusters. In addition, operator nodes are more resource heavy. 

It is important to note that data cannot be queried from within the publisher, it is stored / queried against he [operator](operator.md); 
but, it can be [aggregated](../monitoring/aggregations.md) on the publisher, **before** being stored on operator. 

## Steps
0. Make sure machines in the network can communicate with one another. If they're able to communicate over the local IP 
(`!ip`) then it's recommended to set binding to True, else binding should be False for TCP. 

1. Enable TCP service 
```anylog
<run tcp server where 
    external_ip=!external_ip and external_port=32148 and 
    internal_ip=!ip and internal_port=32148 and 
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

3. (Optional) Create Policy

* **Step 1**: Create policy 
```anylog
<new_policy = create policy query where 
    name=publisher-node and 
    company="My Company" and 
    ip=!external_ip and
    local_ip=!ip and 
    port=32248 and
    rest_port=32249>
```

If TCP bind is **True** then use the following policy: 
```anylog
<new_policy = create policy publisher where 
    name=query-node and 
    company="My Company" and 
    ip=!ip and 
    port=32248 and
    rest_port=32249>
```

* **Step 2**: Publish policy
```anylog
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

4. Enable Publisher service - note that a publisher is the only service that cannot reside with an operator (and vis-a-versa). 
All other AnyLog / EdgeLake services can coexist on the same agent. 

```shell
run streamer 

<run publisher where 
  archive_json=true and compress_json=true and 
  archive_sql=true and compress_sql=true and 
  dbms_name=file_name[0] and table_name=file_name[1]
```
> `dbms_name` and `table_name` are the relative location in the file_name where information resides. Default `db_name.table_name.0.0.json`

5. (Optional) Automatically remove old archived files older than X number of days
```anylog
schedule name=remove_archive and time=1 day and task delete archive where days = 30
```
