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

4. (Optional) Connect to system_query – _Note: the configurations set the system_query logical database to run directly against 
the memory. This allows queries to run faster._
