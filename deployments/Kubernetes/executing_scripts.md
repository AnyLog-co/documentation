# Executing Script
By default, AnyLog provides a series of scripts which help set up a given node. The scripts include things like setting 
environment variables, network and database configurations, declaring policies to the blockchain and scheduling a sync
time against the blockchain (or master node). 

With that in mind, users may want to deploy their own scripts, in addition to the default scripts; these scripts can
be things like - complex MQTT client requests, scheduled processes to check disk space or executing a query every so 
often. When using Kubernetes, as long as the [persistent volumes](volumes.md) are accessible to the deployment, these
scripts will continue to exist. 

## Creating Personalized Script
1. Access the Kubernetes deployment bash interface  
```shell
kubectl exec -it pod/${DEPLOYMENT_POD_NAME} bash
```

**The following commands are within the Pod** 

2. cd into scripts directory - this is the `!loca_scripts` variable in AnyLog 
```shell 
cd AnyLog-Network/scripts/
```

3. Either create a new script, or utilize the existing `local_script.al` file to write the your personalized script. 
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

**The following commands are done within AnyLog**
4. Once the personalized script has been created, you can manually run it by executing `process` command.
```shell
AL anylog-node > process !local_scripts/deployment_scripts/local_script.al
```

## Sample Local Scripts
In addition to the _default_ deployment scripts, the `sample_code` directory provides examples of utilizing MQTT client
with either blockchain policies and / or multiple topics within the same call. 
