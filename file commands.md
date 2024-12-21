# File Commands

The ***file*** command provides the means to operate on files hosted on the local node and files hosted on peer nodes.  
In the examples below, the ***local node*** is the node where the command is executed. 
The ***remote node*** is identified by the IP and Port declared in the [run tcp server](background%20processes.md#the-tcp-server-process) process.

Operations supported:

| Operation                                                                | ----                                                                                                                    | 
|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [file decompress](#compress-and-decompress-a-file)                       | Decompress a file.                                                                                                      |
| [file compress](#compress-and-decompress-a-file)                         | Compress a file.                                                                                                        |
| [file copy](#copy-files-between-nodes-in-the-network)                    | Copy a file or files from the local node to a remote node or, on the local node, copy the file to a different location. | 
| [file to](#copy-a-file-to-a-folder) | Copy a file to a specified folder, with HTTP request, the file can be specified using the -F option.                    | 
| [file delete](#delete-a-file)                                            | Delete a file.                                                                                                          |
| file deliver                                                             | Copy archived data from a remote node.                                                                                  |
| [file get](#file-copy-from-a-remote-node-to-a-local-node)                | Copy a file or files from a remote node to the local node.                                                              |
| [file hash](#calculating-the-hash-value-of-the-data-contained-in-a-file) | Calculate the hash value of the data contained in the file.                                                             |
| [file move](#move-a-file)                                                | Move a file to a different location on the local node.                                                                  |
| [file test](#test-if-a-file-exists)                                      | Test if a file exists.                                                                                                  |
| [file encode](#encode-and-decode-a-file)                                 | Apply base64 encoding.                                                                                                  |
| [file decode](#encode-and-decode-a-file)                                 | Apply base64 decoding.                                                                                                  |


List files or directories:

| Operation  | ---- | 
| ------------- | ---- |
| [get files](#list-files-in-a-given-directory) | List the files in a given directory on a remote node or the local node. |
| [get directories](#list-subdirectories-in-a-given-directory) | List the subdirectories in a given directory on a remote node or the local node. |

Operations on files stored in a dedicated database (details are available in the [Image Mapping](../data%20management/image%20mapping.md#image-mapping) document):

| Operation  | ---- | 
| ------------- | ---- |
| [file remove](../data%20management/image%20mapping.md#delete-a-file-or-a-group-of-files) | Delete a file from a blob database. |
| [file retrieve](../data%20management/image%20mapping.md#retrieve-a-file-or-files) | Retrieve a file from a blob database. |
| [file Store](../data%20management/image%20mapping.md#insert-a-file-to-a-local-database) | Insert a file from to the blob database. |

## Files names

File names are provided with their paths. Users can use keys defined in the dictionary as representatives of file names and paths.    
File names and paths can be prefixed by a key from a dictionary and are translated as follows:  
* A key designated with a single exclamation point ***!*** is replaced by the value in the dictionary of the local node. 
* A key designated with 2 exclamation points ***!!*** is replaced by the value in the dictionary of the remote node.  

Below are valid examples:  

| Path/Name | Comments | 
| ------------- | ---- |
| !blockchain_file | The path and file name of the local blockchain file. | 
| !prep_dir/sensor_data.json | The file ***sensor_data.json*** and a path which is the value assigned to the key ***prep_dir*** in the local node|
| !!prep_dir/sensor_data.json | The file ***sensor_data.json*** and a path which is the value assigned to the key ***prep_dir*** in the remote node|


## Copy a file on the local node

Using the command ***file copy*** users can copy files on the same node.    

Example:
```anylog
file copy !err_dir/data.json !prep_dir/json.data
```
In the example above the file `data.json` from the `!err_dir` was copied to the `!prep_dir` and named `json.data```.

## Copy files between nodes in the network

Users can copy files from the local node to a remote node and from a remote node to the local node.  

* The command ***file copy*** copies a file (or files) from the local node to a remote node.  
* The command ***file get*** copies a file (or files) from a remote node to the local node.  

The remote node is identified by specifying an IP and Port using the command directive: ***run client (IP:Port)***.

## File copy from a local node to a remote node

Usage:
```anylog
run client (destination) file copy [file path and name on the local node] [file path and name on the remote node]
```
***destination*** is the IP and Port of the remote node.  
***file path and name*** identify the file names on each node and can be keys that are translated using the local or remote dictionaries. 

Example:
```anylog
run client 132.148.12.32:2048 file copy !source_dir/data.json !!prep_dir/json.data
```
In the example above:
***prep_dir*** will be mapped to a path using the dictionary of the remote node.


### Copying multiple files from a local node to a remote node

Using the command ***file copy*** and identifying source files on the local node and a destination directory on the remote node, 
users can copy multiple files using a single call.      
Usage:
```anylog
run client (destination) [file copy] [path and files on the local node] [directory on the remote node]
```
***destination*** is the IP and Port of the remote node.  
***path and files on the local node*** is a string representing a path to a directory and files identified by their name prefix and type prefix.  
***directory on the remote node*** is a string representing a valid directory location on the remote node. The last character of the string needs to be a slash (indicating a directory).  

Examples:
```anylog
run client 10.0.0.78:2048 file copy !prep_dir/* !!temp_dir/
```
The above example copies all the files from the directory assigned to the key ***prep_dir*** on the local node to the directory assigned to the key ***temp_dir*** on the remote node.

```anylog
run client 10.0.0.78:2048 file copy !prep_dir/bl*.js* !!temp_dir/
```
The above example only copies files with **bl** as a file name prefix and ***js*** as a prefix to the file type.  


## File copy from a remote node to a local node

The command ***file get*** copies a file from a remote node to the local node.  
Usage:
```anylog
run client 132,148.12.32:2048 [file get] [file path and name on the remote node] [path and file name on the local node]
```

Example:
```anylog
run client 10.0.0.78:2048 file get !!blockchain_file !blockchain_file
```
The example above copies the blockchain file from a member node to the local node.
***!!blockchain_file*** is translated on the remote node and ***!blockchain_file*** is translated on the local node.

### Copying multiple files from a remote node to a local node

Using the command ***file get*** and identifying source files on the remote node and a destination directory on the local node, 
users can copy multiple files in a single call.      
Usage:
```anylog
run client (destination) [file get] [path and files on the remote node] [directory on the local node]
```
***destination*** is the IP and Port of the remote node.  
***path and files on the remote node*** is a string representing a path to a directory and files identified by their name prefix and type prefix.
***directory on the local node*** is a string representing a valid directory location on the local node. The last character of the string needs to be a slash (indicating a directory).  

Examples:

```anylog
run client 10.0.0.78:2048 file get !!prep_dir/* !temp_dir/
```
The above example copies all the files from the directory assigned to the key ***prep_dir*** on the remote node to the directory assigned to the key ***temp_dir*** on the local node.

```anylog
run client 10.0.0.78:2048 file get !!prep_dir/bl*.js* !temp_dir/
```
The above example only copies files with **bl** as a file name prefix and ***js*** as a prefix to the file type.  


## Copy a file to a folder

Files can be copied to a specified folder using the **file to** command:
```anylog
file to where to [path and file name] where source = [path and file name]
```
This command is similar to the copy commands, however, when issuing the command using HTTP, the source file can be specified by the -F option.  
This command is frequently used to copy config files into nodes when users deploy nodes from remote nodes.  
Example:
```anylog
curl -X POST -H \"command: file to !my_dest\" -F \"file=@testdata.txt\" http://10.0.0.78:7849
```


## Move a file
Move the source file to a destination directory on the local node.  
Usage:
```anylog
[move] [source path and file name] [dest directory]
```

Example:
```anylog
file move !prep_dir/my_file !watch_dir
```
The example above moves the file from the prep directory to the watch directory.

 
## Compress and decompress a file
These commands provide a simple interface to compress and decompress files.   
Usage:
```anylog
file compress [source path and file name] [target path and file name]
file decompress [path and file name of compressed file] [target path and file name]
```
For compression, the target path and file name are optional. If omitted, the file location remains unchanged, and the file name is extended by ***.gz***.  
For decompression, the target path and file name are optional. If omitted, the file location remains unchanged, and the file name is extended by ***.dat***.
Examples:
```anylog
file compress source_file.dat new_file.gz
file decompress new_file.gz source_file.dat
```

Compression can be applied to all files in a directory - if file name is asterisk (*), all files that match the type are compressed.  
The compressed file names are the same as the source file names with ***.gz*** extension.  

Example:
```anylog
src_dir = D:\Node\AnyLog-Network\data\prep\ping_sensor
file compress !src_dir\*.json
```

Decompression can be applied to all files in a directory - if file name is asterisk (*), all files that match the type are decompressed.    
If the file type ends with ***gz*** the uncompressed file name removes the ***gz*** extension. Otherwise ***.dat*** type is added to the file name.  

Example:
```anylog
src_dir = D:\Node\AnyLog-Network\data\prep\ping_sensor
file decompress !src_dir\*.gz
```

## Encode and decode a file
These commands allow to apply a base64 Encoding and Decoding.  
Usage:
```anylog
file encode [source path and file name] [target path and file name]
file decode [path and file name of compressed file] [target path and file name]
```
Encoding and decoding can be applied to all files in a directory - if a file name is asterisk (*), all files that match the type are decoded or encoded.  
If a destination file name is not provided, encoding adds the file type ".msg" to the source file name. Decoding adds the extension ".png".   
Users need to modify the file type to represent the correct file format (like mp4).  
Examples:
```anylog
file encode source_file.mp4 new_file.msg
file decode new_file.msg source_file.mp4
src_dir = D:\Node\AnyLog-Network\data\prep\ping_sensor
file encode !src_dir\*.png
```


## Test if a file exists
Usage:
```anylog
file test [path and file name]
```
The call returns True if a file exists or False if the file does not exist.

Example:
```anylog
file test !prep_dir/my_file
```


## Calculate the hash value of the data contained in a file
Usage:
```anylog
file hash [path and file name]
```

Example:
```anylog
file hash !prep_dir/my_file
```

## Delete a file
Usage:
```anylog
file delete [path and file name]
```

Example:
```anylog
file delete !prep_dir/my_file
```

## List files in a given directory
Usage:
```anylog
get files [directory path]
```

Example, list files on the loca node:
```anylog
get files !err_dir
```

Example, list files on a remote node:
```anylog
run client 10.0.0.78:2048 get files !!err_dir
```

## List subdirectories in a given directory
Usage:
```anylog
get directories [directory path]
```

Example, list subdirectories on the local node:
```anylog
get directories !archive_dir
```

Example, list subdirectories on a remote node:
```anylog
run client 10.0.0.78:2048 get directories !!archive_dir
```
