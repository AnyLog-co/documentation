# Prerequisites & Setup Considerations

| Feature             | Requirement |
| ------------------- | ----------- |
| **Operating System** | Linux (Ubuntu, RedHat, Alpine, Suse) <br> Windows |
| **Memory Footprint** | 100 MB (AnyLog without Docker) <br> 300 MB (AnyLog with Docker) |
| **Databases**        | SQLite (default, no installation required) <br> PostgreSQL (optional) <br> MongoDB (only if blob storage is needed) |
| **CPU**              | Intel, ARM, and AMD supported <br> Runs on single CPU machines up to large multi-core servers <br> Deployable on gateways, Raspberry Pi, and large-scale hardware |
| **Storage**          | Horizontally scalable — nodes and storage added dynamically as needed <br> Requirements depend on expected data volume and retention <br> Automated archival and transfer to larger nodes supported |
| **Network**          | TCP-based network required (local, internet, or hybrid) <br> Overlay network recommended (Nebula used by default, but others are supported) <br> Static IP and 3 open ports per node (via overlay or direct) |
| **Cloud Integration**| Built-in integration via REST, Pub/Sub, and Kafka |
| **Deployment Options** | Executable (background process), Docker, or Kubernetes |

---

## Comments

### Databases
- **SQLite**: recommended for smaller nodes and in-memory data.  
- **PostgreSQL**: recommended for larger nodes.  
- **MongoDB**: used for blob storage.  
- Multiple databases can run on the same node if needed.  

### Network
Using an **overlay network** is recommended because:  
- Provides isolation for security considerations.  
- Simplifies IP and port management. Without it, users must manually configure and manage IP/port availability.  
