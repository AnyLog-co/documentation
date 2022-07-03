# Mapping Data

This document considers the mapping process as a transformation process applied to the source data (provided in JSON format)
to generate a destination JSON structure such that the generated data can fit to relational tables.  
The goal of the process is to make the data consistent with a destination table.  
The mapping process can modify the attributes names and values to be consistent with the tables structures and with the 
needed data types and formats that are required in the destination tables.

The mappings are defined in policies of types ***mapping*** that are saved in the shared metadata layer.  
When source JSON structures are processed, the data is transformed using a set of ***mapping*** policies that defines the mapping logic.

## The mapping policy
The mapping is declared as a JSON structure with ***mapping*** as a root key and information on the transformation of the data.

Pulling the needed values from the source data is done using the ****bring command***. Details of the ****bring command***
are available in the [The 'From JSON Object Bring' command](json%20data%20transformation.md#the-from-json-object-bring-command) section.

The source data is assumed to be in a JSON format. The sensor readings are represented in one of 2 ways:
1. As key value pairs in the source JSON.
2. As a list of dictionaries. Each dictionary in the list contains the readings as key value pairs. 

The policy sections are in the form of key-value pairs. The key determines the type of information, and the value provides the details.  
The chart below describes the sections of the policy.

| Key           | Data Type | Mandatory | Details |
| ------------- | --------- | --------- | ----------------------|
| id            | String  |   Yes     | The policy ID, users can provide a unique ID or when the policy is updated, an ID representing the Hash value is added |
| condition     | String  |   No      | An ***if statement*** that determines if the mapping policy needs to be processed  |
| dbms          | String  |   Yes     | The database name   |
| table         | String  |   Yes     | The table name   |
| readings      | String  |   No     | A key to a list of readings in the source JSON   |
| schema        | Dictionary  |   Yes     | The schema of the table with the mapping instructions   |

Note: The ***if statement*** is detailed in the section [Conditional Execution](anylog%20commands.md#conditional-execution).   

### The schema section
The schema is a dictionary whereas the target columns are the keys and each value is a dictionary representing the column's properties including the mapping instructions.  
The ***schema*** sections are detailed in the chart below:

| Key           | Data Type | Mandatory | Details |
| ------------- | --------- | --------- | ----------------------|
| condition     | String    |   No      | An ***if statement*** that determines if the column needs to be processed  |
| bring         | String    |   No      | the ***bring*** command to extract the data from the source JSON (or from each entry in the readings list) |
| type          | String    |   yes     | the column data type |
| default       | String    |   No     | A default value if the bring command does not return a value from the source data or the ***bring*** key is not specified. |

Note: An error is returned if both - the ***bring*** and ***default*** keys are not provided.

## Data type supported

* string
* integer
* float
* char
* timestamp
* bool
* varchar

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
[file=!prep_dir/london.readings.json.0.0.london_mapping, key=results, show= true] = rest get where url = https://datahub.io/core/london-air-quality/r/1.json
</pre> 
Details on retrieving data from a data source using REST GET are available in the section [Using REST command to retrive data from a data source](anylog%20commands.md#using-rest-command-to-retrive-data-from-a-data-source).
 
The example above downloads a JSON file from PurpleAir that includes a list of recent readings. More details on the REST GET command are available in the [AnyLog Commands section](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#rest-command).
 
 The information in the brackets provides the download destination:  
 ***file*** provides the path and file name. ***!prep_dir*** is a path assigned to the variable ***prep_dir***. To view the assigned value, type ```!prep_dir``` on the command line.  
 ***key*** provides the key (in the PurpleAir JSON file) of the list of readings.  
 ***show*** provides a visual status bar that monitors the write to file process.

## Creating the mapping instructions

```
<instruct = {"mapping" : {
               "id" : "london_mapping",
               "dbms" : "lsl_demo",
               "table" : "london",
               "schema" : {
                            "gmt" : {
                                "type" : "CHAR(5)",
                                "default" : "''",      
                                "source_name" : "GMT"
                            },
                           "nitric" : {
                                "type" : "decimal",
                                "default" : 0,
                                "source_name" : "London Mean Background Nitric Oxide (ug/m3)" 
                            },
                           "nitrogen" : {
                                "type" : "decimal",
                                "default" : 0,
                                "source_name" : "London Mean Background Nitrogen Dioxide (ug/m3)"    
                            }
                        }

            }
}> 
``` 
Notes: 
* In the example above, the ID of the policy is set to ***london_mapping***. If not provided, when the policy is updated, a unique ID is generated.
* For simplicity, the example is mapping 3 attributes from each reading (gmt, nitric, Nitrogen), users can update the mapping policy to include all attributes.


Add the policy to the blockchain:
<pre>
blockchain insert where policy = !instruct and local = true and master = !master_node
</pre> 

## Adding the data
Adding data to an Operator can be done by placing data in a ***watch*** directory or sending data using REST or assigning
a broker role to the node and publishing the data. These methods are explained in the section [adding data](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md).

#### Example:

The examples below copy the data to the ***watch*** directory. To see the value assigned to ***watch directory*** type ```!watch_dir``` on the AnyLog CLI.  

When data is copied to the watch directory, the file name serves as the metadata. If the file name is: london.readings.json.0.0.    
***dbms_name = file_name[0]*** will treat the first section of the file name (london) as the logical database name.  
***table_name = file_name[1]*** will treat the second section of the file name (readings) as the logical table name.  
***data_source = file_name[2]*** will treat the third section of the file name (readings) as the representative of the data source.
***hash_value = file_name[3]*** will treat the fourth section of the file name (readings) as the hash value of the file.
***instructions = file_name[4]*** will treat the fifth section of the file name (readings) as the mapping instructions policy id.london_mapping

 
 Copy the data to the ***watch*** directory.  
 The logical database ***london*** will be updated to include the table ***readings*** and the mapping instructions will process the data.
 
To view the status of the Operator:
<pre>
 get operator
</pre> 
 To view the list of tables on a local database:
<pre>
 get tables where dbms = london
</pre> 
To view the list of columns in a table:
<pre>
get columns where dbms = london and table = readings
</pre> 
Examples data queries
<pre>
run client () sql london format = table "select count(*) from readings"
run client () sql london format = table "select gmt, Nitrogen, nitric from readings limit 100"
</pre>

 
# Data mapping with multiple policies

This example maps data generated by Edgex data generator (from [EdgeX Foundry](https://www.edgexfoundry.org/)).
Edgex is an open source platform that facilitates interoperability between devices and applications.

## Sending data to an AnyLog node from EdgeX 
Data transfer from Edgex to AnyLog can be done using REST calls or by publishing the data on an AnyLog node.
Details are available at the [Using EdgeX](/using%20edgex.md#using-edgex) section of the documentation.  
The example below details a mapping process on a sample data detailed [below](#sample-data).

## The Mapping Policies

In this example, data published is split into 2 tables.  
1. rnd_val - A table that collects timestamps and integer values
2. device - A table that collects Temperature, Operational Mode, and Fan Speed as well as the timestamp of the reading.  

```
<mapping1 = {"mapping" : {

               "condition" : "if [device] == 'Random-Integer-Generator01'",

               "id" : "rnd_val",
               
               "dbms" : "edgex",
               "table" : "rnd_val",
                "readings" : "readings",
               
               "schema" : {
                            "timestamp" : {
                                "bring" : "[created]",
                                "type" : "timestamp",   
                                "default" : "''"     
                            },
                           "value" : {
                                "bring" : "[value]",
                                "type" : "decimal"
                            }
                           
                        }
            }
}> 
```

Add the policy to the blockchain:
<pre>
blockchain insert where policy = !mapping1 and local = true and master = !master_node
</pre> 


```
<mapping2 = {"mapping" : {

               "condition" : "if [device] == 'Modbus TCP test device'",

               "id" : "device",
               
               "dbms" : "edgex",
               "table" : "device",
               "readings" : "readings",

               "schema" : {
                            "timestamp" : {
                                "bring" : "[created]",
                                "type" : "timestamp"   
                            },
                            
                           "Temperature" : {
                                "condition" : "if [name] == Temperature",
                                "bring" : "[value]",
                                "type" : "decimal"
                            },
                           "mode" : {
                                "condition" : "if [name] == OperationMode",
                                "bring" : "[value]",
                                "type" : "string"
                            },
                          "speed" : {
                                "condition" : "if [name] == FanSpeed",
                                "bring" : "[value]",
                                "type" : "string"
                            }
                        }
            }
}> 
``` 
Add the policy to the blockchain:
<pre>
blockchain insert where policy = !mapping2 and local = true and master = !master_node
</pre> 

## Associate the policies to a topic
<pre>
run mqtt client where broker=local and log=false and topic=( name=anylog_test and policy = rnd_val and policy = device )
</pre> 

## Validate the assigned policies
<pre>
get msg client
</pre> 

## Publish the sample data

Cut and paste the sample data example [below](#sample-data) to the AnyLog CLI.

The following command on the CLI shows the assigned data to the key ***sample_data***.
<pre>
!sample_data
</pre>

Publish the data using the below command

<pre>
mqtt publish where broker=local and topic=anylog_test and message=!sample_data 
</pre>

<pre>
mqtt publish where broker=10.0.0.78 and port = 7850 and topic=anylog_test and message=!sample_data 
</pre>

View the messages processed by the broker using the following command:
<pre>
get broker 
</pre>


## Sample data
```
<sample_data = [{
  "id": "fb68440c-0dea-49be-b2b2-8e9003ab78c2",
  "pushed": 1656093207769,
  "device": "Random-Integer-Generator01",
  "created": 1656093207759,
  "modified": 1656093207771,
  "origin": 1656093207757297700,
  "readings": [
    {
      "id": "95fa6063-9c6d-4a31-8237-9732c51ec3f7",
      "created": 1656093207759,
      "origin": 1656093207757240800,
      "device": "Random-Integer-Generator01",
      "name": "RandomValue_Int16",
      "value": "-12830",
      "valueType": "Int16"
    }
  ]
},
{
  "id": "fc9e9640-66c3-424a-b572-9bd81126fcf8",
  "pushed": 1656092947759,
  "device": "Random-Integer-Generator01",
  "created": 1656092947754,
  "modified": 1656092947761,
  "origin": 1656092947752393700,
  "readings": [
    {
      "id": "a6fec012-7cc0-4a3b-adf1-6e64952ae46f",
      "created": 1656092947754,
      "origin": 1656092947752350200,
      "device": "Random-Integer-Generator01",
      "name": "RandomValue_Int8",
      "value": "8",
      "valueType": "Int8"
    }
  ]
},
{
  "id": "fcd6662c-893b-42c8-89eb-1d3963359256",
  "pushed": 1656092787767,
  "device": "Random-Integer-Generator01",
  "created": 1656092787757,
  "modified": 1656092787768,
  "origin": 1656092787752256300,
  "readings": [
    {
      "id": "28307823-8b07-42dd-8089-599e6cf339d4",
      "created": 1656092787757,
      "origin": 1656092787752201200,
      "device": "Random-Integer-Generator01",
      "name": "RandomValue_Int32",
      "value": "-1653714562",
      "valueType": "Int32"
    }
  ]
},
{
  "id": "ff2b6be0-890c-4e21-9bac-70bce9d27612",
  "pushed": 1656092885326,
  "device": "Modbus TCP test device",
  "created": 1656092885317,
  "modified": 1656092885327,
  "origin": 1656092885314563800,
  "readings": [
    {
      "id": "57a765d7-80ed-4dbc-b89a-866e35dda251",
      "created": 1656092885317,
      "origin": 1656092885313868000,
      "device": "Modbus TCP test device",
      "name": "Temperature",
      "value": "0.000000e+00",
      "valueType": "Float64",
      "floatEncoding": "eNotation"
    },
    {
      "id": "bde7a5c5-2d61-4f6f-98d8-93a7e2ce1316",
      "created": 1656092885317,
      "origin": 1656092885311935200,
      "device": "Modbus TCP test device",
      "name": "OperationMode",
      "value": "Cool",
      "valueType": "String"
    },
    {
      "id": "f2acb1fb-f785-4cf4-8c80-8b97ab7f6056",
      "created": 1656092885317,
      "origin": 1656092885312948700,
      "device": "Modbus TCP test device",
      "name": "FanSpeed",
      "value": "Low",
      "valueType": "String"
    }
  ]
}]>
```