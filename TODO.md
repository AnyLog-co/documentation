# AnyLog Documentation — TODO

Rolling task list. Re-verified against the actual filesystem again on 2026-07-14 (second pass). This pass found
something more serious than link drift: `queries.md` appears to be genuinely gone from the tree, not just
moved, which means real reference content may have been deleted rather than reorganized. Also found a duplicate
that had been resolved has come back, and a new bug introduced while fixing something else. Read this pass's
findings carefully before assuming anything from the last version still holds.

**Status key:** ✅ Done (verified on disk) · 🟡 In progress / needs a decision · 🔴 New regression/urgent · ⬜ Not started

---

## 0. Most urgent — check these first

- 🔴 **`queries.md` (the full query reference — casts, all query options, time functions, HA flags) is not
  found anywhere in the tree.** Searched the whole repo; no file by that name exists. `08- Northbound
  Connectors/` now contains only `forwarding-data.md`, `northbound-overview.md`, `notifications.md`,
  `python_data.py`, and the three BI-tool subfolders — no query reference at all. Both of the new docs from
  this session (`Query Data.md` and `Databases & Tables.md`) explicitly hand off to `queries.md` for the "full
  reference" on casts, format options, HA `nodes`/`committed` flags, etc. — none of that content is present in
  either new doc, since both were deliberately written as narrower on-ramps. **If `queries.md` was deleted
  rather than renamed, that's a real content loss, not a broken link** — casts, the full query-options table,
  and the HA-specific options don't exist anywhere else in this tree as far as this scan found. Please confirm
  whether it was intentionally deleted, renamed to something not yet found, or lost by accident before anything
  else touches this area.
- 🔴 **`postgres-connector.md` duplicate has come back.** Confirmed resolved in the last pass (Northbound copy
  deleted, only `09- Integrations/A- Databases/Postgres Connector.md` survived). Now both exist again:
  `08- Northbound Connectors/A- BI Tools — Generic/postgres-connector.md` **and**
  `09- Integrations/A- Databases/Postgres Connector.md`. Not clear whether this was a deliberate re-add or an
  accidental restoration (e.g. from an old backup/branch) — worth finding out which before just re-deleting one.

---

## 1. Active work streams

### 1.1 UNS documentation

- ✅ `UNS.md`, `UNS-custom.md`, `UNS-dynamic-custom-example.md` confirmed placed; `ZZZ` duplicates gone.
- ✅ **Now genuinely done** (previously flagged as wrongly-marked-done, then re-verified this pass): the
  reserved-`id` blockchain caveat is confirmed present in `blockchain.md`, under "Two-step prepare / push."
- 🔴 **New bug, introduced while placing the above.** The "Two-step prepare / push" section's second command
  used to be `run client (!master_node) blockchain push !my_policy` — it now reads
  `blockchain insert where policy=!new_policy and local=true and master=!master_npode`. Two problems: (1) this
  is a different command than the one the section is describing (`blockchain insert` is the one-step
  recommended approach documented earlier in the same file, not the two-step prepare→push flow this section is
  about), and (2) `master_npode` is a typo for `master_node`. Looks like the id-caveat blockquote was pasted in
  and this line got overwritten/mangled in the process. Needs fixing — restore the original `run client (...)
  blockchain push !my_policy` line.
- ⬜ EDM/Remote-GUI content still needs a home in `remote-gui.md` (unchanged).

### 1.2 Security / Authentication documentation

- ✅ `Securing the Network.md` and `Authentication.md` confirmed placed and unchanged in substance.
- 🟡 **Still unfixed, unchanged from last pass.** Folder is `A- Built-in Authentication` (typo fixed), but the
  letter collision with `A- Trusted Platform Module (TPM)` remains, and the cross-file links in both
  `Securing the Network.md` and `Authentication.md` still point at a nonexistent file
  (`Policy-Based Users and Keys — Example.md`) instead of the real one (`Authentication-policies.md`). Re-read
  both files this pass — confirmed byte-for-byte identical to the previous check. This was priority #1 last
  time and still hasn't moved.
- ⬜ `TMP Configuration.md` still just "Tb completed Roy" — unchanged.

### 1.3 DNP3 documentation

- ✅ All four DNP3 docs confirmed placed together in `07- Southbound Interfaces/D- Direct Connectors
  Industrial/`: `DNP3.md`, `DNP3 - Deploying Connector via Script.md`, `DNP3 - Mapping-Policies.md`, and
  `DNP3 - TLS test certificates.md`.
- ✅ **The old vulnerable certificate directory is confirmed deleted.** `05- Networking & Security/` now
  contains only the Authentication and TPM folders plus `B- Networking` — the `C- DNP3 certificates/` directory
  (with the real committed private keys) is gone. This is a genuine, confirmed security fix.
- 🟡 The six broken cross-references from renaming (§2.7 below) are unchanged — expected, since fixing them was
  deliberately deferred to the link-checker pass by your own decision, not an oversight.
- ⬜ Unverified: `publish_policy.al` / `error_code` behavior description (unchanged).
- ⬜ `factory-x` vs `mogra` naming inconsistency — unchanged, still unresolved.

### 1.4 EtherNet/IP and OPC-UA merges

- ✅ Still confirmed clean — `EtherNet IP.md` and `OPC UA Integration.md` hold the merged content in place; old
  `etherip.md`/`opcua.md` remain gone. No change this pass.

### 1.5 New this session — Databases & Tables / Query Data

- ✅ Both new docs are placed: `Query Data.md` (the querying on-ramp, renamed from my suggested
  "Introduction to Querying Data.md") and `Databases & Tables.md` (the database/table lifecycle consolidation).
- 🔴 **Both landed in `02- Training & Tutorials/`, not split as originally intended** (`Query Data.md` was meant
  for Training & Tutorials — that part's right — but `Databases & Tables.md` was meant for `04- Core Concepts/`
  and isn't there at all; confirmed via search, no match anywhere in Core Concepts).
- 🔴 **Because of the placement above, several of `Databases & Tables.md`'s own links are now broken:**
  - Its two links to "Introduction to Querying Data.md" (intro paragraph and "See also") use a `../../` prefix
    that assumed the file would sit two folders deep (as originally planned for Core Concepts). From its actual
    one-level-deep location in Training & Tutorials, that's one `../` too many. They also still say
    "Introduction to Querying Data.md" — the actual sibling file is named `Query Data.md`. Both bugs stack.
  - Its two links to `queries.md` have the same `../../` depth problem — moot for now anyway, since `queries.md`
    itself appears to be gone (see §0).
  - Its one link to `Aggregations.md` (`../06- Data Management/...`) happens to still resolve correctly, purely
    by coincidence — both `02- Training & Tutorials/` and `04- Core Concepts/` are top-level siblings at the
    same depth, so a single `../` works from either location.
- `Query Data.md` itself reads clean in isolation — its own internal anchors and its link out to `queries.md`
  are the only issue, and that's really the §0 problem, not a bug in this file specifically.

---

## 2. Original audit findings

### 2.1 Duplicate `ZZZ` drafts

- ✅ Confirmed still fully resolved, no regressions found this pass.
- ⬜ `99- INTERNAL & DRAFT sections/[deprecated] Remote CLI .md` vs `remote_cli.md` — still both present,
  unchanged.
- 🟡 The `test-suite.md`/`test suites.md`/`test suite example.md` trio — confirmed still present, still not
  diffed. Unchanged from last pass.

### 2.2 Cross-section duplicates and fragmentation

- 🔴 `postgres-connector.md` — regressed, see §0.
- ✅ **`sql setup.md` fragmentation is now actually resolved** — both the old `19- Appendices/.../sql
  setup.md` and the newer `08-.../sql-setup.md` are confirmed deleted from the tree. Superseded by
  `Databases & Tables.md` (placement/linking issues aside, tracked separately in §1.5).

### 2.3 Legacy ORPHANS tree

- ⬜ Confirmed still fully intact, byte-for-byte the same subtree as last pass. No change.

### 2.4 Empty/stub Agent Services docs

- ⬜ Confirmed completely unchanged — `Publisher.md` (0 bytes), `Query.md` (0 bytes), `Operator.md` (15 bytes),
  `Metadata Manager.md` mismatch, `ZZZ metadata requests.md` all exactly as before. Still the highest-value,
  lowest-effort item on this entire list, and still nobody has touched it across two full verification passes.

### 2.5 Undocumented code modules

⬜ No change — Hyperledger, EOS/aleos, Danfoss 800 still undocumented.

### 2.6 Minor / lower-priority gaps

⬜ No change on any of these.

### 2.7 Broken cross-references

- ⬜ The three original blockchain-integration links (`19- Appendices/B-...`) — not rechecked this pass.
- 🟡 `Using Kafka.md`'s broken Message Broker Setup link — confirmed still broken, unchanged (`09- Connectors &
  Integrations/C-.../Message Broker Setup.md` vs. the real `09- Integrations/B-.../Message Broker Setup.md`).
- 🟡 `python_data.py`'s column-name mismatch bug — confirmed still present, unchanged. Would still raise a
  `KeyError` if run.
- 🟡 The six DNP3 cross-reference breaks from the renames — confirmed unchanged, per your deliberate deferral
  decision (see §1.3).
- 🔴 **New this pass:** `Databases & Tables.md`'s four broken/misdirected links (see §1.5).
- ⬜ The link-checker pass itself — still not done, now with a growing backlog of specific known breaks to
  sweep up in one pass: Authentication (6 links across 2 files), Kafka (1), DNP3 (6), Databases & Tables (4),
  plus whatever else a systematic pass would surface. That's at least 17 confirmed broken links now sitting in
  the tree from specific, identified causes — a strong argument for doing the systematic pass soon rather than
  keep discovering individual breaks one file at a time.

### 2.8 Folder organization issues

- 🟡 `07- Southbound Interfaces/`'s `E-`/`E-` letter collision (Media vs. RPC) — confirmed still present,
  unchanged.
- 🟡 `08- Northbound Connectors/`'s three `A-` folders — confirmed still present, unchanged. Also now houses
  the regressed `postgres-connector.md` duplicate inside one of them (`A- BI Tools — Generic`), compounding
  both issues in the same spot.

---

## 3. Priority order

1. **Resolve the `queries.md` question (§0)** — find out whether real reference content was actually deleted.
   This is now more urgent than anything else on the list; everything below assumes the doc tree is at least
   not silently losing content.
2. **Fix the `blockchain.md` two-step command bug (§1.1)** — a real, wrong command sitting in a doc right now,
   introduced this session.
3. **Resolve the `postgres-connector.md` duplicate regression (§0)** — figure out why it came back before
   just re-deleting one copy.
4. Fix the Authentication folder/link mismatch (§1.2) — still the oldest open concretely-broken-links item,
   now two verification passes in a row without movement.
5. Fix or relocate `Databases & Tables.md` (§1.5) — decide whether it moves to Core Concepts as originally
   planned or stays in Training & Tutorials permanently, then fix its links to match wherever it ends up.
6. Fix the Kafka broken link (§2.7) — one-line fix, still not done.
7. Fix `python_data.py`'s bug (§2.7) — still not done.
8. Fix the empty Agent Services stubs (§2.4) — still the single best value-for-effort item on the whole list,
   still completely untouched after two full passes.
9. Diff the `test-suite`/`test suites`/`test suite example` trio (§2.1).
10. Run the link-checker pass (§2.7) — now with a substantial, specific backlog to clear in one go.
11. Decide the fate of ORPHANS (§2.3).
12. Write up Hyperledger, EOS/aleos, and Danfoss (§2.5), or confirm and note them as unsupported.
13. Close out the minor/lower-priority gaps (§2.6) and the folder-organization items (§2.8).