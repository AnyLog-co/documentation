---
title: Installing & Deploying AnyLog
description: How to install, configure, and deploy a 3-node AnyLog network using Docker.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-26 | hyperlink fix
--> 

> This guide covers a standard 3-node deployment (master, operator, query) on a single machine. For a conceptual 
> overview of node types, see <a href="{{ '/docs/Getting-Started/getting-started/' | relative_url }}">Introduction to AnyLog</a>.

## Prerequisites

### Machine requirements

| Component | Requirement |
|---|---|
| **Operating System** | Linux (Debian/Ubuntu, RedHat, Alpine, CentOS, Suse) · macOS · Windows |
| **Memory** | 100 MB (without Docker) · 500 MB (with Docker) |
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

### AnyLog Docker access key

<a href="https://anylog.network/download" target="_blank">Request a license and Docker access key</a>. 
You'll need this to pull the AnyLog image. Keep the key handy — one wrong character will cause login to fail.

> **Watch out for `l` vs `1`:** Characters in the key that look like the number `1` may actually be lowercase `l` — 
> and vice versa. If Docker login fails, check every character carefully.

---

## Step 1 — Install Docker, Git, and Make

The following installs Docker on Ubuntu. For other distributions see the [Docker installation docs](https://docs.docker.com/engine/install/).

```bash
# Update packages and install prerequisites
sudo apt update
sudo apt install -y ca-certificates curl make

# Add Docker's GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# Install Docker and Make
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin make
```

Verify: `docker --version` should return `Docker version 29.x.x` or later.

---

## Step 2 — Clone the docker-compose repository

```bash
cd ~/
git clone -b pre-develop https://github.com/AnyLog-co/docker-compose
```

> **Important:** Always use `-b pre-develop`. Cloning without this flag checks out the wrong branch and is not shown in some older documentation.

The repository structure:

```
docker-compose/
└── docker-makefiles/
    ├── anylog-master/
    │   └── node_configs.env
    ├── anylog-operator/
    │   └── node_configs.env
    └── anylog-query/
        └── node_configs.env
```

Each node type has its own [`node_configs.env`](#){: onclick="openEnvModal(); return false;"}. You can duplicate any 
of these directories to maintain multiple configuration sets for the same node type.

---

## Step 3 — Docker login

```bash
# Log out first to clear any stale credentials
docker logout

# Log in with your AnyLog key
docker login docker.io -u anyloguser -p [YOUR-KEY]
```

**Expected output on success**:
```
WARNING! Your credentials are stored unencrypted in '/root/.docker/config.json'
Login Succeeded
```

> **Note:** If you're using the `make login` command, be aware it has a known bug where `ANYLOG_TYPE` may be treated as the password. Log in directly with `docker login` as shown above.

---

## Step 4 — Configure each node

All configuration lives in `docker-makefiles/anylog-[node-type]/node_configs.env`, organized into sections:

```
node_configs.env
├── .env        — Docker deployment settings
├── basic       — Core node config (required)
├── southbound  — Data ingestion protocols (optional)
├── advanced    — Fine-tuning for experienced users (optional)
├── secrets     — Credentials
└── remote-gui  — Companion UI settings
```

New users only need to edit **basic** and **secrets**. The other sections are safe to leave at their defaults.

### Key settings to validate per node

```ini
#==== basic ====

#--- General ---
NODE_NAME=anylog-node
COMPANY_NAME=AnyLog Co.

#--- Networking ---
ANYLOG_SERVER_PORT=32548    # TCP port — must be unique per node
ANYLOG_REST_PORT=32549      # REST port — must be unique per node
ANYLOG_BROKER_PORT=32550    # MQTT broker port (operator only)

#--- Blockchain ---
LEDGER_CONN=127.0.0.1:32048  # Master node IP:port — set this on ALL nodes
```

### Per-node checklist before deploying

- **All nodes:** TCP and REST ports are unique per node; `LEDGER_CONN` points to the master node's IP and TCP port
- **Operator node:** `DEFAULT_DBMS` (logical database name) and `DB_TYPE` (physical database type) are set. If using PostgreSQL, also validate `DB_USER`, `DB_PASSWD`, and the DB host/port
- **Operator node (optional):** If receiving data via MQTT, enable the MQTT service and confirm `MSG_DBMS` matches `DEFAULT_DBMS`

---

## Step 5 — Deploy the nodes

Run from the `~/docker-compose` directory. On a single machine, bring nodes up in order:

```bash
# 1. Master node first
make up ANYLOG_TYPE=anylog-master

# 2. Operator node
make up ANYLOG_TYPE=anylog-operator

# 3. Query node
make up ANYLOG_TYPE=anylog-query
```

Docker pulls the AnyLog image on first run — this takes about 30 seconds. On a single machine, a short delay between 
nodes is built into the configuration to let each one initialize before the next starts.

---

## Step 6 — Validate the network

Attach to the query node:

```bash
make attach ANYLOG_TYPE=anylog-query
```

Run the following at the `AL anylog-query >` prompt:

```
# Validate TCP and REST on this node — both should show "pass"
AL > test node

# Validate all 3 nodes are reachable — each must show "+" in the Status column
AL > test network

# Confirm key services are running
AL > get processes
```

Press `ctrl+d` to detach from the CLI without stopping the node.

---

## make command reference

All `make` commands take the form: `make [cmd] ANYLOG_TYPE=anylog-[master|operator|query]`

| Command | Description |
|---|---|
| `make up` | Start the node |
| `make down` | Stop the node |
| `make attach` | Open the AnyLog CLI |
| `make logs` | View container logs |
| `make logs-f` | Follow (tail) container logs |
| `make exec` | Open the container shell |
| `make clean` | Remove node data (keeps image) |
| `make clean-all` | Remove data and image |

---

## Communicating with AnyLog

There are two ways to interact with a running node:

### 1. CLI (attached directly)

```bash
make attach ANYLOG_TYPE=[config-dir-name]
```

Then type commands at the `AL >` prompt.

### 2. REST API

```bash
curl -X [GET|PUT|POST] [REST_IP]:[REST_PORT] \
  -H "command: [AnyLog command]" \
  -H "User-Agent: AnyLog/1.23" \
  [-H "destination: [remote node TCP IP:port]"]
```

To target a specific remote node, use `-H "destination: [IP:port]"`. To route a query across the entire network 
(letting AnyLog locate the data via metadata), use `-H "destination: network"`.


Visit [using REST documentation](/docs/Network-Services/using-rest.md) for farther details on communicating with the nodes
(and network) via REST.

---

## Basic commands

| Command | Description |
|---|---|
| `help [cmd]` | Help for any command |
| `get processes` | List services and whether each is active |
| `get event log` | Commands executed on this node |
| `get error log` | Errors that have occurred |
| `get databases` | Databases connected on this node |
| `test node` | Validates network connectivity for this node |
| `test network` | Validates communication with other nodes |

---

## Blockchain commands

The blockchain stores network metadata. Use `blockchain get` to inspect policies and node configurations.

```
blockchain get [policy type] [bring condition] [where condition]
```

### Examples

```bash
# Show all policies
blockchain get *

# Show master, operator, and query nodes in a table
blockchain get (master, operator, query) bring.table [*][*][name] [*][ip] [*][port] [*][rest_port]
```

Example output:
```
Policy   Name             Ip             Port   Rest_port
---------|----------------|---------------|-------|---------|
master   |anylog-master   |192.168.65.3   |32048  | 32049   |
operator |anylog-operator |192.168.65.3   |32148  | 32149   |
query    |anylog-query    |192.168.65.3   |32348  | 32349   |
```

```bash
# List tables in the mydb logical database
blockchain get table where dbms=mydb bring [*][name] separator=\n
```

---

## Querying data across the network

### `run client` — remote command execution

```
run client (destination) [command]
```

`destination` can be a direct `IP:port`, or empty `()` to let the network route the request via metadata. For REST 
calls, use the `-H "destination: XXX"` header; use `destination: network` to let AnyLog route automatically.

### Distributed SQL queries

```
run client () sql [db name] "SELECT ..."
```

The query node uses blockchain metadata to identify which operator nodes hold the data, distributes the query, 
collects partial results (operators compute `sum`/`count` for aggregates), and assembles the final result.

```bash
# REST equivalent — query across the network
curl -X GET 127.0.0.1:32349 \
  -H "command: sql mydb format=table SELECT timestamp, value FROM rand_data WHERE period(minute, 1, now(), timestamp)" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"
```

> **SQL tip:** When using time comparisons, always use `>=`. For example: `WHERE insert_timestamp >= NOW() - 10 minutes`. Omitting `>=` will cause a parse error.

---

## Full data cycle — quick test

Push data in via REST PUT (run from a separate terminal, not the AnyLog CLI):

```bash
curl -X PUT "http://127.0.0.1:32149" \
  -H "type: json" \
  -H "dbms: mydb" \
  -H "table: rand_data" \
  -H "mode: streaming" \
  -H "Content-Type: text/plain" \
  --data '[{"timestamp":"2026-03-16T10:00:00Z","value":12.5}]'
```

Expected response: `{"AnyLog.status":"Success", "AnyLog.hash": "0"}`

Query it back:

```bash
curl -X GET 127.0.0.1:32349 \
  -H "command: sql mydb format=table SELECT * FROM rand_data LIMIT 10;" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"
```

---

---

## Node directory structure

The default directory layout (used in Docker deployments):

```
/app/
└── EdgeLake/
    ├── blockchain/          ← local copy of the metadata (JSON)
    └── data/
        ├── archive/         ← archived data files
        ├── blobs/           ← unstructured data
        ├── dbms/            ← persistent SQLite data (if used)
        ├── distr/           ← HA distribution staging
        ├── error/           ← files that failed database storage
        ├── pem/             ← SSL keys and certificates
        ├── prep/            ← intermediate processing
        ├── test/            ← output of test queries
        ├── watch/           ← drop JSON/SQL files here for auto-ingestion
        └── bwatch/          ← unstructured data watch directory
```

Create the work directories on first run:
```anylog
create work directories
```

List the directories configured on this node:
```anylog
get dictionary _dir
```

---

## The AnyLog CLI

When a node starts, it presents the AnyLog CLI with a prompt like `AL anylog-node >`. Update the prompt:
```anylog
set node name [node name]
```

Exit and shut down the node:
```anylog
exit node
```

### The local dictionary

Every node has a dictionary that maps keys to values. Use `!key` to reference a stored value:

```anylog
# Set a value
master_node = 10.0.0.1:32048

# Or use 'set' if the key name conflicts with a command
set dbms_name = mydb

# Read a value
!master_node
get !dbms_name

# List all key-value pairs
get dictionary
```

Environment variables are available with the `$` prefix: `$HOME`, `$PATH`.

### The help command

```anylog
help                          # list all commands
help get                      # list all 'get' commands
help blockchain insert        # usage and examples for a specific command
help index                    # browse commands by category
help index s                  # all commands in category 's'
```

### Logs

Every node maintains three dynamic logs:

```anylog
get event log      # commands executed on this node
get error log      # commands that failed
get query log      # SQL queries executed (must be enabled separately)

reset event log
reset error log
reset query log
```

---

## Troubleshooting

### Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| `Docker login: unauthorized` | Character confusion in key | Check `l` vs `1` in your key. Use `docker login docker.io -u anyloguser -p [KEY]` |
| `make login` fails | Known bug | Skip it — use `docker login` directly |
| `test network` shows blank Status | Nodes not communicating | Check `LEDGER_CONN` in all 3 `node_configs.env` files points to master IP:port |
| `curl` returns chunked-encoding error | Missing newline / line breaks in command | Add `-w "\n"` and ensure the entire command is on one line |
| Node shows error on screen | Various | Run `get error log` for the full message |

### Node communication failures

The most common failure is nodes unable to reach each other — surfaced as a specific error in `get error log` and in 
CLI responses.

To diagnose:
1. Run `test network` to see which nodes are not responding
2. Check `get error log` for the specific error message
3. Use `query status` after a failed query to see which operators received and responded to the request

To resolve:
- **Same DNS network:** Bind node IPs to the shared local IP rather than the external/router-assigned IP
- **Different DNS networks:** Validate that AnyLog's ports are open and accessible externally — check both the 
- machine-level firewall and any router/modem port-forwarding configuration

Reset the error log once resolved: `reset error log`

### Blockchain validation commands

```bash
# Validate the local blockchain copy is intact
blockchain test

# Check metadata version — run locally and against the master; IDs should match
get metadata version

# On an operator node — validate cluster configuration and data sharing
test cluster
```