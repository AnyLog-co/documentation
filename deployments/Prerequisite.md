
# Prerequisite and setup considerations



| Feature               | Requirement  |
| --------------------- | ------------| 
| Operating System      | Linux (Ubuntu, RedHat, Alpine, Suse) | 
|                       | Windows |
| Memory footprint      | 100 MB available for the AnyLog process |
| Databases             | PostgreSQL installed (optional) |
|                       | SQLite (default, no need to install) |
|                       | MongoDB (Only if blob storage is needed) |
| CPU                   | Intel, ARM and AMD are supported. |
|                       | AnyLog can be deployed on a single CPU machine and up to the largest servers (can be deployed on gateways, Raspberry PI, and all the way to the largest multi-core machines).|
| Storage               | AnyLog supports horizontal scaling - nodes (and storage) are added dynamically as needed, therefore less complexity in scaling considerations. Requirements are based on expected volume and duration of data on each node. AnyLog supports automated archival and transfer to larger nodes (if needed). |
| Network               | Required: a TCP based network (local TCP based networks, over the internet and combinations are supported) |
|                       | An overlay network is recommended. We can work with any overlay network vendor and use Nebula as a default. |
| Cloud Integration     | build in integration using REST, Pub-Sub, and Kafka. |
| Deployment options    | Docker and Kubernetes. |

    

