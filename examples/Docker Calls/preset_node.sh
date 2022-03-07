# Deploys a node with preset TCP/REST network configurations. User can manually include authentication (as shown)
docker run --network host --name preset-node \
  -e AUTHENTICATION=true \
  -e USERNAME=anylog \
  -e PASSWORD=demo \
  -e AUTH_TYPE=admin \
  -v al-aiops-preset-node-anylog:/app/AnyLog-Network/anylog:rw \
  -v al-aiops-preset-node-blockchain:/app/AnyLog-Network/blockchain:rw \
  -v al-aiops-preset-node-data:/app/AnyLog-Network/data:rw \
  -v al-aiops-preset-node-local-scripts:/app/AnyLog-Network/local_scripts:rw \
  -v al-aiops-preset-node-scripts:/app/AnyLog-Network/scripts:rw \
  -d -it --detach-keys="ctrl-d" --rm oshadmon/anylog:predevelop