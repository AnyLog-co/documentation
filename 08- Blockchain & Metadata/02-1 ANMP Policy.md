---
title: "ANMP Policy"
description: "AnyLog policy extension logic"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | created document | 2025 |
--->

# ANMP Policy

Blockchain policies are immutable, meaning they cannot be manipulated. However, networking configurations, processes, 
and other parameters are not immutable — they change over time. As such, the metadata needs to change accordingly.

The AnyLog Network Management Policy (ANMP) is used to modify existing policies.

An ANMP policy modifies only the attributes referenced by policy_id — it never touches the original policy's 
type-defining wrapper key, so a publisher policy cannot literally become an operator policy through ANMP.

However, ANMP performs no schema validation: it will accept attribute changes that don't match the target policy's 
original type (e.g. adding a cluster ID to a non-operator policy). Doing so does not make the node behave as that type — 
actual role behavior is determined by which logical databases and services are active on the node, not by policy 
metadata. An engineer patching in mismatched attributes can produce an inconsistent or misleading policy record without 
granting the node any new real capability.

As such, the ANMP policy is intended for updating existing parameters — such as networking configs, updating the node 
name / owner, and enhancing the reference list of certain UNS policies. It should not be used to redefine node type or 
to patch in attributes belonging to a different policy type — doing so does not change actual node behavior and only 
risks creating a misleading or inconsistent policy record.

**Related Topics**:
* [Policy & Metadata](02-%20Policy%20%26%20Metadata.md)
* [Blockchain Full Circle](03-1%20Blockchain%20Full%20Circle.md)
* [Network Processing](../06-%20Networking%20%26%20Security/02-%20Network%20Processing.md)

## ANMP vs Other Policies 

An _ANMP_ policy is different from other policies in that it enhances the other policies, as such there's a layer between 
policy type and its metadata information, whereas with regular policies there is not. 

**Example**: 

* Regular Policy:

```json
{
  "<POLICY_TYPE>": {
    "<key>": "<value>" <-- metadata information
  }
}
```

* ANMP Policy 
```json
{
  "anmp": {
    "<original policy ID>": {
      "<key>": "<value>" <-- metadata information
    }
  }
}
```

## Sample Logic  

The following demonstrates that the IP address of the node has changed from IPv6 to DNS-based. 

1. User defines a node

```anylog
<operator_policy={'operator': {
   'hostname' : !hostname,
   'name' : !node_name',
   'ip': !external_ip,
   'company':  !company_name,
   'port': !anylog_server_port.int,
   'rest_port': !anylog_rest_port.int,
   'cluster': !cluster_id
}}>

blockchain insert where policy = !operator_policy and local = true and master = !ledger_conn 
```

2. The User notices the external IP changed from `172.16.3.32` to `172.16.3.36` and wants to use a static DNS format instead

3. Define an AMNP policy with the new IP address 

* get ID of old Policy 
```anylog 
policy_id = blockchain get operator where ip = !external_ip  and port = !anylog_server_port.int bring [operator][id]
```

* Define new policy 
```anylog 
<anmp = {"anmp" : {
   !policy_id : {
      "ip" : "dev.acme.example.com",
      "local_ip": !ip      
   }
}}>
```

> **Notice the `anmp` policy has only 1 child (the original `!policy_id`) rather than a direct conversion of the 
> original policy.** The original `operator` policy is never rewritten — the `anmp` policy is a separate record, 
> keyed by the ID it modifies, that supplies only the attributes being changed.

## Extending a List Attribute

The same mechanism applies when the modified attribute is a list rather than a scalar. Where a scalar attribute 
(e.g. `ip`) is **replaced**, a list attribute is **extended** — if the attribute already exists on the target 
policy, the new value(s) are appended to it; if it does not yet exist, it is created.

**Example**: A `uns` policy for customer `Sabetha` references a device it does not own via `ref_id`. A second 
Caterpillar-manufactured device is later identified at Sabetha and needs to be added to that same list.

* get ID of the target policy
```anylog
policy_id = blockchain get uns where name = Sabetha and company = Caterpillar bring [uns][id]
```

* define the ANMP policy
```anylog
<anmp = {"anmp" : {
   !policy_id : {
      "ref_id": [!new_device_id]
   }
}}>

blockchain insert where policy = !anmp and local = true and master = !ledger_conn
```

If `ref_id` already exists on `!policy_id`, `!new_device_id` is appended to the existing list. If `ref_id` does 
not yet exist, it is created with `!new_device_id` as its first (and only) entry.