# vfx-shot-manager
A Python learning project focused on VFX pipeline automation, shot management, and render sequence validation.

## Missing-frame check

This early Python prototype checks a sample frame sequence for shot `SH010`.
It expects frames `1001` through `1005` and compares them with the sample list
`[1001, 1002, 1004, 1005]`.

Run from the repository root:

```powershell
python main.py
```

Expected output:

```text
VFX Shot Manager
SH010
1003
```

The current version uses sample numbers. Scanning render folders is a planned next step.
