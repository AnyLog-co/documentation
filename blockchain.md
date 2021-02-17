# Blockchain Configuration

Connecting to a blockchain platform requires the following steps:

* Deploying a contract on the blockchain platform. The contract excepts updates of new policies.
* Pushing new policies from the network nodes to the blockchain.
* Supporting pull of the policies from the blockchain.
* Configuring nodes to periodically pull the blockchain data.


The following example connects to Ethereum node on [Infura](https://infura.io/) and demonstrates the functionality.


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
<blockchain connect ethereum where
        provider = "https://rinkeby.infura.io/v3/45e96d7ac85c4caab102b84e13e795a1" and
		contract = "0x64bb40d197825d173a117c5305c036fac6c8a082" and
		private_key = "a4caa21209188ef5c3be6ee4f73c12a8c306a917c969638fb69f164b0ed95380" and 
		public_key = "0x982AF5e1589f1486b4bA17aFB6eb940aAeBBdfdB" and 
		gas_read = 2000000  and
		gas_write = 3000000>
</pre>

## Test Connection
<pre>
get platforms
</pre>

## Add a new policy
<pre>
<test_policy= {"test" : {
                "company" : "AnyLog",
                "name"   : "test_policy_#x"
    }
}>

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
