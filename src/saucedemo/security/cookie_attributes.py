import json
from dataclasses import dataclass


@dataclass(frozen=True)
class CookieAttributes:
    """Atributos de proteção de um cookie, como o navegador os enxerga."""

    name: str
    secure: bool
    http_only: bool
    same_site: str | None

    def to_json(self) -> str:
        return json.dumps(
            {
                "nome": self.name,
                "secure": self.secure,
                "httpOnly": self.http_only,
                "sameSite": self.same_site,
            },
            indent=2,
        )
