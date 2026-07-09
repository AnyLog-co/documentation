---
title: Deployment Integration
description: The process by which events occur and decisions are made at deployment in order to provide the initiation scripts.  
layout: page
visibility: public
version: open source
tags:
- install
- integration
---

# Deployment Integration

The following document describes the relationship between the compiled source code (ie AnyLog agent) and deployment-scripts
which defines which services to run on a given AnyLog agent. 

As such the document covers a few things: 

1. [How to deploy AnyLog (simple)](#initial-deployment)
2. [The connection between AnyLog & `deployment-scripts`](#what-happens-in-the-docker-container)
3. [Patches & Versions updates](#patches--version-updates)

<img src="../imgs/deployment_stack_layers.png" height="50%" width="50%" />

The document discusses AnyLog, but the same logic also works when deploying EdgeLake. 

## Initial Deployment

1. User clones a repo called `docker-compose` (or `K8s-compose`) containing a set of configuration files.
2. User updates the configuration files as needed.
   **Key configs:**
   1. `LICENSE_KEY`
   2. `LEDGER_CONN`
   3. `NODE_TYPE`

   A user can skip the full config file (i.e. skip `make`) and just run `docker run` with the 3 environment variables directly.
3. Deploy AnyLog / EdgeLake using `make` or `docker run`.

## What Happens in the Docker Container

AnyLog is the actual source code. To configure its services, AnyLog agents use configuration policies driven by a set of 
scripts called **deployment-scripts**.

By default, the docker image ships with the `main` deployment-scripts already baked in. Using the environment params 
`DEPLOYMENTS_REPO` and `DEPLOYMENTS_BRANCH`, a user can point at a different set of deployment-scripts instead.

Resolution happens in two stages — **build time** (compose file generation, driven by `make`) and, for one of the four 
options below, **runtime** (inside the running agent container).

### Stage A — Build script (compose file generation)

The build script picks one of four modes, in order:

| # | Condition | Behavior |
|---|-----------|----------|
| 1 | `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` unset, **or** explicitly set to the default (`https://github.com/AnyLog-co/deployment-scripts` @ `main`) | **Built-in default.** Enables the `${CONTAINER_NAME}-local-scripts` named volume. On first creation, Docker seeds it from the scripts baked into the image; after that it's just a persistent volume. |
| 2 | `DEPLOYMENTS_REPO` is set and is an existing **local directory** on the host | **Host bind mount.** Compose is rewritten to mount that directory directly at `/app/deployment-scripts`, and the named volume + init-service references are stripped out entirely. Fully static — no cloning, no copying. |
| 3 | `DEPLOYMENTS_REPO` is an `http://` or `https://` **URL** | **Reclone at startup.** No volume is mounted at all at build time; the agent clones the repo itself when it starts (see Stage B below). |
| 4 | `DEPLOYMENTS_REPO` is set but matches none of the above (e.g. a docker image reference) | **Secondary deployment-scripts container.** A one-shot helper service is injected into the compose file: `image: ${DEPLOYMENTS_REPO}:${DEPLOYMENTS_BRANCH}`, which copies `/app/deployment-scripts` out of that image into the shared `${CONTAINER_NAME}-local-scripts` named volume, then exits. The main service waits on it (`condition: service_completed_successfully`) before starting. |

> The same build script also has an unrelated block detecting `DOCKER_SOCKET` and setting `DOCKER_GID` (for Docker-in-Docker 
> support). That's a separate concern from deployment-scripts selection.

**Important caveat — this entire table only applies when deploying via `make`.** If a user runs `docker run` directly 
instead (skipping `make`, using just the 3 core env vars), none of this build-time logic ever executes. It becomes the 
user's responsibility to configure everything themselves:
- volumes (highly recommended)
- branch selection for deployment-scripts, if changing from default at all
- anything else this script would otherwise have handled

**Why "a pre-existing volume takes precedence"** (the original point 0): Options 1 and 4 both mount the *same* named 
volume, `${CONTAINER_NAME}-local-scripts`. Docker does not recreate or repopulate an existing named volume just because 
`make` reruns — it's reused as-is. So if that volume already exists from a prior run, it keeps whatever content it has 
regardless of what `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` currently say. This applies specifically to Options 1 & 4 
(the two modes sharing that volume), not to Options 2 or 3.

### Stage B — Runtime (inside the agent container, on startup — Option 3 only)

This clone logic only runs when Stage A resolved to **Option 3** (URL, reclone-at-startup). Options 1, 2, and 4 are all 
static by the time the container starts — no git operations happen for them inside the agent.

```bash
if [[ CURRENT_REMOTE == DEPLOYMENTS_REPO ]] && [[ CURRENT_BRANCH == DEPLOYMENTS_BRANCH ]]; then
  # already matches — skip reclone
elif git ls-remote --exit-code --heads "${DEPLOYMENTS_REPO}" "${DEPLOYMENTS_BRANCH}"; then
  # branch exists on remote — wipe LOCAL_SCRIPTS and reclone fresh
else
  # branch/repo not reachable — error, leave existing LOCAL_SCRIPTS untouched
fi

if [[ ! -d ${LOCAL_SCRIPTS} ]]; then
  # still missing — hard fail, agent won't start
fi
```

- If the currently-recorded remote **and** branch already match `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` → skip re-cloning, reuse what's on disk.
  ⚠️ **This check only compares repo + branch name, not commit hash.** See the Patches section below — this is the mechanism that determines whether a customer picks up a fix automatically.
- Else, if that branch actually exists on the remote → delete the existing `LOCAL_SCRIPTS` directory and clone fresh.
- Else (repo/branch unreachable) → log an error and leave whatever's currently in `LOCAL_SCRIPTS` alone.
- If `LOCAL_SCRIPTS` still doesn't exist after all that → hard fail (`exit 1`). The agent will not start without deployment-scripts present.

*(The "download the repo as a docker container, `DEPLOYMENTS_BRANCH` as the tag" behavior from the original description 
is real — it's Option 4 above, implemented at build time as a helper compose service rather than inside this runtime script.)*

---

## Patches & Version Updates

Standard process for any reported issue:

1. Understand the issue.
2. Check whether it still exists in the latest code.
3. Fix it.
4. Ask the customer to update to the newer build.

What "update to the newer build" actually does **depends on where the bug lives**, because a docker container bundles 
two different things — the AnyLog/EdgeLake agent binary and the deployment-scripts — and they update through different 
mechanisms.

### A. Bug is in the agent itself
Customer pulls the new image and restarts. The agent code updates immediately, since the image itself is what's being 
replaced. Deployment-scripts are untouched by this step — they live in a separate clone/volume/mount, not something baked 
fresh into every container restart.

### B. Bug is in the deployment-scripts
This depends on which of the four build-time options (see Section 2) the customer is running:

- **Option 1 — default, in-image `main` scripts:** a new image pull brings fixed scripts along *only if* the `${CONTAINER_NAME}-local-scripts` volume doesn't already exist. If it does (i.e. this isn't the customer's first run), the volume is reused as-is and the fix never lands — the customer needs to remove that volume (and ideally the associated configuration policy) so it gets reseeded from the new image.
- **Option 2 — local directory (bind mount):** no clone/copy step exists at all here. The customer has to update that host directory themselves; pulling a new agent image has zero effect on it.
- **Option 3 — URL, reclone at startup:** ⚠️ **if the fix is pushed to the *same* branch the customer is already tracking, a restart will NOT pick it up.** The runtime match check only compares repo + branch strings — it has no concept of "is there a newer commit on this branch." Since repo and branch are unchanged, the agent treats its existing clone as current and skips re-cloning.
  - Workarounds until/unless this is fixed: point at a new branch or tag for the patched scripts, manually delete the `LOCAL_SCRIPTS` directory/volume so nothing matches and a reclone is forced, or `docker exec` in and `git pull` manually.
- **Option 4 — secondary deployment-scripts container:** the helper service runs once and copies into the shared named volume, then exits — it doesn't run again on a plain restart. Same volume-reuse caveat as Option 1: if `${CONTAINER_NAME}-local-scripts` already exists, a new image (even with a bumped tag) won't get re-copied in unless the volume is cleared first (or the compose file is regenerated with a config that forces recreation).

**Practical takeaway for triage:** when a customer reports a deployment-scripts bug, first ask which of the four options 
they're in — that determines whether "just pull the new image" is actually sufficient, or whether they also need to clear 
the `local-scripts` volume, bump a branch/tag, or manually sync a local directory. And if they're deploying via bare 
`docker run` instead of `make`, none of this is automatic in the first place — walk through their setup manually.
