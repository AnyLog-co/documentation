# Using Ethereum as a Global Metadata Platform

## Overview

Users can configure their network to use [Ethereum](https://en.wikipedia.org/wiki/Ethereum) as a global metadata layer such 
that all updates to the metadata are represented on the blockchain and shared among all members of the network.

This document explains how to configure an AnyLog network to leverage Ethereum as the underlying blockchain platform.  
Connection to the blockchain platform can be done using a local node or a hosted node.
With a local node, users need to configure and maintain an Ethereum node that hosts a local copy of the blockchain 
data and needs to verify all the transactions on the Ethereum Netowrk.
With a hosted node, users connect to a 3rd party node that provides the local node functionality but maintained by a 3rd party.
The AnyLog network is agnostic to how Ethereum services are provided, in this document we use [Infura](https://infura.io/) hosted node.
With Infura, users can connect to an Ethereum network and for testing purposes, to the Ethereum testnet.
 
