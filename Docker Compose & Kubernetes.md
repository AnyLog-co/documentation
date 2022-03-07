# Deployment of Docker Compose & Kubernetes

## Docker Compose 
The [AnyLog docker-compose](https://github.com/AnyLog-co/docker-compose) provides support for deploying AnyLog using 
docker-compose. There are 2 docker-compose files, one for `python:3.9-alpine` deployment and another for `Ubuntu:20.04` 
based. Both docker-compose files contains deployment for:

**Required Deployments**
* AnyLog-Network
* Postgres v14-alpine

**Optional Deployments**
* Remote-CLI
* [AnyLog GUI](using%20the%20gui.md)
* Grafana v7.5.7 

### Deployment Process
0. [Install docker and docker-compose](https://docs.docker.com/engine/install/)
1. Select the docker-compose file and copy it into `docker-compose.yml`
2. Configure `docker-compose.yml` with the proper IPs, ports and credentials specifically for your deployment
3. Deploy docker-compose file
```commandline
docker-compose up -d 
```
4. To access to one of the docker processes: 
```commandline
docker attach --detach-keys="ctrl-d" ${CONTAINER_NAME} 
```

5. To stop containers via `docker-compose`
```commandline
docker-compose down 
```

## Kubernetes
AnyLog's kubernetes deployment has been tested using [minikube](https://minikube.sigs.k8s.io/docs/), and thus the steps are based on it.

### Requirements
* [docker-compose](Docker%20Compose%20&%20Kubernetes.md#docker-compose)
* [kompose](https://kompose.io/installation/) - A conversion tool for Docker Compose to container orchestrators such as Kubernetes (or OpenShift).
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) - Kubernetes command line tool
* [minikube](https://minikube.sigs.k8s.io/docs/start/) - local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.

### Deployment
1. Start minikube & Evaluate 
```commandline
minikube start --insecure-registry="${LOCAL_IP}:5000"
eval $(minikube docker-env)
```

2. Convert `docker-compose` file into Kubernetes
```commandline
mkdir $HOME/kube
cd $HOME/kube
kompose convert -f ${DOCKER_COMPOSE_PATH}
```

3. Deploy process
```commandline
kubectl apply -f $HOME/kube
```

4. Update anylog-node service to support remote access 
```commandline
kubectl edit service ${anylog-node-process-name}
```

5. Replace `ClusterIP` to `NodePort`
```commandline
# before 
  ports:
  - name: "13480"
    nodePort: 31266
    port: 13480
    protocol: TCP
    targetPort: 13480
  - name: "13481"
    nodePort: 31956
    port: 13481
    protocol: TCP
    targetPort: 13481
  - name: "13482"
    nodePort: 31296
    port: 13482
    protocol: TCP
    targetPort: 13482
  selector:
    io.kompose.service: ${SERVICE_NAME}
  sessionAffinity: None
  type: ClusterIP

# after 
  ports:
  - name: "13480"
    nodePort: 31266
    port: 13480
    protocol: TCP
    targetPort: 13480
  - name: "13481"
    nodePort: 31956
    port: 13481
    protocol: TCP
    targetPort: 13481
  - name: "13482"
    nodePort: 31296
    port: 13482
    protocol: TCP
    targetPort: 13482
  selector:
    io.kompose.service: ${SERVICE_NAME}
  sessionAffinity: None
  type: NodePort
```

6. Generate `IP:PORT` to execute against
```commandline
 minikube service --url ${SERVICE_NAME}
```

7. For AnyLog-GUI, Remote-CLI, Grafana and Postgres (optional) configure port-forwarding
```commandline
kubectl port-forward --address=${LOCAL_IP} service/${SERVICE_NAME} ${LOCAL_PORT}:${REMOTE_PORT}
```
