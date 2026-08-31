"""compare_gcode.py must not fail dual slices for missing left-only wipe markers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compare_gcode import LEFT_ONLY, RIGHT_ONLY, markers_for  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"


class CompareGcodeTests(unittest.TestCase):
    def test_left_fixture_uses_left_markers(self) -> None:
        cand = (FIXTURES / "ideamaker_left_start_end.gcode").read_text(encoding="utf-8")
        mode, markers = markers_for(cand)
        self.assertEqual(mode, "left")
        self.assertTrue(all(m in markers for m in LEFT_ONLY))
        missing = [m for m in markers if m not in cand]
        self.assertEqual(missing, [])

    def test_right_fixture_uses_right_markers(self) -> None:
        cand = (FIXTURES / "ideamaker_right_start_end.gcode").read_text(encoding="utf-8")
        mode, markers = markers_for(cand)
        self.assertEqual(mode, "right")
        self.assertTrue(all(m in markers for m in RIGHT_ONLY))
        self.assertNotIn("M104 T0 S0", markers)
        self.assertNotIn("G1 F200 E10", cand)
        missing = [m for m in markers if m not in cand]
        self.assertEqual(missing, [])

    def test_dual_fixture_does_not_require_left_wipe(self) -> None:
        cand = (FIXTURES / "ideamaker_dual_start_end.gcode").read_text(encoding="utf-8")
        mode, markers = markers_for(cand)
        self.assertEqual(mode, "dual")
        self.assertFalse(any(m in markers for m in LEFT_ONLY))
        self.assertIn(";Filament Name #2:", markers)
        missing = [m for m in markers if m not in cand]
        self.assertEqual(missing, [])

    def test_prusaslicer_dual_fixture_passes_dual_markers(self) -> None:
        cand = (FIXTURES / "dual_start_end.gcode").read_text(encoding="utf-8")
        mode, markers = markers_for(cand)
        self.assertEqual(mode, "dual")
        missing = [m for m in markers if m not in cand]
        self.assertEqual(missing, [])

    def test_prusaslicer_config_footer_does_not_make_left_slice_dual(self) -> None:
        cand = (
            "M99123 x\n;Dimension:\n;Printer Type:\n;Firmware:\n;Filament Name #1:\n"
            "G28 X0 Y0\nG28 Z0\nG1 Z15.0 F300\nG1 F140 E29\nG1 X80 Y0 F140 E1\n"
            "M1001\nSET_VELOCITY_LIMIT ACCEL=5000.00\n"
            "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=10.00\nM1002\nM104 T0 S0\nM140 S0\nM84\n"
            "; prusaslicer_config = begin\n"
            "; start_gcode = T1\\nG1 F200 E10\\nG1 F200 E-11.00\n"
        )
        mode, markers = markers_for(cand)
        self.assertEqual(mode, "left")
        self.assertTrue(all(m in markers for m in LEFT_ONLY))


if __name__ == "__main__":
    unittest.main()
