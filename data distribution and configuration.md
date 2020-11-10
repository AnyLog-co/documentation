
# Data Distribution and Configuration

The distribution of data to nodes in the network is determined by policies published on the blockchain.  
A policy is a JSON object that is structured as a nested dictionaries. The root dictionary has one attribute that determines the type of the policy and the children are structured as needed to describe the policy.  

There are 2 ways to represent how data is distributed.
1. Assigning data to Operators - using this approach, Operators declare the tables they support and the data is distributed to the relevant operators.  
This method does not offer the High Availability (HA) features and is usually used for testing.  
2. Declaring Clusters and assigning Operators to Clusters - this is the recomended approach for production as it offers redundancy and HA.  

## Prerequisites

* A set of policies published on the blockchain that determine how data is distributed.
* The participating Operators are connected to the network.
To view connection information issue the following command:  
```show connections``` on each participating operator.  
* Operators that host data are configured to provide a local database service.  
For example, to support a database called ***lsl_data*** using PotgreSQL, the ***connect dbms*** is called as follows:  
``` connect dbms psql !db_user !db_port lsl_data```  
To view connected databases call:  
```show databases```
 
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
A CLuster is a policy that determines the following:
1. A set of tables that are supported by the Cluster Members.
2. For each table, the portion of the data that will be provided to the Cluster Members for hosting.

### Declaring the Cluster's tables
The cluster policy includes a list of tables that are supported. The tables are identified by:  
***company*** - the name of the company that owns the data (optional).  
***dbms*** - the name of the logical database that hosts the data.  
***name*** - the name of the logical table that hosts the data.  

### The distribution ID
For each table, the policy provides a distribution ID. The distribution ID determines the portion of the table's data that will be managed by the cluster.    
With N Clusters, each Cluster maintains a distribution ID (a number in the range 1 to N), the table's data will be split to N and each Cluster will receive approximately 1/N of the data.
 
### Assigning Operators to Clusters
The Cluster policy determines the logical distribution of the data. The assignments of nodes is by declaring Operators with the ID of the Cluster they manage.  
The Cluster ID is generated when the Cluster policy is added to the blockchain.  

## Activating the policies

When the policies are declared they bacome availabele to the relevant nodes using one of the methods that distributes the blockchain updates.  
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

## Test Cluster policies
The command below tests the validity of the Cluster policies:
<pre>
blockchain query metadata
</pre>

### Example Policies

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
    "ip" : "10.0.0.25",
    "port" : "2048"
    }
}

{"operator" : {
    "cluster" : "6c67e2982a69f606107d3c0f50aae8cc",
    "ip" : "10.0.0.87",
    "port" : "2048"
    }
}

{"operator" : {
    "cluster" : "56142ddfa243bb3bc8c6688848af01db",
    "ip" : "10.0.0.169",
    "port" : "2148"
    }
}
</pre>

