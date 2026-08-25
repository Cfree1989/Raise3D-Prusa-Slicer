"""Run the G-code validator against known-good and unsafe fixtures."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_gcode import validate  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"


class GcodeSafetyTests(unittest.TestCase):
    def test_ideamaker_start_end_passes(self) -> None:
        errors = validate(FIXTURES / "ideamaker_left_start_end.gcode")
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_unsafe_fixture_fails(self) -> None:
        errors = validate(FIXTURES / "unsafe_commands.gcode")
        joined = "\n".join(errors)
        self.assertTrue(any("G29" in e for e in errors), joined)
        self.assertTrue(any("M92" in e for e in errors), joined)
        self.assertTrue(any("M600" in e for e in errors), joined)

    def test_dual_start_end_passes(self) -> None:
        errors = validate(FIXTURES / "dual_start_end.gcode")
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_ideamaker_dual_start_end_passes(self) -> None:
        errors = validate(FIXTURES / "ideamaker_dual_start_end.gcode")
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_start_only_is_not_a_complete_job(self) -> None:
        errors = validate(FIXTURES / "ideamaker_left_start.gcode")
        self.assertTrue(any("M1002" in e for e in errors))
        self.assertTrue(any("shutdown" in e.lower() or "M104 S0" in e or "M84" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
