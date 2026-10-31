"""Asserções reutilizadas pelos steps."""

from playwright.sync_api import Locator, expect

from saucedemo.pages.base_page import LoadablePage


def expect_loaded(page: LoadablePage, description: str) -> None:
    expect(page.marker(), description).to_be_visible()
    actual_path = page.current_path()
    assert actual_path == page.path, f"{description}: caminho '{actual_path}' != '{page.path}'"


def expect_text(locator: Locator, description: str, expected: str) -> None:
    expect(locator, description).to_have_text(expected)


def expect_absent(locator: Locator, description: str) -> None:
    expect(locator, description).to_have_count(0)
