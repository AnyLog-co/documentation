---
title: Installing AnyLog as a Service
description: Deploy AnyLog directly on bare-metal Linux as a systemd service, without Docker or Kubernetes.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | updated hyperlinks - need to update directions (once working)
--> 

By default AnyLog is deployed as a Docker container or via Kubernetes. In some environments — limited disk space, 
regulatory requirements, network constraints, or hardware without container support — it makes more sense to install 
AnyLog directly on the host as a systemd service.

> When running as a service the local CLI is disabled. All interaction with the node after startup is done via REST. 
> See <a href="{{ '/docs/CLI/AnyLog-CLI/' | relative_url }}">AnyLog CLI</a> and
> <a href="{{ '/docs/Network-Services/using-rest/' | relative_url }}">Using REST</a> for reference.

---

## Prerequisites

- Linux host (x86_64)
- `wget`, `curl`, `systemctl` available
- Python 3 (only required for the REST-based deployment path)
- Network ports open for TCP and REST (default: 32548, 32549)

---

## Step 1 — Download the AnyLog binary

A full list of available builds is at <a href="https://downloads.anylog.network/images+vms/" target="_blank">downloads.anylog.network</a>

```shell
mkdir -p $HOME/anylog
cd $HOME/anylog
wget http://45.33.11.32/anylog_v0.0.0_x86_64
chmod 750 $HOME/anylog/anylog_v0.0.0_x86_64
```

Replace `anylog_v0.0.0_x86_64` with the actual build filename for your target version.

---

## Option A — Deploy using the deployment scripts (recommended)

This path uses the same deployment scripts as a Docker-based deployment, with the AnyLog binary substituted for the 
container image.

### 1. Clone the deployment scripts

```shell
cd $HOME
git clone https://github.com/AnyLog-co/deployment-scripts
```

### 2. Prepare the configuration file

```shell
cd $HOME
git clone https://github.com/AnyLog-co/docker-compose
cat $HOME/docker-compose/docker-makefile/* >> $HOME/anylog/anylog_configs.env
```

### 3. Edit `anylog_configs.env`

Open `$HOME/anylog/anylog_configs.env` and update at minimum the following:

```dotenv
# --- Directories ---
ANYLOG_PATH=/home/user                                        # AnyLog root directory
LOCAL_SCRIPTS=/home/user/deployment-scripts/node-deployment   # path to deployment scripts
TEST_DIR=/home/user/deployment-scripts/tests

# --- General ---
LICENSE_KEY=""
NODE_TYPE=generic       # options: generic, master, operator, publisher, query
NODE_NAME=anylog-node
COMPANY_NAME=New Company
DISABLE_CLI=true        # must be true for service deployment
REMOTE_CLI=false

# --- Networking ---
ANYLOG_SERVER_PORT=32548
ANYLOG_REST_PORT=32549
ANYLOG_BROKER_PORT=""   # leave blank if not using a message broker

# --- Database ---
DB_TYPE=sqlite          # or psql for PostgreSQL
DB_USER=""
DB_PASSWD=""
DB_IP=127.0.0.1
DB_PORT=5432

# --- Blockchain ---
LEDGER_CONN=127.0.0.1:32048   # IP:Port of the master node
```

See <a href="{{ '/docs/Getting-Started/deployment-scripts/' | relative_url }}">Deployment Scripts</a> for the full list 
of configuration options.

### 4. Create the systemd service file

Create `/etc/systemd/system/anylog.service`:

```ini
[Unit]
Description=AnyLog Node
After=network.target

[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process /home/user/deployment-scripts/node-deployment/main.al
Restart=always
User=root
Group=root
EnvironmentFile=/home/user/anylog/anylog_configs.env

[Install]
WantedBy=multi-user.target
```

Update the paths to match your actual installation directory and binary filename.

### 5. Start the service

```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog.service   # auto-start on reboot
sudo systemctl start anylog.service
```

### 6. Verify

```shell
# Check service status
sudo systemctl status anylog.service

# Check node is responding
curl -X GET 127.0.0.1:32549

# Check running services
curl -X GET 127.0.0.1:32549 \
  -H "command: get processes" \
  -H "User-Agent: AnyLog/1.23"
```

---

## Option B — Minimal startup + REST-based configuration

This path starts the node with only TCP and REST enabled, then configures all other services via the REST API. It gives 
you full programmatic control over the node with no dependency on the deployment scripts.

### 1. Create a minimal startup script

Create `$HOME/anylog/basic_deployment.al`:

```anylog
on error ignore

:set-params:
anylog_server_port = 32548
anylog_rest_port   = 32549
tcp_bind           = false
rest_bind          = false
tcp_threads        = 3
rest_threads       = 3
rest_timeout       = 30

# Disable CLI and authentication for service mode
set cli off
set authentication off

:tcp-conn:
on error goto tcp-conn-error
<run tcp server where
    external_ip = !external_ip and external_port = !anylog_server_port and
    internal_ip = !ip         and internal_port  = !anylog_server_port and
    bind = !tcp_bind and threads = !tcp_threads>

:rest-conn:
on error goto rest-conn-error
<run rest server where
    external_ip = !external_ip and external_port = !anylog_rest_port and
    internal_ip = !ip         and internal_port  = !anylog_rest_port and
    bind = !rest_bind and threads = !rest_threads and timeout = !rest_timeout>

:end-script:
end script

:tcp-conn-error:
print "Failed to configure TCP connection"
goto end-script

:rest-conn-error:
print "Failed to configure REST connection"
goto end-script
```

### 2. Create a Python configuration script (optional)

Use the [AnyLog API](https://github.com/AnyLog-Co/AnyLog-API) to configure the node after startup:

```shell
chmod +x $HOME/anylog/deployment_script.py
```

### 3. Create the systemd service file

Create `/etc/systemd/system/anylog.service`:

```ini
[Unit]
Description=AnyLog Node
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

`ExecStartPost` runs your Python configuration script after the node starts. Remove that line if you are configuring 
the node manually via REST.

### 4. Start and verify

```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog.service
sudo systemctl start anylog.service

# Verify
sudo systemctl status anylog.service
curl -X GET 127.0.0.1:32549
curl -X GET 127.0.0.1:32549 \
  -H "command: get processes" \
  -H "User-Agent: AnyLog/1.23"
```

---

## Managing the service

```shell
sudo systemctl stop anylog.service      # stop
sudo systemctl restart anylog.service   # restart
sudo systemctl disable anylog.service   # remove from auto-start
journalctl -u anylog.service -f         # tail the service log
```

---

## Next steps

Once the node is running, configure it via REST using the same commands you would use on the CLI — wrap any AnyLog 
command in a REST GET request with the `command` header:

```shell
curl -X GET 127.0.0.1:32549 \
  -H "command: run blockchain sync where source=master and time=30 seconds and dest=file and connection=!master_node" \
  -H "User-Agent: AnyLog/1.23"
```

See <a href="{{ '/docs/Network-Services/using-rest/' | relative_url }}">Using REST</a> and
<a href="{{ '/docs/Network-Services/background-services/' | relative_url }}">Background Services</a> for full 
configuration reference.