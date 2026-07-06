# AnyLog Docs

This is the technical documentation for [AnyLog Edge Data Fabric](https://www.anylog.network/), built with Jekyll and hosted on GitHub Pages.

--- 

## Goal
 
We decided to Provide the documentation via a website at **https://anylog.network/docs** using Jekyll (same theme as OpenHorizon), replacing raw GitHub repo access with a structured, navigable site comparable to EdgeX or ReadTheDocs.
 
---

## Documentation Source

Documentation content is sourced from the public
<a href="https://github.com/AnyLog-co/documentation" target="_blank">AnyLog-co/documentation</a>
repository on the `master` branch.

Do not edit generated Markdown files in `_docs/` in this repository. The Jekyll build runs
`.github/scripts/sync_external_docs.py`, which clones `AnyLog-co/documentation`, converts every upstream `.md`
file into a Jekyll collection page, copies supporting assets into `assets/external-docs/`, and regenerates the sidebar
navigation.

The GitHub Pages workflow rebuilds on pushes and pull requests in this repository, manual workflow dispatch, an hourly
schedule, and `repository_dispatch` events of type `documentation-updated`.

For immediate publishing when `AnyLog-co/documentation` changes, add a workflow in that repository that sends a
`repository_dispatch` event to this repository after pushes to `master`. Without that dispatch, the scheduled rebuild
will still pick up upstream changes within the next hourly run.

---

## Contributing

This documentation is implementing a change control process. Therefore the repository follows a **PR-based workflow** 
There are 2 branches kept permanent : 
- ***'main'*** is the current client version (it contains a version file as the source code) the one that is viewed when accessing the documentation URL (see above)
- ***'pre-develop'*** is the next version being worked on
- Once a month , when a new code version is prepared, the documentation files follow the same process with a ***review of pending PRs pull requests*** before the pre-develop is merged on main

**Required actions :** 
- Find the file you want to update and fork it from 'pre-develop' (or create a new file)
- IF you work locally
  1. Make sure your local copy is in sync with `pre-develop`:
   ```bash
   git fetch origin
   git rebase origin/pre-develop
   ```
  2. Create a feature branch or fork the file, make your changes, then open a pull request **against `pre-develop`**

- once edited, create a **pull request** for review and inclusion at the next update cycle

*note:* direct pushes to `main` or 'pre-develop' are blocked
*note2:* GitHub Pages builds and publishes automatically once the PR is merged

---
 
## Reference : Source repositories
 
| Repo | Purpose | Status |
|---|---|---|
| **https://github.com/AnyLog-co/documentation** | Old docs — ~279 files, comprehensive but unorganised, not a website | Source of truth for migration |
| **EdgeLake documentation site** | Ori's first Jekyll attempt — limited, semi-organised | To be deprecated |
| **https://github.com/AnyLog-co/anylog-docs.github.io** (branch: `main`) | New Jekyll site — active development | Work in progress |

---

## Adding or Updating Content

### 1. Create or edit a page

Documentation pages live in the upstream `AnyLog-co/documentation` repository. Create a new Markdown file or edit an existing one there:

```
<path-in-AnyLog-co/documentation>/<specific-topic>.md
```

The sync script adds Jekyll front matter automatically. Page titles can still come from upstream front matter or headings, but the left sidebar label is always the Markdown filename without the `.md` extension.

If you do add front matter upstream, this site recognizes the `title` and `description` fields:

```yaml
---
title: Introduction to AnyLog
description: Understanding AnyLog's architecture, node types, and core concepts.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-05-12 | updated by ...
--> 
```
Evey file **must** contain a header change log so when reading it one knows when changed / who did it / what date and Anylog version,  use this table format
| Date of change | Relevant Anylog code version | Author | Description |
|---|---|---|---|
| - | - | - | Documentation Copyright Anylog.co 2026 |
| 2026-04-19 | All | Eric Aquaronne | update readme for Anylog |


### 2. Register it in the navigation

Navigation is generated from the synced upstream files. The left sidebar section title is the folder that contains the Markdown file; root-level Markdown files are grouped under `Documentation`.

`.github/scripts/navigation.py` is now only used for optional ordering overrides for known slugs:

```python
ITEM_ORDER = {
    "Getting Started": [
        "getting-started",
        "installing-anylog",
        "my-topic"       # ← add your slug here
    ],
    ...
}
```

The slug is the synced path without the `.md` extension after the sync script normalizes spaces and punctuation. The sidebar display name is the synced filename without `.md`. The order of slugs within each section controls the order they appear in the sidebar.

`navigation.py` is consumed by `validate_docs.py`, which scans the generated `_docs/` directory and writes the `nav` block in `_config.yml`. This runs automatically on `docker compose up` and in GitHub Actions — you do not need to invoke it manually.

---

## Editing/Writing Guidelines

- **Use absolute permalink paths** for links between doc pages — Jekyll builds each page at `/docs/<section>/<slug>/` regardless of which folder the source file is in, so relative paths will break:
```markdown
  [Install](/docs/getting-started/installing-anylog/)
  [Background Services](/docs/network-services/background-services/#rest-service)
```
  The slug is always the filename without `.md`, lowercased, under its section directory name (also lowercased with hyphens).
- **External links** must open in a new tab:
```html
  <a href="https://example.com" target="_blank">Link text</a>
```
- Keep front matter `description` to a single sentence — it appears as the subtitle under the page title
- Keep to short sentences, add drawings/pics (PNG files) to make it easy to understand for readers that probably will be more OT than IT skills base

---

- The title at the top is also used as the page title, there's no need for double title 
**Example**: How not to define the Makefile  
```markdown
---
title: Introduction to AnyLog
description: Understanding AnyLog's architecture, node types, and core concepts.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-05-12 | updated by 
--> 
# Introduction to AnyLog
[content] 
```

---

## Leveraging Claude LLM to Update a Doc Page

A reliable pattern for getting Claude to rewrite or update a page while keeping it consistent with the rest of the docs:

1. Provide the **raw GitHub URL** of the file to update — in GitHub, open the file and click **Raw**, then copy the address bar URL
2. Provide the **raw GitHub URL** of an existing page whose layout you want the output to match
3. Include the required front matter block in your prompt
4. Ask Claude to rewrite the first file to match the structure and style of the second

Keep the prompt substantive — include at least a short paragraph describing the intent and audience for each major section you want changed, not just bullet points. The more context you give about tone, audience, and structure, the better the result.

### Sample prompt

The following is a real example using `remote-gui.md`. Copy and adapt it for any page you want to update.

---

> I need you to update the AnyLog documentation page for the Remote GUI.
>
> **File to update (raw URL):**
> `https://raw.githubusercontent.com/AnyLog-co/anylog-docs.github.io/refs/heads/main/_docs/Tools-UI/remote-gui.md`
>
> **Example file to match in style and structure (raw URL):**
> `https://raw.githubusercontent.com/AnyLog-co/anylog-docs.github.io/refs/heads/main/_docs/Getting-Started/getting-started.md`
>
> **Required front matter — keep this exactly at the top of the file:**
> ```yaml
> ---
> title: Remote GUI
> description: Architecture and developer reference for the AnyLog Remote GUI.
> layout: page
> ---
> ```
>
> **What to change:**
>
> The current page reads like internal notes — it's dense and assumes the reader already knows the codebase. Rewrite it so a new developer joining the project can follow it from top to bottom. The architecture diagram and key terminology table are good and should stay, but the surrounding prose needs more context.
>
> The "Running locally" section currently has two terminal blocks with commands that aren't explained — add a sentence before each block describing what it does and why. The `uvicorn` command in particular looks like it may have a path issue (`CLI.local-cli-backend.main:app` uses dots but the `cd` above already entered the subdirectory); please flag that or correct it.
>
> The "Plugin system" section is the most important part for contributors — expand the intro paragraph to explain *when* someone would want to build a plugin versus modifying a core feature. Keep the code examples as-is.
>
> Use absolute permalink paths for links to other pages in `_docs/` — e.g. `/docs/network-services/background-services/`. Any link to an external repo or external site should use `<a href="URL" target="_blank">` format. Do not change any section headings — the navigation relies on them.

---

Adjust the URLs, front matter, and the description of changes to match whatever page you are working on.

---



## Local Development with Docker

The easiest way to preview the docs locally is via Docker — no Ruby or Jekyll installation required.

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

```bash
git clone https://github.com/AnyLog-co/anylog-docs.github.io.git
cd anylog-docs.github.io
docker compose up -d
```

Once running, open your browser to **http://localhost:4000**.

The container mounts your local `_docs/` directory, so edits are reflected live — no restart needed. To stop:

```bash
docker compose down
```

**Troubleshooting:** If the container exits immediately with a bundle write permissions error (`There was an error while trying to write to /srv/bundle`), run:

```bash
docker compose down -v
docker compose up -d
```

The `-v` flag removes the cached volume so it gets recreated with the correct permissions.

## Local Mac Development

Use the local launcher when you want to run Jekyll directly on macOS without Docker:

```bash
python3 scripts/dev.py
```

The launcher pulls the external documentation, rebuilds `_docs/` and `_config.yml`, installs Bundler and gems into
`vendor/`, and starts Jekyll at **http://localhost:4000**.

macOS system Ruby is not supported for this project because it often lacks the headers needed to build Jekyll's native
gems. Use Ruby 3.x rather than Ruby 4 for GitHub Pages compatibility. Install Homebrew Ruby 3.3 first:

```bash
brew install ruby@3.3
python3 scripts/dev.py
```

Or let the launcher install Homebrew Ruby 3.3:

```bash
python3 scripts/dev.py --install-ruby
```