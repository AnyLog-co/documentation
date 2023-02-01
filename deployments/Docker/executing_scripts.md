## Executing Script
Scripts get executed using the `process` command followed by the path and file name. 

For example, the command below execute a script referenced by the path and file name. 
```
process !anylog_path/AnyLog-Network/demo/ha_operator1.al
```
In the example above, the path is prefixed by ```!anylog_path```. Therefore, anylog_path is treated as a key, which replaced 
by the value of the key in the node.  
The [Node Dictionary](../../getting%20started.md#the-node-dictionary) section explains how values are assigned to keys.  
Use the [get dictionary](../../monitoring%20nodes.md#the-get-dictionary-command) command to view the values assigned to keys.

This example below detail the process to executes the script `sample_code/edegex.al` in a docker deployment:

1. Using the `inspect` command get the path for anylog-node-local-scripts
```shell
docker volume inspect anylog-node-local-scripts
```

2. Based on the _Mountpoint_ copy `sample_code/edgex.al` into `deployment_scripts/local_script.al`
    * Feel free to `vim` into either file to see their content, or develop your own (local) deployment script
```shell
sudo cp /var/lib/docker/volumes/anylog-node-local-scripts/_data/sample_code/edgex.al /var/lib/docker/volumes/anylog-node-local-scripts/_data/deployment_scripts/local_script.al 
```

3. attach to the node 
```shell
docker attach --detach-keys="ctrl-d" anylog-node 

# to detach press ctrl-d
```

4. Within AnyLog CLI execute the new local script. 
```shell
AL anylog-node > process !local_scripts/local_script.al  
```

5. Once the script is done you should be able to see the following changes:
    1. New policies added to the blockchain -- `blockchain get *`
    2. Data coming in to MQTT client -- `get msg client`
   

6. Detach from docker container -- `ctrl-d`


7. Update the .env file to have `DEPLOY_LOCAL_SCRIPT=true` instead of `DEPLOY_LOCAL_SCRIPT=false` so that the local 
script will be deployed each time the node starts up. 
