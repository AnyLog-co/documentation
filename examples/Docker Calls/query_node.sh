# deployment of a standard Query node
docker run --network host --name al-query-node --rm \
    -e NODE_TYPE=query \
    -e ANYLOG_SERVER_PORT=2348 \
    -e ANYLOG_REST_PORT=2349 \
    -e MASTER_NODE=10.0.0.212:2048 \
    -e DB_TYPE=psql \
    -e DB_USER=anylog@127.0.0.1:demo \
    -e DB_PORT=5432 \
    -e SYNC_TIME="30 second" \
    -e COMPANY_NAME=AnyLog \
    -e NODE_NAME=anylog-query \
    -v al-aiops-query-anylog:/app/AnyLog-Network/anylog:rw \
    -v al-aiops-query-blockchain:/app/AnyLog-Network/blockchain:rw \
    -v al-aiops-query-data:/app/AnyLog-Network/data:rw \
    -v al-aiops-query-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -v al-aiops-query-scripts:/app/AnyLog-Network/scripts:rw \
    -d -it --detach-keys="ctrl-d" oshadmon/anylog:predevelop