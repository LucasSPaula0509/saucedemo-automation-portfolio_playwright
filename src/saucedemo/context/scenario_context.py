from dataclasses import dataclass

from saucedemo.performance.navigation_metrics import NavigationMetrics


@dataclass
class ScenarioContext:
    """Estado compartilhado entre os steps de um mesmo cenário (equivalente aos ScenarioContext,
    PerformanceContext e SecurityContext do Java).

    A fixture scenario_context cria uma instância nova por cenário, então nada vaza entre cenários.
    """

    _username: str | None = None
    _navigation: NavigationMetrics | None = None
    _login_to_inventory_ms: int | None = None
    _response_headers: dict[str, str] | None = None

    @property
    def username(self) -> str:
        if self._username is None:
            raise RuntimeError("Nenhum usuário definido no cenário (passo 'Dado' ausente?)")
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @property
    def navigation(self) -> NavigationMetrics:
        """Medições feitas no passo "Quando" e validadas nos passos "Então"."""
        if self._navigation is None:
            raise RuntimeError("Nenhuma métrica de navegação coletada no cenário")
        return self._navigation

    @navigation.setter
    def navigation(self, value: NavigationMetrics) -> None:
        self._navigation = value

    @property
    def login_to_inventory_ms(self) -> int:
        if self._login_to_inventory_ms is None:
            raise RuntimeError("O tempo do login até a página de produtos não foi medido")
        return self._login_to_inventory_ms

    @login_to_inventory_ms.setter
    def login_to_inventory_ms(self, value: int) -> None:
        self._login_to_inventory_ms = value

    @property
    def response_headers(self) -> dict[str, str]:
        """Cabeçalhos capturados no passo "Quando" e avaliados no passo "Então"."""
        if self._response_headers is None:
            raise RuntimeError("Nenhum cabeçalho de resposta capturado no cenário")
        return self._response_headers

    @response_headers.setter
    def response_headers(self, value: dict[str, str]) -> None:
        self._response_headers = value
