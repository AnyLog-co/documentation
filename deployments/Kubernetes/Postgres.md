# PostgreSQL
On machines that will use PostgreSQL - make sure PostgreSQL is installed and accessible. Our deployments package 
provides a docker deployment for PostgreSQL - alternatively a user can deploy / use their own PostgreSQL database. If 
you'd like to install PostgreSQL locally, rather than via Docker feel free to utilize the following documentation: 
* [Install PostgreSQL as a Service](https://www.postgresql.org/download/)
* [Configure PostgreSQL for Remote Access](https://www.linode.com/docs/guides/configure-postgresql/)

1. Update the Postgres volume configurations in `deployments/configurations/helm/postgres_volume.yaml` as you see fit 
```yaml
# deployments/configurations/helm/postgres_volume.yaml 
general:
 namespace: default
 volume_name: postgres-pv
 # nodeSelector - Allows running Kubernetes remotely. If commented out, code will ignore it
 #nodeSelector: ""

spec:
 storage_class: manual
 access_mode: ReadWriteMany
 storage_size: 5Gi
 reclaim_policy: Retain
 host_path: /opt/postgres-data
```

2. Update Postgres deployment configurations in `deployments/configurations/helm/postgres_volume.yaml` as you see fit
```yaml
# deployments/configurations/helm/postgres.yaml 
general:
 namespace: default
 app_name: postgres
 deployment_name: postgres-app
 service_name: postgres-svs
 configmap_name: postgres-configs
 volume_name: postgres-pv
 enable_volume: true
 # nodeSelector - Allows running Kubernetes remotely. If commented out, code will ignore it
 #nodeSelector: ""
 replicas: 1

image:
 repository: postgres
 tag: 14.0-alpine
 pullPolicy: IfNotPresent

networking:
 port_name: psql-port
 port: 5432

credentials:
 username: admin
 password: demo
```

3. Start Postgres  – this needs to be done on nodes that are using Postgres 
```shell
# Deploy Volume for PostgreSQL  
helm install ~/deployments/packages/postgres-volume-14.0-alpine.tgz --values ~/deployments/configurations/helm/postgres_volume.yaml --name-template postgres-volume 

# Deploy actual PostgreSQL node 
helm install ~/deployments/packages/postgres-14.0-alpine.tgz --values ~/deployments/configurations/helm/postgres.yaml --name-template postgres
```
Disclaimer - As long as the user does not remove the postgres volume package from the machine (`helm delete`) the data
will be persistent. 

4. Accessing Postgres CLI  
```shell
# get pod name 
kubectl get pod

<< comment 
NAME                                   READY   STATUS    RESTARTS   AGE
postgres-app-b6656d6df-wklms           1/1     Running   0          29m
>>


# access Postgres instance 
kubectl exec -it pod/postgres-app-b6656d6df-wklms -- psql -h 127.0.0.1 -p 5432 -U
```
