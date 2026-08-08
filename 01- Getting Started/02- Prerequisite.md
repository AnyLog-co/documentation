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

<table>
  <caption>AnyLog Deployment Requirements</caption>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="feature-cell" rowspan="2">Operating System</td>
      <td>Linux (Ubuntu, RedHat, Alpine, Suse)</td>
    </tr>
    <tr>
      <td>Windows</td>
    </tr>
    <tr>
      <td class="feature-cell">Python</td>
      <td>3.11 &ndash; 3.13</td>
    </tr>
    <tr>
      <td class="feature-cell" rowspan="2">Memory footprint</td>
      <td>100 MB available for AnyLog deployed without Docker</td>
    </tr>
    <tr>
      <td>300 MB available for AnyLog deployed with Docker</td>
    </tr>
    <tr>
      <td class="feature-cell" rowspan="3">Databases</td>
      <td>PostgreSQL installed (optional)</td>
    </tr>
    <tr>
      <td>SQLite (default, no need to install)</td>
    </tr>
    <tr>
      <td>MongoDB installed (only if blob storage is needed)</td>
    </tr>
    <tr>
      <td class="feature-cell" rowspan="2">CPU</td>
      <td>Intel, ARM, and AMD are supported.</td>
    </tr>
    <tr>
      <td>AnyLog can be deployed on a single CPU machine and up to the largest servers (gateways, Raspberry Pi, and all the way to the largest multi-core machines).</td>
    </tr>
    <tr>
      <td class="feature-cell">Storage</td>
      <td>AnyLog supports horizontal scaling &mdash; nodes (and storage) are added dynamically as needed, reducing scaling complexity. Requirements are based on expected data volume and retention duration on each node. AnyLog supports automated archival and transfer to larger nodes (if needed).</td>
    </tr>
    <tr>
      <td class="feature-cell" rowspan="3">Network</td>
      <td>Required: a TCP-based network (local TCP-based networks, over the internet, and combinations are supported)</td>
    </tr>
    <tr>
      <td>An overlay network is recommended. Most overlay networks can be used transparently. Nebula is used as the default overlay network.</td>
    </tr>
    <tr>
      <td>Static IP and 3 ports open and accessible on each node (either via an Overlay Network or without one).</td>
    </tr>
    <tr>
      <td class="feature-cell">Cloud Integration</td>
      <td>Built-in integration using REST, Pub-Sub, and Kafka.</td>
    </tr>
    <tr>
      <td class="feature-cell">Deployment options</td>
      <td>Executable (can be deployed as a background process), Docker, or Kubernetes.</td>
    </tr>
  </tbody>
</table>

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