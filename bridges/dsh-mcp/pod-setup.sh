#!/usr/bin/env bash
# pod-setup.sh — idempotent DSH bootstrap for a RunPod (or any Linux) pod.
#
# Run ON the pod (e.g.: ssh -p <port> root@<host> 'bash -s' < pod-setup.sh).
# Installs node if missing, installs @deepseek-ai/dsh globally, and starts
# `dsh web` bound to 127.0.0.1:3080 under nohup with a logfile.
#
# SECURITY (non-negotiable): DSH binds 127.0.0.1 ONLY. Its web API has no
# request auth — the SSH tunnel IS the auth boundary. Never bind 0.0.0.0.
set -euo pipefail

DSH_PORT="${DSH_PORT:-3080}"
DSH_LOG="${DSH_LOG:-/root/dsh-web.log}"
DSH_PIDFILE="${DSH_PIDFILE:-/root/dsh-web.pid}"

echo "== dsh pod setup (port ${DSH_PORT}, 127.0.0.1 only) =="

# 1. node (>=20)
if ! command -v node >/dev/null 2>&1; then
  echo "-- installing node 22 (NodeSource)"
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi
echo "-- node $(node --version)"

# 2. dsh
if ! command -v dsh >/dev/null 2>&1; then
  echo "-- npm i -g @deepseek-ai/dsh"
  npm install -g @deepseek-ai/dsh
fi
echo "-- dsh $(dsh --version)"

# 3. already running and healthy? leave it alone (idempotent)
if [ -f "${DSH_PIDFILE}" ] && kill -0 "$(cat "${DSH_PIDFILE}")" 2>/dev/null; then
  if curl -sf -m 5 -X POST "http://127.0.0.1:${DSH_PORT}/api/host.describe" \
      -H 'content-type: application/json' \
      -d '{"type":"client-request","rpcId":"00000000-0000-4000-8000-000000000000","method":"host.describe","payload":{}}' \
      >/dev/null; then
    echo "-- dsh already running (pid $(cat "${DSH_PIDFILE}")) and healthy; nothing to do"
    exit 0
  fi
  echo "-- stale pid; restarting"
  kill "$(cat "${DSH_PIDFILE}")" 2>/dev/null || true
  sleep 2
fi

# 4. start under nohup, loopback only
echo "-- starting: dsh web --host 127.0.0.1 --port ${DSH_PORT}"
nohup dsh web --host 127.0.0.1 --port "${DSH_PORT}" >>"${DSH_LOG}" 2>&1 &
echo $! > "${DSH_PIDFILE}"
sleep 5

# 5. verify
if curl -sf -m 10 -X POST "http://127.0.0.1:${DSH_PORT}/api/host.describe" \
    -H 'content-type: application/json' \
    -d '{"type":"client-request","rpcId":"00000000-0000-4000-8000-000000000001","method":"host.describe","payload":{}}'; then
  echo
  echo "== dsh up on 127.0.0.1:${DSH_PORT} (pid $(cat "${DSH_PIDFILE}"), log ${DSH_LOG}) =="
else
  echo "!! dsh did not come up; tail of ${DSH_LOG}:"
  tail -30 "${DSH_LOG}"
  exit 1
fi
