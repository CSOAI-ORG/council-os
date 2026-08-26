# dsh-mcp — one shared harness, spoken over MCP

Bridge that exposes a DSH (DeepSeek Harness) web server as MCP tools, so
Claude Code — and later any MCP-speaking platform — drives the same
harness/workspace.

## Architecture (the whole thing)

```
RunPod pod (GPU)                          Mac (or any client machine)
┌─────────────────────────┐               ┌──────────────────────────────┐
│ dsh web                 │   SSH tunnel  │ localhost:3081/3082/...      │
│ 127.0.0.1:3080 ONLY     │◄──────────────┤ (launchd com.meok.dsh-tunnel)│
│ workspace + sessions    │  -L 3081:...  │        │                     │
└─────────────────────────┘               │        ▼                     │
                                          │ dsh-mcp-server.py (stdio)    │
  local DSH on the Mac                    │        │                     │
  (127.0.0.1:3090) works the ──────────►  │        ▼                     │
  same way, no tunnel needed              │ Claude Code / any MCP client │
                                          └──────────────────────────────┘
```

- DSH's web API is unary JSON-RPC over HTTP: `POST /api/<method>` with a
  `client-request` envelope (plus two SSE event streams this bridge doesn't
  use). Methods exposed here: `host.describe`, `session.list/create/prompt/
  history/cancel`, `workspace.list`, `host.listDirectory`.
- **Security**: DSH has no request auth. It must bind `127.0.0.1` only —
  never `0.0.0.0`. The SSH tunnel is the auth boundary. `pod-setup.sh`
  enforces this; do not change it.
- `DSH_URL` selects the target harness (local `:3090`, or a tunnel port for a
  pod). `DSH_TOKEN` is sent as a Bearer header for a future authenticating
  proxy; today nothing checks it.

## Files

| file | purpose |
|---|---|
| `dsh-mcp-server.py` | stdio MCP server; proxies tools to `DSH_URL` |
| `pod-setup.sh` | idempotent: install node + dsh on a pod, run `dsh web` on `127.0.0.1:3080` under nohup |
| `tunnel.plist.template` | launchd SSH tunnel template (matches the existing `com.meok.dsh-tunnel-*` jobs) |
| `install.sh` | prints the exact registration commands (does not run them) |

## Register

```
claude mcp add dsh-harness -- python3 /Users/nicholas/clawd/council-os/bridges/dsh-mcp/dsh-mcp-server.py
# pod via tunnel:
claude mcp add dsh-harness --env DSH_URL=http://127.0.0.1:3081 -- python3 /Users/nicholas/clawd/council-os/bridges/dsh-mcp/dsh-mcp-server.py
```

Prereq: `pip3 install mcp` (same as the other house bridges).

## Tools

`dsh_health` · `dsh_list_sessions` · `dsh_list_workspaces` ·
`dsh_create_session` · `dsh_run_task` (submit prompt; queue or steer) ·
`dsh_get_output` (poll history + running flag) · `dsh_cancel` ·
`dsh_workspace_ls`

## Test record (2026-08-26, local DSH 127.0.0.1:3090, dsh 0.1.1-rc.2)

**Verified** (real stdio MCP handshake — initialize, tools/list, tools/call):
- initialize + tools/list: all 8 tools listed.
- `dsh_health`: returned live host.describe (provider deepseek-official,
  model deepseek-v4-flash-vision-exp, 2 attached sessions).
- `dsh_list_sessions`, `dsh_list_workspaces`: live data returned.
- `dsh_run_task` → `dsh_get_output` → completion detection: full loop ran;
  session created, prompt accepted, polled to `running: false`, event stream
  parsed into messages. The model's reply itself failed with the provider's
  `Insufficient Balance` (402 QUOTA) — an account state, not a bridge fault;
  the bridge surfaces it as `last_turn_end`.
- `dsh_cancel`: accepted against a live session.

**Built, untested**:
- `pod-setup.sh` and `tunnel.plist.template` (no pod was touched per
  constraints; the tunnel template is copied from the working
  `com.meok.dsh-tunnel-master-mine` job).
- `dsh_workspace_ls` against a pod. On the local Mac profile it returns
  DSH's own `directory-picker-unavailable` error (the desktop profile
  composes the "native" picker, not "browse"); a headless pod profile may
  differ — verify on-pod.
- `DSH_TOKEN` passthrough (nothing checks it today).

**Not built** (future lanes, stated honestly):
- AG-UI cards for end-users (chat-first Council OS direction).
- A2A.
- Remote HTTP+SSE MCP endpoint with real token auth for use without an SSH
  tunnel — does not exist yet; today the tunnel is the only supported path.
