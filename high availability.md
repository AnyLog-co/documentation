# High Availability (HA)

## Overview

AnyLog can be configured such that data maintained in the Opertors Nodes is highly available.  
The HA process is such that multiple Operators maintain the same data such that is an Operator fails, the data is available on a surviving Operator and queries 
are directed to the surviving node.    
This document explains how to configure AnyLog to provide High Availability and the commands that monitor and report on the HA state.

## Declaring Clusters

HA is based on distributing the data to clusters. A cluster is a logical collection of data and each cluster is supported by
one or more operators. Operators are assigned to clusters (each operator can be assigned to only one cluster) and the number of
operators assigned to each cluster determine the number of copies of the data maintained in the cluster (all the operators assigned to a cluster maintain the same data).  

Below is an example of a policy declaring a cluster:

<pre>
{'cluster' : {'parent' : 'd11c9bf5ac720f1cf49dbda1126c4055',
               'name' : 'lsl-cluster1',
               'company' : 'Lit San Leandro',
               'table' : [{'dbms' : 'litsanleandro',
                           'name' : 'percentagecpu_sensor',
                           'status' : 'active'}],
               'source' : 'Node at 139.162.126.241:2048',
               'id' : 'c18cda63f631f304155efaaf8dc22f74',
               'date' : '2021-04-02T21:01:26.493845Z',
               'status' : 'active'}}]

</pre>

The cluster includes the list of tables that use the cluster for storage. If the same table is listed in multiple clusters,
the data of the table is split between the clusters.  
Note: A cluster is a logical definition, the actual storage is on the operators that are associated with the cluster (and all the operators assined to a cluster maintain the same data).  




