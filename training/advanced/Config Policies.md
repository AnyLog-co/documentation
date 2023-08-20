# Configuration Policies

Users can create **config policies** that are stored in the metadata layer. When a node restarts, the node is configured
by the instructions in the policy.

This document demonstrate creating and using config policies that represent the setup and configuration detailed in the
[Network Setup](Network%20Setup.md) document.  

An overview of is available in the [Configuration Policies](../../policies.md#configuration-policies) section.

Note: The config policies can be created on an arbitrary node, however, in this document, we assume the policies
are created on the target node such that we can reference the dictionary keys rather than their associated values.

## Configure a node
If configuration policies are available, when a node start, issue the following command on the CLI:
```anylog
config from policy where id = [Policy ID] 
```

## Creating the master node config policy
Create the policy on the master node.
 
```anylog   
<new_policy = {"config": {
   "name": "master-network-config",
   "company": !company_name,
   "ip": "!external_ip",
   "local_ip": "!ip",
   "port": "!anylog_server_port.int",
   "rest_port": "!anylog_rest_port.int",
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