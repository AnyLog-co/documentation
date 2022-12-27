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
* **How to Deploy a Node & Using AnyLog CLI**
  * [Getting Started](getting%20started.md) 
  * [Starting an AnyLog Instance](starting%20an%20anylog%20instance.md)
  * [Master Node](master%20node.md)
  * [Network Configuration](network%20configuration.md)
  * [Understanding Background Processes](background%20processes.md)
  * [Using AnyLog CLI](anylog%20commands.md)
  * [Using REST](using%20rest.md)
  * [Managing Data File Status](managing%20data%20files%20status.md)
  * [Streaming Conditions](streaming%20conditions.md)
  * [Metadata Management](metadata%20management.md)
  * [Kubernetes & Docker Deployment of AnyLog](deployments)
    * [Docker Deployment](deployments/Docker)
    * [Kubernetes Deployment](deployments/Kubernetes)
    
* **Managing Data**
  * [Adding Data](adding%20data.md)
  * [Metadata Requests](metadata%20requests.md)
  * [Mapping data to tables](mapping%20data%20to%20tables.md)
  * [JSON Data Transformation](json%20data%20transformation.md)
  * [Storing Images](image%20mapping.md)
 
* **Monitoring AnyLog**
  * [General Monitoring](monitoring%20calls.md) 
  * [Monitoring Nodes](monitoring%20nodes.md)
  * [Logging Events](logging%20events.md)
  * [Alerts & Monitoring](alerts%20and%20monitoring.md)
  * [Monitoring Data](monitoring%20data.md)
  * [Monitoring File Status](managing%20data%20files%20status.md)
  * [Managing Configurations](managing%20configuration.md)
  
* **Querying Data**
  * [Build Queries](queries.md)
  * [SQL Setup](sql%20setup.md)
  * [Profile & Monitor Queries](profiling%20and%20monitoring%20queries.md)
  * [Querying Across the Network](network%20processing.md)
  * [SQL Testing](test%20suites.md)

* **Security & Authentication**
  * [Secure Network](Secure%20Network.md)
    * [Using NGINX as Proxy](deployments/Networking%20&%20Security/nginx.md)
    * [Using Nebula as Overlay Network](deployments/Networking%20&%20Security/nebula.md)
    * [Deploying Security](deployments/Networking%20&%20Security/security.md)
  * [Authentication](authentication.md)

* **High-Availability (HA)**
  * [high availability](high%20availability.md)
  * [Configuring Data Distribution](data%20distribution%20and%20configuration.md)

* **Southbound Connectors**
  * [AnyLog as a Broker](message%20broker.md) 
  * [Using Edgex](using%20edgex.md)
  * [Using Kafka](using%20kafka.md)
  * [Registering OSIsoft's PI](registering%20pi%20in%20the%20anylog%20network.md)

* **Northbound Connectors**
  * [AnyLog Remote-CLI](northbound%20connectors/remote_cli.md)
  * [AnyLog GUI](northbound%20connectors/using%20the%20gui.md)
  * [Postman](northbound%20connectors/using%20postman.md)
  * [Grafana](northbound%20connectors/using%20grafana.md)
  * [PowerBI](northbound%20connectors/PowerBI.md)
  * [Google Drive](northbound%20connectors/Google.md)
  * [Generic Connector](northbound%20connectors/postgres%20connector.md)

* **Sample Code**
  * [Python Scripts](examples/Sample%20Python%20Scripts)
    * [Blockchain](examples/Sample%20Python%20Scripts/blockchain)
    * [Sending Data](examples/Sample%20Python%20Scripts/data)
  * [cURL Requests](examples/curl.sh)
  * [Configurations Files](examples/Configuration.md)