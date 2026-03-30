# codex_home

Shared Codex control surface extracted from `dotfiles`.

Ownership boundary:
- canonical tracked tree in `dotfiles` is `chezmoi/dot_config/codex`
- `dotfiles/config/codex` is a convenience mirror path and should resolve back to the `chezmoi` path
- this repo is the extracted source of truth that those paths symlink to

Scope:
- skills
- control workflows
- shared control policy
- prompt registry
- schemas
- Codex-facing policy and orchestration assets

Out of scope:
- machine-local runtime state under `~/.config/codex`
- caches
- auth
- logs
- session/state databases

Migration note:
- the extracted tree was rooted from the tracked Codex config and preserves newer resolved changes that had drifted between the old mirrored paths
