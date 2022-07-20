# EdgeX
The demo is using EdgeX random data generator, with data being sent over their app-service-mqtt. The contents that 
changes are set to **BOLD**. 

### Steps 
1. Download our code for Linux Foundation Edge products
```shell
git clone https://github.com/AnyLog-co/lfedge-code
```

2. Update the [.env](https://github.com/AnyLog-co/lfedge-code/blob/main/edgex/.env) file in the lfedge-code/edgex 
directory with relevant MQTT configs (the example is for local deployment) - this will change the configurations in the 
docker-compose.
```dotenv
# Sample for sending data directly into the AnyLog Broker
MQTT_TOPIC=anylogedgex
MQTT_IP_ADDRESS=139.177.195.197
MQTT_PORT=32150
MQTT_USER=""
MQTT_PASSWORD=""
```

3. In docker-compose, update the [EdgeX MQTT service](https://docs.edgexfoundry.org/1.3/examples/Ch-ExamplesAddingMQTTDevice/#add-device-service-to-docker-compose-file-docker-composeyml) 
to support the changes made in the `.env` file.
```dotenv
  app-service-mqtt:
       image: ${APP_SVC_REPOSITORY}/docker-app-service-configurable${ARCH}:${APP_SERVICE_VERSION}
       ports:
         - "127.0.0.1:48101:48101"
       container_name: edgex-app-service-configurable-mqtt
       env_file:
         - common.env
       hostname: edgex-app-service-configurable-mqtt
       networks:
         edgex-network:
           aliases:
             - edgex-app-service-configurable-mqtt
       depends_on:
         - consul
         - data
       read_only: true
       security_opt:
         - no-new-privileges:true
       environment:
         EDGEX_SECURITY_SECRET_STORE: "false"
         Registry_Host: edgex-core-consul
         Clients_CoreData_Host: edgex-core-data
         Clients_Data_Host: edgex-core-data # For device Services
         Clients_Notifications_Host: edgex-support-notifications
         Clients_Metadata_Host: edgex-core-metadata
         Clients_Command_Host: edgex-core-command
         Clients_Scheduler_Host: edgex-support-scheduler
         Clients_RulesEngine_Host: edgex-kuiper
         Databases_Primary_Host: edgex-redis
         # Required in case old configuration from previous release used.
         # Change to "true" if re-enabling logging service for remote logging
         Logging_EnableRemote: "false"
         #  Clients_Logging_Host: edgex-support-logging # un-comment if re-enabling logging service for remote logging
         edgex_profile: mqtt-export
         Service_Host: edgex-app-service-configurable-mqtt
         Service_Port: 48101
         MessageBus_SubscribeHost_Host: edgex-core-data
         Binding_PublishTopic: events
         # Added for MQTT export using app service
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_ADDRESS: ${MQTT_IP_ADDRESS}
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PORT: ${MQTT_PORT}
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PROTOCOL: tcp
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_TOPIC: ${MQTT_TOPIC}
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_AUTORECONNECT: "true"
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_RETAIN: "true"
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_PERSISTONERROR: "false"
#         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PUBLISHER:
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_USER: ${MQTT_USER}
         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PASSWORD: ${MQTT_PASSWORD}
#         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_QOS: ["your quality or service"]
#         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_KEY: [your Key]  
#         WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_CERT: [your Certificate]
```

4. Deploy EdgeX
```shell
cd lfedge-code/edgex
docker-compose up -d 
```

