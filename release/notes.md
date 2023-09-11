
Version: 1.3.2309
Release Date: TBD

## New Features:
1.  pip Install. Details: [pip Install](../training/advanced/Pip%20Install.md)
2.  Deploy AnyLog node as a background process. Details: [Deploy AnyLog as a background process](../training/advanced/background%20deployment.md).
3.  Map local CLI to a peer node. Details: [Assigning a CLI to a peer node](../training/advanced/background%20deployment.md#assigning-a-cli-to-a-peer-node).
4.  Start a new node with a seed from a peer node. Details: [Retrieving the metadata from a source node](../blockchain%20commands.md#retrieving-the-metadata-from-a-source-node)
5.  wait command - pauses execution by time and condition. Details: [The Wait Command](../anylog%20commands.md#the-wait-command)
6.  Create policy command - a command option to declare policies and include default attributes. Details:
    [Creating policies using the Create Policy command](../policies.md#creating-policies-using-the-create-policy-command)
7.  blockchain seed command

## Changes:

1.  The command: **run blockchain sync where source = master**, if connection info is not provided, connection info is
    retrieved from the policy of the Master Node. Details: [Blockchain Synchronizer](../background%20processes.md#blockchain-synchronizer).
    
2. If echo queue is set to True - all stdout messages which are not the result of the user input on the CLI are directed to the echo queue.

3. If license key is not provided - the **get status** command returns a warning on missing license key.    


## Bugs fixed:

1. The command **get inserts** ignored data inserted in immediate mode.