from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "pptx-beautify-lock" / "scripts" / "global_design_jury_gate.py"


def run_gate(report: Path):
    return subprocess.run(
        [sys.executable, str(GATE), str(report), "--expected-slides", "1"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def valid_payload():
    core_checks = {
        "purpose_is_clear": True,
        "focal_point_is_unambiguous": True,
        "hierarchy_is_structural": True,
        "spacing_is_intentional": True,
        "typography_is_crafted": True,
        "color_is_disciplined": True,
        "source_identity_is_preserved": True,
        "signal_to_noise_is_high": True,
        "glance_test_pass": True,
        "brand_and_status_do_not_compete": True,
        "no_generic_template_skin": True,
    }
    scores = {
        "purpose": 94,
        "hierarchy": 94,
        "simplicity": 93,
        "craft": 94,
        "composition": 94,
        "typography": 93,
        "spacing_rhythm": 94,
        "color_discipline": 93,
        "source_identity": 97,
        "signal_to_noise": 94,
        "glance_readability": 94,
        "executive_readiness": 93,
    }
    role_scores = {
        "data_legibility": 95,
        "comparison_structure": 94,
        "scaffolding_restraint": 93,
        "focal_evidence": 94,
        "technical_density_control": 93,
    }
    return {
        "schema": 1,
        "slide_count": 1,
        "render_engine": "contract-test-renderer",
        "reviewer": "contract-test-reviewer",
        "audience_profile": "external top-tier technology customer engineering review",
        "source_render_set": "source-render-sha256:aaa",
        "final_render_set": "final-render-sha256:bbb",
        "review_rounds": 2,
        "review_history": [
            {
                "round": 1,
                "reviewer": "contract-test-reviewer",
                "render_fingerprint": "candidate-render-1",
                "source_render_reference": "source-render-sha256:aaa",
                "final_render_reference": "candidate-render-1",
                "findings_summary": "minor spacing refinement identified",
                "actions_or_verification": "refined spacing and re-rendered",
                "verdict": "fail",
            },
            {
                "round": 2,
                "reviewer": "contract-test-reviewer",
                "render_fingerprint": "final-render-sha256:bbb",
                "source_render_reference": "source-render-sha256:aaa",
                "final_render_reference": "final-render-sha256:bbb",
                "findings_summary": "no blocking world-class defects",
                "actions_or_verification": "independent second verification completed",
                "verdict": "pass",
            },
        ],
        "overall_pass": True,
        "deck_jury_score": 94,
        "jury_lenses": {
            "purpose_hierarchy_craft": {"pass": True, "evidence": "purpose and craft reviewed"},
            "executive_communication": {"pass": True, "evidence": "scan path reviewed"},
            "domain_role_fit": {"pass": True, "evidence": "technical review fit reviewed"},
        },
        "deck_identity": {
            "checks": {
                "source_personality_preserved": True,
                "no_template_convergence": True,
                "no_unjustified_cardification": True,
                "no_unjustified_dark_techification": True,
                "no_unjustified_gradientization": True,
                "no_brand_personality_erasure": True,
            },
            "source_personality": "light technical review with restrained corporate branding",
            "final_personality": "same technical identity with stronger hierarchy and craft",
            "identity_evidence": ["source light canvas retained", "brand anchors retained"],
            "identity_fidelity_score": 97,
            "archetype_fit_score": 95,
            "generic_template_risk": 4,
        },
        "slides": [
            {
                "slide": 1,
                "jury_role": "technical_review",
                "checks": core_checks,
                "scores": scores,
                "slide_jury_score": 94,
                "role_scores": role_scores,
                "role_score": 94,
                "evidence": {
                    "primary_purpose": "technical limits and comparison",
                    "focal_point": "limit table then peer charts",
                    "reading_order": ["title", "table", "L/R charts"],
                    "grid_or_alignment_logic": ["shared table rail", "shared chart top rail"],
                    "spacing_logic": "two spacing tiers separate groups from internal content",
                    "source_identity_anchors": ["light canvas", "corporate brand zone"],
                    "what_was_removed_or_restrained": "decorative noise restrained",
                    "why_this_is_not_a_generic_template": "source density and brand terrain retained",
                },
            }
        ],
    }


class GlobalDesignJuryGateTests(unittest.TestCase):
    def write_report(self, directory: str, payload: dict) -> Path:
        path = Path(directory) / "jury.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_world_class_report_passes(self):
        with tempfile.TemporaryDirectory() as td:
            result = run_gate(self.write_report(td, valid_payload()))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("GLOBAL_DESIGN_JURY_PASS=true", result.stdout)
            self.assertIn("DECK_IDENTITY_PASS=true", result.stdout)

    def test_one_weak_dimension_cannot_hide_behind_high_overall(self):
        with tempfile.TemporaryDirectory() as td:
            payload = deepcopy(valid_payload())
            payload["slides"][0]["scores"]["hierarchy"] = 89
            result = run_gate(self.write_report(td, payload))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("hierarchy score 89", result.stdout)

    def test_generic_template_convergence_fails_identity(self):
        with tempfile.TemporaryDirectory() as td:
            payload = deepcopy(valid_payload())
            payload["deck_identity"]["generic_template_risk"] = 11
            result = run_gate(self.write_report(td, payload))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("DECK_IDENTITY_PASS=false", result.stdout)
            self.assertIn("generic_template_risk 11", result.stdout)

    def test_missing_independent_jury_lens_fails(self):
        with tempfile.TemporaryDirectory() as td:
            payload = deepcopy(valid_payload())
            del payload["jury_lenses"]["executive_communication"]
            result = run_gate(self.write_report(td, payload))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("jury_lenses.executive_communication", result.stdout)

    def test_integer_review_rounds_without_history_does_not_count_as_craft(self):
        with tempfile.TemporaryDirectory() as td:
            payload = deepcopy(valid_payload())
            payload["review_history"] = []
            result = run_gate(self.write_report(td, payload))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("review_history length 0 != review_rounds 2", result.stdout)


if __name__ == "__main__":
    unittest.main()
