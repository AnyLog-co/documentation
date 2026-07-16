# AnyLog Documentation — TODO

Rolling task list. Re-verified against the actual filesystem on 2026-07-14 — several items previously marked
✅ turned out to be only partially done, and a couple of new issues surfaced during the scan. Status changes
from the last version are called out explicitly below rather than silently corrected.

**Status key:** ✅ Done (verified on disk) · 🟡 In progress / needs a decision · ⬜ Not started

---

## 1. Active work streams

### 1.1 UNS documentation

- ✅ `UNS.md`, `UNS-custom.md`, `UNS-dynamic-custom-example.md` all confirmed placed in
  `13- UNS (Unified Name Spaces)/`; `12- MCP & LLMs/` confirmed to contain only `mcp.md` — both `ZZZ` duplicates
  gone.
- ✅ **Correction — this was wrongly marked ✅ last time.** The reserved-`id` blockchain caveat has **not** been
  added to `04- Core Concepts/B- Network-Services/blockchain.md`. Read the file in full — no mention of
  automatic/content-hash `id` assignment anywhere. Still needs writing.
- ⬜ EDM/Remote-GUI content still needs a home in `remote-gui.md` (unchanged from before).

### 1.2 Security / Authentication documentation

- ✅ `Securing the Network.md` and `Authentication.md` confirmed placed and unchanged in substance.
- 🟡 **Correction — this was wrongly marked ✅ last time; it's only half-fixed.**
  - The folder typo *was* fixed: it's now `05- Networking & Security/A- Built-in Authentication/` (not
    `Buit-in`). Good.
  - **But the letter collision was not fixed** — it's still `A-`, still colliding with
    `A- Trusted Platform Module (TPM)`.
  - **And the cross-file links were never updated to match.** `Securing the Network.md` still says
    `.../Built-in Authentication/...` (missing the `A- ` prefix that's actually on the folder) and still links to
    a file called `Policy-Based Users and Keys — Example.md`. The actual file in that folder is named
    `Authentication-policies.md`. `Authentication.md` has the same three broken links to the same wrong
    filename. **Every one of these links is currently dead.** This needs an actual fix, not just a decision.
- ⬜ `TMP Configuration.md` still just "Tb completed Roy" — unchanged.

### 1.3 DNP3 documentation

- ✅ `DNP3.md`, `Deploying a DNP3 Connector via Script.md`, and `DNP3-Mapping-Policies.md` all confirmed placed
  in `07- Southbound Interfaces/D- Direct Connectors Industrial/`.
- ⬜ `DNP3-tls-test-certificates.md` — searched `05- Networking & Security/` for any file matching `*DNP3*`;
  not found. Still not placed.
- ⬜ Unverified: `publish_policy.al` / `error_code` behavior description (unchanged — still based on inference,
  not a read of the actual helper script).
- ⬜ `factory-x` vs `mogra` naming inconsistency — unchanged, still unresolved.

### 1.4 EtherNet/IP and OPC-UA merges — better than tracked, update the record

Not previously in this TODO as a discrete item, but worth noting since it's genuinely done and done well:

- ✅ The EtherNet/IP merge was placed by overwriting `EtherNet IP.md` in place with the merged content
  (rather than creating a new `etherip.md` alongside it) — confirmed by reading the file; it matches the merged
  version exactly, changelog included. Old `etherip.md` is gone. Clean single-file resolution.
- ✅ Same pattern for OPC-UA: `OPC UA Integration.md` now holds the merged content; old `opcua.md` is gone.

---

## 2. Original audit findings

### 2.1 Duplicate `ZZZ` drafts

✅ Every single `ZZZ`/`zzz`-prefixed file in the entire tree is gone — confirmed via a tree-wide search
(zero matches for both `ZZZ*` and `zzz*`). This resolves every item below, including several that were still
marked ⬜ in the last TODO and were never actually worked on in this conversation — someone (you, presumably)
went through and cleaned these up directly:

- ✅ `ZZZ getting-started.md` vs `Getting Started.md`
- ✅ `ZZZ anylog-as-service.md` vs `Deploying Anylog as a Service.md`
- ✅ `ZZZ nebula through anylog.md` + `ZZZ nebula_new.md` vs `Nebula Networking.md`
- ✅ `ZZZ aggregations.md` vs `Aggregations.md`
- ✅ `ZZZ node-monitoring.md` vs `Monitoring Nodes.md`
- ✅ `ZZZ high-availability.md` vs `High Availability.md`
- ✅ `ZZZ data from edgex.md` — resolved as part of the larger EdgeX unification (see below)
- ✅ `ZZZ using-kafka.md`, `ZZZ using rest.md`, `ZZZ syslog.md`, `ZZZ Google.md`, `ZZZ grafana.md` +
  `ZZZ import-grafana-dashboard.md`, `zzz- notification.md` + `zzz- Notifications.md`, `ZZZ FAQ.md`

Not covered by the `ZZZ` sweep — checked separately, still open:

- ⬜ `99- INTERNAL & DRAFT sections/[deprecated] Remote CLI .md` vs `remote_cli.md` — confirmed both files
  still exist. Not a `ZZZ`-prefixed name, so it survived the cleanup pass. Still needs a decision and deletion.

New, related finding — not in any previous version of this list:

- 🟡 `99- INTERNAL & DRAFT sections/` now also has three files that look like the same near-duplicate
  pattern: `test-suite.md`, `test suites.md`, and `test suite example.md`. Not diffed yet — flagging for the
  same treatment as the `ZZZ` pairs (confirm overlap/uniqueness before deleting anything).

### 2.2 Cross-section duplicates and fragmentation

- ✅ `postgres-connector.md` duplicate — confirmed resolved. `08- Northbound Connectors/` has no postgres file
  at all now; `09- Integrations/A- Databases/Postgres Connector.md` is the sole survivor.
- ⬜ `sql setup.md` fragmentation — confirmed still unresolved. `19- Appendices/C- Reference Materials/sql
  setup.md` still exists, still presumably carrying the unmigrated commands (`get local tables`, etc.) that
  `08-.../sql-setup.md` is missing. Not touched.

### 2.3 Legacy ORPHANS tree

- ⬜ Confirmed still fully intact — the entire `ORPHANS/to be zapped x edgelake-docs/` subtree is present
  (commands/, examples/, northbound/, southbound/, training/, ~30 files including the Python examples and JSON
  dashboards), plus the empty `ORPHANS/x edgelake-docs/` scaffolding. Nothing here has been touched.
- Note: while scanning this tree, confirmed that `training/prerequisite.md` — one of the dead links found in the
  cleaned-up `FAQ.md` — does still exist, but only here, in the tree marked for deletion. If this content is
  still relevant, it needs to be migrated before ORPHANS is deleted, not just linked to as-is.
- Also confirms `northbound/twilio.md` and `southbound/fledge.md` (§2.3's original concern) are both still only
  present here — unchanged, still needs the same live-feature check before deletion.

### 2.4 Empty/stub Agent Services docs

- ⬜ Confirmed completely unchanged. `Publisher.md` (0 bytes), `Query.md` (0 bytes), `Operator.md` (15
  bytes, "to be completed"), `Metadata Manager.md` (title/content mismatch), `ZZZ metadata requests.md` (8.74 KB,
  still sitting in the wrong section, still `ZZZ`-prefixed despite the tree-wide cleanup elsewhere — worth
  noting this is the one surviving `ZZZ` file in the whole tree, presumably missed because it wasn't yet
  reconciled with a "real" counterpart the way the others were).

### 2.5 Undocumented code modules

⬜ No change — Hyperledger, EOS/aleos, Danfoss 800 all still undocumented. (Code-side; not verifiable from the
doc tree scan alone.)

### 2.6 Minor / lower-priority gaps

⬜ No change on any of these.

### 2.7 Broken cross-references

- ⬜ The three originally-flagged broken links (Blockchain Configuration/Using Ethereum/Blockchain Demo in
  `19- Appendices/B- Blockchain Integration/`) — not checked this pass, presumed unchanged since nothing in this
  conversation touched those files.
- 🟡 New confirmed broken link, found incidentally while verifying the Kafka merge: `Using Kafka.md` links
  to `../../09- Connectors & Integrations/C- Messages Brokers/Message Broker Setup.md`. The real path is
  `09- Integrations/B- Messages Brokers/Message Broker Setup.md` — wrong top-level folder name ("Connectors &
  Integrations" vs. actual "Integrations") and wrong letter (C- vs. actual B-). Confirmed broken by
  directly checking the real folder structure.
- 🟡 New finding, not yet a confirmed bug beyond inspection: `python_data.py` in `08- Northbound Connectors/`
  queries `min(timestamp) as ts` but then does `df['Time [dd.mm.yyyy hh:mm:ss.ms]']` — a column name that
  doesn't match what the query returns. As written, running this script would raise a `KeyError`. Also unclear
  whether any doc page is meant to accompany this script — it's a loose `.py` file with no obvious companion
  `.md`.
- ⬜ The link-checker pass itself — still not done. Every broken link found so far (in this list and the
  ones found during specific merges earlier in this conversation) has been found incidentally, one file at a
  time. The real count across ~150 files is unknown and likely higher.

### 2.8 New — folder organization issues found this pass (not fixes, just tracking)

- 🟡 `07- Southbound Interfaces/` has the same letter-collision pattern as Security: `E- Direct Connectors
  Media` and `E- Direct Connectors RPC` both use `E`. Discussed, not yet fixed.
- 🟡 `08- Northbound Connectors/` has three folders all starting with `A-` (`A- BI external tools — Grafana`,
  `A- BI external tools — Office`, `A- BI Tools — Generic`), inconsistent naming conventions between them, and
  categorization that doesn't hold up (Qlik under "Office"; Postgres/Postman under "BI Tools"). A restructure
  was proposed (one BI folder, a "Query & Data Access" folder, a "Notifications" folder) but not implemented.

---

## 3. Priority order

1. Actually fix the Authentication folder/link mismatch (§1.2) — this is the most concretely broken thing
   found this pass: real dead links sitting in two files right now, not a "needs a decision" item anymore since
   the folder rename already happened halfway.
2. Fix the Kafka doc's broken link to Message Broker Setup (§2.7) — now that the correct path is confirmed, this
   is a one-line fix.
3. Fix `python_data.py`'s column-name bug (§2.7) before anyone runs it and hits the `KeyError`.
4. Fix the empty Agent Services stubs (§2.4) — still the highest-value, smallest-effort item on the whole list,
   and still untouched.
5. Diff the newly-found `test-suite.md`/`test suites.md`/`test suite example.md` trio (§2.1) before it becomes
   another long-unresolved fragmentation case.
6. Place `DNP3-tls-test-certificates.md` (§1.3) and add the blockchain `id` caveat (§1.1) — both fully drafted,
   just not placed/written respectively.
7. Run the link-checker pass (§2.7) — still the single highest-leverage action across the whole tree, still not
   done.
8. Migrate the unique `sql setup.md` commands forward (§2.2), then retire the old page.
9. Decide the fate of ORPHANS (§2.3) — now with the added wrinkle that `prerequisite.md` genuinely only exists
   there.
10. Write up Hyperledger, EOS/aleos, and Danfoss (§2.5), or confirm and note them as unsupported.
11. Close out the minor/lower-priority gaps (§2.6) and the folder-organization items (§2.8).