---
title: "AnyLog as a Service"
description: "Running AnyLog as a systemd service instead of via Docker/Kubernetes."
layout: page
---
<!--
## Changelog. PUT LATEST CHANGES AT THE TOP PLEASE
-
- 2026-08-07 | Eric Aquaronne | change log format adding ref version | 2.0.2606 
- 2026-07-22 | Merged from "05- Configure as a Service.md" and "07 Deploying Anylog as a Service.md"
               into a single document, restructured around two steps: (1) run AnyLog as a plain
               executable, (2) wrap that into a systemd service.
               NOT treated as final — see the review flags below and the banner at the top of the
               rendered doc. Specific conflicts/bugs found while merging, not resolved here:
                 - Binary version placeholder differs between sources: `anylog_v1.3.2404_x86_64`
                   (05-) vs `anylog_v0.0.0_x86_64` (07). Neither looks like a real current version —
                   needs the actual current release filename.
                 - 07's binary download source is a bare IP over plain HTTP (`http://45.33.11.32/`),
                   no HTTPS, no domain. Worth confirming this is still the right/current source.
                 - Both sources build `anylog_configs.env` by reading from an old docker-compose repo
                   layout (`docker-compose/docker-makefile/master-configs/*.env`, singular
                   "docker-makefile"). This does NOT match the current docker-compose repo structure
                   documented in full-deployment.md (plural "docker-makefiles", one directory per node
                   type, each with its own `node_configs.env`). The step below is preserved from the
                   source material as-is, flagged, rather than silently rewritten to guess the correct
                   current path.
                 - 05-'s systemd approach used `ExecStartPre=... source .../*.env` to load config —
                   this doesn't work: a `source` inside `ExecStartPre` runs in a subshell and has no
                   effect on the environment of the actual `ExecStart` process. Dropped in favor of
                   07's `EnvironmentFile=` directive, which is the mechanism that actually works.
                 - 05-'s systemd unit was internally inconsistent: the service file was named
                   `anylog-master.service` but the doc then ran `systemctl restart anylog.service`
                   (a different, non-existent unit). Fixed to a single consistent name throughout.
                 - Both sources had the same curl typo: `get prcoesses` → `get processes`.
                 - 07's "REST-only" alternative deployment path references a `deployment_script.py`
                   using the AnyLog-API that isn't included/shown anywhere, and its systemd unit
                   points at a misspelled path (`anylog_configs.envs`, trailing "s"). Kept as a
                   flagged, unverified alternative rather than rewritten, since the referenced script
                   itself was never provided.
- 2026-07-22 (rev 2) | Part 1 now runs from `~/Desktop/anylog` (a disposable trial location) using
               `screen` instead of `nohup`, with attach/detach/list reminders. Part 2 now opens with
               a step that relocates the binary/scripts/config to a permanent path
               (`/home/user/services/anylog/`) and sets ownership/permissions before creating the
               systemd unit, rather than running the service directly out of the trial location.
               Added a cross-link from `LICENSE_KEY=""` to full-deployment.md's License Key section
               (noting the executable path doesn't share docker-compose's resolution/prompt logic).
               The "Alternative: Minimal REST-only Setup" section is intentionally left unchanged —
               still pending review once the associated AnyLog API script exists.
-->

> ⚠️ **Draft — needs to be recreated / reviewed once we have a confirmed current binary version.**
> This document was merged from two older, mutually inconsistent drafts. The overall flow (run as an
> executable, then convert to a service) is solid, but specific details — binary version, download
> source, and the config-file-generation path — are carried over from stale source material and are
> flagged inline below rather than guessed at.

# AnyLog as a Service

AnyLog's standard deployment path is a Docker container, run via [Docker](./01-%20Docker.md) or
[Kubernetes](03-%20Kubernetes.md). Under certain conditions — limited disk space, regulatory constraints, or
network restrictions — you may instead want to install AnyLog (or EdgeLake) directly as a service on the host,
with no container runtime involved.

When run this way, the CLI interface is disabled — all communication with the node happens over REST once it's
running.

## Part 1 — Run AnyLog as an Executable

To start, we'll run everything from `~/Desktop/anylog` — a simple, disposable location for the initial trial run.
Part 2 moves this into a permanent location once you're ready to make it a service.

1. Download the AnyLog binary. 🟡 *Confirm the current version/filename and download source before using this in
   production* — see the changelog above.
```shell
mkdir -p $HOME/Desktop/anylog/
cd $HOME/Desktop/anylog
wget http://45.33.11.32/anylog_v0.0.0_x86_64
sudo chmod -R 750 $HOME/Desktop/anylog/anylog_v0.0.0_x86_64
```

2. Clone the deployment scripts, which drive what the node actually does at startup:
```shell
cd $HOME/Desktop/anylog/
git clone https://github.com/AnyLog-co/deployment-scripts
```

3. Build a configuration file. 🟡 *This step is preserved from the source docs as-is — it references an older
   docker-compose repo layout (`docker-compose/docker-makefile/anylog-master/`) that doesn't match the current
   structure in full-deployment.md. Needs a corrected path before this is trustworthy.*
```shell
cd $HOME/Desktop/anylog/
git clone https://github.com/AnyLog-co/docker-compose
cat $HOME/Desktop/anylog/docker-compose/docker-makefile/* >> $HOME/Desktop/anylog/anylog_configs.env
```

   At minimum, `anylog_configs.env` should define:
```dotenv
# file path: $HOME/Desktop/anylog/anylog_configs.env

#--- Directories ---
ANYLOG_PATH=/home/user
LOCAL_SCRIPTS=/home/user/deployment-scripts/node-deployment
TEST_DIR=/home/user/deployment-scripts/tests

#--- General ---
# See full-deployment.md's License Key section for how key resolution/prompting works for the
# docker-compose path — the executable path here still just reads this value directly, unvalidated.
LICENSE_KEY=""
NODE_TYPE=generic
NODE_NAME=anylog-node
COMPANY_NAME=New Company
DISABLE_CLI=true
REMOTE_CLI=false

#--- Networking ---
ANYLOG_SERVER_PORT=32548
ANYLOG_REST_PORT=32549
ANYLOG_BROKER_PORT=""

#--- Database ---
DB_TYPE=sqlite
DB_USER=""
DB_PASSWD=""
DB_IP=127.0.0.1
DB_PORT=5432

#--- Blockchain ---
LEDGER_CONN=127.0.0.1:32048
```

4. Run the executable inside a `screen` session, so it keeps running even after you close the terminal, and you can
   reattach to it later to check on it before committing to a full systemd service:
```shell
# start a new named screen session
screen -S anylog

# inside the session, run AnyLog in the foreground:
$HOME/Desktop/anylog/anylog_v0.0.0_x86_64 process $HOME/Desktop/anylog/deployment-scripts/node-deployment/main.al
```

   **Detach** without stopping the process: press `Ctrl+A`, then `D`.

   **Reattach** later to check on it:
```shell
# list active sessions
screen -ls

# reattach
screen -r anylog
```

   **Stop it** when you're ready to move to Part 2: reattach, then `Ctrl+C` to end the process, then type `exit` to
   close the screen session (or run `screen -X -S anylog quit` from outside the session).

5. Confirm it's up (from a separate terminal, while the screen session is running):
```shell
curl -X GET 127.0.0.1:32549
```

## Part 2 — Convert the Executable into a systemd Service

1. Make sure the `screen` session from Part 1 is stopped before proceeding — the service will start its own instance.

2. Move the executable, deployment scripts, and config out of the disposable `Desktop` location into a permanent
   one. This example uses `/home/user/services/anylog/` — adjust to your actual username/path convention.
```shell
sudo mkdir -p /home/user/services/anylog
sudo mv $HOME/Desktop/anylog/anylog_v0.0.0_x86_64 /home/user/services/anylog/
sudo mv $HOME/Desktop/anylog/deployment-scripts /home/user/services/anylog/
sudo mv $HOME/Desktop/anylog/anylog_configs.env /home/user/services/anylog/
```

   Set ownership and permissions on the new location. `anylog_configs.env` contains the license key and database
   credentials, so it shouldn't be world-readable; the binary needs to stay executable:
```shell
sudo chown -R root:root /home/user/services/anylog
sudo chmod 750 /home/user/services/anylog
sudo chmod 750 /home/user/services/anylog/anylog_v0.0.0_x86_64
sudo chmod 640 /home/user/services/anylog/anylog_configs.env
```

3. Create the service file:
```ini
# file path: /etc/systemd/system/anylog-service.service
[Unit]
Description=AnyLog Deployment
After=network.target

[Service]
Type=simple
ExecStart=/home/user/services/anylog/anylog_v0.0.0_x86_64 process /home/user/services/anylog/deployment-scripts/node-deployment/main.al
EnvironmentFile=/home/user/services/anylog/anylog_configs.env
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

4. Enable and start the service:
```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog-service.service
sudo systemctl restart anylog-service.service
```

5. Validate:
```shell
sudo systemctl status anylog-service.service

# get status
curl -X GET 127.0.0.1:32549

# get processes
curl -X GET 127.0.0.1:32549 -H "command: get processes" -H "User-Agent: AnyLog/1.23"
```

## Alternative: Minimal REST-only Setup

🟡 **Unverified — kept from the source material as-is.** This variant skips `deployment-scripts` entirely and
configures only TCP + REST via a small `.al` script, intended for nodes deployed 100% through REST calls after
startup. It references a `deployment_script.py` (using the
<a href="https://github.com/AnyLog-Co/AnyLog-API" target="_blank">AnyLog API</a>) that isn't included in either
source document — treat this section as a sketch of the approach, not a verified procedure, until that script is
located or rewritten.

1. Prepare a startup script that configures only networking:
```anylog
# file path: $HOME/anylog/basic_deployment.al
on error ignore
:prep-instance:
set cli off
set authentication off

:set-params:
anylog_server_port=32548
anylog_rest_port=32549
tcp_bind = false
rest_bind = false
tcp_threads=3
rest_threads=3
rest_timeout=30

:tcp-conn:
on error goto tcp-conn-error
 <run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

:rest-conn:
on error goto rest-conn-error
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

:end-script:
end script

:tcp-conn-error:
print "Failed to configure TCP connection"
goto end-script

:rest-conn-error:
print "Failed to configure REST connection"
goto end-script
```

2. Create the service file:
```ini
# file path: /etc/systemd/system/anylog-service.service
[Unit]
Description=My Executable Service
After=network.target

[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process /home/user/anylog/basic_deployment.al
ExecStartPost=/usr/bin/python3 /home/user/anylog/deployment_script.py 127.0.0.1:32549 --configs /home/user/anylog/anylog_configs.env
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

3. Start and validate exactly as in Part 2, steps 3–4 above.