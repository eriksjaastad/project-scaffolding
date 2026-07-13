from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from scaffold.cli import cli
from scaffold.seats import (
    SCHEMA_VERSION,
    SeatValidationError,
    validate_seats_data,
    validate_seats_file,
)


def _split() -> dict[str, Any]:
    return {
        "method": "deterministic_hash_modulo",
        "hash_field": "fixture_id",
        "modulo": 5,
        "dev_remainders": [1, 2, 3, 4],
        "sealed_remainders": [0],
        "sealed_unseal_env": "MODEL_BENCH_UNSEAL",
    }


def _seat(seat_id: str, **overrides: Any) -> dict[str, Any]:
    seat = {
        "id": seat_id,
        "job": "Perform a bounded project job.",
        "output_contract": {
            "type": "json",
            "schema_ref": f"schemas/{seat_id}.schema.json",
            "validation": "Validate response JSON against schema_ref before scoring.",
        },
        "input_character": "messy",
        "supervision": "human_in_loop",
        "required_capabilities": ["json_mode"],
        "failure_cost": {
            "level": "medium",
            "description": "Bad output wastes review time and can pollute downstream data.",
        },
        "volume": {
            "expected": 20,
            "unit": "items_per_run",
        },
        "cost_sensitivity": "medium",
        "latency_tolerance": "batch",
        "current_pin": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "status": "LIVE",
            "reason": "Current production chair; safe to benchmark alternatives.",
        },
        "eval_fixtures": {
            "path": f"benchmarks/seats/{seat_id}.jsonl",
            "format": "jsonl",
            "id_field": "fixture_id",
            "input_field": "input",
            "expected_output_field": "expected_output",
            "split": _split(),
        },
    }
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(seat.get(key), dict):
            seat[key].update(value)
        else:
            seat[key] = value
    return seat


def _document(seats: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "id": "pressure-test",
            "name": "Pressure Test",
            "seats_file": "seats.yaml",
        },
        "seats": seats,
    }


def test_reference_template_validates() -> None:
    project_root = Path(__file__).parent.parent
    template = project_root / "templates" / "seats.yaml.template"

    document = validate_seats_file(template)

    assert document["schema_version"] == SCHEMA_VERSION
    assert [seat["id"] for seat in document["seats"]] == [
        "example_json_worker",
        "example_frozen_judge",
    ]


def test_auxesis_registry_shape_pressure_case() -> None:
    """Auxesis-style registry fields map cleanly into seats.v1."""
    registry_rows: list[dict[str, Any]] = [
        {
            "id": "venture_researcher",
            "job": "Research a niche and produce evidence-backed venture findings.",
            "required_capability": "web_search",
            "human_loop_only": True,
            "provider": "anthropic",
            "model": "claude-opus-4-8",
            "role_fit": ["planner", "architect"],
        },
        {
            "id": "seed_manifest_writer",
            "job": "Convert approved research into an Auxesis import manifest.",
            "required_capability": "json_mode",
            "human_loop_only": False,
            "provider": "anthropic",
            "model": "claude-haiku-4-5-20251001",
            "role_fit": ["coder"],
        },
    ]

    seats: list[dict[str, Any]] = []
    for row in registry_rows:
        role_fit = row["role_fit"]
        assert isinstance(role_fit, list)
        seats.append(
            _seat(
                row["id"],
                job=row["job"],
                supervision="human_in_loop" if row["human_loop_only"] else "unattended",
                required_capabilities=[row["required_capability"], "long_context"],
                current_pin={
                    "provider": row["provider"],
                    "model": row["model"],
                    "reason": f"Current registry role_fit: {', '.join(role_fit)}.",
                },
            )
        )

    document = validate_seats_data(_document(seats))

    assert document["seats"][0]["supervision"] == "human_in_loop"
    assert document["seats"][1]["supervision"] == "unattended"


def test_hypocrisynow_three_seats_pressure_case() -> None:
    extraction = _seat(
        "extraction",
        job="Extract political claims from messy article text into normalized claim JSON.",
        output_contract={
            "schema_ref": "schemas/hypocrisynow-claims.schema.json",
            "validation": "JSON array with entity, topic, stance, quote, and confidence fields.",
        },
        input_character="messy",
        supervision="unattended",
        required_capabilities=["json_mode", "long_context"],
        failure_cost={
            "level": "high",
            "description": "Bad claims pollute the claim store and degrade all downstream detection.",
        },
        current_pin={
            "provider": "openai",
            "model": "gpt-4o-mini",
            "reason": "Matches hypocrisynow config.models GPT_MODEL_EXTRACTION.",
        },
    )
    detection = _seat(
        "detection",
        job="Classify claim pairs as contradiction or asymmetry with structured severity metadata.",
        output_contract={
            "schema_ref": "schemas/hypocrisynow-detection.schema.json",
            "validation": "Require classification, confidence, severity, and explanation JSON fields.",
        },
        input_character="adversarial",
        supervision="human_in_loop",
        required_capabilities=["web_search", "tools", "json_mode", "long_context"],
        failure_cost={
            "level": "high",
            "description": "False positives waste editorial review and false negatives hide findings.",
        },
        current_pin={
            "provider": "openai",
            "model": "gpt-4o-mini",
            "reason": "Matches hypocrisynow config.models GPT_MODEL_DETECTION.",
        },
    )
    expert_review = _seat(
        "expert_review",
        job="Decide whether a pending hypocrisy finding should publish or be rejected.",
        output_contract={
            "schema_ref": "schemas/hypocrisynow-expert-review.schema.json",
            "validation": "Require decision, confidence, reasoning, rejection reason, and score JSON.",
        },
        input_character="messy",
        supervision="unattended",
        required_capabilities=["json_mode", "long_context"],
        failure_cost={
            "level": "critical",
            "description": "Wrong unattended decisions can publish unfair findings or bury real ones.",
        },
        volume={
            "expected": 10,
            "unit": "reviews_per_run",
        },
        current_pin={
            "provider": "openai",
            "model": "gpt-4o-mini",
            "reason": "Matches pipeline.expert_reviewer GPT_MODEL via detection config.",
        },
    )

    document = validate_seats_data(_document([extraction, detection, expert_review]))

    assert [seat["id"] for seat in document["seats"]] == [
        "extraction",
        "detection",
        "expert_review",
    ]


def test_ai_memory_frozen_pins_and_sealed_holdout_are_expressible() -> None:
    judge = _seat(
        "benchmark_judge",
        job="Judge benchmark answers using verbatim upstream prompts.",
        input_character="clean",
        supervision="unattended",
        failure_cost={
            "level": "critical",
            "description": "Changing this judge invalidates comparison with the benchmark paper.",
        },
        current_pin={
            "provider": "openai",
            "model": "gpt-4o-2024-08-06",
            "status": "FROZEN",
            "reason": "Frozen because upstream prompts and judge model preserve paper comparability.",
            "parameters": {"temperature": 0},
        },
    )
    answerer = _seat(
        "benchmark_answerer",
        job="Answer benchmark questions with the same model users actually deploy.",
        input_character="messy",
        supervision="unattended",
        failure_cost={
            "level": "critical",
            "description": "Changing this answerer would make scores no longer represent production.",
        },
        current_pin={
            "provider": "anthropic",
            "model": "claude-haiku-4-5-20251001",
            "status": "FROZEN",
            "reason": "Frozen because this is the deployed answerer measured by the benchmark.",
        },
    )

    document = validate_seats_data(_document([judge, answerer]))

    assert document["seats"][0]["current_pin"]["status"] == "FROZEN"
    assert (
        document["seats"][0]["eval_fixtures"]["split"]["sealed_unseal_env"]
        == "MODEL_BENCH_UNSEAL"
    )


def test_frozen_pin_reason_is_required() -> None:
    document = _document([_seat("benchmark_judge")])
    document["seats"][0]["current_pin"]["status"] = "FROZEN"
    del document["seats"][0]["current_pin"]["reason"]

    with pytest.raises(SeatValidationError) as excinfo:
        validate_seats_data(document)

    assert "current_pin.reason" in str(excinfo.value)


def test_malformed_seats_yaml_is_hard_error() -> None:
    document = _document([_seat("bad_split")])
    del document["seats"][0]["eval_fixtures"]["split"]["sealed_remainders"]

    with pytest.raises(SeatValidationError) as excinfo:
        validate_seats_data(document)

    assert "sealed_remainders" in str(excinfo.value)


def test_split_must_cover_all_remainders() -> None:
    document = _document([_seat("incomplete_split")])
    split = document["seats"][0]["eval_fixtures"]["split"]
    split["dev_remainders"] = [1]
    split["sealed_remainders"] = [0]

    with pytest.raises(SeatValidationError) as excinfo:
        validate_seats_data(document)

    assert "must cover every remainder" in str(excinfo.value)


def test_duplicate_yaml_keys_are_hard_error(tmp_path: Path) -> None:
    path = tmp_path / "seats.yaml"
    path.write_text(
        "\n".join(
            [
                "schema_version: seats.v1",
                "project:",
                "  id: duplicate-test",
                "  id: duplicate-test-again",
                "seats: []",
            ]
        )
    )

    with pytest.raises(SeatValidationError) as excinfo:
        validate_seats_file(path)

    assert "duplicate key" in str(excinfo.value)


def test_cli_validate_rejects_malformed_file(tmp_path: Path) -> None:
    document = copy.deepcopy(_document([_seat("bad_cli")]))
    document["schema_version"] = "seats.v0"
    path = tmp_path / "seats.yaml"
    path.write_text(yaml.safe_dump(document))

    result = CliRunner().invoke(cli, ["seats", "validate", str(path)])

    assert result.exit_code != 0
    assert "schema_version" in result.output
