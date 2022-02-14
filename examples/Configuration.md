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

  



