# Configure MQTT TLS and authentication

## Create CA Authority for self signed TLS certificates

```text
<id generate certificate authority where country = US and
  state = CA and locality = "Redwood City" and
  org = AnyLogCA_TLS and
  output_name = "AnyLogCA_TLS" and
  expiration_days = 3650
>
```

## Create certificate request

```text
<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = "Anylog MQTT broker TLS"
  and hostname = op1
  and alt_name = 192.168.1.60
  and ip = 192.168.1.60 and
  output_name = "server-mqtt-op1"
>
```

## Sign certificate with above CA

```text
<id sign certificate request where ca_org = AnyLogCA_TLS and ca_output_name = "AnyLogCA_TLS"
  and server_org = "Anylog MQTT broker TLS" and output_name = "server-mqtt-op1"
  and expiration_days = 3650
>
```

Writes under `!pem_dir`: `AnyLogCA_TLS.crt` / `.key`, `server-mqtt-op1.csr` / `.key` / `.pem`, then `server-mqtt-op1.crt`.

## Start MQTT broker

```text
<run message broker where external_ip = 192.168.1.60 and external_port = 8883 and threads = 6
  and enable_tls = true
  and tls_cert = ./data/pem/server_tls.crt
  and tls_key = ./data/pem/server_tls.key
  and users_ca = ./data/pem/CA_users.crt
  and allowed_users = (user1, user2)
>
```

`allowed_users` is optional. When set, `user1`, `user2`, etc. are the **CN** values in the client certificates that are allowed to connect.

Notes:

- Creating self-signed certificates `server_tls.key` / `server_tls.crt` requires a signing CA, e.g. `AnyLogCA_TLS`.
- The certificate requires IP address(es) and/or a domain name, for example:
  - `IPAddress:192.168.1.60`
  - `DNS:localhost`
- `users_ca` (`CA_users.crt`) is the CA public certificate used to authenticate MQTT clients (mTLS). It is generally provided by the organization that connects with user certificates issued by that CA — not the same file as the broker listener CA (`AnyLogCA_TLS`).

All the above commands are issued on an operator node, say `op1`.

## Create user certificates for an organization

If the organization that wants to connect to the AnyLog MQTT TLS broker does **not** have user certificates, create them and pass the following to the organization:

- `user*.crt` / `user*.key` (one pair per user; CN matches `allowed_users`, e.g. `user1`, `user2`)
- `AnyLogCA_TLS.crt` (broker TLS CA **public** key — so the client can trust the broker)

Do not share any other private key with the organization.

Example on the operator:

```text
<id generate certificate authority where country = US and
  state = CA and locality = "Redwood City" and
  org = CA_users and
  output_name = "CA_users" and
  hostname = CA_users and
  expiration_days = 3650
>

<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = AnyLog and hostname = user1 and output_name = "user1"
>

<id sign certificate request where ca_org = CA_users and ca_output_name = "CA_users"
  and server_org = AnyLog and output_name = "user1" and expiration_days = 825
>

<id generate certificate request where country = US and state = CA and locality = "Redwood City"
  and org = AnyLog and hostname = user2 and output_name = "user2"
>

<id sign certificate request where ca_org = CA_users and ca_output_name = "CA_users"
  and server_org = AnyLog and output_name = "user2" and expiration_days = 825
>
```

Give the organization: `user1.crt` / `user1.key`, `user2.crt` / `user2.key`, and `AnyLogCA_TLS.crt` only. Keep all other keys and CA material on the AnyLog side (`users_ca` still points at `CA_users.crt` on the broker).

## Create local broker for ingestion

For a given topic (`my_topic`) or all topics:

```text
<run msg client where broker = local and
       topic = (name = my_topic and
       dbms = mydb and
       table = my_topic and
       column.payload.str = "bring [value]")
>
```

## Publish data from a client using TLS and user certificate

```bash
mosquitto_pub -p 8883 -h 192.168.1.60 \
  --cafile ./AnyLogCA_TLS.crt \
  --cert ./user1.crt \
  --key ./user1.key \
  -d \
  -m '{"value":"enabled"}' \
  -t test2
```

Note: `--cafile ./AnyLogCA_TLS.crt` may be required if the client application cannot trust the self-signed certificate used for the AnyLog broker TLS listener.

### MQTT Explorer client setup

In MQTT Explorer, configure the connection to `mqtt://192.168.1.60:8883/` with:

- **SERVER CERTIFICATE (CA):** `AnyLogCA_TLS.crt` (or the broker listener CA)
- **CLIENT CERTIFICATE:** e.g. `user1.crt` / `AnyLogUser1.crt`
- **CLIENT KEY:** e.g. `user1.key` / `AnyLogUser1.key`

![MQTT Explorer TLS setup](../imgs/mqtt_explorer_setup.png)

## Share CA Users in the blockchain

If we have the public key for CA Users, we can publish it as a `ca` policy and load `users_ca` from the blockchain:

```text
master_node = <IP>:32048

<policy = {"ca":{"name":"CUSTOMER_CA_users","company":"CUSTOMER company","usage":"mqtt_users","certificate":"-----BEGIN CERTIFICATE-----SOME_BYTES----END CERTIFICATE-----\n"}}
>

blockchain prepare policy !policy

blockchain insert where policy = !policy and local = true and master = !master_node

blockchain get ca where name = CUSTOMER_CA_users

blockchain get ca where name = CUSTOMER_CA_users bring [ca][certificate]

users_ca = blockchain get ca where name = CUSTOMER_CA_users bring [ca][certificate]

<run message broker where external_ip = 192.168.1.60 and external_port = 8883 and threads = 6
  and enable_tls = true
  and tls_cert = /path_to/server_tls.crt
  and tls_key = /path_to/server_tls.key
  and users_ca = !users_ca
  and allowed_users = (user1, user2)
>
```

## Link to resources

- [mosquitto-tls man page](https://mosquitto.org/man/mosquitto-tls-7.html)
- [Mosquitto broker TLS config (Medium)](https://medium.com/@sonadorje/mosquitto-broker-tls-config-5f8bfaa5c047)
