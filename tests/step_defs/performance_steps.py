import json
import time

import allure
from playwright.sync_api import expect
from pytest_bdd import then, when

from saucedemo.context.scenario_context import ScenarioContext
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.products_page import ProductsPage
from saucedemo.performance import performance_limits
from saucedemo.performance.navigation_metrics_collector import NavigationMetricsCollector
from step_defs.step_text import step


@when("o visitante abre a página de login medindo o carregamento")
def opens_login_page_measuring(
    login_page: LoginPage,
    metrics_collector: NavigationMetricsCollector,
    scenario_context: ScenarioContext,
) -> None:
    login_page.open()
    metrics = metrics_collector.collect()
    scenario_context.navigation = metrics
    allure.attach(metrics.to_json(), "Métricas de navegação - login", allure.attachment_type.JSON)


@when(
    step(
        'ele se autentica com a senha "{password:string}" medindo o tempo até a página de produtos'
    )
)
def logs_in_measuring_time_to_products(
    login_page: LoginPage,
    products_page: ProductsPage,
    scenario_context: ScenarioContext,
    password: str,
) -> None:
    """Tempo percebido do clique em Login até a lista de produtos visível, medido pelo teste
    (inclui a latência do Playwright, por isso o limite é folgado).
    """
    start = time.perf_counter()
    login_page.login(scenario_context.username, password)
    expect(products_page.marker(), "Página de produtos exibida").to_be_visible()
    elapsed_ms = round((time.perf_counter() - start) * 1000)
    scenario_context.login_to_inventory_ms = elapsed_ms
    allure.attach(
        json.dumps(
            {
                "usuario": scenario_context.username,
                "tempoMs": elapsed_ms,
                "limiteMs": performance_limits.login_to_inventory_ms(),
                "paginaDeProdutosExibida": True,
            },
            indent=2,
        ),
        "Tempo do login até a página de produtos",
        allure.attachment_type.JSON,
    )


@then("a página de login carrega dentro do limite configurado")
def login_page_loads_within_limit(scenario_context: ScenarioContext) -> None:
    load_ms = scenario_context.navigation.load_ms
    limit_ms = performance_limits.login_page_load_ms()
    assert load_ms <= limit_ms, f"Carregamento da página de login (ms): {load_ms} > {limit_ms}"


@then("o Largest Contentful Paint fica dentro do limite configurado")
def largest_contentful_paint_within_limit(scenario_context: ScenarioContext) -> None:
    lcp_ms = scenario_context.navigation.lcp_ms
    limit_ms = performance_limits.largest_contentful_paint_ms()
    assert lcp_ms is not None, "Largest Contentful Paint (ms): indisponível no navegador"
    assert lcp_ms <= limit_ms, f"Largest Contentful Paint (ms): {lcp_ms} > {limit_ms}"


@then("o tempo até a página de produtos fica dentro do limite configurado")
def time_to_products_within_limit(scenario_context: ScenarioContext) -> None:
    elapsed_ms = scenario_context.login_to_inventory_ms
    limit_ms = performance_limits.login_to_inventory_ms()
    assert elapsed_ms <= limit_ms, (
        f"Tempo do login até a página de produtos (ms): {elapsed_ms} > {limit_ms}"
    )


@then("o tempo até a página de produtos é sinalizado como acima do limite configurado")
def time_to_products_flagged_as_slow(scenario_context: ScenarioContext) -> None:
    elapsed_ms = scenario_context.login_to_inventory_ms
    limit_ms = performance_limits.login_to_inventory_ms()
    assert elapsed_ms > limit_ms, (
        "Tempo do login até a página de produtos (ms, usuário com lentidão): "
        f"{elapsed_ms} <= {limit_ms}"
    )
