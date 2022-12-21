# File Commands

The ***file*** command provides the means to operate on files hosted on the local node and files hosted on peer nodes.  
In the examples below, the ***local node*** is the node where the command is executed. 
The ***remote node*** is identified by the IP and Port declared in the [run tcp server](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#the-tcp-server-process) process.

Operations supported:

| Operation  | ---- | 
| ------------- | ---- |
| [file decompress](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#compress-and-decompress-a-file) | Decompress a file. |
| [file compress](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#compress-and-decompress-a-file) | Compress a file. |
| [file copy](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#copy-files-between-nodes-in-the-network) | Copy a file or files from the local node to a remote node or, on the local node, copy the file to a different location. | 
| [file delete](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#delete-a-file) | Delete a file. |
| file deliver | Copy archived data from a remote node. |
| [file get](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#file-copy-from-a-remote-node-to-a-local-node) | Copy a file or files from a remote node to the local node. |
| [file hash](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#calculating-the-hash-value-of-the-data-contained-in-a-file) | Calculate the hash value of the data contained in the file. |
| [file move](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#move-a-file) | Move a file to a different location on the local node. |
| [file test](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#test-if-a-file-exists) | Test if a file exists. |
| [file encode](#encode-and-decode-a-file) | Apply base64 encoding. |
| [file decode](#encode-and-decode-a-file) | Apply base64 decoding. |


List files or directories:
| Operation  | ---- | 
| ------------- | ---- |
| [get files](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#list-files-in-a-given-directory) | List the files in a given directory on a remote node or the local node. |
| [get directories](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#list-subdirectories-in-a-given-directory) | List the subdirectories in a given directory on a remote node or the local node. |

Operations on files stored in a dedicated database (details are available in the [Image Mapping](https://github.com/AnyLog-co/documentation/blob/master/image%20mapping.md#image-mapping) document):

| Operation  | ---- | 
| ------------- | ---- |
| [file remove](https://github.com/AnyLog-co/documentation/blob/master/image%20mapping.md#delete-a-file-or-a-group-of-files) | Delete a file from a blob database. |
| [file retrieve](https://github.com/AnyLog-co/documentation/blob/master/image%20mapping.md#retrieve-a-file-or-files) | Retrieve a file from a blob database. |
| [file Store](https://github.com/AnyLog-co/documentation/blob/master/image%20mapping.md#insert-a-file-to-a-local-database) | Insert a file from to the blob database. |

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
<pre>
file copy !err_dir/data.json !prep_dir/json.data
</pre>
In the example above the file ```data.json``` from the ```!err_dir``` was copied to the ```!prep_dir``` and named ```json.data```.

## Copy files between nodes in the network

Users can copy files from the local node to a remote node and from a remote node to the local node.  

* The command ***file copy*** copies a file (or files) from the local node to a remote node.  
* The command ***file get*** copies a file (or files) from a remote node to the local node.  

The remote node is identified by specifying an IP and Port using the command directive: ***run client (IP:Port)***.

## File copy from a local node to a remote node

Usage:
<pre>
run client (destination) file copy [file path and name on the local node] [file path and name on the remote node]
</pre>
***destination*** is the IP and Port of the remote node.  
***file path and name*** identify the file names on each node and can be keys that are translated using the local or remote dictionaries. 

Example:
<pre>
run client 132.148.12.32:2048 file copy !source_dir/data.json !!prep_dir/json.data
</pre>
In the example above:
***prep_dir*** will be mapped to a path using the dictionary of the remote node.


### Copying multiple files from a local node to a remote node

Using the command ***file copy*** and identifying source files on the local node and a destination directory on the remote node, 
users can copy multiple files using a single call.      
Usage:
<pre>
run client (destination) [file copy] [path and files on the local node] [directory on the remote node]
</pre>
***destination*** is the IP and Port of the remote node.  
***path and files on the local node*** is a string representing a path to a directory and files identified by their name prefix and type prefix.  
***directory on the remote node*** is a string representing a valid directory location on the remote node. The last character of the string needs to be a slash (indicating a directory).  

Examples:
<pre>
run client 10.0.0.78:2048 file copy !prep_dir/* !!temp_dir/
</pre>
The above example copies all the files from the directory assigned to the key ***prep_dir*** on the local node to the directory assigned to the key ***temp_dir*** on the remote node.

<pre>
run client 10.0.0.78:2048 file copy !prep_dir/bl*.js* !!temp_dir/
</pre>
The above example only copies files with **bl** as a file name prefix and ***js*** as a prefix to the file type.  


## File copy from a remote node to a local node

The command ***file get*** copies a file from a remote node to the local node.  
Usage:
<pre>
run client 132,148.12.32:2048 [file get] [file path and name on the remote node] [path and file name on the local node]
</pre>

Example:
<pre>
run client 10.0.0.78:2048 file get !!blockchain_file !blockchain_file
</pre>
The example above copies the blockchain file from a member node to the local node.
***!!blockchain_file*** is translated on the remote node and ***!blockchain_file*** is translated on the local node.

### Copying multiple files from a remote node to a local node

Using the command ***file get*** and identifying source files on the remote node and a destination directory on the local node, 
users can copy multiple files in a single call.      
Usage:
<pre>
run client (destination) [file get] [path and files on the remote node] [directory on the local node]
</pre>
***destination*** is the IP and Port of the remote node.  
***path and files on the remote node*** is a string representing a path to a directory and files identified by their name prefix and type prefix.
***directory on the local node*** is a string representing a valid directory location on the local node. The last character of the string needs to be a slash (indicating a directory).  

Examples:

<pre>
run client 10.0.0.78:2048 file get !!prep_dir/* !temp_dir/
</pre>
The above example copies all the files from the directory assigned to the key ***prep_dir*** on the remote node to the directory assigned to the key ***temp_dir*** on the local node.

<pre>
run client 10.0.0.78:2048 file get !!prep_dir/bl*.js* !temp_dir/
</pre>
The above example only copies files with **bl** as a file name prefix and ***js*** as a prefix to the file type.  

## Move a file
Move the source file to a destination directory on the local node.  
Usage:
<pre>
[move] [source path and file name] [dest directory]
</pre>

Example:
<pre>
file move !prep_dir/my_file !watch_dir
</pre>
The example above moves the file from the prep directory to the watch directory.

 
## Compress and decompress a file
These commands provide a simple interface to compress and decompress files.   
Usage:
<pre>
file compress [source path and file name] [target path and file name]
file decompress [path and file name of compressed file] [target path and file name]
</pre>
For compression, the target path and file name are optional. If omitted, the file location remains unchanged, and the file name is extended by ***.gz***.  
For decompression, the target path and file name are optional. If omitted, the file location remains unchanged, and the file name is extended by ***.dat***.
Examples:
<pre>
file compress source_file.dat new_file.gz
file decompress new_file.gz source_file.dat
</pre>

Compression can be applied to all files in a directory - if file name is asterisk (*), all files that match the type are compressed.  
The compressed file names are the same as the source file names with ***.gz*** extension.  

Example:
<pre>
src_dir = D:\Node\AnyLog-Network\data\prep\ping_sensor
file compress !src_dir\*.json
</pre>

Decompression can be applied to all files in a directory - if file name is asterisk (*), all files that match the type are decompressed.    
If the file type ends with ***gz*** the uncompressed file name removes the ***gz*** extension. Otherwize ***.dat*** type is added to the file name.  

Example:
<pre>
src_dir = D:\Node\AnyLog-Network\data\prep\ping_sensor
file decompress !src_dir\*.gz
</pre>

## Encode and decode a file
These commands allow to apply a base64 Encoding and Decoding.  
Usage:
<pre>
file encode [source path and file name] [target path and file name]
file decode [path and file name of compressed file] [target path and file name]
</pre>
Encoding and decoding can be applied to all files in a directory - if a file name is asterisk (*), all files that match the type are decoded or encoded.  
If a destination file name is not provided, encoding adds the file type ".msg" to the source file name. Decoding adds the extension ".png".   
Users need to modify the file type to represent the correct file format (like mp4).  
Examples:
<pre>
file encode source_file.mp4 new_file.msg
file decode new_file.msg source_file.mp4
src_dir = D:\Node\AnyLog-Network\data\prep\ping_sensor
file encode !src_dir\*.png
</pre>


## Test if a file exists
Usage:
<pre>
file test [path and file name]
</pre>
The call returns True if a file exists or False if the file does not exists.

Example:
<pre>
file test !prep_dir/my_file
</pre>


## Calculate the hash value of the data contained in a file
Usage:
<pre>
file hash [path and file name]
</pre>

Example:
<pre>
file hash !prep_dir/my_file
</pre>

## Delete a file
Usage:
<pre>
file delete [path and file name]
</pre>

Example:
<pre>
file delete !prep_dir/my_file
</pre>

## List files in a given directory
Usage:
<pre>
get files [directory path]
</pre>

Example, list files on the loca node:
<pre>
get files !err_dir
</pre>

Example, list files on a remote node:
<pre>
run client 10.0.0.78:2048 get files !!err_dir
</pre>

## List subdirectories in a given directory
Usage:
<pre>
get directories [directory path]
</pre>

Example, list subdirectories on the local node:
<pre>
get directories !archive_dir
</pre>

Example, list subdirectories on a remote node:
<pre>
run client 10.0.0.78:2048 get directories !!archive_dir
</pre>
