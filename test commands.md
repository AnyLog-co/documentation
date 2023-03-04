# Test commands

The **test commands** determine the consistency of and availability of the data, metadata and processes in the network.


## Test Node
The ***test node*** command tests the node connections, and the structure of the local blockchain file.

Example:
```anylog
test node
```

## Test Connection
The ***test connection*** command tests the given IP and Port to determine if accessible and open.

Example:
```anylog
test connection 10.0.0.223:2041
```

## Test Table
The ***test table*** command compares the table schema in the blockchain ledger and the schema in the local table.  

Usage:  
```anylog
test table [table name] where dbms = [dbms name]
```
If table name is asterisk, all tables of the specified database are tested.
  
Examples:
```anylog
test table ping_sensor where dbms = lsl_demo
test table * where dbms = lsl_demo
```

## The Test Network Commands

The Test Network Commands determine the availability and consistency of multiple nodes in the network.  
Replies from the Test Network Commands are organized in a table structure with a row in the table representing each participating node.

### Test Network

The test is similar to issuing a **get status** command to all the nodes in the network.
   
Example:
```anylog
test network
```

### Test Network Metadata Version

The test is similar to issuing a [get metadata version](background%20processes.md#synchronizer-status) command to all the nodes in the network.
   
Example:
```anylog
test network metadata version
```

### Test Network Table

The test is similar to issuing a [test table](#test-table) command to all the nodes that host the table's data.

Examples:
```anylog
test network table ping_sensor where dbms = lsl_demo
test network table * where dbms = lsl_demo
```

## The test suite
The test suite commands compare query results to a predefined trusted results. Details are available in the 
[Test Suite](test%20suites.md#the-test-suite) section.  
**The Test Suite commands:**   
[test case](test%20suites.md#the-test-case-command)  
[test suite](est%20suites.md#the-test-suite-command)  

## High Availability Tests
Tests relating to High Availability are detailed in the [High Availability](high%20availability.md#high-availability-ha) section.  
**The HA test commands:**  
[test cluster setup](high%20availability.md#testing-the-node-configuration-for-ha)    
[test cluster data](high%20availability.md#cluster-synchronization-status)  
[test cluster databases](high%20availability.md#cluster-databases)  
[test cluster partitions](high%20availability.md#cluster-databases)  
[test cluster setup](high%20availability.md#testing-the-node-configuration-for-ha)  

