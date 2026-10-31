from dataclasses import dataclass


@dataclass
class ScenarioContext:
    """Estado compartilhado entre os steps de um mesmo cenário.

    A fixture scenario_context cria uma instância nova por cenário, então nada vaza entre cenários.
    """

    _username: str | None = None

    @property
    def username(self) -> str:
        if self._username is None:
            raise RuntimeError("Nenhum usuário definido no cenário (passo 'Dado' ausente?)")
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value
