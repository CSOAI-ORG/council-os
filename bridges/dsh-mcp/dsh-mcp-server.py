#!/usr/bin/env python3
"""DSH (DeepSeek Harness) MCP bridge.

Exposes a DSH `web` profile server (local process or SSH-tunnelled pod) as MCP
tools over stdio, so Claude Code — or any MCP client — can drive the same
harness/workspace a human uses in the DSH web UI.

DSH's web API (derived from @deepseek-ai/dsh-host-apiproxy, verified live):
  POST /api/<method>  with envelope
    {"type": "client-request", "rpcId": "<uuid>", "method": "<method>", "payload": {...}}
  responds
    {"type": "server-response", "rpcId": "...", "result": {"ok": true, "value": {...}}}
  Methods used here: host.describe, session.list, session.create,
  session.prompt, session.history, session.cancel, workspace.list,
  host.listDirectory. (Others exist: session.search/fork/rename, subagent.*,
  goal.*, settings.*, credentials.*, llm.* — add as needed.)
  Streams: GET /api/events.mux and /api/events.host are SSE; not used here
  (this bridge is unary request/response only).

Register (Claude Code):
    claude mcp add dsh-harness -- python3 /Users/nicholas/clawd/council-os/bridges/dsh-mcp/dsh-mcp-server.py

Environment:
    DSH_URL    base URL of the DSH web server (default http://127.0.0.1:3090).
               Point at a tunnel port (3081/3082/3083) to reach a pod.
    DSH_TOKEN  optional bearer token, sent as `Authorization: Bearer <token>`.
               NOTE: DSH 0.1.1-rc.2's web server does not check any request
               auth — the security boundary is 127.0.0.1 binding + SSH
               tunnels. The header is sent only so a future authenticating
               proxy can use it.
"""
import json
import os
import sys
import uuid
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise SystemExit("mcp package not installed; run: pip install mcp") from e

DSH_URL = os.environ.get("DSH_URL", "http://127.0.0.1:3090").rstrip("/")
DSH_TOKEN = os.environ.get("DSH_TOKEN", "")
TIMEOUT = int(os.environ.get("DSH_TIMEOUT", "30"))

mcp = FastMCP("dsh-harness")


def _rpc(method: str, payload: Dict[str, Any], timeout: int = TIMEOUT) -> Dict[str, Any]:
    """One unary DSH RPC. Returns {"ok": bool, "value"|"error": ...}."""
    envelope = {
        "type": "client-request",
        "rpcId": str(uuid.uuid4()),
        "method": method,
        "payload": payload,
    }
    headers = {"Content-Type": "application/json"}
    if DSH_TOKEN:
        headers["Authorization"] = f"Bearer {DSH_TOKEN}"
    req = urllib.request.Request(
        f"{DSH_URL}/api/{method}",
        data=json.dumps(envelope).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e} (is DSH up at {DSH_URL}? is the tunnel running?)"}
    result = body.get("result", {})
    if result.get("ok"):
        return {"ok": True, "value": result.get("value")}
    return {"ok": False, "error": result.get("error", body)}


def _trim(text: Any, limit: int = 2000) -> Any:
    if isinstance(text, str) and len(text) > limit:
        return text[:limit] + f"... [{len(text) - limit} chars trimmed]"
    return text


@mcp.tool()
def dsh_health() -> Dict[str, Any]:
    """Check the DSH harness is reachable and describe it (version, cwd, provider, model, attached sessions)."""
    result = _rpc("host.describe", {})
    return {"dsh_url": DSH_URL, **result}


@mcp.tool()
def dsh_list_sessions(full: bool = False) -> Dict[str, Any]:
    """List harness sessions. Compact by default (id, title, running, cwd, origin, updatedAt); full=True returns raw records."""
    result = _rpc("session.list", {})
    if not result.get("ok") or full:
        return result
    items = []
    for s in result["value"].get("items", []):
        proj = (s.get("projections") or {}).get("values", {})
        items.append({
            "sessionId": s.get("sessionId"),
            "title": proj.get("title"),
            "running": s.get("running"),
            "cwd": s.get("cwd"),
            "origin": s.get("origin"),
            "agentPreset": s.get("agentPreset"),
            "updatedAt": s.get("updatedAt"),
        })
    return {"ok": True, "sessions": items}


@mcp.tool()
def dsh_list_workspaces() -> Dict[str, Any]:
    """List DSH workspaces (workspaceId, path, title, sessionIds)."""
    return _rpc("workspace.list", {})


@mcp.tool()
def dsh_create_session(cwd: Optional[str] = None, agent_preset: Optional[str] = None) -> Dict[str, Any]:
    """Create a new harness session, optionally in a working directory and with an agent preset (e.g. 'standard')."""
    payload: Dict[str, Any] = {}
    if cwd:
        payload["cwd"] = cwd
    if agent_preset:
        payload["agentPreset"] = agent_preset
    return _rpc("session.create", payload)


@mcp.tool()
def dsh_run_task(prompt: str, session_id: Optional[str] = None, cwd: Optional[str] = None,
                 mode: str = "queue") -> Dict[str, Any]:
    """Submit a prompt/task to the harness. Creates a session if session_id is omitted (optionally in cwd).
    mode: 'queue' (run after current work) or 'steer' (interject into the running turn).
    Returns the session_id to poll with dsh_get_output — the task runs asynchronously."""
    if mode not in ("queue", "steer"):
        return {"ok": False, "error": "mode must be 'queue' or 'steer'"}
    if session_id is None:
        created = dsh_create_session(cwd=cwd)
        if not created.get("ok"):
            return {"ok": False, "error": f"session.create failed: {created.get('error')}"}
        session_id = created["value"]["sessionId"]
    result = _rpc("session.prompt", {
        "sessionId": session_id,
        "mode": mode,
        "content": [{"type": "text", "text": prompt}],
    })
    if result.get("ok"):
        return {"ok": True, "sessionId": session_id, "accepted": result["value"].get("accepted", True),
                "note": "task submitted; poll dsh_get_output(session_id) for results"}
    return {"ok": False, "sessionId": session_id, "error": result.get("error")}


@mcp.tool()
def dsh_get_output(session_id: str, max_messages: int = 20, raw: bool = False) -> Dict[str, Any]:
    """Fetch recent messages from a session (newest window; pages backwards from the tail).
    Also reports whether the session is still running. raw=True returns unprocessed history."""
    hist = _rpc("session.history", {"sessionId": session_id, "maxMessages": max_messages})
    if not hist.get("ok"):
        return hist
    running = None
    listed = _rpc("session.list", {})
    if listed.get("ok"):
        for s in listed["value"].get("items", []):
            if s.get("sessionId") == session_id:
                running = s.get("running")
                break
    if raw:
        return {"ok": True, "running": running, "history": hist["value"]}
    # session.history returns an event stream: {"events":[{"event":{type,seq,time,data}}],
    # "hasMore":..., "projections":...}. Extract the conversation-shaped events.
    value = hist["value"]
    messages: List[Dict[str, Any]] = []
    turn_end: Optional[Dict[str, Any]] = None
    for wrapper in value.get("events", []):
        ev = wrapper.get("event", wrapper) if isinstance(wrapper, dict) else {}
        etype = ev.get("type", "")
        data = ev.get("data", {}) or {}
        if etype in ("user/message", "assistant/message"):
            content = data.get("content", [])
            texts = [c.get("text") for c in content
                     if isinstance(c, dict) and c.get("type") == "text" and c.get("text")]
            other = [c.get("type") for c in content
                     if isinstance(c, dict) and c.get("type") != "text"]
            entry: Dict[str, Any] = {"role": data.get("role", etype.split("/")[0]),
                                     "seq": ev.get("seq"), "text": _trim("\n".join(texts))}
            if other:
                entry["other_content"] = other
            messages.append(entry)
        elif etype == "assistant/chunk":
            chunk = data.get("chunk", {})
            if chunk.get("type") in ("text", "text-delta") and chunk.get("text"):
                messages.append({"role": "assistant", "seq": ev.get("seq"),
                                 "text": _trim(chunk["text"]), "partial": True})
        elif etype.startswith("tool/"):
            messages.append({"role": "tool", "seq": ev.get("seq"), "event": etype,
                             "summary": _trim(json.dumps(data), 300)})
        elif etype == "turn/end":
            turn_end = data.get("reason")
    result: Dict[str, Any] = {"ok": True, "running": running, "messages": messages,
                              "hasMore": value.get("hasMore")}
    if turn_end is not None:
        result["last_turn_end"] = turn_end  # e.g. {"kind":"error","error":{...}} on failure
    title = ((value.get("projections") or {}).get("values") or {}).get("title")
    if title:
        result["title"] = title
    return result


@mcp.tool()
def dsh_cancel(session_id: str) -> Dict[str, Any]:
    """Cancel the running turn in a session."""
    return _rpc("session.cancel", {"sessionId": session_id})


@mcp.tool()
def dsh_workspace_ls(path: Optional[str] = None) -> Dict[str, Any]:
    """List a directory on the harness host (the pod's filesystem when DSH_URL points through a tunnel).
    Omit path for the harness home directory."""
    payload = {"path": path} if path else {}
    result = _rpc("host.listDirectory", payload)
    if not result.get("ok"):
        return result
    v = result["value"]
    return {"ok": True, "path": v.get("path"), "home": v.get("home"),
            "truncated": v.get("truncated"),
            "entries": [{"name": e.get("name"), "path": e.get("path"), "hidden": e.get("hidden")}
                        for e in v.get("entries", [])]}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(dsh_health(), indent=2))
    else:
        mcp.run()
