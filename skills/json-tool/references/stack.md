# Stack

Layered contract-first JSON stack:
- canonical contracts: `JSON Schema`
- constraint/unification + interlingua: `CUE`
- wrangling: `jq`, `jaq`
- invariant facts: `CEL`
- authorization: `OPA/Rego`
- rendering: `MiniJinja`
- runtime binding: `Pydantic`

Rules:
- keep `JSON Schema` as canonical accepted-artifact authority
- treat `JSON Schema -> CUE` as the primary interop direction
- use `jq` as the default wrangling engine
- use `CEL` only for deterministic facts over already-shaped objects
