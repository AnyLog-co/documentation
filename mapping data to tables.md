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

# PurpleAir Example

PurpleAir (https://www2.purpleair.com/) provides air quality monitoring solutions. It offers a REST API to download air quality measurements from differenn areas in the world.    
The 2 examples below download the data and update a local database of an Operator.
In the first example, the schema is determined by the PurpleAir data - attributes names are mapped to column names and the data types are determined by evaluating the data.    
In the second example, the schema is determined by a user and the PurpleAir data is mapped to the schema as defined by the user.    


## Prerequisite

1) An AnyLog node member in the network:  
    Use the following command to connect a node to the network using default IP and port 2048:  
    <pre> 
    run tcp server !ip 2048
    </pre>
    Update the operator as a member of the network supporting PurpleAir data.  
    Declare the operator (Note that the the instruction between the ***<...>*** signs below are treated on the AnyLog command line as a continues string): 
    <pre> 
    < operator = {"operator" : {
            "dbms" : "purpleair",
            "table" : "*",
            "ip" : !ip,
            "port" : "2048"
        }
    } >
    </pre>
    Update the blockchain:  
    <pre>
    blockchain add !operator
    </pre>
2) An AnyLog Node configured as an Operator. For example by issuing the following command on the AnyLog command line:
    
    <pre> 
    run operator where create_table = true and dbms_name = file_name[0] and table_name = file_name[1] and compress_sql = true and compress_json = true
    </pre>

The above command configures the node as an Operator. Adding data to an Operator can be done by placing data in a ***watch*** directory or sending data using REST.  
These methods are explained in the section [adding data](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md).
The examples below copy the data to the ***watch*** directory. To see the value assigned to ***watch directory*** type ```!watch_dir``` on the command line.  

When data is copied to the watch directory, the name of the file can determine the metadata. If the file name is: purpleair.readings.json    
***dbms_name = file_name[0]*** will treat the first section of the file name (purpleair) as the logical database name.  
***table_name = file_name[1]*** will treat the second section of the file name (readings) as the logical table name.  

The actual storage can be in Postgress or SQLite. To assign a physical database to the logical database use the following command:

<pre> 
connect dbms sqlite !db_user !db_port purpleair
</pre>

To use Postgress, replace ***sqlite*** with ***psql*** and to see active databases on this node use the command ```show databases```.

Details on Operator configurations are available in the section [background processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#operator-process).

## Downloading the data

Using a REST GET command from the AnyLog Command line: 
 
 <pre> 
[file=!prep_dir/purpleair.readings.json, key=results, show= true] = rest get where url = https://www.purpleair.com/json
 </pre> 
 
 The commands downloads a JSON file from PurpleAir that includes a list of recent readings.
 
 The informtion in the brackets provides the download destination:  
 ***file*** provides the path and file name. ***!prep_dir*** is a path assigned to the variable ***prep_dir***. To view the assigned value, type ```!prep_dir``` on the command line.  
 ***key*** provides the key (in the PurpleAir JSON file) of the list of readings.  
 ***show*** provides a visual status bar that monitors the write to file process.
 
 #### Example 1:
 
 Copy the data to the ***watch*** directory. 
 The logical database ***purpleair*** will be updated to include the table ***readings*** with the PurpleAir Data.
 
 To view the list of tables on a local database:
<pre>
 info dbms purpleair tables
</pre> 
To view the list of columns in a table:
<pre>
 info table purpleair readings columns
</pre> 
To view a sample of the data on the local database:
<pre>
 sql purpleair "select * from readings limit 10"
</pre>

 
 #### Example 2:
 
 To determine the schema add an Instructions Policy to the blockchain as follows:
 * Assign the policy to a variable. Note that the the instructions between the ***<...>*** signs are treated on the AnyLog command line as a continues string.
<pre> 
< instruct = {"instructions" : {
"dbms" : "purpleair",
"table" : "readings",

"schema"     : {

            "device_id" : {
                "data_type" : "int",
                "source_name" : "ID",
                "default_val" : 0
            },
            "loc" : {
                 "data_type" : "str"
                 "source_name" : ["[lat]",",","[lon]"]
            },
            "timestamp" : {
                "data_type" : "timestamp",
                "source_name" : "lastseen"
            },
            "humidity" : {
                "data_type" : "int",
                "source_name" : "humidity"
            },
            "temperature" : {
                "data_type" : "int",
                "source_name" : "temp_f"
            },
            "pressure" : {
                "data_type" : "int",
                "source_name" : "pressure"
            }
    }
}
} >
</pre>

 The policy declares a schema for the table ***readings*** in the ***purpleair*** database.  
 The keys inside the schema determine the column names, the source name determine the attribute name in the PurpleAir JSON file.  
 The key ***loc*** represents the coordinates of the sensor provided the readings and the value in the table is declared as a concatenation of the values with attribute names ***lat*** and ***lon*** separated by a comma.
    
 To add the Policy to the blockchain use the command:

<pre>
blockchain add !instruct
</pre>

Notes:

1) Drop the existing readings schema (if exists) using the command:
    <pre>
    drop table readings where dbms = purpleair
    </pre>

2) This command only updates the local copy of the blockchain. To update a master node, use the command:  
    <pre>
    run client (!master_node) blockchain push !instruct
    </pre>
    and wait for the local copy of the blockchain to be updated.

3) When the policy is added to the blockchain, the Policy is updated with a unique ID. To view the Policy as updated on the blockchain use the command:
    <pre>
    blockchain get instructions
    </pre>

    The ID provides a unique identifier to the policy. To assign the policy to the PurpleAir data change the filename to include the policy ID to be as follows:  
    ***purpleair.readings.0.id.json***  
    The 0 value is usually used for the ID of the data source which we do not use in this example.

4) Configure the operator to consider instructions identified on file names as follows:  
    a) Terminate current Operator configuration using the command line:
    <pre>
    exit opoerator
    </pre>
    b) Provide configuration to treat the instructions when data is loaded using the following command:
    <pre>
    run operator where create_table = true and dbms_name = file_name[0] and table_name = file_name[1] and instructions = file_name[4] and compress_sql = true and compress_json = true
    </pre>

Copy the file ***purpleair.readings.0.id.json*** to the ***watch*** directory. 
The logical database ***purpleair*** will be updated to include the table ***readings*** with the defined schema and PurpleAir Data.
 



 
 
 