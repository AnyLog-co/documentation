---
title: Quick Deployment
description: Deploy a minimal AnyLog network (Master, Query, two Operators) using Docker Compose.
layout: page
---
<!--
## Changelog
- 2026-05-25 | Rewritten to reflect docker-compose workflow; retired bare docker run instructions
-->

Using the [deployment scripts](https://github.com/AnyLog-co/deployment-scripts), users can configure nodes with
custom port values, naming conventions, MQTT settings, and more. For cases where you just need a running network
quickly, each node type ships with a ready-made `docker-compose.yaml` that requires only minimal environment
configuration.

**Other deployments:**
- [Training](../training) — Standard training environment for learning AnyLog
- [Configuration Based](../deployments/deploying_node.md) — Deploy using a config file with environment variables
- [Empty Node](deploying_node.md) — Manually deploy and configure an AnyLog node from scratch

---

## Prerequisites

- Docker and Docker Compose installed
- AnyLog Docker Hub credentials and an active license key — [contact us](mailto:info@anylog.co) if you need access
- All nodes on the same machine, **or** the Master node's TCP connection info (`get connections`) if deploying across machines

---

## Deployment

The following steps bring up a minimal network: one Master, one Query, and two Operator nodes.
Run each step in its own terminal so you can detach and leave the container running.

> **Multi-machine note:** if any node runs on a different machine from the Master, add
> `-e LEDGER_CONN=${MASTER_NODE_TCP_CONN_INFO}` to that node's `docker-compose.yaml` (or export it into the
> environment) before running `docker compose up`.

---

### Step 1 — Log in to Docker Hub

```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```

---

### Step 2 — Start the Master node

The Master node hosts the global metadata ledger. Start it first; all other nodes register against it.

```shell
cd deployments/docker-compose/anylog-master/
docker compose up -d
```

Attach to the container to verify it is running, then detach with **ctrl-d**:

```shell
docker attach --detach-keys=ctrl-d anylog-master
```

Confirm the node is up and note the TCP connection string for use in later steps:

```anylog
get status
get connections
```

---

### Step 3 — Start the Query node

The Query node orchestrates distributed SQL across Operator nodes and exposes results to Grafana and REST clients.

```shell
cd deployments/docker-compose/anylog-query/
docker compose up -d
docker attach --detach-keys=ctrl-d anylog-query
```

---

### Step 4 — Start Operator node 1

Operator nodes host data in local databases and satisfy queries. To automatically populate the node with sample
data over MQTT, set `ENABLE_MQTT=true` in the node's `.env` file before starting.

```shell
cd deployments/docker-compose/anylog-operator/
docker compose up -d
docker attach --detach-keys=ctrl-d anylog-operator
```

---

### Step 5 — Start Operator node 2

A second Operator provides a second cluster and demonstrates distributed query behaviour.

If both Operators run on the **same machine**, make sure their TCP and REST ports don't collide — edit the
`.env` file (or the `docker-compose.yaml`) before starting:

```shell
# Example overrides for a same-machine second operator
ANYLOG_SERVER_PORT=32158
ANYLOG_REST_PORT=32159
NODE_NAME=operator2
CLUSTER_NAME=cluster2
```

Then start the node:

```shell
cd deployments/docker-compose/anylog-operator2/
docker compose up -d
docker attach --detach-keys=ctrl-d anylog-operator2
```

---

## Verifying the network

Once all four nodes are running, connect to any node and run the standard health checks:

```anylog
get processes       # confirm services are running
get connections     # confirm TCP/REST ports
test node           # local TCP + REST + blockchain check
test network        # peer connectivity across all nodes
blockchain test     # local ledger integrity
```

See [Troubleshooting](troubleshooting.md) for a full diagnostic walkthrough.

---

## Optional environment variables

The table below lists commonly used variables you can set in a node's `.env` file. A full reference is available
in [sample_config_file.env](Support/sample_config_file.env).

| Variable | Applies to | Description |
|---|---|---|
| `LICENSE_KEY` | All | Required — your AnyLog license key |
| `LEDGER_CONN` | Query, Operator | Master node TCP address (`IP:port`) when nodes are on different machines |
| `NODE_NAME` | All | Logical name registered in the metadata ledger |
| `CLUSTER_NAME` | Operator | Cluster the Operator belongs to |
| `ANYLOG_SERVER_PORT` | All | TCP port (default 32048 / 32148) |
| `ANYLOG_REST_PORT` | All | REST port (default 32049 / 32149) |
| `ENABLE_MQTT` | Operator | Set `true` to subscribe to sample MQTT data on startup |