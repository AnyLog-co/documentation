# Executing Script
By default, AnyLog provides a series of scripts which help set up a given node. The scripts include things like setting 
environment variables, network and database configurations, declaring policies to the blockchain and scheduling a sync
time against the blockchain (or master node). 

With that in mind, users may want to deploy their own scripts, in addition to the default scripts; these scripts can
be things like - complex MQTT client requests, scheduled processes to check disk space or executing a query every so 
often. These scripts can be added in the [local scripts volume](volumes.md). 

## Creating Personalized Script
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

4. Either create a new script, or utilize the existing `local_script.al` file to write the your personalized script. 
When setting the `Enable Local Script` configuration to **true**, the default deployment process will automatically run
`local_script.al` when starting. 
```shell 
sudo vim /var/lib/docker/volumes/anylog-node-local-scripts/_data/deployment_scripts/local_script.al
```

5. Once the personalized script has been created, you can manually run it by executing `process` command.
```shell
AL anylog-node > process !local_scripts/deployment_scripts/local_script.al
```

## Sample Local Scripts
In addition to the _default_ deployment scripts, the `sample_code` directory provides examples of utilizing MQTT client
with either blockchain policies and / or multiple topics within the same call. 
