# Deployment Process
The following provides insight the work being done in the background to deploy the Publisher node. 

For directions to start an operator node please visit the [publisher node](publisher_node.md) document.

## Steps
1. Set parameters such as 
   * hostname 
   * Local & external IP 
   * ENV parameters from configuration into AnyLog parameters
 
  
2. Connect to TCP, REST and Message broker (if configured) 
```anylog
run tcp server !external_ip !anylog_server_port !ip !anylog_server_port
run rest server !ip !anylog_rest_port

# Connect to message broker if configured
run message broker !external_ip !anylog_server_port !ip !anylog_server_port
```

3. Connect to databases almgm and create tsd_info table – <font color="red">`almgm.tsd_info` contains all metadata 
information about files injested. Other tables in almgm contain information regarding data ingested in peer  nodes in 
the same  cluster.</font>
```anylog
# connect to almgm logical database 
connect dbms !db_type !db_conn !db_port almgm

# create tsd_info table 
create table tsd_info where dbms=almgm 
```

4. (Optional) Connect to system_query – <font color="red">Note: the configurations set the `system_query` logical 
database to run directly against the memory. This allows queries to run faster.</font> 
```anylog
connect dbms sqlite system_query where memory=true
```

5. Set scheduler 1 & blockchain sync
```anylog
# init scheduler processes 
run scheduler 1 

# init blockchain sync
run blockchain sync where source=master and time=!sync_time and dest=file and connection=!ledger_conn
```

6. Declare Publisher Node on the metadata layer
```anylog
# get ID of cluster policy 
<new_policy={"publisher": {
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
policy = blockchain get publisher where ip = !external_ip and local_ip = !ip and company=!company_name and port=!anylog_server_port

# declare policy if DNE
if not !policy then
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and
```

7. Run MQTT 
```anylog 
<run mqtt client where broker=rest and port=!port and log=!mqtt_log and topic=(
   name=!mqtt_topic_name and 
   dbms=!mqtt_topic_dbms and 
   table=!mqtt_topic_table and 
   column.timestamp.timestamp=!mqtt_column_timestamp and 
   column.value=(value=!mqtt_column_value and type=!mqtt_column_value_type)
)>
```

8. Start Publisher - There are 3 steps need to start the operator process:
   * `set buffer threshold` –  By setting the threshold to immediate, data (new) coming in will be stored within the 
   operator database with no delay, whereas when disabled it takes up to 60 seconds for new data to be stored in the 
   database. 
   * `run data distributor` – The distributor tells the node to share its data with other operator instances connected 
   to the same cluster (if  HA  is enabled). In the case of this demo, each of the (two) operators deployed is 
   correlated to a different cluster without HA. 
   * `run publisher` – This is the only required step, as it informs the node to send data to the relevant operator nodes.  
```anylog
set buffer threshold where write_immediate = true

run data distributor  # Optional

run publisher where compress_json=!compress_file and compress_sql=!compress_file and  master_node=!ledger_conn and dbms_name=!dbms_file_location and table_name=!table_file_location
```
 