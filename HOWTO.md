# How To Document

The following document covers the internal workflow — repo setup, file/ID conventions, and formatting — for 
contributing to the AnyLog / EdgeLake documentation site. It does not cover writing style or terminology for the 
documentation content itself.

**General Process** (high-level overview — see the linked sections for the actual commands):
1. Clone the docs (see [Setting Up Env](#setting-up-env))
2. Create your own branch
3. Make sure your branch is up to date
4. Make changes (see [Documenting](#documenting))
5. Check / Test
6. Commit + push your changes (see [Validate Paths + Formatting](#validate-paths--formatting))

Steps 3 - 6 are to be repeated each time. 

## Setting Up Env

1. Clone repos 
   * <a href="https://github.com/AnyLog-co/documentation" target="_blank">Frontend</a> - actual documentation content
   * <a href="https://github.com/AnyLog-co/anylog-docs.github.io" target="_blank">Backend</a> - local GUI deployment (optional)

```shell
cd $HOME/ 

git clone https://github.com/AnyLog-co/documentation

# The example uses a shortened naming for the docs 
git clone https://github.com/AnyLog-co/anylog-docs.github.io anylog-docs
```

2. Checkout branch 

```shell
cd $HOME/documentation 
# create branch (need to do only once) 
git branch [branch name]
git push origin [branch name] 

# use branch - should be done each time you start documenting
git checkout [branch name]
git merge origin/[branch name] --sign

# update to the latest changes  
git merge origin/pre-develop --sign 
```

3. Build / Run local GUI (optional)

```shell
cd $HOME/anylog-docs 

docker compose -f ./docker-compose.yaml up --build -d 
```

4. View docs in browser - http://127.0.0.1:4000


## Documenting

1. Creating / Editing Page(s)

Documentation pages live in the upstream `AnyLog-co/documentation` repository. Create a new Markdown file or edit an 
existing one there:

```
<path-in-AnyLog-co/documentation>/#- <specific-topic>.md
```

The sync script adds Jekyll front matter automatically. Page titles can still come from upstream front matter or 
headings, but the left sidebar label is always the Markdown filename without the numeric ID or `.md` extension.

Numeric IDs keep file ordering, which guarantees their location in the table of contents / sidebar. Additionally, 
files with `99-` numeric ID are **ignored** and will not be added to the documentation. The `<ID>-<subID>` naming 
pattern (e.g., `02-1`, `04-2` in the tree example below) keeps files within the same topic (such as Unified Namespace 
- UNS) grouped under the same numeric ID, in logical order.

**Choosing an ID for a new page:** Existing top-level content is ordered to follow a typical user journey (e.g., 
intro to AnyLog → setting up your machine → installing AnyLog), so a page that fits into that sequence should be 
inserted at the appropriate position, renumbering later files as needed to keep the order intact. Most new content, 
though, is closer to a menu of related topics than a strict sequence (e.g., Security: TPM vs. HSM, Data Management: 
MinIO vs. other blob storage) — for these, just append the next available `<ID>-<subID>` (or top-level ID) under the 
relevant topic instead of renumbering existing files.

**Sample Tree Structure**: 

```tree
oshadmon@oris-yoga:/mnt/c/Users/oshad/AnyLog-code/documentation$ tree 08-\ Blockchain\ \&\ Metadata/
08- Blockchain & Metadata/
├── 01- Blockchain.md
├── 02- Policy & Metadata.md
├── 02-1 ANMP Policy.md
├── 03- Blockchain Commands.md
├── 03-1 Blockchain Full Circle.md
├── 04- Unified Namespace.md
├── 04-1 UNS Custom Dynamic Examples.md
└── 04-2 UNS Custom Examples.md
```

2. File Header

Every documentation file has to have front matter upstream; this site recognizes the `title` and `description` 
fields, in addition to a commented-out section with notes on the changes: 

```markdown
---
title: Introduction to AnyLog
description: Understanding AnyLog's architecture, node types, and core concepts.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Who created it | version # (if applicable) |  Created document
- 2026-05-12 | Updated by... | | what changed 
-->
```
> The title at the top is also used as the page title — there's no need for a duplicate title in the body.
> 
> Keep front matter `description` to a single sentence — it appears as the subtitle under the page title

Alternatively, the change log section can also be written  in table format 

| Date of change | Relevant Anylog code version | Author | Description |
|---|---|---|---|
| 2026-04-19 | All | Eric Aquaronne | update readme for Anylog |


3. Documentation Formatting 

* **Permalink Paths for Docs**

Jekyll builds each page at `/docs/<section>/<slug>/`, regardless of which folder the source file lives in. Because of 
this, links between doc pages should be written as standard **relative** Markdown paths — relative to the current 
file, the same way you'd link files in any repository. Pretend we are in the file 
[01- Getting Started/01- Introduction.md](01-%20Getting%20Started/01-%20Introduction.md):

```markdown
# Example: same directory as 01- Introduction.md
[install anylog](./03-%20install.md) 

# Example: different directory than 01- Introduction.md 
[Background Services](../07-%20CLI/02-%20Background%20Processes.md)
```

A backend script automatically converts these relative paths into full permalinks (`/docs/<section>/<slug>/`) before 
publishing — see **Update URLs** under [Validate Paths + Formatting](#validate-paths--formatting) below.

> Do not hand-write full `/docs/...` paths yourself. They may resolve correctly once built by Jekyll, but they will 
> not work when browsing a local deployment, and will definitely not work when viewing the raw file on GitHub, since 
> `/docs/...` is not an actual path in the repository.

The slug is always the filename without `.md`, lowercased, under its section directory name (also lowercased with 
hyphens). For reference, this is the permalink format the conversion script produces:

```markdown
[Install](/docs/getting-started/installing-anylog/)
[Background Services](/docs/network-services/background-services/#rest-service)
```

* **External links**

Since external links redirect outside of the document, the docs should use HTML in order to open a new tab instead of 
exiting the documentation. 

```html
<a href="https://example.com" target="_blank">Link text</a>
```

* **Image Paths**

Images and diagrams should be stored under [./imgs](./imgs) directory (in root), typically as _png_ for images and 
_svg_ for diagrams. 

To include an image either use standard Markdown **or** HTML - note that with HTML there's more control in terms of 
image size and relative location on the page. 

```markdown
![my image](../imgs/[img_name].png) 

<img src="../imgs/[img_name].png" alt="my image" />
```

## Validate Paths + Formatting 

**Before continuing to the next step, please commit your changes (and push)**

1. Update Table of Contents

```shell
python3 .github/scripts/generate_toc.py 
```

2. Update URLs

This converts external links and image references from Markdown syntax into HTML format: 

```markdown
<!-- Current --> 
[my link](https://example.com) 
![my img](../imgs/[img path].png) 

<!-- updated to --> 
<a href="https://example.com" target="_blank">my link</a>
<img src="../imgs/[my path].png" alt="my img" />
```

**Call**: 

```shell
python3 .github/scripts/convert_html.py $HOME/documentation
```

3. Validate Linkage Between Documentation Files

Validate that links between documentation files are up to date: 

```shell
# show a full list of all files, ignoring `HOWTO.md` and content starting with `99-` 

python3 .github/scripts/link_validation_ignore99.py $HOME/documentation

# Show one file at a time 
python3 .github/scripts/link_validation_ignore99_file.py $HOME/documentation
```

4. Double Check / Update Table of Contents

```shell
python3 .github/scripts/generate_toc.py 
```

5. Commit + Push Changes