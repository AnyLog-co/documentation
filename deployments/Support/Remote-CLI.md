# Remote-CLI
AnyLog's Remote-CLI is an open-source web interface for executing REST request(s) against the network. 

## Deployment
To deploy our [Remote-CLI](https://github.com/AnyLog-co/Remote-CLI), users need to have the following installed. This is all done automatically when running via 
Docker or Kubernetes.
* django 
* requests 
* pyqrcode[pi]
* pypng

1. Clone deployments directory 
```shell
git clone https://github.com/AnyLog-co/deployments

# for a docker based deployment you need to be inside the Remote-CLI directory
cd $HOME/deployments/docker-compose/remote-cli/
```

2. Update configurations 
```shell
# for docker update the .env file 
vim .env

# for kubernetes update the Remote-CLI configuration file
$HOME/deployments/helm/sample-configurations/remote_cli.yaml
```
3. Deploy Remote-CLI
```shell
# for docker 
docker-compose up -d

# for kubernetes 
helm install $HOME/deployments/helm/packages/remote-cli-volume-1.0.0.tgz --name-template remote-cli-vol --values $HOME/deployments/helm/sample-configurations/remote_cli.yaml
helm install $HOME/deployments/helm/packages/remote-cli-1.0.0.tgz --name-template remote-cli --values $HOME/deployments/helm/sample-configurations/remote_cli.yaml
``` 

## Using Remote-CLI
To access Remote-CLI the default URL is [http://${YOUR_LOCAL_IP}:31800]()

Directions for using the Remote-CLI can be found [here](../../northbound%20connectors/remote_cli.md)

### Updating Command Options
The default command options can be found under [djangoProject/static/json/commands.json](https://github.com/AnyLog-co/Remote-CLI/blob/master/djangoProject/static/json/commands.json)
in the Remote-CLI folder.

1. Access folder
```shell
# Docker volume 
docker inspect remote-cli
<< COMMENT 
[
    {
        "CreatedAt": "2023-05-18T19:51:36Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "remote-cli",
            "com.docker.compose.version": "1.25.0",
            "com.docker.compose.volume": "remote-cli"
        },
        "Mountpoint": "/var/lib/docker/volumes/remote-cli/_data",
        "Name": "remote-cli",
        "Options": null,
        "Scope": "local"
    }
]
>> 
sudo ls ls /var/lib/docker/volumes/remote-cli_remote-cli/_data

# Kubernetes Volume
kubectl exec -it ${REMOTE_CLI_POD_NAME} bash
ls /app/Remote-CLI/djangoProject/static/json/
```
2. Update [commands.json](https://github.com/AnyLog-co/Remote-CLI/blob/master/djangoProject/static/json/commands.json) with the new params. 
Example of Remote-CLI button as a JSON object
   * Button - button name 
   * command - command to execute 
   * type - whether the command is _GET_, _PUT_ or _POST_
   * group - section where the command falls under
   * help_url - path for more information. The provided content is added to https://github.com/AnyLog-co/documentation/
```json
{
  "button": "Fleet CMD Sum",
  "command": "sql nvidia format=table \"select component, release, system, version,  helm_release, info, count(*) as num_info from  fleet_command WHERE period(day, 1, '2022-05-29 23:46:33.176572476', timestamp) GROUP by component, release, system, version,  helm_release, info ORDER BY info;\"",
  "type": "GET",
  "group": "Demo",
  "help_info": "blob/master/sql%20setup.md"
}
```

3. Restart Remote-CLI 
