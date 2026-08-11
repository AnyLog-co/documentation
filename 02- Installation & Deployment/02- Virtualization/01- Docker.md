---
title: Full Deployment via Docker Compose
description: Deploying AnyLog nodes using AnyLog's official docker-compose repo — installation, configuration, and how LEDGER_CONN and networking work together.
layout: page
---
<!--
## Changelog
- 2026-08-07 | Eric Aquaronne | change log format adding ref version | 2.0.2606 
- 2026-07-22 | Created document from AnyLog's docker-compose repo (README.md, deploy.sh, Makefile,
               node_configs.env, TOPOLOGY.md), per the "general sense" outline: install
               docker/make/git → clone repo → configure → start node → explain LEDGER_CONN and
               networking.
               Uses the os-dev branch for the docker-compose repo clone and the deployment-scripts
               DEPLOYMENTS_BRANCH, per direction to move off the old default branch.
               Open items surfaced while writing this, not resolved here:
                 - `Makefile`'s default TAG is 2.0.2606, but `deploy.sh`'s own standalone default
                   (used when invoked without make) is still 1.4.2604 — the two don't agree. This
                   doc documents 2.0.2606 as current, since `make` is the primary entry point.
                 - Both `Makefile`'s help text and `deploy.sh`'s `cmd_help`/`cmd_check_vars` still
                   print "default: pre-develop" for TAG, which matches neither actual default above.
                 - `node_configs.env`'s own comment block still lists `master-operator` /
                   `master-publisher` as valid NODE_TYPE values, but the actual supported aliases
                   (in `deploy.sh` and the repo's directory names) are `standalone-operator` /
                   `standalone-publisher`. This doc uses the latter, since that's what the code
                   actually resolves.
                 - `node_configs.env` has an apparent typo: `HOST_SYS="/sy"` (likely meant `/sys`).
                 - The lower-level `test-status`/`test-node`/`test-network` calls in `deploy.sh` use
                   a POST + JSON body, differing from the GET + header convention shown elsewhere
                   in the docs (e.g. install.md). Not resolved here since this doc only exposes the
                   `make`/`deploy.sh` targets, not the raw curl underneath.
-->

> This is the full, configuration-driven deployment path, built around AnyLog's official
> <a href="https://github.com/AnyLog-co/docker-compose" target="_blank">docker-compose</a> repo. For a fast, minimal single-command trial
> instead, see <a href="../../01-%20Getting%20Started/03-%20install.md" target="_blank">Installing & Deploying AnyLog</a>.

## 1. Install Docker, Make, and Git

```shell
# Install Docker on Ubuntu
sudo apt-get -y update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin make git

# Grant your user permission to use Docker without sudo
USER=`whoami`
sudo groupadd docker
sudo usermod -aG docker ${USER}
newgrp docker
```

`make` is optional — every `make` target is a thin wrapper around `deploy.sh`. If `make` isn't available on your
system (e.g. some ARM/Qualcomm hardware), use `bash deploy.sh` directly; behavior is identical either way.

## 2. Clone the Repository

```shell
git clone -b os-dev https://github.com/AnyLog-co/docker-compose
cd docker-compose
```

AnyLog is a private image repository — <a href="https://www.anylog.network/download" target="_blank">request credentials</a> for both your
Docker login and your license key, then log in:

```shell
docker login -u anyloguser -p [Docker Login Passkey]
```

### Repository layout

```
docker-compose/
├── Makefile                          # Thin wrapper around deploy.sh
├── deploy.sh                         # Node lifecycle manager — works without make
├── docker-makefiles/
│   ├── anylog-generic/
│   │   └── node_configs.env          # Config template — copy and customise per node
│   ├── anylog-master/
│   ├── anylog-operator/
│   ├── anylog-publisher/
│   ├── anylog-query/
│   ├── anylog-standalone-operator/
│   ├── anylog-standalone-publisher/
│   ├── build_docker_compose.sh       # Generates docker-compose.yaml from configs
│   ├── prep_configs.sh               # Pre-flight config validation
│   └── docker-compose-files/         # Generated compose files land here (not committed)
├── license-generator/                # License validation/acceptance service used by `deploy.sh up`
└── support/                          # Grafana, PostgreSQL, MongoDB, Remote-GUI
```

Both the short form (`operator`) and the full directory name (`anylog-operator`) are accepted everywhere `ANYLOG_TYPE`
is used — both `make` and `deploy.sh` resolve the alias automatically.

### Container runtime

`deploy.sh` auto-detects your environment — no configuration needed. It uses `podman` in place of `docker` if
`podman` is installed, and for compose it prefers `podman-compose`, falling back to `docker-compose`, then
`docker compose`, in that order. All the `make`/`bash deploy.sh` commands in this guide work unchanged regardless
of which of these is actually present on your system.

## 3. Node Types

Every node type runs the exact same AnyLog image — what differs is which services are enabled. Quick summary:

| Node Type | Role                                                                                                                                                              |
|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Master** (Metadata / `master`) | Hosts the network's metadata — the Metadata Manager described in <a href="../../01-%20Getting%20Started/01-%20Introduction.md" target="_blank">Introduction to AnyLog</a>|                                                                    |                                                                  |
| **Operator** (`operator`) | Stores data and answers queries                                                                                                                                   |
| **Publisher** (`publisher`) | A non-storage node that distributes data from edge sources across Operator nodes                                                                                  |
| **Query** (`query`) | Coordinates distributed queries across Operators                                                                                                                  |
| **Generic** (`generic`) | A sandbox with only TCP, REST, and Message Broker configured — no storage, no cluster role. Useful for testing connectivity before committing to a real node type. |

`standalone-operator` and `standalone-publisher` combine Master with an Operator or Publisher, respectively, on a
single agent.

## 4. Configure Your Node

For full control over node behavior, copy the generic template and customize it:

```shell
cp -r docker-makefiles/anylog-generic docker-makefiles/my-operator
```

Edit `docker-makefiles/my-operator/node_configs.env`. At minimum, update:

| Variable | Purpose |
|---|---|
| `NODE_TYPE` | Node role: `generic`, `master`, `operator`, `query`, `publisher`, `standalone-operator`, `standalone-publisher` |
| `NODE_NAME` | Must be unique per node |
| `COMPANY_NAME` | Owner of the node |
| `ANYLOG_SERVER_PORT`, `ANYLOG_REST_PORT` | Must be unique per machine |
| `LEDGER_CONN` | IP:port of the Master/Metadata Manager node — see <a href="#6-understanding-ledger_conn" target="_blank">below</a> |
| `CLUSTER_NAME` | Unique per Operator, unless HA is enabled |
| `LICENSE_KEY` | Optional to set here — see <a href="#license-key" target="_blank">License Key</a> below |
| `DB_USER` / `DB_PASSWD` | Only if using PostgreSQL |

You'll also want to decide your networking setup (`NETWORK_TYPE`, `OVERLAY_IP`, etc.) — covered in
<a href="#7-understanding-the-network-configuration" target="_blank">Understanding the Network Configuration</a> below.

### License Key

Every `up` command validates a license before starting the node:

1. If `LICENSE_KEY` is already set in `node_configs.env`, deployment proceeds immediately — no prompts.
2. If no key is set, and you don't pass one via `--license-key`, you'll be prompted interactively: the license
   agreement is displayed, you provide name/email/project and accept, and the accepted key is written back into
   `node_configs.env` automatically so future deployments skip the form.

```shell
# Pass explicitly
make up ANYLOG_TYPE=my-operator LICENSE_KEY="<key>"
bash deploy.sh up --type my-operator --license-key "<key>"

# Or just set LICENSE_KEY="<key>" directly in node_configs.env beforehand
```

## 5. Start the Node

```shell
# via make
make up ANYLOG_TYPE=my-operator

# via deploy.sh (no make required)
bash deploy.sh up --type my-operator
```

Check it came up:

```shell
make logs ANYLOG_TYPE=my-operator
bash deploy.sh logs --type my-operator
```

Verify it's actually working:

```shell
make full-test ANYLOG_TYPE=my-operator
bash deploy.sh full-test --type my-operator
```

`full-test` runs `test-status` (confirms the process is running), `test-node` (validates node configuration), and
`test-network` (confirms it can see its peers) in sequence — the same three checks from the Quick Install guide,
just wrapped into a single command.

To deploy a second node of the same type, copy the folder again and update `NODE_NAME`, ports, and `CLUSTER_NAME`:

```shell
cp -r docker-makefiles/my-operator docker-makefiles/my-operator2
# edit node_configs.env in my-operator2 first
make up ANYLOG_TYPE=my-operator2
```

## 6. Understanding LEDGER_CONN

`LEDGER_CONN` is how every non-Master node (Operator, Query, Publisher) finds the Metadata Manager (Master) node —
it's set to that node's **TCP port**, not its REST port:

```dotenv
LEDGER_CONN=127.0.0.1:32048
```

This is the single most common source of "my node won't join the network" problems, because the correct value
depends entirely on your Docker networking mode (see below):

- **Host networking (Linux/WSL, `NETWORK_TYPE` empty or `network`)** — containers share the host's network stack
  directly, so `127.0.0.1:<master's TCP port>` (or the Master's real host IP, if on a different machine) works as-is.
- **Port-mapped mode (Windows/macOS, `NETWORK_TYPE=ports`)** — containers do *not* share the host network. `127.0.0.1`
  inside one container does not reach another container. You need the **host machine's LAN IP** here instead — set
  via `OVERLAY_IP` on the Master, and reference that same IP in `LEDGER_CONN` on every other node.
- **Custom/overlay network (`NETWORK_TYPE=<network-name>`)** — nodes reach each other by container name or overlay
  IP across physical machines. `LEDGER_CONN` should use the Master's overlay IP (or container name, if on the same
  named network), not its host IP.

If `test network` doesn't show all expected peers after deployment, `LEDGER_CONN` pointing at the wrong address is
the first thing to check.

## 7. Understanding the Network Configuration

AnyLog's networking is split across two independent layers — getting one right doesn't automatically fix the other.

### Layer 1 — Docker Network Topology (`NETWORK_TYPE`)

Controls how the **container** connects to the host and to other containers. Purely a Docker-level concern; it has
no effect on how AnyLog itself resolves or advertises its IP.

| Value | Behavior | When to use |
|---|---|---|
| *(empty)* | Auto-detect | Recommended default — host mode on Linux/WSL, port-mapped on Windows/macOS |
| `network` | `network_mode: host` | Linux/WSL only |
| `ports` | Explicit port mapping | Windows, macOS, or Linux when host networking isn't available |
| `<custom-name>` | Pre-created external Docker network | Multi-machine deployments (VPN, Swarm overlay) |

For a multi-host Swarm overlay, create the network once, then point every node at it:

```shell
docker network create --scope=swarm --attachable -d overlay anylog-net
```
```dotenv
NETWORK_TYPE=anylog-net
```

### Layer 2 — AnyLog Network Identity

Controls how AnyLog resolves and **advertises its own IP** — the address it registers in the blockchain/metadata
layer and binds its TCP/REST/Broker ports to. Getting this wrong means other nodes can see your node in the
metadata but can't actually reach it.

| Variable | Purpose |
|---|---|
| `NIC_TYPE` | Resolve the node's IP from a specific network interface (e.g. `eth0`) — useful on multi-NIC hosts |
| `OVERLAY_IP` | Overrides the resolved IP entirely — required whenever the container's internal IP isn't reachable from outside (port-mapped mode, NAT, Swarm overlay) |
| `TCP_BIND` / `REST_BIND` / `BROKER_BIND` | Whether each protocol binds to the resolved/overlay IP specifically (`true`) or all interfaces (`false`) |

### Quick reference

| Scenario | `NETWORK_TYPE` | `OVERLAY_IP` |
|---|---|---|
| Linux, single node | *(empty)* | *(empty)* |
| Windows/macOS, single node | `ports` or *(empty)* | host's LAN IP |
| Multi-node, same LAN (Linux) | *(empty)* | *(empty)* |
| Multi-node, VPN/overlay | `<network-name>` | overlay/VPN IP |
| Multi-node, cloud/NAT | `ports` or `<network-name>` | public/elastic IP |

In short: **Layer 1 decides how the container talks to the network at all; Layer 2 decides what address it tells
other nodes to use.** On a single Linux machine you can usually leave both at their defaults. The moment you're on
Windows/macOS or spanning multiple machines, `OVERLAY_IP` (Layer 2) is almost always the setting you need — and it
has to match whatever `LEDGER_CONN` (§4 above) expects on the other end.