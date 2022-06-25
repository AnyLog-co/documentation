# Mapping Data

Mapping is transformation instructions that are applied to JSON data structures in the process of mapping the JSON data to tables.
The default process treats every attribute name in the JSON file as a column name in the table.
The mapping process can modify the attributes names and values to be consistent with the tables structures and with the needed formats of the data.

The mapping are defined in policies of types ***instructions*** that are saved in the shared metadata layer.  
When JSON structures are processed, the data is transformed using a set of ***instructions*** that defines the mapping logic.

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

# London Air Example

Datahub (https://datahub.io/docs/about) allows organizations to publish, deploy and share their data.
It offers a REST API to download air quality measurements from different areas in the world.   
In this doc, we download the London air quality data from datahub and provide 2 examples:  
In the first example, the schema is determined by the data - attributes names are mapped to column names and the data types are determined by evaluating the data.    
In the second example, the schema is determined by a user, and the data is mapped to the schema as defined by the user.    


## Prerequisite

1) An AnyLog Operator node.  
   Details on Operator configurations are available in the section [background processes](background%20processes.md#operator-process).
2) Define a physical database (i.e.: PostgreSQL or SQLite) to the logical database name (london). 
   Details on database configurations are available in the section [Connecting to a local database](sql%20setup.md#connecting-to-a-local-database).

   
## Downloading the data

Using a REST GET command from the AnyLog Command line: 
 
<pre> 
[file=!prep_dir/london.readings.json, key=results, show= true] = rest get where url = https://datahub.io/core/london-air-quality/r/1.json
</pre> 
Details on retrieving data from a data source using REST GET are available in the section [Using REST command to retrive data from a data source](anylog%20commands.md#using-rest-command-to-retrive-data-from-a-data-source).
 
The example above downloads a JSON file from PurpleAir that includes a list of recent readings. More details on the REST GET command are available in the [AnyLog Commands section](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#rest-command).
 
 The informtion in the brackets provides the download destination:  
 ***file*** provides the path and file name. ***!prep_dir*** is a path assigned to the variable ***prep_dir***. To view the assigned value, type ```!prep_dir``` on the command line.  
 ***key*** provides the key (in the PurpleAir JSON file) of the list of readings.  
 ***show*** provides a visual status bar that monitors the write to file process.

## Adding the data
Adding data to an Operator can be done by placing data in a ***watch*** directory or sending data using REST or assigning
a broker role to the node and publishing the data. These methods are explained in the section [adding data](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md).

The examples below copy the data to the ***watch*** directory. To see the value assigned to ***watch directory*** type ```!watch_dir``` on the AnyLog CLI.  

When data is copied to the watch directory, the file name serves as the metadata. If the file name is: london.readings.json    
***dbms_name = file_name[0]*** will treat the first section of the file name (london) as the logical database name.  
***table_name = file_name[1]*** will treat the second section of the file name (readings) as the logical table name.  

#### Example 1:
 
 Copy the data to the ***watch*** directory. 
 The logical database ***london*** will be updated to include the table ***readings***.
 
To view the status of the Operator:
<pre>
 get operator
</pre> 
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
                "type" : "int",
                "source_name" : "ID",
                "default" : 0
            },
            "loc" : {
                 "type" : "str",
                 "source_name" : ["[lat]",",","[lon]"]
            },
            "timestamp" : {
                "type" : "timestamp",
                "source_name" : "lastseen"
            },
            "humidity" : {
                "type" : "int",
                "source_name" : "humidity"
            },
            "temperature" : {
                "type" : "int",
                "source_name" : "temp_f"
            },
            "pressure" : {
                "type" : "int",
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
    ***purpleair.readings.0.0.1eb8c6aae8898cb59905219b4056b619.json***  
    The Policy ID is placed in the 5th segment of the file name and therefore when the Operator process is initiated, the script includes: "instructions = file_name[4]"

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
 



 
 
 