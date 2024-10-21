# Blockchain Demo 

AnyLog Network, which is available with both EdgeLake and Enterprise uses layer-2 logic to publish data onto the 
blockchain. The following demonstrates two nodes on [Optimism](https://www.optimism.io/) test network.

 The steps provided below are automatically executed when deloying EdgeLake & EdgeLake enterprise via a AnyLog's deployment 
 processes. 

### Configurations 
* `SYNC_TIME` (default: 30 seconds) - How often to sync from blockchain
* `BLOCKCHAIN_SOURCE` (default: master) - Source of where the data is coming from. When `LOCAL_BLOCKCHAIN` is set to _false_, 
value should be set to _blockchain_
* `PROVIDER` (default: infura) - SubQuery network participant who is responsible for serving RPC queries for blockchain 
data to their customers. We're using [infura](https://www.infura.io/)
* `PLATFORM` (default: optimism) - Blockchain to use. We're using an off-chain extension ([layer-2]()) 
blockchain named <a herf="https://www.optimism.io/" target="_blank">Optimism</a>
* `BLOCKCHAIN_DESTINATION` - Where will the copy of the blockchain be stored locally
* `PRIVATE_KEY` & `PUBLIC_KEY` - keys to access crypto wallet(s)
* `CHAIN_ID` - Wallet ID

### Key Term
* **[Layer-2](https://iq.wiki/wiki/layer-2/)** sits on top of layer-1 blockchain (example Ethereum), allowing to have 
seem-less security and network infrastructure guarantees of the blockchain layer-1 for less. 
* **[Optimism](https://www.optimism.io/)** is a layer-2 protocol for Ethereum. The reason we've selected it as our blockchain
protocol is due to its ability to execute **rollups**; which batches multiple transactions into a single transaction that is committed 
on-chain. The batching approach ultimately improves the transaction throughput while drastically reducing the cost of 
each transaction from tens of dollars to pennies if not less.
*  **[Sepolia](https://sepolia.etherscan.io/)** is _Optimism_'s test network.   
* **[Infera](https://www.infera.org/)** is a remote procedure call (RPC), provides us with an endpoint to connect to 
Optimism blockchain. 

### Links 
* [Blockchain Commands](blockchain%20commands.md)
* [Blockchain Configuration.md](blockchain%20configuration.md)
* [policies.md](policies.md)

## Sepolia for Optimism as Blockchain
1. Specify [infura](https://www.infura.io/) as our RPC provider and connect to it. 

Infura is a _RPC_ provider, which allows us to connect AnyLog to Optimism blockchain. Optimism is a layer-2
with a test network platform named **Sepolia**.
```anylog
platform = optimsm 
provider = infra 

blockchain connect to !platform where provider = !provider
```

2. If user does not have private and public keys for Optimism, then create one. Make sure to save both private and public
keys in a secure location. To re-use private / public keys in future docker container, make sure to set value(s) in 
**advance configs**.
```anylog
blockchain create account !platform

print !public_key 
print !private_key 
```

3. Load the crypto wallet for Optimism Sepolia test network blockchain platform ID 
```anylog
chain_id = 71143311

<blockchain set account info where 
    platform = !platform and 
    private_key = !private_key and 
    public_key = !public_key and 
    chain_id = !chain_id>
```

4. Validate account has been set
```anylog
get platforms
```

5. Deploy a contract - Set up a metadata layer using a smart contract on Optimism. Smart contracts are executing 
programmable contract that nodes interact with and use to store the source of truth. An AnyLog Network only needs one 
smart contract to maintain the network metadata layer. 
```anylog
contract = blockchain deploy contract where  platform = optimism and public_key = !public_key

print !contract
```

6. Associate contract with an account
```anylog
blockchain set account info where platform = !platform and contract = !contract
```

7. Automatically sync against the blockchain
```anylog
blockchain_source=blockchain
   
run blockchain sync where source = blockchain and time = !sync_time and dest = file and platform = optimism
```

At this point AnyLog should be connected to the Optimism blockchain. 


## AnyLog Policies on Optimism
**Declaring a node policy**
1. Create policy 
```anylog
<new_node = {
    "policy_type": {
        "name": [Policy Name],
        "company": [Policy owner],
        ... 
        [Other policy configs]
        ...
    }
}>
```

2. Insert policy onto the blockchain
```anylog
blockchain insert where policy=!new_policy and local=true and blockchain=!platform
```
 
**Update Policies**: 

Generally speaking, content that's stored on a blockchain is non-fungible (ie cannot change). However, nodes that are 
part of the AnyLog network can have configuration changes - such as: node ownership, network information, permissions or 
simply adding / removing information for a pre-existing policy. We recommend looking into [ANMP](policies.md/#anmp-policy)
in order to modify existing policies. 


 





