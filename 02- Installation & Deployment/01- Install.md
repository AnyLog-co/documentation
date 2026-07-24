---
title: Installation Overview
description: How to install AnyLog — choose a deployment method (virtualization, orchestrator, or bare metal), review prerequisites, and understand the general install flow before diving into a specific guide.
layout: page
---
<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
| 2026-07-24 | Ori Shadmon | Create introduction document |
--->

# Installing AnyLog

The following provides directions on how to install AnyLog — whether through an orchestration tool, via
virtualization, or directly on bare metal.

Please review the [prerequisites](../01-%20Getting%20Started/02-%20Prerequisite.md) before getting started.

* [Docker / Podman](02-%20Virtualization/01-%20Docker.md)
* [VirtualBox - OVA](02-%20Virtualization/02-%20Installing%20the%20VM%20OVA.md)
* [Kubernetes](02-%20Virtualization/03-%20Kubernetes.md)
* [IBM's Open Horizon](03-%20Orchestrators/01-%20Open%20Horizon.md)


## General Directions

1. Install prerequisites — e.g. `git`, Docker, VirtualBox, etc.
2. Download the appropriate repo with configuration support.
3. <a href="https://anylog.network/downloads" target="_blank">Request a license</a>.
4. Update the configuration files.
5. Deploy the AnyLog agent(s).