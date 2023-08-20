# Configuration Policies

Users can create **config policies** that are stored in the metadata layer. When a node restarts, the node is configured
by the instructions in the policy.

This document demonstrates creating and using config policies that represent the setup and configuration detailed in the
[Network Setup](Network%20Setup.md) document.  

An overview of is available in the [Configuration Policies](../../policies.md#configuration-policies) section.

Note: The config policies can be created on an arbitrary node, however, in this document, we assume the policies
are created on the target node such that we can reference the dictionary keys rather than their associated values.

## Configure a node
If configuration policies are available, when a node start, issue the following command on the CLI:
```anylog
config from policy where id = [Policy ID] 
```
Example:
```anylog
master_policy_id = master_policy_id = blockchain get config where name = master-network-config bring [config][id]
config from policy where id = !master_policy_id
```


## Creating the Master Node config policy
Create the policy on the Master Node.
 
```anylog   
<new_policy = {"config": {
   "name": "master-network-config",
   "company": !company_name,
   "ip": !external_ip,
   "local_ip": !ip,
   "port": !anylog_server_port.int,
   "rest_port": !anylog_rest_port.int,
    "script" : [
                "set authentication off",
                "set echo queue on",
                "set node_name = !node_name",
                "set company_name =  !company_name",            
                "set ledger_conn = !ledger_conn",
                "connect dbms blockchain where type=sqlite",
                "run scheduler 1",
                "run blockchain sync where source=master and time=\"30 seconds\" and dest=file and connection=!ledger_conn"
    ]
}}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

## Creating the Query Node config policy
Create the policy on the Query Node.
 
```anylog   
<new_policy = {"config": {
   "name": "query-network-config",
   "company": !company_name,
   "ip": !external_ip,
   "local_ip": !ip,
   "port": !anylog_server_port.int,
   "rest_port": !anylog_rest_port.int,
    "script" : [
                "set authentication off",
                "set echo queue on",
                "set node_name = !node_name",
                "set company_name =  !company_name",            
                "set ledger_conn = !ledger_conn",
                "connect dbms system_query where type=sqlite and memory=true",
                "run scheduler 1",
                "run blockchain sync where source=master and time=\"30 seconds\" and dest=file and connection=!ledger_conn"
    ]
}}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

## Creating the Operator Node config policy
Create the policy on the Operator Node.

Because the operator process is with multiple variables, for convenience, we organize ir in a code block
and associate it with a key in the dictionary.
```anylog 
<operator_process = "run operator where
    create_table=true and
    update_tsd_info=true and
    compress_json=true and
    compress_sql=true and 
    archive=true and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads = !operator_threads"
> 
```

 
```anylog   
<new_policy = {"config": {
   "name": "operator-network-config",
   "company": !company_name,
   "ip": !external_ip,
   "local_ip": !ip,
   "port": !anylog_server_port.int,
   "rest_port": !anylog_rest_port.int,
    "script" : [
                "set authentication off",
                "set echo queue on",
                "set node_name = !node_name",
                "set company_name =  !company_name",            
                "set ledger_conn = !ledger_conn",
                "set default_dbms = test",
                "connect dbms almgm where type=sqlite",
                "connect dbms !default_dbms where type=sqlite",
                "partition !default_dbms * using insert_timestamp by 1 day",
                "run scheduler 1",
                "run blockchain sync where source=master and time=\"30 seconds\" and dest=file and connection=!ledger_conn",
                "operator_id = blockchain get operator where name=operator1-node and company=!company_name  bring.first [*][id]",
                "set buffer threshold where time=60 seconds and volume=10KB and write_immediate=true",
                " !operator_process"
    ]
}}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```