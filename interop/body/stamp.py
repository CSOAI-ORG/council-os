#!/usr/bin/env python3
"""Body stamp rule: RFC 8785 JCS of {schema, preimage_rule, card_id, attachments}.

Named: csoai.instrument-body/0.1. body_id = sha256(JCS). Not card-v1.
Unsigned v0 is fine; missing preimage_rule is rejected.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any


def utf16_sort_key(s: str) -> bytes:
    return s.encode("utf-16-be")


def es6_number_to_string(n: float) -> str:
    if not math.isfinite(n):
        raise ValueError("NaN/Infinity")
    if n == 0:
        return "0"
    if abs(n) < 1e21 and n == math.trunc(n):
        return str(int(n))
    s = json.dumps(n)
    return re.sub(r"e([+-])0+(\d)", r"e\1\2", s)


def jcs(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value) if abs(value) < 1e21 else es6_number_to_string(float(value))
    if isinstance(value, float):
        return es6_number_to_string(value)
    if isinstance(value, list):
        return "[" + ",".join(jcs(v) for v in value) + "]"
    if isinstance(value, dict):
        keys = sorted((str(k) for k in value.keys()), key=utf16_sort_key)
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + jcs(value[k]) for k in keys) + "}"
    raise TypeError(type(value))


STAMP_KEYS = ("schema", "preimage_rule", "card_id", "attachments")


def stamp(body: dict) -> dict:
    if "preimage_rule" not in body:
        raise ValueError("REJECTED: missing preimage_rule")
    if body.get("schema") != "csoai.instrument-body/0.1":
        raise ValueError("REJECTED: unknown schema")
    subset = {k: body[k] for k in STAMP_KEYS if k in body}
    preimage = jcs(subset).encode("utf-8")
    out = dict(body)
    out["body_id"] = hashlib.sha256(preimage).hexdigest()
    return out
