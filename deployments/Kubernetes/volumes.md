# Volumes
Docker volumes are really a directory that seats on the physical machine and is associated with the docker instance(s). 
While Kubernetes volumes are more of an abstract idea, where (persistent) data can be stored either on the local machine, 
or cloud (ex. AWS S3) and get associated with a Kubernetes deployment (pod). 

AnyLog "requires" storing certain content generated throughout the usage locally, in order to have a backup for when a 
node (physically) resets, or when migrating data from one machine to another. These include:
* `anylog` directory - which contains authentication keys
* `blockchain` directory - which contains a copy of the blockchain (as JSON file)
* `data` directory - which contains data coming in, as well as the files SQLite database(s) [if created]. 

Our [deployment package](https://github.com/AnyLog-co/deployments) has Kubernetes Helm package for both volume and node
deployment for: 
* AnyLog Node 
* Remote-CLI 
* Postgres 
* Grafana 

## Deployment Process
0. Package both the deployment and volume directories
1. Deploy the volume package 
2. Deploy the deployment package 

As long as the volume package is still running data would be persistent.

## Other 
* [Kubernetes Volume Support](https://kubernetes.io/docs/concepts/storage/volumes/)
* The _Docker_ deployment also persists `scripts` directory, which is where the deployment scripts are. However, when 
attempting to persist the directory in Kubernetes we fail as the persistency for "downloaded" files should be done from 
cloud, rather than Docker hub. Steps to resolve the issue could be found here: [Storage Options (Stackoverflow)](https://stackoverflow.com/questions/70895121/how-to-save-data-in-kubernetes-i-have-tried-persistent-volume-but-it-doesnt-so)   