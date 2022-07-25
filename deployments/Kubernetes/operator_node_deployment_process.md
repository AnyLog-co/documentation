# Deployment Process
The following provides insight the work being done in the background to deploy the Operator node. 

For directions to start an operator node please visit the [operator node](operator_node.md) document.

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
# connect to almgm logical database - for SQLite there's only a need to specify the database type 
connect dbms almgm where type=!db_type and ip=!db_ip and port=!db_port and user=!db_user and password=!db_password

# create tsd_info table 
create table tsd_info where dbms=almgm 
```

4. Connect to the operator database - this is where device data is ultimately stored
```anylog
# for SQLite there's only a need to specify the database type 
connect dbms test where type=!db_type and ip=!db_ip and port=!db_port and user=!db_user and password=!db_password
 
```

5. (Optional) Connect to system_query – <font color="red">Note: the configurations set the `system_query` logical 
database to run directly against the memory. This allows queries to run faster.</font> 
```anylog
# for SQLite there's only a need to specify the database type 
connect dbms system_query where type=!db_type and memory=!memory
```

6. Set scheduler 1 & blockchain sync
```anylog
# init scheduler processes 
run scheduler 1 

# init blockchain sync
run blockchain sync where source=master and time=!sync_time and dest=file and connection=!ledger_conn
```

7. Check if cluster exists & if not create it 
```anylog
# declartion of policy
<new_policy={"cluster": {
    "company": !company_name, 
    "dbms": !default_dbms, 
    "name": !cluster_name, 
    "master": !ledger_conn
}}> 

# check if policy exists 
policy = blockchain get cluster where name=!cluster_name and company=!company_name bring.first

# declare policy if DNE
if not !policy  
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

8. Declare Operator Node on the metadata layer
```anylog
# get ID of cluster policy 
cluster_id = blockchain get cluster where name=!cluster_name and company=!company_name bring.first [cluster][id]

# declartion of policy
<new_policy={"operator": {
    "hostname": !hostname, 
    "name": !node_name, 
    "company": !company_name, 
    "local_ip": !ip, 
    "ip": !external_ip, 
    "port" : !anylog_server_port.int, 
    "rest_port": !anylog_rest_port.int,
    "cluster": !cluster_id, 
    "loc": !loc,
    "country": !country,
    "state": !state, 
    "city": !city
}}> 
# check if policy exists
policy = blockchain get operator where ip = !external_ip and local_ip = !ip and company=!company_name and port=!anylog_server_port

# declare policy if DNE
if not !policy then
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and
```

9. Set partitioning of the data & schedule to drop old partitions once a day
```anylog 
# set partiitons
partition !default_dbms !table_name using !partition_column by !partition_interval

# set scheduler to drop partition 
schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep
```

10. Run MQTT 
```anylog 
<run mqtt client where broker=local and port=!port and log=!mqtt_log and topic=(
   name=!mqtt_topic_name and 
   dbms=!mqtt_topic_dbms and 
   table=!mqtt_topic_table and 
   column.timestamp.timestamp=!mqtt_column_timestamp and 
   column.value=(value=!mqtt_column_value and type=!mqtt_column_value_type)
)>
```

11. Start Operator - There are 3 steps need to start the operator process:
   * `set buffer threshold` –  By setting the threshold to immediate, data (new) coming in will be stored within the operator database with no delay, whereas when disabled it takes up to 60 seconds for new data to be stored in the database. 
   * `run data distributor` – The distributor tells the node to share its data with other operator instances connected to the same cluster (if  HA  is enabled). In the case of this demo, each of the (two) operators deployed is correlated to a different cluster without HA. 
   * `run operator` – This is the only required step, as it informs the node that it needs to host data. 
```anylog
set buffer threshold where write_immediate = true

run data distributor  # Optional

operator_id = blockchain get operator where ip = !external_ip and local_ip = !ip and company=!company_name and port=!anylog_server_port bring [operator][id] 
run operator where create_table=true and update_tsd_info=true and archive=true and distributor=true and master=!ledger_conn and policy=!operator_id
```