# Prompt registry overlay note

This directory is shipped as a standalone registry bundle.
The main prompt remains unchanged and is not modified by this overlay.
Workflow units under `prompt-registry/` are retrieval overlays, not the source of truth.
Canonical workflow authority remains under `control/`, and prompt-registry workflow records should declare their `control/` derivation explicitly.
