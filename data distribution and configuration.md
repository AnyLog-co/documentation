
# Data Distribution and Configuration

The distribution of data to nodes in the network is determined by policies published on the blockchain.  
A policy is a structure that determines how nodes needs to treat or process data or information that is required during the processing of the data.     
Each policy is a JSON object that is structured as nested dictionaries. The root dictionary has one attribute that determines the type of the policy and the children provide the content of the policy.  

There are 2 ways to represent how data is distributed.
1. Assigning data to Operators - using this approach, Operators declare the tables they support and the data is distributed to the relevant operators.  
This method does not offer the High Availability (HA) features and is usually used for testing.  
2. Declaring Clusters and assigning Operators to Clusters - this is the recommended approach for production as it offers redundancy and High Availability (HA).

## The organization of the data for HA

Users view the data as if it is organized in tables assigned to databases.  
The physical organization of the data partitions the data to clusters. Each of the clusters is supported by multiple Operators
that maintain identical copies of the cluster's data. Therefore if an Operator nodes fails, the cluster's data is available on a surviving node.    
The way data is treated is as follows:  
* Data is assigned to a logical table.
* Each table is assigned to one or more clusters. With N clusters assigned to a table, the table's data is partitioned to N.
* Each cluster is assigned to X operators. If X is 4, there are 4 copies of the cluster's data, one on each assigned Operator.

In the example below, the data of tables 1-4 is distributed to 2 clusters. Each cluster will have approximately half of the data.    
The data of each cluster is maintained by 2 Operators such that if an Operator fails, the data remains available with the second Operator
(and based on the policies, the network protocol will initiate a new Operator and a process to replicate the data to the new Operator).

<pre>
|--------------------|          |--------------------|          |--------------------|  
|                    |          |                    |   --->   |     Operator 1     |          
|                    |   --->   |                    |          |--------------------|  
|                    |          |      Cluster 1     |  
|      Table 1       |          |                    |          |--------------------|  
|                    |          |                    |   --->   |     Operator 2     |  
|      Table 2       |          |--------------------|          |--------------------|  
|                    |  
|      Table 3       |          |--------------------|          |--------------------|  
|                    |          |                    |   --->   |     Operator 3     |  
|      Table 4       |          |                    |          |--------------------|  
|                    |          |      Cluster 2     |  
|                    |   --->   |                    |          |--------------------|  
|                    |          |                    |   --->   |     Operator 4     |  
|--------------------|          |--------------------|          |--------------------|  
</pre>

## Prerequisites

* A set of policies published on the blockchain that determine how data is distributed.
* The participating Operators are connected to the network.
To view connection information issue the following command:  
```get connections``` on each participating operator.  
* Operators that host data are configured to provide a local database service.  
For example, to support a database called ***lsl_data*** using PotgreSQL, the ***connect dbms*** is called as follows:  
``` connect dbms psql !db_user !db_port lsl_data```  
To view connected databases call:  
```get databases```
 
## Assigning data to Operators

Using the first method, Operators declare the tables supported using a policies as the example below:

### Example

<pre>
{"operator" : {
    "dbms" : "lsl_data"
    "table" : ["ping_sensor", "percentage_cpu", "pressure_sensor"],
    "ip" : "10.0.0.25",
    "port" : "2048"
    }
}>
</pre>

When data is distributed to a table or is being queried, all the relevant Operators will participate in the process.

## Declaring Clusters and assigning Operators to Clusters 

This method declares clusters, assigns Operators to Clusters and provides redundancy and HA.  
A CLuster is a policy that groups together the following:
1. A set of tables.
2. A set of Operators that will maintain the cluster data.

Declaring clusters and assigning Operators to each cluster can be done in 2 ways:
1.  Listing the tables on each Cluster Policy and assigning the Operators to the cluster.
2.  Listing the tables on the Operator's Policies and assigning the Operators to the cluster.  

### Declaring the Cluster's tables
With method 1, the cluster policy includes a list of tables that are supported. The tables are identified by:  
***company*** - the name of the company that owns the data (optional).  
***dbms*** - the name of the logical database that hosts the data.  
***name*** - the name of the logical table that hosts the data.  
With method 2, the cluster policy includes compamy name only. Tables will be assigned to the cluster using the Policies of the Operators.


### Assigning Operators to Clusters
The Cluster policy determines the logical distribution of the data. The assignments of nodes is by declaring Operators with the ID of the Cluster they manage.  
The Cluster ID is generated when the Cluster policy is added to the blockchain.  
Operators associated to a cluster are identified uniquely by a Member ID.   
The Member ID is generated automatically and is used to uniquely Identify a member of the cluster (using a shorter ID than the Node ID).  

## Activating the policies

When the policies are declared they become available to the relevant nodes using one of the methods that distributes the blockchain updates.  
For example, by configuring the nodes to use the blockchain synchronizer using the command:
<pre>
run blockchain sync
</pre>
Information on the Synchronizer process is available at [background processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#blockchain-synchronizer).  
The Synchronizer process will automatically update the metadata by the policies declared.
To manually force the updated policies, use the command:
<pre>
blockchain load metadata
</pre>

## View data distribution policies
The command below provides a visual chart of how data is distributed to nodes in the network:
<pre>
blockchain query metadata
</pre>
The command presents a hierarchical view of how the data is distributed:
<pre>
|-- Company --|   |-- DBMS  --|     |------ Table -----|     |------------- Cluster ID and Name------------|    |--- Operator Connection, Member ID, Status ---|     
litsanleandro ==> litsanleandro ==> ping_sensor          ==> 2436e8aeeee5f0b0d9a55aa8de396cc2 (lsl-cluster1) ==> 139.162.126.241:2048       [0206  local  active]
                                                                                                                                            [0008  remote active]
                                                         ==> 8ceb5aecc8d2a739099551cf48fed201 (lsl-cluster2) ==> 139.162.164.95:2048        [0168  remote active]
                                                                                                                                            [0015  remote active]
                                                         ==> 5631d115eb456882a6c6f0173808e63f (lsl-cluster3) ==> 172.105.13.202:2048        [0243  remote active]
                                                                                                                                            [0012  remote active]
                                ==> percentagecpu_sensor ==> 2436e8aeeee5f0b0d9a55aa8de396cc2 (lsl-cluster1) ==> 139.162.126.241:2048       [0206  local  active]
                                                                                                                                            [0008  remote active]
                                                         ==> 8ceb5aecc8d2a739099551cf48fed201 (lsl-cluster2) ==> 139.162.164.95:2048        [0168  remote active]
                                                                                                                                            [0015  remote active]
                                                         ==> 5631d115eb456882a6c6f0173808e63f (lsl-cluster3) ==> 172.105.13.202:2048        [0243  remote active]
                                                                                                                                            [0012  remote active]

</pre>

## Test Cluster policies
The command below tests the validity of the Cluster policies:
<pre>
blockchain test metadata
</pre>

## Example Policies

The following example declares the following:  
1. 2 tables: cos_data and sin_data.  
2. 2 clusters, the first supports the 2 tables and the second supports cos_data only.  
3. 3 Operators - 2 Operators supporting the first cluster and 1 operator supporting the second cluster.  

#### Declaring the tables
<pre>
{"table": {"create": "CREATE TABLE IF NOT EXISTS cos_data(  row_id SERIAL "
                      "PRIMARY KEY,  insert_timestamp TIMESTAMP NOT NULL "
                      "DEFAULT NOW(),  timestamp TIMESTAMP NOT NULL DEFAULT "
                      "NOW(),  value FLOAT ); CREATE INDEX "
                      "cos_data_timestamp_index ON cos_data(timestamp); CREATE "
                      "INDEX cos_data_insert_timestamp_index ON "
                      "cos_data(insert_timestamp);",
            "dbms": "purpleair",
            "id": "c096ee7b923554382cb1cf875f13278a",
            "name": "cos_data"}}


{"table": {"create": "CREATE TABLE IF NOT EXISTS sin_data(  row_id SERIAL "
                      "PRIMARY KEY,  insert_timestamp TIMESTAMP NOT NULL "
                      "DEFAULT NOW(),  timestamp TIMESTAMP NOT NULL DEFAULT "
                      "NOW(),  value FLOAT ); CREATE INDEX "
                      "sin_data_timestamp_index ON sin_data(timestamp); CREATE "
                      "INDEX sin_data_insert_timestamp_index ON "
                      "sin_data(insert_timestamp);",
            "dbms": "purpleair",
            "id": "e46d9b768d7eef2abaacb17b251191aa",
            "name": "sin_data"}}

</pre>

#### Declaring the Clusters
<pre>
{"cluster" : {
                "company" : "anylog",
                "status" : "active",
                "table" : [
                            { "name" : "cos_data",
                              "dbms" : "purpleair",
                               "distribution" : 1,
                               "status" : "active",
                               "start_date" : "2020-11-08"
                            },
                            { "name" : "sin_data",
                               "dbms" : "purpleair",
                               "distribution" : 1,
                               "status" : "active",
                               "start_date" : "2020-11-08"
                            }
                ]

    }
}

cluster = {"cluster" : {
                "company" : "anylog",
                "status" : "active",
                "table" : [
                            { "name" : "cos_data",
                               "dbms" : "purpleair",
                               "distribution" : 2,
                               "status" : "active"
                            }
                            ]

    }
}
</pre>

#### Declaring the Operators

<pre>
{"operator" : {
    "cluster" : "6c67e2982a69f606107d3c0f50aae8cc",
    "member" : 1,
    "ip" : "10.0.0.25",
    "port" : "2048"
    }
}

{"operator" : {
    "cluster" : "6c67e2982a69f606107d3c0f50aae8cc",
    "member" : 2,
    "ip" : "10.0.0.87",
    "port" : "2048"
    }
}

{"operator" : {
    "cluster" : "56142ddfa243bb3bc8c6688848af01db",
    "member" : 1,
    "ip" : "10.0.0.169",
    "port" : "2148"
    }
}
</pre>

