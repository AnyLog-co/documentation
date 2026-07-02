#!/usr/bin/env bash
# reorg_docs.sh
# Moves the legacy flat `documentation/` content into the new 01-09 numbered tree.
# Run from inside the `documentation/` directory (the root that contains
# `Getting Started.md`, `deployments/`, `examples/`, `training/`, etc.)
#
#   cd /mnt/c/Users/oshad/AnyLog-code/documentation
#   bash reorg_docs.sh
#
# Safe to re-run: skips anything already moved, warns (doesn't fail) on missing files.

set -uo pipefail

DEST_GETTING_STARTED="01-getting-started"
DEST_CLI="02-cli"
DEST_NETWORK="03-network-services"
DEST_SOUTHBOUND="04-southbound-services"
DEST_NORTHBOUND="05-northbound-services"
DEST_TOOLS_UI="06-tools-ui"
DEST_REFERENCES="07-references"
DEST_VERSION_CONTROL="08-version-control"
DEST_EXAMPLES_TRAINING="09-examples-training"
DEST_REVIEW="${DEST_EXAMPLES_TRAINING}/_review"   # unmapped / needs-a-human-look items

MISSING_LOG="reorg_missing.log"
> "$MISSING_LOG"

mkdir -p \
  "$DEST_GETTING_STARTED" "$DEST_CLI" "$DEST_NETWORK" "$DEST_SOUTHBOUND" \
  "$DEST_NORTHBOUND" "$DEST_TOOLS_UI" "$DEST_REFERENCES" "$DEST_VERSION_CONTROL" \
  "$DEST_EXAMPLES_TRAINING" "$DEST_REVIEW"

# safe_mv SRC DEST_DIR
safe_mv() {
  local src="$1" dest_dir="$2"
  if [ -e "$src" ]; then
    mv -v -- "$src" "$dest_dir"/
  else
    echo "MISSING: $src" | tee -a "$MISSING_LOG"
  fi
}

echo "== 01-getting-started =="
safe_mv "getting started.md" "$DEST_GETTING_STARTED"
safe_mv "Deploying_AnyLog.md" "$DEST_GETTING_STARTED"
safe_mv "docker image.md" "$DEST_GETTING_STARTED"
safe_mv "starting an anylog instance.md" "$DEST_GETTING_STARTED"
safe_mv "quick deployment.md" "$DEST_GETTING_STARTED"
safe_mv "registering pi in the anylog network.md" "$DEST_GETTING_STARTED"
safe_mv "dictionary.md" "$DEST_GETTING_STARTED"
safe_mv "deployments/quick deployment.md" "$DEST_GETTING_STARTED"
safe_mv "deployments/anylog as service.md" "$DEST_GETTING_STARTED"
safe_mv "examples/Service AnyLog/Executable.md" "$DEST_GETTING_STARTED"
safe_mv "examples/Service AnyLog/Service.md" "$DEST_GETTING_STARTED"
safe_mv "examples/Service AnyLog/README.md" "$DEST_GETTING_STARTED"
safe_mv "training/prerequisite.md" "$DEST_GETTING_STARTED"
safe_mv "training/Fast Deployment.md" "$DEST_GETTING_STARTED"

echo "== 02-cli =="
safe_mv "cli.md" "$DEST_CLI"
safe_mv "anylog commands.md" "$DEST_CLI"
safe_mv "file commands.md" "$DEST_CLI"
safe_mv "http commands.md" "$DEST_CLI"
safe_mv "test commands.md" "$DEST_CLI"
safe_mv "test suites.md" "$DEST_CLI"
safe_mv "helpers.md" "$DEST_CLI"
safe_mv "northbound connectors/remote_cli.md" "$DEST_CLI"
safe_mv "deployments/Support/cheatsheet.md" "$DEST_CLI"

echo "== 03-network-services =="
safe_mv "network configuration.md" "$DEST_NETWORK"
safe_mv "network processing.md" "$DEST_NETWORK"
safe_mv "node configuration.md" "$DEST_NETWORK"
safe_mv "secure network.md" "$DEST_NETWORK"
safe_mv "software tpm.md" "$DEST_NETWORK"
safe_mv "authentication.md" "$DEST_NETWORK"
safe_mv "message broker.md" "$DEST_NETWORK"
safe_mv "high availability.md" "$DEST_NETWORK"
safe_mv "master node.md" "$DEST_NETWORK"
safe_mv "scheduled pull.md" "$DEST_NETWORK"
if [ -d "deployments/Networking & Security" ]; then
  mv -v "deployments/Networking & Security"/* "$DEST_NETWORK"/
else
  echo "MISSING: deployments/Networking & Security/*" | tee -a "$MISSING_LOG"
fi
# known exact duplicate of Securing the Network.md -> park for review instead of overwriting
safe_mv "examples/Secure Network.md" "$DEST_REVIEW"

echo "== 04-southbound-services =="
safe_mv "adding data.md" "$DEST_SOUTHBOUND"
safe_mv "json data transformation.md" "$DEST_SOUTHBOUND"
safe_mv "mapping data to tables.md" "$DEST_SOUTHBOUND"
safe_mv "image mapping.md" "$DEST_SOUTHBOUND"
safe_mv "bucket data management.md" "$DEST_SOUTHBOUND"
safe_mv "sql setup.md" "$DEST_SOUTHBOUND"
safe_mv "metadata management.md" "$DEST_SOUTHBOUND"
safe_mv "metadata requests.md" "$DEST_SOUTHBOUND"
safe_mv "streaming conditions.md" "$DEST_SOUTHBOUND"
safe_mv "opcua.md" "$DEST_SOUTHBOUND"
safe_mv "enthernetip.md" "$DEST_SOUTHBOUND"
safe_mv "using edgex.md" "$DEST_SOUTHBOUND"
safe_mv "using kafka.md" "$DEST_SOUTHBOUND"
safe_mv "using syslog.md" "$DEST_SOUTHBOUND"
safe_mv "using grpc.md" "$DEST_SOUTHBOUND"
safe_mv "using ethereum.md" "$DEST_SOUTHBOUND"
safe_mv "video streaming.md" "$DEST_SOUTHBOUND"
safe_mv "node red.md" "$DEST_SOUTHBOUND"
safe_mv "blockchain commands.md" "$DEST_SOUTHBOUND"
safe_mv "blockchain configuration.md" "$DEST_SOUTHBOUND"
safe_mv "blockchain_demo.md" "$DEST_SOUTHBOUND"
safe_mv "deployments/Support/edgex.md" "$DEST_SOUTHBOUND"
safe_mv "deployments/Support/data from edgex.md" "$DEST_SOUTHBOUND"
safe_mv "deployments/Support/configuring mongodb.md" "$DEST_SOUTHBOUND"
# monitoring split (no dedicated monitoring bucket in the 01-09 tree) -- operational side
safe_mv "monitoring nodes.md" "$DEST_SOUTHBOUND"
safe_mv "monitoring calls.md" "$DEST_SOUTHBOUND"
safe_mv "alerts and monitoring.md" "$DEST_SOUTHBOUND"
safe_mv "managing data files status.md" "$DEST_SOUTHBOUND"
safe_mv "logging events.md" "$DEST_SOUTHBOUND"
safe_mv "examples/Resource Monitoring.md" "$DEST_SOUTHBOUND"
safe_mv "examples/Data Monitoring.md" "$DEST_SOUTHBOUND"

echo "== 05-northbound-services =="
safe_mv "queries.md" "$DEST_NORTHBOUND"
safe_mv "aggregations.md" "$DEST_NORTHBOUND"
safe_mv "dashboard generation.md" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/Google.md" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/Import Grafana Dashboard.md" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/notifciation.md" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/Postgres Connector.md" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/powerbi.md" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/python_data.py" "$DEST_NORTHBOUND"
safe_mv "northbound connectors/qlik.md" "$DEST_NORTHBOUND"
safe_mv "examples/Querying Data.md" "$DEST_NORTHBOUND"
safe_mv "examples/Aggregations Examples.md" "$DEST_NORTHBOUND"
# monitoring split -- query/profiling side
safe_mv "profiling and monitoring queries.md" "$DEST_NORTHBOUND"

echo "== 06-tools-ui =="
safe_mv "northbound connectors/using grafana.md" "$DEST_TOOLS_UI"
safe_mv "northbound connectors/using postman.md" "$DEST_TOOLS_UI"
safe_mv "deployments/Support/grafana.md" "$DEST_TOOLS_UI"

echo "== 07-references =="
safe_mv "policies.md" "$DEST_REFERENCES"
if [ -d "Tips & Tricks" ]; then
  mv -v "Tips & Tricks"/* "$DEST_REFERENCES"/
else
  echo "MISSING: Tips & Tricks/*" | tee -a "$MISSING_LOG"
fi
if [ -d "license" ]; then
  mv -v license/* "$DEST_REFERENCES"/
else
  echo "MISSING: license/*" | tee -a "$MISSING_LOG"
fi

echo "== 08-version-control =="
safe_mv "release/notes.md" "$DEST_VERSION_CONTROL"

echo "== 09-examples-training (everything else) =="
# remaining examples/ content (after the specific files already pulled above)
if [ -d "examples" ]; then
  mv -v examples/* "$DEST_EXAMPLES_TRAINING"/ 2>>"$MISSING_LOG" || true
fi
# remaining training/ content
if [ -d "training" ]; then
  mv -v training/* "$DEST_EXAMPLES_TRAINING"/ 2>>"$MISSING_LOG" || true
fi
# Open-Horizon deployment demo
if [ -d "deployments/OpenHorizon" ]; then
  mv -v deployments/Open-Horizon "$DEST_EXAMPLES_TRAINING"/
fi
# whatever's left in deployments/Support (deprecated remote-cli writeup, demo configs, etc.)
if [ -d "deployments/Support" ]; then
  mv -v deployments/Support/* "$DEST_EXAMPLES_TRAINING"/ 2>>"$MISSING_LOG" || true
fi

echo
echo "== Cleanup check: now-empty source directories =="
for d in deployments examples training "northbound connectors" release "Tips & Tricks" license; do
  if [ -d "$d" ]; then
    if [ -z "$(ls -A "$d" 2>/dev/null)" ]; then
      echo "EMPTY (safe to rmdir): $d"
    else
      echo "NOT EMPTY, left some content behind: $d"
      ls -A "$d"
    fi
  fi
done

echo
echo "Done. Review $MISSING_LOG for anything that didn't match an expected source path."
echo "Review ${DEST_REVIEW}/ for items parked for manual verification (e.g. known duplicate of secure network.md)."