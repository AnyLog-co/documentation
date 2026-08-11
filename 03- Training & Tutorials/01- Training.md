---
title: "Training & Tutorials"
description: "A quick run through of the training for AnyLog"
layout: page
source_path: "training/01- Training.md"
---

The <a href="../02-%20Installation%20&%20Deployment" target="_blank">previous section</a> covered the different ways a user can download and
install AnyLog — whether via Docker / Kubernetes, directly on the machine, via pip or as a service, or using an
orchestration tool like IBM's Open Horizon or ZEDEDA.

This section covers what happens once the AnyLog agent(s) is installed and running.

## What's in This Section

* <a href="02-%20Basic%20Commands.md" target="_blank">Basic commands</a>
* <a href="03-%20Query%20Data.md" target="_blank">Query Data</a>
* <a href="04-%20deployment-process.md" target="_blank">Deployment Process</a>
* <a href="05-%20deployment-scripts.md" target="_blank">Deployment Scripts</a>
* <a href="06-%20Nodes.md" target="_blank">Node Configuration Process</a>
* <a href="../13-%20Support%20&%20Troubleshooting/04-%20Third-Party%20Support/01-%20Docker%20&%20K8s%20Commands.md" target="_blank">Basic Docker / K8s Commands</a>

<a href="../12-%20Examples%20&%20Use%20Cases" target="_blank">Section 12</a> provides full examples for deploying a local / demo network from start to finish.

## The Process

Recap of the previous section:

1. `git clone` the docker-compose repo (or another repo that eases the deployment of AnyLog).
2. Update the configuration files in the dotenv. There's a unique dotenv file per AnyLog node type.
3. Start the AnyLog agent.

Once a user executes `make up` on an AnyLog agent, the following steps occur:

1. A process (`docker_compose_builder.sh`) takes the different parts of the dotenv configuration and the relative
   path of the configuration file to generate a `docker-compose.yml`:
   * Container name — same as `NODE_NAME` if provided, else the directory name is used as the container name.
   * Container volumes are created if they don't already exist.
   * Networking is configured based on user input, falling back to the operating system's defaults if no input is
     provided.
2. `docker compose up` is executed.
3. The deployment-scripts repo is downloaded if needed, or reused if it already exists (see the
   <a href="./04-%20deployment-process.md" target="_blank">deployment scripts deep dive</a> for the different sourcing strategies).
4. The AnyLog agent starts inside the docker container.

What happens inside AnyLog:

1. Deployment-scripts shell environment parameters are converted into AnyLog params (e.g. `$NODE_NAME` → `!node_name`).
2. Based on the node type, a configuration policy is created if one does not already exist.
3. The configuration policy is deployed:
   1. Network connectivity is defined.
   2. The node policy is defined (if it does not already exist).
   3. Connections to databases are established as needed.
   4. Connections to services such as `blockchain sync` and `run operator` are established, based on the AnyLog
      agent type.

Once that's done, the agent can work independently with the rest of the members in the network.