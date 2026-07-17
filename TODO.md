# AnyLog Documentation — Status Check

*A note before anything else: an earlier pass claimed all `ZZZ`-prefixed files were deleted, based on a
tree-wide search returning zero matches. That was wrong — a fresh direct scan of the tree shows several are
still present. The search tool was apparently giving false negatives, and that wasn't caught before being
reported as confirmed. Everything below is based on directly reading the file tree and, where marked
"confirmed," actual file content — not on tool searches alone.*

---

## 1. What's actually done (verified by direct read + confirmed placement)

- **UNS** — `UNS.md`, `UNS-custom.md`, `UNS-dynamic-custom-example.md` in `13- UNS/`.
- **Security overview** — `Securing the Network.md`, `Authentication.md`, `Authentication-policies.md` placed —
  **but still has broken cross-links** (see §2/§3 of the working backlog below; unchanged from prior passes).
- **DNP3** — four files in `07-.../D- Direct Connectors Industrial/`, plus a real security fix: deleted the
  directory that had actual private keys committed to the repo.
- **EtherNet/IP, OPC-UA** — merged in place, no surviving duplicate files.
- **EdgeX** — consolidated from four overlapping files down to two.
- **PowerBI, Qlik, Google Drive, PostgreSQL connector** — each merged to one file, links fixed.
- **Notifications, FAQ** — merged, no surviving duplicates.
- **`Databases & Tables.md`, `SQL Database.md` (as `sql-databases.md`), `Query Data.md`** — all placed;
  `Databases & Tables.md` substantially expanded (partitioning detail, system columns, table creation).

---

## 2. Duplicates — confirmed and newly spotted

### Confirmed still present — the `ZZZ` files (previously misreported as deleted)

`ZZZ getting-started.md`, `ZZZ anylog-as-service.md`, `ZZZ metadata requests.md`, `ZZZ aggregations.md`,
`ZZZ node-monitoring.md`, `ZZZ high-availability.md`.

Spot-checked one: `ZZZ getting-started.md` vs. `Getting Started.md` — the latter is a fuller unification that
genuinely supersedes it (confirmed by reading both in full). The other four have **not** been individually
re-verified this pass — don't treat them as safe to delete without checking each first.

### New — a four-way duplicate on "querying," not two

Only two of these were ever compared against each other:

- `06- Data Management/B- Query & Aggregations/Queries.md`
- `06- Data Management/C- Data Examples/Querying Data.md`
- `08- Northbound Connectors/queries.md` (believed retired — it's back, unreviewed)
- `02- Training & Tutorials/Query Data.md` (the one built up over this session as "canonical")

### New — networking

- `03- Installation & Deployment/Networking.md`
- `05- Networking & Security/B- Networking/networking.md`

Never compared to each other.

### New — message brokers

- `07- Southbound Interfaces/A- Direct Connectors Generic/message-broker.md` (built this session)
- `09- Integrations/B- Messages Brokers/Message Broker Setup.md`
- `09- Integrations/B- Messages Brokers/Broker Setup Example.md`

`message-broker.md` was written without knowing `Message Broker Setup.md` already existed — and
`Getting Started.md` (see below) links to `Message Broker Setup.md`, not the new file.

### New — Core Concepts overlap

- `04- Core Concepts/Background Processes.md` vs. `04-.../B- Network-Services/background-services.md`
- `04- Core Concepts/Metadata Management.md` vs. `04-.../B- Network-Services/policies-metadata.md` vs.
  `04-.../Policies.md`

### New — Getting Started cluster

- `01- Getting Started/Quick Deployment Guide.md` vs. `quick-start.md`
- Possibly `Executable.md` / `Service.md` / `starting an anylog instance.md` all overlapping on "how to run
  AnyLog"

### Not yet diffed at all

`99- INTERNAL & DRAFT sections/test-suite.md` / `test suites.md` / `test suite example.md`.

### Probably fine, worth a sanity check

`00- archive/` looks like a deliberate backup folder (old copies of `Securing the Network.md`,
`Network Processing.md`, `networking.md`, `overlay-network.md`) — likely intentional and inert, but its actual
purpose hasn't been confirmed.

### A large, separate finding inside `Getting Started.md` itself

Its own embedded changelog documents seven more open issues left by whoever last unified it — including a
`MODBUS.md`/`modbus.md` casing duplicate, a `southbound-overview.md` title mismatch, and an ambiguous
"Using EdgeX" link between two candidate targets. None of this was visible before reading the file directly.

---

## 3. Missing content

**Unchanged from the original audit:**
- `Publisher.md`, `Query.md`, `Operator.md` — the Agent Services stubs, still empty/placeholder.
- Hyperledger Fabric, EOS/aleos, Danfoss 800 — undocumented code, still undocumented.
- `TMP Configuration.md` — still just "Tb completed Roy."

**New, surfaced by reading `Getting Started.md`:**
- A "Master Node setup" page referenced but not found anywhere in the numbered tree.
- A "Starting an AnyLog Instance" page whose only copy lives inside `ORPHANS`.

---

## Suggested next step

Before doing any more merges, it's worth actually reading and comparing the four querying files — that's the
most concrete, highest-impact unresolved item found this pass, and the one most likely to already have had
its "fix" applied to the wrong file.