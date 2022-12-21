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
  * [Starting an AnyLog Instance](deploying%20nodes%20&%20AnyLog%20CLI/starting%20an%20anylog%20instance.md)
  * [Master Node](deploying%20nodes%20&%20AnyLog%20CLI/master%20node.md)
  * [Understanding Background Processes](deploying%20nodes%20&%20AnyLog%20CLI/background%20processes.md)
  * [Using AnyLog CLI](deploying%20nodes%20&%20AnyLog%20CLI/anylog%20commands.md)
  * [Kubernetes & Docker Deployment of AnyLog](deployments/README.md)
    * [Docker Deployment](deployments/Docker)
    * [Kubernetes Deployment](deployments/Kubernetes)
    
* [Managing Data](data%20management)
  * [Adding Data](data%20management/adding%20data.md)
  * [Mapping data to tables](data%20management/mapping%20data%20to%20tables.md)

* [Querying Data](query%20data/)
  * [Build Queries](query%20data/queries.md)
  * [SQL Setup](query%20data/sql%20setup.md)
  * [SQL Testing](query%20data/test%20suites.md) 
* [Security & Authentication](security%20&%20authentication)
  * [Secure Network](security%20&%20authentication/Secure%20Network.md)
    * [Using NGINX as Proxy](deployments/Networking/nginx.md)
    * [Using Nebula as Overlay Network](deployments/Networking/nebula.md)
  * [Authentication](security%20&%20authentication/authentication.md)

* [Southbound Connectors](southbound%20connectors)
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