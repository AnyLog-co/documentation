---
title: Data Persistence
description: AnyLog image and volumes 
layout: page
---

<!---
## Changelog. PUT LATEST CHANGES AT THE TOP PLEASE
-
- 2026-08-07 | Eric Aquaronne | change log format adding ref version | 2.0.2606
    2026-07-25 | Ori Shadmon | Create document
    2026-07-25 | Ori Shadmon | Fixed grammar (subject/verb agreement in the intro, reworded the "Via Executable"
                 intro sentence for clarity). Made the volume table's container paths match the real mount
                 points from docker-compose-template.yaml (added the missing /app/ prefix). Added a Kubernetes
                 equivalent to "Accessing Volumes" — the intro contrasts Docker's concrete volumes against
                 Kubernetes' more abstract model, but the section itself only showed Docker commands. Flagged
                 (not corrected) whether `make exec` is actually a valid target on this Makefile — the
                 confirmed-good "01- Docker.md" shows up/logs/full-test as targets here, but `exec` only
                 appears on the separate docker-compose/support Makefile, which uses SERVICE= instead of
                 ANYLOG_TYPE=. Worth confirming before publishing.
--->

## Persistent Volumes in AnyLog Deployment 
A volume is a directory that sits on the physical machine and is associated with one or more Docker instances.
Kubernetes volumes are more of an abstract concept, since persistent data can live either on the machine or in the
cloud (e.g. AWS S3).

AnyLog "requires" storing certain content generated throughout usage (locally) in order to have a backup for when a 
node (physically) resets, or when migrating data from one machine to another. 

In addition to the built-in directories, the `deployment-scripts` directory is downloaded (via `git clone`) locally and used
to help convert the configurations into actual active services and connected logical databases. 

|              Volume               |     Directory (in container)     |                                                                          Usage                                                                           | 
|:---------------------------------:|:--------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    `${CONTAINER_NAME}-anylog`     |  `/app/AnyLog-Network/anylog/`   |                                                               used for authentication keys                                                               | 
|  `${CONTAINER_NAME}-blockchain`   | `/app/AnyLog-Network/blockchain` |                                           directory that contains a copy of the the blockchain (as JSON) file                                            |
|     `${CONTAINER_NAME}-data`      |    `/app/AnyLog-Network/data`    |          directory that would contain data coming into the node and blob storage (not in database) and  data stored in SQLite database (file).           |
| `${CONTAINER_NAME}-local-scripts` |    `/app/deployment-scripts/`    | A copy of <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">deployment-scripts</a> used to initiate + configure the AnyLog agent |

### Data Directory

The following provides a breakdown of the different directories under ${CONTAINER_NAME}-data

```tree 
/var/lib/docker/volumes/anylog-node-data/_data
├── archive <-- Archive/Backup of data hosted on the node  
│   └── 22 <-- Year of when data came in 
│       └── 06 <-- Month of when data came in 
│          ├── 05 <-- Day of when data came in
│          ├── 06
│          ├── 07
│          ├── 08
│          ├── 09
│          └── 10
├── bkup <-- Data that has been sent to an operator (on publisher node) 
├── dbms <-- directory containing SQLite (non-memory) data 
├── distr <-- That coming in from other operator nodes on the same cluster
├── error <-- Data files that filed to get processed 
├── pem 
├── prep <-- Data being prepared to be stored 
├── rest <-- Data coming in via REST  
├── test <-- Test case 
└── watch <-- Data ready to be stored or sent to other operators
```

### Deployment Scripts

Please visit [deployment-scripts](../../03-%20Training%20&%20Tutorials/05-%20deployment-scripts.md) for more details. 

## Accessing Volumes

### Docker 

1. Get list of all your volumes 
```shell
docker volume ls 
<< COMMENT
DRIVER    VOLUME NAME
local     anylog-node-anylog
local     anylog-node-blockchain
local     anylog-node-data
local     anylog-node-local-scripts
local     postgres_pgdata
<< 
```

2. Using the `inspect` command get the directory path of the volume
```shell
docker volume inspect anylog-node-local-scripts
<< COMMENT
[
    {
        "CreatedAt": "2022-07-04T18:11:50Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/anylog-node-local-scripts/_data",
        "Name": "anylog-node-local-scripts",
        "Options": {},
        "Scope": "local"
    }
]
<< 
```

3. Once you know the _Mountpoint_, you can access the content within that volume. Note - Depending on the permissions, 
you may need to do a `sudo` command.
```shell
sudo tree /var/lib/docker/volumes/anylog-node-local-scripts/_data
<< COMMENT
/var/lib/docker/volumes/anylog-node-local-scripts/_data
├── README.md
├── create_dir_structure.sh
├── deployment_clean.sh
├── deployment_scripts
│   ├── configure_dbms_almgm.al
│   ├── configure_dbms_blockchain.al
│   ├── configure_dbms_operator.al
│   ├── configure_dbms_system_query.al
│   ├── data_partitioning.al
│   ├── declare_cluster.al
│   ├── declare_generic_policy.al
│   ├── declare_k8s_generic_policy.al
│   ├── declare_k8s_operator.al
│   ├── declare_operator.al
│   ├── deploy_operator.al
│   ├── deploy_publisher.al
│   ├── local_script.al
│   ├── mqtt.al
│   ├── network_configs.al
│   ├── pre_deployment.al
│   ├── run_scheduler.al
│   ├── set_params.al
│   └── validate_policy.al
├── sample_code
│   ├── edgex.al
│   ├── fledge.al
│   └── fledge_old.al
└── start_node.al
```

### Kubernetes

Kubernetes volumes are provisioned through a `PersistentVolumeClaim` rather than named directly like Docker
volumes, so the discovery path looks slightly different:

1. List the persistent volume claims to find the one backing your node:
```shell
kubectl get pvc
```

2. Get the underlying `PersistentVolume` and its actual storage location — this varies by provisioner (local disk,
   NFS, cloud block storage, etc.), so the exact path/endpoint shown will depend on your cluster:
```shell
kubectl describe pv <persistent-volume-name>
```

3. If your provisioner backs onto a local or NFS path reachable from a node, you can inspect it directly the same
   way as the Docker `tree` example above. If it's cloud-backed (e.g. an EBS volume or S3 bucket), use that
   provider's own tooling instead — there's no local filesystem path to `tree` into.

> **To verify:** the exact `kubectl` workflow above depends on how AnyLog's Helm charts provision storage
> (StorageClass, provisioner, etc.) — worth confirming against the actual Kubernetes deployment docs rather than
> treating this as authoritative.

### Via Executable

Docker lets you access a volume's files directly from the host filesystem, as shown above. With Kubernetes — and
often with Docker too, for convenience — it's simpler to just exec into the running container instead.

1. Attach to the executable 

```shell
cd docker-compose
make exec ANYLOG_TYPE=[AnyLog agent type]
```

> **To verify:** whether `exec` is actually a valid target on this Makefile. The confirmed-current deployment
> guide ("01- Docker.md") lists `up`, `logs`, and `full-test` as targets here — `exec` (with `SERVICE=`, not
> `ANYLOG_TYPE=`) only appears on the separate `docker-compose/support` Makefile. If this Makefile doesn't
> actually have an `exec` target, the equivalent is likely `bash deploy.sh exec --type [AnyLog agent type]`,
> following the same `make`/`deploy.sh` pattern used throughout "01- Docker.md."

2. Install vim - by default we do not install vi / vim

```shell
apt-get -y update && apt-get -y install vim
```

3. cd into deployment-scripts

```shell
cd /app/deployment-scripts  
```

4. using `vim` update the scripts as needed