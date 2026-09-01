"""Checks the Potterbot vendor bundle structure."""

from __future__ import annotations

import configparser
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "Potterbot.ini"
IDX = ROOT / "vendor" / "Potterbot.idx"
BUNDLE = ROOT / "profiles" / "Potterbot-9-bundle.ini"


class VendorStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        text = VENDOR.read_text(encoding="utf-8")
        parser = configparser.RawConfigParser(strict=False)
        parser.optionxform = str
        parser.read_string(text)
        cls.ini = parser
        cls.raw = text

    def test_vendor_files_exist(self) -> None:
        self.assertTrue(VENDOR.is_file())
        self.assertTrue(IDX.is_file())
        self.assertTrue(BUNDLE.is_file())
        self.assertEqual(VENDOR.read_text(encoding="utf-8"), BUNDLE.read_text(encoding="utf-8"))

    def test_vendor_and_model(self) -> None:
        self.assertEqual(self.ini["vendor"]["name"], "3D Potter (experimental)")
        self.assertEqual(self.ini["vendor"]["config_version"], "0.1.2")
        self.assertEqual(self.ini["printer_model:POTTERBOT9"]["variants"], "1;2;3;4;5;6;7;8;9;10")
        self.assertEqual(
            self.ini["printer_model:POTTERBOT9"]["default_materials"],
            "Clay Potterbot;Clay Potterbot Retract",
        )

    def test_printer_common_is_cold_rrf(self) -> None:
        common = self.ini["printer:*common*"]
        self.assertEqual(common["gcode_flavor"], "reprapfirmware")
        self.assertEqual(common["host_type"], "duet")
        self.assertEqual(common["autoemit_temperature_commands"], "0")
        self.assertEqual(common["use_relative_e_distances"], "1")
        self.assertEqual(common["retract_length"], "0")
        self.assertEqual(common["pause_print_gcode"], "M25")
        start = common["start_gcode"].replace("\\n", "\n")
        end = common["end_gcode"].replace("\\n", "\n")
        self.assertIn("G28 ;Home all", start)
        self.assertNotIn("M104", start)
        self.assertNotIn("M109", start)
        self.assertIn("G0 Z10 E-500 F1000", end)
        self.assertIn("G28 ;Home all", end)

    def test_bed_is_bat_clipped_to_y_travel(self) -> None:
        p = self.ini["printer:3D Potterbot 9 5mm"]
        self.assertEqual(p["bed_shape"], "0x0,381x0,381x360,0x360")
        self.assertEqual(p["max_print_height"], "400")
        self.assertEqual(p["nozzle_diameter"], "5")

    def test_ten_nozzle_variants_and_two_vase_modes(self) -> None:
        common = self.ini["print:*common*"]
        self.assertEqual(common["layer_height"], "1.5")
        self.assertEqual(common["first_layer_height"], "1.5")
        for nozzle in range(1, 11):
            self.assertIn(f"printer:3D Potterbot 9 {nozzle}mm", self.ini)
            printer = self.ini[f"printer:3D Potterbot 9 {nozzle}mm"]
            self.assertGreaterEqual(float(printer["max_layer_height"]), 1.5)
            self.assertIn(f"print:1.5mm Vase Hollow @Potterbot {nozzle}mm", self.ini)
            self.assertIn(f"print:1.5mm Vase Bottom @Potterbot {nozzle}mm", self.ini)
            self.assertIn(f"print:1.5mm Infill Retract @Potterbot {nozzle}mm", self.ini)
            hollow = self.ini[f"print:1.5mm Vase Hollow @Potterbot {nozzle}mm"]
            bottom = self.ini[f"print:1.5mm Vase Bottom @Potterbot {nozzle}mm"]
            self.assertEqual(hollow["bottom_solid_layers"], "0")
            self.assertEqual(bottom["bottom_solid_layers"], "3")
            self.assertEqual(hollow.get("spiral_vase") or common["spiral_vase"], "1")
            self.assertEqual(hollow.get("layer_height") or common["layer_height"], "1.5")
            self.assertEqual(hollow["extrusion_width"], str(nozzle))
            self.assertNotIn("layer_height", hollow)
            self.assertIn(f"nozzle_diameter[0]=={nozzle}", hollow["compatible_printers_condition"])

    def test_official_cura_speeds_and_shell(self) -> None:
        p = self.ini["print:*common*"]
        self.assertEqual(p["perimeter_speed"], "40")
        self.assertEqual(p["travel_speed"], "80")
        self.assertEqual(p["solid_infill_speed"], "20")
        self.assertEqual(p["first_layer_speed"], "40")
        self.assertEqual(p["fill_density"], "0%")
        self.assertEqual(p["top_solid_layers"], "0")
        self.assertEqual(p["perimeters"], "1")
        self.assertEqual(p["skirts"], "3")
        self.assertEqual(p["skirt_distance"], "8")
        self.assertEqual(p["wipe_tower"], "0")
        five = self.ini["print:1.5mm Vase Hollow @Potterbot 5mm"]
        self.assertEqual(five.get("layer_height") or p["layer_height"], "1.5")
        self.assertEqual(five["extrusion_width"], "5")

    def test_infill_retract_is_slow_ram_not_faq(self) -> None:
        infill = self.ini["print:1.5mm Infill Retract @Potterbot 5mm"]
        self.assertEqual(infill["spiral_vase"], "0")
        self.assertEqual(infill["fill_density"], "15%")
        self.assertEqual(infill["bottom_solid_layers"], "3")
        self.assertEqual(infill["avoid_crossing_perimeters"], "1")
        self.assertEqual(self.ini["printer:*common*"]["retract_length"], "0")
        retract = self.ini["filament:Clay Potterbot Retract"]
        self.assertEqual(retract["filament_retract_length"], "80")
        self.assertEqual(retract["filament_retract_speed"], "17")
        self.assertEqual(retract["filament_deretract_speed"], "17")
        self.assertEqual(retract["filament_retract_lift"], "5")
        self.assertEqual(retract["filament_retract_before_travel"], "15")
        self.assertEqual(retract["filament_retract_layer_change"], "1")
        self.assertEqual(retract["filament_retract_restart_extra"], "10")
        self.assertLess(float(retract["filament_retract_speed"]), 85)
        self.assertNotEqual(retract["filament_retract_speed"], "1000")
        self.assertNotEqual(retract["filament_retract_length"], "1000")

    def test_clay_filament_is_cold(self) -> None:
        f = self.ini["filament:Clay Potterbot"]
        self.assertEqual(f["temperature"], "0")
        self.assertEqual(f["first_layer_temperature"], "0")
        self.assertEqual(f["bed_temperature"], "0")
        self.assertEqual(f["max_fan_speed"] if "max_fan_speed" in f else self.ini["filament:*common*"].get("max_fan_speed", "0"), "0")
        diameter = f.get("filament_diameter") or self.ini["filament:*common*"]["filament_diameter"]
        self.assertEqual(diameter, "1.75")

    def test_post_process_validator(self) -> None:
        post = self.ini["print:*common*"]["post_process"]
        self.assertIn("validate_gcode.py", post)
        self.assertIn("C:\\\\Windows\\\\py.exe -3", post)
        self.assertIn("C:\\\\Repos\\\\Prusa-Slicer-Print-Profiles\\\\Potterbot\\\\scripts\\\\", post)


if __name__ == "__main__":
    unittest.main()
