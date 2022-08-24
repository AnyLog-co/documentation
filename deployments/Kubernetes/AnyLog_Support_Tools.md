# Support Tools

## Grafana 
We currently support Grafana version 7.5.7 -- Feel free to visit [Using Grafana](../../northbound%20connectors/using%20grafana.md) 
for support in terms of generating graphs against it. 

### Deployment
1. [Install Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)
```shell
cd deployments/docker-compose/grafana
docker-compose up -d
```
2. Once docker is deployed, the user can access Grafana against port 3000 using the IP of the machine running it. 
Example: [https://${YOUR_LOCAL_IP}:3000]()


3. The default Username and password are: _admin_. Grafana asks the user to change their password when first logging-in


4. Once you're logged, you'll be able to connect to AnyLog using their [JSON data source](https://grafana.com/grafana/plugins/simpod-json-datasource/). 
For more information & support in terms of utilizing Grafana, visit or [Grafana North-bound documentation](../../northbound%20connectors/using%20grafana.md).  

## Remote CLI
Our Remote CLI is an open source web interface used for querying data; it is considered as a "better" alternative (for AnyLog) 
to _Postman_ and _cURL_ as it allows to easily query and manage nodes via web browser. 

### Deployment
1. Install Remote CLI
```shell
cd deployments/docker-compose/remote_cli
docker-compose up -d 
```
2. Once docker is deployed, the user can access the Remote CLI against port 31800 using the IP of the machine running 
it. Example: [https://${YOUR_LOCAL_IP}:31800]()


3. [Query Data](../../northbound%20connectors/remote_cli.md)  

