from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from diffusion_image_watermark.core import run_demo, write_report
from diffusion_image_watermark.experiments import export_recipe_report


if __name__ == "__main__":
    result = run_demo("open source information hiding demo")
    print(result.to_markdown())
    write_report(ROOT / "docs" / "demo_report.md", "open source information hiding demo")
    export_recipe_report(ROOT / "docs", 3)
