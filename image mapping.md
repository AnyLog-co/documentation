# Image Mapping

An AnyLog Operator node can host images (or any type of _blob_ data like videos, photos, voice etc.) locally on the node and transfer the images to a destination node upon request.    
The process of managing images is similar to the process of managing streaming data with an additional process to store the image locally.  
Logically, the image is considered as a column in the database that hosts the data.  
Physically, the table column includes an identifier of the image, and the image is hosted separately using one (or both) 
of the following options:
1) in a dedicated database (using MongoDB as a default database).
2) in a dedicated folder.

A streaming process that includes an image is shown in the following diagram:
```
                                         -------------------            --------------------------
                                         |    AnyLog or    |            |                        |
  Data published to a Broker             |    External     |  ------>   |      AnyLog Client     |
  ---------------------------------->    |    Broker       |            |                        |
                                         -------------------            --------------------------
                                                                           |
                                                                           |
                                                                           V
                                                               -----------------        -----------------
                                                               |  Client Data  |        |  Extract      |
                                                               |  Mapper       |   -->  |  Image        |
                                                               |  f(Topic)     |        |               |
                                                               -----------------        -----------------
                                                                       |                       |
                                                                       |                       |
                                                                       V                       V
                                                               -----------------        -----------------
                                                               |               |        |  Image        |
                                                               |Relational DBMS|  <-->  |  Storage      |
                                                               |               |        |               |
                                                               -----------------        -----------------
         

```

## Transforming source data to a destination format

The data flow is as follows (and see the diagram above):
1) Data is published to a broker.
2) An AnyLog client process is subscribing to the broker (and a topic).
3) The subscription process (enable using `run mqtt client` command) associates a policy to the subscription.
4) The policy provides the instructions of the data transformation including how to extract the image data.
5) The transformation of the source data generates a data structure that updates the relational store and extracts the image data.
6) The image data is maintained as a file on the operating system or stored in a dedicated database like MongoDB (or both).

## The Blobs database
The separation of the blob data to a different physical database is addressing efficiency considerations as relational databases are not efficient in blob storage.  
However, each blob data is logically part of the data that is stored in the relational database.  
Therefore, rows in the relational database represent the blobs using a column that includes an identifier to the blob data.  
The identifier can be provided by a user (i.e. a unique file name), like an image name, or provided by the system, in that case the identifier is the 
hash value of the blob.  
As each blob data is associated with a row in a table of the relational database, we maintain a similar representation in the blob database:
1) The logical database name in the blobs' database is the same as the logical database name in the relational table with a prefix extension of: _blobs__.  
   For example: if the database name is "my_dbms", the blobs database name will be "blobs_my_dbms"
2) The logical table name is maintain with the blobs data such that each blob is associated with a table name which is the same as the relational table name.  
Each blob data is associated with a key representing the date the file was added to the database.  
The date key is in the format: _YYMMDD_ representing the date in the UTC time zone.  
   
This approach associates the following to each file:
1) A unique Hash Value (or a file name)
2) A database name
3) A table name
4) A time Key
   
## Blobs storage commands

The following commands allow to store, retrieve and monitor blob data:

### Declare the blobs dbms

Using a database for blob storage requires associating the logical database name with a physical storage.  
The command `connect dbms` is used to associate the logical database name with a physical database.  
The default choice for a logical name would be as the logical database name in the relational dbms that is referencing the blob data
- see details [above](#the-blobs-database).  

Usage:
```anylog 
connect dbms [logical name prefixed with blobs_] where type = [physical database name] and ip = [ip] and port = [port] and user = [use name] and password = [password]
``` 

Example:
```anylog 
connect dbms blobs_lsl where type = mongo and ip = localhost and port = 27017
``` 

Additional information is available at the [configuring a local database](sql%20setup.md#configuring-a-local-database) section.

### Dropping the blobs database

Dropping a database is a 2 step process.
1) Disconnect from the database.
2) Drop the database. The drop will delete all files stored in the logical database.  

Example:
```anylog
disconnect dbms blobs_lsl
drop dbms blobs_lsl from mongo where ip = localhost and port = 27017
```

### Get the list of files stores in the blobs database

Usage:
```anylog
get files where dbms = [dbms name] and table = [table name] and id = [file name] and hash = [hash value] and date = [YYMMDD in UTC] and limit = [limit]
```
Specifying the dbms is mandatory. All the other parameters are optional and serve as a filter.  
* Limit sets a cap on the number of files listed.
* Date is a 6-digits date in the format YYMMDD and limits the listed file by the update date. 

The following examples retrieve list of files assigned to a table (and their file size):
```anylog
get files where dbms = blobs_edgex and table = image and limit = 100
get files where dbms = blobs_edgex and table = image
```

Use the following example to View all the files assigned to a table in a particular date:
```anylog
get files where dbms = blobs_edgex and table = video and date = 220723 and limit = 100
get files where dbms = blobs_edgex and date = 220723  limit = 100
```

### get files count

The command returns the count of files stored in each table of the database.  
Usage:
```anylog
get files count where dbms = [dbms name] and table = [table name]
```
* DBMS name is optional - if not provided, all databases are considered.
* Table name is optional - if not provided, all tables of the specified database are considered.

Example:
```anylog
get files count where dbms = blobs_edgex and table = image
```

### Retrieve a file or files

Retrieving a blob file or files is by providing a search criteria and a destination folder to the retrieved files.  
Since file names are unique within a table, a specific file can be retrieved by specifying the database name, the 
table name, and a file unique ID (file name or hash value).  
If a file is retrieved using the file unique ID, the destination can be specified as a folder, in that case the file name 
remains, or as a path and a file name, in that case the file will be written to the folder with the new assigned name.
A group of files can be retrieved by a combination of the following search criteria:
1) A database and table name
2) Optionally a time Key (UTC time in YYMMDD format) - retrieving the files assigned to a table by a date.
If a group of files is retrieved, the destination can only be a folder.
   
Usage:
```anylog
file retrieve where dbms = [dbms name] and table = [table name] and id = [file id] and dest = [destination folder and optionally a file name]
file retrieve where dbms = [dbms name] and table = [table name] and hash = [file hash] and dest = [destination folder and optionally a file name]
file retrieve where dbms = [dbms name] and table = [table name] and date = [date key] and dest = [destination folder]
```

Examples:  
```anylog
file retrieve where dbms = blobs_edgex and table = image and id = 9439d99e6b0157b11bc6775f8b0e2490.png and dest = !blobs_dir/test_video.mp4
file retrieve where dbms = blobs_edgex and table = image and dest = !blobs_dir
```

### Delete a file or a group of files

Files are removed from storage using the `file remove` command.  
A single fle is removed by identifying the database name, the table name, the file unique ID (name) or the hash value.   
A group of files gets removed by identifying the database name a table name and a date key (YYMMDD in UTC format).  
Usage:
```anylog
  file remove where dbms = [dbms name] and table = [table name] and hash = [hash value]
  file remove where dbms = [dbms name] and table = [table name] and id = [file id]
  file remove where dbms = [dbms name] and table = [table_name]
  file remove where dbms = [dbms name] and and table = [table_name] and date = [date key]
```

Examples:
```anylog
  file remove where dbms = blobs_edgex and table = videos and id = 9439d99e6b0157b11bc6775f8b0e2490
  ile remove where dbms = blobs_edgex and table  = image
  file remove where dbms = blobs_edgex and table = image and date  = 220723
```


### Insert a file to a local database

Files can be added to the database and assigned to a table. 
When a file is added to the database, a file name and the hash value of the file serve as unique identifiers of the file (per table).

A file can be added and assigned to a table in a blobs database using the following command:
```anylog
file store where dbms = [dbms name] and table = [table name] and hash = [hash value] and source = [path and file name] and dest = [path and file name]
```
Explanation:

| Command Option | Details                                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------------------|
| dbms           | The database name - The database name                                                                                    |
| table          | The table name                                                                                                           |
| hash           | Any unique value provided by the user. If a value is not specified, the hash of the file will be calculated and included |
| source         | The source file (path and name) - note: with a REST call, the file can be transferred using -F option (see example blow) |
| dest           | The file name assigned in the blobs database - (required when the file is provided using REST with the -F option         |

The dbms and table name can be provided using one of the following options:
* Provided explicitly in the command line.
* As an extension to the file name. If the dbms and table names are not specified in the command line, 
 it is expected that these values would be embedded in the file name using the following format:  [dbms_name].[table name].[file name]

Examples:
1) In the example below, the database and table names are specified in the command.
```anylog
file store where dbms = admin and table = test and source = !prep_dir/testdata.txt
```
2) In the example below, the database name and table name are extracted from the file name: **admin** and **files** respectively.
```anylog
 file store where source = !prep_dir/admin.files.test.txt
 ```
3) Using a REST call, the source file is specified in the -F option. This option requiers to specify the name of the file in the blobs storage:
```anylog
curl -X POST -H "command: file store where dbms = admin and table = files and dest = file_rest " -F "file=@testdata.txt" http://10.0.0.78:7849
```

**Note:** 
For the hash variable, a user can calculate the hash value of a file using the command **file hash** 
```anylog
file hash !prep_dir/device12atpeak.bin
```

**Using Trace**  
To trace a failure, the following command outputs the failure error to stdout:
```anylog
trace level = 1 file store
```
Use the following command to disable the trace outputs:
```anylog
trace level = 0 file store
```

### Retrieve a blob file from a different node

A node in the network can copy a file from a storage database of a peer node (assuming proper permissions).  
The command [file get](file%20commands.md#file-copy-from-a-remote-node-to-a-local-node)
is used to copy files from a remote node to the local node.   
If the file on the remote node is stored in a database, the file to copy is specified by identifying the database name and the file unique ID.  

This process is frequently used to augment a SQL query, if the rows returned include the remote machines and the file IDs,
the query process can complete the query by a call to retrieve files from the remote machines.

Usage:
```anylog
run client [Remote node IP and Port] file get (dbms = [dbms name] and table = [table name] and id = [file ID]) [destination folder]
```

The file sample-5s.mp4 is stored on a different node (at 10.0.0.78:7848) and is copied to the current node
using the following command:
```anylog
run client 10.0.0.78:7848 file get (dbms = blobs_edgex and table = videos and id = sample-5s.mp4) !tmp_dir
```

# Example - processing data with images

The following example demonstrates data published on an AnyLog node that acts as a broker.  
The data includes an image and information relating to the image.  
A policy is assigned to the topic, and the incoming data updates the streaming data database (PostgresSQL) and 
a blobs storage database (MongoDB).  
The rows in the streaming database reference the blobs database such that, given a query to a remote node (that stores the data), the
query returns the location and identifier of the images that are associated with the returned data.  This information 
is sufficient to retrieve the needed images from the remote nodes.
be retrieved from the remote node.

Note: In the examples below, AnyLog Commands and Data Assignments are sometimes enclosed within angle brackets (“less than” or “greater than”) -
it allows to cut and paste the commands to the AnyLog CLI and process the commands as a code block.

## Prerequisite

1) An operational AnyLog Network
2) An Operator node configured with the following functionalities:
    * As a message broker - the new data is published on AnyLog node as a Broker.  
      Example:  
      ```anylog
      run message broker where external_ip = !external_ip and external_port = 7850 and internal_ip = !ip and internal_port = 7850 and threads = 6
      ```
      Details on configuration of AnyLog as a broker are available [here](message%20broker.md#configuring-an-anylog-node-as-a-message-broker).
    * As a Blobs Archiver - this process loads the images into blobs database (such as MongoDB).  
      Example:    
      ```anylog
      run blobs archiver where dbms = true and folder = true and compress = False
      ```
      Details on configuration of the Blobs Archiver process are available [here](background%20processes.md#the-blobs-archiver).
    
## Example data
The data reading below includes a JPEG image (assigned to the binaryValue attribute)

```
<sample_data = {
   "apiVersion" : "v2",
   "deviceName" : "Camera001",
   "id" : "8311655d-d11a-4a15-98e7-1b577785fe3e",
   "origin" : 1657247227381195746,
   "profileName" : "camera",
   "readings" : [
      {
         "binaryValue" : "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",
         "deviceName" : "Camera001",
         "id" : "bf31e9b6-295a-42d7-82b4-de479fa266e3",
         "mediaType" : "image/jpeg",
         "origin" : 1657247227381195746,
         "profileName" : "camera",
         "resourceName" : "OnvifSnapshot",
         "valueType" : "Binary"
      }
   ],
   "sourceName" : "OnvifSnapshot"
}>
```


## Example Policy

The policy below can be applied to the data above to retrieve the columns of interest.  
When the policy is applied (on the data) the following processes generate the info of interest:

1. The ID of the policy is named to be "id_image_mapping" - if an ID is not included in the policy, 
   an ID will be dynamically added when the policy is added to the ledger.
2. The DBMS and Table are provided in the policy as "edgex" and "image" respectively.
3. The Source attribute in the policy represents the source of the data, it will be provided by the _bring_ function applied to the "deviceName"
   attribute in the data (to retrieve the value - "Camera001"). 
   If the source data does not have a "deviceName" attribute, it will use the default value (_12_). 
   If a "deviceName" attribute is missing, it will use the value "0" to represent that data source is not represented.  
4. The "readings" attributes in the policy maps to the name of the readings attribute in the data. If a "readings" attribute is missing,
   it is assumed that the data does not contain the readings under a special attribute.
5. In the data example above, the data readings appear as a list under the "readings" attribute. Therefore, the 
   policy below identifies the "readings" attribute and identifies the needed info such that:  
    a. _Timestamp_ value is generated from the function now().  
    b. _Profilename_ is derived from the "profilename" attribute (within the readings attribute).  
    c. _ValueType_ is derivrd from the "valueType" attribute (within the readings attribute).  
    d. The _file_ attribute describes the file info as follows:  
    * It is a blob type of info.
    * It is derived from the "binaryValue" attribute.
    * It will be placed in a file with an extension "png".
    * It is uniquely identified by the Hash value (based on md5 hashing).
    * When stored, it will be decoded using base 64 decoding (see details [here](https://en.wikipedia.org/wiki/Base64).)
    
This process ends with a table _image_ assigned to a database _edgex_ that includes the following columns:    
a. _Timestamp_ - the current time   
b. _Profilename_ - taken from the readings  
c. _ValueType_ - taken from the readings  
d. _file_ - the hash value of the image including the file type (i.e.: 9439d99e6b0157b11bc6775f8b0e2490.png) is stored in a varchar column.

Based on the configuration of the Archiver Process, the image (from the attribute "binaryValue") is stored in an object database assigned to a table _image_
and a database _blobs_edgex_.  

```anylog
<mapping_policy = {"mapping" : {
    
        "id" : "id_image_mapping",
        
        "dbms" : "edgex",
        "table" : "image",
                     
        "source" : {
                        "bring" : "[deviceName]",
                        "default" : "12"       
                  },
        
        "readings" : "readings",
        
                "schema" : {
                        "timestamp" : {
                            
                            "type" : "timestamp",   
                            "default" : "now()"     
                        },
                        
                        "file" : {
                            "blob" : true,
                            "bring" : "[binaryValue]",
                            "extension" : "png",
                            "apply" : "base64decoding",
                            "hash" : "md5",
                            "type" : "varchar"
                        },
                        "profilename" : {
                            "bring" : "[profileName]",
                            "type" : "string"
                        },
                        "valueType" : {
                        "bring" : "[valueType]",
                        "type" : "string"
                        }
                 }
        }
}> 
```

## The Demo Process

Follow the following commands to configure the needed setup and process the data:

### Declare the participating databases
The [data example](#example-data) was generated from an [EdgeX](https://www.edgexfoundry.org/) based platform.  
The example names the logical database as follows:  
* _edgex_ - to represent the streaming data in a PostgresSQL database.
* _blobs_edgex_ - to represent the image (blob) data in a MongoDB database.

```anylog 
connect dbms edgex where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432
``` 
```anylog 
connect dbms blobs_edgex where type = mongo and ip = localhost and port = 27017
``` 

**Note: To maintain the association between the blobs and the relational data, the logical database name in the blobs
database is the same as the logical database name in the relational table with a prefix extension of: blobs.**

### Add the policy to the metadata
Cut and paste the policy definition above to the AnyLog CLI such that _mapping_policy_ is assigned with the policy info.  
The following command will display the policy info: `!mapping_policy`

 
Use the following command to update the metadata with the policy of the example above:  
```anylog
blockchain insert where policy = !mapping_policy and local = true  and master = !master_node
``` 
Use the following command to view the update of the metadata with the new policy:
```anylog
blockchain get mapping where id = id_image_mapping
``` 

### Subscribe to the published data 
The new data will be published to a topic called images and the command below associates data published to the 
_images_ topic with the policy above such that when the data is published, the data is mapped according to the mapping policy.

```anylog
run mqtt msg where broker=local and log=false and topic=( name=images and policy = id_image_mapping)
``` 

### Publish the data
To test the setup above, the configured node can publish the data to the broker.  
The data example contain some image characters that are modified when are pasted on the AnyLog CLI.  
To publish, cut and paste the [data example](#example-data) to a file (i.e.: image_setup.al in the prep directory) and assign the data using the command:
```anylog
process !prep_dir/image_setup.al 
``` 

The following command will display the sample data:
```anylog
!sample_data 
``` 

The command below publishes the data to the _images_ topic and trigger the processing:

```anylog
mqtt publish where broker=local and topic=images and message=!sample_data 
```


### Monitor the process:
The streaming data is passed through the following processes:  
* The client subscription receives the published data, and transforms the data according to the policy assigned to the topic.
* From the client process, the data is pushed to the streaming buffers.
* From the streaming buffers, the data is transferred to the Blobs Archiver that adds the image to the blob database.
* From the Blobs Archiver the data is pushed to the Operator process that inserts the streaming data to the local streaming database. 

These processes are monitored using the following commands:

Monitor the messages processed by the client (per topic):
```anylog
get msg client
```

Monitor the streaming buffers:
```anylog
get streaming
```

Monitor the Blobs Archiver:
```anylog
get blobs archiver
```

Monitor the Operator:
```anylog
get operator
```


### Get the list of files stores in the blobs database

View all the files assigned to a table:
```anylog
get files where dbms = blobs_edgex and table = image and limit = 100
```

View a list of up to 100 files assigned to a table in a particular date:
```anylog
get files where dbms = blobs_edgex and table = image  and date = 220807 and limit = 100
```

### get rows count
```anylog
get rows count where dbms = blobs_edgex and table = image
```

### Retrieve a file
```anylog
  file retrieve where dbms = edgex and table = images and dest = !prep_dir and limit = 10
  file retrieve where dbms = blobs_edgex and table = images and id = 07da45a366e5778fc7d34bf231bddcfa.png and dest = !prep_dir
```

### Delete a file or a group of files
```anylog
  file remove where dbms = blobs_edgex and table = videos and id = 9439d99e6b0157b11bc6775f8b0e2490.png
  file remove where dbms = blobs_edgex and table  = image
  file remove where dbms = blobs_edgex and table = image and date  = 220723
```
  
### Drop a database:
```anylog
disconnect dbms blobs_edgex
drop dbms blobs_edgex from mongo where ip = localhost and port = 27017
```

### Retrieve a blob file from a different node
The file sample-5s.mp4 is stored on a different node (at 10.0.0.78:7848) and is copied to the current node
using the following command:
```anylog
run client 10.0.0.78:7848 file get (dbms = blobs_edgex and table = images and id = sample-5s.mp4) !!tmp_dir
```

