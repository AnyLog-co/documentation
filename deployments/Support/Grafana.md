# Grafana 

Grafana is an open-source BI tool managed by [Grafana Labs](https://grafana.com/). We utilize to demonstrate data coming 
into AnyLog via a common graphical interface. Our [Northbound Connectors](../../northbound%20connectors/using%20grafana.md)
has directions for how to generate  graphs with data coming in via AnyLog. 

* [Support](https://grafana.com/docs/grafana/latest/)

## Deployment
### Deploying Grafana via Docker
1. Clone deployments directory & cd into Grafana directory
```shell
git clone https://github.com/AnyLog-co/deployments
cd $HOME/deployments/docker-compose/grafana/
```
2. Update Configurations
```shell
vim grafana.env
```
3. Deploy Grafana 
```shell
docker-compose up -d
``` 

### Deploying Grafana via Kubernetes
1. Clone deployments directory
```shell
git clone https://github.com/AnyLog-co/deployments
```

2. Update Configurations
```shell
# volume configurations
vim $HOME/deployments/helm/sample-configurations/grafana_volume.yaml

# deployment configurations 
vim $HOME/deployments/helm/sample-configurations/grafana.yaml
```

3. Deploy Volume -- as long as volume exists on the node, data will be persistent
```shell
helm install $HOME/deployments/helm/packages/grafana-volume-7.5.7.tgz --name-template grafana-vol --values $HOME/deployments/helm/sample-configurations/grafana_volume.yaml
```

3. Deploy Instance
```shell
helm install $HOME/deployments/helm/packages/grafana-7.5.7.tgz --name-template grafana --values $HOME/deployments/helm/sample-configurations/grafana.yaml
```

### Install Grafana Locally
To Install Grafana OSS locally, please follow the directions on their [website](https://grafana.com/grafana/download?edition=oss)

## Configure Grafana 
To access Grafana the default URL is [http://${YOUR_LOCAL_IP}:3000]()

1. The default Username and password are: _admin_. Grafana asks the user to change their password when first logging-in

2. Once you're logged, you'll be able to connect to AnyLog using their [JSON data source](https://grafana.com/grafana/plugins/simpod-json-datasource/). 

3. For more information & support in terms of utilizing Grafana, visit or [Grafana North-bound documentation](../../northbound%20connectors/using%20grafana.md)