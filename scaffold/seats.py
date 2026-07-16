"""Validation for the portfolio-wide seats.yaml contract."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

SCHEMA_VERSION = "seats.v1"

OUTPUT_TYPES = {"free_text", "json", "code", "image"}
INPUT_CHARACTERS = {"clean", "messy", "adversarial"}
SUPERVISION_MODES = {"human_in_loop", "unattended"}
REQUIRED_CAPABILITIES = {
    "web_search",
    "tools",
    "json_mode",
    "vision",
    "image_generation",
    "long_context",
}
FAILURE_COST_LEVELS = {"low", "medium", "high", "critical"}
COST_SENSITIVITIES = {"low", "medium", "high"}
LATENCY_TOLERANCES = {"interactive", "standard", "batch"}
PIN_STATUSES = {"LIVE", "FROZEN"}
FIXTURE_FORMATS = {"jsonl", "json", "yaml", "csv"}
SPLIT_METHODS = {"deterministic_hash_modulo"}
CONTEXT_PROVIDER_SOURCES = {"fixture_field", "project_file"}
REVIEW_GATE_TYPES = {"model", "human"}
SEALED_LABEL_POLICIES = {"co_located", "external"}

_SEAT_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_PROJECT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_ENV_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
_MIME_TYPE_RE = re.compile(r"^image/[a-z0-9][a-z0-9.+-]*$")
_ASPECT_RATIO_RE = re.compile(r"^[1-9][0-9]*:[1-9][0-9]*$")


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that treats duplicate mapping keys as malformed input."""


class SeatValidationError(ValueError):
    """Raised when a seats.yaml document fails the v1 contract."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(self._message())

    def _message(self) -> str:
        if len(self.errors) == 1:
            return self.errors[0]
        return "seats.yaml validation failed:\n- " + "\n- ".join(self.errors)


def load_seats_file(path: Path) -> dict[str, Any]:
    """Load a YAML seats file and raise SeatValidationError on parse errors."""
    try:
        data = yaml.load(path.read_text(), Loader=_UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise SeatValidationError([f"{path}: invalid YAML: {exc}"]) from exc

    if data is None:
        raise SeatValidationError([f"{path}: empty seats.yaml document"])
    if not isinstance(data, dict):
        raise SeatValidationError([f"{path}: top-level document must be a mapping"])
    return data


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    seen: set[Any] = set()
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def validate_seats_file(path: Path) -> dict[str, Any]:
    """Load and validate a seats.yaml file for bench consumption."""
    data = load_seats_file(path)
    return validate_seats_data(data)


def validate_seats_data(data: dict[str, Any]) -> dict[str, Any]:
    """Validate a parsed seats.yaml document and return it unchanged on success."""
    errors: list[str] = []

    _validate_unknown_keys(
        errors,
        "root",
        data,
        {"schema_version", "project", "seats"},
    )
    _require_exact(errors, data, "schema_version", SCHEMA_VERSION, "root.schema_version")

    project = _require_mapping(errors, data, "project", "root.project")
    if project:
        _validate_project(errors, project)

    seats = _require_list(errors, data, "seats", "root.seats")
    if seats is not None:
        if not seats:
            errors.append("root.seats: must contain at least one seat")
        _validate_seats(errors, seats)

    if errors:
        raise SeatValidationError(errors)
    return data


def _validate_project(errors: list[str], project: dict[str, Any]) -> None:
    _validate_unknown_keys(
        errors,
        "root.project",
        project,
        {"id", "name", "owner", "seats_file", "notes"},
    )
    project_id = _require_str(errors, project, "id", "root.project.id")
    if project_id and not _PROJECT_ID_RE.match(project_id):
        errors.append(
            "root.project.id: must use lowercase letters, digits, hyphen, or underscore"
        )
    _optional_str(errors, project, "name", "root.project.name")
    _optional_str(errors, project, "owner", "root.project.owner")
    seats_file = _optional_str(errors, project, "seats_file", "root.project.seats_file")
    if seats_file:
        _validate_relative_path(errors, seats_file, "root.project.seats_file")
    _optional_str(errors, project, "notes", "root.project.notes")


def _validate_seats(errors: list[str], seats: list[Any]) -> None:
    seen: set[str] = set()
    for index, seat in enumerate(seats):
        path = f"root.seats[{index}]"
        if not isinstance(seat, dict):
            errors.append(f"{path}: seat must be a mapping")
            continue
        seat_id = _validate_seat(errors, seat, path)
        if not seat_id:
            continue
        if seat_id in seen:
            errors.append(f"{path}.id: duplicate seat id '{seat_id}'")
        seen.add(seat_id)
    for index, seat in enumerate(seats):
        if not isinstance(seat, dict):
            continue
        gates = seat.get("review_gates")
        if not isinstance(gates, list):
            continue
        for gate_index, gate in enumerate(gates):
            if not isinstance(gate, dict) or gate.get("type") != "model":
                continue
            seat_id = gate.get("seat_id")
            if isinstance(seat_id, str) and seat_id not in seen:
                errors.append(
                    f"root.seats[{index}].review_gates[{gate_index}].seat_id: "
                    f"unknown seat id '{seat_id}'"
                )


def _validate_seat(errors: list[str], seat: dict[str, Any], path: str) -> str | None:
    _validate_unknown_keys(
        errors,
        path,
        seat,
        {
            "id",
            "job",
            "output_contract",
            "input_character",
            "supervision",
            "required_capabilities",
            "pipeline_provided_capabilities",
            "review_gates",
            "failure_cost",
            "volume",
            "cost_sensitivity",
            "latency_tolerance",
            "current_pin",
            "eval_fixtures",
            "notes",
        },
    )

    seat_id = _require_str(errors, seat, "id", f"{path}.id")
    if seat_id and not _SEAT_ID_RE.match(seat_id):
        errors.append(
            f"{path}.id: must start with a lowercase letter and use lowercase "
            "letters, digits, or underscores"
        )

    _require_str(errors, seat, "job", f"{path}.job")
    _require_enum(
        errors,
        seat,
        "input_character",
        INPUT_CHARACTERS,
        f"{path}.input_character",
    )
    _require_enum(errors, seat, "supervision", SUPERVISION_MODES, f"{path}.supervision")
    _validate_string_list_enum(
        errors,
        seat,
        "required_capabilities",
        REQUIRED_CAPABILITIES,
        f"{path}.required_capabilities",
    )
    if "pipeline_provided_capabilities" in seat:
        _validate_string_list_enum(
            errors,
            seat,
            "pipeline_provided_capabilities",
            REQUIRED_CAPABILITIES,
            f"{path}.pipeline_provided_capabilities",
        )
        model_capabilities = seat.get("required_capabilities")
        pipeline_capabilities = seat.get("pipeline_provided_capabilities")
        if isinstance(model_capabilities, list) and isinstance(
            pipeline_capabilities, list
        ):
            overlap = sorted(
                value
                for value in set(model_capabilities) & set(pipeline_capabilities)
                if isinstance(value, str)
            )
            if overlap:
                errors.append(
                    f"{path}: model-native and pipeline-provided capabilities "
                    f"overlap: {overlap}"
                )
    if "review_gates" in seat:
        _validate_review_gates(errors, seat, path)
    _require_enum(
        errors,
        seat,
        "cost_sensitivity",
        COST_SENSITIVITIES,
        f"{path}.cost_sensitivity",
    )
    _require_enum(
        errors,
        seat,
        "latency_tolerance",
        LATENCY_TOLERANCES,
        f"{path}.latency_tolerance",
    )
    _optional_str(errors, seat, "notes", f"{path}.notes")

    output_contract = _require_mapping(
        errors, seat, "output_contract", f"{path}.output_contract"
    )
    if output_contract:
        _validate_output_contract(errors, output_contract, f"{path}.output_contract")

    failure_cost = _require_mapping(errors, seat, "failure_cost", f"{path}.failure_cost")
    if failure_cost:
        _validate_failure_cost(errors, failure_cost, f"{path}.failure_cost")

    volume = _require_mapping(errors, seat, "volume", f"{path}.volume")
    if volume:
        _validate_volume(errors, volume, f"{path}.volume")

    current_pin = _require_mapping(errors, seat, "current_pin", f"{path}.current_pin")
    if current_pin:
        _validate_current_pin(errors, current_pin, f"{path}.current_pin")

    eval_fixtures = _require_mapping(
        errors, seat, "eval_fixtures", f"{path}.eval_fixtures"
    )
    if eval_fixtures:
        _validate_eval_fixtures(errors, eval_fixtures, f"{path}.eval_fixtures")

    return seat_id


def _validate_output_contract(
    errors: list[str], output_contract: dict[str, Any], path: str
) -> None:
    _validate_unknown_keys(
        errors,
        path,
        output_contract,
        {"type", "schema_ref", "image", "validation", "notes"},
    )
    contract_type = _require_enum(errors, output_contract, "type", OUTPUT_TYPES, f"{path}.type")
    if contract_type == "json":
        schema_ref = _require_str(errors, output_contract, "schema_ref", f"{path}.schema_ref")
        if schema_ref:
            _validate_relative_path(errors, schema_ref, f"{path}.schema_ref")
    else:
        _optional_str(errors, output_contract, "schema_ref", f"{path}.schema_ref")
    if contract_type == "image":
        image = _require_mapping(errors, output_contract, "image", f"{path}.image")
        if image:
            _validate_image_contract(errors, image, f"{path}.image")
    elif "image" in output_contract:
        errors.append(f"{path}.image: is only valid when type is 'image'")
    _require_str(errors, output_contract, "validation", f"{path}.validation")
    _optional_str(errors, output_contract, "notes", f"{path}.notes")


def _validate_image_contract(
    errors: list[str], image: dict[str, Any], path: str
) -> None:
    _validate_unknown_keys(
        errors,
        path,
        image,
        {
            "allowed_mime_types",
            "min_width_px",
            "min_height_px",
            "max_bytes",
            "allowed_aspect_ratios",
        },
    )
    mime_types = _require_list(
        errors, image, "allowed_mime_types", f"{path}.allowed_mime_types"
    )
    if mime_types is not None:
        _validate_string_values(
            errors,
            mime_types,
            f"{path}.allowed_mime_types",
            pattern=_MIME_TYPE_RE,
            pattern_message="must be a lowercase image MIME type",
        )
    for field in ("min_width_px", "min_height_px", "max_bytes"):
        if field in image:
            _require_positive_int(errors, image, field, f"{path}.{field}")
    if "allowed_aspect_ratios" in image:
        aspect_ratios = _require_list(
            errors,
            image,
            "allowed_aspect_ratios",
            f"{path}.allowed_aspect_ratios",
        )
        if aspect_ratios is not None:
            _validate_string_values(
                errors,
                aspect_ratios,
                f"{path}.allowed_aspect_ratios",
                pattern=_ASPECT_RATIO_RE,
                pattern_message="must use positive integer WIDTH:HEIGHT form",
            )


def _validate_review_gates(
    errors: list[str], seat: dict[str, Any], seat_path: str
) -> None:
    path = f"{seat_path}.review_gates"
    gates = _require_list(errors, seat, "review_gates", path)
    if gates is None:
        return
    if not gates:
        errors.append(f"{path}: must contain at least one gate")
        return
    for index, gate in enumerate(gates):
        gate_path = f"{path}[{index}]"
        if not isinstance(gate, dict):
            errors.append(f"{gate_path}: must be a mapping")
            continue
        _validate_unknown_keys(
            errors, gate_path, gate, {"type", "required", "seat_id", "notes"}
        )
        gate_type = _require_enum(
            errors, gate, "type", REVIEW_GATE_TYPES, f"{gate_path}.type"
        )
        _require_bool(errors, gate, "required", f"{gate_path}.required")
        if gate_type == "model":
            seat_id = _require_str(errors, gate, "seat_id", f"{gate_path}.seat_id")
            if seat_id and not _SEAT_ID_RE.match(seat_id):
                errors.append(f"{gate_path}.seat_id: must be a lowercase seat id")
        elif "seat_id" in gate:
            errors.append(f"{gate_path}.seat_id: is only valid for a model gate")
        _optional_str(errors, gate, "notes", f"{gate_path}.notes")


def _validate_failure_cost(
    errors: list[str], failure_cost: dict[str, Any], path: str
) -> None:
    _validate_unknown_keys(errors, path, failure_cost, {"level", "description"})
    _require_enum(errors, failure_cost, "level", FAILURE_COST_LEVELS, f"{path}.level")
    _require_str(errors, failure_cost, "description", f"{path}.description")


def _validate_volume(errors: list[str], volume: dict[str, Any], path: str) -> None:
    _validate_unknown_keys(errors, path, volume, {"expected", "unit", "burst", "notes"})
    _require_positive_number(errors, volume, "expected", f"{path}.expected")
    _require_str(errors, volume, "unit", f"{path}.unit")
    if "burst" in volume:
        _require_positive_number(errors, volume, "burst", f"{path}.burst")
    _optional_str(errors, volume, "notes", f"{path}.notes")


def _validate_current_pin(
    errors: list[str], current_pin: dict[str, Any], path: str
) -> None:
    _validate_unknown_keys(
        errors,
        path,
        current_pin,
        {"provider", "model", "status", "reason", "parameters", "notes"},
    )
    _require_str(errors, current_pin, "provider", f"{path}.provider")
    _require_str(errors, current_pin, "model", f"{path}.model")
    _require_enum(errors, current_pin, "status", PIN_STATUSES, f"{path}.status")
    _require_str(errors, current_pin, "reason", f"{path}.reason")
    if "parameters" in current_pin and not isinstance(current_pin["parameters"], dict):
        errors.append(f"{path}.parameters: must be a mapping when present")
    _optional_str(errors, current_pin, "notes", f"{path}.notes")


def _validate_eval_fixtures(
    errors: list[str], eval_fixtures: dict[str, Any], path: str
) -> None:
    _validate_unknown_keys(
        errors,
        path,
        eval_fixtures,
        {
            "path",
            "format",
            "id_field",
            "input_field",
            "expected_output_field",
            "context_providers",
            "sealed_labels",
            "split",
            "notes",
        },
    )
    fixture_path = _require_str(errors, eval_fixtures, "path", f"{path}.path")
    if fixture_path:
        _validate_relative_path(errors, fixture_path, f"{path}.path")
    _require_enum(errors, eval_fixtures, "format", FIXTURE_FORMATS, f"{path}.format")
    _require_str(errors, eval_fixtures, "id_field", f"{path}.id_field")
    _require_str(errors, eval_fixtures, "input_field", f"{path}.input_field")
    _require_str(
        errors,
        eval_fixtures,
        "expected_output_field",
        f"{path}.expected_output_field",
    )
    _optional_str(errors, eval_fixtures, "notes", f"{path}.notes")
    if "context_providers" in eval_fixtures:
        _validate_context_providers(errors, eval_fixtures, path)
    if "sealed_labels" in eval_fixtures:
        sealed_labels = _require_mapping(
            errors, eval_fixtures, "sealed_labels", f"{path}.sealed_labels"
        )
        if sealed_labels:
            _validate_sealed_labels(errors, sealed_labels, f"{path}.sealed_labels")
    split = _require_mapping(errors, eval_fixtures, "split", f"{path}.split")
    if split:
        _validate_split(errors, split, f"{path}.split")


def _validate_context_providers(
    errors: list[str], eval_fixtures: dict[str, Any], fixture_path: str
) -> None:
    path = f"{fixture_path}.context_providers"
    providers = _require_list(errors, eval_fixtures, "context_providers", path)
    if providers is None:
        return
    if not providers:
        errors.append(f"{path}: must contain at least one provider")
        return
    seen: set[str] = set()
    for index, provider in enumerate(providers):
        provider_path = f"{path}[{index}]"
        if not isinstance(provider, dict):
            errors.append(f"{provider_path}: must be a mapping")
            continue
        _validate_unknown_keys(
            errors,
            provider_path,
            provider,
            {"id", "source", "source_ref", "required", "notes"},
        )
        provider_id = _require_str(errors, provider, "id", f"{provider_path}.id")
        if provider_id:
            if not _SEAT_ID_RE.match(provider_id):
                errors.append(f"{provider_path}.id: must be a lowercase identifier")
            if provider_id in seen:
                errors.append(
                    f"{provider_path}.id: duplicate context provider id '{provider_id}'"
                )
            seen.add(provider_id)
        source = _require_enum(
            errors,
            provider,
            "source",
            CONTEXT_PROVIDER_SOURCES,
            f"{provider_path}.source",
        )
        source_ref = _require_str(
            errors, provider, "source_ref", f"{provider_path}.source_ref"
        )
        if source == "project_file" and source_ref:
            _validate_relative_path(errors, source_ref, f"{provider_path}.source_ref")
        _require_bool(errors, provider, "required", f"{provider_path}.required")
        _optional_str(errors, provider, "notes", f"{provider_path}.notes")


def _validate_sealed_labels(
    errors: list[str], sealed_labels: dict[str, Any], path: str
) -> None:
    _validate_unknown_keys(errors, path, sealed_labels, {"policy", "path", "notes"})
    policy = _require_enum(
        errors, sealed_labels, "policy", SEALED_LABEL_POLICIES, f"{path}.policy"
    )
    if policy == "external":
        labels_path = _require_str(errors, sealed_labels, "path", f"{path}.path")
        if labels_path:
            _validate_relative_path(errors, labels_path, f"{path}.path")
    elif "path" in sealed_labels:
        errors.append(f"{path}.path: is only valid when policy is 'external'")
    _optional_str(errors, sealed_labels, "notes", f"{path}.notes")


def _validate_split(errors: list[str], split: dict[str, Any], path: str) -> None:
    _validate_unknown_keys(
        errors,
        path,
        split,
        {
            "method",
            "hash_field",
            "modulo",
            "dev_remainders",
            "sealed_remainders",
            "sealed_unseal_env",
            "notes",
        },
    )
    _require_enum(errors, split, "method", SPLIT_METHODS, f"{path}.method")
    _require_str(errors, split, "hash_field", f"{path}.hash_field")
    modulo = _require_int(errors, split, "modulo", f"{path}.modulo")
    if modulo is not None and modulo < 2:
        errors.append(f"{path}.modulo: must be at least 2")
    dev_remainders = _require_int_list(errors, split, "dev_remainders", f"{path}.dev_remainders")
    sealed_remainders = _require_int_list(
        errors, split, "sealed_remainders", f"{path}.sealed_remainders"
    )
    if modulo is not None:
        _validate_remainders(errors, dev_remainders, modulo, f"{path}.dev_remainders")
        _validate_remainders(
            errors, sealed_remainders, modulo, f"{path}.sealed_remainders"
        )
    if dev_remainders is not None and sealed_remainders is not None:
        overlap = sorted(set(dev_remainders) & set(sealed_remainders))
        if overlap:
            errors.append(f"{path}: dev and sealed remainders overlap: {overlap}")
        if modulo is not None:
            expected = set(range(modulo))
            actual = set(dev_remainders) | set(sealed_remainders)
            missing = sorted(expected - actual)
            if missing:
                errors.append(
                    f"{path}: dev and sealed remainders must cover every "
                    f"remainder from 0 to {modulo - 1}; missing {missing}"
                )
    unseal_env = _require_str(errors, split, "sealed_unseal_env", f"{path}.sealed_unseal_env")
    if unseal_env and not _ENV_RE.match(unseal_env):
        errors.append(
            f"{path}.sealed_unseal_env: must be an uppercase environment variable name"
        )
    _optional_str(errors, split, "notes", f"{path}.notes")


def _validate_unknown_keys(
    errors: list[str], path: str, value: dict[str, Any], allowed: set[str]
) -> None:
    for key in value:
        if key not in allowed:
            errors.append(f"{path}.{key}: unknown field")


def _require_exact(
    errors: list[str], data: dict[str, Any], key: str, expected: str, path: str
) -> None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return
    if data[key] != expected:
        errors.append(f"{path}: must be '{expected}'")


def _require_mapping(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> dict[str, Any] | None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return None
    value = data[key]
    if not isinstance(value, dict):
        errors.append(f"{path}: must be a mapping")
        return None
    return value


def _require_list(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> list[Any] | None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return None
    value = data[key]
    if not isinstance(value, list):
        errors.append(f"{path}: must be a list")
        return None
    return value


def _require_str(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> str | None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return None
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")
        return None
    return value


def _optional_str(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> str | None:
    if key not in data:
        return None
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string when present")
        return None
    return value


def _require_enum(
    errors: list[str], data: dict[str, Any], key: str, allowed: set[str], path: str
) -> str | None:
    value = _require_str(errors, data, key, path)
    if value is None:
        return None
    if value not in allowed:
        errors.append(f"{path}: must be one of {sorted(allowed)}")
        return None
    return value


def _validate_string_list_enum(
    errors: list[str],
    data: dict[str, Any],
    key: str,
    allowed: set[str],
    path: str,
) -> None:
    values = _require_list(errors, data, key, path)
    if values is None:
        return
    if not values:
        errors.append(f"{path}: must contain at least one value")
        return
    seen: set[str] = set()
    for index, value in enumerate(values):
        item_path = f"{path}[{index}]"
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{item_path}: must be a non-empty string")
            continue
        if value not in allowed:
            errors.append(f"{item_path}: must be one of {sorted(allowed)}")
        if value in seen:
            errors.append(f"{item_path}: duplicate value '{value}'")
        seen.add(value)


def _require_positive_number(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> float | int | None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return None
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{path}: must be a positive number")
        return None
    if value <= 0:
        errors.append(f"{path}: must be greater than zero")
        return None
    return value


def _require_positive_int(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> int | None:
    value = _require_int(errors, data, key, path)
    if value is not None and value <= 0:
        errors.append(f"{path}: must be greater than zero")
        return None
    return value


def _require_bool(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> bool | None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return None
    value = data[key]
    if not isinstance(value, bool):
        errors.append(f"{path}: must be a boolean")
        return None
    return value


def _require_int(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> int | None:
    if key not in data:
        errors.append(f"{path}: missing required field")
        return None
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{path}: must be an integer")
        return None
    return value


def _require_int_list(
    errors: list[str], data: dict[str, Any], key: str, path: str
) -> list[int] | None:
    values = _require_list(errors, data, key, path)
    if values is None:
        return None
    if not values:
        errors.append(f"{path}: must contain at least one remainder")
        return None
    result: list[int] = []
    seen: set[int] = set()
    for index, value in enumerate(values):
        item_path = f"{path}[{index}]"
        if isinstance(value, bool) or not isinstance(value, int):
            errors.append(f"{item_path}: must be an integer")
            continue
        if value in seen:
            errors.append(f"{item_path}: duplicate remainder {value}")
        seen.add(value)
        result.append(value)
    return result


def _validate_string_values(
    errors: list[str],
    values: list[Any],
    path: str,
    *,
    pattern: re.Pattern[str],
    pattern_message: str,
) -> None:
    if not values:
        errors.append(f"{path}: must contain at least one value")
        return
    seen: set[str] = set()
    for index, value in enumerate(values):
        item_path = f"{path}[{index}]"
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{item_path}: must be a non-empty string")
            continue
        if not pattern.match(value):
            errors.append(f"{item_path}: {pattern_message}")
        if value in seen:
            errors.append(f"{item_path}: duplicate value '{value}'")
        seen.add(value)


def _validate_remainders(
    errors: list[str], remainders: list[int] | None, modulo: int, path: str
) -> None:
    if remainders is None:
        return
    for value in remainders:
        if value < 0 or value >= modulo:
            errors.append(f"{path}: remainder {value} must be between 0 and {modulo - 1}")


def _validate_relative_path(errors: list[str], value: str, path: str) -> None:
    candidate = Path(value)
    if candidate.is_absolute():
        errors.append(f"{path}: must be a project-relative path")
    if ".." in candidate.parts:
        errors.append(f"{path}: must not contain parent-directory segments")
