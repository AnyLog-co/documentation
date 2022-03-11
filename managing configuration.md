# Managing configurations

Node configuration is a 2 steps process, where AnyLog commands serve as follows:
1) Updating the local dictionary - Updating the local dictionary of a node with the values that are needed by the node processes.
2) Initiating processes - Initiating the processes that determine how the node operates.

The configuration can be done in different ways:
a) Dynamically issuing REST calls (with AnyLog commands) from an application.
b) By a script file that contains AnyLog commands. The advantage in a script file is that it can be organized 
as a program with ***if*** conditions and ***goto statements***.
c) By a JSON file the contains AnyLog commands.
d) Using a table in a database that contains the AnyLog command.


## Dynamically issuing REST calls (with AnyLog commands) from an application

Issuing REST calls to an AnyLog node is explained in the [Using REST](.//using%20rest.md#using-rest) section.


## Issuing AnyLog commands as command lime arguments when AnyLog is initiated.

With multiple commands, enclose each command with quotation marks and separate each command with the keyword ```and```.
    
In the ex:
<pre>
AnyLog process !anylog_path/AnyLog-Network/demo/ha_operator1.al
</pre>

