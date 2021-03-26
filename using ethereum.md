# Using Ethereum as a Global Metadata Platform

## Overview

Users can configure their network to use [Ethereum](https://en.wikipedia.org/wiki/Ethereum) as a global metadata layer such 
that all updates to the metadata are represented on the blockchain and shared among all members of the network.

This document explains how to configure an AnyLog Network to leverage Ethereum as the underlying blockchain platform.  
Connection to the blockchain platform can be done using a local node or a hosted node.
With a local node, users need to configure and maintain an Ethereum node that hosts a local copy of the blockchain 
data and needs to verify all the transactions of the Ethereum Network.  
With a hosted node, users connect to a 3rd party node that provides the local node functionality but maintained by a 3rd party.  
The AnyLog network is agnostic to how Ethereum services are provided, in this document we use [Infura](https://infura.io/) hosted node.
With Infura, users can connect to an Ethereum network and for testing purposes, to the Ethereum TestNet.
 
This document details how to use Ethereum as the metadata layer by providing an enabling the following functionality:
* Connect to Ethereum
* Create accounts, the accounts are used for blockchain transactions payments.
* Publish the AnyLog contract, the contract contains the global metadata (in the form of Policies) which is shared by members of the network.
* Update a policy on the blockchain.
* Configure an AnyLog node to continuously synchronize the local copy of the metadata (that is hosted on the node) with the global copy of the metadata (that is hosted on the blockchain).

Note, the AnyLog metadata is represented on the blockchain in the form of Policies. Policies are detailed in the [Managing Metadata](https://github.com/AnyLog-co/documentation/blob/master/metadata%20management.md#managing-metadata) section.  

## Prerequisites

* Open an account in Infura - instructions are [here](https://blog.infura.io/getting-started-with-infura-28e41844cc89/).
* From Infura get a Project ID and API endpoint.
* An AnyLog node to configure.

## Connecting to Ethereum



