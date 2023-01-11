# Volumes
Docker volumes are a set of directories that seats on the physical machine and are associated with docker instance(s). 
Kubernetes volumes, are more of an abstract idea as persistent data can be stored either on the machine or cloud (ex. AWS S3). 

AnyLog "requires" storing certain content generated throughout the usage (locally) in order to have a backup for when a 
node (physically) resets, or when migrating data from one machine to another. These include:
* `anylog` directory - which contains authentication keys
* `blockchain` directory - which contains a copy of the blockchain (as JSON file)
* `data` directory - which contains data coming in, as well as the files SQLite database(s) [if created]. 

Our [deployment package](https://github.com/AnyLog-co/deployments) has Kubernetes Helm package for both volume and node
deployment for: 
* AnyLog Node 
* Remote-CLI 
* Postgres
* MongoDB
* Grafana 

## Deployment Process
0. Package both the deployment and volume directories
1. Deploy the volume package 
2. Deploy the deployment package 

As long as the volume package is still running data would be persistent.

## Accessing Volumes

Unlike _Docker_, Kubernetes volumes cannot be accessed via Shell interface; thus an AnyLog instance **must** be running and
associated with the volume(s) in order to access them. 


## Other 
* [Kubernetes Volume Support](https://kubernetes.io/docs/concepts/storage/volumes/)
* The _Docker_ deployment also persists `scripts` directory, which is where the deployment scripts are. However, when 
attempting to persist the directory in Kubernetes we fail as the persistency for "downloaded" files should be done from 
cloud, rather than Docker hub. Steps to resolve the issue could be found here: [Storage Options (Stackoverflow)](https://stackoverflow.com/questions/70895121/how-to-save-data-in-kubernetes-i-have-tried-persistent-volume-but-it-doesnt-so)   
