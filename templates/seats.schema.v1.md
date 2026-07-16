# seats.yaml Schema v1

`seats.yaml` is the portfolio-wide contract for describing model seats. A
project owns its own seats because only the project knows the real work, real
fixtures, and real failure modes. Benches consume this file; they do not invent
it and they do not act as the registry.

This document defines the form only. It does not assign a project to any model
and it does not change any model pin.

## Version And Location

- File location: repository root, named `seats.yaml`.
- Schema version: `seats.v1`.
- Validator: `scaffold seats validate path/to/seats.yaml`.
- Python API: `scaffold.seats.validate_seats_file(Path("seats.yaml"))`.

Benches must validate before loading. Validation failure is a hard error. A
malformed `seats.yaml` must never be silently skipped.

## Top-Level Shape

```yaml
schema_version: seats.v1
project:
  id: example-project
  name: Example Project
  seats_file: seats.yaml
seats:
  - id: example_seat
    job: One-line job description.
    output_contract: ...
    input_character: messy
    supervision: human_in_loop
    required_capabilities: [json_mode]
    pipeline_provided_capabilities: [tools]
    review_gates: ...
    failure_cost: ...
    volume: ...
    cost_sensitivity: medium
    latency_tolerance: batch
    current_pin: ...
    eval_fixtures: ...
```

Unknown fields and duplicate YAML mapping keys are invalid in v1. Additions
require a schema version bump or an explicit validator change.

## Project Fields

Required:

- `id`: lowercase project identifier. Allowed characters: `a-z`, `0-9`, `_`, `-`.

Optional:

- `name`: display name.
- `owner`: owning person, bench, or team.
- `seats_file`: project-relative path. Expected value is `seats.yaml`.
- `notes`: free text for project-level context.

## Seat Fields

Required for every entry in `seats`:

- `id`: stable unique seat id within the project. Lowercase snake case only.
- `job`: one line describing what the model is asked to do.
- `output_contract`: how output validity is checked.
- `input_character`: one of `clean`, `messy`, `adversarial`.
- `supervision`: one of `human_in_loop`, `unattended`.
- `required_capabilities`: non-empty list from the allowed capability set.
- `failure_cost`: what breaks if this seat is wrong.
- `volume`: expected workload.
- `cost_sensitivity`: one of `low`, `medium`, `high`.
- `latency_tolerance`: one of `interactive`, `standard`, `batch`.
- `current_pin`: model currently in the chair.
- `eval_fixtures`: real sample inputs plus sealed holdout discipline.

Optional:

- `pipeline_provided_capabilities`: non-empty list from the allowed capability
  set. Use this for capabilities supplied by orchestration around the model,
  rather than by the model itself. It must not overlap
  `required_capabilities`.
- `review_gates`: non-empty list of model or human approvals that run after
  this seat. See Review Gates below.
- `notes`: seat-level context for humans and bench reports.

## Output Contract

```yaml
output_contract:
  type: json
  schema_ref: schemas/claim-extraction.schema.json
  validation: Validate every response against the schema before scoring.
```

Fields:

- `type`: `free_text`, `json`, `code`, or `image`.
- `schema_ref`: required when `type` is `json`; must be project-relative.
- `image`: required only when `type` is `image`. See Image Output Contract
  below.
- `validation`: required for all output types. If the output is
  machine-checkable, this says how the bench gates validity before scoring.
- `notes`: optional.

Validity comes before quality. A bench should reject or separately score an
invalid output before asking any model judge whether it is good.

### Image Output Contract

```yaml
output_contract:
  type: image
  image:
    allowed_mime_types: [image/png, image/webp]
    min_width_px: 1024
    min_height_px: 1024
    max_bytes: 10485760
    allowed_aspect_ratios: ["1:1", "16:9"]
  validation: Decode the artifact and enforce the declared image constraints.
```

`image.allowed_mime_types` is required, non-empty, and contains unique
lowercase `image/*` MIME types. The remaining image fields are optional:

- `min_width_px` and `min_height_px`: positive integer minimum dimensions.
- `max_bytes`: positive integer artifact-size limit.
- `allowed_aspect_ratios`: non-empty list of unique positive integer
  `WIDTH:HEIGHT` values.

The bench must validate the artifact itself; a model claim about its format or
dimensions is not sufficient.

## Input Character

- `clean`: well-formed, normalized input.
- `messy`: real-world inputs with missing fields, boilerplate, ambiguity, or
  inconsistent formatting.
- `adversarial`: inputs intentionally designed to confuse, jailbreak, spoof, or
  trigger false positives.

## Supervision

- `human_in_loop`: a human reviews or accepts the model output before it changes
  product state.
- `unattended`: the model output can change product state, user-visible output,
  spend, or downstream data without immediate human approval.

Auxesis-style `human_loop_only: true` maps to `supervision: human_in_loop`.
`human_loop_only: false` maps to `supervision: unattended`.

## Required Capabilities

Allowed values:

- `web_search`
- `tools`
- `json_mode`
- `vision`
- `image_generation`
- `long_context`

Auxesis-style `required_capability` maps to the v1 list field
`required_capabilities`.

`required_capabilities` means capabilities the model must provide natively.
`pipeline_provided_capabilities` uses the same allowed values for capabilities
provided by tools or orchestration. A capability cannot appear in both lists;
this distinction prevents a bench from rejecting an otherwise valid model for
a capability the pipeline already supplies.

## Review Gates

```yaml
review_gates:
  - type: model
    seat_id: expert_review
    required: true
  - type: human
    required: true
    notes: An editor approves publication.
```

Each gate has:

- `type`: `model` or `human`.
- `required`: boolean indicating whether the gate must pass.
- `seat_id`: required for a model gate and forbidden for a human gate. It must
  identify a declared seat in the same document.
- `notes`: optional operational context.

The list must contain at least one gate when present. Gates describe downstream
approval; they do not replace the seat's `supervision` declaration.

## Failure Cost

```yaml
failure_cost:
  level: high
  description: Bad output pollutes the review queue and can publish a false finding.
```

`level` is one of `low`, `medium`, `high`, `critical`.

The description should be specific enough for a bench to decide whether a cheap
or weak model is allowed near the seat.

## Volume, Cost, And Latency

```yaml
volume:
  expected: 20
  unit: items_per_run
  burst: 100
cost_sensitivity: high
latency_tolerance: batch
```

- `volume.expected`: positive number.
- `volume.unit`: human-readable unit, such as `items_per_run`, `calls_per_day`,
  or `reviews_per_week`.
- `volume.burst`: optional positive number.
- `cost_sensitivity`: `low`, `medium`, or `high`.
- `latency_tolerance`: `interactive`, `standard`, or `batch`.

## Current Pin

```yaml
current_pin:
  provider: openai
  model: gpt-4o-2024-08-06
  status: FROZEN
  reason: Verbatim upstream judge prompts must remain comparable with the paper.
  parameters:
    temperature: 0
```

Fields:

- `provider`: provider or runtime owner.
- `model`: exact model id used today.
- `status`: `LIVE` or `FROZEN`.
- `reason`: required for every pin. It is load-bearing for `FROZEN`.
- `parameters`: optional mapping of relevant call parameters.
- `notes`: optional.

Bench behavior:

- `LIVE`: benches may score alternatives and recommend a replacement.
- `FROZEN`: benches may report baseline cost and score, but must not recommend
  a replacement, rewrite the pin, or include the seat in optimization sweeps
  unless the bench has an explicit operator override for frozen seats.
- Both the MacBook model-bench and the Auxesis Mac Mini bench must honor this
  rule the same way.

The motivating case is ai-memory: its benchmark judge is frozen to
`gpt-4o-2024-08-06` with upstream prompts for comparability, and its benchmark
answerer is frozen to the deployed answerer model so reported scores reflect
the real product.

## Eval Fixtures

```yaml
eval_fixtures:
  path: benchmarks/seats/example.jsonl
  format: jsonl
  id_field: fixture_id
  input_field: input
  expected_output_field: expected_output
  context_providers:
    - id: policy_context
      source: project_file
      source_ref: benchmarks/context/policy.md
      required: true
  sealed_labels:
    policy: external
    path: benchmarks/seats/example.labels.jsonl
  split:
    method: deterministic_hash_modulo
    hash_field: fixture_id
    modulo: 5
    dev_remainders: [1, 2, 3, 4]
    sealed_remainders: [0]
    sealed_unseal_env: MODEL_BENCH_UNSEAL
```

Fields:

- `path`: project-relative path to real fixture inputs.
- `format`: `jsonl`, `json`, `yaml`, or `csv`.
- `id_field`: stable fixture id field.
- `input_field`: field containing the model input.
- `expected_output_field`: field containing the expected output, rubric label,
  or gold metadata.
- `context_providers`: optional non-empty list describing context supplied to
  every evaluated case. See Context Providers below.
- `sealed_labels`: optional declaration of whether gold labels are co-located
  with fixture inputs or stored separately. See Sealed Labels below.
- `split`: deterministic dev/sealed partition.

### Context Providers

Each provider has:

- `id`: unique lowercase identifier within the seat's provider list.
- `source`: `fixture_field` or `project_file`.
- `source_ref`: a fixture field name for `fixture_field`, or a project-relative
  path without parent-directory segments for `project_file`.
- `required`: boolean indicating whether a runner must fail when the context is
  unavailable.
- `notes`: optional.

Context providers make retrieval and prompt assembly explicit without turning
those inputs into model-native capability requirements.

### Sealed Labels

`sealed_labels.policy` is either:

- `co_located`: labels remain in the fixture rows. `path` is forbidden.
- `external`: labels live in a separate project-relative file, and `path` is
  required.

`notes` is optional for either policy. This declaration records label storage;
the split and `sealed_unseal_env` still control whether a runner may access
sealed cases and their labels.

For backward compatibility, omitting `sealed_labels` means the legacy
`co_located` behavior: labels may be committed beside inputs and are isolated
only by the explicit unseal process. That process gate prevents accidental
evaluation access; it does not make committed labels secret.

Split behavior:

- v1 supports `deterministic_hash_modulo`.
- Benches compute `sha256(str(hash_field_value).encode("utf-8")).digest()[0] %
  modulo`.
- A fixture is dev when the result is in `dev_remainders`.
- A fixture is sealed when the result is in `sealed_remainders`.
- `dev_remainders` and `sealed_remainders` must be non-empty and disjoint.
- Together, `dev_remainders` and `sealed_remainders` must cover every remainder
  from `0` through `modulo - 1`; no fixture may fall outside both splits.
- A runner must refuse to touch sealed fixtures unless
  `sealed_unseal_env=1` is present in the environment.

This copies ai-memory's contamination discipline: development and prompt tuning
use only `dev`; publication or final comparison numbers use a deliberate,
explicitly unsealed `sealed` run.

## Real-Case Pressure Notes

The v1 shape intentionally covers:

- Auxesis-style staffing tables and registries: `required_capability` becomes
  `required_capabilities`, and `human_loop_only` becomes `supervision`.
- hypocrisynow's three seats:
  - `extraction`: messy article text to claim JSON.
  - `detection`: claim pairs plus context to structured contradiction or
    asymmetry classification.
  - `expert_review`: editorial publish/reject JSON with high failure cost.
- ai-memory's frozen benchmark seats, including required frozen-pin reasons and
  sealed holdout fixtures.
