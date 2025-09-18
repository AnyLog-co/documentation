# Monitoring Containers

## Docker & Podman through AnyLog / EdgeLake

Monitoring Docker nodes is pretty straight forward, as it only requires referencing the `docker.socket` path in the 
Docker Compose configuration.

### Requirements 

Docker server rather than Docker desktop as it's using `docker.socket`

### Steps 
1. Locate `docker.socket` path 
2. Create logical database called `monitoring` with an optional partitioning 

**SQLlite**: 
```anylog 
connect dbms monitoring where type=sqlite 
set partition monitoring * using insert_timestamp by 12 hours
<schedule time="1 day" and name="Drop monitoring partitions" task 
    drop partition where dbms=monitoring and table=* and keep=3> 
```

**PostgresSQL**: 
```anylog 
<connect dbms monitoring where 
    type=psql and 
    ip=127.0.0.1 and 
    port=54332 and 
    user=[DB user] and 
    password=[DB password]> 
set partition monitoring * using insert_timestamp by 12 hours
<schedule time="1 day" and name="Drop monitoring partitions" task 
    drop partition where dbms=monitoring and table=* and keep=3> 
```

2. Using `scheduled pull` function gather pull 
```anylog
<run scheduled pull
  where name = docker_insights
  and type = docker
  and frequency = 5
  and continuous = true
  and dbms = monitoring
  and table = docker_insight>
```

## Kubernetes with KubeArmor
KubeArmor is a runtime security enforcement tool for Kubernetes that protects containers and workloads at the operating 
system (OS) level. It monitors and enforces security policies in real time, helping prevent malicious or unintended 
behavior inside containers.

1. **Behavioral Runtime Protection** – Observes system calls and kernel-level events (such as file access, network 
connections, and process executions) from containers.
2. **Policy Enforcement** – Enforces pre-defined security policies to control what containers are allowed to do.
3. **Auditing and Visibility** – Provides logs and alerts for any policy violations.
4. **Security-focused Container Monitoring** – KubeArmor does not monitor traditional metrics like CPU or disk I/O. 
Instead, it focuses on runtime[monitoring_container.md](monitoring_container.md) security, detecting and logging policy violations in real time.

Using [gRPC](../southbound-services/using_grpc.md) users can gather information generated through KubeArmor and store it on their respected operator nodes. 
This allows to view (Kubernetes) container insights in a decentralized manner. 

### Steps
1. Directions to start KubeArmor can be found in <a href="https://docs.kubearmor.io/kubearmor/quick-links/deployment_guide" target="_blank">their documentation</a> 

2. Access the AnyLog / EdgeLake container executable  
```shell
# Docker 
docker exec -it my-operator /bin/sh 

# Kubernetes 
kubectl exec -it my-operator -- /bin/bash
```

3. Compile the protocol file 
```shell
python3 /app/deployment-scripts/gRPC/compile.py /app/deployment-scripts/gRPC/kubearmor/kubearmor.proto
```

4. In [deployment-scripts/gRPC/kubearmor/deploy_kubearmor_system.al]() assert the following configs are corrrect:
* `grpc_client_ip`
* `grpc_client_port`


3. Attach to the Docker / Kubernetes container
```shell
# Docker 
docker attach --detach-keys=ctrl-d my-operator 

# Kubernetes (ctrl-pq to detach) 
kubectl attach -it pod/anylog-master-deployment-7b4ff75fb7-mnsxf 
```

5. Execute gRPC client 
```anylog
process !anylog_path/deployment-scripts/grpc/kubearmor/deploy_kubearmor_system.al
```

6. To view data as they come into the node
```anylog
get grpc client 
get streaming
```

