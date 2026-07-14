# DNP3

AnyLog can act as a **DNP3 master** over **TCP** or **TLS** (using **hostname** and **port**, default **20000**). Data is read on a schedule and streamed into your local operator database as JSON, using the same **`run plc client`** pattern as [Modbus](https://github.com/AnyLog-co/documentation/blob/pre-develop/07-%20Southbound%20Interfaces/A-%20Direct%20-%20Built-in%20connectors%20(protocols%20AnyLog%20natively%20accepts%20from%20devices)/MODBUS.md), OPC UA, and EtherNet/IP.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **`opendnp3` (yadnp3)** | Must be installed in the AnyLog runtime environment. |

Declare the target DBMS before streaming, for example:

```anylog
connect dbms new_company where type = sqlite
```

---

## Connection and map

DNP3 uses **`hostname`** and **`port`**. **`master_id`** and **`outstation_id`** are the DNP3 link addresses (defaults: master **1**, outstation **10**).

**`map`** is a **JSON array** of points. Each object must include:

| Key | Required | Meaning |
|---|---|---|
| `name` | yes | Column / logical label |
| `index` | yes | Point index on the outstation |
| `type` | one of `type` or `group`+`variation` | Point class (see table below) |
| `group`, `variation` | alternative to `type` | Raw DNP3 group/variation |

Supported **`type`** values (case-insensitive; spaces/underscores ignored):

| `type` | DNP3 group / variation |
|---|---|
| `Analog` | 30 / 6 |
| `Binary` | 1 / 2 |
| `BinaryOutputStatus` | 10 / 2 |
| `AnalogOutputStatus` or `AnalogOutput` | 40 / 4 |
| `Counter` | 20 / 6 |
| `DoubleBit` or `DoubleBitBinary` | 3 / 2 |

Optional **TLS** (all three PEM paths required when `enable_tls = true`):

| Keyword | Meaning |
|---|---|
| `enable_tls` | Use TLS instead of plain TCP |
| `tls_ca` | CA certificate (PEM file path) |
| `tls_cert` | Client certificate (PEM file path) |
| `tls_key` | Client private key (PEM file path) |

---

## One-shot read

```anylog
<get plc values where type = dnp3 and
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    map = [{"name":"analog_0","type":"Analog","index":0},
           {"name":"binary_0","type":"Binary","index":0},
           {"name":"counter_0","type":"Counter","index":0},
           {"name":"doublebit_0","type":"DoubleBit","index":0}]
>
```

Alias: **`get dnp3 values`** (same keywords).

With TLS (certificates from `certs/ca_chain/` — see [DNP3 Out Station Testing](#dnp3-out-station-testing)):

```anylog
<get dnp3 values where
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    enable_tls = true and
    tls_ca = certs/ca_chain/anylogDNP3ca.cert and
    tls_cert = certs/ca_chain/master1.cert and
    tls_key = certs/ca_chain/master1.key and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

---

## Continuous ingest — wide table (default)

With **`table = ...`** and **`dbms`**, all points from **`map`** land in **one table**. Each poll inserts **one row**; every object in **`map`** is **one column**: the map **`name`** is the **column name**, and that column stores the value read for that point.

```anylog
<run plc client where type = dnp3 and
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    frequency = 20 and
    name = dnp3_rtu and
    dbms = new_company and
    table = substation and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

---

## Continuous ingest — dynamic tables (`dynamic = true`)

Omit **`table`** and omit **`namespace`** for plain dynamic ingest. Each object in **`map`** is written to its **own table**. The table name is derived from the client **`name`** and the map **`name`** (for example, **`dnp3_rtu_analog_0`** when **`name = dnp3_rtu`** and the map entry’s **`name`** is **`analog_0`**). Each row includes **`timestamp`**, **`tag`**, and **`value`**.

```anylog
<run plc client where type = dnp3 and
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    frequency = 20 and
    name = dnp3_dyn and
    dbms = new_company and
    dynamic = true and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

---

## Dynamic ingest with UNS (`namespace` + `master_node`)

With **`dynamic = true`**, you can add a **Unified Namespace** path and a **master node** so DNP3 ingest is registered in the UNS alongside your policies and DBMS. **`namespace`** requires **`master_node = [ip:port]`** for policy updates.

```anylog
run plc client where type = dnp3 and
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    frequency = 20 and
    name = dnp3_uns and
    dbms = new_company and
    dynamic = true and
    master_node = 192.168.1.88:32048 and
    namespace = FA9/MID9/DEVICE9 and
    map = [{"name":"analog_0","type":"Analog","index":0}]
```

**Table names** follow the same pattern as plain **`dynamic = true`** (client **`name`** plus map **`name`**). Under UNS, layout follows **UNS policies** — see [Unified Namespace](https://github.com/AnyLog-co/documentation/tree/pre-develop/11-%20UNS%20%28Unified%20Name%20Spaces%29) in the AnyLog documentation.

---

## DNP3 Out Station Testing

The [opendnp3](https://github.com/dnp3/opendnp3) library includes a demo outstation for lab tests. Build it with demos enabled (TLS optional):

```bash
git clone --recursive -b release-2.x https://github.com/dnp3/opendnp3.git
cd opendnp3
mkdir build && cd build
cmake -DDNP3_DEMO=ON -DDNP3_TLS=ON ..    # omit -DDNP3_TLS=ON for TCP-only
make -j
```

See the [OpenDNP3 CMake guide](https://dnp3.github.io/docs/guide/3.0.0/build/cmake/) and [TLS support](https://dnp3.github.io/docs/guide/3.0.0/api/tls/) (OpenSSL ≥ 1.1.1 required for TLS).

### Plain TCP outstation

From the opendnp3 build directory:

```bash
cd ~/opendnp3/build
./outstation-demo
```

The demo listens on **any IP address**, port **20001**, outstation link id **10**, and expects master link id **1**. Use those values in AnyLog:

```anylog
<get dnp3 values where type = dnp3 and
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    map = [{"name":"analog_0","type":"Analog","index":0},
           {"name":"binary_0","type":"Binary","index":0},
           {"name":"counter_0","type":"Counter","index":0},
           {"name":"doublebit_0","type":"DoubleBit","index":0}]
>
```

Once started, the demo logs traffic and waits for input to send unsolicited measurement changes:

```text
Enter one or more measurement changes then press <enter>
c = counter, b = binary, d = doublebit, a = analog, o = octet string, 'quit' = exit
```

### TLS outstation

Generate test certificates first:

```bash
cd certs/ca_chain
bash create_certificates.sh
```

| Side | CA (peer) | Certificate | Private key |
|------|-----------|-------------|-------------|
| AnyLog master | `anylogDNP3ca.cert` | `master1.cert` | `master1.key` |
| Outstation | `anylogDNP3ca.cert` | `outstation1.cert` | `outstation1.key` |

From the opendnp3 build directory, start the TLS demo with three PEM paths (CA, outstation certificate, outstation private key):

```bash
cd ~/opendnp3/build
./outstation-tls-demo \
  /path/to/AnyLog-Network/certs/ca_chain/anylogDNP3ca.cert \
  /path/to/AnyLog-Network/certs/ca_chain/outstation1.cert \
  /path/to/AnyLog-Network/certs/ca_chain/outstation1.key
```

Same link ids and port as plain TCP (**master_id = 1**, **outstation_id = 10**, port **20001**). AnyLog master uses the **master** certificate files from the same CA chain:

Example AnyLog one-shot read:

```anylog
<get dnp3 values where type = dnp3 and
    hostname = 127.0.0.1 and
    port = 20001 and
    master_id = 1 and
    outstation_id = 10 and
    enable_tls = true and
    tls_ca = certs/ca_chain/anylogDNP3ca.cert and
    tls_cert = certs/ca_chain/master1.cert and
    tls_key = certs/ca_chain/master1.key and
    map = [{"name":"analog_0","type":"Analog","index":0}]
>
```

More detail: [certs/ca_chain/README.md](certs/ca_chain/README.md).

### Third-party simulator

Another option is a commercial DNP3 outstation simulator, for example the [FreyrSCADA DNP3 development bundle](http://freyrscada.com/dnp3-ieee-1815-Client-Simulator.php#Download-DNP3-Development-Bundle). After download, **DNPOutstationSimulator.exe** under the **Simulator** folder can be installed on Windows (32-bit).

---

## Command keywords (summary)

| Keyword | Required / notes |
|---|---|
| `type` | `dnp3` |
| `hostname`, `port` | DNP3 TCP/TLS target (default port **20000**) |
| `master_id` | Master link address (default **1**) |
| `outstation_id` | Outstation link address (default **10**) |
| `frequency` | Poll interval (seconds) |
| `name` | Unique client name |
| `dbms` | Target DBMS |
| `table` | Wide-table ingest; omit with **`dynamic = true`** |
| `dynamic` | `true` for per-map tables or UNS |
| `map` | JSON array of points |
| `namespace` | UNS path (DNP3 + **`dynamic = true`** only) |
| `master_node` | Required when **`namespace`** is set |
| `enable_tls`, `tls_ca`, `tls_cert`, `tls_key` | Optional TLS (all three PEM paths required) |
