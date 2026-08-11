---
title: Certificate Authority (CA)
description: What a Nebula mesh's Certificate Authority does, why it's a separate concern from the lighthouse, and how to handle the CA key safely.
layout: page
visibility: hidden
version: open source
tags:
- networking
- security
- nebula
- third-party
- index
---

<!--
## Changelog
- 2026-07-13 | Created document
- 2026-07-17 | Eric Aquaronne | added change log
- 2026-07-25 | Ori Shadmon | Merged two copies of this file. One had a broken frontmatter/changelog block — the
  opening `<!--` comment tag was missing entirely, so the changelog table and the orphaned closing `-->` would
  have rendered as visible garbage text instead of a hidden comment. Kept the properly-wrapped version's
  structure and folded in the missing changelog entry. Updated the "Overlay Networking" cross-link, which
  pointed at a pre-restructure path (`../overlay-network.md` / `../../B- Networking/03 overlay-network.md`) —
  neither resolves now. Since this doc specifically expands on Nebula's lighthouse/host/CA roles, it now points
  at **Nebula** (where that terminology actually lives) rather than the general **Overlay Networking** concept
  doc.
-->

# Certificate Authority (CA)

> This document assumes familiarity with Nebula's lighthouse/host roles, covered in
> <a href="./02-%20Nebula.md#terminology" target="_blank">Nebula</a>. It expands on one part of that setup: the certificate authority that
> establishes trust between nodes in the mesh.

Every Nebula mesh has exactly one Certificate Authority: a certificate (`ca.crt`) trusted by every member of the mesh, 
and a private key (`ca.key`) used only to sign new lighthouse and host certificates. `ca.crt` is distributed freely — 
it's how every node verifies that a peer's certificate is legitimate. `ca.key`, by contrast, is the single most 
sensitive artifact in the entire mesh: whoever holds it can mint a valid certificate for *any* identity, so anyone 
holding it can impersonate any node on the network.

**Important distinction:** being the lighthouse and being the CA are two separate roles that happen to be bundled 
together in the `nebula-anylog` repo purely for convenience. Nothing about Nebula's architecture requires the CA to 
live on the lighthouse — the automation script generates the CA on the lighthouse's first boot simply because it's 
the easiest thing to script for a quick single-lighthouse setup, not because the two roles are architecturally 
linked.

This matters because the two roles have very different risk profiles:

- The **lighthouse** needs to be reachable and running continuously — it's a live service other nodes depend on for 
  discovery.
- The **CA key** ideally almost never needs to be *used* after the mesh is initially set up (it's only needed when 
  signing a *new* host certificate), and every moment it sits on a network-connected, always-on machine is a moment 
  it's exposed to compromise.

For a quick test or demo, having the CA auto-generate on the lighthouse (as this repo does) is a reasonable default. 
For anything longer-lived, the safer pattern is to generate the CA once, offline, sign whatever lighthouse and host 
certs you need up front, and then keep `ca.key` off any running node entirely — including the lighthouse itself.