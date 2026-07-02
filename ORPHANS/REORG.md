# Documentation Reorg — `os-dev` branch

## 1. Where we are now

Before this work, the `documentation` repo had everything documentation related cluttered and disorganized.

In addition, we had `anylog-docs/` — a partial migration of the documentation that had roughly 30–40% populated of the
original content post-Claude scanning.

However, the reality was that instead of migrating missing documents into the new `anylog-docs/` repo, we continued
editing the existing documentation repo, thus ended up with 2 parallel projects.

As such, Roy converted the `anylog-docs/` repository into the frontend, while keeping `documentation` as the backend /
content base for the documentation.

## 2. What I did

Building on top of the work done by Roy, and under the `documentation/` repository:

1. Created the `os-dev` branch off latest `main`/`master`.
2. Copied the content of `anylog-docs/` into the `documentation` repo as a backup before reorganizing anything.
3. Had Claude review the full `documentation/` tree (root files + all subfolders) and propose a mapping of every
   legacy file into the 9-category taxonomy already implied by `anylog-docs/`.
4. Restructured that mapping into a flatter, numbered tree (so ordering matches a rough "learning path" rather
   than alphabetical, and so it's obvious at a glance what's been migrated vs. not):

   ```
    01-getting-started/      Installing, deploying, and starting a first AnyLog node — onboarding path.
    02-cli/                  The AnyLog command-line interface: commands, syntax, test/cheat-sheet references.
    03-network-services/     Node networking, security, authentication, overlay networks, and node-to-node messaging.
    04-southbound-services/  Getting data INTO AnyLog — ingestion, mapping/transformation, protocols (MQTT, OPC-UA, EdgeX, etc.), and data/node monitoring.
    05-northbound-services/  Getting data OUT of AnyLog — querying, aggregations, and BI/dashboard connectors (Grafana, PowerBI, Qlik, etc.).
    06-tools-ui/             GUI and visualization tooling for interacting with a network (Grafana setup, Postman, remote CLI/GUI).
    07-references/           Glossary, FAQ, licensing, and other lookup material that isn't a how-to.
    08-version-control/      Release notes and changelogs.
    09-examples-training/    Worked examples, training curriculum, and demo/deployment walkthroughs — staged for cleanup as AnyLog-API matures.
    ```

5. Ran a [move script](copy.sh) to actually relocate every legacy file into its new home per that mapping.
6. Along the way, found a confirmed exact duplicate (`examples/Secure Network.md` is word-for-word the same as
   the root's `secure network.md`) — parked the duplicate in `09-examples-training/_review/` instead of deleting
   it outright, so it can be verified before removal rather than silently lost.

This is a **first pass**, not a finished migration — see "Next steps" below for what's still rough.

## 3. Next steps

1. **Review the current structure.** Walk the new `01-09` tree, confirm the category placements make sense, and
   resolve the open items below before treating this as final:
   - Decide numbering and what type of content goes where.
   - Review orphaned or duplicate content:
     - Resolve the parked duplicate — confirm `_review/Secure Network.md` is safe to delete in favor of the
       canonical copy in `03-network-services`.
     - Resolve the Nebula doc duplication — `nebula.md` vs `nebula_new.md` in `03-network-services`, decide
       which supersedes the other.
   - Decide on the deprecated Remote CLI doc sitting in `09-examples-training` vs. the live version in
     `02-cli/remote_cli.md`.
   - Content-level dedup pass on a few more likely-overlapping clusters not yet verified line-by-line:
     blockchain commands/configuration/demo, the broker setup docs, onboarding/CLI command lists, and the
     Grafana docs split across `05-northbound-services` and `06-tools-ui`.
   - Reconcile with `anylog-docs/` — decide whether it stays as the rendered frontend pulling from this
     content, or gets retired now that the numbered tree covers more ground than the original partial
     migration did.

2. **Begin running the files through Claude and other AI agents**, keeping in mind the reorg has likely broken
   link paths along the way:
   - Fix relative links and image paths — moving files into subfolders breaks relative `.md` links and
     `imgs/` references; needs a dedicated pass before content edits, not after, so AI agents aren't fixing
     content around broken links.
   - Regenerate `_sidebar.md` (docsify nav) to reflect the new tree.
   - Add `how-to-rest-shell.md` and `how-to-rest-python.md` to `05-northbound-services`, and finish the
     AnyLog-API tool to replace `examples/` as the canonical code reference.
   - Team review pass — once the above is settled, each category folder should get a quick read-through from
     whoever's closest to that area, since this reorg moved files but didn't rewrite content.