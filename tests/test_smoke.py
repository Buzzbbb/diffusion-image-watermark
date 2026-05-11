from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from diffusion_image_watermark.core import run_demo
from diffusion_image_watermark.experiments import available_recipes, export_recipe_report, run_recipe


class SmokeTest(unittest.TestCase):
    def test_demo_recovers_or_reports_payload(self):
        result = run_demo("smoke payload")
        self.assertTrue(result.metrics)
        self.assertTrue(result.recovered)

    def test_recipes_exist(self):
        self.assertGreaterEqual(len(available_recipes()), 5)
        result = run_recipe(2)
        self.assertIn("recipe_id", result.metrics)

    def test_export_recipe_report(self):
        path = export_recipe_report(ROOT / "docs", 1)
        self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
