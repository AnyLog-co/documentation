# Registering PI in the AnyLog Network

This document explains how data is mapped to a relational schema.    

PI instances can become members of the AnyLog Network. When a PI instance becomes a member, SQL queries that are issued to the network consider the data on the PI instance.  
If the data on the PI instance is part of the data set that is needed to be considered to satisfy the SQL query,  
the data is retrieved and evaluated as if it is being stored in a relational database.  
To make PI a member of the AnyLog network, the PI data is mapped to one or more relational tables.  
When a query in SQL is issued against a relational table, the relevant mapped PI data become part of the returned data set.  

The mapping of PI data to a relational schema is done using JSON object and it assumes the following:  
a) PI data is Hierarchical - PI objects are organized in a tree structure.  
b) Attributes in the hierarchy can be mapped to Relational table and users can issue SQL queries against these table as if the data is organized in a relational database.  

## The treatment of the data in PI
AnyLog treats the PI data as if it is organized in a hierarchical model with 4 layers: 
 1) Asset Frameworks (AF)
 2) Databases
 3) Elements
 4) Attributes
 
### Mapping of PI data to a Relational Table 

The mapping process involves 3 types of declarations:
 
#### 1) Declaring the AF and Database to use
 
To map PI data to a relational table structure, the relevant Asset Framework and Database needs to be declared and assigned to a logical database.  
For example:  ```connect dbms pi anylog@127.0.0.1:demo 5432 lsl_demo``` assign PI to the lsl_demo database/
The declaration of the PI Asset Framework and the PI Database means that the data in the named database can be considered for lsl_demo.  
The declaration is done by naming the asset framework name using ***af.name*** and asset framework ID using ***af.id***.

#### 2) Declaring the data conditions 
This is an optional declaration that assigns data data to a table only if the named values exist in PI.  
In the example below, data is considered in the ping_sensor table only if the element name is "ADVA ALM OTDR" and the sensor name is "ping".
  
#### 3) Declaring the participating attributes
This declaration mapps the attribute names in PI and the attribute names in the relational table.  
The mapping is done by mentioning the attribute name in PI followed by the attribute name in the Relational table.

Example:
```json
operator = {"operator" : {
    "id" : "0x184df883229af3b3b978493008345de3377723",
    "dbms" : "lsl_demo",
    "table": "ping_sensor",
    "ip" : "10.0.0.13",
    "port" : "2048",
    "type" : "pi",
    "mapping" : {"ip" : "10.0.0.13",
                 "port" : "7400",
                 "af.name" : "XOMPASS-LITSL",
                 "af.dbms" : "LitSanLeandro",
                 "dest" : "lsl_demo.ping_sensor",
                 "attributes" : "Timestamp to timestamp, Value to value, sensor.Name to device_name, sensor.WebId to webid",
                 "conditions": { 
                            "element.Name" : "ADVA ALM OTDR",
                            "sensor.Name" : "ping"
                            }
                }
    }
```

The first part of the JSON structure declares the AnyLog Operator instance that manage the PI instance.  
This section of the JSON is the same as a declaration of an Operator using a relational database.
The ***"mapping"*** section maps the PI data to the relational view.  
In this example, the data of database "LitSanLeandro" in the AF called "XOMPASS-LITSL" is mapped to the "ping_sensor" table in the logical database of "lsl_demo".
The sensor data from sensors called "ping" belonging to element "ADVA ALM OTDR" are mapped to the "ping_sensor" table such that:  
* Sensor Timestamp is mapped to column timestamp in the "ping_sensor" table.
* Sensor Value is mapped to column value in the "ping_sensor" table.
* Sensor Name is mapped to device_name in the "ping_sensor" table.
* Sensor WebId is mapped to webid in the "ping_sensor" table.

