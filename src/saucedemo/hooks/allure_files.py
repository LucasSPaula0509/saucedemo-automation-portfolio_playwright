"""Arquivos de apoio do Allure gravados em allure-results: ambiente e categorias."""

import platform
import shutil
from pathlib import Path
from typing import Final

CATEGORIES: Final = Path(__file__).resolve().parents[3] / "allure" / "categories.json"


def write_environment(results_dir: Path, environment: dict[str, str]) -> None:
    """environment.properties com os campos do Java ("Python" no lugar de "Java")."""
    values = {**environment, "OS": f"{platform.system()} {platform.release()}"}
    values["Python"] = platform.python_version()
    content = "".join(f"{key}={value}\n" for key, value in values.items())
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "environment.properties").write_text(content, encoding="utf-8")


def copy_categories(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CATEGORIES, results_dir / "categories.json")
