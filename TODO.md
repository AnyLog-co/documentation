# AnyLog Documentation — What Was Done, and What's Gone

Checked against the fresh tree scan taken right after the reorg. Status markers reflect actual structural
evidence (duplicate files reappearing, retired files coming back) — not guesses. Where I can't tell without
reading content, it's marked as needing verification rather than assumed either way.

**Status key:** 🔴 Confirmed reverted/duplicated · 🟡 Needs content verification · ✅ Confirmed still intact

---

## 🔴 Most urgent — a real security fix was reverted

The DNP3 TLS certificate directory (`C- DNP3 certificates/ca_chain/`) — containing actual committed private
keys — was deleted earlier this session and replaced with a self-generating-script approach. **It's back**, now
inside a new folder (`05- Anylog Nodes Network & Security/`) that didn't exist before the reorg. This needs
fixing before anything else on this list.

**New, from reviewing `REORG.md`:** the proposed new structure sources its Network & Security content directly
from this same `05- Anylog Nodes Network & Security/` folder, including the DNP3 cert material, with no
indication the document's author knows this directory contains real committed keys. This needs flagging to
whoever owns that section *before* it gets treated as an ordinary move.

---

## 🔴 Confirmed reverted or re-duplicated

- **`Using REST.md`** — merge undone; both the numbered and unnumbered copies exist side by side again in
  `07-.../A- Direct Connectors Generic/`.
- **`Using Syslog.md`** — worse than before the merge: now four files across two folders (`Syslog integration.md`,
  two differently-numbered `Using Syslog.md` variants, `Ingesting Syslog msgs.md`).
- **PowerBI / Qlik / Google Drive connectors** — `08-.../A- BI external tools — Office/` now has both
  numbered and unnumbered copies of all three, plus two files I've never seen (`Qlik How to.md`,
  `Google example.md`).
- **EtherNet/IP, OPC-UA merges** — both undone; numbered and unnumbered copies of `EtherNet IP.md` and
  `OPC UA Integration.md` both present in `07-.../D- Direct Connectors Industrial/`.
- **EdgeX consolidation** — fragmented again, now across *three* folders (`07-B`, `07-D`, `09-B`), each with
  its own variant, worse than the four-files-in-one-folder state before the merge.
- **PostgreSQL connector merge** — three copies now, across two sections.
- **FAQ merge** — back to two files, in two different sections (`17-` and `19-`).
- **`queries.md`** — retired file is back in `08- Northbound Connectors`.
- **`sql-setup.md`** — retired file is back in `08- Northbound Connectors`.
- **`DNP3.md`** base file — numbered and unnumbered copies both present (the three DNP3 companion docs this
  session added did survive intact, see below).
- **`Securing the Network.md`** — now exists in three places: the archive folder, the original
  `03- Installation & Deployment/` location (never moved), and a new numbered copy in the new
  `05- Anylog Nodes Network & Security/` folder.
- **`Background Processes.md`** — appears to exist in both `04- Core Concepts/` and `15- Development &
  Scripting/` now — not confirmed as the same content, but the naming collision is new.

## 🟡 Needs content verification before treating either way

- **UNS docs** — `13-.../01 UNS.md` / `02 UNS example.md` sit alongside the original unprefixed `UNS.md`,
  `UNS-custom.md`, `UNS-dynamic-custom-example.md`. Could be a clean rename, could be old content restored
  alongside new — can't tell from filenames alone.
- **Reserved-`id` blockchain caveat** — no plain `blockchain.md` visible anymore; closest candidate is
  `04-.../03 Blockchain & Metadata.md`. Unknown whether the caveat text survived a rename or was reverted.
- **Notifications** — `06 notifications.md` plus a new `06-1 Notifications example.md` — unclear whether the
  second one is the old draft (with the flagged real Slack token) coming back, or something new.
- **The two flagged real credentials** (EdgeX broker credential, Slack webhook token) — since the files they
  lived in are back in duplicated form, these may have returned too. Needs an actual content check, not
  assumption.
- **Agent Services stubs** (`Operator.md`, `Query.md`, `Publisher.md`) — still need checking whether they're
  still empty or whether anything changed.
- **`TMP Configuration.md`** — needs checking whether it's still a placeholder.

## ✅ Confirmed still intact

- **`Databases & Tables.md`** — present, unduplicated, in `02- Training & Tutorials/`.
- **`SQL Database.md`** (as `sql-databases.md`) — present, unduplicated, in `09- Integrations/A- Databases/`.
- **`Query Data.md`** — present, unduplicated, in `02- Training & Tutorials/`.
- **The three DNP3 companion docs** (`DNP3 - Deploying Connector via Script.md`, `DNP3 - Mapping-Policies.md`,
  `DNP3 - TLS test certificates.md`) — all present, though the TLS-certificates doc's entire reason for existing
  (replacing the committed-keys directory) has been undermined by that directory coming back elsewhere.
- **`05- Networking & Security/A- Built-in Authentication/`** (`Authentication.md`, `Authentication-policies.md`)
  — present, though now the *only* thing left in that folder, with TPM/Networking/DNP3-certs having moved to
  the new duplicate `05-` folder instead.

---

## Formatting issue found in the live docs (raised separately, tracked here)

The changelog block in at least `Using REST.md` is currently rendering as a **visible Markdown table at the top
of the document** — meaning it shows up on the actual published site — instead of the intended hidden HTML
comment block. Example of the regression:

**Current (wrong — user-facing):**
```markdown
# ### 📜 Change Log
 **Date**   | **Name**       | **Change** | **Version** |
 |------------|----------------|------------|----------|
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 ...
```

**Should be (hidden, internal-only):**
```markdown
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-23 | Moved to Network and Services; added POST as GET alternative, AnyLog-Agent header, blockchain insert command, Python examples
...
-->
```

This is a formatting/rendering regression, not a content duplication — but it likely affects every file whose
changelog got touched during the reorg pass, not just `Using REST.md`. Worth a dedicated check across the tree
for any doc that now opens with a visible changelog table instead of a hidden comment block.

---

## New items surfaced by reviewing the colleague's `REORG.md` proposal

- 🟡 **Where do the Agent Service stub docs actually go?** `Operator.md`, `Publisher.md`, `Query.md`,
  `Metadata Manager.md` have no explicit destination in the new proposed tree — their content is folded as
  topics into `intro-to-anylog.md` and `node-architecture.md` instead. This might be an intentional, good
  resolution (four empty stubs become one real doc), but it needs to be a stated decision, not something that
  happens by omission. Confirm with whoever wrote `REORG.md` before assuming either way.
- 🟡 **Possible new duplicate not yet caught by the reorg's own author:** `blockchain-as-a-service.md` and
  `blockchain-and-metadata.md` both appear as separate files in the proposed `07- Blockchain + Metadata`
  section with no stated difference between them. The section's own comment acknowledges general merge risk
  but doesn't resolve this specific pair.
- 🔴 **Structural inconsistency:** MCP is annotated as needing to sit "immediately after UNS," but is placed in
  a different section (`09- Extended Services`) than UNS (`07- Blockchain + Metadata`), with Data Management
  (`08`) sitting between them in the numbering. Needs reconciling — either move MCP or drop the "immediately
  after" framing.
- 🟡 **The wind-turbine example's specific 5-part template isn't in the document.** Discussed separately in this
  session (project README → step-by-step setup → connecting Claude/Perplexity via MCP → sample prompts →
  downloadable sample GUI) but the `REORG.md` entry for it is generic. Since this section is marked 100% owned
  by Mark, make sure that specific structure actually reaches him rather than assuming the generic description
  implies it.
- 🟡 **Sections 12–14 in `REORG.md` are thinner than the version worked out earlier in this session** — missing
  the FAQ dual-location warning (`17-` vs `19-`) and the `MOSHE-NOTES.md` gap (exists in the source Release
  Notes folder, not accounted for in either version). Worth reconciling the two documents rather than treating
  `REORG.md` as the final word on those three sections.
- ⬜ **Possible marker error:** `node-monitoring.md` under the new Southbound/Monitoring folder is marked 🆕
  (new), but a file by that name already exists in the current tree. Could be an intentional rewrite, could be
  a marker slip — worth a quick confirmation either way.
- ⬜ **Document itself is incomplete in one spot:** the Southbound section's comment #2 cuts off mid-sentence
  ("Syslog.md can reside as either 3rd party... But also") — not something to interpret or fill in, just flag
  that the source document wasn't finished there.
- ⬜ **Scope note:** this proposed structure is numbered independently of both the *actual current* (post-reorg)
  tree and the version worked through earlier in this session — implementing it means a bigger jump from
  present reality than continuing from where things left off. Not a problem, just worth going in aware of the
  size of the gap.

---

## Still open regardless of the reorg (never fixed to begin with)

- Authentication folder/link mismatch.
- Empty Agent Services stubs (pending the destination decision above).
- Hyperledger, EOS/aleos, Danfoss — undocumented.
- The `test-suite.md` / `test suites.md` / `test suite example.md` trio — never diffed, and now possibly joined
  by more duplicates given the pattern seen elsewhere.
- `python_data.py`'s column-name bug.
- The full systematic link-checker pass — never completed, and now likely needs to restart given how much has
  moved.