# Deploy an AnyLog instance of type REST without any authentication
docker run --network host --name rest-node \
  -e NODE_TYPE=rest \
  -e NODE_NAME=rest-node \
  -e COMPANY_NAME=AnyLog \
  -e ANYLOG_SERVER_PORT=2048 \
  -e ANYLOG_REST_PORT=2049 \
  -v al-aiops-rest-node-anylog:/app/AnyLog-Network/anylog:rw \
  -v al-aiops-rest-node-blockchain:/app/AnyLog-Network/blockchain:rw \
  -v al-aiops-rest-node-data:/app/AnyLog-Network/data:rw \
  -v al-aiops-rest-node-local-scripts:/app/AnyLog-Network/local_scripts:rw \
  -v al-aiops-rest-node-scripts:/app/AnyLog-Network/scripts:rw \
  -d -it --detach-keys="ctrl-d" --rm oshadmon/anylog:predevelop