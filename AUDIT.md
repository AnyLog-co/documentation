# Cross-Tree Content Audit: `01-09` vs `anylog-docs` vs `edgelake-docs`

Legend: 
* **✓** = content actually read and compared. 
* No mark = grouped by filename/topic match only — verify before deleting.

## Getting Started / Onboarding

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `edgelake-docs/getting_started.md` ✓ | `01-getting-started/getting started.md`, `dictionary.md` (has a "Local Dictionary" section covering this) | `Getting-Started/getting-started.md` | — |
| `edgelake-docs/training/quick_start.md` | `01-getting-started/Fast Deployment.md`? (check overlap) | `Getting-Started/quick-start.md` | — |
| `edgelake-docs/training/fast_deployment.md` | `01-getting-started/Fast Deployment.md` | — | — |
| `anylog-docs/Getting-Started/installing-anylog.md` | `01-getting-started/Deploying_AnyLog.md`, `docker image.md`, `starting an anylog instance.md`, `registering pi in the anylog network.md` | `install-ova.md`, `deployment-scripts.md` | — |
| `anylog-docs/Getting-Started/anylog-as-service.md` | `01-getting-started/anylog as service.md`, `Executable.md`, `Service.md` | — | — |

## CLI

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `anylog-docs/CLI/AnyLog-CLI.md` | `02-cli/cli.md`, `anylog commands.md` | — | (partial overlap: CLI section inside `getting_started.md`) |
| `anylog-docs/CLI/get-cmds.md` | `02-cli/file commands.md`, `http commands.md`, `helpers.md` | — | — |
| `anylog-docs/Tools-UI/test-suite.md` | `02-cli/test commands.md`, `test suites.md`, `09-examples-training/testsuite.md` | — | — |
| `02-cli/cheatsheet.md` | — | — | — (unique, no overlap found) |
| `edgelake-docs/northbound/remote_cli.md` (largest, 14KB) | `02-cli/remote_cli.md`, `09-examples-training/[deprecated] Remote CLI .md` | `Tools-UI/remote-gui.md` | — |

## Network Services

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `edgelake-docs/commands/backgound_services.md` ✓ | (root, unmoved) `background processes.md` | `Network-Services/background-services.md` | — |
| `edgelake-docs/commands/network_processes.md` | `03-network-services/network configuration.md`, `network processing.md`, `node configuration.md` | `Network-Services/network-configurations.md`, `node-architecture.md` | — |
| `anylog-docs/Network-Services/messaging-services.md` | `03-network-services/message broker.md`, `09-examples-training/Broker Setup.md` | — | (section inside `backgound_services.md`) |
| `03-network-services/secure network.md` (only real candidate; no migrated copy exists yet) | `09-examples-training/_review/Secure Network.md` ✓ (confirmed exact duplicate) | — | — |
| `03-network-services/authentication.md`, `software tpm.md` | — | — | — (no overlap found; keep as-is) |
| `anylog-docs/Monitoring-Operations/high-availability.md` | `03-network-services/high availability.md` | — | — |
| `anylog-docs/Monitoring-Operations/scheduler.md` | `03-network-services/scheduled pull.md` | — | — |
| `03-network-services/master node.md` | — | — | — (no overlap found) |
| `edgelake-docs/training/kubernetes.md` + `advanced_kubernetes.md` | `03-network-services/kubernetes networking.md`, `kubernetes volumes.md` | — | — |
| `03-network-services/nebula_new.md` ✓ (revision of nebula.md, confirmed near-duplicate earlier) | `nebula.md` ✓, `nebula through anylog.md` (verify — may be distinct angle), `Configuring Overlay with AnyLog.md`, `nginx.md`, `docker volumes.md` | — | — |

## Southbound (Data In)

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `edgelake-docs/commands/data_management.md` | `04-southbound-services/adding data.md`, `mapping data to tables.md`, `json data transformation.md`, `image mapping.md`, `bucket data management.md`, `streaming conditions.md` | `Managing-Data-Southbound/data-ingestion.md`, `mapping-policies.md`, `southbound-overview.md` | — |
| `edgelake-docs/commands/metadata.md` | `04-southbound-services/metadata management.md`, `metadata requests.md` | — | — |
| `edgelake-docs/southbound/edgex.md` ✓ | `04-southbound-services/edgex.md`, `using edgex.md`, `data from edgex.md` | `Managing-Data-Southbound/edgex.md` | — |
| `edgelake-docs/southbound/kafka.md` | `04-southbound-services/using kafka.md` | `using-kafka.md` | — |
| `edgelake-docs/southbound/syslog.md` (largest) | `04-southbound-services/using syslog.md`, `09-examples-training/deployments/syslog.md` | `Managing-Data-Southbound/syslog.md` | — |
| `edgelake-docs/grpc.md` (root) | `04-southbound-services/using grpc.md` | `Managing-Data-Southbound/grpc.md` | — |
| `edgelake-docs/southbound/node_red.md` | `04-southbound-services/node red.md` | `Managing-Data-Southbound/node-red.md` | — |
| `edgelake-docs/southbound/telegraf.md` (larger) | — | `Managing-Data-Southbound/telegraf.md` | — |
| `anylog-docs/Managing-Data-Southbound/opcua.md` | `04-southbound-services/opcua.md` | — | — (no edgelake equivalent) |
| `anylog-docs/Managing-Data-Southbound/etherip.md` | `04-southbound-services/enthernetip.md` | — | — |
| `anylog-docs/Managing-Data-Southbound/video-streaming.md` | `04-southbound-services/video streaming.md` | — | — |
| `anylog-docs/Managing-Data-Southbound/live-data-generator.md` | `09-examples-training/Data Generator.md` | — | — |
| `anylog-docs/Network-Services/blockchain.md` | `04-southbound-services/blockchain commands.md`, `blockchain configuration.md` | — | (covered partly by `commands/metadata.md`) |
| `04-southbound-services/blockchain_demo.md`, `using ethereum.md`, `configuring mongodb.md` | — | — | — (no overlap found; verify if these are truly unique) |
| `edgelake-docs/southbound/fledge.md`, `kubearmor.md` | — | — | — (net-new EdgeLake topics, no AnyLog equivalent) |
| `anylog-docs/Managing-Data-Southbound/modbus.md`, `UNS.md`, `UNS-custom.md` | — | — | — (net-new, no overlap found) |

## Monitoring (split across southbound/northbound in your tree — needs its own verification pass)

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| **Unverified — flagging only.** Candidates: `anylog-docs/Monitoring-Operations/node-monitoring.md` vs `anylog-docs/Managing-Data-Southbound/node-monitoring.md` (note: **same filename exists twice inside anylog-docs itself**) vs `04-southbound-services/monitoring nodes.md` | `monitoring calls.md`, `alerts and monitoring.md`, `logging events.md`, `managing data files status.md`, `Data Monitoring.md`, `Resource Monitoring.md` | two `node-monitoring.md` files (internal anylog-docs dup) | `commands/backgound_services.md` links *out* to the old `monitoring nodes.md` on GitHub rather than replacing it — suggests EdgeLake hasn't written a replacement yet |
| `05-northbound-services/profiling and monitoring queries.md` | — | — | — |

## Northbound (Data Out / Querying)

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `edgelake-docs/commands/query_data.md` | `05-northbound-services/queries.md`, `Querying Data.md` | `Querying-Data-Northbound/queries.md` | — |
| `05-northbound-services/aggregations.md` | `Aggregations Examples.md` | `Monitoring-Operations/aggregations.md` | — |
| `04-southbound-services/sql setup.md` (misfiled — topic is northbound) | — | `Querying-Data-Northbound/sql-setup.md` | — |
| `edgelake-docs/northbound/Grafana.md` (largest, 22.6KB) | `05-northbound-services/dashboard generation.md`, `Import Grafana Dashboard.md`, `06-tools-ui/grafana.md`, `using grafana.md` | `Querying-Data-Northbound/grafana.md`, `import-grafana-dashboard.md` | — |
| `edgelake-docs/northbound/PowerBI.md` | `05-northbound-services/powerbi.md` | `Querying-Data-Northbound/PowerBI.md` | — |
| `anylog-docs/Querying-Data-Northbound/Qlik.md` | `05-northbound-services/qlik.md` | — | — (no edgelake equivalent) |
| `anylog-docs/Querying-Data-Northbound/postgres-connector.md` | `05-northbound-services/Postgres Connector.md` | — | — |
| `anylog-docs/Querying-Data-Northbound/Google.md` | `05-northbound-services/Google.md` | — | — |
| `edgelake-docs/northbound/notifciation.md` | `05-northbound-services/notifciation.md` | `Querying-Data-Northbound/notification.md` | — |
| `edgelake-docs/northbound/using_postman.md` | `06-tools-ui/using postman.md` | — | — |
| `edgelake-docs/northbound/repeatable_queries.md`, `twilio.md` | — | — | — (net-new, no overlap) |
| `anylog-docs/Tools-UI/mcp.md` | — | — | — (net-new, no overlap) |

## Reference

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `anylog-docs/Reference/FAQ.md` | `07-references/FAQ.md` | — | — |
| `anylog-docs/Reference/troubleshooting.md` | `07-references/common_issues.md` (verify overlap) | — | — |
| `07-references/configure_AWS.md`, `networking_MTU_size.md`, `policies.md`, licenses | — | — | — (no overlap found; keep) |

## Version Control

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `08-version-control/*` ✓ (already confirmed identical filenames — this is the wholesale copy made as a backup step) | — | `Version-Control/DEPLOYMENT_SCRIPTS-CHANGELOGS.md`, `DOCKER_COMPOSE-CHANGELOG.md`, `SOURCE-CHANGELOGS.md` (exact same files) | — |
| `08-version-control/notes.md` | — | — | — (unique, no dup) |

## REST docs

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `anylog-docs/Network-Services/using-rest.md` ✓ (read in full earlier — comprehensive) | (root, unmoved) `using rest.md` | — | `examples/rest_examples.md` (complementary worked-examples, not a pure duplicate — verify before merging) |

## Training / Demos

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `edgelake-docs/training/session1.md` | `09-examples-training/Session I (Demo).md` | — | — |
| `edgelake-docs/training/session2.md` | `09-examples-training/Session II (Deployment).md` | — | — |
| `edgelake-docs/training/prerequisite.md` | `01-getting-started/prerequisite.md` | — | — |
| `09-examples-training/advanced/*` (Config Policies, Network Setup, Pip Install, background deployment) | — | — | — (verify against `edgelake-docs/training/advanced_kubernetes.md` — possible overlap on the k8s-flavored ones) |

## Examples / Code

| best | duplicate (01-09) | anylog-docs | edgelake-docs |
|---|---|---|---|
| `edgelake-docs/examples/python_examples/*` (has `__init__.py` — actually packaged, aligns with the AnyLog-API plan) | `09-examples-training/Sample Python Scripts/*` (same `blockchain_add_policy_simple.py`, near-identical `data/` folder) | — | — |
| `edgelake-docs/examples/node_red_sample_flow.json` | `09-examples-training/node_red_sample_flow.json` | — | — |
| `edgelake-docs/northbound/jsons/network_summary.json` | `09-examples-training/grafana_json/network_summary.json` (same filename) | — | — |
| `09-examples-training/Sample Go Scripts/put_data.go` | — | — | — (no Go equivalent yet — future AnyLog-API Go target per earlier discussion) |
| `09-examples-training/curl.sh` | — | — | — (verify against `rest_examples.md` — may be redundant once that doc exists) |

## Internal duplicates worth flagging on their own

- `09-examples-training/Open Horizon.md` **and** `09-examples-training/OpenHorizon/Open Horizon.md` — same title, two copies, same tree.
- `anylog-docs/Managing-Data-Southbound/node-monitoring.md` **and** `anylog-docs/Monitoring-Operations/node-monitoring.md` — identical filename in two anylog-docs categories.
- `09-examples-training/deployments/syslog.md` is a **4th** copy of the syslog doc (alongside `04-southbound-services`, `anylog-docs`, `edgelake-docs`).

## Not yet migrated anywhere

- `background processes.md` and `using rest.md` are still sitting loose at the `documentation/` root — never went through the original move script.