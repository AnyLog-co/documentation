# Remote-CLI
AnyLog's Remote-CLI is an open-source web interface for executing REST request(s) against the network. 

## Deployment
### Deploying Remote-CLI via Docker
1. Clone deployments directory & cd into Remote-CLI directory
```shell
git clone https://github.com/AnyLog-co/deployments
cd $HOME/deployments/docker-compose/remote-cli/
```
2. Update Configurations
```shell
vim .env
```
3. Deploy Remote-CLI 
```shell
docker-compose up -d
``` 

### Deploying Remote-CLI via Kubernetes
1. Clone deployments directory
```shell
git clone https://github.com/AnyLog-co/deployments
```

2. Update Configurations
```shell
# volume configurations
vim $HOME/deployments/helm/sample-configurations/remote_cli_volume.yaml

# deployment configurations 
vim $HOME/deployments/helm/sample-configurations/remote_cli.yaml
```

3. Deploy Volume -- as long as volume exists on the node, data will be persistent
```shell
helm install $HOME/deployments/helm/packages/remote-cli-volume-1.0.0.tgz --name-template remote-cli-vol --values $HOME/deployments/helm/sample-configurations/remote_cli_volume.yaml
```

3. Deploy Instance
```shell
helm install $HOME/deployments/helm/packages/remote-cli-1.0.0.tgz --name-template remote-cli --values $HOME/deployments/helm/sample-configurations/remote_cli.yaml
```

## Using Remote-CLI
To access Remote-CLI the default URL is [http://${YOUR_LOCAL_IP}:31800]()

* The default options shown are set in the [commands.json]() to access this data: 
  
    **On Docker**: 
  1. Get the volume path for `remote-cli` -- `docker volume inspect remote-cli`
  2. cd into relevant path 
  3. using `sudo` command vim into `commands.json` file 
  4. make desired changes & save
  5. If updates don't appear on your instance (automatically) then restart remote-cli -- `docker restart remote-clie` 

    **On Kubernetes**
  1. Attach into the active pod -- `kubectl exec -it ${REMOTE_CLI_POD_NAME} bash`
  2. cd in Remote-CLI (anylog_query/static/json/)
  3. vim into `commands.json`
  4. save 
  5. detach from pod - `ctrl-p` + `ctrl-q` 
  6. Updates should appear on your instance 

  
When using _Kubernetes_, changes done in `commands.json` will not be persistent due to the way [Kubernetes volumes](../Networking%20&%20Security/kubernetes_volumes.md) 
work. 

* Examples of using Remote-CLI can be found in our [northbound connectors](../../northbound%20connectors/remote_cli.md) section