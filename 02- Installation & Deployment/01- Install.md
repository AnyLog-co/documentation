---
title: Installation Overview
description: How to install AnyLog — choose a deployment method (virtualization, orchestrator, or bare metal), review prerequisites, and understand the general install flow before diving into a specific guide.
layout: page
---
<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
- 2026-08-07 | Eric Aquaronne | change log format | 2.0.2606 
| 2026-07-24 | Ori Shadmon | Create introduction document |
--->

# Installing AnyLog

The following provides directions on how to install AnyLog — whether through an orchestration tool, via
virtualization, or directly on bare metal.

Please review the <a href="../01-%20Getting%20Started/02-%20Prerequisite.md" target="_blank">prerequisites</a> before getting started.

* <a href="02-%20Virtualization/01-%20Docker.md" target="_blank">Docker / Podman</a>
* <a href="02-%20Virtualization/02-%20Installing%20the%20VM%20OVA.md" target="_blank">VirtualBox - OVA</a>
* <a href="02-%20Virtualization/03-%20Kubernetes.md" target="_blank">Kubernetes</a>
* <a href="03-%20Orchestrators/01-%20Open%20Horizon.md" target="_blank">IBM's Open Horizon</a>

## General Directions

1. Install prerequisites — e.g. `git`, Docker, VirtualBox, etc.
2. Download the appropriate repo with configuration support.
3. <a href="https://anylog.network/downloads" target="_blank">Request a license</a>.
4. Update the configuration files.
5. Deploy the AnyLog agent(s).