# Deployment Process
The following provides insight the work being done in the background to deploy the Query node. 

For directions to start a master node please visit the [query node](query_node.md) document.

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

3. Connect to system_query – <font color="red">Note: the configurations set the `system_query` logical 
database to run directly against the memory. This allows queries to run faster.</font> 
```anylog
# for SQLite there's only a need to specify the database type 
connect dbms system_query where type=!db_type and memory=!memory
```

4. Set scheduler & blockchain sync
```anylog
# init scheduler processes 
run scheduler 1 

# init blockchain sync
run blockchain sync where source=master and time=!sync_time and dest=file and connection=!ledger_conn
```

5. Declare the Query in the metadata (Query Node Policy)
```anylog
# declaration of policy
<new_policy={"query": {
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
policy = blockchain get query where ip = !external_ip and local_ip = !ip and company=!company_name and port=!anylog_server_port 

# declare policy if DNE
if not !policy then 
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```