#!/usr/bin/env python3
"""Validate the v0.6 Global Design Jury report.

The jury is intentionally stricter than basic Visual/Composition QA. It rejects
slides that are merely tidy but not world-class in purpose, hierarchy, craft,
communication, role fit, or source identity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

GLOBAL_JURY_SCHEMA = 1

CORE_CHECKS = (
    "purpose_is_clear",
    "focal_point_is_unambiguous",
    "hierarchy_is_structural",
    "spacing_is_intentional",
    "typography_is_crafted",
    "color_is_disciplined",
    "source_identity_is_preserved",
    "signal_to_noise_is_high",
    "glance_test_pass",
    "brand_and_status_do_not_compete",
    "no_generic_template_skin",
)

CORE_SCORES = (
    "purpose",
    "hierarchy",
    "simplicity",
    "craft",
    "composition",
    "typography",
    "spacing_rhythm",
    "color_discipline",
    "source_identity",
    "signal_to_noise",
    "glance_readability",
    "executive_readiness",
)

IDENTITY_CHECKS = (
    "source_personality_preserved",
    "no_template_convergence",
    "no_unjustified_cardification",
    "no_unjustified_dark_techification",
    "no_unjustified_gradientization",
    "no_brand_personality_erasure",
)

REQUIRED_EVIDENCE = (
    "primary_purpose",
    "focal_point",
    "reading_order",
    "grid_or_alignment_logic",
    "spacing_logic",
    "source_identity_anchors",
    "what_was_removed_or_restrained",
    "why_this_is_not_a_generic_template",
)

JURY_LENSES = (
    "purpose_hierarchy_craft",
    "executive_communication",
    "domain_role_fit",
)

ROLE_SCORES = {
    "keynote_launch": (
        "stage_readability",
        "single_idea_focus",
        "visual_pause",
        "emotional_tone_fit",
        "hero_focus",
    ),
    "executive_strategy": (
        "decision_path_clarity",
        "evidence_priority",
        "scan_efficiency",
        "status_risk_clarity",
        "executive_density_control",
    ),
    "technical_review": (
        "data_legibility",
        "comparison_structure",
        "scaffolding_restraint",
        "focal_evidence",
        "technical_density_control",
    ),
    "research_academic": (
        "figure_caption_relation",
        "method_result_structure",
        "citation_legibility",
        "research_density_control",
        "evidence_traceability",
    ),
    "brand_editorial": (
        "typographic_expression",
        "art_direction",
        "whitespace_control",
        "asymmetric_balance",
        "brand_expression",
    ),
    "agenda_section_closing": (
        "navigation_clarity",
        "pacing",
        "brand_continuity",
        "artifact_cleanliness",
        "transition_role_fit",
    ),
    "comparison": (
        "comparison_structure",
        "peer_balance",
        "difference_salience",
        "scan_efficiency",
        "evidence_priority",
    ),
    "other": (
        "role_fit",
        "audience_fit",
        "information_density_control",
        "reading_path",
        "visual_coherence",
    ),
}


def _present(value) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return value is not None


def _validate_numeric(scores: dict, keys, floor: float, label: str, errors: list[str]):
    values: list[float] = []
    for key in keys:
        value = scores.get(key)
        if not isinstance(value, (int, float)):
            errors.append(f"{label}: numeric score {key} is required")
            continue
        value = float(value)
        values.append(value)
        if value < floor:
            errors.append(f"{label}: {key} score {value:g} < minimum {floor:g}")
        if value > 100:
            errors.append(f"{label}: {key} score {value:g} > 100")
    return values


def validate_report(
    report: dict,
    expected_slides: int,
    min_dimension: float = 90.0,
    min_slide_overall: float = 93.0,
    min_role_dimension: float = 90.0,
    min_role_overall: float = 92.0,
    min_identity: float = 95.0,
    min_archetype_fit: float = 92.0,
    max_generic_risk: float = 10.0,
    min_deck_overall: float = 93.0,
):
    errors: list[str] = []

    if report.get("schema") != GLOBAL_JURY_SCHEMA:
        errors.append(f"schema must be {GLOBAL_JURY_SCHEMA}")
    if report.get("slide_count") != expected_slides:
        errors.append(
            f"slide_count {report.get('slide_count')!r} != expected {expected_slides}"
        )
    if not str(report.get("render_engine", "")).strip():
        errors.append("render_engine is required")
    if not str(report.get("reviewer", "")).strip():
        errors.append("reviewer is required")
    if not str(report.get("audience_profile", "")).strip():
        errors.append("audience_profile is required")

    review_rounds = report.get("review_rounds")
    if not isinstance(review_rounds, int) or review_rounds < 2:
        errors.append("review_rounds must be an integer >= 2")

    lenses = report.get("jury_lenses")
    if not isinstance(lenses, dict):
        errors.append("jury_lenses object is required")
        lenses = {}
    for lens in JURY_LENSES:
        item = lenses.get(lens)
        if not isinstance(item, dict):
            errors.append(f"jury_lenses.{lens} object is required")
            continue
        if item.get("pass") is not True:
            errors.append(f"jury_lenses.{lens}.pass must be true")
        if not _present(item.get("evidence")):
            errors.append(f"jury_lenses.{lens}.evidence is required")

    identity = report.get("deck_identity")
    if not isinstance(identity, dict):
        errors.append("deck_identity object is required")
        identity = {}

    identity_checks = identity.get("checks")
    if not isinstance(identity_checks, dict):
        errors.append("deck_identity.checks object is required")
        identity_checks = {}
    for key in IDENTITY_CHECKS:
        if identity_checks.get(key) is not True:
            errors.append(f"deck_identity.checks.{key} must be true")

    for key in ("source_personality", "final_personality", "identity_evidence"):
        if not _present(identity.get(key)):
            errors.append(f"deck_identity.{key} is required")

    identity_score = identity.get("identity_fidelity_score")
    if not isinstance(identity_score, (int, float)):
        errors.append("deck_identity.identity_fidelity_score is required")
    elif identity_score < min_identity:
        errors.append(
            f"deck_identity.identity_fidelity_score {identity_score} < minimum {min_identity}"
        )

    archetype_fit = identity.get("archetype_fit_score")
    if not isinstance(archetype_fit, (int, float)):
        errors.append("deck_identity.archetype_fit_score is required")
    elif archetype_fit < min_archetype_fit:
        errors.append(
            f"deck_identity.archetype_fit_score {archetype_fit} < minimum {min_archetype_fit}"
        )

    generic_risk = identity.get("generic_template_risk")
    if not isinstance(generic_risk, (int, float)):
        errors.append("deck_identity.generic_template_risk is required")
    elif generic_risk > max_generic_risk:
        errors.append(
            f"deck_identity.generic_template_risk {generic_risk} > maximum {max_generic_risk}"
        )

    slides = report.get("slides")
    if not isinstance(slides, list):
        errors.append("slides must be a list")
        slides = []

    seen = set()
    slide_overalls: list[float] = []
    for item in slides:
        if not isinstance(item, dict):
            errors.append("each slides[] item must be an object")
            continue
        slide_no = item.get("slide")
        if not isinstance(slide_no, int):
            errors.append("slide number must be an integer")
            continue
        if slide_no in seen:
            errors.append(f"duplicate slide review: {slide_no}")
        seen.add(slide_no)
        label = f"slide {slide_no}"

        role = item.get("jury_role")
        if role not in ROLE_SCORES:
            errors.append(
                f"{label}: jury_role must be one of {sorted(ROLE_SCORES)}"
            )
            role = "other"

        checks = item.get("checks")
        if not isinstance(checks, dict):
            errors.append(f"{label}: checks object is required")
            checks = {}
        for key in CORE_CHECKS:
            if checks.get(key) is not True:
                errors.append(f"{label}: {key} must be true")

        scores = item.get("scores")
        if not isinstance(scores, dict):
            errors.append(f"{label}: scores object is required")
            scores = {}
        core_values = _validate_numeric(
            scores, CORE_SCORES, min_dimension, label, errors
        )
        if isinstance(scores.get("source_identity"), (int, float)) and scores["source_identity"] < min_identity:
            errors.append(
                f"{label}: source_identity score {scores['source_identity']} < minimum {min_identity}"
            )
        if isinstance(scores.get("craft"), (int, float)) and scores["craft"] < 92:
            errors.append(f"{label}: craft score {scores['craft']} < minimum 92")

        overall = item.get("slide_jury_score")
        if not isinstance(overall, (int, float)):
            errors.append(f"{label}: slide_jury_score is required")
        else:
            overall = float(overall)
            slide_overalls.append(overall)
            if overall < min_slide_overall:
                errors.append(
                    f"{label}: slide_jury_score {overall:g} < minimum {min_slide_overall:g}"
                )
            if overall > 100:
                errors.append(f"{label}: slide_jury_score {overall:g} > 100")
            if core_values:
                avg = sum(core_values) / len(core_values)
                if overall > avg + 3:
                    errors.append(
                        f"{label}: slide_jury_score {overall:g} is implausibly higher "
                        f"than core dimension average {avg:.1f}"
                    )

        role_scores = item.get("role_scores")
        if not isinstance(role_scores, dict):
            errors.append(f"{label}: role_scores object is required")
            role_scores = {}
        role_values = _validate_numeric(
            role_scores, ROLE_SCORES[role], min_role_dimension, f"{label} role", errors
        )
        role_overall = item.get("role_score")
        if not isinstance(role_overall, (int, float)):
            errors.append(f"{label}: role_score is required")
        else:
            role_overall = float(role_overall)
            if role_overall < min_role_overall:
                errors.append(
                    f"{label}: role_score {role_overall:g} < minimum {min_role_overall:g}"
                )
            if role_values:
                role_avg = sum(role_values) / len(role_values)
                if role_overall > role_avg + 3:
                    errors.append(
                        f"{label}: role_score {role_overall:g} is implausibly higher "
                        f"than role dimension average {role_avg:.1f}"
                    )

        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            errors.append(f"{label}: evidence object is required")
            evidence = {}
        for key in REQUIRED_EVIDENCE:
            if not _present(evidence.get(key)):
                errors.append(f"{label}: evidence.{key} is required")

    expected = set(range(1, expected_slides + 1))
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing:
        errors.append(f"slides missing jury review: {missing}")
    if extra:
        errors.append(f"unexpected slide numbers in jury review: {extra}")

    deck_score = report.get("deck_jury_score")
    if not isinstance(deck_score, (int, float)):
        errors.append("deck_jury_score is required")
    else:
        deck_score = float(deck_score)
        if deck_score < min_deck_overall:
            errors.append(
                f"deck_jury_score {deck_score:g} < minimum {min_deck_overall:g}"
            )
        if slide_overalls:
            avg_slides = sum(slide_overalls) / len(slide_overalls)
            if deck_score > avg_slides + 2:
                errors.append(
                    f"deck_jury_score {deck_score:g} is implausibly higher than "
                    f"slide average {avg_slides:.1f}"
                )

    if report.get("overall_pass") is not True:
        errors.append("overall_pass must be true")

    identity_ok = not any(error.startswith("deck_identity") for error in errors)
    return not errors, identity_ok, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Global Design Jury gate / 世界級投影片評審閘門"
    )
    parser.add_argument("report")
    parser.add_argument("--expected-slides", type=int, required=True)
    parser.add_argument("--min-dimension", type=float, default=90.0)
    parser.add_argument("--min-slide-overall", type=float, default=93.0)
    parser.add_argument("--min-role-dimension", type=float, default=90.0)
    parser.add_argument("--min-role-overall", type=float, default=92.0)
    parser.add_argument("--min-identity", type=float, default=95.0)
    parser.add_argument("--min-archetype-fit", type=float, default=92.0)
    parser.add_argument("--max-generic-risk", type=float, default=10.0)
    parser.add_argument("--min-deck-overall", type=float, default=93.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        ok, identity_ok, errors = validate_report(
            report,
            args.expected_slides,
            args.min_dimension,
            args.min_slide_overall,
            args.min_role_dimension,
            args.min_role_overall,
            args.min_identity,
            args.min_archetype_fit,
            args.max_generic_risk,
            args.min_deck_overall,
        )
    except Exception as exc:
        ok, identity_ok, errors = False, False, [str(exc)]

    result = {
        "GLOBAL_DESIGN_JURY_PASS": ok,
        "DECK_IDENTITY_PASS": identity_ok,
        "global_jury_schema": GLOBAL_JURY_SCHEMA,
        "required_core_checks": list(CORE_CHECKS),
        "required_core_scores": list(CORE_SCORES),
        "required_identity_checks": list(IDENTITY_CHECKS),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"GLOBAL_DESIGN_JURY_PASS={'true' if ok else 'false'}")
        print(f"DECK_IDENTITY_PASS={'true' if identity_ok else 'false'}")
        print(f"global_jury_errors={len(errors)}")
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
