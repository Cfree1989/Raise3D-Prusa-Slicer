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
        self.assertEqual(self.ini["vendor"]["config_version"], "0.5.4")
        self.assertNotIn("printer_model:PRO2PLUS_HS", self.ini)
        self.assertIn("printer_model:PRO2PLUS_HS_DUAL", self.ini)
        self.assertNotIn("printer:Raise3D Pro2 Plus Hyper Speed 0.4 Left", self.ini)

    def test_print_and_filament_are_tied_to_dual_printer(self) -> None:
        filament = self.ini["filament:Generic PLA @Raise3D Pro2 Plus HS"]
        printp = self.ini["print:0.20mm SPEED @Raise3D Pro2 Plus HS"]
        cond_f = filament.get("compatible_printers_condition") or self.ini["filament:*common*"][
            "compatible_printers_condition"
        ]
        cond_p = printp.get("compatible_printers_condition") or self.ini["print:*common*"][
            "compatible_printers_condition"
        ]
        self.assertIn("PRINTER_MODEL_PRO2PLUS_HS", cond_f)
        self.assertIn("PRINTER_VARIANT_DUAL", cond_p)
        self.assertNotIn("PRINTER_VARIANT_LEFT", cond_p)
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
        self.assertIn("G1 F200 E10", start)
        self.assertIn("G1 F200 E-11.00", start)
        self.assertIn("G1 X20 Y0 F140 E1", start)
        self.assertNotIn("G1 X40 Y0", start)
        self.assertIn("M104 T1 S180", start)
        self.assertIn("M83", start)
        self.assertNotIn("M82", start)
        self.assertIn("G28 X0 Y0", start)
        self.assertIn("G28 Z0", start)
        self.assertIn("M1001", start)
        self.assertNotIn("G29", start)
        self.assertNotIn("M92", start)
        self.assertNotIn("M218", start)
        self.assertNotIn(";Extruder Offset #2", start)
        self.assertEqual(p["retract_length_toolchange"], "11,11")
        self.assertNotIn("M116", p["toolchange_gcode"])
        self.assertNotIn("temperature[previous_extruder]", p["toolchange_gcode"])
        self.assertNotIn("X30.000 Y295.000", p["toolchange_gcode"])
        self.assertNotIn("X96", p["toolchange_gcode"])
        self.assertIn("M104 T0 S180", p["toolchange_gcode"])
        self.assertIn("{if previous_extruder == 0}", p["toolchange_gcode"])
        self.assertIn("M109 T{next_extruder}", p["toolchange_gcode"])
        self.assertIn("M104 T1 S0", p["end_gcode"])
        self.assertIn("M1002", p["end_gcode"])
        printp = self.ini["print:0.20mm SPEED @Raise3D Pro2 Plus HS"]
        cond = printp.get("compatible_printers_condition") or self.ini["print:*common*"][
            "compatible_printers_condition"
        ]
        self.assertIn("PRINTER_VARIANT_DUAL", cond)
        self.assertEqual(printp.get("wipe_tower") or self.ini["print:*common*"]["wipe_tower"], "1")

    def test_print_is_xl_layout_capped_at_hyper_fff_l1(self) -> None:
        p = self.ini["print:*common*"]
        self.assertEqual(p["perimeters"], "2")
        self.assertEqual(p["skirts"], "0")
        self.assertEqual(p["fill_pattern"], "grid")
        self.assertEqual(p["first_layer_height"], "0.2")
        self.assertEqual(p["perimeter_generator"], "arachne")
        self.assertEqual(p["max_print_speed"], "150")
        self.assertEqual(p["perimeter_speed"], "150")
        self.assertEqual(p["infill_speed"], "150")
        self.assertEqual(p["travel_speed"], "150")
        self.assertEqual(p["default_acceleration"], "2500")
        self.assertLessEqual(int(p["travel_acceleration"]), 5000)
        self.assertEqual(p["wipe_tower"], "1")
        self.assertEqual(p["wipe_tower_cone_angle"], "25")
        self.assertEqual(p["wipe_tower_brim_width"], "3")
        self.assertEqual(p["wipe_tower_bridging"], "8")
        self.assertEqual(p["wipe_tower_extra_spacing"], "150")
        self.assertEqual(p["single_extruder_multi_material_priming"], "0")
        self.assertEqual(p["duplicate_distance"], "6")
        self.assertEqual(p["support_material_extruder"], "0")
        self.assertEqual(p["support_material_interface_extruder"], "0")
        self.assertNotIn("wipe_tower_x", p)
        self.assertNotIn("wipe_tower_rotation_angle", p)
        filament = self.ini["filament:Generic PLA @Raise3D Pro2 Plus HS"]
        self.assertEqual(filament["filament_max_volumetric_speed"], "15")

    def test_xl_style_print_family_exists(self) -> None:
        expected = [
            "print:0.10mm FAST DETAIL @Raise3D Pro2 Plus HS",
            "print:0.15mm SPEED @Raise3D Pro2 Plus HS",
            "print:0.15mm STRUCTURAL @Raise3D Pro2 Plus HS",
            "print:0.20mm SPEED @Raise3D Pro2 Plus HS",
            "print:0.20mm STRUCTURAL @Raise3D Pro2 Plus HS",
            "print:0.25mm SPEED @Raise3D Pro2 Plus HS",
            "print:0.25mm STRUCTURAL @Raise3D Pro2 Plus HS",
            "print:0.28mm DRAFT @Raise3D Pro2 Plus HS",
        ]
        for section in expected:
            self.assertIn(section, self.ini)
        structural = self.ini["print:0.20mm STRUCTURAL @Raise3D Pro2 Plus HS"]
        self.assertEqual(structural["perimeter_speed"], "80")
        self.assertEqual(structural["external_perimeter_speed"], "45")
        self.assertEqual(self.ini["print:0.15mm SPEED @Raise3D Pro2 Plus HS"]["layer_height"], "0.15")
        self.assertEqual(self.ini["print:0.10mm FAST DETAIL @Raise3D Pro2 Plus HS"]["layer_height"], "0.1")

    def test_wizard_filament_is_generic_pla_only(self) -> None:
        self.assertIn("filament:Generic PLA @Raise3D Pro2 Plus HS", self.ini)
        self.assertEqual(self.ini["filament:Generic PLA @Raise3D Pro2 Plus HS"]["alias"], "Generic PLA")
        self.assertNotIn("filament:PLA @Raise3D Pro2 Plus HS", self.ini)
        self.assertNotIn("filament:PETG @Raise3D Pro2 Plus HS", self.ini)
        self.assertNotIn("filament:ABS @Raise3D Pro2 Plus HS", self.ini)
        self.assertNotIn("filament:ASA @Raise3D Pro2 Plus HS", self.ini)
        self.assertNotIn("filament:FLEX @Raise3D Pro2 Plus HS", self.ini)
        self.assertEqual(
            self.ini["printer_model:PRO2PLUS_HS_DUAL"]["default_materials"],
            "Generic PLA @Raise3D Pro2 Plus HS",
        )

    def test_klipper_flavor_and_relative_e(self) -> None:
        common = self.ini["printer:*common*"]
        self.assertEqual(common["gcode_flavor"], "klipper")
        self.assertEqual(common["use_relative_e_distances"], "1")
        self.assertIn("G92 E0", common["before_layer_gcode"])
        self.assertEqual(common["autoemit_temperature_commands"], "0")
        self.assertEqual(common.get("thumbnails", ""), "")


if __name__ == "__main__":
    unittest.main()
