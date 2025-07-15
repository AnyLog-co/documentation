## AnyLog Install

AnyLog can be installed from Docker, Kubernetes or by downloading the codebase from GitHub and calling an installation script. 
Directions for deployment can be found [here](deployments). 

Starting AnyLog from the command line is demonstrated in the section: [Starting an AnyLog Instance](starting%20an%20anylog%20instance.md).

## Local directory structure

AnyLog directory setup is configurable. The default setup is detailed below: 

```anylog
Directory Structure   Explabnation
-------------------   -----------------------------------------
--> AnyLog-Network    [AnyLog Root]
    -->anylog         [Directory containing authentication keys and passwords]
    -->blockchain     [A JSON file representing the metadata relevant to the node]
    -->data           [Users data and intermediate data processed by this node]
       -->archive     [The root directory of and archival directory]
       -->bkup        [Optional location for backup of user data]
       -->blobs       [Directory containing unstructured data]
       -->dbms        [Optional location for persistent database data. If using SQLite, used for persistent SQLIte data]
       -->distr       [Directory used in the High Availability processes]
       -->error       [The storage location for new data that failed database storage]
       -->pem         [Directory containing keys and certificates]
       -->prep        [Directory for system intermediate data]
       -->test        [Directory location for output data of test queries] 
       -->watch       [Directory monitored by the system, data files placed in the directory are being processed] 
       -->bwatch      [Directory monitored by the system, managing unstructured data]
    -->source         [The root directory for source or executable files]
    -->scripts        [System scripts to install and configure the AnyLog node]
       -->install     [Installation scripts]
       -->anylog      [Configuration Scripts]
    -->local_scripts  [Users scripts]
```

Notes: 
* The following command creates the work folders if they do not exist:
    ```anylog
    create work directories
    ```
    The command needs to be issued only once on the physical or virtual machine.
    
* The following command list the directories on an AnyLog node:
     ```anylog
    get dictionary _dir
    ``` 
## Basic operations

### Initiating Configuring AnyLog instances

AnyLog is deployed and initiated using Docker or Kubernetes. The way the node operates depends on the configuration.  
AnyLog can be configured in many ways:
* Using command line arguments when AnyLog is called. These are a list of AnyLog commands separated by the _and_ keyword.
* By issuing configuration commands on the command line.
* By calling a script file that lists the AnyLog configuration commands (calling the command _process_ followed by the path to the script).
* By calling a configuration file that is hosted in a database.  
* Associating a Configuration Policy with the node. 

Related documentation:

| Section       | Information provided  |
| ------------- | ------------| 
| [Node configuration](node%20configuration.md#node-configuration) | Details on the configuration process. |
| [Deploying a node](deployments/deploying_node.md#deploying-a-node) | Basic deployment using Docker or Kubernetes. |
| [Network Setup](training/advanced/Network%20Setup.md) | A step by step example of a network deployment. |
| [Configuration Policies](policies.md#configuration-policies) | Policy based configuration. |



