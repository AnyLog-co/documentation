# Prerequisite and setup considerations

| Feature               | Requirement  |
| --------------------- | ------------| 
| Operating System      | Linux (Ubuntu, RedHat, Alpine, Suse) | 
|                       | Windows |
| Memory footprint      | 100 MB available for the AnyLog process |
| Databases             | PostgreSQL installed (optional) |
|                       | SQLite (default, no need to install) |
|                       | MongoDB installed (Only if blob storage is needed) |
| CPU                   | Intel, ARM and AMD are supported. |
|                       | AnyLog can be deployed on a single CPU machine and up to the largest servers (can be deployed on gateways, Raspberry PI, and all the way to the largest multi-core machines).|
| Storage               | AnyLog supports horizontal scaling - nodes (and storage) are added dynamically as needed, therefore less complexity in scaling considerations. Requirements are based on expected volume and duration of data on each node. AnyLog supports automated archival and transfer to larger nodes (if needed). |
| Network               | Required: a TCP based network (local TCP based networks, over the internet and combinations are supported) |
|                       | An overlay network is recommended. Most overlay networks can be used transparently. Nebula used as a default overlay network. |
| Cloud Integration     | Build in integration using REST, Pub-Sub, and Kafka. |
| Deployment options    | Docker and Kubernetes. |


**Comments**:
* Databases: 
  - SQLite recommended for smaller nodes and in-memory data.
  - PostgreSQL recommended for larger nodes.
  - MongoDB used for blob storage.
  - Multiple databases can be deployed and used on the same node.
    
* Network:
    An Overlay network is recommended for the following reasons:
    - Isolate the network for security considerations.
    - Manage IP and Ports availability. Without an overlay network, users needs to configure and manage availability 
      of IP and Ports used.
    

