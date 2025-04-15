# JSON Data Transformation

Using command line instructions, users can transform JSON data to target structures.    
Examples of usage:
* Retrieve needed values from JSON objects.
* Retrieve needed values from the ledger policies. Details ate available at the [Query policies](blockchain%20commands.md#query-policies) 
section in the [Blockchain commands](blockchain%20commands.md#blockchain-commands) documentation. 
* Map source JSON data to a target structure - Details are available at the [Bring Command](message%20broker.md#bring-command)
section in the [Message Broker](message%20broker.md#using-a-message-broker) documentation.


## Creating JSON Objects and Policies

JSON Objects are a commonly used data structure in the AnyLog processes. In particular, Policies stored in the metadata 
layer are JSON Objects with a single key at the root layer. The key at the root is considered as the Policy Type.  

Below is an example of script creating a Policy of Type Operator assigned to a variable called new_operator:

```anylog
operator_name = opr_375
operator_port = 2048

< new_operator = {'operator' : {'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a',
                        'name' : !operator_name,
                        'ip' : !external_ip,
                        'port' : !operator_port}} >


```

Note:
* The less than and greater than signs (< ... >) that wrap the policy allow to consider multiple lines on the AnyLog CLI as a single command.
* A value associated to `external_ip` is set by default when AnyLog node is initiated. 

The following command returns the value assigned to the variable new_operator on the AnyLog CLI:
```anylog
!new_operator
```
The following command returns the value of new_operator using a REST call:
```anylog
get !new_operator
```

## Transforming JSON representatives to JSON Objects

The command `json` returns a JSON object or validates a correct JSON structure whereas variable names are replaced by their assigned values.     
Usage:
```anylog
json [JSON object] [test]
```
 
Example (referencing the [script in the example above](#creating-json-objects-and-policies)):
```anylog
AL anylog-node > json !new_operator
{'operator' : {
  'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a', 
  'name' : "opr_375", 
  'ip' : "24.23.250.144", 
  'port' : "2048"
  }
}
```
 

### Validating the JSON object structure
The keyword `test` is optional. If added, the command returns _true_ if the structure is correct and _false_ if the test structure is not in JSON format.
Example:
```anylog
json !new_operator test
```

## The 'From JSON Object Bring' command

The `bring` command retrieves values from a JSON object and formats the retrieved data.

The `bring` command is followed by a list of keys and string values. The keys are applied on the JSON object to retrieve the
values associated with the keys and the string values are added to the retrieved data. 
   
* The formatting instruction may use the keyword `separator` to provide a suffix to the output string returned from each object.  
### Special separators:

| separator  | Explanation |
| ---- | ------------|
| separator = \n | A new line character is added at the end of the data returned from each JSON object  |
| separator = \t | A tab is added at the end of the data returned from each JSON object  |

### The `bring` keyword
  
* The keyword bring can be suffixed with one or more of the following keywords (see example #3 below with multiple keywords):     
    * ```bring.unique``` - returns unique values.  
    * ```bring.first``` - returns the value from the JSON object with the earliest date. If a date is missing from the objects, the first object in the ledger file is returned.
    * ```bring.recent``` - returns the value from the JSON object with the latest date. If a date is missing from the objects, the last object in the ledger file is returned.  
    * ```bring.json``` - returns the requested keys and values in a JSON format. Additional formatting instructions are ignored.
    * ```bring.table``` - returns the requested keys and values in a table format. The bring command determines the table columns.
    * ```bring.table.sort``` - returns the values in a sorted table format. Users can specify columns id used in the sort. For example **bring.table.sort(1,0)** sorts by the second column followed by the first.
    * ```bring.count``` - returns the number of entries that satisfy the result.
    * ```bring.null``` - includes null values in the returned JSON.
    * ```bring.ip_port``` - return a comma seperated list of IP and ports.
    * ```bring.min``` - return the minimum value of an attribute.
    * ```bring.max``` - return the maximum value of an attribute.
  


### Special Bring Values
* **Basic Usage:**
  If the **bring** command values are wrapped in square brackets, it designates keys into the policy, and the associated values are returned.
  For example, ```bring [operator][name]``` will pull the name value from an Operator policy.


* **Wildcard Usage:**
  If an asterisk (*) sign is used, it is replaced with the policy type. For example, in an Operator policy, ```[*][name]``` is the same as ```[operator][name]```.


* **Empty Brackets:**
  Empty brackets ([]) designate the policy processed.


* **Substring Operations:**
  These special operations allow to retrieve specific substrings based on certain conditions.  
  The operations inside the parentheses are applied on the value extracted by the key.
  * rfind(substr) - finds the last occurrence of a specific substring (substr) within a string. It returns the substring starting from the last occurrence of substr to the end of the string.
  * find(substr) - finds the first occurrence of a specific substring (substr) within a string. It returns the substring starting from the beginning of the string to the first occurrence of substr.
  * prefix(n) - returns the first n characters of the string, essentially providing a truncated version from the start of the string.
  * suffix(n) - returns the last n characters of the string, essentially providing a truncated version from the end of the string.

  
### Examples:
  1. Return policy info in a table structure:
```anylog
 blockchain get (master,operator,query) bring.table [*][name] [*][ip]
```
  2. Return policy info in a JSON structure:
```anylog
 blockchain get (master,operator,query) bring.json [*][name] [*][ip]
```
  3. Return policy info in a JSON structure and include null values:
```anylog
 blockchain get (master,operator,query) bring.json.null [*][name] [*][ip] [*][address]
```
  4. Return policy info in a sorted table structure:   
```anylog
blockchain get * bring.table.sort [] [*][name] [*][ip]
```
  5. Return policy info in a sorted table structure and determine the sort columns:   
```anylog
blockchain get * bring.table.sort(3,1,0) [] [*][name] [*][ip]
```
  6. Return an IP port list from all the operators in the USA:   
```anylog
blockchain get operator where [country] contains US bring.ip_port
```
Note: In the 3rd example, if address is not included in the policy, the returned JSON includes the key "address" with an empty value.   

### Retrieving data from a JSON object
Usage:
```anylog
from [JSON object] bring [list of keys and formatting instructions]
```

Example:
```anylog
< policy = {'cluster' : {'company' : 'anylog',
               'name' : 'cluster_1',
               'status' : 'active',
               'ledger' : 'global'}} >

from !policy bring [cluster][name] " : " [cluster][status]
```

### Retrieving data from a ledger policy.
Usage:
```anylog
blockchain get [get instructions] bring [list of keys and formatting instructions]
```

Examples:

* Retrieve the member ID of an operator:
```anylog
blockchain get operator where ip =24.23.250.144 bring [operator][member]
```

* Retrieve the list of tables with the database name for each table:
```anylog
blockchain get table bring [table][dbms] " : " [table][name] \n
```

* Retrieve the list of tables including the database of each table and return result as a list of json entries:
```anylog
blockchain get table bring.json [table][dbms] [table][name]
```

* The following example retrieves unique databases which are in the policies describing the tables:  
```anylog
blockchain get table bring.unique ['table']['dbms'] separator = " " 
```

* The following example retrieves unique databases which are in the policies describing the tables and returns the reply in JSON format:  
```anylog
blockchain get table bring.unique.json ['table']['dbms']
```

* The following example returns the list of IPs and Ports of the Operators as a list of JSON objects.
```anylog
blockchain get operator bring.json [operator][ip] [operator][port]
```

* The following example returns the number of policies of type 'table'.
```anylog
blockchain get table bring.count
```
* The following examples returns the min and max value of the port values assigned to nodes.
```anylog
blockchain get (operator, query, publisher, master) bring.min [*][port]
blockchain get (operator, query, publisher, master) bring.max [*][port]
```
* The following examples return substrings.
```anylog
blockchain get tag bring.table [tag][table] [tag][path(rfind(/))]
blockchain get tag bring.table [tag][table] [tag][path(find(/))]
blockchain get tag bring.table [tag][table] [tag][path(suffix(10))]
blockchain get tag bring.table [tag][table] [tag][path(prefix(10))]
```