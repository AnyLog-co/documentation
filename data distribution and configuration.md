
# Data Distribution and Configuration

The distribution of data to nodes in the network is determined by policies published on the blockchain.  
A policy is a JSON object that is structured as a nested disctionaries. The root dictionary has one attribute that determines the type of the policy and the children are structured as needed to describe the policy.  

There are 2 ways to represent how data is distributed.
1. Assigning data to Operators - using this approach, Operators declare the tables they support and the data is distributed to the relevant operators.  
This method does not offer the High Availability (HA) features and is usually used for testing.  
2. Declaring Clusters and assigning Operators to Clusters - this is the recomended approach for production as it offers redundancy and HA.  

## Prerequisites

* A set of policies published on the blockchain that determine how data is distributed.
* The participating Operators are connected to the network.
To view connection information call:  
```show connections``` on each participating operator.  
* Operators that host data are configured to provide a local database service.  
For example, to support a database called ***lsl_data*** using PotgreSQL, the ***connect dbms*** is called as follows:  
``` connect dbms psql !db_user !db_port lsl_data```
To view connected databases call:
```show databases```
 
## Assigning data to Operators

Operators declare the tables supported using a policies as the example below:

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

A CLuster is a policy that determines the following:
1. A set of tables that are supported by the Cluster Members.
2. For each table, the portion of the data that will be provided to the Cluster Members for hosting.

### Declaring the Cluster's tables
The cluster policy includes a list of tables that are supported. The tables are identified by:  
***company*** - the name of the company that owns the data (optional).  
***dbms*** - the name of the logical database that hosts the data.  
***name*** - the name of the logical table that hosts the data.  