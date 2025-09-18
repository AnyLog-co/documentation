# Operator Node

Operator node(s) are Anylog / EdgeLake agents that are dedicated to managing the actual data both at the edge and in the 
cloud. 

The idea is that data (both time-series and blobs) is pushed into the operator either directly or via a 
[publisher node](publisher.md) and then stored on the local database. 

Once data is stored on the operator, the agent is then used to query the local data for the _Query node_, as well as 
manage data partitioning and shared distribution (high-availability for AnyLog). 

## Steps to Deploy Operator
0. Make sure machines in the network can communicate with one another. If they're able to communicate over the local IP 
(`!ip`) then it's recommended to set binding to True, else binding should be False for TCP. 

1. Enable TCP service 
```anylog
<run tcp server where 
    external_ip=!external_ip and external_port=32148 and 
    internal_ip=!ip and internal_port=32148 and 
    bind=false and threads=3> 
```

2. Declare Cluster Policy
* **Step 1**: Create policy 
```anylog
<new_policy = create policy cluster where 
    name=my-cluster and 
    company="My Company">  
```

* **Step 2**: Publish policy
```anylog
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

3. Declare Operator policy
* **Step 1**: Get cluster policy ID - Operators that are part of an HA configuration with one another will have the same
Cluster ID. While operators that that are not part of the same HA configuration should have unique cluster IDs.  
```anylog 
cluster_id = blockchain get cluster where name=my-cluster and company="My Company" bring.first [*][id]
```

* **Step 2**: Create Operator policy 
```anylog
<new_policy = create policy operator where
    name=my-operator1 and
    company="My Company" and 
    cluster=!cluster_id and 
    ip=!external_ip and
    local_ip=!ip and
    port=!anylog_server_port>
```

If TCP bind is **True** then use the following policy: 
```anylog
<new_policy = create policy operator where
    name=my-operator1 and
    company="My Company" and 
    cluster=!cluster_id and 
    ip=!ip and
    port=32148>
```


* **Step 3**: Declare Operator Policy
```anylog
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
> `!ledger_conn` is the TCP service IP and Port for the master node. Directions for using the blockchain can be found [here]().


4. Create logical database(s) to store data 
* Create `almgm.tsd_info` logical table and database - this is used to keep a record of the data flowing in, both in 
order to not have repeating data (files) and when sharing data across operators for high-availability

**SQLite database**
```anylog 
connect dbms almgm where type=sqlite
create table tsd_info where dbms=almgm
```

**PostgresSQL Database**
```anylog
<connect dbms almgm where 
    type=psql and 
    ip=127.0.0.1 and 
    port=54332 and 
    user=[DB user] and 
    password=[DB password]> 
create table tsd_info where dbms=almgm
```

5. Connect to local database - this is where real-time /device data will be stored

**SQLite database**
```anylog 
connect dbms mydb where type=sqlite
```

**PostgresSQL Database**
```anylog
<connect dbms mydb where 
    type=psql and 
    ip=127.0.0.1 and 
    port=54332 and 
    user=[DB user] and 
    password=[DB password]> 
```

**MongoDB Database** - When deploying with MongoDB, it is the same name as the PostgresSQL / SQLLite database name, but 
the system automatically recognizes it as `[DB Name]_blobs`. 
```anylog
<connect dbms mydb where 
    type=mongo and 
    ip=127.0.0.1 and 
    port=27017 and 
    user=[DB user] and 
    password=[DB password]> 
```

6. Accept blobs data 
```anylog
<run blobs archiver where
    dbms=!mydb and
    folder=[true - if not stroed to mongo | false - if stored to mongo] and
    compress=true and
    reuse_blobs=true  
>
```
> `reuse_blobs` means that if an image repeats itself (identical hash value) then reuse rather than save duplicate 

7. (Optional) For AnyLog **only**, enable high-availability (HA). This includes sending data to other operators that reside 
in the same cluster group, and accepting data from operators that reside in the same cluster group. The logical database 
`almgm` (from step  4) makes sure the same data isn't being repeatedly ping-ponged between operators. 
```anylog 
run data distributor
run data consumer where start_date="-30" 
```
> `start_date` is number of days back to start consuming data from other operators from 

8. Run the actual operator service
```anylog 
operator_id = blockchain get operator where cluster=!cluster_id and name=my-operator1 and company="My Company" bring.last [*][id]

<run operator where 
    create_table=true and update_tsd_info=true and 
    compress_json=true and compress_sql=true and 
    archive_json=true and archive_sql=true and 
    master_node=!ledger_conn and policy=!operator_id and 
    threads=6>
```

