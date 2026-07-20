---
title: Installing AnyLog via OVA
description: Deploy a pre-configured AnyLog demo environment using the OVA virtual machine image.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

The AnyLog Demo OVA is a pre-configured virtual machine image containing a complete, multi-node AnyLog environment. It is designed for demonstrations, training, evaluations, and proof-of-concept deployments — everything runs inside a single VM.

---

## What's included

| Component | Description | Default port |
|---|---|---|
| **Standalone Node** | Combined master + operator — control plane, query federation, and data storage | `VM_IP:32149` |
| **Operator Node** | Second data ingestion and storage node | `VM_IP:32159` |
| **GUI** | Web-based management UI — query builder, node health, metadata viewer | `http://localhost:31800` |
| **Grafana** | Pre-configured monitoring dashboard | `http://localhost:3000` |

All components start automatically when the VM boots.

---

## Prerequisites

- Hypervisor: VMware Workstation, VMware ESXi, or VirtualBox
- Minimum 4 GB RAM, 2 vCPUs, 20 GB disk recommended
- AnyLog license key — get one at <a href="https://www.anylog.network/download" target="_blank">https://www.anylog.network/download</a>

---

## Installation

### 1. Import the OVA

Import the `.ova` file into your hypervisor. In VMware: **File → Open** and select the file. In VirtualBox: **File → Import Appliance**.

Boot the VM and log in. The AnyLog scripts are located at `~/AnyLog/`.

### 2. Make scripts executable

```bash
chmod +x ~/AnyLog/ALinstall.sh
chmod +x ~/AnyLog/startup.sh
```

### 3. Configure the environment (optional)

Edit `~/AnyLog/ALinstall.env` before installing. At minimum, set your license key:

```bash
nano ~/AnyLog/ALinstall.env
```

Key variables:

| Variable | Default | Description |
|---|---|---|
| `LICENSE_KEY` | *(blank)* | **Required.** Prompted interactively if left blank. |
| `COMPANY_NAME` | `Anylog-Demo` | Name stamped on node policies in the metadata layer. |
| `TAG` | `pre-develop` | AnyLog Docker image tag / version to deploy. |
| `LEDGER_CONN` | `127.0.0.1:32148` | TCP address of the master node (blockchain ledger). |
| `ENABLE_MQTT` | `true` | Enable MQTT data ingestion. |
| `MQTT_BROKER` | `172.104.228.251` | External MQTT broker address for the demo data feed. |
| `MSG_DBMS` | `new_company` | Database name for MQTT-ingested data. |
| `DEFAULT_DBMS` | `new_company` | Default database name. |
| `NODE_MONITORING` | `true` | Enable node health monitoring. |
| `STORE_MONITORING` | `true` | Persist monitoring metrics to a local database. |
| `SYSLOG_MONITORING` | `true` | Collect syslog messages from the host. |
| `DOCKER_MONITORING` | `true` | Collect Docker container stats. |

### 4. Install the demo environment

```bash
cd ~/AnyLog
./ALinstall.sh -d -s install
```

The `-d` flag enables demo mode (installs the full pre-configured environment). The `-s` flag starts all nodes immediately after installation.

Logs are written to `./logs/ALinstall_install_<timestamp>.log`.

### 5. Verify

```bash
docker ps
```

All containers should be running. Then open the GUI:

```
http://localhost:31800
```

Default credentials:
```
Username: edgelake
Password: edgelake
```

> **Change these immediately for any non-demo or networked deployment.**

---

## ALinstall.sh reference

```bash
./ALinstall.sh [-e env_file] [-n node1,node2,...] [-s] [-k] [-d] <command>
```

### Commands

| Command | Description |
|---|---|
| `install` | Clone docker-compose repo, configure, and optionally start nodes |
| `uninstall` | Stop and remove containers and images |
| `update` | Uninstall then reinstall with current config |
| `start` | Start previously installed nodes |
| `stop` | Stop running nodes |

### Flags

| Flag | Description |
|---|---|
| `-d` | Demo mode — installs the full demo environment (overrides `-n`) |
| `-s` | Auto-start nodes after `install` or `update` |
| `-k` | Auto-stop running nodes before `uninstall` or `update` |
| `-n node1,node2` | Target specific node types only |
| `-e path` | Path to a custom environment file (default: `./ALinstall.env`) |

### Node types

| Node type | Description |
|---|---|
| `anylog-standalone-operator` | Combined master + operator (used in demo mode) |
| `anylog-master` | Metadata ledger node only |
| `anylog-operator` | Data ingestion and storage node |
| `anylog-query` | Federated SQL query node |
| `anylog-publisher` | Data routing node |
| `anylog-generic` | Generic node — any combination of services |

### Common examples

```bash
# Full demo install, auto-start
./ALinstall.sh -d -s install

# Install specific node types only
./ALinstall.sh -n anylog-master,anylog-query install

# Install with a custom config file, auto-start
./ALinstall.sh -e /opt/myconfig.env -s install

# Stop demo nodes
./ALinstall.sh -d stop

# Restart demo nodes
./ALinstall.sh -d -s start

# Uninstall a single node
./ALinstall.sh -n anylog-operator uninstall

# Update all nodes (stop existing, reinstall, restart)
./ALinstall.sh -k -s update
```

---

## Default dataset

The demo environment ships with a pre-loaded dataset:

- **Database:** `new_company`
- **Table:** `rand_data`

Data is continuously ingested via an MQTT feed on first launch. You can query it immediately from the GUI or via REST:

```bash
curl -X GET http://localhost:32149 \
  -H "command: sql new_company format=table \"select * from rand_data limit 10\"" \
  -H "User-Agent: AnyLog/1.23"
```

---

## Troubleshooting

**Containers not running:**
```bash
docker ps -a          # check all containers including stopped ones
docker logs <name>    # view logs for a specific container
```

**Restart the demo:**
```bash
./ALinstall.sh -d -s start
```

**Reinstall from scratch:**
```bash
./ALinstall.sh -d uninstall
./ALinstall.sh -d -s install
```

**Upgrade to a newer version:**
```bash
# Edit ALinstall.env and update TAG to the desired version, then:
./ALinstall.sh -d -k -s update
```

**Logs:**
```bash
ls ~/AnyLog/logs/           # list install logs
cat ~/AnyLog/logs/ALinstall_install_*.log
```

---

## Next steps

Once the demo environment is running, explore it via the GUI at `http://localhost:31800`, or connect to the standalone node directly:

- **REST endpoint:** `http://VM_IP:32149`
- **Query node endpoint:** `http://VM_IP:32349`

To move beyond the demo and deploy a production-grade environment, see:
- <a href="{{ '/docs/Getting-Started/installing-anylog/' | relative_url }}">Installing AnyLog via Docker</a>
- <a href="{{ '/docs/Getting-Started/anylog-as-service/' | relative_url }}">Installing AnyLog as a Service</a>
- <a href="{{ '/docs/Getting-Started/deployment-scripts/' | relative_url }}">Deployment Scripts</a>