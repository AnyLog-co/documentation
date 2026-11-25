---

title: Modbus TCP
description: Pull coils, discrete inputs, and holding/input registers from Modbus TCP devices into AnyLog using run plc client.
layout: page
source_path: "02 MODBUS.md"
---



AnyLog can act as a **Modbus TCP client** (over `hostname` and `port`, typically port **502**). Data is read on a 
schedule and streamed into your local operator database as JSON, using the same `run plc client` pattern as 
[OPC-UA](./03-%20OPC-UA.md) and [EtherNet/IP](./04-%20EtherIP.md#the-run-plc-client-command).

---

## Prerequisites

| Requirement    | Notes                                                |
| -------------- | ---------------------------------------------------- |
| `pymodbus` | Must be installed in the AnyLog runtime environment. |

Declare the target DBMS before streaming, for example:

```anylog
connect dbms modbus_sensors where type = sqlite
```

---

## Connection and map

AnyLog only reads values from the Modbus device and it never writes to coils or registers.  
The **Device access** column below describes what the device allows, not what AnyLog does.

Modbus uses `hostname` and `port` (not `url`). `device_id` is the **Modbus PDU unit id** (often `0` or `1` on TCP). `map` is a **JSON array** of points; each object must include a `name` (column / logical label) and exactly one address field:

| Key | Kind | Size | Modbus function | Device access | Meaning |
|---|---|---|---|---|---|
| `coil` | Bit | 1 bit | FC 1 (read coils) | Read and write | Coil (0-based address) |
| `input` | Bit | 1 bit | FC 2 (read discrete inputs) | Read only | Discrete input (0-based address) |
| `register` | Word | 16 bits per register | FC 3 (read holding registers) | Read and write | Holding register (single address or list for blocks) |
| `inputRegister` | Word | 16 bits per register | FC 4 (read input registers) | Read only | Input register (single address or list for blocks) |

### Bits: coils and discrete inputs

A **coil** and a **discrete input** are both bits. Each one holds a single on/off value, read as `0` or `1`. They differ in who controls them:

* A **coil** is an output on the device, such as a relay or an alarm flag. A Modbus master can write it, and the device's own logic can change it too. AnyLog only reads coils, with `coil`.
* A **discrete input** is an input to the device, such as a door contact or a limit switch. Only the device sets it. AnyLog reads it with `input`.

Bit items are emitted as `0` or `1`.

### Words: holding registers and input registers

A **holding register** and an **input register** are both 16-bit words. Each one holds a whole number from 0 to 65535. A list of registers can be combined into a larger value with `type` (for example `float` from two registers, or `long` from four). They differ in who controls them:

* A **holding register** is read and write on the device, so it is used for settings and setpoints as well as values. AnyLog reads it with `register`.
* An `input` `register` is read only, and is normally used for sensor measurements. AnyLog reads it with `inputRegister`.

### Addresses in the device manual

Device manuals often number the Modbus objects in ranges: coils `00001`–`09999`, discrete inputs `10001`–`19999`, input registers `30001`–`39999` and holding registers `40001`–`49999`.   

The `coil`, `input`, `inputRegister` and `register` values in the map are the Modbus addresses, so check your manual for the address base: a coil listed as `00001` is usually address `0` in the map.

---

In AnyLog, we use a map (a JSON array of points).  
Each point has a `name` (the column name) and a Modbus key (`input`, `coil`, `inputRegister` or `register`) that tells the client where to read the value from.  
Other keys such as `type`, `scale`, `offset`, `formula` and `value` (for constants) are optional.

```json
[{"name":"door_open","input":0},
 {"name":"alarm_active","coil":0},
 {"name":"motor_current","inputRegister":5396},
 {"name":"temperature_setpoint","register":101}]
```

---

## One-shot read

This map has one item for each address key: `register`, `inputRegister`, `coil` and `input`. It is a JSON array of four elements:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"door_open","input":0},
           {"name":"alarm_active","coil":0},
           {"name":"motor_current","inputRegister":5396},
           {"name":"temperature_setpoint","register":101}]
>
```

Alias: `get modbus values` (same keywords).

```
Modbus TCP values
Column               Tag     Value Error Note 
--------------------|-------|-----|-----|----|
door_open           |di:0   |    0|     |    |
alarm_active        |c:0    |    1|     |    |
motor_current       |ir:5396|   17|     |    |
temperature_setpoint|hr:101 |22860|     |    |
```

The **Tag** prefix shows the Modbus object: `hr:` is a holding register, `ir:` an input register, `c:` a coil and `di:` a discrete input. The simulator defines only holding registers, so the input register, coil and discrete input return `0`. Those rows show the format only.

## Mapping with type

`type` decodes one or more registers into one value. There are three types:

* `float`: two registers form one 32-bit IEEE 754 float.
* `long`: one to four registers form one signed integer. Two registers give 32 bits, four give 64 bits.
* `byte`: more than four registers. The result is a list, one 16-bit value per register.

Without `type`, one register is an unsigned 16-bit value.

Holding registers on the simulator, with the values the node returns:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"pressure","register":[5397,5398],"type":"long"},
           {"name":"counter","register":[5399,5400,5401,5402],"type":"long"},
           {"name":"block_bytes","register":[5409,5410,5411,5412,5413],"type":"byte"},
           {"name":"humidity","register":5396}]
>
```

```
Modbus TCP values
Column      Tag       Value                     Error Note 
-----------|---------|-------------------------|-----|----|
temperature|hr:5394+2|                     23.5|     |    |
pressure   |hr:5397+2|               1149063168|     |    |
counter    |hr:5399+4|               1234567890|     |    |
block_bytes|hr:5409+5|[100, 200, 300, 400, 500]|     |    |
humidity   |hr:5396  |                      452|     |    |
```

* `temperature` is a float from two registers: `23.5`.
* `pressure` is a long from two registers: `1149063168`.
* `counter` is a long from four registers: `1234567890`.
* `block_bytes` is a byte over five registers: a list of five values.
* `humidity` has no `type`, so raw value is `452`.

The same types work on input registers. The simulator defines only holding registers, so input registers return `0`:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"temperature","inputRegister":[5394,5395],"type":"float"},
           {"name":"pressure","inputRegister":[5397,5398],"type":"long"}]
>
```

```
Modbus TCP values
Column      Tag       Value Error Note 
-----------|---------|-----|-----|----|
temperature|ir:5394+2|  0.0|     |    |
pressure   |ir:5397+2|    0|     |    |
```

---

## Scale, offset and convert

These options change a value after it is read. They apply to `register` and `inputRegister` items only. The steps run in this order: `swap`, `type`, `scale` and `offset`, then `convert`.

The examples in this section were run against the AnyLog Modbus simulator (`hostname = 127.0.0.1`, `port = 1502`, `device_id = 1`).

### Scale and offset (`scale`, `offset`)

`scale` multiplies the value and `offset` adds to it: `value * scale + offset`. You can use either one alone.

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"humidity_pct","register":5396,"scale":0.1},
           {"name":"temperature_k","register":[5394,5395],"type":"float","offset":273.15},
           {"name":"adjusted","register":5404,"scale":0.01,"offset":-100},
           {"name":"model_text","register":[5406,5407,5408],"convert":"string"}]
>
```

```
Modbus TCP values
Column        Tag       Value  Error Note 
-------------|---------|------|-----|----|
humidity_pct |hr:5396  |  45.2|     |    |
temperature_k|hr:5394+2|296.65|     |    |
adjusted     |hr:5404  |245.61|     |    |
model_text   |hr:5406+3|ANYLOG|     |    |
```

* `humidity_pct`: the register holds `452`, and `scale` `0.1` gives `45.2`.
* `temperature_k`: the float `23.5` plus `offset` `273.15` gives `296.65`.
* `adjusted`: the register holds `34561`. `scale` `0.01` gives `345.61`, and `offset` `-100` gives `245.61`.

Rules:

* `scale` and `offset` must be numbers. Any other value rejects the whole command.
* The result is a decimal number. `offset` alone on the register `452` returns `402.0`.
* Without `type`, a list of several registers is not scaled. `[100, 200]` with `scale` `0.5` and `offset` `10` returns `[100, 200]`. Use `type`, `formula` or `outputs` instead.
* `scale` and `offset` are not applied to text. With `convert` `"string"`, the text is returned unchanged.
* Do not combine `scale` or `offset` with `formula` on the same item. The formula does the calculation instead; see [Formulas](#formulas).
* Floating-point arithmetic can add noise. For example, the float `23.5` with `offset` `-273.15` returns `-249.64999999999998`.

### Text from registers (`convert`)

With `"convert":"string"`, each register holds two characters, high byte first:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"model_text","register":[5406,5407,5408],"convert":"string"}]
>
```

```
Modbus TCP values
Column     Tag       Value  Error Note 
----------|---------|------|-----|----|
model_text|hr:5406+3|ANYLOG|     |    |
```

`"convert":"raw"` keeps the number as it is, the same as leaving `convert` out. The register `452` returns `452`.

---

## Word order (`swap`)

`swap` reorders the words before `type`, `scale`, `offset`, `convert` or a `formula` runs. The registers hold `100` and `200`; with `"swap":"words"` they are read as `200`, `100`:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"swapped","register":[5409,5410],"swap":"words","formula":"x[0] * 1000 + x[1]"}]
>
```

```
Modbus TCP values
Column  Tag       Value  Error Note 
-------|---------|------|-----|----|
swapped|hr:5409+2|200100|     |    |
```

Without `swap`, the same formula gives `100200`.

The three `swap` values are `bytes`, `words`, and `both`. Any other value returns an error. The table shows the output on the simulator:

| Registers | `swap` | Value |
|---|---|---|
| `[5409, 5410]` | none | `[100, 200]` |
| `[5409, 5410]` | `bytes` | `[25600, 51200]` |
| `[5409, 5410]` | `words` | `[200, 100]` |
| `[5409, 5410]` | `both` | `[51200, 25600]` |
| `5396` | none | `452` |
| `5396` | `bytes` | `50177` |
| `5396` | `words` | `452` |
| `5396` | `both` | `50177` |

With one register, `words` has no effect. `bytes` and `both` give the same result.

---

## Formulas

A `register` or `inputRegister` map item can carry a `formula`: a math expression that converts the raw register value into the value you want. The formula runs on every read, in `get plc values` and in `run plc client`.

```json
{"name":"humidity_pct","register":5396,"formula":"0.1 * x"}
```

### What `x` is

The raw words are processed in this order: `swap` → `type` → `formula`. `x` is the result of the first two steps:

| Map item                       | `x` is                                                              |
| ------------------------------ | ------------------------------------------------------------------- |
| One register, no `type`        | The unsigned 16-bit value (0 to 65535)                              |
| `"type":"long"`                | The signed integer (1 to 4 consecutive registers)                   |
| `"type":"float"`               | The IEEE 754 float (2 consecutive registers)                        |
| A list of registers, no `type` | The list of 16-bit words; use `x[0]`, `x[1]`, ... (0-based) |

### What a formula can contain

| Element | Allowed |
|---|---|
| Numbers and `x` | Integers and decimals; `x[i]` with an integer index |
| Operators | `+` `-` `*` `/` `//` (floor division) `%` (modulo) `**` (power), parentheses, unary `-` |
| Functions | `sin` `cos` `tan` `asin` `acos` `atan` `atan2` `sqrt` `log` `log10` `log2` `ln` `exp` `abs` `min` `max` `round` `pow` |
| Constants | `pi` `e` `tau` |

`log` and `ln` are both the natural logarithm; use `log10` or `log2` for the other bases. The absolute value of an exponent (`**` or `pow`) is limited to 10000. Strings, other variable names, attribute access and any other function calls are rejected.

### Rules

* Formulas apply to `register` and `inputRegister` items only. `coil` and `input` items do not support modifiers.
* A `formula` replaces `convert`, `scale` and `offset`. Using them on the same item is rejected with `formula is used instead of convert, scale, and offset`.
* The expression is checked when the command is issued. A syntax error, an unknown name, or a call to a function that is not in the list above rejects the whole command with a message such as `Modbus: map item 't': formula: unknown name 'foo'`.
* A formula that fails while reading (for example a division by zero) returns no value for that point. The Error column shows the reason, such as `decode error: division by zero`. The other points of the command are still returned.
* A register can be used by one map item only. If two items read the same register, the first one is silently dropped and only the last one is returned. In the test, `first` (`0.1 * x`) and `second` (plain) both read `5396`, and only `second` came back (`452`). To derive several values from one block, use `outputs`.

### How formulas evaluate

These results are the formula engine's output for the given `x`. They do not come from a device:

| Formula | Raw register(s) | Result |
|---|---|---|
| `-50 + 0.02 * x` | `x = 1000` | `-30.0` |
| `x % 256` (low byte) | `x = 513` | `1` |
| `x // 256` (high byte) | `x = 513` | `2` |
| `20 * log10(x)` | `x = 100.0` | `40.0` |
| `20 * x[0] + 50 * x[1]` | registers `[3, 2]` | `160` |
| `round(0.1 * x, 1)` | `x = 1234` | `123.4` |
| `max(x[0], x[1])` | registers `[4, 9]` | `9` |

---

## Map examples (`get plc values`)

The examples in this section and the next ones were run against the AnyLog Modbus simulator (`hostname = 127.0.0.1`, `port = 1502`, `device_id = 1`). The simulator holds these registers:

| Registers | Content |
|---|---|
| 5394–5395 | Float `23.5` (temperature) |
| 5396 | `452` |
| 5397–5398 | Float `1013.25` |
| 5399–5402 | Long `1234567890` |
| 5403 | `87` (a status word) |
| 5404 | `34561` |
| 5406–5408 | Text `ANYLOG` |
| 5409–5412 | `100`, `200`, `300`, `400` |

Only holding registers are defined on this simulator. The examples use holding registers only.

## Formulas on the map

One-shot read with three formulas: a single register scaled, a float converted to Fahrenheit, and two registers combined:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"temperature_f","register":[5394,5395],"type":"float","formula":"round(x * 1.8 + 32, 1)"},
           {"name":"mix","register":[5409,5410],"formula":"20 * x[0] + 50 * x[1]"}]
>
```

```
Modbus TCP values
Column        Tag       Value Error Note 
-------------|---------|-----|-----|----|
humidity_pct |hr:5396  | 45.2|     |    |
temperature_f|hr:5394+2| 74.3|     |    |
mix          |hr:5409+2|12000|     |    |
```

* `humidity_pct`: the register holds `452`, and `0.1 * x` gives `45.2`.
* `temperature_f`: `type` `float` first turns the two registers into `23.5`, then the formula gives `74.3`.
* `mix`: the two registers hold `100` and `200`, so `20 * 100 + 50 * 200 = 12000`.
* Floating-point arithmetic can add noise: without `round`, the `temperature_f` formula returns `74.30000000000001`. Use `round(..., n)` to keep the stored value clean.

---

## Several values from one register block (`outputs`)

When a device packs several values in consecutive registers, read the block once and derive each column with its own formula. The block item lists the registers and an `outputs` array of `{"name": ..., "formula": ...}`. In each formula, `x[i]` is register `i` of the block (0-based), after the block's `swap`. Each output becomes a column named by its `name`.

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"island_inputs",
            "register":[5409,5410,5411,5412],
            "outputs":[{"name":"sum_01","formula":"x[0] + x[1]"},
                       {"name":"half_2","formula":"0.5 * x[2]"},
                       {"name":"max_all","formula":"max(x[0], x[1], x[2], x[3])"}]}]
>
```

```
Modbus TCP values
Column  Tag       Value Error Note 
-------|---------|-----|-----|----|
sum_01 |hr:5409+4|  300|     |    |
half_2 |hr:5409+4|150.0|     |    |
max_all|hr:5409+4|  400|     |    |
```

One read of four registers (`hr:5409+4`) produced three columns. `sum_01` is `100 + 200`, `half_2` is half of `x[2]` (`300`), and `max_all` is the largest of the four registers.

**Note:** you only add an `outputs` entry for each column you want — you do **not** need one output per register. To skip a value, omit it from `outputs`.  
That matters when the device forces a wide read (for example **10** registers at once) but only **3** of them hold useful data: list those three in `outputs` and ignore the rest.

If one output fails while reading, only that column reports the error. Here `x[1] - 200` is `0`:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"blk","register":[5409,5410],
            "outputs":[{"name":"ok","formula":"x[0] + x[1]"},
                       {"name":"bad","formula":"x[0] / (x[1] - 200)"}]}]
>
```

```
Modbus TCP values
Column Tag       Value Error                           Note 
------|---------|-----|-------------------------------|----|
ok    |hr:5409+2|  300|                               |    |
bad   |hr:5409+2|     |formula error: division by zero|    |
```

Rules for `outputs`:

* The item must be a `register` or `inputRegister` block (a list of registers) and `outputs` must be a non-empty list.
* The block can use `swap`, but not `type`, `convert`, `formula`, `scale` or `offset`.
* Every output needs a `name` and a `formula`, and every formula is checked when the command is issued.
* If one output fails while reading, only that column is reported as a `formula error`; the other outputs of the block are still returned.
* Each output is its own column. `emit` on the block does not hide them (see below).
* The block needs at least two registers. With a one-register list, `outputs` is not applied: the raw value is returned instead (for example, `hr:5404` returns `34561`). For one register, use a formula or `swap`.

---

## Reading without storing (`emit`)

By default every point in `map` is stored. Set `"emit": false` on a point to read it without storing it:

```json
{"name":"module_2_status","register":5403,"emit":false}
```

With `emit: false`:

* The register is still read on every poll, and its value and any error are shown by `get plc values`. The **Note** column shows `not emitted`.
* The point is not written to the table (wide table or `table_per_value` table), and it does not get a UNS object or a policy column.

Use it for a value you want to see on the command line, or check during testing, but do not want in the database. Typical cases are a module status or diagnostic register, or a raw register that a formula or another point depends on.

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"temperature_c","register":[5394,5395],"type":"float"},
           {"name":"module_2_status","register":5403,"emit":false}]
>
```

```
Modbus TCP values
Column          Tag       Value Error Note        
---------------|---------|-----|-----|-----------|
temperature_c  |hr:5394+2| 23.5|     |           |
module_2_status|hr:5403  |   87|     |not emitted|
```

`module_2_status` is read (`87`) and shown, with the note `not emitted`. It is not stored, and `temperature_c` is stored as usual.

Rules:

* The value must be a JSON boolean: `false` or `true`. The string `"false"` is rejected with `emit must be true or false`. If `emit` is omitted, the point is stored.
* `emit` applies to `register`, `inputRegister`, `coil` and `input` items.
* `emit` on a constant (`value`) item is accepted and ignored: the constant is still copied onto the row, and `get plc values` does not show `not emitted` for it.
* `emit` on a block with `outputs` does not hide the outputs. They are still returned and stored, because each output is named by its own `name`, not by the block's.
* `emit` does not reduce polling. To stop reading a point, remove it from `map`.

---

## Constant columns (`value`)

A map item with a `value` and no address is not read from the device. Its `name` becomes a column, and the same value is copied onto every row of a fixed (wide) table:

```json
{"name":"station_id","value":"WST_1"}
```

Use a constant for something the device does not report but every row should carry, such as a station id, a model, a serial number, or a manufacturer. The value can be a string, a number, or a boolean. A list or an object is rejected with `value must be a string, number, or bool`.

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"humidity","register":5396},
           {"name":"model_id","value":"WS-200"},
           {"name":"serial_no","value":"SN-0004521"},
           {"name":"manufacturer","value":"Acme Sensors"},
           {"name":"station_id","value":"WST_1"}]
>
```

```
Modbus TCP values
Column       Tag     Value        Error Note     
------------|-------|------------|-----|--------|
humidity    |hr:5396|         452|     |        |
model_id    |      -|WS-200      |     |constant|
serial_no   |      -|SN-0004521  |     |constant|
manufacturer|      -|Acme Sensors|     |constant|
station_id  |      -|WST_1       |     |constant|
```

The constants have `-` in the Tag column because nothing is read for them, and `constant` in the Note column.

Rules:

* A constant item has `name` and `value` only. Combining `value` with `register`, `inputRegister`, `coil` or `input` is rejected with `value is a constant and cannot be combined with a register`.
* A map needs at least one register point. A map that contains only constants is rejected with `map['values'] has no entries`. Keep the constants in the same map as the points they describe.
* The `name` must be unique in the map. A duplicate name is rejected.
* In a `run plc client` command, constants are copied onto each stored row of a fixed (wide) table and onto the objects of a fixed-table UNS path. Per-value tables and per-value UNS objects do not carry constants. The plain `table_per_value = true` path (no `namespace`) writes each point to its own table with `tag` and `value` columns, and does not carry the constant columns.
* You can also set constants on the `run plc client` command itself — see [Command-line `constants` and `group_by_attributes](#command-line-constants-and-group_by_attributes)`. A command-line value **replaces** a map constant with the same `name`.

---

## All map options together

One command with a float, formulas, a two-register formula, a point that is read but not stored (`emit`), and constants:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"temperature_c","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure_hpa","register":[5397,5398],"type":"float"},
           {"name":"counter","register":[5399,5400,5401,5402],"type":"long"},
           {"name":"module_2_status","register":5403,"emit":false},
           {"name":"level_m","register":5404,"formula":"x * 0.001"},
           {"name":"temp_f","register":5405,"formula":"x * 0.0018 + 32"},
           {"name":"mix","register":[5409,5410],"formula":"20 * x[0] + 50 * x[1]"},
           {"name":"model_id","value":"WS-200"},
           {"name":"serial_no","value":"SN-0004521"},
           {"name":"manufacturer","value":"Acme Sensors"},
           {"name":"station_id","value":"WST_1"}]
>
```

```
Modbus TCP values
Column          Tag       Value        Error Note        
---------------|---------|------------|-----|-----------|
temperature_c  |hr:5394+2|        23.5|     |           |
humidity_pct   |hr:5396  |        45.2|     |           |
pressure_hpa   |hr:5397+2|     1013.25|     |           |
counter        |hr:5399+4|  1234567890|     |           |
module_2_status|hr:5403  |          87|     |not emitted|
level_m        |hr:5404  |      34.561|     |           |
temp_f         |hr:5405  |     94.2098|     |           |
mix            |hr:5409+2|       12000|     |           |
model_id       |        -|WS-200      |     |constant   |
serial_no      |        -|SN-0004521  |     |constant   |
manufacturer   |        -|Acme Sensors|     |constant   |
station_id     |        -|WST_1       |     |constant   |
```

How to read it:

* **Column** is the map `name`: the variable name used as the column in the table.
* **Tag** is what was read: `hr:5394+2` is two holding registers starting at 5394, `hr:5403` is one register.
* `temperature_c`, `pressure_hpa` and `counter` are decoded with `type` (`float` from two registers, `long` from four registers). No formula is needed.
* `humidity_pct`, `level_m`, `temp_f` and `mix` are formula results: `0.1 * 452`, `34561 * 0.001`, `34561 * 0.0018 + 32`, and `20 * 100 + 50 * 200`.
* `module_2_status` was read (`87`) but is marked `not emitted`, so it is not stored.
* The four constants have `-` as the Tag and `constant` as the Note.

---

## Data reading error

A holding register that the device does not define returns a Modbus exception. Here register `103` does not exist on the simulator, so its column shows the error and the other point still returns its value:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"not_there","register":103},
           {"name":"good","register":5396,"formula":"0.1 * x"}]
>
```

```
Modbus TCP values
Column    Tag     Value Error                                                 Note 
---------|-------|-----|-----------------------------------------------------|----|
not_there|hr:103 |     |read holding registers: illegal data address (code=2)|    |
good     |hr:5396| 45.2|                                                     |    |
```

Coils and discrete inputs do not return this error for an undefined address. On the simulator, `coil 103`, `input 103`, and `inputRegister 103` return `0`.

---

## Data conversion error

Here `1 / (x - 87)` divides by zero, because the status register holds `87`:

```anylog
<get plc values where type = modbus and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"bad_div","register":5403,"formula":"1 / (x - 87)"},
           {"name":"good","register":5396,"formula":"0.1 * x"}]
>
```

```
Modbus TCP values
Column  Tag     Value Error                          Note 
-------|-------|-----|------------------------------|----|
bad_div|hr:5403|     |decode error: division by zero|    |
good   |hr:5396| 45.2|                              |    |
```

---

## Continuous ingest — one table with all data

With `table` and `dbms` set, all points from `map` land in **one table**. Each poll inserts **one row**; every object in `map` is **one column**: the map `name` is the **column name**, and that column stores the **value** read for that point.

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.62 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev10 and
    dbms = env_sensor and
    table = modbus_sensors and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure","register":[5397,5398],"type":"float"},
           {"name":"station_id","value":"WST_1"}]
>
```

Tables:

* `modbus_sensors`

The constant `station_id` is a column on the same table, copied onto every row:

```
Schema for DBMS: 'env_sensor' and Table: 'modbus_sensors'
Column Name      Column Type                 
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
timestamp       |timestamp without time zone|
duration        |int                        |
temperature     |decimal                    |
humidity_pct    |decimal                    |
pressure        |decimal                    |
station_id      |char(5)                    |
```

---

## Continuous ingest — one table per value (`table_per_value = true`)

Omit `table` for plain `table_per_value` ingest. Each object in `map` is written to its **own table**. The table name is derived from the client `name` and the map `name` (for example, `fdev10_temperature` when `name = fdev10` and the map entry’s `name` is `temperature`). Each row includes `timestamp`, `tag`, and `value`.

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.62 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev10 and
    dbms = env_sensor and
    table_per_value = true and
    auto_uns = false and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure","register":[5397,5398],"type":"float"},
           {"name":"station_id","value":"WST_1"}]
>
```

Tables:

* `fdev10_temperature`
* `fdev10_humidity_pct`
* `fdev10_pressure`

A map constant such as `station_id` is accepted, but with plain `table_per_value` (no UNS) it does **not** become a table and is **not** added as a column on the per-value tables. Example columns for `fdev10_pressure` (the other two tables use the same layout):

```
Schema for DBMS: 'env_sensor' and Table: 'fdev10_pressure'
Column Name      Column Type                 
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
timestamp       |timestamp without time zone|
tag             |char(8)                    |
value           |decimal                    |
```

---

## Command-line `constants` and `group_by_attributes`

On `run plc client`, you can specify constants on the **command line** (`constants = {...}`) and/or in the **map** (`{"name":...,"value":...}`). Which you use is up to you. Either way, each constant becomes a **column** in the table. You can also pass `group_by_attributes` as a command keyword.

* `constants = {"station_id":"WS-001",...}` copies those keys onto **every stored row** (schema columns). A command-line constant **replaces** a map `{"name":...,"value":...}` entry with the same name.
* `group_by_attributes = [station_id]` stores those attribute values on each UNS **object** as a `where` clause (for example `station_id = 'WS-001'`). Names in the list must match keys from `constants`. Only schema columns are inserted as data; `group_by_attributes` shapes the object/`where`.

See [Use case with multiple weather stations with multiple operators](#use-case-with-multiple-weather-stations-with-multiple-operators) for a full example.

---

## Ingest with UNS (`auto_uns` + `master_node`)

With `auto_uns = true` and `master_node`, Modbus ingest is registered in the UNS (object policies on the blockchain). Optional `namespace` sets the UNS path. See [Unified Namespace](../../08-%20Blockchain%20&%20Metadata/04-%20Unified%20Namespace.md) for background.

### `table_per_value` with `namespace`

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.62 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev11 and
    dbms = env_sensor and
    table_per_value = true and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    namespace = FA9/MID9/DEVICE9 and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure","register":[5397,5398],"type":"float"},
           {"name":"station_id","value":"WST_1"}]
>
```

Tables:

* `fdev11_temperature_1`
* `fdev11_humidity_pct_1`
* `fdev11_pressure_1`

(The trailing `_1` is from the UNS mapping.)

Example columns for `fdev11_temperature_1` (the other two tables use the same layout, with the value column named for that map point):

```
Schema for DBMS: 'env_sensor' and Table: 'fdev11_temperature_1'
Column Name      Column Type                 
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
temperature     |decimal                    |
timestamp       |timestamp without time zone|
```

Namespace (one leaf per map point; constant `station_id` is not a table):

* `fa9/mid9/device9/fdev11_temperature`
* `fa9/mid9/device9/fdev11_humidity_pct`
* `fa9/mid9/device9/fdev11_pressure`

```anylog
blockchain get uns where name = fdev11_temperature bring.extend
```

```json
[
  {
    "uns": {
      "name": "fdev11_temperature",
      "namespace": "fa9/mid9/device9/fdev11_temperature",
      "parent": "912ecf2f339aae56d4886fe57267f2e4",
      "object_id": "3f9b6d18008bcbb611a4e2b70cee8f0d",
      "id": "d72da78756153f87dbdf13436f32c580",
      "source_node": "anylog-standalone-operator@192.168.1.62:32148",
      "date": "2026-11-25T12:49:20.834333Z",
      "ledger": "global"
    },
    "object": {
      "name": "fdev11_temperature",
      "description": "object for Modbus fa9/mid9/device9/fdev11_temperature",
      "dbms": "env_sensor",
      "table": "fdev11_temperature_1",
      "id": "3f9b6d18008bcbb611a4e2b70cee8f0d",
      "date": "2026-11-25T12:49:20.831010Z",
      "ledger": "global"
    }
  }
]
```

### `table_per_value` without `namespace`

Same map, different client `name`, no `namespace`:

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.62 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev12 and
    dbms = env_sensor and
    table_per_value = true and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure","register":[5397,5398],"type":"float"},
           {"name":"station_id","value":"WST_1"}]
>
```

Tables:

* `fdev12_temperature_1`
* `fdev12_humidity_pct_1`
* `fdev12_pressure_1`

Columns match the `fdev11_*` layout above (value column named for the map point). Namespace (auto, no user `namespace`):

* `fdev12_1/register/temperature`
* `fdev12_1/register/humidity_pct`
* `fdev12_1/register/pressure`

```anylog
blockchain get uns where name = fdev12_temperature bring.extend
```

```json
[
  {
    "uns": {
      "name": "fdev12_temperature",
      "namespace": "fdev12_1/register/temperature",
      "parent": "21af1889873ec2704268ff791a04d9c0",
      "object_id": "d0600595393c1f766ee30e6a0298756d",
      "id": "b095fb0be512dd9acec746159b6f1c40",
      "source_node": "anylog-standalone-operator@192.168.1.62:32148",
      "date": "2026-11-25T12:49:24.848714Z",
      "ledger": "global"
    },
    "object": {
      "name": "fdev12_temperature_1",
      "description": "object for Modbus fdev12_temperature_1",
      "dbms": "env_sensor",
      "table": "fdev12_temperature_1",
      "id": "d0600595393c1f766ee30e6a0298756d",
      "date": "2026-11-25T12:49:24.845011Z",
      "ledger": "global"
    }
  }
]
```

### Fixed table with `namespace`

One wide table, same map, with `auto_uns` and `namespace`:

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.62 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev13 and
    dbms = env_sensor and
    table = modbus_sensors_uns and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    namespace = FA9/MID9/DEVICE9 and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure","register":[5397,5398],"type":"float"},
           {"name":"station_id","value":"WST_1"}]
>
```

Tables:

* `modbus_sensors_uns`

```
Schema for DBMS: 'env_sensor' and Table: 'modbus_sensors_uns'
Column Name      Column Type                 
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
timestamp       |timestamp without time zone|
duration        |int                        |
temperature     |decimal                    |
humidity_pct    |decimal                    |
pressure        |decimal                    |
station_id      |char(5)                    |
```

Namespace (one leaf per sensor column; constant `station_id` is on each object and as a table column):

* `fa9/mid9/device9/fdev13_temperature`
* `fa9/mid9/device9/fdev13_humidity_pct`
* `fa9/mid9/device9/fdev13_pressure`

```anylog
blockchain get uns where name = fdev13_temperature bring.extend
```

```json
[
  {
    "uns": {
      "name": "fdev13_temperature",
      "namespace": "fa9/mid9/device9/fdev13_temperature",
      "object_id": "2646b4ab2611fec14e0e6494e1fc0e6b",
      "parent": "912ecf2f339aae56d4886fe57267f2e4",
      "id": "8c32d4f3de462eb73d341c224f270f86",
      "date": "2026-11-25T12:49:42.716352Z",
      "ledger": "global"
    },
    "object": {
      "station_id": "WST_1",
      "name": "temperature",
      "column": "temperature",
      "modbus": {
        "register": "hr:5394+2",
        "type": "float"
      },
      "dbms": "env_sensor",
      "table": "modbus_sensors_uns",
      "id": "2646b4ab2611fec14e0e6494e1fc0e6b",
      "date": "2026-11-25T12:49:42.712390Z",
      "ledger": "global"
    }
  }
]
```

### Fixed table without `namespace`

Same wide-table pattern, no `namespace`:

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.62 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev14 and
    dbms = env_sensor and
    table = modbus_sensors_uns2 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    map = [{"name":"temperature","register":[5394,5395],"type":"float"},
           {"name":"humidity_pct","register":5396,"formula":"0.1 * x"},
           {"name":"pressure","register":[5397,5398],"type":"float"},
           {"name":"station_id","value":"WST_1"}]
>
```

Tables:

* `modbus_sensors_uns2`

Columns match `modbus_sensors_uns` above (`temperature`, `humidity_pct`, `pressure`, `station_id`). Namespace (auto, no user `namespace`):

* `fdev14_1/register/fdev14_temperature`
* `fdev14_1/register/fdev14_humidity_pct`
* `fdev14_1/register/fdev14_pressure`

```anylog
blockchain get uns where name = fdev14_temperature bring.extend
```

```json
[
  {
    "uns": {
      "name": "fdev14_temperature",
      "namespace": "fdev14_1/register/fdev14_temperature",
      "object_id": "6be11d74bd508abc75259e33eef8277e",
      "parent": "cb45500f386715883a0830a656be26d4",
      "id": "3cc4cd6b9f518aa415cf88fba8072e34",
      "date": "2026-11-25T12:54:44.926344Z",
      "ledger": "global"
    },
    "object": {
      "station_id": "WST_1",
      "name": "temperature",
      "column": "temperature",
      "modbus": {
        "register": "hr:5394+2",
        "type": "float"
      },
      "dbms": "env_sensor",
      "table": "modbus_sensors_uns2",
      "id": "6be11d74bd508abc75259e33eef8277e",
      "date": "2026-11-25T12:54:44.920535Z",
      "ledger": "global"
    }
  }
]
```

---

## Command keywords (summary)

| Keyword            | Required / notes                                                                |
| ------------------ | ------------------------------------------------------------------------------- |
| `type`             | `modbus`                                                                        |
| `hostname`, `port` | Modbus TCP target                                                               |
| `device_id`        | PDU unit id                                                                     |
| `frequency`        | Poll interval                                                                   |
| `name`             | Unique client name                                                              |
| `dbms`             | Target DBMS                                                                     |
| `table` | Wide-table ingest; omit when `table_per_value = true` |
| `table_per_value` | `true` for one table per map point (omit `table`) |
| `auto_uns` | Set `true` with `master_node` (and optional `namespace`) to register the ingested data in the UNS |
| `map` | JSON array of points |
| `constants` | Optional JSON object; copies those values onto fixed (wide) table rows and fixed-table UNS objects (overrides a map constant with the same name) |
| `group_by_attributes` | Optional list of constant names; stored on each UNS object as `where` |
| `namespace` | Optional UNS path used with `auto_uns` |
| `master_node` | Required when `auto_uns` builds or updates UNS policies |

---

## Use case with multiple weather stations with multiple operators

Each operator node runs **one** `run plc client` for its station — same map and shared table `weather_stations_modbus`, different host, client `name`, and `constants` (here `station_id` **WS-001** vs **WS-002**). `group_by_attributes = [station_id]` keeps each station’s UNS objects scoped by station.

**The map and the constant names must be the same on every operator.** All operators that write to `weather_stations_modbus` must use the identical `map` (same `name` values and the same register addresses) and the same constant keys (`device`, `model`, `station_id`). Otherwise the rows do not match the table schema. Only the values change from one operator to the next: `hostname`, client `name`, and the constant values (`station_id`, `device`, `model`).

Note: The table `weather_stations_modbus` is virtual and its information stays in the ledger once created, so the first node that runs the command creates the table and its metadata, and every other operator node sees that it exists and writes its data into it, as long as it uses the same `dbms`, `table`, and `map`.

**Operator 1 — station WS-001**

```anylog
<run plc client where type = modbus and
    name = modbus-1 and
    hostname = 127.0.0.1 and
    port = 1502 and
    device_id = 1 and
    frequency = 10 and
    dbms = env_sensor and
    table = weather_stations_modbus and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    group_by_attributes = [station_id] and
    constants = {"device":"mb1-dev1","model":"MX1234D1","station_id":"WS-001"} and
    map = [{"name":"pressure_hpa","register":5394},
           {"name":"temperature_f","register":5395},
           {"name":"relative_humidity_pct","register":5396},
           {"name":"wind_speed_ms","register":5397},
           {"name":"wind_direction_deg","register":5398}]
>
```

**Operator 2 — station WS-002**

```anylog
<run plc client where type = modbus and
    name = modbus-2 and
    hostname = 127.0.0.2 and
    port = 1502 and
    device_id = 1 and
    frequency = 10 and
    dbms = env_sensor and
    table = weather_stations_modbus and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    group_by_attributes = [station_id] and
    constants = {"device":"mb2-dev2","model":"FX1234D9","station_id":"WS-002"} and
    map = [{"name":"pressure_hpa","register":5394},
           {"name":"temperature_f","register":5395},
           {"name":"relative_humidity_pct","register":5396},
           {"name":"wind_speed_ms","register":5397},
           {"name":"wind_direction_deg","register":5398}]
>
```

Tables:

* `weather_stations_modbus`

Both operators write to the same table. Rows are distinguished by `station_id` (and the other constants). The table has the five sensor columns plus `device`, `model`, and `station_id`:

```
Schema for DBMS: 'env_sensor' and Table: 'weather_stations_modbus'
Column Name             Column Type                 
-----------------------|---------------------------|
row_id                 |integer                    |
insert_timestamp       |timestamp without time zone|
tsd_name               |char(3)                    |
tsd_id                 |int                        |
timestamp              |timestamp without time zone|
duration               |int                        |
pressure_hpa           |decimal                    |
temperature_f          |decimal                    |
relative_humidity_pct  |decimal                    |
wind_speed_ms          |decimal                    |
wind_direction_deg     |decimal                    |
device                 |char(...)                  |
model                  |char(...)                  |
station_id             |char(...)                  |
```

Sample rows from both operators in the same table (`station_id` **WS-001** vs **WS-002**):

```
timestamp       pressure_hpa temperature_f relative_humidity_pct wind_speed_ms wind_direction_deg device   model    station_id
--------------- ------------ ------------- --------------------- ------------- ------------------ -------- -------- ----------
YY-MM-DD H:M:S          1013          72.5                  45.0           3.2                180 mb1-dev1 MX1234D1 WS-001
YY-MM-DD H:M:S          1009          68.1                  52.0           4.1                225 mb2-dev2 FX1234D9 WS-002
YY-MM-DD H:M:S          1013          72.6                  45.0           3.3                182 mb1-dev1 MX1234D1 WS-001
YY-MM-DD H:M:S          1009          68.0                  52.0           4.0                224 mb2-dev2 FX1234D9 WS-002
```

Example UNS object for station **WS-001** (`where` from `group_by_attributes`) of temperature — see `column` and `where`:

```json
{
  "object": {
    "device": "mb1-dev1",
    "model": "MX1234D1",
    "station_id": "WS-001",
    "name": "temperature_f",
    "column": "temperature_f",
    "modbus": {"register": "hr:5395"},
    "dbms": "env_sensor",
    "table": "weather_stations_modbus",
    "where": "station_id = 'WS-001'"
  }
}
```

---

## Related

- [Adding Data to Nodes in the Network](../../04-%20Southbound%20Interfaces/01-%20Southbound%20Interfaces.md)
- [Unified Namespace](../../08-%20Blockchain%20&%20Metadata/04-%20Unified%20Namespace.md)
- [OPC-UA](./03-%20OPC-UA.md)
- [EtherNet/IP](./04-%20EtherIP.md)