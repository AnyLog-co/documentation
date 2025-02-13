# Updating Scripts

AnyLog is configured using the AnyLog commands. These commands can be issued on the AnyLog CLI, or organized in script 
files that can either be standalone or part of something called [configuration policies](../policies.md#configuration-policies).

These scripts configure an empty AnyLog instance to do everything from setting configuring the node and declaring its 
policies on the network, to more personalized things such as connecting to north and south-bound services. 
 
By default, when a node is deployed it uses the scripts located in <a href="https://github.com/AnyLog-co/deploymnet-scripts" target="_blank">deployment-scripts</a>.
However, there are situations where users may want to utlize their own script(s). 

## Extending deployment-scripts

When running with default scripts, the process is as follows: 
1. Based on user-defined environment variables, set the AnyLog dictionary 
2. Declare network configuration
3. pull a copy of the blockchain from ledger
4. declare a configuration policy
5. connect to database and add blockchin sync service
6. declare node specific policies 
7. configure node (type) specific services
8. If enabled, run support services
   * MQTT 
   * monitoring
   * personalized scripts

Within deployment-scripts --> node-deployment there's an empty file called `local_script.al`, this can be used for 
creating a personalized script to be run as part of future deployment. 

Since the file resides within the persistent data volumes it can be updated in 2 ways: 
* Using the exec command 
* Accessing the volume itself.

### Using Exec command
1. Access the Kubernetes deployment bash interface  
```shell
# for docker 
docker exec -it ${NODE_NAME} /bin/bash

# for Kubernetes 
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



 

### Accessing the volume
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

