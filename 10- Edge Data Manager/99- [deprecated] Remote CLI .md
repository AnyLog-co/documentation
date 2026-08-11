---
title: Remote GUI
description: Architecture, deployment, and developer reference for the AnyLog Remote GUI (successor to Remote-CLI).
layout: page
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 |            |                |                  |          |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-04-17 |                | file creation    |  |
--->

> **Note:** This page merges and replaces the deprecated *Remote-CLI* documentation. Remote-CLI was AnyLog's earlier web interface for executing REST requests against the network; the Remote GUI is its successor (React frontend + FastAPI backend). Deployment steps below are carried over from the Remote-CLI doc — double-check the paths, image names, and pod/volume names against the current `deployments/` repo before relying on them, since they haven't been re-verified against the new project layout.

> **Audience:** This page covers the internal architecture of the Remote GUI and is primarily intended for developers extending or contributing to it. For end-user usage, refer to the GUI itself.

## What is the Remote GUI?

The Remote GUI is a browser-based control panel for working with AnyLog nodes. It supports command execution, monitoring, SQL queries, file management, and bookmarks/presets — with an optional plugin system for additional capabilities.

It is split into two components:
- **React frontend** — the browser UI (`CLI/local-cli-fe-full`)
- **FastAPI backend** — the API server, node access layer, and plugin router (`CLI/local-cli-backend`)

---

## Architecture

```
[ User / Browser ]
       │
       ▼
[ React SPA (Frontend) ]
       │  HTTP requests
       ▼
[ FastAPI Backend ]
       │  AnyLog commands
       ▼
[ AnyLog Node (host:port) ]
```

1. The user interacts with frontend features to send commands or queries
2. Requests are sent from the frontend to the FastAPI backend
3. The backend routes commands to the target AnyLog node
4. The node executes the command and returns output
5. The backend may parse the output before returning it
6. Results are displayed in the frontend

---

## Key terminology

| Term | Description |
|---|---|
| `Remote-GUI` | This product/repo — web UI + API server |
| `Backend` | `CLI/local-cli-backend` — FastAPI app (`main.py`), mounts routers and `/static` |
| `Frontend` | `CLI/local-cli-fe-full` — React/Vite SPA |
| `Feature` | A first-class UI area (client, monitor, sqlquery, bookmarks…) toggled in `feature_config.json` |
| `Plugin` | An optional vertical: a folder under `plugins/` on both backend and frontend with extra routes and a `*Page.js` screen |
| `Connection / node` | A target `host:port` the user selects; the backend runs commands against it |
| `VITE_API_URL` | Base URL for API calls (build-time for Vite; Docker `start.sh` writes `config.js` for runtime) |
| `feature_config.json` | Enables/disables features and plugins; frontend reads `/feature-config` |
| `plugin_order.json` | Optional ordering for sidebar loading |
| `api_router` | The `FastAPI APIRouter` instance each backend plugin must export for auto-loading |

---

## Backend architecture

`main.py` hosts the FastAPI app, CORS configuration, middleware, and core routes (e.g. `send-command`, `monitor`). It also includes routers for core functionality such as `sql_router`.

New features are built as **plugins** in the `plugins/` folder:
- `plugins/loader.py` scans for `plugins/<pluginname>/<pluginname>_router.py`, imports the `api_router`, and respects `plugin_order.json` and `feature_config.json`
- Middleware blocks paths when a feature is disabled
- `helpers.py` and `parsers.py` handle JSON parsing and shared utilities

> **Note:** Always install the `anylog-api` pip package — the Remote GUI is built on top of it.

---

## Frontend architecture

The frontend is a standard React app under `CLI/local-cli-fe-full/src/`:

```
src/
├── assets/        — images, logo
├── components/    — reusable elements and tables
├── pages/         — core pages (corresponding to main.py routes)
├── services/      — API endpoint functions + feature config for plugins
├── styles/        — CSS files
└── plugins/       — frontend equivalents of backend plugins
    └── loader.js  — autodiscovers src/plugins/*/**Page.js
```

`services/featureConfig.js` fetches `/feature-config`, caches it, and uses `isPluginEnabled` to filter plugin routes.

Each plugin's `*Page.js` can export a `pluginMetadata` object (`{ name, icon }`) for sidebar labeling. The route path matches the folder name.

---

## Running locally (development)

You'll need two terminals.

**Terminal 1 — Backend:**

```bash
cd CLI/local-cli-backend/
python -m venv venv && source venv/bin/activate
cd ../..
pip install -r requirements.txt
# Also install the anylog-api pip package
uvicorn CLI.local-cli-backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**

```bash
cd CLI/local-cli-fe-full/
npm install
npm start
# If needed, set VITE_API_URL to point at the backend port
```

Alternatively, use `make up` or build with Docker:

```bash
docker build -f Dockerfile . -t anylogco/remote-gui:latest
docker compose -f docker-compose.yaml up -d
```

---

## Deploying to production

<!-- Carried over from the deprecated Remote-CLI doc. The directory/volume/pod names below
     (e.g. "remote-cli") reflect the old product's deployments/ layout — confirm whether the
     current deployments repo uses "remote-gui" naming instead before publishing. -->

### Via Docker Compose
1. Clone the deployments directory and `cd` into the Remote GUI's compose directory:
   ```shell
   git clone https://github.com/AnyLog-co/deployments
   cd $HOME/deployments/docker-compose/remote-cli/
   ```
2. Update configuration:
   ```shell
   vim .env
   ```
3. Deploy:
   ```shell
   docker-compose up -d
   ```

### Via Kubernetes (Helm)
1. Clone the deployments directory:
   ```shell
   git clone https://github.com/AnyLog-co/deployments
   ```
2. Update configuration:
   ```shell
   # volume configuration
   vim $HOME/deployments/helm/sample-configurations/remote_cli_volume.yaml

   # deployment configuration
   vim $HOME/deployments/helm/sample-configurations/remote_cli.yaml
   ```
3. Deploy the volume — as long as it exists on the node, data will be persistent:
   ```shell
   helm install $HOME/deployments/helm/packages/remote-cli-volume-1.0.0.tgz --name-template remote-cli-vol --values $HOME/deployments/helm/sample-configurations/remote_cli_volume.yaml
   ```
4. Deploy the instance:
   ```shell
   helm install $HOME/deployments/helm/packages/remote-cli-1.0.0.tgz --name-template remote-cli --values $HOME/deployments/helm/sample-configurations/remote_cli.yaml
   ```

### Accessing the deployed instance

By default the GUI is reachable at `http://${YOUR_LOCAL_IP}:31800`.

Configuration that used to live in Remote-CLI's `commands.json` (default command shortcuts shown in the UI) is superseded in the Remote GUI by `feature_config.json` and `plugin_order.json`, described under <a href="#key-terminology" target="_blank">Key terminology</a> above. If you still need the old-style editable command list on a running container/pod:

**On Docker:**
1. Get the volume path: `docker volume inspect remote-cli` (name may differ under the new deployment — check `docker volume ls`)
2. `cd` into that path
3. Edit the relevant JSON file with `sudo vim`
4. Save your changes
5. If changes don't appear automatically, restart the container: `docker restart <container-name>`

**On Kubernetes:**
1. Attach to the active pod: `kubectl exec -it ${REMOTE_GUI_POD_NAME} bash`
2. `cd` into the config directory inside the pod
3. Edit the relevant JSON file with `vim`
4. Save
5. Detach from the pod: `ctrl-p` + `ctrl-q`

> Note: on Kubernetes, changes made this way are **not persistent** across pod restarts unless backed by a <a href="../Networking%20%26%20Security/kubernetes%20volumes.md" target="_blank">persistent volume</a>.

---

## Plugin system

### Creating a new plugin

**Backend** — create `CLI/local-cli-backend/plugins/<name>/<name>_router.py` exporting `api_router`:

```python
from fastapi import APIRouter
api_router = APIRouter(prefix="/<name>", tags=["<name>"])

@api_router.get("/example")
def example():
    return {"status": "ok"}
```

**Frontend** — create `CLI/local-cli-fe-full/src/plugins/<name>/<name>Page.js`:

```js
export const pluginMetadata = { name: 'My Plugin', icon: '🔌' }

export default function MyPluginPage() {
  return <div>My Plugin</div>
}
```

**Register in `feature_config.json`** (both backend and frontend):

```json
{
  "plugins": {
    "<name>": { "enabled": true, "description": "My plugin" }
  }
}
```

**Optional:** Add `<name>` to `plugin_order.json` to control sidebar position.

**API calls in frontend:** Use `window._env_?.VITE_API_URL` (or generated `*_api.js` wrappers) with paths under your router prefix.

After changes: restart the backend; rebuild the frontend if running a production build (dev server hot-reloads automatically).

---

## Long-term roadmap

- Mobile application support
- Dashboard integration (Grafana or in-app)
- Full plugin modularization — every feature becomes a plugin; the base Remote GUI becomes a minimal image with a downloadable plugin catalog

---

## See also

- Examples of driving the underlying API can be found in the <a href="../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/remote_cli.md" target="_blank">northbound connectors</a> section.