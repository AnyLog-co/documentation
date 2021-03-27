# Using Ethereum as a Global Metadata Platform

## Overview

Users can configure their network to use [Ethereum](https://en.wikipedia.org/wiki/Ethereum) as a global metadata layer such 
that all updates to the metadata are represented by the blockchain and shared among all members of the network.

This document explains how to leverage Ethereum as the underlying global metadata platform for the AnyLog Network and demonstrates the 
initial setup that is needed to facilitate Ethereum as the metadata layer.   
Once the setup is completed, nodes can synchronize their local metadata with the global metadata by configuring the synchronizer 
to connect to Ethereum. The details of configuring a node to sync with Ethererum are detailed at the
[Blockchain Configuration](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20configuration.md) section.


Connection to the blockchain platform can be done using a local node or a hosted node.
With a local node, users need to configure and maintain an Ethereum node that hosts a local copy of the blockchain 
data and needs to verify all the transactions of the Ethereum Network.  
With a hosted node, users connect to a 3rd party node that provides the local node functionality but maintained by a 3rd party.  
The AnyLog network is agnostic to how Ethereum services are provided, in this document we use [Infura](https://infura.io/) hosted node.
With Infura, users can connect to an Ethereum network and for testing purposes, to the Ethereum TestNet.

***Note***: In the examples below, the accounts and keys are exposed and are not maintained in a secure way. In a deployment which 
is using the Ethereum MainNet, users should do the following:
* Delegate private key creation and management to software clients (like [Geth](https://geth.ethereum.org/)) 
  or wallets (like [MetaMask](https://metamask.io/)). These projects provide a secure way to generate and handle private keys for blockchain interactions.
* Enable the AnyLog encryption functionality for the keys that are stored and used by the AnyLog node.
 
This document details how to use Ethereum as the metadata layer by providing and enabling the following functionality:
* Connect to Ethereum
* Create accounts, the accounts are used for blockchain transactions payments. Note that although accounts creation is available 
  directly from an AnyLog node, the functionality is supported to simplify testing and users should create accounts using proper tools (see the highlighted note above). 
* Publish the AnyLog contract, the contract manages the global metadata (in the form of Policies) which is shared by members of the network.
  Policies are detailed in the [Managing Metadata](https://github.com/AnyLog-co/documentation/blob/master/metadata%20management.md#managing-metadata) section.
* Update a policy on the blockchain.
* Configure an AnyLog node to continuously synchronize the local copy of the metadata (that is hosted on the node) with the global copy of the metadata (that is hosted on the blockchain).

## Prerequisites

* Open an account in Infura - instructions are [here](https://blog.infura.io/getting-started-with-infura-28e41844cc89/).
* From Infura get a Project ID and API endpoint.
  Or use the following demo ID and endpoint:
  * Project ID: 1qJR0deXYuwf0JYwdTz3YXQ14MZ
  * Project Endpoint: https://rinkeby.infura.io/v3/YOUR-PROJECT-ID
* An AnyLog node to configure.

## The blockchain commands
The AnyLog Blockchain commands are detailed [here](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-blockchain-commands).

## Connecting to Ethereum

* Assign the Endpoint to a variable:
<pre>
provider = https://rinkeby.infura.io/v3/45e96d7ac85c4caab102b84e13e795a1
</pre>

* Use the following command to connect using the Endpoint:
<pre>
blockchain connect ethereum where provider = !provider
</pre>

* Use the following command to test the connection parameters and status:
<pre>
get platforms
</pre>

Executing the ***get platforms*** command provides the following output:
<pre>
Blockchains connected
Name     Active Balance                   URL                                                           Public Key/Contract
--------|------|-------------------------|-------------------------------------------------------------|-------------------|
ethereum|True  |Failed to extract balance|https://rinkeby.infura.io/v3/45e96d7ac85c4caab102b84e13e795a1|                   |
        |      |                         |                                                             |                   |
</pre>
Note that keys were not yet created and therefore there in no available balance.  

## Create an Account 

Use the following command to create a  new Ethereum account:
<pre>
blockchain create account ethereum
</pre>

Executing the ***create account*** command provides an account address and a private key that can be used to create and maintain the metadata contract.

## Associate an account with the Ethereum connection

* Assign the the public key and private key to variables as in the example below:
<pre>
public_key = 0xb425E72041d1c5a640BFc4479A808Da83b83b515
private_key = 0x2e0796621732f74ac49a532e523bedbd707e4d1324506ff63528b553dc101ab0
</pre>

* Use the ***set account info*** command to specify the account information to use:

<pre>
blockchain set account info where platform = ethereum and private_key = !private_key and public_key = !public_key
</pre>

## Transfer funds to the account
For a Rinkeby TestNet, funds can be added from this [webite](https://www.rinkeby.io/#faucet). 

## Publish the AnyLog contract on the blockchain

The following command will deploy a contract that contains the logic to anchor the policies which are shared by the nodes in the network.
Users can maintain multiple independent networks by deploying multiple contracts and associating nodes to different contracts.  
Nodes that are assigned to the same contract, form a network.

<pre>
contract = blockchain deploy contract where  platform = ethereum and public_key = !public_key
</pre>

Executing the ***deploy contract*** command provides the contract address.    
Nodes that share the same contract form a network.

Add the contract information to the Ethererum connection information using the command
<pre>
blockchain set account info where platform = ethereum and contract = !contract
</pre>


## Updating a policy on the blockchain

The following command updates a policy on the blockchain:

<pre>
blockchain commit to ethereum !test_policy
</pre>

The variable ***test_policy*** is assigned with the policy to update.

## Synchronize the local copy of the metadata with the blockchain data

Details are available in the [Blockchain Configuration](https://github.com/AnyLog-co/documentation/blob/master/blockchain.md#blockchain-configuration) section.