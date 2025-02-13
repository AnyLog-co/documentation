# Configure as Service

The process of deploying AnyLog as a service is built on the information in [Executable.md](Executable.md), which 
explains how to deploy AnyLog executable. 

## Prepare Machine for AnyLog as Servie 
1. Repeat steps 1-6 in [Executable.md](Executable.md)
 
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

## AnyLog as aa Service
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



