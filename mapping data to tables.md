# Mapping Data

Mapping is transformation instructions that are applied to JSON files in the process of generating SQL files which are consistent with the tables structures.
The SQL files are files containing Insert statements that are loaded by a local database to add new data.  
The default process treats every attribute name in the JSON file as a column name in the table.
The mapping process can modify the attributes names and values to be consistent with the tables structures and with the needed formats of the data.

The mapping of JSON data to tables structure is declared by ***instructions*** that are saved in the blockchain and are identified by a unique ID.  
When JSON files are processed, the files can be assigned to a set of ***instructions*** that define the mapping logic.

### The mapping Instructions
The mapping is declared in a JSON structure. The name of the structure is ***instructions*** and it contains information on the transformation of the data.  
The ***default transformation*** compares all the attributes names in the JSON file to the table columns. If an attribute name and a column name are the same, the data from the JSON file is assigned to the table's column. 
If an attribute name is not represented as a column, the attribute value is ignored.

#### Sections in the mapping Instructions

* Generic Info - optional information to identify and classify the instructions.  
For example, database name and table name that are the target of the transformation. 
The name or type of the sensor that generates the data and any other type of information that is needed to serve as an identifier of the instructions.

* A Unique ID - provided by the user defining the instructions, or if an ID is not declared, the system will generate a unique ID based on the has value of the Instructions.

* Script - a section providing transformation instructions which are not specific to a particular attribute.  
Script Definitions:  
 ```type:inclusive``` - mapping instructions that are added to the ***default transformation***.  
 ```type:exclusive``` - mapping instructions that replace the ***default transformation***.
 
 * Attributes - a section providing mapping instructions for named attributes.  
 Mapping assigned to an attribute name can be one or more of the following:
 
    * ***name*** - a column name in the table which is different than the attribute name.
    * ***type*** - use the specified type to validate the data type of the attribute value.
    * ***default*** - a default value if the attribute value is missing or the value is not convertable to the declared type.
    * ***if then statements*** a list of python based rules that can be validated and operated on the attribute name or attribute value during the transformation process.
    
#### Example
```
<instruct = {"instructions" : {
   "dbms" : "lsl_demo",
   "table" : "ping_sensor",
   "script" : {
      "type" : "inclusive"
   },
   "attributes" : {
      "device_number" : {
         "name" : "device",
         "type" : "CHAR(30)",
         "default" : "''"
      },
      "device_name" : [
         "if value.upper()[:2] == 'VM' then value = 'Basic Network Element'",
         "if value.upper().startswith('F') then value = 'FSP3000'",
         "if value.upper() == 'ADVA FSP3000R7' then value = 'FSP3000'",
         "if value.upper() == 'ADVA ALM OTDR' then value = 'OTDR'",
         "if value.upper().find('APC') != -1 then value = 'OTDR'",
         "if value.startswith('Ubiquiti') then value = 'Ubiquity 10G Switch'",
         "if value.endsswith('Ubiquity') then value = 'Ubiquity 10G Switch'",
         "if value.startwith('ULoco') then value = 'ULoco Dev'",
         "if value.startswith('Catalyst') then value = 'ULoco Dev'",
         "if value.upper().startswith('CATALYST') then value = 'ULoco Dev'"
         ]
      }
   }
}> 
```  


 