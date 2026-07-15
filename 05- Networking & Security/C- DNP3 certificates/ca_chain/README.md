# DNP3 TLS test certificates

Lab CA chain for mutual TLS between an AnyLog DNP3 **master** and an **outstation** (for example [opendnp3](https://github.com/dnp3/opendnp3) `outstation-demo` configured for TLS).

## Generate

```bash
cd "05- Networking & Security/C- DNP3 certificates/ca_chain"
bash create_certificates.sh
```

## Files

| File | Role |
|------|------|
| `anylogDNP3ca.cert` / `anylogDNP3ca.key` | Root CA |
| `master1.cert` / `master1.key` | AnyLog master (TLS client) |
| `outstation1.cert` / `outstation1.key` | Primary test outstation (TLS server) |
| `outstation2.cert` / `outstation2.key` | Second outstation (optional) |

## AnyLog master

Use paths relative to your working directory when running AnyLog, for example:

| Keyword | Path |
|---------|------|
| `tls_ca` | `05- Networking & Security/C- DNP3 certificates/ca_chain/anylogDNP3ca.cert` |
| `tls_cert` | `05- Networking & Security/C- DNP3 certificates/ca_chain/master1.cert` |
| `tls_key` | `05- Networking & Security/C- DNP3 certificates/ca_chain/master1.key` |

## Outstation (TLS server)

Configure the outstation with:

| Setting | Path |
|---------|------|
| Peer / CA | `anylogDNP3ca.cert` |
| Local certificate | `outstation1.cert` |
| Private key | `outstation1.key` |

## Outstation (TLS server)

After `bash create_certificates.sh`, from `~/opendnp3/build`:

```bash
./outstation-tls-demo \
  /path/to/documentation-anylog-co/"05- Networking & Security/C- DNP3 certificates/ca_chain"/anylogDNP3ca.cert \
  /path/to/documentation-anylog-co/"05- Networking & Security/C- DNP3 certificates/ca_chain"/outstation1.cert \
  /path/to/documentation-anylog-co/"05- Networking & Security/C- DNP3 certificates/ca_chain"/outstation1.key
```

Plain TCP (no TLS): `./outstation-demo` from the same directory.

**For testing only** — do not reuse these keys in production.

See also: [DNP3](../../07-%20Southbound%20Interfaces/A-%20Direct%20-%20Built-in%20connectors%20%28protocols%20AnyLog%20natively%20accepts%20from%20devices%29/DNP3.md#dnp3-out-station-testing).
