# Registering PI in the AnyLog Network

PI objects are organized in a tree structure.  
Attributes in the hierarchy can be mapped to Relational table and users can issue SQL queries against these table as if the data is organized in a relational database.  

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
