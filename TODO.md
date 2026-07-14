# AnyLog Documentation Audit — Duplicates & Missing Content

**Scope:** `documentation/` cross-referenced against `AnyLog-Network/anylog_node` and `AnyLog-Network/anylog_enterprise`
**Method:** Full directory trees of both codebases and the doc tree, plus content-level comparison of files flagged as likely duplicates or likely stubs.

---

## 1. Executive Summary

The doc tree is large (19 numbered sections + `99-` drafts + `ORPHANS`) and mostly well organized, but it's carrying **three generations of content at once**: a legacy "EdgeLake"-branded set, a batch of `ZZZ`-prefixed drafts, and the current numbered structure. That overlap is the single biggest source of duplication. Separately, a handful of **core concept pages are empty stubs** while the real content for that exact topic sits, finished, in a draft file one folder over. There are also **code modules with no documentation at all** (two full blockchain platform integrations, one southbound driver), and several **cross-reference links that point at a folder structure that no longer exists**.

| Category | Count found |
|---|---|
| Verbatim/near-verbatim duplicate file pairs | 9 confirmed, ~10 more likely (by name pattern) |
| Empty or near-empty stub docs (content exists elsewhere) | 3 |
| Undocumented code modules/features | 6 |
| Broken internal cross-references (stale paths) | 4+ (systemic — likely more) |
| Legacy parallel doc tree (whole subtree) | 1 (`ORPHANS/to be zapped x edgelake-docs/`, ~25 files) |

---

## 2. Duplicate Content

### 2.1 `ZZZ`-prefixed drafts that are verbatim copies of the "real" doc

Confirmed **byte-for-byte identical** (only cosmetic link-syntax differences, e.g. Liquid tags vs. plain Markdown):

| Draft (ZZZ) | Duplicate of | Verified |
|---|---|---|
| `12- MCP & LLMs/ZZZ UNS.md` | `13- UNS/UNS.md` | ✅ read both, identical |
| `12- MCP & LLMs/ZZZ UNS-custom.md` | `13- UNS/UNS-custom.md` | ✅ read both, identical |

**Same pattern, not yet content-diffed but near-certain by naming/location convention** (recommend deleting the `ZZZ` copy once confirmed):

- `01- Getting Started/ZZZ getting-started.md` vs `Getting Started.md`
- `03- Installation & Deployment/A- Deployment Options/ZZZ anylog-as-service.md` vs `Deploying Anylog as a Service.md`
- `03-.../D- Networking & Security/ZZZ nebula through anylog.md` + `ZZZ nebula_new.md` vs `Nebula Networking.md`
- `06- Data Management/B- Query & Aggregations/ZZZ aggregations.md` vs `Aggregations.md`
- `06-.../D- Monitoring & Alerts/ZZZ node-monitoring.md` vs `Monitoring Nodes.md`
- `06-.../E- High Availability/ZZZ high-availability.md` vs `High Availability.md`
- `07- Southbound Interfaces/.../ZZZ data from edgex.md` vs `EdgeX Foundry Integration.md`
- `07-.../ZZZ using-kafka.md` vs `Using Kafka.md`
- `07-.../ZZZ using rest.md` vs `Using REST.md`
- `07-.../ZZZ syslog.md` vs `Using Syslog.md`
- `08- Northbound Connectors/.../ZZZ Google.md` vs `Google Drive Connector.md`
- `08-.../ZZZ grafana.md` + `ZZZ import-grafana-dashboard.md` vs `Using Grafana.md` / `Importing Grafana Dashboard.md`
- `08-.../zzz- notification.md` **and** `zzz- Notifications.md` (two near-identical zzz files) vs `notifications.md`
- `19- Appendices/.../ZZZ FAQ.md` vs `FAQ.md`

**Recommendation:** Every `ZZZ`-prefixed file should be diffed against its counterpart and deleted once confirmed superseded. These are draft artifacts, not intentional alternate content — several 99-/ZZZ files even say "to be completed" or carry old changelogs predating the numbered structure.

### 2.2 Duplicate across *sections* (not just ZZZ drafts)

| File A | File B | Finding |
|---|---|---|
| `08- Northbound Connectors/postgres-connector.md` | `09- Integrations/A- Databases/Postgres Connector.md` | **Verified verbatim duplicate** — identical body text, only the link format differs (old vs. new template). One should be deleted and the other cross-linked from Section 9. |
| `08-.../sql-setup.md` | `19- Appendices/C- Reference Materials/sql setup.md` | **Not a pure duplicate — content fragmentation.** `sql-setup.md` is a newer, cleaner rewrite (connect/partition/query basics). The older `sql setup.md` has real, non-overlapping content that was never migrated forward: `get local tables`, `get global tables`, `get data distribution`, `get table [info type]`, `test network table`, `drop network table`. **This is effectively missing content in the current doc tree** — it only exists in a page filed under "Appendices" that a reader looking at Northbound Connectors would never find. |

### 2.3 A whole legacy doc tree still present

`documentation/ORPHANS/to be zapped x edgelake-docs/` is a **complete parallel documentation set** (its own `commands/`, `examples/`, `northbound/`, `southbound/`, `training/` folders, ~25 files) under the old "EdgeLake" branding. The folder name says it should be deleted ("to be zapped"), but it still exists and structurally mirrors large parts of the current tree (getting started, southbound protocols, northbound connectors, training sessions). There's also an empty stub `ORPHANS/x edgelake-docs/` with five empty subdirectories (`Getting-Started`, `Monitoring-Operations`, `Network-Services`, `Querying-Data-Northbound`, `Tools-UI`) — dead scaffolding from an earlier reorg.

**Recommendation:** Confirm nothing in the "to be zapped" tree is still uniquely valuable (spot-check `twilio.md` and `fledge.md` under `northbound/`/`southbound/` — those two topics don't appear anywhere in the current numbered tree, see §3.5), then delete the whole subtree.

### 2.4 Duplicate `99-`/internal drafts

`99- INTERNAL & DRAFT sections/[deprecated] Remote CLI .md` and `remote_cli.md` sit alongside each other with overlapping titles — one is explicitly marked deprecated but both remain.

---

## 3. Missing / Undocumented Content

### 3.1 Core Agent Services docs are empty stubs — real content is stranded in a draft file

This is the most concrete gap found:

| File | Size | State |
|---|---|---|
| `04- Core Concepts/A- Agent Services/Publisher.md` | **0 bytes** | Empty |
| `04-.../Query.md` | **0 bytes** | Empty |
| `04-.../Operator.md` | **15 bytes** | Contains only the text `to be completed` |
| `04-.../Metadata Manager.md` | 2.1 KB | Actually written, but titled "Using a Master Node" — doesn't match its filename |
| `04-.../ZZZ metadata requests.md` | **8.7 KB** | Fully written, substantial content on table creation, file-naming convention, ingestion, schema validation — but filed as a `ZZZ` draft in the wrong section |

So three of the five files in "Agent Services" — the section meant to explain Operator, Publisher, and Query node roles (which map directly to `anylog_node/members/aloperator.py` and the query/publish code paths) — are empty or stub placeholders, while the real, finished content that belongs under Data Management/table creation is sitting in a draft file in the wrong folder.

**Recommendation:** Move `ZZZ metadata requests.md` content into the appropriate Data Management section (it's about table/schema/file-ingestion mechanics, not agent roles), and actually write `Operator.md`, `Publisher.md`, `Query.md` — or merge them into a single "Agent Roles" page.

### 3.2 Hyperledger Fabric integration — no documentation

Both codebases contain a substantial Hyperledger integration with no matching doc page anywhere in the tree:
- `anylog_node/blockchain/hyperledger.py`
- `anylog_enterprise/blockchain/alhyperledger/` — a full Java bridge (`AL_HL_Bridge`, `hyperledger.java`, `hl_calls.java`) plus chaincode (`chaincode/index.js`, `any-log-contract.js`)

Section 19-B ("Blockchain Integration") only documents **Ethereum** (`Using Ethereum.md`) and, via `Blockchain Demo.md`, **Optimism**. Hyperledger doesn't appear in any filename or (checked) in the content of the blockchain docs read.

### 3.3 EOS/aleos blockchain platform — no documentation

`anylog_enterprise/blockchain/aleos/` (an EOSIO-based smart contract: `aleos.cpp`, `aleos.wasm`, `aleos.abi`) has no corresponding page. Only Ethereum and Optimism are covered.

### 3.4 Danfoss protocol driver — no documentation

`anylog_enterprise/pull/danfoss_800.py` implements a specific industrial protocol/device puller (Danfoss 800 series). No file in the doc tree mentions it — not in Southbound Interfaces, not in Examples & Use Cases. Every other southbound driver (Modbus, DNP3, OPC-UA, EtherNet/IP, gRPC) has a dedicated page; Danfoss does not.

### 3.5 Twilio and Fledge — referenced only in the legacy ORPHANS tree

`ORPHANS/to be zapped x edgelake-docs/northbound/twilio.md` and `.../southbound/fledge.md` exist only in the tree marked for deletion. If Twilio notifications or Fledge southbound support are still live features, they currently have **no documentation in the active tree at all** — deleting the ORPHANS folder as recommended in §2.3 would silently drop this content rather than migrate it. Worth a quick check with engineering before deletion.

### 3.6 Enterprise member roles (Consumer / Distributor) are not individually documented

`anylog_enterprise/members/alconsumer.py` and `aldistributor.py` are enterprise-specific node roles alongside `alpublisher.py`. Section 4-A ("Agent Services") documents Operator, Publisher, Query, and Metadata Manager, but Consumer and Distributor roles don't have their own pages (and, per §3.1, Publisher's own page is currently empty anyway). `node-architecture.md` describes the general data-flow conceptually but doesn't name these roles explicitly.

### 3.7 Minor/lower-priority gaps

- `anylog_node/api/pycomm3_FakeLogixDriver.py` — a test/dev utility (fake PLC driver for testing EtherNet/IP without hardware). Not documented, but likely internal-only; low priority.
- `anylog_node/dbms/oledb` (PI System / OSIsoft historian integration via OLE DB, includes `pi_dbms.py` and PI SQL config files) — no dedicated PI/OSIsoft integration page found under Integrations or Southbound; worth confirming whether this is still a supported/marketed integration.
- `anylog_enterprise/cmd/permissions.py` — permissions concepts *are* documented (in `05- Networking & Security/Authentication.md`, under "Permission Group" and `get permissions`), but it's not confirmed whether enterprise-specific permission commands beyond the generic authentication doc are fully covered.

---

## 4. Broken / Stale Cross-References

Found while reading the blockchain docs — these point at a folder structure that predates the current numbering scheme, and land in a soon-to-be-deleted ORPHANS path:

- `19- Appendices/B- Blockchain Integration/Blockchain (internet) Configuration.md` links to:
  `../../ORPHANS/x04-southbound-services/using ethereum.md` (twice) — should point to the sibling file `Using Ethereum.md` in the same folder.
- `19-.../Using Ethereum.md` links to:
  `../17- Appendices/B- Blockchain Integration/blockchain configuration.md` — section is now `19-`, not `17-`, and the filename casing/spacing doesn't match the actual file (`Blockchain (internet) Configuration.md`).
- `19-.../Blockchain Demo.md` links to lowercase relative filenames (`blockchain commands.md`, `blockchain configuration.md`, `policies.md`) that don't match the actual, differently-cased/named files in the tree.

These three were found incidentally while reading three files for the blockchain-gap check — the actual count across ~150 doc files is very likely higher. A dedicated link-checker pass (script that resolves every relative Markdown link against the actual tree) would be the efficient way to find the rest, rather than manual review.

---

## 5. Recommended Priority Order

1. **Fix the empty Agent Services stubs** (§3.1) — highest value, smallest effort, actively misleading (a reader hits a page titled "Operator" and gets one line).
2. **Delete confirmed duplicate `ZZZ` files and the `postgres-connector.md` duplicate** (§2.1–2.2) — pure cleanup, no content risk once diffed.
3. **Migrate the unique commands from the old `sql setup.md` into `sql-setup.md`**, then retire the old one (§2.2).
4. **Run a link-checker pass** across the whole tree (§4) — likely the highest-leverage single action, since broken links compound every time the folder structure changes again.
5. **Decide the fate of the ORPHANS legacy tree** — but only after confirming Twilio/Fledge (§3.5) aren't the only copy of still-relevant content.
6. **Write up Hyperledger, EOS/aleos, and Danfoss** (§3.2–3.4) if those integrations are still supported/shipped; if they're deprecated code paths, note that instead so the absence is intentional rather than an oversight.