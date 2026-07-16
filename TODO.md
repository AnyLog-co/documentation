# AnyLog Documentation — TODO

Rolling task list. Started from the original duplicate/gap audit (§2 onward below); Part 1 tracks the three
work streams that have since been actively worked on and are mid-flight.

**Status key:** ✅ Done · 🟡 In progress / needs a decision · ⬜ Not started

---

## 1. Active work streams

### 1.1 UNS documentation

- ✅ Diffed `13- UNS/UNS.md` vs `12- MCP & LLMs/ZZZ UNS.md` — confirmed byte-for-byte identical, merged into one
  canonical `UNS.md`, fixed a duplicated "see" typo in the process.
- ✅ Diffed `13- UNS/UNS-custom.md` vs `12- MCP & LLMs/ZZZ UNS-custom.md` — same result, merged.
- ✅ Removed Remote GUI / EDM content from `UNS.md` (out of scope for that page — belongs in
  `11- EDM tool (Edge Data Manager)/remote-gui.md`).
- ✅ Created `UNS-dynamic-custom-example.md` — factory-floor walkthrough covering full-JSON `dynamic=true`
  ingestion, explicit `column.*` mapping, per-row table splitting, and a traced example of the resulting policy
  tree (root → device → mac → motor → leaf) showing exactly which levels come from the raw topic vs. the
  personalized mapping.
- ✅ Added "Building a namespace the customer can actually navigate" section to that page (topic naming design,
  and where a pure topic-driven tree runs out — many-to-many tag/association relationships).
- ⬜ **Not yet done:** write up the EDM/Remote-GUI content that was removed from `UNS.md` — it needs a home in
  `remote-gui.md`, including the known issue that the Remote-GUI's UNS view currently hardcodes the recognized
  timestamp column name (use `insert_timestamp`, not custom names, until fixed).
- ✅ **Not yet done:** add the reserved-`id` blockchain caveat (AnyLog assigns `id` automatically; don't supply
  your own; uniqueness is content-hash based) to `04- Core Concepts/blockchain.md` — surfaced from a customer
  email, never written up.
- ✅ Actually place `UNS.md`, `UNS-dynamic-custom-example.md`, and `UNS-custom.md` on disk (currently only
  produced as outputs; not confirmed copied into `13- UNS (Unified Name Spaces)/`), and delete the two `ZZZ`
  duplicates from `12- MCP & LLMs/` once confirmed superseded.

### 1.2 Security / Authentication documentation

- ✅ Rewrote `03- Installation & Deployment/Securing the Network.md` as a general overview (authentication
  options, TPM, overlay networking) — placed on disk correctly.
- ✅ Wrote `Authentication.md` (implementation reference: node/key auth, user auth, SSL certs) — placed on disk.
- ✅ Wrote the worked-example sub-file (13-step 2-operator demo + certificate example) — placed on disk, **but
  saved as `Authentication-policies.md` instead of the originally planned `Policy-Based Users and Keys —
  Example.md`.**
- ✅ **Needs a decision, then a fix:** the folder was created as `05- Networking & Security/A- Buit-in
  Authentication/` — typo (`Buit-in` → `Built-in`), and it collides with `A- Trusted Platform Module (TPM)` —
  two folders both using letter `A`. Once you confirm the intended folder name and letter, I'll fix:
  - The 4 links in `Securing the Network.md` pointing at `.../Built-in Authentication/...`
  - The 3 links in `Authentication.md` pointing at `Policy-Based Users and Keys — Example.md` (need to match
    whatever the example file ends up named — currently `Authentication-policies.md`)
  - The 2 links in `Securing the Network.md` pointing at the same example file
- ⬜ `05- Networking & Security/A- Trusted Platform Module (TPM)/TMP Configuration.md` is still just the
  placeholder text "Tb completed Roy" — linked from `Securing the Network.md` with a note that it's a
  placeholder, but the actual content is still missing.

### 1.3 DNP3 documentation

- ✅ Rewrote `DNP3.md` — fixed stale certificate paths, added cross-references to the two new companion docs.
  Confirmed correctly placed on disk.
- ✅ Wrote `Deploying a DNP3 Connector via Script.md` (deployment script walkthrough) — **not yet placed on
  disk.**
- ✅ Wrote `DNP3-Mapping-Policies.md` (reusable `dnp3` policy type for point maps) — **not yet placed on disk.**
- ✅ Wrote `DNP3-tls-test-certificates.md` (self-generating cert script, replacing committed keys) — **not yet
  placed on disk.**
- ✅ Confirmed the old `05- Networking & Security/C- DNP3 certificates/` directory (which had real private keys
  committed, guarded only by a `.gitignore` that excluded `*.srl`) has already been deleted.
- ⬜ Place the three files above in `07- Southbound Interfaces/A- Direct.../` and `05- Networking &
  Security/` respectively — `DNP3.md`'s links already point at their intended names, so no further link edits
  needed once they land.
- ⬜ Unverified: `Deploying a DNP3 Connector via Script.md` describes `!local_scripts/node-deployment/policies/publish_policy.al`
  based only on how the sample script calls it (never read the helper script itself) — confirm the description
  of its `error_code` behavior is accurate.
- ⬜ Unresolved stylistic question from earlier: the sample script and one edited section use `factory-x` as a
  topic prefix while the rest of the DNP3/UNS example material uses `mogra` — never resolved whether to
  standardize on one.

---

## 2. Original audit findings — not yet started

### 2.1 Duplicate `ZZZ` drafts (beyond UNS, already done above)

Still need diffing and (once confirmed identical) deletion:

- [ ] `01- Getting Started/ZZZ getting-started.md` vs `Getting Started.md`
- [ ] `03- Installation & Deployment/A- Deployment Options/ZZZ anylog-as-service.md` vs `Deploying Anylog as a Service.md`
- [✅] `03-.../D- Networking & Security/ZZZ nebula through anylog.md` + `ZZZ nebula_new.md` vs `Nebula Networking.md`
- [ ] `06- Data Management/B- Query & Aggregations/ZZZ aggregations.md` vs `Aggregations.md`
- [ ] `06-.../D- Monitoring & Alerts/ZZZ node-monitoring.md` vs `Monitoring Nodes.md`
- [ ] `06-.../E- High Availability/ZZZ high-availability.md` vs `High Availability.md`
- [ ] `07- Southbound Interfaces/.../ZZZ data from edgex.md` vs `EdgeX Foundry Integration.md`
- [✅] `07-.../ZZZ using-kafka.md` vs `Using Kafka.md`
- [✅] `07-.../ZZZ using rest.md` vs `Using REST.md`
- [✅] `07-.../ZZZ syslog.md` vs `Using Syslog.md`
- [ ] `08- Northbound Connectors/.../ZZZ Google.md` vs `Google Drive Connector.md`
- [ ] `08-.../ZZZ grafana.md` + `ZZZ import-grafana-dashboard.md` vs `Using Grafana.md` / `Importing Grafana Dashboard.md`
- [ ] `08-.../zzz- notification.md` **and** `zzz- Notifications.md` vs `notifications.md`
- [ ] `19- Appendices/.../ZZZ FAQ.md` vs `FAQ.md`
- [ ] `99- INTERNAL & DRAFT sections/[deprecated] Remote CLI .md` vs `remote_cli.md` — one is explicitly marked
      deprecated; confirm and delete

### 2.2 Cross-section duplicates and fragmentation

- [ ] `08- Northbound Connectors/postgres-connector.md` vs `09- Integrations/A- Databases/Postgres Connector.md`
      — verified verbatim duplicate; delete one, cross-link from the other.
- [ ] Migrate unique commands from `19- Appendices/C- Reference Materials/sql setup.md` (`get local tables`,
      `get global tables`, `get data distribution`, `get table [info type]`, `test network table`,
      `drop network table`) into `08-.../sql-setup.md`, then retire the old page.

### 2.3 Legacy ORPHANS tree

- [ ] Spot-check `ORPHANS/to be zapped x edgelake-docs/northbound/twilio.md` and `.../southbound/fledge.md` —
      confirm whether Twilio notifications / Fledge southbound support are still live features with no other
      documentation anywhere in the active tree. If so, migrate before deleting.
- [ ] Once confirmed nothing else of value remains, delete the whole `ORPHANS/to be zapped x edgelake-docs/`
      subtree (~25 files) and the empty `ORPHANS/x edgelake-docs/` scaffolding (5 empty subdirectories).

### 2.4 Empty/stub Agent Services docs

- [ ] `04- Core Concepts/A- Agent Services/Publisher.md` — currently 0 bytes.
- [ ] `04-.../Query.md` — currently 0 bytes.
- [ ] `04-.../Operator.md` — currently 15 bytes, just "to be completed".
- [ ] `04-.../Metadata Manager.md` — has content, but it's actually about using a master node; title/filename
      mismatch, needs either a rename or a rewrite to match its title.
- [ ] Move `04-.../ZZZ metadata requests.md` (8.7 KB, fully written — table creation, file-naming convention,
      ingestion, schema validation) out of Agent Services and into the correct Data Management section; it isn't
      about agent roles at all.
- [ ] While rewriting Operator/Publisher/Query: also decide whether to document the enterprise-specific
      Consumer/Distributor member roles (`alconsumer.py`, `aldistributor.py`) here or elsewhere (§2.6 below).

### 2.5 Undocumented code modules

- [ ] Hyperledger Fabric integration (`anylog_node/blockchain/hyperledger.py`,
      `anylog_enterprise/blockchain/alhyperledger/` — Java bridge + chaincode) — zero documentation anywhere.
      Confirm still supported before writing it up.
- [ ] EOS/aleos blockchain platform (`anylog_enterprise/blockchain/aleos/`) — zero documentation. Confirm still
      supported.
- [ ] Danfoss 800 protocol driver (`anylog_enterprise/pull/danfoss_800.py`) — zero documentation, unlike every
      other southbound driver (Modbus, DNP3, OPC-UA, EtherNet/IP, gRPC all have dedicated pages).

### 2.6 Minor / lower-priority gaps

- [ ] `anylog_node/api/pycomm3_FakeLogixDriver.py` — internal test/dev utility, likely doesn't need public docs;
      confirm and close out.
- [ ] `anylog_node/dbms/oledb` (PI System / OSIsoft historian integration) — no dedicated page under Integrations
      or Southbound; confirm whether this is still a supported/marketed integration before writing it up.
- [ ] `anylog_enterprise/cmd/permissions.py` — confirm whether enterprise-specific permission commands go beyond
      what's already documented in the new `Authentication.md` (§1.2 above), now that that page has moved and
      been rewritten.
- [ ] Enterprise Consumer/Distributor member roles — not individually documented anywhere (see §2.4).

### 2.7 Broken cross-references

- [ ] `19- Appendices/B- Blockchain Integration/Blockchain (internet) Configuration.md` — two links to
      `../../ORPHANS/x04-southbound-services/using ethereum.md`, should point to the sibling `Using Ethereum.md`.
- [ ] `19-.../Using Ethereum.md` — link to `../17- Appendices/...` (stale section number; now `19-`), plus
      filename casing mismatch.
- [ ] `19-.../Blockchain Demo.md` — three lowercase relative links that don't match actual (differently-cased)
      filenames.
- [ ] **Run an actual link-checker pass** (a script resolving every relative Markdown link against the real
      tree) across all ~150 files — the three above were found incidentally, not systematically; the real count
      is very likely higher. This has been flagged as the single highest-leverage remaining action since the
      original audit and still hasn't been done.

---

## 3. Priority order

1. Resolve the naming/placement issues in the three active work streams (§1) — these are half-finished and
   currently have dead links; cheapest to fix while context is fresh.
2. Fix the empty Agent Services stubs (§2.4) — highest value, smallest effort, actively misleading to a reader.
3. Run the link-checker pass (§2.7) — highest-leverage single action across the whole tree.
4. Delete confirmed duplicate `ZZZ` files and the `postgres-connector.md` duplicate (§2.1–2.2).
5. Migrate the unique `sql setup.md` commands forward, then retire the old page (§2.2).
6. Decide the fate of the ORPHANS legacy tree, after confirming Twilio/Fledge aren't the only copy of live
   content (§2.3).
7. Write up Hyperledger, EOS/aleos, and Danfoss (§2.5) — or explicitly note them as deprecated/unsupported if
   that's the case, so the absence reads as intentional rather than an oversight.
8. Close out the minor/lower-priority gaps (§2.6).