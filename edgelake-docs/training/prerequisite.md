---
layout: default
parent: Training
title: Prerequisite
nav_order: 1
---

# Prerequisite and setup considerations
<table>
  <thead>
    <tr>
      <th style="tex-align: center; font-weight: bold">Feature</th>
      <th style="tex-align: center; font-weight: bold">Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Operating System</td>
      <td>Docker-based deployment, Linux (Ubuntu, RedHat, Alpine, Suse), Windows, Mac-OSX</td>
    </tr>
    <tr>
      <td>Memory footprint</td>
      <td>100 MB available for the AnyLog deployed without Docker<br>300 MB available for AnyLog deployed with Docker</td>
    </tr>
    <tr>
      <td>Databases</td>
      <td>PostgreSQL installed (optional)<br>SQLite (default, no need to install)<br>MongoDB installed (Only if blob storage is needed)</td>
    </tr>
    <tr>
      <td>CPU</td>
      <td>Intel, ARM and AMD are supported.<br>AnyLog can be deployed on a single CPU machine and up to the largest servers (can be deployed on gateways, Raspberry PI, and all the way to the largest multi-core machines).</td>
    </tr>
    <tr>
      <td>Storage</td>
      <td>AnyLog supports horizontal scaling - nodes (and storage) are added dynamically as needed, therefore less complexity in scaling considerations. Requirements are based on expected volume and duration of data on each node. AnyLog supports automated archival and transfer to larger nodes (if needed).</td>
    </tr>
    <tr>
      <td>Network</td>
      <td>Required: a TCP based network (local TCP based networks, over the internet and combinations are supported)<br>An overlay network is recommended. Most overlay networks can be used transparently. Nebula used as a default overlay network.<br>Static IP and 3 ports open and accessible on each node (either via an Overlay Network, or without an Overlay).</td>
    </tr>
    <tr>
      <td>Cloud Integration</td>
      <td>Build in integration using REST, Pub-Sub, and Kafka.</td>
    </tr>
    <tr>
      <td>Deployment options</td>
      <td>Executable (can be deployed as a background process), or Docker or Kubernetes.</td>
    </tr>
  </tbody>
</table>


**Comments**:
* For Mac OSX installation you may need to add <code>envsubst</code> command functionality via <a href="https://www.gnu.org/software/gettext/" target="_blank">gettext</a>.
<pre class="code-frame"><code class="language-shell">
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install envsubst
brew install gettext
</code></pre>

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
    

