"""Limites de performance em [tool.saucedemo] (sobrescrevíveis por variável de ambiente)."""

from saucedemo.config import settings


def login_page_load_ms() -> int:
    return settings.get_int("perf.login.page.max.ms")


def login_to_inventory_ms() -> int:
    return settings.get_int("perf.login.to.inventory.max.ms")


def largest_contentful_paint_ms() -> int:
    return settings.get_int("perf.lcp.max.ms")
