---
title: Deployment Scripts
description: How AnyLog's deployment-scripts repository configures, launches, and customises each node type at startup.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | updated hyperlinks
- 2026-04-25 | updated [page.html](../../_layouts/page.html) to support pop-up for env configs 
--> 

> This page extends the different installation processes by explaining what happens *inside* the container after 
> `make up` — how configuration flows from your `.env` file into a running, networked AnyLog node.

---

## The two-part Docker image

An AnyLog Docker container is made of two independent pieces:

```
┌─────────────────────────────────┐
│  AnyLog binary (compiled image) │  ← the engine — never edited
├─────────────────────────────────┤
│  deployment-scripts (git clone) │  ← your scripts — fork and customise
└─────────────────────────────────┘
```

The **binary** is the compiled AnyLog runtime. It knows how to execute `.al` scripts but does nothing on its own.

The <a href="https://github.com/AnyLog-co/deployment-scripts/" target="_blank">**deployment-scripts**</a> repo tells the 
binary what to do: which services to start, which databases to connect, which policies to publish. It's designed to be 
forked — you own the logic.

```ini
DEPLOYMENTS_REPO="https://github.com/AnyLog-co/deployment-scripts"
DEPLOYMENTS_BRANCH="pre-develop"
```

**Option 1 — Git clone (default):** Docker pulls the repo at container start. Change `DEPLOYMENTS_REPO` and 
`DEPLOYMENTS_BRANCH` to point to your own fork.

**Option 2 — Local path (recommended for development):** If `DEPLOYMENTS_REPO` is set to an absolute path on your 
machine (e.g. `/home/user/deployment-scripts`), the docker-compose logic detects that it's a local directory and 
mounts it as a volume instead of cloning. Changes you make on your host are reflected inside the container immediately 
— no rebuild or re-pull needed.

```ini
# Use a local checkout instead of cloning from GitHub
DEPLOYMENTS_REPO="/home/user/my-deployment-scripts"
DEPLOYMENTS_BRANCH=""            # not used for local paths
```

This is the recommended workflow when you're actively editing scripts — edit on your host, restart the container 
(`make down && make up`), changes are live.

---

## Repository structure

```
deployment-scripts/
├── node-deployment/               ← core startup scripts (main entry point)
│   ├── main.al                    ← called first when the container starts
│   ├── set_params.al              ← converts env vars to AnyLog variables
│   ├── database/                  ← database connectivity scripts
│   └── policies/
│       ├── config_policy.al       ← builds and publishes the config policy
│       ├── cluster_policy.al      ← cluster definition (operator nodes)
│       └── node_policy.al         ← node registration on the blockchain
│
├── data-generator/                ← sample scripts to receive data via MQTT/REST
│   └── mapping/                   ← mapping policies for msg client
│
├── sample-scripts/                ← ready-to-run connector examples
│   ├── basic_msg_client.al        ← MQTT ingestion (used when ENABLE_MQTT=true)
│   ├── telegraf.al                ← Telegraf metrics
│   └── aggregation.al             ← aggregation service
│
├── southbound-industrial/         ← OPC-UA and industrial connectors
├── southbound-monitoring/         ← node, Docker, and syslog monitoring
└── southbound-video-streaming/    ← live video ingestion and AI inference
```

---

## Startup flow

When you run `make up ANYLOG_TYPE=anylog-operator`, Docker starts the container and immediately calls:

```
process /app/deployment-scripts/node-deployment/main.al
```

<a href="https://github.com/AnyLog-co/deployment-scripts/blob/main/node-deployment/main.al" target="_blank">`main.al`</a> 
orchestrates the entire startup in fixed stages:

```
docker run
  │
  ├─ 1. authentication mode configuration
  ├─ 2. Detect AnyLog vs EdgeLake
  ├─ 3. Set directory paths  (!anylog_path, !local_scripts)
  ├─ 4. Create work directories
  ├─ 5. process set_params.al          ← env vars → AnyLog variables
  └─ 6. process config_policy.al       ← everything else (see below)
         │
         ├─ connect databases
         ├─ blockchain seed / connect
         ├─ publish cluster policy (operators)
         ├─ publish node policy
         ├─ run scheduler
         ├─ set buffer thresholds + run streamer
         ├─ run operator / run data distributor / run data consumer (if HA)
         ├─ run mcp server (if enabled)
         ├─ process aggregation.al (if ENABLE_AGGREGATIONS=true)
         ├─ process basic_msg_client.al (if ENABLE_MQTT=true)
         ├─ process video_ai.al (if ENABLE_VIDEO_STREAMING=true)
         ├─ process deploy_monitoring.al
         └─ process local_script.al (if DEPLOY_LOCAL_SCRIPT=true)
```

After startup, `main.al` runs `get processes` and (if MQTT is on) `get msg client` so the output is visible in `make logs`.

---

## node_configs.env — section by section
All node configuration lives in a single [`node_configs.env`](#){: onclick="openEnvModal(); return false;"} file. New users only 
need to edit **basic** and **secrets**. Every other section is optional and safe to leave at its defaults.


### `.env` — Docker deployment settings

```ini
INIT_TYPE=prod                   # prod = run node; bash = shell only
IMAGE=anylogco/anylog-network
DEPLOYMENTS_REPO="https://github.com/AnyLog-co/deployment-scripts"
DEPLOYMENTS_BRANCH="pre-develop"
```

### `basic` — required for all deployments

```ini
#--- General ---
NODE_TYPE=master-operator        # master | operator | query | publisher
                                 # master-operator | master-publisher
NODE_NAME=anylog-node
COMPANY_NAME=AnyLog Co.

#--- Networking ---
ANYLOG_SERVER_PORT=32148         # TCP port (peer communication)
ANYLOG_REST_PORT=32149           # REST port (external apps, curl)
ANYLOG_BROKER_PORT=32150         # MQTT broker port

#--- Database ---
DB_TYPE=sqlite                   # sqlite | psql
DB_IP=127.0.0.1
DB_PORT=5432

#--- Blockchain ---
LEDGER_CONN=127.0.0.1:32148     # Master node IP:port — set on ALL nodes
BLOCKCHAIN_SOURCE=master         # master | optimism
BLOCKCHAIN_SYNC=60 second

#--- Operator ---
CLUSTER_NAME=anylog-cluster1
DEFAULT_DBMS=mydb
```

> **The one setting that breaks everything if wrong:** `LEDGER_CONN` must point to the master node's TCP IP and port on
> every operator and query node. Wrong value = nodes can't find each other.

### `southbound` — data ingestion (all off by default)

| Variable | Default | Description |
|---|---|---|
| `ENABLE_MQTT` | `false` | Start the basic msg client on boot |
| `MQTT_BROKER` | `172.104.228.251` | AnyLog's live demo broker |
| `MQTT_PORT` | `1883` | |
| `MSG_TOPIC` | `anylog-demo` | Topic to subscribe to |
| `MSG_DBMS` | `mydb` | Target database |
| `ENABLE_OPCUA` | `false` | Start OPC-UA client on boot |
| `ENABLE_VIDEO_STREAMING` | `false` | Start video ingestion on boot |
| `NODE_MONITORING` | `false` | Monitor this node's resources |
| `SYSLOG_MONITORING` | `false` | Accept syslog over TCP |
| `DOCKER_MONITORING` | `false` | Monitor container stats |

### `advanced` — fine-tuning (safe to leave as defaults)

Notable settings:

```ini
DEPLOY_LOCAL_SCRIPT=false        # run your own local_script.al at end of startup
TCP_BIND=true                    # bind TCP to specific IP (set false if behind NAT)
REST_BIND=false
ENABLE_HA=false                  # high availability — requires cluster peers
WRITE_IMMEDIATE=true             # write to DB immediately vs buffering
THRESHOLD_TIME=60 seconds        # buffer flush time
THRESHOLD_VOLUME=10KB            # buffer flush volume
QUERY_POOL=6                     # parallel query threads
```

### `secrets` — credentials (never commit to version control)

```ini
LICENSE_KEY=""
DB_USER=admin
DB_PASSWD=passwd
MQTT_USER=anyloguser
MQTT_PASSWD=mqtt4AnyLog!
BLOB_STORAGE_USER=admin
BLOB_STORAGE_PASSWORD=passwd
```

### `remote-gui` — companion UI

```ini
ENABLE_REMOTE_GUI=true
REMOTE_GUI_FE=31800              # frontend port → http://[node-ip]:31800
REMOTE_GUI_BE=8080               # backend API port
REMOTE_GUI_TAG=beta2
```

---

## The config policy

The config policy is a JSON document published to the blockchain that permanently records how this node is configured. 
Other nodes in the network read it to know how to communicate with this node.

It is built automatically from your env vars during startup by `config_policy.al`. A simplified example:

```json
{"config": {
  "name":            "operator-smart-city",
  "company":         "Smart City",
  "node_type":       "operator",
  "ip":              "!ip",
  "port":            "!anylog_server_port",
  "rest_port":       "!anylog_rest_port",
  "broker_port":     "!anylog_broker_port",
  "script": [
    "process !local_scripts/database/deploy_database.al",
    "process !local_scripts/connect_blockchain.al",
    "process !local_scripts/policies/cluster_policy.al",
    "process !local_scripts/policies/node_policy.al",
    "run scheduler 1",
    "set buffer threshold where time=!threshold_time and volume=!threshold_volume",
    "run streamer",
    "if !enable_ha == true then run data distributor",
    "if !enable_ha == true then run data consumer where start_date=!start_date",
    "if !enable_mqtt == true then process !local_scripts/sample-scripts/basic_msg_client.al",
    "if !enable_video_streaming == true then process .../video_ai.al",
    "process .../southbound-monitoring/deploy_monitoring.al",
    "if !deploy_local_script == true then process !local_scripts/local_script.al"
  ]
}}
```

The `script` array is the actual startup sequence — each string is an AnyLog command executed in order. This means 
**you can change what runs at startup by editing this policy**, without touching `main.al`.

To view the config policy for a running node:
```anylog
blockchain get config where name = [node name]
```

---

## Running your own startup logic

The cleanest way to add custom behaviour without modifying the core scripts:

1. Set `DEPLOY_LOCAL_SCRIPT=true` in `node_configs.env`
2. Create `local_script.al` in your deployment-scripts fork
3. Write any AnyLog commands you want — additional msg clients, custom schedulers, extra databases

This script runs last, after all standard services are up.

---

## Node types

| `NODE_TYPE` | Role |
|---|---|
| `master` | Blockchain emulator — stores metadata for the network |
| `operator` | Stores data; the database node |
| `query` | Dedicated query routing node |
| `publisher` | Distributes data to multiple operators (AnyLog only) |
| `master-operator` | Combined master + operator on a single node (good for standalone / dev) |
| `master-publisher` | Combined master + publisher |
| `generic` | Network only — useful for sandbox/testing |

> `publisher` is not available in EdgeLake deployments.