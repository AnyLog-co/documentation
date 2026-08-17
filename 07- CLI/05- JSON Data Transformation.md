---
title: "JSON Data Transformation"
description: ""
layout: page
source_path: "05- JSON Data Transformation.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name**      | **Change**         | **Version** |
 |------------|---------------|---------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
--->

# JSON Data Transformation

Using command line instructions, users can transform JSON data to target structures.    
Examples of usage:
* Retrieve needed values from JSON objects.
* Retrieve needed values from the ledger policies. Details ate available at the [Query policies](../08-%20Blockchain%20&%20Metadata/03-%20Blockchain%20Commands.md#query-the-blockchain) 
section in the [Blockchain commands](../08-%20Blockchain%20&%20Metadata/03-%20Blockchain%20Commands.md) documentation. 
* Map source JSON data to a target structure - Details are available at the [Bring Command](#the-bring-keyword)
section in the [Message Broker](../06-%20Networking%20&%20Security/05-%20MQTT%20Message%20Broker.md) documentation.

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
    * ```bring.list``` - returns the requested keys and values in a list format.
    * ```bring.table``` - returns the requested keys and values in a table format. The bring command determines the table columns.
    * ```bring.table.sort``` - returns the values in a sorted table format. Users can specify columns id used in the sort. For example **bring.table.sort(1,0)** sorts by the second column followed by the first.
    * ```bring.count``` - returns the number of entries that satisfy the result.
    * ```bring.null``` - includes null values in the returned JSON.
    * ```bring.ip_port``` - return a comma separated list of IP and ports.
    * ```bring.min``` - return the minimum value of an attribute.
    * ```bring.max``` - return the maximum value of an attribute.
    * ```bring.list``` - return the requested attributes as a list.
    * ```bring.children``` - returns the immediate children of a policy by retrieving all policies whose `parent` attribute matches the policy's `id`.
    * ```bring.parents``` - returns the policy with a dynamic `parents` attribute containing the IDs of all policies that reference it as their immediate child.
    * ```bring.paths``` - returns the policy with all paths that contain the policy.
    * ```bring.extend``` - returns the policy extended with the policy identified by the value of its `object_id` attribute.

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
  7. Return a list of values (each value in the list is the dbms and table values from the policy, separated by a comma):   
```anylog
blockchain get tag bring.list [tag][dbms] . [tag][table]
```
  8. Return the immediate children of a policy:   
```anylog
blockchain get *  where [id] = "sub"  bring.children.table.sort(0) [*][parent] [*] [*][id] [*][parent] [*][namespace]
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

## Navigating Policy Relationships with `bring`

Policies can reference other policies to create relationships and hierarchical structures. A common example is a Unified Namespace (UNS), where `uns` policies define paths and reference `object` policies containing the metadata associated with each object.

The following `bring` extensions allow applications to navigate and resolve these relationships:

| Command | Description |
|---|---|
| `bring.extend` | Extends a policy with the policy referenced by its `object_id` |
| `bring.children` | Returns the immediate child policies of the selected policy |
| `bring.parents` | Returns the UNS policies that reference the selected object |
| `bring.paths` | Returns the complete UNS path or paths associated with an object |

Consider the following UNS hierarchy:

```text
manufacturer
    └── Caterpillar
          └── Generator
```

The hierarchy is represented by `uns` policies, while the information associated with each element is maintained in separate `object` policies.

For example:

```json
{
    "object": {
        "name": "Generator",
        "id": "85b7bcddf4e0cf05ce32f002af42d6fb"
    }
}
```

The corresponding UNS policy references the object using `object_id`:

```json
{
    "uns": {
        "namespace": "manufacturer/Caterpillar/Generator",
        "object_id": "85b7bcddf4e0cf05ce32f002af42d6fb",
        "parent": "0fa2a4130b6e132bf5d982c33b9a6204",
        "id": "e23c9eadfe2182db44252ed7b0e30ff2"
    }
}
```

This separation allows the same object to participate in different hierarchies or paths without duplicating the object metadata.

---

### `bring.extend`

`bring.extend` resolves the `object_id` referenced by a UNS policy and returns the corresponding `object` policy together with the UNS policy.

```anylog
blockchain get uns bring.extend
```

Example result:

```json
[
    {
        "uns": {
            "namespace": "manufacturer/Caterpillar",
            "object_id": "257e7557a2206c8517e913606eb56cf7",
            "parent": "06bd59ebecfa093a1015527055bed273",
            "id": "0fa2a4130b6e132bf5d982c33b9a6204"
        },
        "object": {
            "name": "Caterpillar",
            "id": "257e7557a2206c8517e913606eb56cf7"
        }
    }
]
```

The returned structure contains both:

- the `uns` policy defining the position in the hierarchy; and
- the `object` policy containing the metadata associated with that element.

For example, the root UNS policy:

```json
{
    "uns": {
        "namespace": "manufacturer",
        "object_id": "e47882f7e3f920b05ddca15c9b3aa314"
    }
}
```

can be extended with the referenced object:

```json
{
    "object": {
        "name": "manufacturer",
        "description": "Asset/provenance view: organized by manufacturer, device type, model, customer type, and customer instance.",
        "id": "e47882f7e3f920b05ddca15c9b3aa314"
    }
}
```

`bring.extend` is useful when the UNS defines the relationship or hierarchy while the object policy maintains the descriptive metadata.

---

### `bring.children`

`bring.children` returns the **immediate child policies** of the selected policy.

For example, the root of the hierarchy is:

```text
manufacturer
```

with policy ID:

```text
06bd59ebecfa093a1015527055bed273
```

To return its children:

```anylog
blockchain get * where id = 06bd59ebecfa093a1015527055bed273 bring.children
```

Result:

```json
[
    {
        "uns": {
            "namespace": "manufacturer/Caterpillar",
            "object_id": "257e7557a2206c8517e913606eb56cf7",
            "parent": "06bd59ebecfa093a1015527055bed273",
            "id": "0fa2a4130b6e132bf5d982c33b9a6204"
        }
    }
]
```

In this example:

```text
manufacturer
    └── Caterpillar
```

`Caterpillar` is returned because its UNS policy identifies the `manufacturer` policy as its parent.

`bring.children` returns the next level of the hierarchy rather than recursively returning every descendant.

---

### `bring.parents`

An object can be referenced by one or more UNS policies. `bring.parents` identifies the UNS policy or policies that reference the selected object.

For example:

```anylog
blockchain get * where id = 85b7bcddf4e0cf05ce32f002af42d6fb bring.parents
```

Result:

```json
[
    {
        "object": {
            "name": "Generator",
            "id": "85b7bcddf4e0cf05ce32f002af42d6fb"
        },
        "parents": [
            "e23c9eadfe2182db44252ed7b0e30ff2"
        ]
    }
]
```

The `parents` array contains the IDs of the UNS policies that reference the object.

In this example:

```text
85b7bcddf4e0cf05ce32f002af42d6fb
```

is the ID of the `Generator` object, while:

```text
e23c9eadfe2182db44252ed7b0e30ff2
```

is the ID of the UNS policy that places the object at:

```text
manufacturer/Caterpillar/Generator
```

An object can participate in multiple UNS hierarchies. In that case, `parents` can contain multiple UNS policy IDs.

---

### `bring.paths`

`bring.paths` resolves the complete UNS hierarchy associated with an object.

For example:

```anylog
blockchain get object where id = 85b7bcddf4e0cf05ce32f002af42d6fb bring.paths
```

The selected object is:

```text
Generator
```

and its UNS path is:

```text
manufacturer → Caterpillar → Generator
```

The result contains the object together with a `paths` object:

```json
[
    {
        "object": {
            "name": "Generator",
            "id": "85b7bcddf4e0cf05ce32f002af42d6fb"
        },
        "paths": {
            "e23c9eadfe2182db44252ed7b0e30ff2": [
                {
                    "uns": {
                        "namespace": "manufacturer",
                        "object_id": "e47882f7e3f920b05ddca15c9b3aa314",
                        "id": "06bd59ebecfa093a1015527055bed273"
                    },
                    "object": {
                        "name": "manufacturer",
                        "id": "e47882f7e3f920b05ddca15c9b3aa314"
                    }
                },
                {
                    "uns": {
                        "namespace": "manufacturer/Caterpillar",
                        "object_id": "257e7557a2206c8517e913606eb56cf7",
                        "parent": "06bd59ebecfa093a1015527055bed273",
                        "id": "0fa2a4130b6e132bf5d982c33b9a6204"
                    },
                    "object": {
                        "name": "Caterpillar",
                        "id": "257e7557a2206c8517e913606eb56cf7"
                    }
                },
                {
                    "uns": {
                        "namespace": "manufacturer/Caterpillar/Generator",
                        "object_id": "85b7bcddf4e0cf05ce32f002af42d6fb",
                        "parent": "0fa2a4130b6e132bf5d982c33b9a6204",
                        "id": "e23c9eadfe2182db44252ed7b0e30ff2"
                    },
                    "object": {
                        "name": "Generator",
                        "id": "85b7bcddf4e0cf05ce32f002af42d6fb"
                    }
                }
            ]
        }
    }
]
```

The key under `paths` is the ID of the UNS policy that references the selected object.

The array describes the complete hierarchy from the root policy to the selected object:

```text
manufacturer
    ↓
Caterpillar
    ↓
Generator
```

Each element contains both the UNS policy and its associated object policy.

---

### Objects in Multiple Paths

An important property of the AnyLog metadata model is that an object can participate in more than one hierarchy.

For example, the same `Generator` object could appear in:

```text
manufacturer → Caterpillar → Generator
```

and:

```text
City → Plant → Electricity → Generator
```

The `Generator` object does not need to be duplicated. Each UNS hierarchy can reference the same object ID:

```text
85b7bcddf4e0cf05ce32f002af42d6fb
```

In this case:

```anylog
blockchain get object where id = 85b7bcddf4e0cf05ce32f002af42d6fb bring.parents
```

can return multiple UNS policy IDs, and:

```anylog
blockchain get object where id = 85b7bcddf4e0cf05ce32f002af42d6fb bring.paths
```

can return the complete path associated with each of those UNS policies.

This allows AnyLog to maintain **multiple logical views of the same physical or logical object** while keeping the object's metadata in a single object policy.

---

### Summary

The relationship-oriented `bring` commands provide different views of the same metadata graph:

| Command | Starting Point | Returns |
|---|---|---|
| `bring.extend` | UNS policy | The UNS policy together with its referenced object policy |
| `bring.children` | Policy | Its immediate child policies |
| `bring.parents` | Object policy | UNS policy IDs that reference the object |
| `bring.paths` | Object policy | Complete root-to-object path(s), including UNS and object policies |

Together, these commands allow applications to navigate the AnyLog metadata and UNS structure without manually resolving policy IDs and parent relationships.