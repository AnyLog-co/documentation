# Configuration Examples

This document provides configuration examples.

## Starting a node with a configuration file

When an AnyLog node is initiated, it can be called with a command line parameters. The command line parameters 
are one or more AnyLog commands (with multiple commands, each command is enclosed by quotation mark and seperated by the keyword ***and***).  
Usage:
<pre>
python3 user_cmd.py "command 1" and "command 2" ... and "command n"
</pre>


The command ***process*** followed by a path and a file name will process all the commands in the specified file.  
The following example starts an AnyLog node and configures the node according to the commands listed in a file called ***autoexec.al***.

<pre>
python3 user_cmd.py "process !local_scripts\autoexec.al"
</pre>

## Updating the configuration file

Users can update the configuration file using an editor.

Alternatively, users can update the configuration file from the ***Remore CLI***.

### Configuring a node from the Remote CLI

#### Prerequisite: 
* An AnyLog node running.
* The node is configured with a REST connection.

#### Updating the config file
* In the Remote CLI, select the config section.  
* In tne config section update the REST IP and Port of the destination node (the REST IP and Port associated by the node).
* If authentication is enabled, add username and password in the appropriate fields.
* Select one of the following files from the pull-down menu:
  Autoexec
  Operator
  Publisher
  Query
  Master
  Standalone
* Select ***Load*** to retrieve the config file associated with the selected option.
* Note: Autoexec is the config file currently used. The other options are default options for a target role.
* Make changes as needed.
* To update the changes, select ***Save***.
* Note: ***Changes are saved to the Autoexec file*** regardless the file selected with the ***Load***.

Restart the AnyLog Node - if the node is initiated as in the [example above](#starting-a-node-with-a-configuration-file), the updated ***Autoexec*** file will determine the configuration.

  
## Configuring data removal and archival

### Configuring Backup, Archive and Removal of data

Multiple options are available to backup, archive and remove old data.

#### Setting a standby node

Declare a second operator node associated with an existing cluster. The second node will be dynamically updated with the
data assigned to the cluster.  
This process is detailed in the [High Availability (HA)](https://github.com/AnyLog-co/documentation/blob/master/high%20availability.md#high-availability-ha) section.

#### Archival of data

If an Opertaor node is configured with archive option enabled, data that is streaming to the local database is organized in 
files, compressed, and stored in the archival directory by ingestion date.  
The default archival directory is ```AnyLog-Network\data\archive```  
If needed, these files can be copied to an AnyLog ***watch*** directory to be ingested to a new database.
Details are availabel in [Placing data in the WATCH directory](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#placing-data-in-the-watch-directory) section.

#### Partitioning of data

A table that is managed by AnyLog can be partitioned by time.  
The ***Partition Command*** id detailed [here](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#partition-command).  
Partitions can be dropped by naming the partitions, or by requesting to drop the oldest partition, or by a request to
keep N number of partition, or to drop old partitions as long as disk space is lower than threshold.  
The ***Drop Partition*** command is detailed [here](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#drop-partition-command)

These processes can be placed on the AnyLog scheduler to be repeated periodically.  
For example, a table is partitioned by day and the scheduler is executed daily to remove the oldest partition if disk space 
is under a threshold.

Configuring the scheduler is detailed in the [Monitoring Nodes](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#monitoring-nodes) section.

### Backup Partition

Users can leverage the [archival directory](#archival-of-data) for the data backup.  
Alternatively, uses can actively archive a partition using the [backup table](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#backup-command) 
command (and specify the needed partition).



