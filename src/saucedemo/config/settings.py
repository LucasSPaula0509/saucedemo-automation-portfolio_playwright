"""Leitura das configurações do projeto (equivalente ao ConfigReader + Environment do Java).

Precedência: variável de ambiente (CHAVE_COM_UNDERSCORE) > [tool.saucedemo] do pyproject.toml.
Base URL, navegador e headless também aceitam as opções do pytest-playwright (--base-url,
--browser, --browser-channel, --headed), que têm prioridade.
"""

import os
import tomllib
from functools import cache
from pathlib import Path
from typing import Any

PYPROJECT = Path(__file__).resolve().parents[3] / "pyproject.toml"


@cache
def _file_settings() -> dict[str, Any]:
    with PYPROJECT.open("rb") as file:
        return tomllib.load(file)["tool"]["saucedemo"]


def _env_name(key: str) -> str:
    return key.upper().replace(".", "_")


def get(key: str) -> str:
    value = os.environ.get(_env_name(key), "").strip()
    if value:
        return value
    if key not in _file_settings():
        raise KeyError(f"Configuração obrigatória ausente: {key}")
    return str(_file_settings()[key])


def get_int(key: str) -> int:
    return int(get(key))


def get_bool(key: str) -> bool:
    return get(key).lower() == "true"


def base_url() -> str:
    return get("base.url").rstrip("/")


def timeout_ms() -> int:
    return get_int("timeout.seconds") * 1000


def viewport() -> dict[str, int]:
    return {"width": get_int("window.width"), "height": get_int("window.height")}


def screenshot_every_step() -> bool:
    return get_bool("screenshot.every.step")


def fail_on_security_findings() -> bool:
    """True: achados das verificações passivas de segurança reprovam o cenário."""
    return get_bool("security.fail.on.findings")
