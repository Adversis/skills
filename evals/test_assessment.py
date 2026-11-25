"""Regression tests for assessment evidence and register references."""

import json
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_assessment import unique_fields, validate_assessment


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "examples/assessment.json").read_text())
        register = ROOT / "evals/river-archive/base/docs/security-requirements.yaml"
        self.register = yaml.safe_load(register.read_text())
        self.check = self.record["checks"]["SEC-001/denied-export"]

    def test_existing_test_without_run(self):
        validate_assessment(self.record, self.register)

    def test_unmapped_finding_without_register(self):
        self.record.update(affected_requirements=[], checks={})
        self.record["findings"][0]["requirement_ids"] = []
        validate_assessment(self.record)

    def test_result_needs_evidence_from_the_candidate(self):
        for status in ("passed", "failed"):
            with self.subTest(status=status):
                self.check.update(status=status, run=None)
                with self.assertRaises(ValueError):
                    validate_assessment(self.record)
                run = {"revision": "old", "environment": "fixture", "evidence": ["run 1, denied export"]}
                self.check["run"] = run
                with self.assertRaisesRegex(ValueError, "revision"):
                    validate_assessment(self.record)
                run["revision"] = self.record["revision"]
                validate_assessment(self.record, self.register)

    def test_unknown_case(self):
        self.record["checks"]["SEC-001/unknown-case"] = self.check
        with self.assertRaisesRegex(ValueError, "Unknown verification cases"):
            validate_assessment(self.record, self.register)

    def test_missing_revision_needs_a_limitation(self):
        self.record.update(revision=None, limitations=[])
        with self.assertRaises(ValueError):
            validate_assessment(self.record)
        self.record["limitations"].append("The design has no candidate revision.")
        validate_assessment(self.record)

    def test_omitted_affected_id(self):
        self.record["affected_requirements"] = []
        with self.assertRaisesRegex(ValueError, "missing from affected_requirements"):
            validate_assessment(self.record)

    def test_duplicate_json_fields(self):
        with self.assertRaisesRegex(ValueError, "Repeated JSON field"):
            json.loads('{"check": {"status": "failed", "status": "passed"}}', object_pairs_hook=unique_fields)
