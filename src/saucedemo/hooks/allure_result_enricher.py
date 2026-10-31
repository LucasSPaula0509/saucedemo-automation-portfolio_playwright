"""Ajusta cada resultado logo antes de o Allure gravá-lo (equivalente ao TestLifecycleListener).

- Label Feature a partir da tag da funcionalidade (@login, @produtos...).
- Parâmetro "Navegador" e historyId por navegador, para que a mesma execução em Chrome e Firefox
  não apareça como retentativa no relatório consolidado do CI.
- Cenários @defeito recebem o link de issue mapeado em known_defects.py; quando falham, a
  mensagem ganha o prefixo [Defeito conhecido DEF-xxx], usado pela categoria "Defeitos
  conhecidos" do categories.json.
"""

from typing import Final

import allure_commons
from allure_commons.model2 import Label, Link, Parameter, StatusDetails, TestResult

from saucedemo.data.known_defects import KNOWN_DEFECTS

TAG_LABEL: Final = "tag"
FEATURE_LABEL: Final = "feature"
DEFECT_TAG: Final = "defeito"
FAILED_STATUSES: Final = {"failed", "broken"}
FEATURES: Final = {
    "login": "Login",
    "produtos": "Produtos",
    "carrinho": "Carrinho",
    "checkout": "Checkout",
    "performance": "Performance",
    "seguranca": "Segurança",
}


class AllureResultEnricher:
    def __init__(self, browser_name: str, issue_url_pattern: str) -> None:
        self.browser_name = browser_name
        self.issue_url_pattern = issue_url_pattern

    @allure_commons.hookimpl(tryfirst=True)
    def report_result(self, result: TestResult) -> None:
        tags = [label.value for label in result.labels if label.name == TAG_LABEL]
        feature = next((FEATURES[tag] for tag in tags if tag in FEATURES), None)
        if feature is not None:
            self._replace_feature(result, feature)
        self._separate_by_browser(result)
        if DEFECT_TAG in tags:
            defect_id = next((KNOWN_DEFECTS[tag] for tag in tags if tag in KNOWN_DEFECTS), None)
            self._mark_known_defect(result, defect_id)

    @staticmethod
    def _replace_feature(result: TestResult, feature: str) -> None:
        result.labels = [label for label in result.labels if label.name != FEATURE_LABEL]
        result.labels.append(Label(name=FEATURE_LABEL, value=feature))

    def _separate_by_browser(self, result: TestResult) -> None:
        result.parameters.append(Parameter(name="Navegador", value=self.browser_name))
        result.historyId = f"{result.historyId}:{self.browser_name}"

    def _mark_known_defect(self, result: TestResult, defect_id: str | None) -> None:
        if defect_id is not None:
            url = self.issue_url_pattern.format(defect_id)
            result.links.append(Link(type="issue", url=url, name=defect_id))
        if result.status not in FAILED_STATUSES:
            return
        details = result.statusDetails or StatusDetails()
        details.known = True
        details.message = f"[Defeito conhecido {defect_id or 'sem ID'}] {details.message or ''}"
        result.statusDetails = details
