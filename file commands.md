# File Commands

The ***file*** command provides the means to operate on files hosted on the local node and files hosted on peer nodes.    

Operations supported:

| Operation  | ---- | 
| ------------- | ---- |
| file copy | Copy a file from the local node to a remote node or, on the local node, copy the file to a different location. | 
| file get | Copy a file from a remote node to the current node. |
| directory copy | Copy all files from a specified directory to a remote node. |
| directory get | Copy all files from a directory in a remote node to the local node. |
| file move | Move a file to a different location on the local node. |
| file compress | Compress a file. |
| file decompress | Decompress a file. |
| file test | Test if a file exists. |
| file delete | Delete a file. |
| file hash | Calculate the hash value of the data contained in the file. |
| get files | List the files in a given directory on a remote node or the local node. |
| get directories | List the subdirectories in a given directory on a remote node or the local node. |

## Files names:

File names needs to be provided with the path to the file. Users can use keys defined in the dictionary as representatives of file names and paths.    
File names and paths can be prefixed by a key from a dictionary and are translated as follows:  
* A key designated with a single exclamation point ***!*** is replaced to a value using the dictionary of the local node. 
* A key designated with 2 exclamation points ***!!*** is replaced to a value using the dictionary of the remote node.  
Below are valid examples:  

| Path/Name | Comments | 
| ------------- | ---- |
| !blockchain_file | The path and file name for the local blockchain file. | 
| !prep_dir/sensor_data.json | The file ***sensor_data.json*** at the directory assigned to the key ***prep_dir*** in the local node|
| !!prep_dir/sensor_data.json | The file ***sensor_data.json*** at the directory assigned to the key ***prep_dir*** in the remote node|


## Copy a file on the local node
Using the command ***file copy*** users can copy files on the same node.    

Example:
<pre>
file copy !err_dir/data.json !!prep_dir/json.data
</pre>
In the example above the file ```data.json``` from the ```!err_dir``` was copied to the ```!prep_dir``` and named ```json.data```.

## Copy files between nodes in the network

Users can copy files from a remote node to the local node or from the local node to a remote node.  

The command ***file copy*** copies a file from the current node to a remote node.
The command ***file get*** copies a file  from a remote node to the current node.

To transfer the files, users specify the remote node using ***run client (IP:Port)*** instruction whereas the IP:Port is the address of the remote node.

## File copy from a local node to a remote node

Usage:
<pre>
run client (destination) [copy] [file path and name on the local node] [file path and name on the remote node]
</pre>
***destination*** is the IP and Port of the remote node.  
***file path and name*** can be the path and name on the local and remote nodes or keys that are translated using the local or remote dictionaries. 

Example:
<pre>
run client 132.148.12.32:2048 file copy !source_dir/data.json !!prep_dir/json.data
</pre>
In the example above:
***prep_dir*** will be mapped to a path using the dictionary of the remote node.

## File copy from a remote node to a local node

The command ***file get*** copies a file from a remote node to the local node.  
Usage:
<pre>
run client 132,148.12.32:2048 [get] [file path and name on the remote node] [path and file name on the local node]
</pre>

Example:
<pre>
run client 10.0.0.78:2048 file get !!blockchain_file !blockchain_file
</pre>
The example above copies the blockchain file from a member node to the current node.
***!!blockchain_file*** is translated on the remote node and ***!blockchain_file*** is translated on the local node.

### Copying multiple files from a remote node to a local node
Using the command ***file get*** and identifying source files on the remote note and a destination directory on the local node, 
users can copy multiple files ina single call.      
Usage:
<pre>
run client (destination) [get] [path and files on the remote node] [destination directory on the local node]
</pre>
***destination*** is the IP and Port of the remote node.  
***path and files on the remote node*** is a string representing a path to a directory and files identified by their name prefix and type prefix.
***destination directory on the local node*** is a string representing a valid directory location on the local node. The last character of the string needs to be a slash (indicating a directory).  

Examples:

<pre>
run client 10.0.0.78:2048 file get !!prep_dir/* !temp_dir/
</pre>
The above example copies all the files from the directory assigned to the key ***prep_dir*** on the remote machine to the directory assigned to the key ***temp_dir*** on the local machine.

<pre>
run client 10.0.0.78:2048 file get !!prep_dir/bl*.js* !temp_dir/
</pre>
The above example only copies files with **bl** as a file name prefix and ***js*** and a prefix to the file type.  

### Move a file
Move the source file to a destination directory
<pre>
[move] [source path and file name] [dest directory]
</pre>

Examples:
<pre>
file move !prep_dir/my_file !watch_dir
</pre>
The example above moves the file from the prep directory to the watch directory.

 
### Compress and decompress a file

<pre>
file compress [source path and file name] [target path and file name]
file decompress [path and file name of compressed file] [target path and file name]
</pre>
For compression, the target path and file name are optional. If omitted, the target file name and the location is the same and the source file with the extension ***.gz***.  
For decompression, the target path and file name are optional. If omitted, the target file name and the location is the same and the compressed file with the extension ***.dat***.
Examples:
<pre>
file compress source_file.dat new_file.gz
file decompress new_file,gz source_file.dat
</pre>


### Test if a file exists
<pre>
file test [path and file name]
</pre>
The call returns True if a file exists or False if the file does not exists.

Example:
<pre>
file test !prep_dir/my_file
</pre>


### Calculating the hash value of the data contained in a file
<pre>
file hash [path and file name]
</pre>

Example:
<pre>
file hash !prep_dir/my_file
</pre>

### delete a file
<pre>
file delete [path and file name]
</pre>

Example:
<pre>
file delete !prep_dir/my_file
</pre>

