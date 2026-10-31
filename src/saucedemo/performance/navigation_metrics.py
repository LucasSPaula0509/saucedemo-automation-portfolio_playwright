import json
from dataclasses import dataclass


@dataclass(frozen=True)
class NavigationMetrics:
    """Métricas de uma navegação completa (Navigation Timing Level 2 + Largest Contentful Paint),
    em milissegundos a partir do início da navegação. lcp_ms é None quando o navegador não expõe
    LCP.
    """

    url: str
    time_to_first_byte_ms: float
    dom_content_loaded_ms: float
    load_ms: float
    lcp_ms: float | None

    def to_json(self) -> str:
        return json.dumps(
            {
                "url": self.url,
                "timeToFirstByteMs": round(self.time_to_first_byte_ms, 1),
                "domContentLoadedMs": round(self.dom_content_loaded_ms, 1),
                "loadMs": round(self.load_ms, 1),
                "largestContentfulPaintMs": None if self.lcp_ms is None else round(self.lcp_ms, 1),
            },
            indent=2,
        )
