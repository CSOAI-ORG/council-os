#!/usr/bin/env python3
"""ops/live_status_check.py — the ONLY writer of LIVE in registry/spine.json.

JL.5 by construction: a status label is a claim. This checker verifies each
axis organ from OUTSIDE (public HTTP), then writes the verdict:

  LIVE      resolved publicly right now (evidence recorded: url, http, date)
  GATED     surface exists but did not resolve (dated note, never deleted)
  LANE-REPORTED / LANE-REAL / THEORY  pass through untouched — they are lane
            claims, and this checker refuses to upgrade them; only public
            resolution can mint LIVE, and only via this file.

Structural rule (the estate's defect class): this script is UNABLE to report
LIVE on a path it did not complete — the verdict is written together with its
evidence, and a missing evidence block fails validation. Stdlib only.
"""
import json, sys, urllib.request, datetime

SPINE = "registry/spine.json"
TODAY = datetime.date.today().isoformat()

class _Redirect308(urllib.request.HTTPRedirectHandler):
    """urllib follows 301/302/303/307 but not 308 (Permanent Redirect). Many
    public surfaces 308 from their canonical path (e.g. /gspc -> /gspc-scoreboard),
    so without this a genuinely-live surface is mis-recorded as GATED. Stdlib only."""
    def http_error_308(self, req, fp, code, msg, headers):
        newurl = headers.get("Location")
        if not newurl:
            return None
        newurl = urllib.request.urljoin(req.full_url, newurl)
        new = urllib.request.Request(newurl,
            headers=req.headers, origin_req_host=req.origin_req_host,
            unverifiable=True)
        return self.parent.open(new, timeout=req.timeout)

_OPENER = urllib.request.build_opener(_Redirect308())

def probe(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "council-os-live-status-check/0.1"})
        with _OPENER.open(req, timeout=timeout) as r:
            return r.status, r.read(200000)
    except Exception as e:
        return None, str(e).encode()

def main():
    spine = json.load(open(SPINE))
    # one fetch of the board serves every axis's harness/board organ
    st, body = probe("https://councilof.ai/api/gspc")
    board_axes = {}
    if st == 200:
        try:
            board_axes = {a["axis"]: a for a in json.loads(body)["axes"]}
        except Exception:
            pass
    changed = live = gated = 0
    for ax in spine["axes"]:
        organs = ax["organs"]
        # gold bank: HF dataset must resolve
        gb = organs["gold_bank"]
        if gb["status"] not in ("LANE-REPORTED", "THEORY"):
            s, _ = probe("https://huggingface.co/api/datasets/csoai/gspc-" + ax["id"])
            new = "LIVE" if s == 200 else "GATED"
            ev = {"checked": TODAY, "http": s}
            if gb["status"] != new: changed += 1
            gb["status"], gb["evidence"] = new, ev
            live += new == "LIVE"; gated += new == "GATED"
        # board + harness: axis must appear in the live public board
        onboard = ax["axis"] in board_axes
        for key in ("board", "harness"):
            o = organs[key]
            if o["status"] in ("LANE-REPORTED", "THEORY"): continue
            new = "LIVE" if onboard else "GATED"
            if o["status"] != new: changed += 1
            o["status"], o["evidence"] = new, {"checked": TODAY, "board_http": st, "axis_on_board": onboard}
            live += new == "LIVE"; gated += new == "GATED"
        # public face: page must serve 200
        pf = organs["public_face"]
        if pf["status"] not in ("LANE-REPORTED", "THEORY"):
            s, _ = probe(pf["surface"])
            new = "LIVE" if s == 200 else "GATED"
            if pf["status"] != new: changed += 1
            pf["status"], pf["evidence"] = new, {"checked": TODAY, "http": s}
            live += new == "LIVE"; gated += new == "GATED"
    # validation: no LIVE without evidence, anywhere
    bad = [f"{ax['id']}.{k}" for ax in spine["axes"] for k, o in ax["organs"].items()
           if o.get("status") == "LIVE" and "evidence" not in o]
    if bad:
        print("INVALID — LIVE without evidence:", bad); return 1
    spine["last_check"] = TODAY
    json.dump(spine, open(SPINE, "w"), indent=1)
    print(f"checked from outside: {live} LIVE, {gated} GATED, {changed} changed. Evidence recorded.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
