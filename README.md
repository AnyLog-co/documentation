# AnyLog Network 

<div align="center">
    <img src="imgs/anylog_logo.png" />
</div> 

AnyLog allows managing your data on edge nodes as if they're located at a single point. We currently operate with a 
selected group of companies that are using the network to manage their data, as well as  companies that build 
applications that leverage the network as a unified source of IoT data. 

As we are in an early beta stage, this program is not available to all. To join the program, email a request to 
[info@anylog.co](mailto:info@anylog.co)


## Table of Content 
* [How to Deploy a Node & Using AnyLog CLI](deploying%20nodes%20&%20AnyLog%20CLI)
  * [Getting Started](deploying%20nodes%20&%20AnyLog%20CLI/getting%20started.md) 
  * [Starting an AnyLog Instance](deploying%20nodes%20&%20AnyLog%20CLI/starting%20an%20anylog%20instance.md)
  * [Master Node](deploying%20nodes%20&%20AnyLog%20CLI/master%20node.md)
  * [Network Configuration](deploying%20nodes%20&%20AnyLog%20CLI/network%20configuration.md)
  * [Understanding Background Processes](deploying%20nodes%20&%20AnyLog%20CLI/background%20processes.md)
  * [Using AnyLog CLI](deploying%20nodes%20&%20AnyLog%20CLI/anylog%20commands.md)
  * [Using REST](deploying%20nodes%20&%20AnyLog%20CLI/using%20rest.md)
  * [Managing Data File Status](deploying%20nodes%20&%20AnyLog%20CLI/managing%20data%20files%20status.md)
  * [Streaming Conditions](deploying%20nodes%20&%20AnyLog%20CLI/streaming%20conditions.md)
  * [Metadata Management](data%20management/metadata%20management.md)
  * [Kubernetes & Docker Deployment of AnyLog](deployments)
    * [Docker Deployment](deployments/Docker)
    * [Kubernetes Deployment](deployments/Kubernetes)
    
* [Managing Data](data%20management)
  * [Adding Data](data%20management/adding%20data.md)
  * [Metadata Requests](data%20management/metadata%20requests.md)
  * [Mapping data to tables](data%20management/mapping%20data%20to%20tables.md)
  * [JSON Data Transformation](data%20management/json%20data%20transformation.md)
  * [Storing Images](data%20management/image%20mapping.md)
 
* [Monitoring AnyLog](monitoring)
  * [General Monitoring](monitoring/monitoring%20calls.md) 
  * [Monitoring Nodes](monitoring/monitoring%20nodes.md)
  * [Logging Events](monitoring/logging%20events.md)
  * [Alerts & Monitoring](monitoring/alerts%20and%20monitoring.md)
  * [Monitoring Data](monitoring/monitoring%20data.md)
  * [Monitoring File Status](monitoring/managing%20data%20files%20status.md)
  * [Managing Configurations](deploying%20nodes%20&%20AnyLog%20CLI/managing%20configuration.md)
  
* [Querying Data](query%20data/)
  * [Build Queries](query%20data/queries.md)
  * [SQL Setup](query%20data/sql%20setup.md)
  * [Profile & Monitor Queries](query%20data/profiling%20and%20monitoring%20queries.md)
  * [Querying Across the Network](query%20data/network%20processing.md)
  * [SQL Testing](query%20data/test%20suites.md)

* [Security & Authentication](security%20&%20authentication)
  * [Secure Network](security%20&%20authentication/Secure%20Network.md)
    * [Using NGINX as Proxy](deployments/Networking/nginx.md)
    * [Using Nebula as Overlay Network](deployments/Networking/nebula.md)
  * [Authentication](security%20&%20authentication/authentication.md)

* [High-Availability (HA)](high-availability)
  * [high availability](high-availability/high%20availability.md)
  * [Configuring Data Distribution](high-availability/data%20distribution%20and%20configuration.md)

* [Southbound Connectors](southbound%20connectors)
  * [AnyLog as a Broker](southbound%20connectors/message%20broker.md) 
  * [Using Edgex](southbound%20connectors/using%20edgex.md)
  * [Using Kafka](southbound%20connectors/using%20kafka.md)
  * [Registering OSIsoft's PI](southbound%20connectors/registering%20pi%20in%20the%20anylog%20network.md)

* [Northbound Connectors](northbound%20connectors)
  * [AnyLog Remote-CLI](northbound%20connectors/remote_cli.md)
  * [AnyLog GUI](northbound%20connectors/using%20the%20gui.md)
  * [Postman](northbound%20connectors/using%20postman.md)
  * [Grafana](northbound%20connectors/using%20grafana.md)
  * [PowerBI](northbound%20connectors/PowerBI.md)
  * [Google Drive](northbound%20connectors/Google.md)
  * [Generic Connector](northbound%20connectors/postgres%20connector.md)

* [Sample Code](examples)
  * [Python Scripts](examples/Sample%20Python%20Scripts)
    * [Blockchain](examples/Sample%20Python%20Scripts/blockchain)
    * [Sending Data](examples/Sample%20Python%20Scripts/data)
  * [cURL Requests](examples/curl.sh)
  * [Configurations Files](examples/Configuration.md)