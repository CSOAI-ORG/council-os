# Joined-spec adapters — call their verifier

These wrappers **import or subprocess** the pin in `registry/bindings.json`.
They do not contain Emilia, C2PA, SCITT-CCF, or XRPL protocol source.

```
pip install c2pa-python==0.37.8
pip install opentimestamps-client==0.7.2   # LGPL — do not copy sources here
pip install pyscitt==0.14.2
pip install pycose==1.1.0
pip install xrpl-py==5.1.0
```

Missing pin → exit 2 `UNCHECKABLE`. That is fail-closed, not a pass.

Do not `git subtree add` emilia-protocol, c2pa-rs, or scitt-ccf-ledger.
`python3 ops/reject_vendor_trees.py` must stay green.
