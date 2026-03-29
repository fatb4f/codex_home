# JSON Tool Sequence DAG

Machine-readable equivalent:
- `assets/workflow.json`

1. `J0_route`
- Route by `input_kind=external_ds|json_instance`.

2. `J1_extract` (optional)
- Only for unstructured or mixed-source ingress.
- Emit `candidate_envelope`.

3. `J2_unify_validate`
- Constrain if needed.
- Validate accepted JSON against canonical contracts.

4. `J3_derive`
- Use `jq` as the default wrangling engine.
- Emit downstream JSON artifacts.

5. `J5_check` / `J6_authorize` (optional)
- Compute `validation_facts` with CEL-style logic.
- Authorize guarded transitions with OPA/Rego-style policy.

6. `J7_render` (optional)
- Render Markdown or payload outputs after contracts and facts are stable.
