# AnyLog Documentation

## Deploy AnyLog
- [Getting Started](documentation/getting%20started.md)
- [The AnyLog CLI](documentation/cli.md)
- [Basic AnyLog Deployment](documentation/training)
- [Docker Image](documentation/docker%20image.md)
- [Background Processes](documentation/background%20processes.md)
- [Starting an AnyLog Instance](documentation/starting%20an%20anylog%20instance.md)
- [Master Node](documentation/master%20node.md)
- [Node Configuration](documentation/node%20configuration.md)
- [Network Configuration](documentation/network%20configuration.md)
- [Network Processing](documentation/network%20processing.md)
- [Using REST](documentation/using%20rest.md)
- [Managing Data File Status](documentation/managing%20data%20files%20status.md)
- [Metadata Management](documentation/metadata%20management.md)
- [Kubernetes & Docker Deployment of AnyLog](documentation/deployments)
- [Setting Test Suites](documentation/test%20suites.md)

## AnyLog Commands
- [Main Commands](documentation/anylog%20commands.md)
- [File Commands](documentation/file%20commands.md)
- [Test Commands](documentation/test%20commands.md)
- [HTTP Commands](documentation/http%20commands.md)
- [The Dictionary](documentation/dictionary.md)

## Managing Data
- [Adding Data](documentation/adding%20data.md)
- [Metadata Requests](documentation/metadata%20requests.md)
- [Mapping Data to Tables](documentation/mapping%20data%20to%20tables.md)
- [JSON Data Transformation](documentation/json%20data%20transformation.md)
- [Storing Images](documentation/image%20mapping.md)

## Managing Metadata
- [Blockchain Commands](documentation/blockchain%20commands.md)
- [Policies](documentation/policies.md#policies-based-metadata)
- [Blockchain Configuration](documentation/blockchain%20configuration.md)
- [Using Ethereum](documentation/using%20ethereum.md)

## Monitoring AnyLog
- [General Monitoring](documentation/monitoring%20calls.md)
- [Monitoring Nodes](documentation/monitoring%20nodes.md)
- [Streaming Conditions](documentation/streaming%20conditions.md)
- [Logging Events](documentation/logging%20events.md)
- [Alerts & Monitoring](documentation/alerts%20and%20monitoring.md)
- [Aggregations](documentation/aggregations)
- [Monitoring File Status](documentation/managing%20data%20files%20status.md)

## Querying Data
- [Data Queries](documentation/queries.md)
- [SQL Setup](documentation/sql%20setup.md)
- [Profile & Monitor Queries](documentation/profiling%20and%20monitoring%20queries.md)
- [Querying Across the Network](documentation/network%20processing.md)

## Security & Authentication
- [Authentication](documentation/authentication.md)
- [Secure Network](documentation/secure%20network.md)
- [Using NGINX as Proxy](documentation/deployments/Networking%20&%20Security/nginx.md)
- [Using Nebula as Overlay Network](documentation/deployments/Networking%20&%20Security/nebula.md)

## High-Availability (HA)
- [High Availability](documentation/high%20availability.md)

## Southbound Connectors
- [AnyLog as a Broker](documentation/message%20broker.md)
- [Using Edgex](documentation/using%20edgex.md)
- [Using Kafka](documentation/using%20kafka.md)
- [Using gRPC](documentation/using%20grpc.md)
- [Using SysLog](documentation/using%20syslog.md)
- [Registering OSIsoft's PI](documentation/registering%20pi%20in%20the%20anylog%20network.md)
- [OPC-UA](documentation/opcua.md)
- [EtherNet/IP](documentation/enthernetip.md)
- [Scheduled Pull](documentation/scheduled%20pull.md)

## Northbound Connectors
- [AnyLog Remote-CLI](documentation/northbound%20connectors/remote_cli.md)
- [Postman](documentation/northbound%20connectors/using%20postman.md)
- [Grafana](documentation/northbound%20connectors/using%20grafana.md)
- [PowerBI](documentation/northbound%20connectors/PowerBI.md)
- [Google Drive](documentation/northbound%20connectors/Google.md)
- [Generic Connector](documentation/northbound%20connectors/postgres%20connector.md)

## Sample Code
- [Python Scripts](documentation/examples/Sample%20Python%20Scripts)
  - [Blockchain](documentation/examples/Sample%20Python%20Scripts/blockchain_add_policy_simple.py)
  - [Sending Data](documentation/examples/Sample%20Python%20Scripts/data)
- [cURL Requests](documentation/examples/curl.sh)
- [Configurations Files](documentation/examples/Configuration.md)

---

## Suggested Standard Structure

To align with common documentation practices:

### Introduction
- What is *AnyLog*? -- [intro_to_anylog.md](intro_to_anylog.md) 
- Key Concepts (Nodes, Blockchain, Query, P2P) - Look @ [FAQ](FAQ.md)
- [Architecture](intro_to_anylog.md)
- Whitepapers

### Quick Start
- [Quick Start](quick_start.md) - this is very big! we need to break this down 
- One machine (Windows / macOS / Ubuntu)
- Two machines (networked)

### Installation
- System Requirements -- [prerequisite.md](prerequisite.md)
- Docker Hub Access 
- License Activation
- Configuration Basics

### Node Types
- Edge Node
- Coordinator Node
- Query Node
- Blockchain Node

### Tokenomics
*(if applicable)*

### User Guides
- Run your first query
- Connect external DB
- Add new metadata to blockchain

### Advanced Topics
- Security & Encryption
- Scaling a multi-node setup
- Monitoring
- [Updating or Restarting Nodes](deployments/upgrade_anylog.md)

### Troubleshooting
- Common Errors
- Logs Explained
- [FAQs](FAQ.md)

### Resources
- Video Tutorials <-  added icon
- Community & Support <-  added icon
- Legal Links
