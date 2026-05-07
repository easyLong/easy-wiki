from __future__ import annotations

import sys
import unittest
from pathlib import Path


GOVERNANCE_DIR = Path(__file__).resolve().parents[1] / "services" / "governance"
if str(GOVERNANCE_DIR) not in sys.path:
    sys.path.insert(0, str(GOVERNANCE_DIR))

from governance_core import Artifact, ArtifactRegistry, StepContract, build_trace_record, resolve_inputs


class GovernanceCoreTestCase(unittest.TestCase):
    def test_source_plus_derived_requires_source_and_line_granularity(self) -> None:
        registry = ArtifactRegistry(
            [
                Artifact(
                    id="script-source",
                    type="source",
                    granularity="line",
                    provenance={"source_spans": [{"line_start": 1, "line_end": 20}]},
                ),
                Artifact(
                    id="script-ir",
                    type="ir",
                    granularity="line",
                    provenance={"derived_from": ["script-source"]},
                ),
            ]
        )
        contract = StepContract(
            step_id="build-shot-plan",
            name="Build Shot Plan",
            goal="Generate a shot plan without losing script detail.",
            output_type="shot-plan",
            primary_input_types=["ir"],
            secondary_input_types=["source", "expert"],
            must_read_source=True,
            requires_granularity="line",
            detail_loss_tolerance="low",
            provenance_requirement="source-span",
            selection_policy={"strategy": "source_plus_derived"},
        )

        decision = resolve_inputs(contract, registry)

        self.assertTrue(decision.allowed)
        self.assertEqual([artifact.id for artifact in decision.selected_inputs], ["script-ir", "script-source"])
        self.assertEqual(decision.missing_requirements, [])

    def test_low_detail_loss_blocks_summary_only_inputs(self) -> None:
        registry = ArtifactRegistry(
            [
                Artifact(
                    id="scene-summary",
                    type="summary",
                    granularity="section",
                    provenance={"derived_from": ["script-source"]},
                )
            ]
        )
        contract = StepContract(
            step_id="build-production-output",
            name="Build Production Output",
            goal="Generate an output that must preserve evidence detail.",
            output_type="production-output",
            primary_input_types=["summary"],
            must_read_source=False,
            requires_granularity="section",
            detail_loss_tolerance="low",
            provenance_requirement="input-artifacts",
            selection_policy={"strategy": "derived_only"},
        )

        decision = resolve_inputs(contract, registry)

        self.assertFalse(decision.allowed)
        self.assertIn("low detail-loss steps cannot use summary-only inputs", decision.missing_requirements)

    def test_trace_record_collects_source_artifacts_and_spans(self) -> None:
        selected = [
            Artifact(
                id="script-source",
                type="source",
                granularity="line",
                provenance={"source_spans": [{"line_start": 10, "line_end": 12}]},
            ),
            Artifact(
                id="script-ir",
                type="ir",
                granularity="line",
                provenance={"derived_from": ["script-source"]},
            ),
        ]

        trace = build_trace_record(
            output_id="shot-plan-v1",
            step_id="build-shot-plan",
            selected_inputs=selected,
            derivation_note="Resolved by governance contract.",
        )

        self.assertEqual(trace.input_artifact_ids, ["script-source", "script-ir"])
        self.assertEqual(trace.source_artifact_ids, ["script-source"])
        self.assertEqual(trace.source_spans[0]["artifact_id"], "script-source")
        self.assertEqual(trace.source_spans[0]["line_start"], 10)


if __name__ == "__main__":
    unittest.main()
