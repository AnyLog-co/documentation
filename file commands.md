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
Below are valid examples:  

| Path/Name | Comments | 
| ------------- | ---- |
| !blockchain_file | The path and file name for the local blockchain file. | 
| !prep_dir/sensor_data.json | The file ***sensor_data.json*** at the directory assigned to the key ***prep_dir*** |

When a command is executed on 2 nodes, users can use use 2 exclamation points to indicate translation of the key on the remote node (see the examples below).


### Copy files between nodes in the network

Files can be copied to and from nodes in the network.  
The command ***file copy*** copies a file from the current node to a remote node.
The command ***file get*** copies a file  from a remote node to the current node.

#### file copy

Copy a file from the current node to a destination node.
<pre>
[copy] [file path and name on curret node] [destination path and name on target machine]
</pre>

Example:
<pre>
run client (destination) file copy !source_dir/data.json !!prep_dir/json.data
</pre>
In the example above:
***destination*** is the IP and Port of the destination node.  
***prep_dir*** will be mapped to a path using the dictionary of the target machine.

#### file get

Get a file from a member node.
<pre>
[get] [file path and name on the member node] [destination path and file name on current node]
</pre>

Example:
<pre>
run client (destination) file get !!blockchain_file !blockchain_file
</pre>
The example above copies the blockchain file from a member node to the current node.
***!blockchain_file*** is translated on the current node and ***!!blockchain_file*** is translated on the member node.

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

