# GitHub Actions CI Automation

This repository uses **GitHub Actions** to automatically update the project version (`setup.cfg`), maintain the changelog, and build and push Docker images whenever branches are updated.

Because some branches (like `ms-dev`) are **protected branches**, normal workflows using `GITHUB_TOKEN` cannot push commits to them.
To solve this, we use a **GitHub App (`anylog-ci-bot`)** to authenticate and push updates.

This document explains:

* Why the GitHub App exists
* How the workflows work
* How to configure new branches to use the same automation

---

# Architecture Overview

Two workflows exist:

```
.github/
├─ scripts/
│   ├─ generate_git_id.py
│   └─ version_control.py
└─ workflows/
    ├─ ci.yml
    └─ version-update-ms-dev.yml
```

| File                        | Purpose                                                          |
| --------------------------- | ---------------------------------------------------------------- |
| `generate_git_id.py`        | Python script that updates the version inside `setup.cfg`        |
| `version_control.py`        | Python script that updates `CHANGELOG.md`                        |
| `ci.yml`                    | Generic workflow for all branches except `ms-dev`                |
| `version-update-ms-dev.yml` | Special workflow that can push to protected branch `ms-dev`      |

---

# Branch Behavior

| Branch         | Version bump | CHANGELOG | Docker build         |
| -------------- | ------------ | --------- | -------------------- |
| `os-dev`       | ✅           | ✅        | ✅ (no tag)          |
| `pre-develop`  | ✅           | ❌        | ✅ (versioned tag)   |
| `main`         | ✅           | ❌        | ✅ (`latest`)        |
| `ms-dev`       | ✅           | ❌        | ❌                   |
| any other      | ✅           | ❌        | ❌                   |

---

# Why a GitHub App Is Required

GitHub protected branches often block pushes from the default GitHub Actions token (`GITHUB_TOKEN`).

Example error:

```
remote: error: GH006: Protected branch update failed
You're not authorized to push to this branch
```

To bypass this restriction securely, we created a **GitHub App**:

```
anylog-ci-bot
```

The workflow generates an **installation token** from the app and uses it for the push.

This allows automation while keeping branch protection enabled.

---

# GitHub App Configuration

The GitHub App must have the following permissions and repository access.

### Permissions

```
Repository permissions:
  Contents → Read & Write
```

### Repository Access

Install the app on the organization:

```
AnyLog-co
```

and grant access to:

```
AnyLog-Network
```

---

# Repository Secrets

The workflows require the following secrets, configured under:

```
Settings → Secrets → Actions
```

| Secret              | Used by                  | Description                           |
| ------------------- | ------------------------ | ------------------------------------- |
| `GITHUB_TOKEN`      | `ci.yml`                 | Auto-provided by GitHub Actions       |
| `ANYLOG_APP_ID`     | `version-update-ms-dev`  | GitHub App ID                         |
| `MOSHE_PEM`         | `version-update-ms-dev`  | Private key (.pem) for the GitHub App |
| `DOCKERHUB_USERNAME`| `ci.yml`                 | Docker Hub username                   |
| `DOCKERHUB_TOKEN`   | `ci.yml`                 | Docker Hub access token               |

Example private key format:

```
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

Never commit this file to the repository.

---

# Protected Branch Configuration

If a branch is protected, the GitHub App must be allowed to push.

Go to:

```
Repository → Settings → Branches
```

Edit the rule for the branch (example: `ms-dev`) and add:

```
anylog-ci-bot (GitHub App)
```

under:

```
Restrict who can push to matching branches
```

---

# Workflow: Standard Branches (`ci.yml`)

Triggers on pushes to all branches **except** `ms-dev`.

Bot commits are ignored to prevent infinite loops:

```yaml
if: github.actor != 'anylog-ci-bot[bot]' && github.actor != 'github-actions[bot]'
```

### Jobs

**`update-version`** — runs on every branch

```
push
 ↓
checkout repository
 ↓
git pull --rebase (avoid conflicts)
 ↓
run generate_git_id.py → updates setup.cfg
 ↓
commit and push
 ↓
[os-dev only] run version_control.py → updates CHANGELOG.md
 ↓
commit and push
```

**`docker-build`** — runs only on `os-dev`, `pre-develop`, `main`

```
pull latest
 ↓
build image
 ↓
push to Docker Hub

Tags:
  pre-develop → version string from setup.cfg
  main        → latest
  os-dev      → no tag
```

Authentication:

```
GITHUB_TOKEN
```

---

# Workflow: Protected Branch (`version-update-ms-dev.yml`)

Triggers on pushes to `ms-dev` only.

Because the branch is protected, the workflow:

1. Generates a GitHub App token
2. Checks out the repository using the app token
3. Updates the version in `setup.cfg`
4. Pushes back to `ms-dev`

Key step:

```yaml
- name: Generate GitHub App token
  id: app-token
  uses: actions/create-github-app-token@v1
  with:
    app-id: ${{ secrets.ANYLOG_APP_ID }}
    private-key: ${{ secrets.MOSHE_PEM }}
    owner: AnyLog-co
    repositories: AnyLog-Network
```

---

# How to Enable Automation for Another Protected Branch

Example: `release-dev`

### 1. Create a workflow

Copy:

```
version-update-ms-dev.yml
```

Rename:

```
version-update-release-dev.yml
```

Update the trigger:

```yaml
on:
  push:
    branches:
      - release-dev
```

Update the push target:

```yaml
git push origin HEAD:release-dev
```

### 2. Allow the GitHub App to push

```
Repo → Settings → Branches
```

Edit the rule for `release-dev` and add `anylog-ci-bot` under:

```
Restrict who can push to matching branches
```

### 3. Commit the workflow

```
git add .github/workflows/version-update-release-dev.yml
git commit -m "add version automation for release-dev"
git push
```

The automation will now run for the new branch.

---

# Adding a New Standard Branch

Any branch that is **not** `ms-dev` will automatically get version bump automation from `ci.yml` — no changes needed.

If you also want Docker builds to run for a new branch, add it to the `docker-build` job condition in `ci.yml`:

```yaml
if: |
  github.ref_name == 'pre-develop' ||
  github.ref_name == 'main'        ||
  github.ref_name == 'os-dev'      ||
  github.ref_name == 'your-new-branch'
```

Then add a matching branch in the `Build & Push` step to define its tag and platform behavior.

---

# Security Notes

* The GitHub App private key **must never be stored in the repository**.
* Always store it in **GitHub Actions Secrets**.
* If the key is ever exposed, rotate it immediately.

---

# Maintenance

If the GitHub App stops working:

1. Verify the app is installed on the organization
2. Verify repository permissions (`Contents → Read & Write`)
3. Verify secrets (`ANYLOG_APP_ID`, `MOSHE_PEM`)
4. Verify branch protection allows `anylog-ci-bot`

If `ci.yml` bot commits trigger the workflow in a loop, verify that both bot actor names are in the `if` guard:

```yaml
if: github.actor != 'anylog-ci-bot[bot]' && github.actor != 'github-actions[bot]'
```

---

# Summary

| Component            | Purpose                                      |
| -------------------- | -------------------------------------------- |
| `ci.yml`             | Version bump, CHANGELOG, Docker for all branches except `ms-dev` |
| `version-update-ms-dev.yml` | Version bump for protected `ms-dev` branch  |
| GitHub App           | Allows pushing to protected branches         |
| Actions Secrets      | Stores Docker Hub and GitHub App credentials |
| Branch rule          | Grants push permission to the bot            |