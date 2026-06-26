# Common Issues

### Attempting to run a query and getting an error message

**Error Type 1**: `Failed to load table metadata from blockchain` 

```AnyLog
AL query +> run client () sql my_db "select count(*) from t1;"
Failed to load table metadata from blockchain
AL query +> get error log
ID     Count Thread     Time                     Type  Text                                                                                                 
------|-----|----------|------------------------|-----|----------------------------------------------------------------------------------------------------|
702271|    1|MainThread|Mon May 26 20:52:20 2025|Error|Failed to retrieve table definition from metadata policy for table: 'my_db.t1'                      |
702272|    1|MainThread|Mon May 26 20:52:20 2025|Error|Failed to get metadata info from Table Policy with DBMS: 'my_db' and Table: 't1'                    |
702273|    1|MainThread|Mon May 26 20:52:20 2025|Error|(Failed: Failed to load table metadata from blockchain) run client () sql my_db "select count(*) fro|
      |     |          |                        |     |m t1;"                                                                                              |
```

In this situation, the metadata information is yet to be accessible usually due to buffer / blockchain sync time, time between the nodes. 
This issue resolves itself once data is processed and node is synced against the blockchain.
    
**Error Type 2**: `Local query database not available: 'system_query'`

```AnyLog
AL query +> run client () sql my_db "select count(*) from t1;" 
AL query +> DBMS not open
AL query +> get error log 
ID     Count Thread     Time                     Type  Text                                                                     
------|-----|----------|------------------------|-----|--------------------------------------------------------------------------|
698413|    1|MainThread|Mon May 26 20:45:56 2025|Error|Local query database not available: 'system_query'                        |
698414|    1|MainThread|Mon May 26 20:45:56 2025|Error|(Failed: DBMS not open) run client () sql my_db "select count(*) from t1;"|
```

In this situation, the user is missing the `system_query` logical database, which is used to aggregate results from operator node(s).
Details can be found in [SQL Setup](../sql%20setup.md#system-databases-and-system-tables).

```AnyLog
connect dbms system_query where type=sqlite and memory=true
```

### Why is data result in consistent? 

When users deploy multiple operators they sometimes notice the data coming in from only 1 out of 2 of the operators, but 
the data isn't consistent. specifically the data appears and then disappears. This is most commonly due to the operators
sharing a cluster name, but HA is not enabled. There are 2 ways to resolve this: 

**Option 1**: When running AnyLog you can enable by either restarting the operator nodes with HA enabled or running 
the following commands on operator nodes
```AnyLog
run data distributor
run data consumer where start_date=!start_data
```

**Option 2**: Restart the second operator with a new cluster name - this would work for EdgeLake
1. Attach to the node 
```AnyLog
docker attach --detach-keys=ctrl-d edgelake-operator2
```

2. Drop operator policy for the node 
```anylog
operator_id = blockchain drop policy where name = edgelake-operator2 bring [*][id]
run client (!ledger_conn) blockchcain drop policy where id=!operator_id 
```

3. Detach from container - `ctrl-d` 
4. Stop Operator - `docker stop edgelake-operator2`
5. Remove blockchain volume - `docker volume rm docker-comose_edgelake-operator2-anylog-blockchain`

6. In the (basic) configuration file for operator 2, update the cluster name 

7. Start Operator 2
```shell
make up ANYLOG_TYPE=operator2 
```