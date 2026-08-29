# emilia-runner — independent cell

Apache-2.0. Reads **only** `vectors.reference.json` at pin
`emiliaprotocol/emilia-protocol@e507acdf`. No Emilia imports. No card keys.

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python verify_statement_identity.py
.venv/bin/python -m unittest test_offline.py
```

EP authorization is UNCHECKABLE (bytes not in this JSON). Not a GSPC card.
Do not track `emilia-protocol` `main`. No PR to their repo unless they ask.
