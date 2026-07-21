# Documentation Reorganization Notes

This tree represents the proposed target documentation structure for AnyLog / Edge Data Fabric documentation.

The goal of this reorganization is not to rewrite the documentation from scratch. Existing content should be preserved 
where possible, but reorganized into a structure that better matches how users learn, deploy, operate, and extend 
AnyLog.

## Why this reorganization is needed

The original documentation structure evolved alongside the development of the AnyLog platform. Initially, documentation 
was created as a collection of files and later organized around technical components, engineering areas, and internal 
platform capabilities. This structure successfully captured the technical knowledge required to build and maintain 
AnyLog. However, as the platform matures, the documentation needs to evolve from an engineering-oriented organization 
into a user-oriented  workflow.

The primary question changes from:

  "What components exist in AnyLog and where are their documents?"

to:

  "What does a user need to understand and accomplish in order to successfully deploy and operate an Edge Data Fabric?"


A user does not typically approach AnyLog by looking for internal components. Instead, users need answers to operational 
questions:

  - What is AnyLog and how does the Edge Data Fabric work?
  - How do I deploy my first AnyLog node?
  - How does a standalone deployment grow into a production network?
  - How does data enter the system and where does it go?
  - How do I query and consume data?
  - How do nodes communicate and remain secure?
  - How do I manage metadata, policies, and distributed data?

The objective of this reorganization is to preserve the existing technical knowledge while restructuring it around the user's journey.

## Documentation flow

The new documentation flow follows the lifecycle of an AnyLog deployment:

  1. Understand AnyLog and the Edge Data Fabric
  2. Deploy a simple system
  3. Expand from standalone → small network → production → HA
  4. Understand how data enters, moves through, and leaves the system
  5. Understand the distributed metadata and blockchain layers
  6. Operate, troubleshoot, and extend the platform

The new structure separates documentation into clear categories:

  - **Conceptual documentation**
      What is AnyLog?
      How does the Edge Data Fabric work?

  - **Installation & Deployment documentation**
      How do I deploy and grow an AnyLog network?

  - **Training & Tutorials**
      How do I use AnyLog, commands, APIs, and development tools?

  - **Connector documentation**
      How does data enter and leave the system?

  - **Reference documentation**
      Commands, APIs, configuration, and technical details.

## Documentation philosophy

The documentation should follow the same progression as a user's adoption of AnyLog.

The goal is not to require users to understand the entire internal architecture before deploying the platform. Instead, 
users should first learn how to deploy and operate a working system, then progressively learn deeper capabilities.

The expected progression is:

  Deploy → Connect Data → Query Data → Secure → Manage → Extend

Technical concepts should be introduced at the point where they help users accomplish a task.

For example:
- A new user should understand that metadata and blockchain enable distributed coordination before needing to understand the internal implementation.
- A deployment engineer should understand node communication before configuring advanced networking.
- A developer should understand APIs and query behavior before extending the platform.

## Intended audience

AnyLog documentation serves multiple personas. Each section should explicitly identify its intended audience and 
expected outcome.

The primary operational role is the **AnyLog Administrator**, similar to a traditional DBA or system administrator, who 
is responsible for deploying, maintaining, and operating an Edge Data Fabric.

Additional users include:

  - **Field / Edge Engineer**
      Uses AnyLog to monitor operational data, understand machine performance, and troubleshoot edge systems.

  - **Business User / Department Manager**
      Uses collected data for analytics, reporting, performance analysis, and cost optimization.

  - **Deployment Engineer / Solution Engineer**
      Builds larger deployments, integrates AnyLog into existing environments, and develops applications on top of AnyLog.

For each documentation section, we should understand:

  - Who is the intended audience?
  - What problem are they trying to solve?
  - What level of technical detail do they need?
  - What action should they be able to complete after reading the documentation?

## Documentation boundaries

The purpose of documentation is to enable users to successfully deploy, operate, and extend AnyLog.

Documentation should help users accomplish common operational tasks, such as:

  - Deploying nodes
  - Adding nodes to a network
  - Publishing data
  - Querying data
  - Understanding data flow
  - Managing configurations
  - Operating production deployments

Support should focus on advanced or custom scenarios, such as:

  - Developing new southbound connectors
  - Integrating unsupported external systems
  - Extending platform functionality

The goal is to reduce dependency on support for normal operational workflows while allowing engineering resources to 
focus on advanced platform extensions.

## Content organization principles

Some concepts will intentionally appear in multiple locations because users encounter the same concept at different 
stages of their journey.

For example:

  - Data lifecycle is introduced in Getting Started,
  - Explained technically in Training & Tutorials,
  - Demonstrated practically in Examples & Use Cases.

This is intentional. Good documentation reinforces important concepts at the appropriate depth.

However, the same document should not exist in multiple locations. Each topic should have a clear primary location with 
references from other sections when needed.

---

The previous documentation structure was organized primarily around engineering components and internal development areas.

The new structure is organized around the user's workflow to build and operate a production-level Edge Data Fabric:

  Understand → Deploy → Connect Data → Query Data → Secure → Manage → Extend

The objective is that a new user can begin with:

  `01- Getting Started/`

and progressively move through:

  Deployment → Data Flow → Security → Metadata → Storage → Applications → Production


---
Legend:
  🆕  New document/content that does not currently exist
  🔄  Existing content moved/reorganized
  🔀  Multiple existing documents merged into one
  ❓  Needs validation or ownership decision
  👤  Ownership marker
  📍  Current path(s), added from a fresh file-level scan — annotation only, does not change the plan
  ⚠️  Flagged discrepancy between this document and the actual current tree — not corrected here, just noted
---
## Tree 
```
01- Getting Started/
|- intro-to-anylog.md 🆕
|   Purpose:  Primary introduction to AnyLog and Edge Data Fabric.
|   Topics:
|    - What is AnyLog?
|    - What is Edge Data Fabric (EDF)?
|    - EdgeLake vs Enterprise
|    - Terminology:
|        - Operator
|        - Publisher
|        - Query Node
|        - Metadata Manager (Data vs Metadata)
|          - Policy
|          - Blockchain
|    - High-level architecture
|    - Explain the fundamental lifecycle of data inside AnyLog. This is the conceptual version, a deeper dive belongs under 11- Examples & Use Cases/.
|        PLC generates Data → southbound connector → generate table → insert data → query data across nodes 
|   Source material:
|    - 04- Core Concepts/
|    - 01- Getting Started/
|   📍 04- Core Concepts/01 Policies.md, 02 Metadata Management.md; 01- Getting Started/01 Getting Started.md
|      and 01- Getting Started/Getting Started.md (both an unnumbered and numbered copy currently exist)
|- prerequisites.md 🔄
|   Existing content.
|   Keep mostly as-is.
|   Source:
|    - 01- Getting Started/
|   📍 01- Getting Started/02 Prerequisite.md
|   Check Missing: Docker/K8s versions, Python versions, OS / Ubuntu, Databases
|- install.md 🔄
|    Purpose: Customer-facing quick installation guide.
|    Todo: Convert the current customer email installation instructions into formal documentation.
|    ⚠️ No exact current file matches this — the "Todo" note suggests the source is an email, not existing
|       tree content, so there may be nothing to point at yet. Closest existing material:
|       01- Getting Started/07 Configure as a Service.md, 08 Installing 3 Anylog node.md, 09 Installing the VM OVA.md
|- deployment-journey.md 🆕
|   Purpose: Explain how a deployment grows over time.
|     Stage 1: standalone node → add a secondary operator and/or deploy each agent by itself →  multiple operators → HA to the cloud
|- full-deployment.md 🔄
|   Purpose: Step-by-step zero-touch deployment. 
|   Source: Installation/deployment documentation
|   📍 Best match (source line was not a specific path): 01- Getting Started/08 Installing 3 Anylog node.md
```
**Comments**: 
1. It might be worthwhile to have `deployment-journey.md` as part of the `intro-to-anylog.md` and `full-deployment.md` as part 
of the `install.md` document. 
For `intro-to-anylog.md`, the idea of `deployment-journey.md` would be a pargraph / diagram after "High-level architecture".
For `install.md` it would be built such that: 
* Part 1: here's recap of the email / how to get started 
* Part 2: here's how to deploy a larger network 

We also need to provide an architecture of the network vs architecture of the node. The network should be 
a part of intro, while the node should be a part of install. 

2. In `prereqs` we should have  compatibility matrix
    Purpose:
      Define supported environments.
    Topics:
      - Operating systems
      - Docker versions
      - Kubernetes versions
      - Database versions
      - Python versions
      - Supported connectors


```
02- Installation & Deployment/
  |- intro.md 🆕
  |   Purpose: Explain deployment models before showing commands.
  |   Topics:
  |   - Standalone
  |   - Small network
  |   - Production
  |   - HA deployment
  |- node-architecture.md 🔄
  |   Topics:
  |   - "What is"
  |   - Operator
  |    - Publisher
  |    - Query Node
  |    - Metadata Manager
  |  Source: 04- Core Concepts/
  |  📍 04- Core Concepts/B- Nodes Network Services/01 Nodes Network Architecture.md
  |- configuration-file.md 🆕 ❓ (Needs validation with Mark.)
  |   Purpose: Explain configuration flow.
  |   Logic:
  |   - User inputs configuration into .env file  
  |     → execute Make command
  |       → Docker / Kubernetes environment variables
  |         → AnyLog startup
  |           → convert Env variables into AnyLog variables: `set_params.al`
  |           Notes:
  |            - Most parameters have defaults.
  |            - Document which values require user input - `LEDGER_CONN`, `NODE_TYPE`, `LICENSE_KEY`, recommended: `COMPANY_NAME`
  |- docker.md 🔄
  |   Topics:
  |   - Zero-touch deployment
  |   - Configured deployment
  |   - Docker lifecycle
  |   Source: 03- Installation & Deployment/
  |   📍 03- Installation & Deployment/B- Containerization & Orchestration/01 Docker Image.md, 02 Docker Volumes.md
  |- k8s.md 🔄
  |   Source: 03- Installation & Deployment/
  |   📍 03- Installation & Deployment/B- Containerization & Orchestration/03 Kubernetes Networking.md, 04 Kubernetes Volumes.md
  |- ova.md 🔄
  |   Source: 03- Installation & Deployment/
  |   ⚠️ The stated source doesn't have an OVA file. The actual OVA content currently lives in
  |      01- Getting Started/09 Installing the VM OVA.md — different section entirely.
  |- on-prem.md 🔄
  | Source: 03- Installation & Deployment/
  |  📍 03- Installation & Deployment/A- Deployment Options/07 Deploying Anylog as a Service.md
  |     (also possibly relevant: 01- Getting Started/05 Executable Deployment.md, 07 Configure as a Service.md)
  |- orchestration-tools/
  |  |- ibm-ieam.md 🔄
  |  |   Source: 09- Integrations/C- Deployment tools/
  |  |   📍 09- Integrations/C- Deployment tools/03 IBM IEAM (Edge Application Manager).md
  |  |- open-horizon.md 🔄
  |  |   Source: 09- Integrations/C- Deployment tools/A- Open-Horizon (IBM)/
  |  |   📍 09- Integrations/C- Deployment tools/A- Open-Horizon (IBM)/Open Horizon.md
  |  |- barbara.md 🔄
  |  |   Source: 09- Integrations/C- Deployment tools/
  |  |   📍 09- Integrations/C- Deployment tools/02 Barbara.md
  |  |- dell-distributed-private-cloud.md 🔄
  |  |    Source: 09- Integrations/C- Deployment tools/
  |  |    📍 09- Integrations/C- Deployment tools/01 DELL Distributed Private Cloud.md
  |  |- zededa.md 🆕 (Planned but not documented)
  |     📍 Confirmed — no file by this name or subject exists anywhere in the current tree.
```

```
03- Training & Tutorials/
  |- background-processes.md 🔄
  |   Existing tutorial.
  |   Source: 02- Training & Tutorials/
  |   ⚠️ 02- Training & Tutorials/ has no "background processes" content — its closest-named file,
  |      "B- Advanced Topics/Background Deployment.md", is about deploying in the background, a different
  |      subject. The actual "Background Processes" content currently exists at
  |      04- Core Concepts/04 Background Processes.md and, separately, 15- Development & Scripting/01 background
  |      processes.md (two copies, not yet confirmed as identical content — flagged in the TODO already).
  |- deployment-scripts-explained.md 🔀
  |   Merge: deployment-process.md & deployment-scripts.md
  |   Source: 09- Integrations/
  |   📍 09- Integrations/01 deployment-process.md, 02 deployment-scripts.md
  |- querying-data-basics.md 🆕 <-- I think this hides in different files that can be merged into 1
  |   Purpose: Beginner query tutorial.
  |   Topics:
  |    - Direct query
  |    - REST query
  |    - Basic examples
  |- data-flow-and-query-flow.md 🆕
  |   Purpose: Explain how a query travels through the EDF.
  |   Example: REST Request → Query Node → Metadata Lookup → Identify Operators → Distributed Query → Merge Results → Return Response
  |- cli-and-commands/ 🔄
  |   Moved from: 14- Commands & CLI/
  |  |- cli.md 🔄
  |  |   📍 14- Commands & CLI (Command Line Interface)/02 CLI.md
  |  |- commands-cheatsheet.md 🆕
  |     ⚠️ Already exists: 14- Commands & CLI (Command Line Interface)/01 Commands cheatsheet.md — marker
  |        should likely be 🔄, not 🆕.
  |- command-categories/
  |  |- anylog-commands.md 🔄
  |  |   📍 14-.../A- Command Categories/01 Anylog Commands.md
  |  |- blockchain-commands.md 🔄
  |  |   📍 14-.../A- Command Categories/05 Blockchain Commands.md
  |  |- file-commands.md 🔄
  |  |   📍 14-.../A- Command Categories/02 File Commands.md
  |  |- http-commands.md 🔄
  |  |   📍 14-.../A- Command Categories/03 HTTP Commands.md
  |  |- test-commands.md 🔄
  |  |   📍 14-.../A- Command Categories/04 Test Commands.md
  |  |   ⚠️ Not accounted for anywhere in this plan: 14-.../03 get-cmds.md and 04 node-status commands.md
  |     both exist in the source folder but aren't listed above.
  |- development-and-scripting/
  |  |- executing-scripts.md 🔄
  |  |    Source: 15- Development & Scripting/A- Scripting/
  |  |    📍 15- Development & Scripting/A- Scripting/Executing Scripts.md
  |  |- debugging.md 🔄
  |  |    Source: 15- Development & Scripting/B- Debugging/
  |  |    📍 15- Development & Scripting/B- Debugging/Debugging.md
  |  |- python-apis.md 🔄
  |  |    Source: 15- Development & Scripting/C- APIs/
  |  |    📍 15- Development & Scripting/C- APIs/Python APIs.md
  |- sample-scripts/ 🔄
  |  |- Contains: Go examples, Python examples
  |     📍 15- Development & Scripting/A- Scripting/Sample Go Scripts/, Sample Python Scripts/
```
**Comments**: 
1. `querying-data-basics.md` and `data-flow-and-query-flow.md` could be merged into: here's what happens when you run a query (cmd: `query explain`) and 
here's how to run the query.
2. sample-scripts/ - we want a repo that has a "pip" capability for customers to download and use. That repo would contain
examples of python scripts and potentially the same thing for go, shell and other commonly used langauges.  

```
04- Southbound Interfaces/
  |- intro.md 🆕
  |   Purpose: Explain how external systems send data into AnyLog.
  |   Topics:
  |    - Industrial systems
  |    - Applications
  |    - IoT devices
  |    - Message brokers
  |- direct-connectors/ <-- Existing connector documentation.
  |   Covers:
  |    - Modbus
  |    - OPC-UA
  |    - DNP3
  |    - EtherNet/IP
  |    - gRPC
  |    - Other connectors
  |   📍 07- Southbound Interfaces/D- Direct Connectors Industrial/ — heavily duplicated currently: both
  |      numbered (01 Using GRPC.md ... 07 video-streaming.md) and unnumbered copies of DNP3.md, MODBUS.md,
  |      EtherNet IP.md, OPC UA Integration.md exist side by side. Also present: the three DNP3 companion docs
  |      built this session (DNP3 - Deploying Connector via Script.md, DNP3 - Mapping-Policies.md,
  |      DNP3 - TLS test certificates.md) and 05 data from edgex.md (an older draft, unrelated to the numbered
  |      sequence around it).
  |- generic/
  |  |- using-rest.md 🔄
  |  |    Purpose: Generic REST ingestion documentation.
  |  |    📍 07-.../A- Direct Connectors Generic/01 Using REST.md and an unnumbered duplicate Using REST.md
  |  |- message-broker.md 🔀
  |  |   Merge: Message Broker Setup.md
  |  |   Purpose: Core message broker concept.
  |  |   📍 07-.../A- Direct Connectors Generic/message-broker.md (already exists, built this session) +
  |  |      09- Integrations/B- Messages Brokers/01 Message Broker Setup.md (the file to merge in)
  |  |- mapping-policies.md 🆕
  |  |    Purpose: Explain how incoming data is mapped into the EDF.
  |  |    Topics:
  |  |    - Schema mapping
  |  |    - Policies
  |  |    - Metadata creation
  |  |    ⚠️ Already exists: 07-.../A- Direct Connectors Generic/02 mapping-policies.md — marker should
  |  |       likely be 🔄, not 🆕. Worth checking whether its current content already covers these topics
  |  |       or whether this is meant to be a rewrite.
  |- Monitoring/
  |  |- syslog.md 🔄
  |  |   📍 Fragmented across four files currently: 07-.../B- Third-party.../06 Syslog integration.md,
  |  |      06-1 Using Syslog.md, 062 Ingesting Syslog msgs.md, and 07-.../C- Direct Connectors Monitoring/
  |  |      Using Syslog.md.
  |  |- container-monitoring.md 🆕
  |  |   📍 No existing match found — genuinely new.
  |  |- node-monitoring.md 🆕
  |     ⚠️ Already exists, in two places: 07- Southbound Interfaces/03 node-monitoring.md and
  |        07-.../C- Direct Connectors Monitoring/node-monitoring.md — marker should likely be 🔄, not 🆕.
  |- third-party-apps/
  |  |- edgex/
  |  |  |- edgex.md 🔄
  |  |  |   📍 07-.../B- Third-party.../EdgeX.md
  |  |  |- edgex-complete-example.md 🔄
  |  |  |   📍 07-.../B- Third-party.../EdgeX - complete example.md
  |  |  |- edgex-integration.md 🔀
  |  |  |   Move from: 09- Integrations/B- Messages Brokers/
  |  |  |   Reason:
  |  |  |   - EdgeX belongs with EdgeX documentation,
  |  |  |   - not generic message brokers.
  |  |  |   📍 09- Integrations/B- Messages Brokers/03 edgex integration.md, 03-1 EdgeX Foundry Integration example.md
  |  |  |   ⚠️ Not accounted for anywhere in this plan: 07-.../B- Third-party.../04 Using MQTT (EdgeX).md —
  |  |  |      also EdgeX-related, currently unmentioned.
  |  |- kafka.md 🔄 <--  remote Kafka broker
  |  |    Source: 09- Integrations/B- Messages Brokers/
  |  |    ⚠️ The stated source doesn't have a Kafka file. The actual current Kafka doc is
  |  |       07-.../B- Third-party.../05 Using Kafka.md.
  |  |- node-red.md 🔄
  |  |   📍 07-.../B- Third-party.../02 node-red.md
  |  |- telegraf.md 🔄
  |  |   📍 07-.../B- Third-party.../03 telegraf.md
  |  |- kubearmor.md 🔄
  |  |   📍 07-.../B- Third-party.../01 kubearmor.md
  |  |- Mosquitto.md  🆕 <-- remote MQTT broker 
  |     📍 Confirmed — no file by this name or subject exists anywhere in the current tree.
```
**Comment**: 
1. if we're dealing with `message broker` and that covers AnyLog as an MQTT broker + "Kaflka" broker, then we need to discuss
_Confluent_ as opposed to Kafka.md and include Mosquitto.md as a counter for MQTT foreign / remote broker. 
2. Syslog.md can reside as either 3rd party, which makes sense because it's an extrnal app sending dat ainto AnyLog. But also 


```
05- Northbound Connectors/
  |- intro.md 🆕
  |   Purpose: Explain how applications consume AnyLog data.
  |   Topics:
  |    - REST
  |    - SQL
  |    - BI tools
  |    - Applications
  |- query-data.md 🔄
  |   Purpose: Querying data and metadata from external applications.
  |   📍 02- Training & Tutorials/Query Data.md (its current home is Training & Tutorials, not Northbound)
  |- generic/
  |  |- postman-integration.md 🔄
  |  |   📍 08- Northbound Connectors/02 Postman Integration.md and an unnumbered duplicate under
  |  |      A- BI Tools — Generic/Postman Integration.md
  |  |- postgres-connector.md 🔄
  |  |    Note: This document covers the situation where the BI Tool does not have native REST, and instead requires connecting to Postgres database directly (ex. Taboola an Looker).
  |  |    📍 Three copies currently: 08- Northbound Connectors/03 postgres-connector.md,
  |  |       08-.../A- BI Tools — Generic/postgres-connector.md, and
  |  |       09- Integrations/A- Databases/01 Postgres Connector.md
  |  |- notifications.md 🔄
  |     📍 08- Northbound Connectors/06 notifications.md, 06-1 Notifications example.md
  |- bi-tools/ 🔄
  |   Absorbs: 10- Visualization & Dashboards/
  |  |- grafana/
  |  |  |- using-grafana.md 🔄
  |  |  |   📍 08-.../A- BI external tools — Grafana/Using Grafana.md AND
  |  |  |      08-.../A- BI external tools — Office/03 Using Grafana.md (duplicated across two different
  |  |  |      "A-" folders, not just numbered/unnumbered within one)
  |  |  |- importing-grafana-dashboard.md 🔄
  |  |  |   📍 08-.../A- BI external tools — Grafana/Importing Grafana Dashboard.md AND
  |  |  |      08-.../A- BI external tools — Office/03-2 Importing Grafana Dashboard.md
  |  |  |- grafana-setup.md 🔄
  |  |  |   📍 10- Visualization & Dashboards/A- Grafana/01 Grafana Setup.md
  |  |- powerbi/
  |  |   📍 08-.../A- BI external tools — Office/04 Power BI Connector.md, MS Office Connector.md
  |  |- qlik/
  |  |   📍 08-.../A- BI external tools — Office/01 Qlik Connector.md, 02 Qlik How to.md,
  |  |      Qlik Connector.md (unnumbered duplicate)
  |  |   ⚠️ Also present in that same folder: "03-1 Connecting Grafana.md" — filed between two Qlik entries
  |  |      but appears to be Grafana content by name, worth checking whether it's misfiled.
  |  |- google-drive/
  |     📍 08-.../A- BI external tools — Office/05 Google Drive Connector.md, 05-1 Google example.md,
  |        Google Drive Connector.md (unnumbered duplicate)
  |- node-red-dashboards.md 🔄
  |     Source: Visualization & Dashboards/
  |     📍 10- Visualization & Dashboards/02 Node Red.md
  |- llm-dashboard-generation.md 🔄
  |    Source: Visualization & Dashboards/
  |    📍 10- Visualization & Dashboards/01 LLM Dashboard Generation.md
 ```
```
06- Network & Security/
  |- intro.md 🆕 <-- This should be the entry point before TPM, certificates, and networking details.
  |   Purpose: Explain the security model of the Edge Data Fabric.
  |   Topics:
  |   - Trust model
  |   - Node identity
  |   - Authentication
  |   - Authorization
  |   - Certificates
  |   - Encryption
  |   - Network topology
  |- networking/
  |   Purpose: Consolidate all network-level documentation.
  |  |- network.md 🆕
  |  |    Explain AnyLog network communication.
  |  |    📍 No exact existing file, though 05- Anylog Nodes Network & Security/01 Network Exchanges.md
  |  |       and the various networking.md copies may be relevant source material.
  |  |- nginx.md 🔄
  |  |    Existing NGINX/networking documentation.
  |  |    📍 05- Anylog Nodes Network & Security/B- Networking/NGINX Configuration.md
  |  |- dnp3-tls-test-certificates.md 🔄
  |  |    Source:
  |  |      05- AnyLog Nodes Network & Security/
  |  |     DNP3 certificates/
  |  |    📍 05- Anylog Nodes Network & Security/C- DNP3 certificates/ca_chain/ca-chain README.md
  |  |    ⚠️⚠️ CRITICAL — this exact source directory also currently contains real, committed private key
  |  |       files: anylogDNP3ca.key, master1.key, outstation1.key, outstation2.key, alongside their .cert
  |  |       counterparts and create_certificates.sh. This is the security issue flagged repeatedly earlier
  |  |       in this project — a version of this same content with no committed key material already exists
  |  |       at 07- Southbound Interfaces/D- Direct Connectors Industrial/DNP3 - TLS test certificates.md.
  |  |       Recommend sourcing from that clean file instead of this directory, and deleting this directory's
  |  |       key files regardless of what happens to the doc.
  |  |- Overlay Network documents
  |  |    📍 05- Anylog Nodes Network & Security/B- Networking/02 overlay-certificate-authority.md,
  |  |       03 overlay-network.md
  |  |- certificate-authority.md 🔄 (nebula)
  |  |   Source: 05- AnyLog Nodes Network & Security/
  |  |   📍 05- Anylog Nodes Network & Security/B- Networking/02 overlay-certificate-authority.md
  |- authentication.md 🔄  <-- Existing authentication documentation.
  |   Source:
  |   - 05- Networking & Security/
  |   - 05- AnyLog Nodes Network & Security/
  |   📍 05- Networking & Security/A- Built-in Authentication/Authentication.md AND
  |      05- Anylog Nodes Network & Security/02 Authentication.md (two separate copies, different folders)
  |- authentication-example.md 🔄
  |   Purpose: Authentication walkthrough/example.
  |   Source: 05- Networking & Security/
  |   📍 05- Networking & Security/A- Built-in Authentication/Authentication-policies.md
  |- securing-the-network.md 🔄
  |   Purpose: Explain how nodes securely communicate.
  |   Topics:
  |    - Node trust
  |    - Secure communication
  |    - Certificate validation
  |    - Network protection
  |   Source: 05- AnyLog Nodes Network & Security/
  |   📍 05- Anylog Nodes Network & Security/03 Securing the Network.md — also currently exists at
  |      03- Installation & Deployment/Securing the Network.md and 00- archive/05- Networking & Security/
  |      Securing the Network.md (three copies total across the tree)
  |- tpm/  <-- Existing TPM documentation.
  |  |- Source:
  |  |    05- AnyLog Nodes Network & Security/
  |  |    A- Trusted Platform Module (TPM)
  |  |  📍 05- Anylog Nodes Network & Security/A- Trusted Platform Module (TPM)/01 TMP Configuration.md,
  |  |     02 Software TPM.md

```
**Comments**:
1. Maybe we should merge the authentication documents into 1: explain -> here's how to do it
2. DNP3 (`os-reorg`) does not have  all the certification, but rather is broken into 3 files
3. DNP3 is a southbound services not networking

```
07- Blockchain + Metadata/
  |- intro.md 🆕
  |   Purpose: Explain the Edge Data Fabric control plane.
  |   Key concept:
  |     Blockchain: The distributed network coordination layer.
  |     Metadata: The knowledge layer describing / what exists in the network.
  |     Policies: The behavior layer defining /  how data is handled.
  |   Topics:
  |    - How the EDF knows where data exists
  |    - How nodes discover information
  |    - How metadata enables distributed queries
  |    - policy types: node, config, schedule, security, UNS
  |- blockchain-as-a-service.md 🔄
  |   Existing blockchain documentation.
  |   Source:
  |   - 19- Appendices/B- Blockchain Integration
  |   - Blockchain-related documentation
  |   📍 19- Appendices/B- Blockchain Integration/01 Blockchain (internet) Configuration.md,
  |      02 Blockchain example.md, 03 Using Ethereum.md
  |- blockchain-and-metadata.md 🔄 
  |   Purpose:  Core EDF explanation - Explain the relationship between: Data vs Metadat and Policies vs Bloclchain 
  |   📍 04- Core Concepts/B- Nodes Network Services/03 Blockchain & Metadata.md
  |   ⚠️ That same folder also has a separate "03 policies-metadata.md" — same numeric prefix (03), two
  |      different files. Worth confirming whether blockchain-as-a-service.md and blockchain-and-metadata.md
  |      are meant to stay genuinely distinct, since their names and this section's own later comment both
  |      suggest real overlap risk.
  |- metadata.md 🆕
  |   Purpose: Dedicated metadata reference.
  |   Topics:
  |    - Metadata structures
  |    - Metadata lifecycle
  |    - Data discovery
  |    - Query routing
  |   📍 Possibly relevant existing source, despite the 🆕 marker: 04- Core Concepts/02 Metadata Management.md
  |- policies.md 🔄
  |   Purpose: Explicit policy documentation.
  |   Topics:
  |    - Data policies
  |    - Mapping policies
  |    - Distribution policies
  |    - Query policies
  |    - Network behavior
  |   Source: Existing policy documentation
  |   📍 Best match (source line was not a specific path): 04- Core Concepts/01 Policies.md
  |- uns/
  |   Source: 13- UNS/ 
  |   📍 13- UNS (Unified Name Spaces)/ currently has both numbered (01 UNS.md, 02 UNS example.md) and
  |      unnumbered (UNS.md, UNS-custom.md, UNS-dynamic-custom-example.md) copies side by side.
  |  |- uns.md 🔄 
  |  |   📍 13-.../01 UNS.md and the unnumbered UNS.md
  |  |- uns-custom.md 🔄
  |  |   📍 13-.../UNS-custom.md (unclear whether "02 UNS example.md" is meant to correspond to this file
  |  |      or to uns-dynamic-custom-example.md below — worth confirming)
  |  |- uns-dynamic-custom-example.md 🔄
  |     📍 13-.../UNS-dynamic-custom-example.md
  ```

**Comment**: This section probably has a lot of content that can be merged into a single file.

```
08- Data Management/
  |- intro.md 🆕
  |   Purpose: Explain how AnyLog stores and manages data.
  |   Topics:
  |    - SQL storage
  |    - Blob storage
  |    - NoSQL
  |    - Streaming data
  |   - Partitioning
  |   - Aggregation
  |- SQL Storage/
  |   Absorbs: 09- Integrations/A- Databases/
  |- sql-database.md 🔄
  |    Source: 09- Integrations/A- Databases/
  |    📍 09- Integrations/A- Databases/sql-databases.md
  |- databases-and-tables.md 🔄
  |   Source: 06- Data Management/
  |   ⚠️ Its actual current home is 02- Training & Tutorials/Databases & Tables.md, not 06- Data Management —
  |      that section has no file by this name.
  |- adding-data.md 🔄
  |    Source: 06- Data Management/
  |    📍 06- Data Management/A- Data Ingestion/01 Adding Data.md
  |- mapping-data-to-tables.md 🔄
  |    Source: 06- Data Management/
  |    📍 06- Data Management/A- Data Ingestion/02 Mapping Data to Tables.md
  |- json-data-transformation.md 🔄
  |   Source: 06- Data Management/
  |   📍 06- Data Management/A- Data Ingestion/03 JSON Data Transformation.md
  |- streaming-data.md 🔄
  |   Source: 06- Data Management/
  |   📍 06- Data Management/A- Data Ingestion/04 Streaming Data Into Anylog.md
  |-  partitioning + aggregations.md 🔄
  |     Source: 06- Data Management/
  |     📍 06- Data Management/B- Query & Aggregations/02 Aggregations.md — note the actual partitioning
  |        commands/detail currently live in 02- Training & Tutorials/Databases & Tables.md, not in
  |        06- Data Management at all.
  |- Blobs & NoSQL/
  |  |- bucket-data-management.md 🔄
  |  |   📍 04- Core Concepts/03 Bucket Data Management.md
  |  |- milvusdb.md 🔄
  |  |    Source: 09- Integrations/A- Databases/
  |  |    📍 09- Integrations/A- Databases/milvusdb.md
  |  |- configuring-mongodb.md 🔄
  |  |    Source: 09- Integrations/A- Databases/
  |  |    📍 09- Integrations/A- Databases/02 configuring mongodb.md
  |  |- Minio.md 🔄
  |     📍 19- Appendices/C- Reference Materials/minio.md
```
**Comments**: 
1. The SQL stuff, I'm not sure if it's standalone files or multiple files in the repo
2. We could potentially merge some stuff here as well 

```
09- Extended Services/
  |- intro.md 🆕
  |   Purpose: Advanced operational capabilities.
  |   Audience: Users who already understand:
  |      - Deployment
  |      - Data lifecycle
  |      - Metadata
  |      - Queries
  |- mcp.md 🔄 <-- Single file.
  |   Position: Immediately after UNS because MCP builds / on metadata and AI interaction.
  |   Source: 12- MCP & LLMs/
  |   📍 12- MCP & LLMs/01 mcp.md
  |   ⚠️ Note: UNS currently sits in section 07 (Blockchain + Metadata), not adjacent to this section —
  |      the "immediately after UNS" intent and the actual numbered placement don't currently match.
  |- profiling-and-monitoring-queries.md 🆕
  |   Purpose: Explain query analysis and optimization.
  |   Topics:
  |    - Query profiling
  |    - Performance analysis
  |    - Troubleshooting slow queries
  |   ⚠️ Already exists: 06- Data Management/B- Query & Aggregations/03 Profiling & Monitoring Queries.md —
  |      marker should likely be 🔄, not 🆕.
  |- scheduler + scheduled-pull.md 🔄 <-- Existing scheduled pull functionality.
  |   📍 15- Development & Scripting/02 scheduler.md and 06- Data Management/B- Query & Aggregations/
  |      04 Scheduled Pull.md
  |- monitoring-and-alerts/
  |  |- alerts-and-monitoring.md 🔄
  |  |    Source: 06- Data Management/D- Monitoring & Alerts/
  |  |    📍 06- Data Management/D- Monitoring & Alerts/01 Alerts & Monitoring.md
  |  |- monitoring-nodes.md 🔄
  |  |   📍 06-.../D- Monitoring & Alerts/02 Monitoring Nodes.md
  |  |- monitoring-calls.md 🔄
  |  |   📍 06-.../D- Monitoring & Alerts/03 Monitoring Calls.md
  |  |- logging-events.md 🔄
  |     📍 06-.../D- Monitoring & Alerts/05 Logging Events.md
  |     ⚠️ Not accounted for anywhere in this plan: 06-.../D- Monitoring & Alerts/04 Continuous Monitoring
  |        with Automated Alerts.md and 06 Managing Data Files Status.md, both present in the source folder.
  |- high-availability.md 🔄
  |   Purpose: Explain SQL/data redundancy.
  |   Topics:
  |    - Data replication
  |    - Redundancy strategy
  |    - Production HA architecture
  |   Source: 06- Data Management/E- High Availability/
  |   📍 06- Data Management/E- High Availability/High Availability.md
  |- performance-tuning.md 🆕
  |   Purpose: Advanced performance guidance.
  |   Topics:
  |    - Query optimization
  |    - Storage optimization
  |    - Partitioning strategy
  |    - Scaling operators
  |- upgrade-guide.md 🆕
  |   Purpose: Explain upgrades between releases.
  |   Topics:
  |    - Version compatibility
  |    - Upgrade process
  |    - Migration considerations
```
```
10- EDM (Edge Data Manager)/ 👤 100% Roy
  |- edm.md <-- Main EDM overview.
  |   📍 11- EDM tool (Edge Data Manager)/02 EDM.md
  |   ⚠️ Not accounted for anywhere in this plan: 11- EDM tool (Edge Data Manager)/01 remote-gui.md, also
  |      present in the source folder.
  |- install.md 🆕
  |   Purpose: EDM installation process.
  |- UNS.md 🆕
  |   Purpose: Explain EDM integration with UNS.
  |- MCP.md 🆕
  |   Purpose: Explain EDM MCP integration.
  |- add-remove-plugins.md 🆕
  |   Purpose: Plugin lifecycle management.
  |   Topics:
  |      - Add plugins
  |      - Remove plugins
  |      - Configure plugins

11- Examples & Use Cases/ 👤 100% Mark
  |- intro.md 🆕
  |   Purpose:Introduction to practical AnyLog examples.
  |   Topics:
  |     - What examples are available
  |     - How examples are structured
  |     - What each example demonstrates
  |     - Expected outcomes after completing an example
  |     - Data lifecycle overview - Explain the complete flow of data through AnyLog:
  |         Data Source → Southbound Connector → Data Mapping / Policies → Operator (Storage)  → Query Data → Application / Dashboard
  |- sample-options.md 🆕
  |   Purpose Document the built-in examples available with AnyLog.
  |   Topics:
  |     - Overview of each example
  |     - Required deployment setup
  |     - Data sources used
  |     - Capabilities demonstrated
  |     - Expected results
  |- node-red-example/
  |   Purpose: Demonstrate integration with Node-RED.
  |   Contains:
  |     - Setup instructions
  |     - Data flow explanation
  |     - Example workflows
  |- wind-turbine-example/
  |   Purpose: End-to-end Edge Data Fabric example.
  |   Demonstrates:
  |     - Data ingestion
  |     - Metadata
  |     - Querying
  |     - Application integration
  |     - MCP / LLM interaction (if applicable)
  |- node-monitoring-example/
  |   Purpose: Demonstrate monitoring an AnyLog deployment.
  |   Demonstrates:
  |     - Publisher monitoring
  |     - Operator monitoring
  |     - Query node monitoring
  |     - Network visibility
  |- video-streaming-example/
  |   Purpose: Demonstrate streaming data/video use cases.
  |   Demonstrates:
  |     - High-volume data flow
  |     - Streaming ingestion
  |     - Data consumption
  |
  | 📍 This whole section's likely source material — not individually cited above — is
  |    16- Examples & Use Cases/01 Onboarding Commands.md, 02 Connecting Nodes.md, 03 Data Monitoring.md,
  |    04 Resource Monitoring.md, 05 Video Streaming.md.
```
```
12- Support & Troubleshooting/
  |- intro.md 🆕
  |   Purpose: Explain troubleshooting methodology.
  |   Topics:
  |   - Where to start
  |   - Logs
  |   - Monitoring
  |   - Common failure points
  |   - Escalation process
  |- troubleshooting.md 🔄
  |   Source:
  |    17- Support & Troubleshooting/
  |    01 troubleshooting.md
  |- FAQ.md 🔄
  |   Source:
  |     17- Support & Troubleshooting/
  |     02 FAQ 4 troubleshooting.md
  |   ⚠️ Still a duplicate: 19- Appendices/C- Reference Materials/FAQ.md also currently exists, separately.
  |- common-issues.md 🔄
  |   Source:
  |     17- Support & Troubleshooting/
  |     03 ND common_issues.md
  |-  networking-MTU-issues.md 🔄
  |     Source:
  |       17- Support & Troubleshooting/
  |       04 ND Issue Networking_MTU_size.md
  |- live-data-generator.md 🔄
  |   Source: 17- Support & Troubleshooting/
  |   📍 17- Support & Troubleshooting/live-data-generator.md (unnumbered, sits alongside the four numbered
  |      files above rather than being part of that sequence)
  |- best-practices.md 🆕
  |   Purpose: Operational guidance before issues occur.
  |   Topics:
  |    - Deployment recommendations
  |    - Naming conventions
  |    - Security practices
  |    - Scaling recommendations
  |    - Backup strategies
  |    - Monitoring recommendations
```
```
13- RELEASE Notes/ <--  Existing release documentation.
  📍 18- Releases Notes/01 AnylogEDF Releases Notes.md, 02 AnylogEDF SOURCE-CHANGELOGS.md,
     03 AnylogEDF DEPLOYMENT_SCRIPTS-CHANGELOGS.md, 04 AnylogEDF DOCKER_COMPOSE-CHANGELOG.md
     (a previously-flagged "MOSHE-NOTES.md" file does not appear in the current source folder in this scan —
     worth confirming it was intentionally removed rather than just missed.)
```
```
14- Appendices/
  Purpose: Reference information that does not belong in the main learning path.
  |- A- Legal & Licensing 🔄
  |   📍 19- Appendices/A- Legal & Licensing/01 AnylogEDF Evaluation License Agreement.md,
  |      02 Privacy Policy.md, 03 Notice of Open Source Usage.md,
  |      AnylogEDF used OPENSOURCE-NOTICE.html, AnylogEDF used OPENSOURCE-NOTICE.md
  |- B- Blockchain Integration 🔄
  |   📍 19- Appendices/B- Blockchain Integration/01 Blockchain (internet) Configuration.md,
  |      02 Blockchain example.md, 03 Using Ethereum.md
  |- C- Reference Materials 🔄
  |   📍 19- Appendices/C- Reference Materials/FAQ.md, configuration examples.md, dictionary.md,
  |      helpers.md, image mapping.md, minio.md, sql setup.md, streaming conditions.md
  |      (the FAQ.md and sql setup.md here are both still-open duplicate/fragmentation issues flagged
  |      elsewhere in this project — see the FAQ note under 12- Support & Troubleshooting above.) 
  ```