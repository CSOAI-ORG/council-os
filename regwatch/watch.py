#!/usr/bin/env python3
"""regwatch/watch.py — SHA-256 change-diffing for free official regulation feeds.

Same SHA-256 primitive the attestation core uses (there over a frozen
instrument), here applied to regulation-tracking: fetch a regulation's text,
hash the body, compare against the stored hash in regwatch/state.json.

Three-state, honest by construction:

  NEW        URL never seen before — hash stored, nothing to diff yet
  UNCHANGED  fetched, hash equals the stored hash
  CHANGED    fetched, hash differs from the stored hash (word-level diff shown)
  UNKNOWN    fetch FAILED — we did NOT read the text, so we refuse to claim
             "unchanged". A failed read is never a silent false negative.

The committed run does not hit live endpoints (they may rate-limit and need
polite scheduling). Use --selftest to prove the diff logic offline against
local fixtures. Stdlib only.
"""
import argparse
import datetime
import difflib
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state.json")
UA = "council-os-regwatch/0.1 (+https://council-os; polite low-frequency poll)"

# three-state verdicts
NEW = "NEW"
UNCHANGED = "UNCHANGED"
CHANGED = "CHANGED"
UNKNOWN = "UNKNOWN"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_state(path: str = STATE) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict, path: str = STATE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def word_diff(old: str, new: str, max_lines: int = 40) -> str:
    """Word-level unified-ish diff, so a human sees WHAT moved."""
    old_words = old.split()
    new_words = new.split()
    sm = difflib.SequenceMatcher(a=old_words, b=new_words)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag in ("replace", "delete"):
            out.append("  - " + " ".join(old_words[i1:i2]))
        if tag in ("replace", "insert"):
            out.append("  + " + " ".join(new_words[j1:j2]))
    if not out:
        return "  (hashes differ but no word-level delta rendered)"
    if len(out) > max_lines:
        out = out[:max_lines] + [f"  ... ({len(out) - max_lines} more)"]
    return "\n".join(out)


def fetch(url: str, timeout: int = 20):
    """Return (ok, body_text). ok=False means UNKNOWN — never treat as unchanged."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
        return True, raw.decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        sys.stderr.write(f"fetch failed for {url}: {e}\n")
        return False, ""


def classify(url: str, ok: bool, body: str, state: dict):
    """Return (verdict, diff_text, new_hash_or_None). Pure — does not mutate state."""
    if not ok:
        # We did NOT read the text. Refuse to claim unchanged.
        return UNKNOWN, "", None
    new_hash = sha256(body)
    prev = state.get(url)
    if prev is None:
        return NEW, "", new_hash
    if prev.get("hash") == new_hash:
        return UNCHANGED, "", new_hash
    diff = word_diff(prev.get("last_body", ""), body)
    return CHANGED, diff, new_hash


def run_url(url: str, keep_body: bool = True) -> int:
    state = load_state()
    ok, body = fetch(url)
    verdict, diff, new_hash = classify(url, ok, body, state)
    today = datetime.date.today().isoformat()

    print(f"{verdict}  {url}")
    if verdict == UNKNOWN:
        print("  (fetch failed — state left untouched; NOT reported as unchanged)")
        return 2  # nonzero: an unknown is not a clean result
    if verdict == CHANGED:
        print(diff)

    # store hash (and body, to power the next word-diff) for NEW / UNCHANGED / CHANGED
    entry = {"hash": new_hash, "checked": today}
    if keep_body:
        entry["last_body"] = body
    state[url] = entry
    save_state(state)
    return 0


def selftest() -> int:
    """Prove the three-state diff logic against local fixtures. No network."""
    print("regwatch selftest — SHA-256 three-state diff logic (no network)")
    url = "fixture://reg/example-clause"
    v1 = "The provider shall log all inference requests for 12 months."
    v2 = "The provider shall log all inference requests for 24 months and notify users."

    state = {}
    failures = []

    # 1) NEW: never seen
    verdict, _, h1 = classify(url, True, v1, state)
    ok1 = verdict == NEW and h1 == sha256(v1)
    print(f"  [1] first sight        -> {verdict:9s} (expect NEW)        {'OK' if ok1 else 'FAIL'}")
    if not ok1:
        failures.append("NEW")
    state[url] = {"hash": h1, "last_body": v1, "checked": "fixture"}

    # 2) UNCHANGED: same bytes
    verdict, _, _ = classify(url, True, v1, state)
    ok2 = verdict == UNCHANGED
    print(f"  [2] same bytes         -> {verdict:9s} (expect UNCHANGED)  {'OK' if ok2 else 'FAIL'}")
    if not ok2:
        failures.append("UNCHANGED")

    # 3) CHANGED: different bytes, with a real word-level delta
    verdict, diff, h2 = classify(url, True, v2, state)
    ok3 = verdict == CHANGED and h2 == sha256(v2) and h2 != h1 and diff.strip() != ""
    print(f"  [3] different bytes    -> {verdict:9s} (expect CHANGED)    {'OK' if ok3 else 'FAIL'}")
    if not ok3:
        failures.append("CHANGED")
    else:
        for ln in diff.splitlines():
            print(f"        {ln}")

    # 4) UNKNOWN: fetch failed — must NOT collapse to UNCHANGED
    verdict, _, h4 = classify(url, False, "", state)
    ok4 = verdict == UNKNOWN and h4 is None
    print(f"  [4] fetch failed       -> {verdict:9s} (expect UNKNOWN)    {'OK' if ok4 else 'FAIL'}")
    if not ok4:
        failures.append("UNKNOWN-not-UNCHANGED")

    print()
    if failures:
        print(f"SELFTEST FAIL: {', '.join(failures)}", file=sys.stderr)
        return 1
    print("SELFTEST OK: NEW / UNCHANGED / CHANGED / UNKNOWN all correct; "
          "a failed fetch never reads as unchanged.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="SHA-256 change-diffing for regulation feeds.")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the diff logic offline against fixtures (no network)")
    ap.add_argument("--url", help="fetch this URL and diff against stored hash")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.url:
        return run_url(args.url)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
