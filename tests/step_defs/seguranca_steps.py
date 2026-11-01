"""Verificações passivas: só leem o que o navegador já recebeu numa navegação normal.

Achados são anexados ao Allure e só reprovam o cenário com security.fail.on.findings=true.
"""

import logging
from typing import Final

import allure
import pytest
from pytest_bdd import then, when

from saucedemo.config import settings
from saucedemo.context.scenario_context import ScenarioContext
from saucedemo.data import cookies, paths
from saucedemo.pages.browser_navigation import BrowserNavigation
from saucedemo.pages.login_page import LoginPage
from saucedemo.security.security_headers_inspector import SecurityHeadersInspector
from saucedemo.security.session_cookie_inspector import SessionCookieInspector

LOG = logging.getLogger("saucedemo.steps.seguranca")
ADEQUATE_PASSWORD_AUTOCOMPLETE: Final = ("current-password", "new-password", "off")


@when("o visitante acessa o site pelo protocolo HTTP")
def visitor_accesses_over_http(browser_navigation: BrowserNavigation) -> None:
    browser_navigation.open_over_http()


@then("a página é servida via HTTPS")
def page_is_served_over_https(browser_navigation: BrowserNavigation) -> None:
    url = browser_navigation.url()
    assert url.startswith("https://"), f"URL após acessar via HTTP: '{url}'"


@then("os atributos Secure, HttpOnly e SameSite do cookie de sessão são verificados")
def session_cookie_attributes_are_checked(cookie_inspector: SessionCookieInspector) -> None:
    cookie = cookie_inspector.cookie(cookies.SESSION)
    assert cookie is not None, f"Cookie de sessão '{cookies.SESSION}' ausente"
    findings = []
    if not cookie.secure:
        findings.append(f"Cookie '{cookie.name}' sem o atributo Secure")
    if not cookie.http_only:
        findings.append(f"Cookie '{cookie.name}' sem o atributo HttpOnly")
    if cookie.same_site is None or cookie.same_site.lower() == "none":
        findings.append(f"Cookie '{cookie.name}' com SameSite {cookie.same_site or 'ausente'}")
    _report("Cookie de sessão", cookie.to_json(), findings)


@then("o atributo autocomplete do campo de senha é verificado")
def password_autocomplete_is_checked(login_page: LoginPage) -> None:
    autocomplete = login_page.password_field_autocomplete()
    findings = []
    if autocomplete is None or autocomplete.strip() not in ADEQUATE_PASSWORD_AUTOCOMPLETE:
        shown = "ausente" if autocomplete is None else f'"{autocomplete}"'
        findings.append(
            f"Campo de senha com autocomplete {shown} "
            f"(esperado: {', '.join(ADEQUATE_PASSWORD_AUTOCOMPLETE)})"
        )
    _report("Autocomplete do campo de senha", f"autocomplete={autocomplete}", findings)


@when("o visitante abre a página de login registrando os cabeçalhos da resposta")
def opens_login_page_capturing_headers(
    headers_inspector: SecurityHeadersInspector, scenario_context: ScenarioContext
) -> None:
    if not headers_inspector.is_supported():
        pytest.skip(
            "Cabeçalhos de segurança restritos a Chrome/Edge, como no projeto Java "
            f"(navegador atual: {headers_inspector.browser_name()})"
        )
    scenario_context.response_headers = headers_inspector.document_response_headers(paths.LOGIN)


@then("os cabeçalhos de segurança da resposta são verificados")
def security_headers_are_checked(scenario_context: ScenarioContext) -> None:
    headers = scenario_context.response_headers
    findings = []
    if "content-security-policy" not in headers:
        findings.append("Cabeçalho Content-Security-Policy ausente")
    if "x-frame-options" not in headers and "frame-ancestors" not in headers.get(
        "content-security-policy", ""
    ):
        findings.append(
            "Proteção contra clickjacking ausente (X-Frame-Options ou CSP frame-ancestors)"
        )
    if headers.get("x-content-type-options", "").strip().lower() != "nosniff":
        findings.append("Cabeçalho X-Content-Type-Options diferente de 'nosniff' ou ausente")
    if "strict-transport-security" not in headers:
        findings.append("Cabeçalho Strict-Transport-Security (HSTS) ausente")
    evidence = "\n".join(f"{name}: {value}" for name, value in headers.items())
    _report("Cabeçalhos de segurança", evidence, findings)


def _report(check: str, evidence: str, findings: list[str]) -> None:
    allure.attach(evidence, f"{check} - evidência", allure.attachment_type.TEXT)
    allure.attach(
        "\n".join(findings) if findings else "Nenhum achado",
        f"{check} - achados",
        allure.attachment_type.TEXT,
    )
    for finding in findings:
        LOG.warning("Achado de segurança [%s]: %s", check, finding)
    if settings.fail_on_security_findings():
        assert not findings, f"Achados de segurança - {check}: {findings}"
