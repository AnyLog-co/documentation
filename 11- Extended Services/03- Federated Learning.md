---
title: "Federated Learning: Example & Explained"
description: A structured explainer covering what federated learning is, why it's hard to deploy, how AnyLog automate it, and a worked hospital-HVAC example.
layout: page
---

<!--
## Changelog PUT LATEST CHANGES AT THE TOP PLEASE
- 2026-08-07 | Eric Aquaronne | added change log   | 2.0.2606 
- 2026-08-07 | Ori Shadmon | based on existing content usd  Claude to create a FL document 

-->

## What Is Federated Learning?

Federated learning (FL) is a way of training a machine learning model across many separate data sources — hospitals, 
banks, factories, sensors, phones — without ever moving the raw data into one central place. Each participant trains the 
model locally, on its own data, and only the resulting model updates (weights, not records) are sent onward and combined 
into a single, improved model.

### Centralized Learning vs. Federated Learning

The conventional approach to machine learning centralizes data first and trains second: every source ships its raw data 
to one training environment, and a model is built from the combined pool. Federated learning inverts this — the model 
travels to the data, trains where the data already lives, and only a compact summary of what it learned (the model 
update) travels back.

| Aspect |                        Centralized Learning                        | Federated Learning |
| :---: |:------------------------------------------------------------------:| :---: |
| Where training happens |                  One central server / datacenter                   | Locally, on each participant's own device or site |
| What moves across the network |                              Raw data                              | Only model updates (weights/gradients) |
| Data ownership |                       Data leaves the source                       | Raw data never leaves the local device or system |
| Privacy / compliance exposure |  Higher — centralizing data increases breach and regulatory risk   | Lower — well suited to HIPAA and similar regulated environments |
| Typical use case fit |                   Simple, single-owner datasets                    | Multi-institution or highly distributed data (healthcare, finance, IoT) |

*Comparison derived from the EdgeLake-FL presentation ("What is Federated Learning?" slide, citing the OpenFL project) and the AnyLog Network engineering blog.*

### Why It Matters

Because raw data never leaves its source, federated learning is naturally suited to:

- Privacy-regulated domains such as healthcare (HIPAA) and finance, where centralizing patient or customer records is legally and ethically fraught.
- Highly distributed data environments such as IoT, where thousands of devices each hold a small, local slice of the overall picture.
- Any setting where reducing data-breach exposure and data-governance overhead is a priority.

---

## 2. The Problem: Why Federated Learning Hasn't Been Widely Adopted

Federated learning is conceptually well understood and has existed as a research topic for years, yet real-world, production deployments remain rare. The gap is not technical understanding — it's operational. FL is a massive engineering challenge once you move past a whiteboard diagram, for five main reasons:

**1. Distributed data**
There is no efficient, built-in method to operate on data that is scattered across many independent sites.

**2. Data heterogeneity**
Each participant tends to structure its data differently (different schemas, formats, naming). Without a way to unify or harmonize this automatically, model training breaks or requires constant manual mapping.

**3. Participant heterogeneity**
Coordinating many participants — with different hardware, connectivity, and availability — has no efficient, automated orchestration method in most FL toolkits.

**4. Breadth of skills required**
Standing up FL from scratch demands expertise across distributed systems, networking, databases, cryptography, and machine learning simultaneously — a rare combination on one team.

**5. Operational complexity**
- Standing up distributed infrastructure and distributing models to every node.
- Running and maintaining an aggregator.
- Deploying a federated learning algorithm on every device individually.
- Conducting the continuous, multi-round training process by hand.
- None of this scales gracefully to 100, 1,000, or 10,000 nodes.

As a result, most existing FL frameworks (TensorFlow Federated, Flower, IBM-FL, and similar) provide useful building blocks — optimizers, aggregation algorithms — but stop well short of end-to-end automation. Someone still has to manually wire together data access, node coordination, and inference deployment. The market reflects this gap: federated learning in healthcare is a small fraction of the overall AI-in-healthcare market, not because the need is small, but because the infrastructure to deploy it hasn't existed.

---

## 3. The Solution: How EdgeLake / AnyLog Solve This

EdgeLake (the open-source project, distributed by the Linux Foundation Edge) and AnyLog (its enterprise counterpart) take a different starting point: instead of treating federated learning as a research algorithm that still needs infrastructure built around it, they treat it as a data and orchestration problem, and automate the parts that have historically required manual engineering.

### The Core Idea: A Virtual, Decentralized Data Lake

In the conventional model, every edge device ships all of its data up to the cloud, where a central AI/analytics layer queries it. EdgeLake flips this: each edge node keeps its data locally, and instead of moving data to the query, EdgeLake moves the query to the data. An AI layer sends a query once; EdgeLake distributes it across the relevant nodes, each node processes its own local data, and only the (much smaller) result sets flow back and are combined. The network of edge nodes behaves like a single virtual data lake, even though nothing is physically centralized.

### A Blockchain-Backed Metadata Layer

EdgeLake nodes share a decentralized metadata layer, synchronized via blockchain, that gives every node the same consistent view of what data, models, and training applications exist across the network — without any node needing to see another node's raw data. This shared metadata layer is what lets the rest of the process be automated rather than manually coordinated.

### EdgeFL: The Automated Federated Learning Lifecycle

Built on top of AnyLog, EdgeFL automates the full federated learning lifecycle — training, aggregation, and inference — while keeping data in place. In practice this comes down to five steps, only the first of which is manual:

| Step | Who / What | Action | Automated? |
| :---: |---| :---: |---|
| 1 | ML Engineer | Writes a training application once and publishes it to the shared metadata layer (blockchain) | Manual (one-time) |
| 2 | Edge node | Queries the training app and current model weights; generates a local sub-model using its own local data | Automated |
| 3 | Edge node | Publishes the resulting sub-model back to the shared metadata layer | Automated |
| 4 | Aggregator node | Pulls the published sub-models, aggregates them, and publishes an updated / final model | Automated |
| 5 | Edge node | Runs inference locally against the final model to produce real-time predictions | Automated |

*Steps synthesized from the "Automating Federated Learning" slide (EdgeLake-FL presentation, PET Conf 2025) and the EdgeFL lifecycle description on the AnyLog Network blog.*

Because model weights are pulled by each node rather than pushed out by a central coordinator, nodes are not hard-coupled to one another. This pull-based architecture gives the system fault tolerance and lets it scale horizontally — new nodes can join, drop off, or reconnect without breaking the training process.

### What This Removes From the Engineer's Plate

> **Key capabilities AnyLog automate:**
> - Dynamic schema harmonization — no manual, hand-written SQL mapping between participants' differing data structures.
> - Model distribution and synchronization across nodes — handled transparently by the platform.
> - Deployment of production inference endpoints directly on edge nodes, without custom integration work per site.
> - Security and access control — an encrypted peer-to-peer messaging layer with policy-based, cryptographically signed access, so each node only gets the access it's explicitly permitted.
> - Horizontal scaling — edge nodes operate without hard dependencies on each other.
> - Hardware- and library-agnostic training — existing hardware (including GPUs) and any Python ML library can be used to write the training application.

### Key Benefits at a Glance

- **Automation** — fully automated distributed model training; transfers and node synchronization are transparent to the user.
- **AI model enablement** — automatic model deployment; EdgeLake hosts production inference endpoints directly at the edge.
- **Security & privacy** — encrypted peer-to-peer messaging; raw data always remains in place.
- **Scaling** — edge nodes operate independently, enabling horizontal scaling.
- **Simplicity** — networking, security, deployment, and synchronization are all handled by the platform rather than the engineering team.

---

## 4. Worked Example: Hospital HVAC Temperature Prediction

The following scenario, drawn from the EdgeLake-FL live demo, illustrates the abstract lifecycle above in a concrete setting.

### Scenario

A hospital has multiple units, each equipped with sensors that monitor temperature and air quality to support HVAC (heating, ventilation, and air conditioning) system management. The hospital wants a model that predicts temperature in order to optimize energy usage — but each unit's sensor data should stay within that unit.

### Architecture

- 4 nodes total: 3 nodes store data locally, each representing an independent hospital unit that processes its own sensor data on-site.
- 1 node functions as the aggregator (this role can also be handled by a training node).
- Each unit maintains its own data; a blockchain layer secures synchronization and model distribution across all four nodes.
- In each unit, a machine learning model derives local insights, and local inference enables predictions based on the federated model — without that unit's raw sensor data ever having to leave the building.

### Demo Setup

- **Goal:** predict temperature to optimize energy usage.
- **Setup:** 3 EdgeLake operator nodes plus 1 aggregator node.
- **Data fields used:** `actuatorState`, `co2Value`, `eventCount`, `humidity`, `switchStatus`, `temperature`.
- **Model:** a Long Short-Term Memory (LSTM) network — a type of recurrent neural network (RNN) well suited to time-series sensor data.
- The demo used real sensor data, contributed by AnyLog's partner Winniio.

### Walking Through the Lifecycle for This Example

1. A machine-learning engineer writes the LSTM training application once and publishes it to the shared metadata layer.
2. Each of the 3 hospital-unit nodes queries the training app and the current model weights, then trains a sub-model locally on its own temperature, humidity, CO2, and actuator/switch data.
3. Each unit publishes its trained sub-model (not its raw sensor readings) back to the shared metadata layer.
4. The aggregator node pulls the three sub-models, aggregates them into an updated model, and publishes the final model back to the network.
5. Each hospital unit can now run inference locally against the final model — producing temperature predictions used to optimize HVAC energy usage in real time, on-site.

The net result: a single, more accurate temperature-prediction model trained on the combined experience of all three hospital units — achieved without a single row of any unit's sensor data ever leaving that unit.

---

## 5. Sources

- [EdgeLake-FL: An Automated Federated Learning Platform for the Edge](https://www.youtube.com/watch?v=eQWARlXZvoc) — presentation, PET Conf 2025 (uploaded PDF), talk by Ori Shadmon & Moshe Shadmon
- [AnyLog — Enabling Federated Learning](https://www.youtube.com/watch?v=4qooadahj0Q) (YouTube, LF Open Source Summit)
- [AI Federated Learning with AnyLog Edge (EdgeLake) in 5 mins](https://www.youtube.com/watch?v=UzmagWhQUQU) (YouTube)
- [Solving the Hardest Problem in Federated Learning: Deployment at Scale with AnyLog & EdgeLake](https://medium.com/anylog-network/solving-the-hardest-problem-in-federated-learning-deployment-at-scale-with-anylog-edgelake-2c673c0e4f27) — Roy Shadmon, AnyLog Network (Medium)