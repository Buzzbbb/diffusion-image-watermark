"""Experiment runner and recipe utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from . import recipe_bank
from .core import PROJECT_NAME, PROJECT_KIND
from .toolkit import ExperimentResult, run_pipeline, write_json


def available_recipes(limit: int = 12) -> List[Dict[str, object]]:
    return recipe_bank.all_recipes()[:limit]


def run_recipe(recipe_id: int = 1) -> ExperimentResult:
    recipe = recipe_bank.get_recipe(recipe_id)
    result = run_pipeline(PROJECT_NAME, PROJECT_KIND)
    result.notes.append(f"recipe={{recipe['name']}}, capacity={{recipe['capacity']}}, attack={{recipe['attack']}}")
    result.metrics["recipe_id"] = recipe_id
    result.metrics["recipe_capacity"] = recipe["capacity"]
    return result


def export_recipe_report(output_dir: Path, recipe_id: int = 1) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run_recipe(recipe_id)
    data = {"project": PROJECT_NAME, "recovered": result.recovered, "metrics": result.metrics, "notes": result.notes}
    path = output_dir / f"recipe_{recipe_id:03d}.json"
    write_json(path, data)
    return path
