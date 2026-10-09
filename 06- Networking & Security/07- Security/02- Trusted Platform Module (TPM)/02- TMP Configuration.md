---
title: "Hardware TPM for AnyLog"
description: ""
layout: page
source_path: "01 TPM Configuration.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name**      | **Change**         | **Version** |
 |------------|---------------|---------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-10-09 | Massimiliano | Added a basic hardware TPM setup |  |

--->

# Hardware TPM for AnyLog

A hardware TPM is a physical TPM 2.0 chip on the machine. AnyLog does not talk to the chip directly. It uses the same [AnyLog-TPM](https://github.com/royshadmon/AnyLog-TPM/tree/fulltest) REST API as the [software TPM](./01-%20Software%20TPM.md). The API is pointed at the chip instead of `swtpm`.

The AnyLog commands after that are the same, including `make_persistent = true`.

## Check the chip

The chip should appear as a device. `/dev/tpmrm0` is the resource manager and is the device to use. `/dev/tpm0` is the raw device.

```bash
ls -l /dev/tpm*
```

Install the TPM tools and allow your user to open the device:

```bash
sudo apt-get update
sudo apt-get install -y tpm2-tools tpm2-abrmd
sudo usermod -aG tss $USER
```

Log out and back in so the `tss` group applies, then confirm the chip answers:

```bash
TSS2_TCTI=device:/dev/tpmrm0 tpm2_getcap properties-fixed
```

## Point the API at the chip

On the machine that has the chip, start the AnyLog-TPM API with the device TCTI set:

```bash
export TSS2_TCTI="device:/dev/tpmrm0"
export TPM2TOOLS_TCTI="device:/dev/tpmrm0"
```

Confirm the API is up. Use the port the API was started on:

```bash
curl http://127.0.0.1:8000/health
```

The AnyLog-TPM repository has a longer hardware walkthrough in `docs/HARDWARE_TPM_GUIDE.md`, including how to run the API in the background.

## Connect AnyLog

From the AnyLog CLI, register that API and turn TPM on. `tpm_dir` is the directory where the API keeps key metadata. With `make_persistent = true`, the key handle itself is stored in the chip and survives a reboot.

```anylog
tpm set where conn = 192.168.1.10:8000 and tpm_dir = /opt/anylog/tpm_dir
tpm enabled = on
tpm get info
```

Create keys the same way as on the software TPM. `make_persistent = true` is accepted on these commands:

```anylog
id create keys for node where password = abc and make_persistent = true
```

```anylog
id create keys where password = abc and keys_file = root_keys and make_persistent = true
```

```anylog
<id generate certificate authority where country = US and state = CA and locality = "Redwood City" and
    org = AnyLog and output_name = anylogca and
    hostname = anylogca and
    expiration_days = 3650 and
    tpm = true and
    make_persistent = true
>
```

`id generate certificate request` and `id sign certificate request` do not create a TPM key, so they do not take `make_persistent`. The rest of the AnyLog sequence is in [Software TPM — Typical AnyLog Workflow](./01-%20Software%20TPM.md#typical-anylog-workflow).

Clearing a hardware TPM deletes the keys stored in the chip. Do that only when those keys should be discarded.