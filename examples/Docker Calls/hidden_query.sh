# deployment of a Query node that can communicate with the network, but is not declared on it
docker run --network host --name al-hidden-query-node --rm \
    -e NODE_TYPE=hidden-query \
    -e ANYLOG_SERVER_PORT=2448 \
    -e ANYLOG_REST_PORT=2449 \
    -e MASTER_NODE=10.0.0.212:2048 \
    -e DB_TYPE=psql \
    -e DB_USER=anylog@127.0.0.1:demo \
    -e DB_PORT=5432 \
    -e SYNC_TIME="30 second" \
    -e COMPANY_NAME=AnyLog \
    -e NODE_NAME=anylog-hidden-query \
    -v al-aiops-hidden-query-anylog:/app/AnyLog-Network/anylog:rw \
    -v al-aiops-hidden-query-blockchain:/app/AnyLog-Network/blockchain:rw \
    -v al-aiops-hidden-query-data:/app/AnyLog-Network/data:rw \
    -v al-aiops-hidden-query-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -v al-aiops-hidden-query-scripts:/app/AnyLog-Network/scripts:rw \
    -it --detach-keys="ctrl-d" oshadmon/anylog:predevelop