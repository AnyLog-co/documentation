# High Availability (HA)

## Overview

AnyLog can be configured such that data maintained in the Opertors Nodes is highly available.  
The HA process is such that multiple Operators maintain the same data such that is an Operator fails, the data is available on a surviving Operator and queries 
are directed to the surviving node.    
This document explains how to configure AnyLog to provide High Availability and the commands that monitor and report on the HA state.

## The Cluster Policy

HA is based on distributing the data to clusters. A cluster is a logical collection of data and each cluster is supported by
one or more operators. Operators are assigned to clusters (each operator can be assigned to only one cluster) and the number of
operators assigned to each cluster determine the number of copies of the data maintained in the cluster (all the operators assigned to a cluster maintain the same data).  

Below is an example of a policy declaring a cluster:

<pre>
 {'cluster' : {'company' : 'Lit San Leandro',
               'name' : 'lsl-cluster2',
               'master' : '45.33.41.185:2048',
               'table' : [{'name' : 'ping_sensor',
                           'dbms' : 'litsanleandro',
                           'status' : 'active'},
                          {'name' : 'perecentagecpu_sensor',
                           'dbms' : 'litsanleandro',
                           'status' : 'active'}],
               'id' : '11612ba3c05e123e2a3fef9fcd4d53fe',
               'date' : '2021-04-02T18:31:46.802694Z',
               'status' : 'active'}},
</pre>

The cluster includes the list of tables that use the cluster for storage. If the same table is listed in multiple clusters,
the data of the table is split between the clusters.  
Notes: 
1) A cluster is a logical definition, the actual storage is on the operators that are associated with the cluster (and all the operators assined to a cluster maintain the same data).
2) The ID and Date attributes of the policy are added by the network protocol.
3) A policy ID uniquely identifies a policy, therefore, the ID of the cluster policy uniquely identifies the cluster.

## The Operator Policy

An Operator is assigned to a cluster in the following manner:

<pre>
{'operator' : {'cluster' : '11612ba3c05e123e2a3fef9fcd4d53fe',
                'ip' : '24.23.250.144',
                'local_ip' : '10.0.0.78',
                'port' : 7848,
                'id' : '52612f21b18cf29f7d2e511e3ca56ca6',
                'date' : '2021-04-02T21:43:20.129597Z',
                'member' : 145}}]
</pre>

Note: 
1) The value for the key ***cluster*** is the Cluster ID that is assigned to the Operator.
2) All the data provided to the cluster will be hosted with the operator (as well as with the other operators that are associated with the cluster).

