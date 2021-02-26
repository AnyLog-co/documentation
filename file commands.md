# File Commands

The ***file*** command provides the means to operate on files including deleting files, compressing and decompressing files and copying files between member nodes.

## Files operations:

To operate with a file, both the file path and the file name needs to be provided. 
Users can specify a complete file path and name or use the pre-declared parameters.
For example: ```!prep_dir``` can be used to represent the path to the ***prep*** directory. In this case the path is translated using the dictionary of the node processing the command.  
Some commands (like ***get*** and ***copy***) are executed on 2 nodes. in these cases it is possible to use 2 exclamation points to indicate translation of the variable on the second machine (see the examples below).

### Copy files between nodes in the network

Files can be copied to and from nodes in the network.  
The command ***file copy*** copies a file from the current node to a member node.
The command ***file get*** copies a file  from a member node to the current node.

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

