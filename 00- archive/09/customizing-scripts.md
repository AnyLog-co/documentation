---
title: Customizing Deployment Scripts
description: How to create, update, or point at your own deployment scripts — from a single local script to a fully custom repo and entry point.
layout: page
visibility: public
version: open source
tags:
- install
- integration
- deployment-scripts
---

<!--
Changed in this revision:
- Fixed heading level: "Last resort: forking the shipped scripts directly" was a sub-heading (###) under option 3;
  promoted to a top-level option (##) since it's a fourth choice, not a detail of option 3
- Added an explicit cross-link to deployment-process.md next to the condensed table, so the two tables don't
  silently drift out of sync if the build logic changes
- Expanded the "entry script isn't named main.al" section into two concrete, copy-pasteable overrides:
  one for docker-compose, one for `docker run` — including the tradeoff of bypassing deploy_anylog.sh's
  other setup steps when you do this
-->

# Customization: Extending Without Breaking the Defaults

Pick the path that matches what you're actually trying to do.

## 1. I just want to run a small custom script — no repo changes needed

Use the built-in hook: `local_script.al`. It's an intentionally empty placeholder, automatically invoked by the
deployment flow via `if !deploy_local_script == true then process !local_scripts/local_script.al`. Set
`DEPLOY_LOCAL_SCRIPT=true` to turn it on, then drop your logic (custom MQTT/Kafka handling, custom scheduled
tasks, etc.) directly into the file. Nothing else needs to change, and it survives future updates to the
deployment-scripts repo since you're not touching any baked-in file.

**To reach and edit it on a running deployment:**
- Get the node up (or at least created — the volume exists once the container is created, even if not running yet).
- Locate the named Docker volume `[container-name]-local-scripts` (e.g. `docker volume inspect <container-name>-local-scripts` to find its mountpoint).
- Edit `local_script.al` at that mounted path directly — changes persist without a rebuild.

## 2. I want to run my own deployment process entirely

This means swapping out `deployment-scripts` for your own repo, rather than just adding one file. There are two ways to point at it, controlled by `DEPLOYMENTS_REPO` / `DEPLOYMENTS_BRANCH` at build time (via `make`):

| # | Condition | Behavior |
|---|-----------|----------|
| 1 | Unset, or explicitly the default (`https://github.com/AnyLog-co/deployment-scripts` @ `main`) | **Built-in default.** Docker seeds the `${CONTAINER_NAME}-local-scripts` named volume from the image on first creation. |
| 2 | `DEPLOYMENTS_REPO` is an existing **local directory** on the host | **Host bind mount.** Compose mounts that directory directly at `/app/deployment-scripts` — no volume, no cloning. |
| 3 | `DEPLOYMENTS_REPO` is an `http://`/`https://` **URL** (your own repo) | **Reclone at startup.** `deploy_anylog.sh` clones your repo itself when the container starts. |
| 4 | `DEPLOYMENTS_REPO` matches none of the above (e.g. a docker image reference) | **Secondary container.** A one-shot helper copies `/app/deployment-scripts` out of that image into the shared named volume, then exits; the main service waits on it. |

This is the condensed version of the table — see [Deployment Integration](deployment-process.md#what-happens-in-the-docker-container)
for the full build-time/runtime mechanics (including the runtime reclone logic and the volume-reuse caveats below), so
this page doesn't get out of sync if that logic changes.

So if you've simply created your own repo with the same structure, option 3 (or 2, if it's local) is usually the one you want — point `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` at it and the rest of the machinery (volumes, cloning) is handled for you.

**Two caveats:**
- This table only applies when deploying via `make`. `docker run` directly bypasses it — volumes, branch selection, and everything else becomes your own responsibility.
- Options 1 and 4 share the same named volume. Docker won't recreate/repopulate it just because `make` reruns — if it already exists from a prior run, it keeps its old content regardless of what `DEPLOYMENTS_REPO`/`DEPLOYMENTS_BRANCH` currently say. (Doesn't apply to 2 or 3.)

## 3. I have my own repo, and my entry script isn't named `main.al`

The container's `ENTRYPOINT` (`/app/deploy_anylog.sh`) hardcodes the path it runs:

```bash
${ANYLOG_PATH}/${APP_NAME} process $ANYLOG_PATH/deployment-scripts/node-deployment/main.al
```

This path is fixed in the entrypoint script itself — it doesn't follow `$LOCAL_SCRIPTS`/`$ANYLOG_PATH` the way `main.al`'s *internal* references do. So you have two options:

**Simplest — no override needed:** name (or copy) your custom entry script to `node-deployment/main.al` within your repo. The entrypoint picks it up with zero further changes, regardless of whether your repo is loaded via option 2, 3, or 4 above.

**If you need a genuinely different filename**, override the container's entrypoint so it calls your script's actual path instead of the hardcoded one. This bypasses `deploy_anylog.sh`'s other setup steps (OpenBao secret fetch, version/arch detection, deployment-scripts resolution, the Kubernetes `/etc/hosts` patch, etc.) — only do this if you've already handled those yourself, or if you maintain your own modified copy of `deploy_anylog.sh` that still does them before calling your script.

*Docker Compose:*
```yaml
services:
  anylog-node:
    image: your-anylog-image
    environment:
      - ANYLOG_PATH=/app
      - APP_NAME=anylog_v1.0.0_x86_64   # or however your image derives this
    entrypoint: ["/bin/bash", "-c"]
    command:
      - >
        ${ANYLOG_PATH}/${APP_NAME} process ${ANYLOG_PATH}/deployment-scripts/node-deployment/my_custom_main.al
```

*Docker Run:*
```bash
docker run \
  --entrypoint /bin/bash \
  your-anylog-image \
  -c '${ANYLOG_PATH}/${APP_NAME} process ${ANYLOG_PATH}/deployment-scripts/node-deployment/my_custom_main.al'
```

Both forms replace `deploy_anylog.sh` entirely for that container, so double-check you don't need anything it would
otherwise have done for you before reaching this line.

## 4. Last resort: forking the shipped scripts directly

For deployments that diverge significantly from any of the above, maintaining a modified copy of the relevant
`.al` files is the heaviest option — reserved for cases where none of the lighter-weight hooks are sufficient.