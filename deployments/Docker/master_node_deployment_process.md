# Deployment Process
The following provides insight the work being done in the background to deploy the Master node. 

For directions to start a master node please visit the [master node](master_node.md) document.

## Steps
1. Set parameters such as 
   * hostname 
   * Local & external IP 
   * ENV parameters from configuration into AnyLog parameters

   
2. Connect to TCP & REST 
```anylog
run tcp server !external_ip !anylog_server_port !ip !anylog_server_port
run rest server !ip !anylog_rest_port
```

3. Connect to blockchain database & create ledger table – Note: blockchain.ledger contains the metadata policies. 
For example, the different node types connected to the network & data tables associated with each node.
```anylog
# connect to logical database 
connect dbms !db_type !db_conn !db_port blockchain

# create ledger table  
create table ledger where dbms=blockchain
```

4. (Optional) Connect to system_query – <font color="red">Note: the configurations set the `system_query` logical 
database to run directly against the memory. This allows queries to run faster.</font> 
```anylog
connect dbms sqlite system_query where memory=true
```

5. Set scheduler & blockchain sync
```anylog
# init scheduler processes 
run scheduler 1 

# init blockchain sync
run blockchain sync where source=master and time=!sync_time and dest=file and connection=!ledger_conn
```

6. Declare the Master in the metadata (Master Node Policy)
```anylog
# declaration of policy
<new_policy={"master": {
   "hostname": !hostname, 
   "name": !node_name, 
   "ip" : !external_ip, 
   "local_ip": !ip, 
   "company": !company_name, 
   "port" : !anylog_server_port.int, 
   "rest_port": !anylog_rest_port.int, 
   "loc": !loc,
   "country": !country,
   "state": !state, 
   "city": !city
}}>

# check if policy exists  
policy = blockchain get master where ip = !external_ip and local_ip = !ip and company=!company_name and port=!anylog_server_port 

# declare policy if DNE
if not !policy then 
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
