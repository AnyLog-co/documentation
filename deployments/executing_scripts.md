# Executing Script

AnyLog is configured using the AnyLog commands. These commands can be issued on the AnyLog CLI, or organized in script 
files or within policies that are hosted on a ledger.
AnyLog provides a series of default scripts which help set up a given node. 
Using these scripts, users can configure and set environment variables, network and database configurations, 
declare policies that are stored on a ledger, scheduling a sync time against the blockchain (or a master node), 
apply mapping on data published on a node, scheduled processes to check disk space, execute a scheduled query and more.   

These scripts can be added in the local scripts' volume or added to the ledger using 
[configuration policies](../policies.md#configuration-policies) or using a combination of both.

The example below details deployment using Docker or Kubernetes.

## Creating Personalized Script on Docker
1. Get list of all your volumes
```shell
docker volume ls 
```

2. Using the `inspect` command get the directory path of the volume
```shell 
docker volume inspect ${VOLUME_NAME}
```

3. Once you know the _Mountpoint_, you can access the content within that volume. Depending on the permissions, 
you may need to do a `sudo` command in order to access content on said volume.

Sample mountpoint Path: 
```shell
/var/lib/docker/volumes/anylog-node-local-scripts/_data/deployment_scripts/local_script.al
```

4. Either create a new script, or utilize the existing `local_script.al` file to write your personalized script. 
When setting the `Enable Local Script` configuration to **true**, the default deployment process will automatically run
`local_script.al` when starting. 
```shell 
sudo vim /var/lib/docker/volumes/anylog-node-local-scripts/_data/deployment_scripts/local_script.al
```

5. Once the personalized script has been created, you can manually run it by executing `process` command.
```shell
AL anylog-node > process !local_scripts/deployment_scripts/local_script.al
```

## Creating Personalized Script on Kubernetes
1. Access the Kubernetes deployment bash interface  
```shell
kubectl exec -it pod/${DEPLOYMENT_POD_NAME} bash
```

2. cd into scripts directory - this is the `!loca_scripts` variable in AnyLog 
```shell 
cd AnyLog-Network/scripts/
```

3. Either create a new script, or utilize the existing `local_script.al` file to write your personalized script. 
When setting the `Enable Local Script` configuration to **true**, the default deployment process will automatically run
`local_script.al` when starting.
```shell
vim deployment_scripts/local_scripts.al 
```

If _vim_ or other text editor program does not work, users can easily install it. 
```shell
# Debian / Ubuntu 
apt-get -y install vim 

# Alpine 
apk add vim 

# Redhat / CentOS
yum -y install vim
```

4. Once the personalized script has been created, detach from the bash interface and reattach to the AnyLog console. 
```shell
# detach: ctrl-p +ctrl-pq 
kubectl attach -it pod/${DEPLOYMENT_POD_NAME}
```

5. Once the personalized script has been created, you can manually run it by executing `process` command.
```anylog 
AL anylog-node > process !local_scripts/deployment_scripts/local_script.al
```


## Sample Local Scripts
In addition to the _default_ deployment scripts, the `sample_code` directory provides examples of utilizing MQTT client
with either blockchain policies and / or multiple topics within the same call. 

```anylog
# Shorthand
AL anylog-node >  ls !local_scripts/sample_code

# Full path 
AL anylog-node > ls /app/AnyLog-Network/scripts/sample_code 
```
