# The Remote CLI

The Remote CLI is a web application that offers a REST based GUI that allows to issue commands to nodes in the network.    
The GUI replaces the need to log to specific nodes by allowing to deliver the commands using REST.  

A similar functionality is achieved using [cURL](https://curl.se/) as well as with other tools such as [Postman](https://www.postman.com/).
Note: [Using Postman](../using%20postman.md) details the usage of Postman with AnyLog nodes.

## Installing the Remote CLI

## Configuring the Remote CLI
The Remote CLI can be configured to support specific settings, default values and frequently used commands.  
The configurations files are organized in the static/json folder as a set of JSON files.

### The setting files

The **setting.json** file determines the initialization settings when the Remote CLI form is used.  
The JSON file includes the following sections:
* **client** - specifies the default values on the client form.
* **certificates**
* **monitor**
 


## Usage examples



The following queries were all executed through the Query node to show that from a single point the user can get 
not only the data, but also metadata and general machine information.

* Show tables in network: 

`curl -X GET 23.239.12.151:32349 -H "command: get tables where dbms=*" -H "User-Agent: AnyLog/1.23"`
![get databases](../imgs/remote_cli_get_databases.png)

* Show columns in a given table - `litsanleandro.ping_sensor`: 

`curl -X GET 23.239.12.151:32349 -H "command: get columns where dbms=litsanleandro and table=ping_sensor" -H "User-Agent: AnyLog/1.23"`
![get columns](../imgs/remote_cli_get_columns.png)

* Query data in Blockchain - list all operators for company _Lit San Leandro_. There are 6 operators, but we only see 1 
 due to screen size. Please note, for `where`  conditions, user(s) should know what they're looking for -- whether it's 
a specific type of node based on a given IP address; or all the policies associated with a given owner (company).  
  
`curl -X GET 23.239.12.151:32349 -H 'command:blockchain get operator where company="Lit San Leandro"' -H "User-Agent: AnyLog/1.23"` 
![view operators in blockchain](../imgs/remote_cli_blockchain_operators.png)

* Get list of data nodes (operators) and what kind of data they contain. 

`curl -X GET 23.239.12.151:32349 -H "command:get data nodes" -H "User-Agent: AnyLog/1.23" `
![Data Nodes](../imgs/remote_cli_data_nodes.png)

* Query the last 90 seconds - notice that unlike the previous examples the "network" option is enabled & data is coming 
from 3 of the 6 nodes. 

`curl -X GET /23.239.12.151:32349 -H 'command: sql litsanleandro format=table "select timestamp, value FROM ping_sensor WHERE timestamp >= NOW() -90 seconds"' -H "User-Agent: AnyLog/1.23" -H "destination: network"`
![Last 90 seconds of data](../imgs/remote_cli_select_last_90sec.png)

* Query the last 10 minutes of data per node - notice that like the previous example the "network" option is enabled & data is coming 
from 3 of the 6 nodes. (The reason for the limit is so the result will easily fit the screen)

`curl -X GET 23.239.12.151:32349 -H 'command: sql test format=table and extend=(+ip, +node_name) "select timestamp, value FROM rand_data WHERE timestamp >= NOW() - 10 minutes ORDER BY value LIMIT 50"' -H "User-Agent: AnyLog/1.23" -H "destination: network"`
![Last 10 minutes of data](../imgs/remote_cli_select_last_10min.png)