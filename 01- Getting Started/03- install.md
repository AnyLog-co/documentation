---
title: Installing & Deploying AnyLog
description: How to install, configure, and deploy a 3-node AnyLog network using Docker.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-26 | hyperlink fix
- 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606
- 2026-07-22 | Fixed changelog rendering (was a visible table, now hidden per doc convention).
               Corrected Docker memory requirement to 300 MB, matching prerequisites.md.
               Added a Node Architecture section explaining which services start on a Standalone
               node and why, based on node type.
               Labeled the two install paths as Part 1 (quick single-instance install) and
               Part 2 (growing to a full network), per the intended structure.
               Open items, not resolved in this pass:
                 - The `make`-based persistent/volume deployment link in Quick Install step 4 is a
                   placeholder — to be filled in once the install docs are finished.
                 - Publisher node deployment intentionally omitted from this guide (adds more
                   complexity than it's worth for a basic getting-started flow).
                 - Kubernetes deployment intentionally not covered here.
- 2026-07-22 (rev 2) | Added a `host.docker.internal` note for same-machine LEDGER_CONN setup.
               Added "Verify the Standalone Instance" (Part 1) and "Verify the Network" (Part 2)
               sections with status/test node/test network curl checks, closing the previous gap
               where the guide ended without confirming the deployment actually worked.
-->

The directions below provide a zero-touch* quick deployment that does not persist the data — the goal here is just to get 
off the ground and get a feel for AnyLog, not to stand up a production-ready system.
 
This document covers deploying AnyLog from a single node all the way to a small network consisting of 1 master / metadata 
node, 2 operators, and 1 query node. We start with a single node running the three major services combined — metadata 
management (blockchain database / ledger table), data storage (sensor data coming into AnyLog), and `system_query` (the 
logical database used for aggregating results from operator(s) into a unified result for the user) — and then grow that 
out into a dedicated master, query, and 2 operators, each running on its own node.
 
For a more comprehensive deployment, please visit:
 
* [Docker](../02-%20Installation%20&%20Deployment/01-%20Deployment%20Options/01-%20Docker.md) — includes directions for a persistent, volume-based deployment
* [Virtual Machine (OVA)](../02-%20Installation%20&%20Deployment/01-%20Deployment%20Options/02-%20Installing%20the%20VM%20OVA.md)
* [Kubernetes](../02-%20Installation%20&%20Deployment/01-%20Deployment%20Options/03-%20Kubernetes.md)

<sub>*A zero-touch deployment is a simple deployment where everything is automatically defined by the blockchain / 
default values. In general, this means not providing any env variables. However, since this is a single codebase 
that's able to deploy different services, the user must include the type of AnyLog agent (`NODE_TYPE`), the connection 
information to join the network — IP:Port for the Master / metadata node (`LEDGER_CONN`) — and the activation key for 
AnyLog (`LICENSE_KEY`).</sub>
 
## Prerequisites

### Machine requirements

| Component | Requirement |
|---|---|
| **Operating System** | Linux (Debian/Ubuntu, RedHat, Alpine, CentOS, Suse) · macOS · Windows |
| **Memory** | 100 MB (without Docker) · 300 MB (with Docker) |
| **CPU** | Intel, ARM, AMD x64. x86 available on request. |
| **Networking** | TCP-based network (local, internet, or hybrid) |

Recommended minimum for a dev/demo machine: **2 GB RAM, 50 GB disk**. A cloud VM (AWS, DigitalOcean, Linode) works well.

### Open ports

The default ports for a single-machine 3-node deployment:

| Node | TCP | REST | Broker |
|---|---|---|---|
| Master | 32048 | 32049 | — |
| Operator | 32148 | 32149 | 32150 |
| Query | 32348 | 32349 | — |

If nodes are on separate machines, confirm these ports are accessible between them before deploying.


## Part 1 — Quick Install 

The following provides a quick installation of a single AnyLog (docker) instance. 

1. Make sure you have [Docker](https://docs.docker.com/engine/install/ubuntu/) and _make_ installed.
2. <a href="https://www.anylog.network/download" target="_blank">Request License and Access key</a>
3. Login to Docker

```shell
docker login -u anyloguser
```

4. Start AnyLog Standalone - an instance of AnyLog that contains Master, Operator and Query as a single agent 

```shell
docker run -it --network host \
  -e NODE_TYPE=master-operator \
  -e LICENSE_KEY={LICENSE_KEY} \
--name anylog-standalone --rm anylogco/anylog-network:2.0.2606 
```
Please use `make` functionality (in [Install](03-%20install.md)) to deploy a persistent / volume-based AnyLog agent.

5. At this point a single instance of AnyLog is installed on your system 

### Verify the Standalone Instance

Confirm the node is up and responding:

```shell
curl -X GET http://127.0.0.1:32149
```

A response confirms the container is running and the REST service is reachable.

### Node Architecture

When a node starts, which services come up depends on the node type and how it's configured. For the Standalone
instance above (Master + Operator + Query combined), starting the node brings up:

* **Communication services** — TCP and REST are always started. The Message Broker only starts on Operator and
  Publisher node types.
* **Logical databases** — which ones a node needs depends on its role:
  * A **Master / Metadata** node requires the `blockchain` ledger database.
  * An **Operator** node requires a logical database to store the actual data, plus an `almgm` database — the
    archive hash info database — that stores a hash of each incoming file to prevent duplicate data and support
    validation for HA. Local data hashes are stored in `almgm.tsd_info`; hashes for data replicated in from other
    operators are stored per-source in `almgm.tsd_[operator ID]`.
  * A **Query** node requires the `system_query` database.
* **`run blockchain sync`** — a background service that keeps the node's local copy of the blockchain/metadata in
  sync with the rest of the network.
* **Persistence scheduler** *(Operator-specific)* — manages persistence of partitioned data and the original raw
  JSON files as they arrive.
* **Monitoring scheduler** *(Operator-specific, enabled by default)* — provides ongoing health/status insight for
  the node.

All of this — and more (e.g. southbound connector services) — can be configured in more detail using a configuration
file rather than passing everything through `docker run` environment variables directly.

## Part 2 — From Single Agent to Full Network

The following provides directions on how to deploy a full network  -- 1 master, 2 operator, 1 query. 
Feel free to skip steps 1&2 if you already have a license. Additionally feel free to skip adding a master node if you'd
like to extend the network with the existing standalone instance from the pervious set of directions. 

1. Make sure you have [Docker](https://docs.docker.com/engine/install/ubuntu/) and _make_ installed.
2. <a href="https://www.anylog.network/download" target="_blank">Request License and Access key</a>
3. Login to Docker -- this is required on each machine 

```shell
docker login -u anyloguser
```

4. Start Master / Metadata node 

```shell
docker run -it --network host \
  -e NODE_TYPE=master \
  -e LICENSE_KEY={LICENSE_KEY} \
--name anylog-master --rm anylogco/anylog-network:2.0.2606 
```

5. Using the command `get connections` (via REST) the value that'll be used as LEDGER_CONN 

```shell
curl -X GET http://127.0.0.1:32049 \
  -H "command: get connections" \
  -H "User-Agent:AnyLog/1.23"
```

If you are using a standalone node from step 1 the URL is `http://127.0.0.1:32149`.

> **Same machine?** If all nodes are running on the same machine, you can use `host.docker.internal` in place of the
> Master's IP for `LEDGER_CONN` — e.g. `LEDGER_CONN=host.docker.internal:32048` — instead of looking up the actual
> host IP.

6.  Start Operator

```shell
docker run -it --network host \
  -e NODE_TYPE=operator \
  -e LICENSE_KEY={LICENSE_KEY} \
  -e LEDGER_CONN=[IP:TCP_PORT for Master] \
--name anylog-operator1 --rm anylogco/anylog-network:2.0.2606 
```

7. Wait for Operator1 to come up and start Operator 2

```shell
docker run -it --network host \
  -e NODE_TYPE=operator \
  -e LICENSE_KEY={LICENSE_KEY} \
  -e LEDGER_CONN=[IP:TCP_PORT for Master] \
--name anylog-operator2 --rm anylogco/anylog-network:2.0.2606 
```

if the second operator resides on the same machine is operator 1 / standalone node then make sure to update the env varibale 
`ANYLOG_SERVER_PORT`, `ANYLOG_REST_PORT` and `ANYLOG_BROKER_PORT` 

8. Start Query node 

```shell
docker run -it --network host \
  -e NODE_TYPE=query \
  -e LICENSE_KEY={LICENSE_KEY} \
  -e LEDGER_CONN=[IP:TCP_PORT for Master] \
--name anylog-query --rm anylogco/anylog-network:2.0.2606 
```

### Verify the Network

Once all four nodes are running, confirm each is up and that the network has formed correctly. Run these against any
node's REST port (see the [Open ports](#open-ports) table) — for example `http://127.0.0.1:32349` for the Query node.

**Check status** — confirms the node is up and its REST service is reachable:
```shell
curl -X GET http://[ip]:[port]
```

**Check node** — confirms the node itself is correctly configured:
```shell
curl -X GET http://[ip]:[port] -H "command: test node" -H "User-Agent: AnyLog/1.23"
```

**Check network** — confirms the node can see its peers (Master, Operators, Query):
```shell
curl -X GET http://[ip]:[port] -H "command: test network" -H "User-Agent: AnyLog/1.23"
```

If `test network` doesn't show all expected peers, double-check `LEDGER_CONN` was set correctly on each node and that
the required ports (see [Open ports](#open-ports)) are reachable between them.