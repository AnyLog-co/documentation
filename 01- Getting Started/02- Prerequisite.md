---
title: "Prerequisite and setup considerations"
description: "pre-req for AnyLog"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change** | **Version** |
 |------------|----------------|------------|-------------|
 |            |                |            |             |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606    |
 |            |
--->


---
# Prerequisite and setup considerations

| Feature            | Requirement                                                                                                                                                                                                                                                                                              |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| Operating System   | Linux (Ubuntu, RedHat, Alpine, Suse)                                                                                                                                                                                                                                                                     | 
|                    | Windows                                                                                                                                                                                                                                                                                                  |
| Python             | 3.11 - 3.13                                                                                                                                                                                                                                                                                              |
| Memory footprint   | 100 MB available for the AnyLog deployed without Docker                                                                                                                                                                                                                                                  |
|                    | 300 MB available for AnyLog deployed with Docker                                                                                                                                                                                                                                                         |
| Databases          | PostgreSQL installed (optional)                                                                                                                                                                                                                                                                          |
|                    | SQLite (default, no need to install)                                                                                                                                                                                                                                                                     |
|                    | MongoDB installed (Only if blob storage is needed)                                                                                                                                                                                                                                                       |
| CPU                | Intel, ARM and AMD are supported.                                                                                                                                                                                                                                                                        |
|                    | AnyLog can be deployed on a single CPU machine and up to the largest servers (can be deployed on gateways, Raspberry PI, and all the way to the largest multi-core machines).                                                                                                                            |
| Storage            | AnyLog supports horizontal scaling - nodes (and storage) are added dynamically as needed, therefore less complexity in scaling considerations. Requirements are based on expected volume and duration of data on each node. AnyLog supports automated archival and transfer to larger nodes (if needed). |
| Network            | Required: a TCP based network (local TCP based networks, over the internet and combinations are supported)                                                                                                                                                                                               |
|                    | An overlay network is recommended. Most overlay networks can be used transparently. Nebula used as a default overlay network.                                                                                                                                                                            |
|                    | Static IP and 3 ports open and accessible on each node (either via an Overlay Network, or without an Overlay).                                                                                                                                                                                           |
| Cloud Integration  | Build in integration using REST, Pub-Sub, and Kafka.                                                                                                                                                                                                                                                     |
| Deployment options | Executable (can be deployed as a background process), or Docker or Kubernetes.                                                                                                                                                                                                                           |


**Comments**:
* Databases: 
  - SQLite recommended for smaller nodes and in-memory data.
  - PostgreSQL recommended for larger nodes.
  - MongoDB used for blob storage.
  - Multiple databases can be deployed and used on the same node.
    
* Network:
    An Overlay network is recommended for the following reasons:
    - Isolate the network for security considerations.
    - Manage IP and Ports availability. Without an overlay network, users needs to configure and manage availability 
      of IP and Ports used.

---

## Compatibility Matrix

| Component                | Status                                                                                                                                                                                                                                                                                                                                                                             |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Python**               | 3.11 - 3.13                                                                                                                                                                                                                                                                                                                                                                        |
| **Operating System**     | No hard requirement - validated on Ubuntu 22.04, Ubuntu 24.04, Windows, and macOS.                                                                                                                                                                                                                                                                                                 |
| **Docker**               | No hard version requirement.                                                                                                                                                                                                                                                                                                                                                       |
| **Kubernetes**           | No hard version requirement.                                                                                                                                                                                                                                                                                                                                                       |
| **Database versions**    | AnyLog connects via standard pip packages rather than maintaining its own version list: `psycopg2` (PostgreSQL), the `pymongo` package (MongoDB), `boto3` (S3), and Python's built-in `sqlite3` (SQLite). Version support therefore tracks whatever each of those packages supports - not a separate AnyLog-maintained matrix. PostgreSQL 12-16 are explicitly guaranteed to work. |
| **Supported connectors** | 🟡 Not yet listed here - needs a confirmed list (see southbound/northbound connector docs).                                                                                                                                                                                                                                                                                        |

**Recommendation:** For Docker and Kubernetes deployments, use AnyLog's default docker-compose / Kubernetes deployment process rather than a custom setup - the specific Docker/Kubernetes version in use isn't a concern as long as the default deployment process is followed.