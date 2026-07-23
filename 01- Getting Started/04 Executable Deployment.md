---
title: "Deploy AnyLog Executable and Configure as Service"
description: Directions on how to deploy AnyLog as an executable directly on the machine and configure it as a service.
layout: page
source_path: "examples/Service AnyLog/05 Executable Deployment and 07 Configure as a Service.md"
visibility: private
tags:
  - getting-started
  - install
---

<!--- 
### 📜 Change Log
 **Date**   | **Name**       | **Change**      | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-2  | Eric A         |  merger conf as a service in the file | 2.0.2606 |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 |            |
--->

---
# Deploy AnyLog Executable

The following provides step-by-step directions for installing AnyLog (executable) on _Ubuntu 22.04 LTS_.

1. Install requirements
```shell
for cmd in update upgrade ; do apt-get -y ${cmd} ; done 

sudo apt-get install -y bash git openssh-client gcc python3-dev musl-dev
sudo apt-get install -y bash python3 python3-dev python3-pip wget build-essential libffi-dev
sudo python3 -m pip install --upgrade pip

mkdir ~/AnyLog-code ; cd ~/AnyLog-code
```

2. Download and Install AnyLog / EdgeLake Python requirements 
```shell
curl https://raw.githubusercontent.com/EdgeLake/EdgeLake/main/requirements.txt -o ~/AnyLog-code/requirements.txt 
python3 -m pip install --upgrade -r ~/AnyLog-code/requirements.txt
```

3. Download AnyLog - make sure version matches with in terms of Operating System and CPU architecture  
```shell
curl http://173.255.254.34:31900/ubuntu/anylog_v1.3.2404_x86_64 -o ~/AnyLog-code/anylog_v1.3.2404_x86_64 
```

4. Download configurations file
```shell
cd ~/AnyLog-code
git clone <a href="https://github.com/AnyLog-co/docker-compose" target="_blank">https://github.com/AnyLog-co/docker-compose</a> 
```

5. Update [configuration files](https://github.com/AnyLog-co/docker-compose/tree/os-dev/docker-makefile) & export configurations. We recommend updating the following params: 
   * **base_configs.env**
     * [`LICENSE_KEY`](https://anylog.co/download-anylog/)
     * `NODE_NAME` 
     * `COMPANY_NAME`
     * `LEDGER_CONN`
   * **advance_configs.env**
     * Directories (`ANYLOG_PATH`, `LOCAL_SCRIPTS`, `TEST_DIR`) - when deploying AnyLog as executable we recommend setting 
     the path to `~/AnyLog-code` 
     * `DISABLE_CLI` to _true_ if planned to [run in background](/docs/getting-started/07-configure-as-a-service/)
```shell
while IFS= read -r line ; do if [[ $line != \#* ]] && [[ $line != "" ]] && [[ "$line" != '=""' ]] ; then export "${line}" ; fi ; done < ~/AnyLog-code/docker-compose/docker-makefile/master-configs/base_configs.env
while IFS= read -r line ; do if [[ $line != \#* ]] && [[ $line != "" ]] && [[ "$line" != '=""' ]] ; then export "${line}" ; fi ; done < ~/AnyLog-code/docker-compose/docker-makefile/master-configs/advance_configs.env
```

6. Download Deployment scripts
```shell
cd ~/AnyLog-code
git clone <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">https://github.com/AnyLog-co/deployment-scripts</a>
```

7. Start AnyLog
```shell
cd ~/AnyLog-code
chmod -x anylog_v1.3.2404_x86_64
./anylog_v1.3.2404_x86_64 process deployment-scripts/node-deployment/main.al 
```

---
# Configure as Service

The process of deploying AnyLog as a service is built on the information in [Executable Deployment](/docs/getting-started/05-executable-deployment/), which 
explains how to deploy AnyLog executable.

## Prepare Machine for AnyLog as Service 
1. Repeat steps 1-6 in [Executable Deployment](/docs/getting-started/05-executable-deployment/)

2. One of the parameters in the (advance) configuration file is `DISABLE_CLI`, which disables the AnyLog CLI from running.
The parameter is located in the advanced configs of the corresponding node type - example 
[docker-compose/docker-makefile/master-configs/advance_configs.env](https://github.com/AnyLog-co/docker-compose/blob/main/docker-makefile/master-configs/advance_configs.env).

3. Export configuration for the corresponding node type 
```shell
source ~/AnyLog/docker-compose/docker-makefile/master-configs/*.env
```

**Deploying AnyLog in Background**:
```shell
nohup ~/AnyLog-code/anylog_v1.3.2404_x86_64 process deployment-scripts/node-deployment/main.al > /tmp/anylog_output.txt 2>&1 &
```

## AnyLog as a Service
0. Make sure AnyLog is not running in the background 

1. Create service file `/etc/systemd/system/anylog-master.service`
```service
[Unit]
Description=AnyLog Deployment

[Service]
Type=simple
ExecStartPre=/bin/bash -c 'source ~/AnyLog-code/docker-compose/docker-makefile/master-configs/*.env'
ExecStart=/bin/bash -c 'nohup ~/AnyLog-code/anylog_v1.3.2404_x86_64 process deployment-scripts/node-deployment/main.al > /tmp/anylog_output.txt 2>&1'
Restart=on-failure
```

2. Start Service 
```shell
sudo systemctl daemon-reload
sudo systemctl restart anylog.service
```

3. Validate connections via REST
```shell
curl -X GET 127.0.0.1:32049 
```
