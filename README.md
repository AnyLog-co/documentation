# AnyLog Network 

<div align="center">
    <img src="imgs/anylog_logo.png" />
</div> 

AnyLog provides Real-Time Visibility and Management of Distributed Edge Data, Applications and Infrastructure.   
AnyLog transforms the edge to a scalable data tier that is optimized for IoT data, enabling organizations
to extract real-time insight for any use case in any industries spanning Manufacturing, Utilities, Oil & Gas, Retail,
Robotics, Smart Cities, Automotive, and more.  
With AnyLog deployed on edge nodes, the nodes become members of a peer-to-peer (P2P) network that provides access to
distributed IoT data from a single point, as if the data is organized and unified on a single machine. 
This approach creates two tiers: a physical tier that automates data management on the edge nodes, and a virtualized tier that
provides access to the distributed data from a single point.
This approach provides a cloud-like setup for the distributed edge making IoT data available in real time anywhere, anytime 
and for any use case, without the need to move the data and without locking customers into specific clouds, applications or hardware.

To receive additional info, email to: [info@anylog.co](mailto:info@anylog.co)


## Table of Content 
* **Deploy AnyLog**
  * [Getting Started](getting%20started.md)
  * [The AnyLog CLI](cli.md)  
  * [Basic AnyLog Deployment](training/)
  * [Docker Image](docker%20image.md)
  * [Background Processes](background%20processes.md)
  * [Starting an AnyLog Instance](starting%20an%20anylog%20instance.md)
  * [Master Node](master%20node.md)
  * [Node Configuration](node%20configuration.md)  
  * [Network Configuration](network%20configuration.md)
  * [Network Processing](network%20processing.md)  
  * [Using REST](using%20rest.md)
  * [Managing Data File Status](managing%20data%20files%20status.md)
  * [Metadata Management](metadata%20management.md)
  * [Kubernetes & Docker Deployment of AnyLog](deployments) 
  * [Setting Test Suites](test%20suites.md)
  
* **AnyLog Commands**
  * [Main Commands](anylog%20commands.md)
  * [File Commands](file%20commands.md)
  * [Test Commands](test%20commands.md)
  * [http commands](http%20commands.md)
  * [The dictionary](dictionary.md)
  
* **Managing Data**
  * [Adding Data](adding%20data.md)
  * [Metadata Requests](metadata%20requests.md)
  * [Mapping data to tables](mapping%20data%20to%20tables.md)
  * [JSON Data Transformation](json%20data%20transformation.md)
  * [Storing Images](image%20mapping.md)
  
* **Managing Metadata**
  * [Blockchain Commands](blockchain%20commands.md)
  * [Policies](policies.md#policies-based-metadata)  
  * [Blockchain Configuration](blockchain%20configuration.md)
  * [Using Ethereum](using%20ethereum.md)
 
* **Monitoring AnyLog**
  * [General Monitoring](monitoring%20calls.md) 
  * [Monitoring Nodes](monitoring%20nodes.md)
  * [Streaming Conditions](streaming%20conditions.md)
  * [Logging Events](logging%20events.md)
  * [Alerts & Monitoring](alerts%20and%20monitoring.md)
  * [Aggregations](aggregations)
  * [Monitoring File Status](managing%20data%20files%20status.md)
    
* **Querying Data**
  * [Data Queries](queries.md)
  * [SQL Setup](sql%20setup.md)
  * [Profile & Monitor Queries](profiling%20and%20monitoring%20queries.md)
  * [Querying Across the Network](network%20processing.md)

* **Security & Authentication**
  * [Authentication](authentication.md)
  * [Secure Network](secure%20network.md)
  * [Using NGINX as Proxy](deployments/Networking%20&%20Security/nginx.md)
  * [Using Nebula as Overlay Network](deployments/Networking%20&%20Security/nebula.md)

* **High-Availability (HA)**
  * [high availability](high%20availability.md)

* **Southbound Connectors**
  * [AnyLog as a Broker](message%20broker.md) 
  * [Using Edgex](using%20edgex.md)
  * [Using Kafka](using%20kafka.md)
  * [Using gRPC](using%20grpc.md)
  * [Using SysLog](using%20syslog.md)
  * [Registering OSIsoft's PI](registering%20pi%20in%20the%20anylog%20network.md)
  * [OPC-UA](opcua.md)

* **Northbound Connectors**
  * [AnyLog Remote-CLI](northbound%20connectors/remote_cli.md)
  * [Postman](northbound%20connectors/using%20postman.md)
  * [Grafana](northbound%20connectors/using%20grafana.md)
  * [PowerBI](northbound%20connectors/PowerBI.md)
  * [Google Drive](northbound%20connectors/Google.md)
  * [Generic Connector](northbound%20connectors/postgres%20connector.md)

* **Sample Code**
  * [Python Scripts](examples/Sample%20Python%20Scripts)
    * [Blockchain](examples/Sample%20Python%20Scripts/blockchain_add_policy_simple.py)
    * [Sending Data](examples/Sample%20Python%20Scripts/data)
  * [cURL Requests](examples/curl.sh)
  * [Configurations Files](examples/Configuration.md)