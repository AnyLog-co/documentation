# Blockchain Configuration

Nodes in the network can be configured to synchronize their local metadata with a global metadata hosted by a blockchain platform.
With propper configuration, when a node updates the metadata, the updates will be published on the blockchain platform
and at the same time, updates done by peer nodes and are published on the blockchain, become available to 
the members of the network.  
This document explains how to configure a node sch that updates to the metadata are published on the 
blockchain platform and how to configure to continuously receive metadata updates published by peers.

Notes:
* Using the blockchain as a metadata platform requires a contract that manages the metadata information. The initial contract setup
with Ethereum is detailed at the section [Using Ethereum as a Global Metadata Platform](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md).
* The published metadata is represented as Policies which are detailed in the [Policies](https://github.com/AnyLog-co/documentation/blob/master/metadata%20management.md#policies) section.
* The examples below use Ethereum (TestNet) as the blockchain platform and a hosted node using [Infura](https://infura.io/).  

## Prerequisites

* An AnyLog contract on the blockchain platform. The contract manages the metadata policies (publishing the contract is detailed at 
  [Publish the AnyLog contract on the blockchain](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md#publish-the-anylog-contract-on-the-blockchain)).
* The blockchain connection and contract information.
* An anylog instance to configure.


## Setup of a new node
<pre>
run tcp server !ip 2048
run rest server !ip 2049
set authentication off
set echo queue on
connect dbms sqlite anylog@127.0.0.1:demo 5432 system_query
</pre>

## Connect to Ethereum node on Infura and provide contract info
<pre>
< blockchain connect to ethereum where
        provider = "https://rinkeby.infura.io/v3/45e96d7ac85c4caab102b84e13e795a1" and
		contract = "0x64bb40d197825d173a117c5305c036fac6c8a082" and
		private_key = "a4caa21209188ef5c3be6ee4f73c12a8c306a917c969638fb69f164b0ed95380" and 
		public_key = "0x982AF5e1589f1486b4bA17aFB6eb940aAeBBdfdB" and 
		gas_read = 2000000  and
		gas_write = 3000000 >
</pre>

## Test Connection
<pre>
get platforms
</pre>

## Add a new policy
<pre>
< test_policy= {"test" : {
                "company" : "AnyLog",
                "name"   : "test_policy_#x"
    }
} >

blockchain commit to ethereum !test_policy
</pre>

## Pull policies
<pre>
blockchain checkout from ethereum 
</pre>


## Synchronize the blockchain data with a local copy every 30 seconds
<pre>
run blockchain sync where source = blockchain and platform = ethereum and time = 30 seconds and dest = file
</pre>
