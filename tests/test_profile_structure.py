"""Checks that the vendor bundle has the expected wizard structure and G-code markers."""

from __future__ import annotations

import configparser
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "Raise3D.ini"
IDX = ROOT / "vendor" / "Raise3D.idx"


class VendorStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        text = VENDOR.read_text(encoding="utf-8")
        # configparser needs interpolation off because of {placeholders}
        parser = configparser.RawConfigParser(strict=False)
        parser.optionxform = str
        parser.read_string(text)
        cls.ini = parser
        cls.raw = text

    def test_vendor_and_model_sections(self) -> None:
        self.assertTrue(VENDOR.is_file())
        self.assertTrue(IDX.is_file())
        self.assertIn("vendor", self.ini)
        self.assertEqual(self.ini["vendor"]["name"], "Raise3D (experimental)")
        self.assertEqual(self.ini["vendor"]["config_version"], "0.2.1")
        self.assertIn("printer_model:PRO2PLUS_HS", self.ini)
        self.assertIn("printer_model:PRO2PLUS_HS_DUAL", self.ini)

    def test_left_printer_preset(self) -> None:
        section = "printer:Raise3D Pro2 Plus Hyper Speed 0.4 Left"
        self.assertIn(section, self.ini)
        p = self.ini[section]
        self.assertIn("0x0,305x0,305x305,0x305", p["bed_shape"])
        self.assertEqual(p["max_print_height"], "605")
        self.assertIn("PRINTER_VENDOR_RAISE3D", p["printer_notes"])
        self.assertIn("PRINTER_VARIANT_LEFT", p["printer_notes"])
        start = p["start_gcode"]
        self.assertTrue(start.startswith("M99123 "))
        self.assertIn("G28 X0 Y0", start)
        self.assertIn("G28 Z0", start)
        self.assertIn("G1 X20 Y0 F140 E30", start)
        self.assertIn("M1001", start)
        self.assertNotIn("G29", start)
        self.assertNotIn("M92", start)
        self.assertNotIn("M218", start)
        self.assertIn("M1002", p["end_gcode"])
        self.assertIn("M84", p["end_gcode"])

    def test_print_and_filament_are_tied_to_left_printer(self) -> None:
        filament = self.ini["filament:PLA @Raise3D Pro2 Plus HS"]
        printp = self.ini["print:0.20mm L1 Conservative @Raise3D Pro2 Plus HS Left"]
        cond_f = filament.get("compatible_printers_condition") or self.ini["filament:*common*"][
            "compatible_printers_condition"
        ]
        cond_p = printp.get("compatible_printers_condition") or self.ini["print:*common*"][
            "compatible_printers_condition"
        ]
        self.assertIn("PRINTER_MODEL_PRO2PLUS_HS", cond_f)
        self.assertNotIn("PRINTER_VARIANT_LEFT", cond_f)
        self.assertIn("PRINTER_VARIANT_LEFT", cond_p)
        self.assertIn(";Filament Name: PLA", filament["start_filament_gcode"])
        self.assertIn("filament_extruder_id", filament["start_filament_gcode"])
        self.assertNotIn("230", filament.get("temperature", "200"))

    def test_dual_printer_preset(self) -> None:
        section = "printer:Raise3D Pro2 Plus Hyper Speed 0.4 Dual"
        self.assertIn(section, self.ini)
        p = self.ini[section]
        self.assertEqual(p["nozzle_diameter"], "0.4,0.4")
        self.assertEqual(p["extruder_offset"], "0x0,0x0")
        self.assertIn("PRINTER_VARIANT_DUAL", p["printer_notes"])
        start = p["start_gcode"]
        self.assertTrue(start.startswith("M99123 "))
        self.assertIn("is_extruder_used[0]", start)
        self.assertIn("is_extruder_used[1]", start)
        self.assertIn("M104 T1", start)
        self.assertIn("M109 T1", start)
        self.assertIn("T1", start)
        self.assertIn("G1 X20 Y0 F140 E30", start)
        self.assertIn("G1 X40 Y0 F140 E30", start)
        self.assertIn("G28 X0 Y0", start)
        self.assertIn("G28 Z0", start)
        self.assertIn("M1001", start)
        self.assertNotIn("G29", start)
        self.assertNotIn("M92", start)
        self.assertNotIn("M218", start)
        self.assertNotIn("M116", p["toolchange_gcode"])
        self.assertIn("M109 T{next_extruder}", p["toolchange_gcode"])
        self.assertIn("M104 T1 S0", p["end_gcode"])
        self.assertIn("M1002", p["end_gcode"])
        printp = self.ini["print:0.20mm L1 Conservative @Raise3D Pro2 Plus HS Dual"]
        cond = printp.get("compatible_printers_condition") or ""
        self.assertIn("PRINTER_VARIANT_DUAL", cond)
        self.assertEqual(printp["wipe_tower"], "0")

    def test_klipper_flavor_and_no_relative_e(self) -> None:
        common = self.ini["printer:*common*"]
        self.assertEqual(common["gcode_flavor"], "klipper")
        self.assertEqual(common["use_relative_e_distances"], "0")
        self.assertEqual(common["autoemit_temperature_commands"], "0")


if __name__ == "__main__":
    unittest.main()
