#!/usr/bin/env bash
# install.sh — print (not run) the exact registration commands for the DSH MCP bridge.
# The bridge itself has no dependencies beyond `pip install mcp` (already the
# house pattern for the other local MCP bridges).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER="${HERE}/dsh-mcp-server.py"

python3 -c "import mcp" 2>/dev/null || echo "NOTE: run first:  pip3 install mcp"

cat <<EOF

Register with Claude Code (local DSH on 3090):

  claude mcp add dsh-harness -- python3 ${SERVER}

Register pointing at a pod tunnel (example: master-mine tunnel on 3081):

  claude mcp add dsh-harness --env DSH_URL=http://127.0.0.1:3081 -- python3 ${SERVER}

Claude Desktop / Cursor (claude_desktop_config.json style):

  "dsh-harness": {
    "command": "python3",
    "args": ["${SERVER}"],
    "env": { "DSH_URL": "http://127.0.0.1:3090" }
  }

Tunnel to a pod: fill in tunnel.plist.template (see comments inside), then:

  cp com.meok.dsh-tunnel-<name>.plist ~/Library/LaunchAgents/
  launchctl load ~/Library/LaunchAgents/com.meok.dsh-tunnel-<name>.plist
  launchctl start com.meok.dsh-tunnel-<name>

Smoke test without any MCP client:

  DSH_URL=http://127.0.0.1:3090 python3 ${SERVER} --test
EOF
