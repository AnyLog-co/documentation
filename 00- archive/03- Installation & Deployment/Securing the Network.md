---
title: "Securing the Network"
description: An overview of AnyLog's security options — built-in authentication, Trusted Platform Module (TPM) support, and overlay networking
layout: page
source_path: "Securing the Network.md"
---

<!--
## Changelog
- (original) Created as a single combined document covering key-based authentication, a full policy demo, and
  certificate-based authentication for 3rd parties
- 2026-07-14 | Rewritten as a general overview. The step-by-step policy demo moved to
              06- Networking & Security/Built-in Authentication/Policy-Based Users and Keys — Example.md.
              The command-level authentication reference moved to
              06- Networking & Security/Built-in Authentication/Authentication.md. This page now summarizes all
              three security mechanisms and links out to the detailed docs for each.
-->

# Securing the Network

AnyLog secures a network through three independent mechanisms, which can be used separately or combined:

1. **Built-in authentication** — key-based authentication between member nodes, username/password authentication
   for external users and applications, and certificate-based (SSL/X.509) authentication for 3rd-party
   applications.
2. **Trusted Platform Module (TPM)** — hardware- or software-backed protection for the private keys used by
   authentication, so key material isn't held in plain form on the node's filesystem.
3. **Overlay networking** — a 3rd-party overlay (AnyLog uses [Nebula](https://nebula.defined.net/docs/) as a
   worked example) that gives nodes a stable, authenticated address to reach each other by, independent of the
   underlying physical network.

These three mechanisms address different layers of the problem: authentication controls *who* is allowed to send
a node a command or a policy and *what* they're allowed to do; TPM controls *how safely the keys behind that
authentication are stored*; overlay networking controls *how nodes reach each other* in the first place, without
exposing the broader network they sit on.

---

## Our Authentication Options

AnyLog supports three built-in authentication mechanisms. All three can be enabled independently, and a single
node can use more than one at once (for example, key-based authentication between member nodes plus
certificate-based authentication for a Grafana dashboard querying the same node).

### 1. Key-Based (Node) Authentication

Each node — and optionally each individual user — is assigned a private key and a public key. A message from a
node to a peer is signed with the sender's private key; the receiving peer authenticates the sender using the
sender's public key, then checks the sender's permissions against the relevant policies before processing the
message. This is the mechanism that secures node-to-node traffic within the network itself.

- **Concept and commands:** [Node Authentication](../05-%20Networking%20&%20Security/Built-in%20Authentication/Authentication.md#node-authentication)
- **Worked example (policies, permissions, a full 2-operator demo):** [Policy-Based Users and Keys — Example](../05-%20Networking%20&%20Security/Built-in%20Authentication/Policy-Based%20Users%20and%20Keys%20—%20Example.md)

### 2. User Authentication

Username/password authentication for external users and applications connecting over REST — for example, an
admin logging into the CLI, or a 3rd-party tool like Grafana or Postman issuing basic-auth REST calls against a
node. Unlike key-based authentication, this doesn't require issuing keys; users are added directly to a node
with a name, password, and optional expiration.

- **Concept and commands:** [Users Authentication](../05-%20Networking%20&%20Security/Built-in%20Authentication/Authentication.md#users-authentication)

### 3. Certificate-Based (SSL) Authentication

For 3rd-party applications that aren't members of the network at all (i.e., they don't hold a node key pair),
AnyLog can act as a Certificate Authority: it issues and signs X.509 certificates, and the resulting certificate
takes the place of a public key in a member policy. This is the mechanism behind HTTPS access from tools like
cURL, Postman, or Grafana.

- **Concept and commands:** [Using SSL Certificates](../05-%20Networking%20&%20Security/Built-in%20Authentication/Authentication.md#using-ssl-certificates)
- **Worked example (issuing a cert to a 3rd-party app, then using it from cURL/Grafana/Remote CLI):**
  [Policy-Based Users and Keys — Example](../05-%20Networking%20&%20Security/Built-in%20Authentication/Policy-Based%20Users%20and%20Keys%20—%20Example.md#using-certificates)

Authentication (of any of the above types) is toggled with:

```anylog
set authentication [on/off]
get authentication
```

Node authentication and user authentication can also be toggled independently — see
[Authentication](../05-%20Networking%20&%20Security/Built-in%20Authentication/Authentication.md) for the specific
commands.

---

## Trusted Platform Module (TPM)

TPM support protects the private keys that the authentication mechanisms above depend on, so that key material
isn't stored in plain form. AnyLog supports both a software-emulated TPM (`swtpm`, useful for development or
hardware without a physical TPM chip) and hardware TPM configuration.

- **Software TPM setup and the `tpm` commands:** [Software TPM](../05-%20Networking%20&%20Security/A-%20Trusted%20Platform%20Module%20(TPM)/Software%20TPM.md)
- **Hardware TPM configuration:** [TPM Configuration](../05-%20Networking%20&%20Security/A-%20Trusted%20Platform%20Module%20(TPM)/TMP%20Configuration.md)
  *(this page is currently a placeholder pending full documentation)*

A typical flow layers TPM underneath key-based authentication: configure the TPM connection (`tpm set`), enable
it (`tpm enabled = on`), create the node's keys as usual (`id create keys for node`), then store the node key
password with the TPM (`tpm set node key password`) before enabling node authentication.

---

## Overlay Networking

An overlay network lets nodes reach each other over a stable, authenticated address, independent of the physical
network(s) they actually sit on — useful for connecting nodes across sites, behind NAT, or on networks you don't
want to expose directly. AnyLog uses [Nebula](https://nebula.defined.net/docs/) as a worked example: a
certificate-based mesh with no dedicated VPN server, lightweight enough for edge hardware, and simple to run
alongside AnyLog in Docker. Any overlay technology that provides the same kind of stable, authenticated
addressing would satisfy the same need — Nebula isn't a hard requirement.

- **Concepts (lighthouse vs. host, why a dedicated lighthouse instance is the better default) and full Nebula
  deployment steps:** [Overlay Networking](../05-%20Networking%20&%20Security/B-%20Networking/overlay-network.md)
- **The Nebula mesh's Certificate Authority — what it is and how to handle the CA key safely:**
  [Certificate Authority (CA)](../05-%20Networking%20&%20Security/B-%20Networking/overlay-certificate-authority.md)

At a high level, an overlay network still relies on ordinary IP networking underneath — it tunnels through
firewalls rather than bypassing them, so the relevant port (`4242`/UDP by default for Nebula) needs to be open or
forwarded between the machines that need to discover and reach each other.

---

## Choosing what to combine

These three mechanisms are independent, and most production deployments use more than one:

| Mechanism | Secures | Typical use |
|---|---|---|
| Key-based authentication | Node-to-node and user-to-node messages within the network | Always recommended once a network has more than one operator |
| User authentication | External REST access from users/apps that aren't network members | Admin CLI access, internal dashboards |
| Certificate-based authentication | External REST access from 3rd-party apps, over HTTPS | Grafana, Postman, custom integrations |
| TPM | The private keys behind any of the above | Environments where plain-file key storage is a concern |
| Overlay networking | Node-to-node reachability across networks/NAT | Multi-site deployments, nodes behind restrictive NAT |

None of them are mutually exclusive, and none require the others — a small single-site test network might run
with none of this enabled at all, while a production multi-operator deployment would typically combine key-based
authentication with TPM-backed keys and, if nodes span sites, an overlay network on top.