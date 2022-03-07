# Deploy an empty AnyLog instance
docker run --network host --name empty-node \
  -e NODE_TYPE=none \
  -v al-aiops-empty-node-anylog:/app/AnyLog-Network/anylog:rw \
  -v al-aiops-empty-node-blockchain:/app/AnyLog-Network/blockchain:rw \
  -v al-aiops-empty-node-data:/app/AnyLog-Network/data:rw \
  -v al-aiops-empty-node-local-scripts:/app/AnyLog-Network/local_scripts:rw \
  -v al-aiops-empty-node-scripts:/app/AnyLog-Network/scripts:rw \
  -d -it --detach-keys="ctrl-d" --rm oshadmon/anylog:predevelop