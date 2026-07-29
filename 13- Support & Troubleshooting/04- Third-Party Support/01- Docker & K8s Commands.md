---
title: Docker & Kubernetes Commands (support)
description: The following document provides support on to use Docker and Kubernetes beyond installation of AnyLog agent
layout: page
---
<!--
## Changelog
- 2026-07-24 | Ori Shadmon | Initial document mainly Docker 
---> 
# Docker & K8s Commands

Basic Docker and Kubernetes (K8s) commands for working with AnyLog containers — both raw `docker` invocations and their `make` equivalents.

---

## Table of Contents

- [Docker](#docker)
  - [Command Reference](#command-reference)
  - [Accessing Volumes](#accessing-volumes)
    - [How Data Persistence Works](#how-data-persistence-works)
    - [Working with Volumes](#working-with-volumes)
- [Kubernetes](#kubernetes)

---

## Docker

### Command Reference

| Function | `docker` | `make` |
|---|---|---|
| View all containers | `docker ps -a` | — |
| Attach to an AnyLog instance | `docker attach --detach-keys=ctrl-d [container-name]` | `make attach ANYLOG_TYPE=[AnyLog Dir Name]` |
| Detach from instance | `ctrl-d` | `ctrl-d` |
| Attach to the container's shell (OS-level) | `docker exec -it [container-name] -- /bin/sh` | `make exec ANYLOG_TYPE=[AnyLog Dir Name]` |
| Detach from shell | `ctrl-d` | `ctrl-d` |

> `ANYLOG_TYPE` / `[container-name]` refers to the directory name of the specific AnyLog instance you're targeting (e.g. `anylog-operator`, `anylog-query`, etc.).

**Attach vs. exec** — these serve different purposes:
- **`attach`** connects to the AnyLog process's own console (its CLI), the same session the container was started with.
- **`exec` / `sh`** drops you into a separate shell inside the container's OS, letting you browse the filesystem, inspect files, or run OS-level commands independent of the AnyLog process.

---

### Accessing Volumes

Users may want to directly inspect the persistent (raw) data AnyLog writes to disk — JSON files, deployment scripts, and other artifacts that survive container restarts.

#### How Data Persistence Works

Persistent data is backed by named Docker volumes, declared and wired into the generated `docker-compose.yml`. The **deployment-scripts** volume is a representative example, and it supports four distinct sourcing strategies depending on how `DEPLOYMENTS_REPO` / `DEPLOYMENTS_BRANCH` are set:

| Option | Trigger condition | Behavior |
|---|---|---|
| **1. Built-in default** | `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` unset, **or** set to the default AnyLog repo (`https://github.com/AnyLog-co/deployment-scripts`) on `main` | Uses the deployment-scripts baked into the image. Uncomments the named volume mount in the compose file. |
| **2. Host directory** | `DEPLOYMENTS_REPO` points to an existing local directory | Mounts that host path directly at `/app/deployment-scripts`, bypassing the init container and named volume entirely. |
| **3. Remote URL, no volume** | `DEPLOYMENTS_REPO` is an `http://` or `https://` URL | Removes the deployment-scripts mount altogether — the container reclones the repo itself at startup. |
| **4. Secondary container** | `DEPLOYMENTS_REPO` is set to something else (e.g. a private/custom source) | Spins up a dedicated `<node>-deployment-scripts` init-style container that clones the repo into a shared named volume, which the main service then depends on (`service_completed_successfully`). |

Before any of the above runs, the setup script validates the target repo/branch:
- If using the built-in default or a local host directory, no clone/validation is attempted.
- Otherwise, it checks whether the local scripts directory already matches the requested `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` (via `git config --get remote.origin.url` and `git rev-parse --abbrev-ref HEAD`) and skips recloning if so.
- If it doesn't match, it verifies the branch exists on the remote (`git ls-remote --exit-code --heads`) before wiping and recloning the local scripts directory.
- If the branch/repo can't be reached, it leaves the existing local directory untouched and reports an error rather than destroying working data.
- Finally, it confirms the local scripts directory actually exists — exiting with an error if the clone/mount step failed to produce it.

> **Note:** this same pattern (baked-in image / host mount / remote URL / dedicated container) is the general model AnyLog's compose tooling uses for making other persistent assets configurable — deployment-scripts is simply the concrete example here.

#### Working with Volumes

```bash
# 1. View all volumes
docker volume ls

# 2. Locate a volume's directory on the host
docker volume inspect [volume-name]

# 3. Browse the mounted path directly
ls [mounted-path]
```

---

## Kubernetes

*Coming soon.*