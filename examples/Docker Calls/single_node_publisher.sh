# Single publisher node running against SQLite
docker run --network host --name al-single-node-publisher-node --rm \
    -e NODE_TYPE=single-node-publisher \
    -e ANYLOG_SERVER_PORT=2648 \
    -e ANYLOG_REST_PORT=2649 \
    -e MASTER_NODE=10.0.0.212:2648 \
    -e DB_TYPE=sqlite \
    -e DB_USER=pi@127.0.0.1:razzburry \
    -e DB_PORT=5432 \
    -e LOCATION="0.0, 0.0" \
    -e SYNC_TIME="30 second" \
    -e COMPANY_NAME=AnyLog \
    -e NODE_NAME=anylog-single-node-publisher \
   -v al-aiops-single-node-publisher-anylog:/app/AnyLog-Network/anylog:rw \
    -v al-aiops-single-node-publisher-blockchain:/app/AnyLog-Network/blockchain:rw \
    -v al-aiops-single-node-publisher-data:/app/AnyLog-Network/data:rw \
    -v al-aiops-single-node-publisher-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -v al-aiops-single-node-publisher-scripts:/app/AnyLog-Network/scripts:rw \
    -d -it --detach-keys="ctrl-d" oshadmon/anylog:predevelop