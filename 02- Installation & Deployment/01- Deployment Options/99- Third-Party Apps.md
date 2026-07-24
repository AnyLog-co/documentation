---
title: Third Party Apps Install
description: The following document provides support on how to use built-in configs (as part of docker-compose)to 
  seamlessly install third-party applications.
layout: page
---
<!--
## Changelog
- 2026-07-24 | Ori Shadmon | Initial document on third-party apps
---> 

> This page documents the services managed under `docker-compose/support`: how they're configured, how the Makefile 
> drives their lifecycle, and how to add new ones.

## Overview

`support/` holds the tooling to configure, generate, and manage the Docker/Podman containers that run alongside AnyLog:

| Service | Managed by Makefile? | Purpose |
|---|---|---|
| [Remote-GUI](#remote-gui) | ✅ | Web UI for AnyLog |
| [Grafana](#grafana) | ✅ | Dashboards / visualization |
| [PostgreSQL](#postgresql) | ✅ | Relational datastore |
| [MongoDB](#mongodb) | ✅ | Document datastore |
| [Ollama](#ollama) | ❌ (standalone) | Local LLM runtime for MCP function calling |
| [Video Inference Models](#video-inference-models) | ❌ (standalone) | CV/ML inference on edge video streams |
| [Nebula Overlay Network](#nebula-overlay-network) | ❌ (standalone) | Encrypted peer-to-peer overlay networking |
| [Syslog Forwarding](#syslog-forwarding) | ✅ (special-cased) | Forwards host syslog traffic to the AnyLog broker port |

### Requirements

- Docker ≥ 20.10 **or** Podman ≥ 4.0
- `docker compose` plugin **or** `docker-compose` / `podman-compose`
- Bash ≥ 4.0 (for `docker_compose_builder.sh`)
- `make`

The Makefile auto-detects whichever container engine and compose command are installed (`podman`/`podman-compose` preferred, falling back to `docker`/`docker-compose`/`docker compose`).

### Directory Structure

```
support/
├── Makefile                      # All lifecycle commands
├── README.md                     # Project readme
├── Ollama.md                     # Ollama setup guide
├── Video-Inferences.md           # Video inference models guide
├── Nebula.md                     # Nebula overlay network setup guide
├── docker_compose_builder.sh     # Generates docker-compose.yml from configs.yaml
├── syslog.sh                     # Configures host syslog daemon → AnyLog broker port
├── grafana/
│   ├── configs.yaml
│   └── docker-compose.yml        # generated — do not edit by hand
├── mongodb/
│   ├── configs.yaml
│   └── docker-compose.yml
├── ollama/
│   ├── configs.yaml
│   ├── docker-compose.yaml
│   ├── docker-compose-gpu.yaml
│   └── ollama-configs.png
├── postgres/
│   ├── configs.yaml
│   └── docker-compose.yml
└── remote-gui/
    ├── configs.yaml
    └── docker-compose.yml
```

Each `docker-compose.yml` is auto-generated from its sibling `configs.yaml`, either explicitly via `make dry-run` or automatically on the first `make up` for that service. **Any subdirectory containing a `configs.yaml` is automatically recognized as a service** — no Makefile edits are needed to add new instances.

---

## Quick Start

```bash
# 1. (Optional) Pre-generate all docker-compose files
make dry-run

# 2. Start all default services (generates compose files on-demand if missing)
make up

# 3. Start a specific service
make up SERVICE=grafana

# 4. List all services the Makefile can see
make list
```

---

## Config File Format

Each service directory contains a `configs.yaml` that drives `docker_compose_builder.sh`, with four sections:

```yaml
GENERAL:
  IMAGE: <registry/image>
  TAG:   <tag>
  NAME:  <container name>          # also becomes the compose service key

NETWORK_CONFIGS:
  NETWORK_MODE: host | ports       # host → network_mode: host; ports → publishes listed ports
  PORTS:
    - <port>

ENV_VARS:
  KEY: value                       # passed as environment variables
  # comment lines are stripped

VOLUMES:
  volume-name: /container/path     # named volumes — declared at top level automatically
```

> **`REMOTE_GUI_NIC`** (remote-gui only): when this key is present in `ENV_VARS`, the builder resolves its value as a network interface name at generation time and injects `VITE_API_URL=http://<resolved-ip>:<REMOTE_GUI_BE>`. Leave the key absent to skip `VITE_API_URL` entirely.

All generated compose files also include:

```yaml
restart: always
stdin_open: true
tty: true
```

---

## Service Configs

### Remote-GUI

| Field | Value |
|---|---|
| Image | `anylogco/remote-gui:1.0.0` |
| Ports | `8080` (backend), `31800` (frontend) |
| Key env vars | `REMOTE_GUI_FE`, `REMOTE_GUI_BE`, `GRAFANA_URL`, `REMOTE_GUI_NIC` |
| Volumes | `image-vol`, `usr-mgm-vol`, `report-configs` |
| Aliases | `remote-gui`, `gui` |

### Grafana

| Field | Value |
|---|---|
| Image | `grafana/grafana:latest` |
| Port | `3000` |
| Key env vars | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_INITDB_ARGS` |
| Volumes | `grafana-data`, `grafana-log`, `grafana-config` |
| Aliases | `grafana` |

### PostgreSQL

| Field | Value |
|---|---|
| Image | `postgres:16.0-alpine` |
| Port | `5432` |
| Key env vars | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_INITDB_ARGS` |
| Volumes | `pgdata` |
| Aliases | `postgres`, `psql` |
| Native client | `psql -U admin -d postgres` (via `make attach`) |

### MongoDB

| Field | Value |
|---|---|
| Image | `mongo:latest` |
| Port | `27017` |
| Key env vars | `MONGO_USER`, `MONGO_PASSWORD` |
| Volumes | `mongo-data`, `mongo-configs` |
| Aliases | `mongodb`, `mongo` |
| Native client | `mongosh` (via `make attach`) |

### Ollama

Standalone — **not managed by the Makefile**. Lightweight open-source framework for running LLMs locally; AnyLog/EdgeLake use it as the tested model framework for MCP function calling in the Remote-GUI.

| Field | Value |
|---|---|
| Image | `ollama/ollama:latest` |
| Port | `11434` |
| GPU variant | `ollama/docker-compose-gpu.yaml` (requires NVIDIA Container Toolkit) |
| Default model | `qwen2.5:7b-instruct` |

→ Full setup guide: `Ollama.md`

### Video Inference Models

Standalone — **not managed by the Makefile**. CV/ML inference on edge video streams, feeding results into AnyLog/EdgeLake nodes.

→ Full setup guide: `Video-Inferences.md`
→ Source repository: `AnyLog-co/AnyLog-Video-Inference-Models`

### Nebula Overlay Network

Standalone — **not managed by the Makefile**. Nebula creates an encrypted peer-to-peer mesh across physically separated machines, giving distributed AnyLog/EdgeLake nodes a shared overlay IP space without requiring them to be on the same LAN or VPN.

| Field | Value |
|---|---|
| Deployed via | `docker compose` on each node |
| Min. nodes | 1 lighthouse + 1 host |
| Overlay port | UDP `4242` |
| Auth | Mutual certificate-based (CA you control) |

→ Full setup guide: `Nebula.md`
→ Source repository: `oshadmon/nebula-anylog`

### Syslog Forwarding

Special-cased in the Makefile: when `SERVICE=syslog` is passed, `setup`, `remove`, and `help` delegate directly to `syslog.sh` instead of the docker-compose lifecycle path.

`syslog.sh` reads `SYSLOG_MONITORING` and `ANYLOG_BROKER_PORT` directly from a `node_configs.env` file — no extra arguments needed once the node config is set up. Both `setup` and `remove` are **no-ops** when `SYSLOG_MONITORING != "true"`; `setup` is idempotent (safe to call repeatedly).

| Field | Value |
|---|---|
| Config keys | `SYSLOG_MONITORING` (must be `"true"`), `ANYLOG_BROKER_PORT` |
| Linux | rsyslog drop-in `/etc/rsyslog.d/60-custom-forwarding.conf` (TCP) |
| macOS | `/etc/syslog.conf` append (UDP) — ensure the broker port is open for UDP |
| Default `NODE_CONFIGS` path | `docker-makefiles/anylog-generic/node_configs.env` |

```bash
# Direct invocation
bash syslog.sh setup  [NODE_CONFIGS]
bash syslog.sh remove [NODE_CONFIGS]

# Via make (SERVICE=syslog intercepts before docker-compose logic)
make setup  SERVICE=syslog                                                               # prompts for config path
make setup  SERVICE=syslog NODE_CONFIGS=../docker-makefiles/anylog-operator/node_configs.env
make remove SERVICE=syslog NODE_CONFIGS=../docker-makefiles/anylog-operator/node_configs.env
```

If `NODE_CONFIGS` is not supplied on the command line, `make setup`/`make remove` prompt interactively for the config file path.

---

## `docker_compose_builder.sh`

Reads a `configs.yaml` and writes a `docker-compose.yml` next to it.

```bash
# Usage
./docker_compose_builder.sh [config_file] [output_file]

# Defaults
./docker_compose_builder.sh                                          # configs.yaml → docker-compose.yml
./docker_compose_builder.sh remote-gui/configs.yaml                  # custom input
./docker_compose_builder.sh remote-gui/configs.yaml out-compose.yml  # custom input + output
```

### Port Conflict Detection

Before writing the compose file, the builder checks whether any port in `NETWORK_CONFIGS.PORTS` is already in use, adapting the check to the network mode:

| `NETWORK_MODE` | How ports are bound | Check method |
|---|---|---|
| `ports` | Docker proxy | `docker ps --format '{{.Ports}}'` |
| `host` | Host OS directly | `ss -tlnp` (falls back to `lsof`) |

If a conflict is found, the builder prints which container or process holds the port and exits non-zero — the compose file is **not** written.

---

## Makefile Reference

### Targets

| Target | Description |
|---|---|
| `dry-run` | Generate `docker-compose.yml` for all discovered services (or `SERVICE=one`) |
| `up` | Start service(s); generates the compose file on-demand if missing |
| `down` | Stop service(s) |
| `clean` | Stop and remove volumes |
| `clean-all` | Stop, remove volumes, and remove the image |
| `logs` | Print container logs — `SERVICE=` required |
| `logs-f` | Follow container logs — `SERVICE=` required |
| `attach` | Attach the service's **native client** (`psql` for postgres*, `mongosh` for mongo*) — `SERVICE=` required. Any other service prints "Unsupported attach option." |
| `exec` | Open a **plain bash shell** in the container — `SERVICE=` required |
| `list` | Print default and all auto-discovered services |
| `setup` | `SERVICE=syslog` only — install the host syslog → AnyLog forwarding rule |
| `remove` | `SERVICE=syslog` only — remove the host syslog → AnyLog forwarding rule |
| `help` | Show usage and the list of targets (delegates to `syslog.sh help` when `SERVICE=syslog`) |

> **Note on `attach` vs `exec`:** these are two distinct targets. `attach` drops you into the database client that matches the service name pattern (`postgres*` → `psql -U admin -d postgres`, `mongo*` → `mongosh`); `exec` always opens `/bin/bash` regardless of service type.

Omit `SERVICE` to act on all four default services (`remote-gui`, `grafana`, `postgres`, `mongodb`) for `up`, `down`, `clean`, and `clean-all`. `logs`, `logs-f`, `attach`, and `exec` always require an explicit `SERVICE=`.

### Service Aliases

| Service | Accepted values for `SERVICE=` |
|---|---|
| Remote-GUI | `remote-gui`, `gui` |
| Grafana | `grafana` |
| PostgreSQL | `postgres`, `psql` |
| MongoDB | `mongodb`, `mongo` |

### Custom Instances

To run a second PostgreSQL or MongoDB instance (e.g. for a different AnyLog node), create a new directory with a `configs.yaml` — no Makefile changes required:

```bash
cp -r postgres/ postgres-prod/
# edit postgres-prod/configs.yaml (change NAME, port, volumes as needed)

make up   SERVICE=postgres-prod
make logs SERVICE=postgres-prod
make attach SERVICE=postgres-prod    # drops into psql automatically (matches postgres* pattern)
```

`make list` shows every directory the Makefile has discovered.

### Example Commands

```bash
# Generate compose files
make dry-run                           # all discovered services
make dry-run SERVICE=remote-gui        # one service

# Lifecycle
make up                                # start all 4 defaults
make up        SERVICE=gui
make up        SERVICE=postgres-prod   # custom instance
make down      SERVICE=grafana
make clean     SERVICE=mongo
make clean-all SERVICE=psql

# Logs
make logs   SERVICE=gui                # print and exit
make logs-f SERVICE=mongo              # follow

# Native client access (psql / mongosh)
make attach SERVICE=psql               # psql -U admin -d postgres
make attach SERVICE=mongo              # mongosh
make attach SERVICE=postgres-prod      # psql -U admin -d postgres (matches postgres* pattern)

# Plain bash shell in the container
make exec SERVICE=gui                  # /bin/bash
make exec SERVICE=psql                 # /bin/bash
make exec SERVICE=mongo                # /bin/bash

# Syslog forwarding
make setup  SERVICE=syslog             # prompts for node config path
make setup  SERVICE=syslog NODE_CONFIGS=../docker-makefiles/anylog-operator/node_configs.env
make remove SERVICE=syslog NODE_CONFIGS=../docker-makefiles/anylog-operator/node_configs.env

# Discovery
make list                              # show default + all discovered services
make help                              # show usage and target list
```