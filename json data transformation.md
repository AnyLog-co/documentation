# JSON Data Transformation

Using command line instructions, users can transform JSON data to target structures.    
Examples of usage:
* Retrieve needed values from JSON objects.
* Retrieve needed values from the ledger policies. Details ate available at the [Query policies](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#query-policies) 
section in the [Blockchain commands](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#blockchain-commands) documentation. 
* Map source JSON data to a target structure - Details are available at the [Bring Command](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#bring-command)
section in the [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#using-a-message-broker) documentation.


## Creating JSON Objects and Policies

JSON Objects are a commonly used data structure in the AnyLog processes. In particular, Policies stored in the metadata 
layer are JSON Objects with a single key at the root layer. The key at the root is considered as the Policy Type.  

Below is an example of script creating a Policy of Type Operator assigned to a variable called new_operator:

<pre>
operator_name = opr_375
operator_port = 2048

< new_operator = {'operator' : {'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a',
                        'name' : !operator_name,
                        'ip' : !external_ip,
                        'port' : !operator_port}} >


</pre>

Note:
* The less than and greater than signs (< ... >) that wrap the policy allow to consider multiple lines on the AnyLog CLI as a single command.
* A value associated to ***external_ip*** is set by default when AnyLog node is initiated. 

The following command returns the value assigned to the variable new_operator on the AnyLog CLI:
<pre>
!new_operator
</pre>
The following command returns the value of new_operator using a REST call:
<pre>
get !new_operator
</pre>

## Transforming JSON representatives to JSON Objects

The command ***json*** returns a JSON object or validates a correct JSON structure whereas variable names are replaced by their assigned values.     
Usage:
<pre>
json [JSON object] [test]
</pre>
 
Example (referencing the [script in the example above](#creating-json-objects-and-policies)):
<pre>
json !new_operator
</pre>
Retutns:
<pre>
{'operator' : {'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a', 'name' : "opr_375", 'ip' : "24.23.250.144", 'port' : "2048"}}
</pre>
 

### Validating the JSON object structure
The keyword ***test*** is optional. If added, the command returns ***true*** if the structure is correct and ***false*** if the test structure is not in JSON format.
Example:
<pre>
json !new_operator test
</pre>

## The 'From JSON Object Bring' command

The Bring command retrieves values from a JSON object and formats the retrieved data.

The bring is followed by a list of keys and string values. The keys are applied on the JSON object to retrieve the
values associated withe the keys and the string values are added to the retrieved data. 
   
* The formatting instruction may use the keyword ***separator*** to provide a suffix to the output string returned from each object.  
### Special separators:

| separator  | Explanation |
| ---- | ------------|
| separator = \n | A new line character is added at the end of the data returned from each JSON object  |
| separator = \t | A tab is added at the end of the data returned from each JSON object  |

### The bring keyword
  
* The keyword bring can be suffixed with one or more of the following keywords (see example #3 below with multiple keywords):     
    * ```bring.unique``` - returns unique values.  
    * ```bring.first``` - returns the value from the JSON object with the earliest date. If a date is missing from the objects, the first object in the ledger file is returned.
    * ```bring.recent``` - returns the value from the JSON object with the latest date. If a date is missing from the objects, the last object in the ledger file is returned.  
    * ```bring.json``` - returns the requested keys and values in a JSON format. Additional formatting instructions are ignored.
    * ```bring.table``` - returns the requested keys and values in a table format. The bring command determines the table columns.
    * ```bring.count``` - returns the number of entries that satisfy the result.
    * ```bring.null``` - includes null values in the returned JSON.
    * ```bring.table.sort``` - returns the values in a sorted table format.
    
### Special bring values

If the bring values are wrapped in square brackets, it designates keys into the policy considered.
For example ```bring [operator][name]``` will pull the name value from an Operator policy.  
If an asterisk sign is used. it is replaced with the policy type. For example, in an Operator policy, ```[operator][name]``` is the same as  ```[*][name]```.  
Empty brackets ```[]``` designate the policy type.
  
### Examples:
1) Return policy info in a table structure:
<pre>
 blockchain get (master,operator,query) bring.table [*][name] [*][ip]
</pre>
2) Return policy info in a JSON structure:
<pre>
 blockchain get (master,operator,query) bring.json [*][name] [*][ip]
</pre>
3) Return policy info in a JSON structure and include null values:
<pre>
 blockchain get (master,operator,query) bring.json.null [*][name] [*][ip] [*][address]
</pre>
In the 3rd example, if address is not included in the policy, the returned JSON includes the key "address" with an empty value. 
4) Return policy info in a sorted table structure:   
<pre>
blockchain get * bring.table.sort [] [*][name] [*][ip]
</pre>

### Retrieving data from a JSON object
Usage:
<pre>
from [JSON object] bring [list of keys and formatting instructions]
</pre>

Example:
<pre>
< policy = {'cluster' : {'company' : 'anylog',
               'name' : 'cluster_1',
               'status' : 'active',
               'ledger' : 'global'}} >

from !policy bring [cluster][name] " : " [cluster][status]
</pre>

### Retrieving data from a a ledger policy.
Usage:
<pre>
blockchain get [get instructions] bring [list of keys and formatting instructions]
</pre>

Examples:

* Retrieve the member ID of an operator:
<pre>
blockchain get operator where ip =24.23.250.144 bring [operator][member]
</pre>

* Retrieve the list of tables with the database name for each table:
<pre>
blockchain get table bring [table][dbms] " : " [table][name] \n
</pre>

* Retrieve the list of tables including the database of each table and return result as a list of json entries:
<pre>
blockchain get table bring.json [table][dbms] [table][name]
</pre>

* The following example retrieves unique databases which are in the policies describing the tables:  
<pre>
blockchain get table bring.unique ['table']['dbms'] separator = " " 
</pre>

* The following example retrieves unique databases which are in the policies describing the tables and returns the reply in JSON format:  
<pre>
blockchain get table bring.unique.json ['table']['dbms']
</pre>

* The following example returns the list of IPs and Ports of the Operators as a list of JSON objects.
<pre>
blockchain get operator bring.json [operator][ip] [operator][port]
</pre>

* The following example returns the number of policies of type 'table'.
<pre>
blockchain get table bring.count
</pre>
