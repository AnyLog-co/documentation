<new_policy = {
    "mapping": {
        "id": "my-data",
        "dbms": !default_dbms,
        "table": "my_data",
        "group_by_attributes": ["device_name"],
        "readings": "",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]"
            },
            "device_name": {
                "type": "string",
                "bring": "[device_name]"
            },
            "value": {
                "type": "float",
                "bring": "[value]"
            }
        }
    }
}>


process !local_scripts/node-deployment/policies/publish_policy.al

<run msg client where
    broker=local and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name="sensors/#" and
        policy="my-data" and
        dynamic=true
    )>