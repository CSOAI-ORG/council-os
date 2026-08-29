See plugin `TUI3-DONE-NEXT.md`. Interop tree lives here so a stranger can rerun without the Grok plugin pin.

```
pip install -r interop/requirements.lock
python interop/emilia-runner/verify_statement_identity.py
python -m unittest interop/emilia-runner/test_offline.py interop/body/test_body.py
```

bindings.json is the monorepo substitute. No Emilia / c2pa-rs / scitt subtree.
