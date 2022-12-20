# Cheat Sheet 
## Basic Commands
### Docker
* Starting a container 
```shell 
docker run --network host -it --detach-keys="ctrl-d" --name anylog-node --rm anylogco/anylog-network:develop 

# using docker-compose
cd $HOME/deployments/docker-compose/anylog-rest/ 
docker-compose up -d 
```
* Viewing all containers
```shell
docker ps -a
```
* View volumes
```shell
docker volume ls 
```
* View images 
```shell
docker image ls 
```
* Attaching to a container & Detaching from a container
```shell
# to detach: ctrl-d
docker attach --detach-keys=ctrl-d anylog-node  
```
* Accessing a volume
```shell
# inspect volume to get Mountpoint
docker volume inspect anylog-node_anylog-node-local-scripts 
"""
[
    {
        "CreatedAt": "2022-11-28T17:50:50Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "anylog-operator",
            "com.docker.compose.version": "1.29.2",
            "com.docker.compose.volume": "anylog-operator-node-local-scripts"
        },
        "Mountpoint": "/var/lib/docker/volumes/anylog-node_anylog-node-node-local-scripts/_data",
        "Name": "anylog-operator_anylog-operator-node-local-scripts",
        "Options": null,
        "Scope": "local"
    }
]
"""
 
 # access MountPont - sudo permissions required   
 cd  /var/lib/docker/volumes/anylog-node_anylog-node-node-local-scripts/_data
 
 # view directories / files to changes 
 ls -l 
 
```
* Stopping a container 
```shell
docker stop anylog-node 
```
* Removing an Image
```shell
docker rm anylog-node 
```
* Removing a volume
```shell
docker volume rm anylog-node_anylog-node-local-scripts

# to remove all volumes
echo y | docker volume prune 
```

* A node that was deployed with docker-compose cna be removed using docker-compose as well 
```shell
cd $HOME/deployments/docker-compose/anylog-rest/

# -v will remove volumes associated with the docker-compose
# --rmi all will remove image(s) associated with the docker-compose  
docker-compose down -v --rmi all 
```
### Kubernetes / Helm 
* Starting a container
```shell
git clone https://github.com/AnyLog-co/deployments 
# deploy volume for container 
helm install $HOME/helm/packages/anylog-node-volume-1.22.3.tgz --name-template anylog-node-volume 

# deploy container 
helm install $HOME/helm/packages/anylog-node-1.22.3.tgz --name-template anylog-node
```
* Viewing all services
```shell
# viewing all helm packages deployed 
helm list 

# viewing all Kubernetes instance on default namespace 
kubectl get all 

# viewing all Kubernetes instance
kubectl get all -A 
```
* Attaching to a AnyLog CLI & Detaching from a AnyLog CLI
```shell
# attach to AnyLog CLI -- to detach ctrl-p + ctrl-q
kubecttl attach -it ${POD_NAME}

# attach to docker bash for kubernetes instance 
kubecttl exec -it ${POD_NAME} bash  
```

* Stopping a service - note as long as you don't remove the volume installation data would stay persistent 
```shell
helm delete anylog-node 
```

## Basic AnyLog Commands 
### Validate node is running & check (internal) network communication
* check connections
```anylog
get connections
```
* view processes
```anylog
get processes 
```
* view database open against the given node 
```anylog
get databases 
```
* check local communication
```anylog
test node  
```
* check network communication - node should have access to the blockchain
```anylog
test network 
```
### Blockchain 
* view all policies on blockchain
```anylog
blockchain get * 
```
* get list of all query nodes on blockchain 
```anylog 
blockchain get query 
```
* view information regarding data nodes (operators)
```anylog 
get data nodes 
```

### Other Commands
* list of tables in blockchain 
```shell
# using blockchain command 
blockchain get table bring [table][name] separator=\n

# using get function 
get tables where dbms=* 
```
* query data 
```anylog
run client () sql test format=table "select * from rand_data"
```
