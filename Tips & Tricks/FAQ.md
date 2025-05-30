# FAQ

This repository serves as a reference for understanding node types in the AnyLog ecosystem, common operational issues, and 
differences between the enterprise-grade AnyLog and EdgeLake deployments.

## 📖 Overview

**AnyLog** is a decentralized data platform for managing and querying operational and IoT data.  
**EdgeLake** is the open-source version of AnyLog

| Feature                              | EdgeLake (Community Version)         | AnyLog Enterprise (Subscription)    |
|--------------------------------------|--------------------------------------|-------------------------------------|
| **License**                          | Open-source (Linux Foundation)       | Commercial (Contact for pricing)    |
| **Virtual Edge Layer**               | ✅                                    | ✅                                  |
| **Rule Engine**                      | ✅                                    | ✅                                  |
| **Policy-Based Data Management**     | ✅                                    | ✅                                  |
| **Node Management**                  | ✅                                    | ✅                                  |
| **Unified APIs, CLIs, Admin UI**     | ✅                                    | ✅                                  |
| **Supported IoT Connectors**         | ✅                                    | ✅                                  |
| **Blockchain Abstraction**           | Optional Add-on                      | ✅                                  |
| **Aggregations**                     | ❌                                    | ✅                                  |
| **Security Protocol**                | ❌                                    | ✅                                  |
| **High Availability (HA)**           | ❌                                    | ✅                                  |
| **Test Suites**                      | ❌                                    | ✅                                  |
| **Training**                         | ❌                                    | ✅                                  |
| **Technical Support**                | ❌                                    | ✅                                  |

For details: [AnyLog Pricing](https://www.anylog.network/pricing)

## ❓ Frequently Asked Questions (FAQ)

### What are the different types of nodes in the AnyLog Network?

All AnyLog containers run the same source code / image, it is the configurations that force a distinction in behavior between the node types:

* **Master**: An AnyLog instance that simulates the role of a blockchain, serving as a decentralized "oracle" for managing metadata, smart contracts, and overall network coordination.
* **Operator**: An AnyLog instance responsible for storing data collected from devices.
  * **Cluster**: A logical policy that defines the relationship between Operator nodes, enabling high availability (HA) and informing members of the network about the location and distribution of data. Each Operator node belongs to a Cluster, and a Cluster can consist of multiple Operator nodes.
* **Query**: An AnyLog instance dedicated to processing and executing data queries. Any node can serve as a Query Node if it includes the `system_query` logical database.
* **Publisher**: An AnyLog instance responsible for distributing or publishing data to Operator nodes. Publishers typically act as gateways for ingesting real-time data into the network.
> ⚠️ **Note**: Publisher is not supported in **EdgeLake**.

### How do I configure an AnyLog node to act as a specific node type?

Configuration is done through either a dotenv file for Docker / Podman or YAML file for Kubernetes.
The configurations can be done in 2 parts
* **basic** which consists of the standard configurations, such as networking and database configurations
* **advance** which consists of more advanced configurations such as number of threads to use and enabling advanced services.   

Configurations can be found in our [docker-compose](https://github.com/AnyLog-co/docker-compose/) 

### How does the deployment process work? 

A node is deployed using the following logic

1. Using the dotenv / YAML configuration file(s), a user defines an AnyLog node (type) with their prefered configurations
2. The user then deploys the docker or Kubernetes container with the given configurations
3. The docker image will download a copy of our [deployment-scripts](https://github.com/AnyLog-co/deployment-scripts) 
4. It will then convert the user-defined environment variables to AnyLog variables
5. The code will then declare a configurations policy (if not exists) that specifies how to configure a node.    
```json
{"config" : {
    "name" : "operator-iotech-configs", 
    "company" : "IoTech System", 
    "node_type" : "operator",
    "ip" : "!external_ip",
    "local_ip" : "!overlay_ip",
    "port" : "!anylog_server_port.int",
    "rest_port" : "!anylog_rest_port.int",
    "broker_port" : "!anylog_broker_port.int",
    "threads" : "!tcp_threads.int",
    "tcp_bind" : "!tcp_bind",
    "rest_threads" : "!rest_threads.int",
    "rest_timeout" : "!rest_timeout.int",
    "rest_bind" : "!rest_bind",
    "broker_threads" : "!broker_threads.int",
    "broker_bind" : "!broker_bind",
    "script" : [
      "process !local_scripts/connect_blockchain.al", 
      "process !local_scripts/policies/cluster_policy.al",
      "process !local_scripts/policies/node_policy.al",
      "process !local_scripts/database/deploy_database.al",
      "run scheduler 1",
      "set buffer threshold where time=!threshold_time and volume=!threshold_volume and write_immediate=!write_immediate",
      "run streamer", 
      "if !enable_ha == true then run data distributor",
      "if !enable_ha == true then run data consumer where start_date=!start_data",
      "if !operator_id and !blockchain_source != master then run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and compress_json=!compress_file and compress_sql=!compress_sql and archive_json=!archive and archive_sql=!archive_sql and blockchain=!blockchain_source and policy=!operator_id and threads=!operator_threads",
      "if !operator_id and !blockchain_source == master then run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and compress_json=!compress_file and compress_sql=!compress_sql and archive_json=!archive and archive_sql=!archive_sql and master_node=!ledger_conn and policy=!operator_id and threads=!operator_threads",
      "if !enable_mqtt == true then process !anylog_path/deployment-scripts/demo-scripts/basic_msg_client.al",
      "if !enable_opcua == true then process !anylog_path/deployment-scripts/demo-scripts/opcua_client.al", 
      "if !enable_aggregations == true then set aggregations where dbms=!default_dbms and intervals=!aggregations_intervals and time=!aggregations_time and time_column=!aggregation_time_column and value_column=!aggregation_value_column", 
      "if !monitor_nodes == true then process !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al",
      "if !syslog_monitoring == true then process !anylog_path/deployment-scripts/demo-scripts/syslog.al",
      "if !deploy_local_script == true then process !local_scripts/local_script.al",
      "if !is_edgelake == false then process !local_scripts/policies/license_policy.al"
    ],
    "id" : "87ac01c5b6e4a95fb7f96898a5bf8cc0",
    "date" : "2025-05-15T22:20:38.799160Z",
    "ledger" : "global"
}}
```
6. AnyLog will then deploy / configure the different services based on the configuration policy. 
> `!` is the equivalent of `$` for AnyLog/EdgeLake. 

### What is the purpose of the Cluster policy and how does it work?

The _cluster_ policy is a logical policy that defines the relationship between Operator nodes, enabling high availability 
HA) and informing members of the network about the location and distribution of data. Each Operator node belongs to a 
Cluster, and a Cluster can consist of multiple Operator nodes. 

When an operator receives new data one of the things it does is check whether the table (and cluster) definition exist both 
locally and on the blockchain (as metadata). this information is then used by all other members of the network to query 
and share the data. 

### How does AnyLog ensure data consistency across Operator nodes?

Each operator node has a management database that keeps track of the files coming in, where they came from and where 
they went (for HA). This guarantees consistency, validation and remove of repeating data (files).      

### Can a single AnyLog node perform multiple roles at once?

A node can perform different roles based on the enabled services and databases it is connected to. The only limitation is 
enabling the operator and publisher services on the same instance.

### How is data partitioned in AnyLog and why do some tables have the par_ prefix?

AnyLog / EdgeLake partition the data automatically for the user. This can be disabled 
or personalized in the configuration file. When executing a query, AnyLog/EdgeLake basically scans only the relevant 
partitioned rather than the entire data, making it that much more efficient. 

Details can be found in [Metadata Requests](../metadata%20requests.md#creating-data-tables).

### What are the hardware or resource requirements for running different node types?
| Feature            | Requirement                                                                                                                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Operating System**| Linux (Ubuntu, RedHat, Alpine, Suse) <br> Windows  <br> Mac                                                                                                                                        |
| **Memory footprint**| 100 MB available for AnyLog deployed without Docker <br> 300 MB available for AnyLog with Docker                                                                                                   |
| **Databases**       | PostgreSQL installed (optional) <br> SQLite (default, no installation needed) <br> MongoDB (only if blob storage is needed)                                                                        |
| **CPU**             | Intel, ARM, and AMD architectures supported <br> Runs on single CPU machines up to large multi-core servers (including gateways, Raspberry Pi, etc.)                                               |
| **Storage**         | Supports horizontal scaling by adding nodes dynamically <br> Storage requirements depend on data volume and retention per node <br> Automated archival and data transfer to larger nodes supported |
| **Network**         | TCP-based network required (local, internet, or hybrid) <br> Overlay networks recommended (Nebula is default) <br> Static IP and 3 open ports accessible per node (via overlay or direct network)  |
| **Cloud Integration**| Built-in support for REST, Pub-Sub, and Kafka                                                                                                                                                      |
| **Deployment Options**| Executable (background process), Docker, or Kubernetes                                                                                                                                             |

Please visit [prerequisite.md](../training/prerequisite.md) for farther details. 

### How do I monitor the health and status of nodes in the AnyLog network?

AnyLog (and EdgeLake) have alert and monitoring capabilities that both on the machine level (ex. CPU, RAM, Network I/O and disk usage)
as well as on the data level. 

Details can be found in [alerts and monitoring.md](../alerts%20and%20monitoring.md).

### What is the difference between blockchain abstraction in EdgeLake and AnyLog Enterprise?


### How do I handle node failures or network partitions?


### Is it possible to upgrade EdgeLake to AnyLog Enterprise?

Since AnyLog builds on top of EdgeLake and a node its services based on user-defined configurations, update is as simple
as updating the image name in the docker-compose file from `anylogco/edgelake` to `anylogco/anylog-network`.

Directions for upgrading can be found [here](). 
