# Securing the Network

## Overview

The network is secured using 3 mechanisms:
1) Using a 3rd party Overlay Network. An example of an overlay network is [Nebula](https://nebula.defined.net/docs/).
2) Securing the messages transferred between AnyLog nodes using Key-Based Authentication (Public Key Authentication).
3) Securing messages transferred between 3rd parties applications and AnyLog nodes using certificates and passwords.

## Deploying a 3rd party overlay network

The overlay network allows for:
a) Authorize the nodes allowed to participate in the network.
b) Identify the members of the network by unique IP and Port.
c) Resolve network routing issues.
d) Encrypted messaging between the member nodes.

Refer to the 3rd party vendor manual for instalation and configuration instructions.

## Key-Based Authentication

These processes are based on the following processes:  
* Each node is assigned with a private key and a public key^.
* A message from a node to a peer is signed by the private key.
* The peer receiving th message authenticates the sender using the public key.
* If the sender is authenticated, the sender permissions are validated using the relevant policies. 
* If the sender is authenticated, and the message request is permitted, the message will be processed.

^Note: A private key and a public key can be assigned to users - it allows for administrators to operate on the node's CLI
using their assigned permissions which may be less restrictive compared to the permissions assigned to the node.

The relevant AnyLog commands are detailed in the section [Node Authentication](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#node-authentication).  




