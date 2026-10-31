from typing import Final

from saucedemo.pages.base_page import BasePage
from saucedemo.performance.navigation_metrics import NavigationMetrics

# Retorna null até o evento load terminar; o wait_for_function repete o script até ter valor.
NAVIGATION_TIMING: Final = """() => {
  const nav = performance.getEntriesByType('navigation')[0];
  if (!nav || nav.loadEventEnd === 0) {
    return null;
  }
  return {
    url: nav.name,
    ttfb: nav.responseStart - nav.startTime,
    domContentLoaded: nav.domContentLoadedEventEnd - nav.startTime,
    load: nav.loadEventEnd - nav.startTime
  };
}"""

# LCP só é exposto via PerformanceObserver; buffered: true entrega as entradas já registradas.
# Sem suporte (ou sem entrada em 1 s), devolve null.
LARGEST_CONTENTFUL_PAINT: Final = """() => new Promise(done => {
  try {
    new PerformanceObserver(list => {
      const entries = list.getEntries();
      done(entries[entries.length - 1].startTime);
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (unsupported) {
    done(null);
    return;
  }
  setTimeout(() => done(null), 1000);
})"""


class NavigationMetricsCollector(BasePage):
    """Lê as métricas da navegação atual direto do navegador (window.performance), sem gerar
    requisições extras ao site.
    """

    def collect(self) -> NavigationMetrics:
        nav = self.page.wait_for_function(NAVIGATION_TIMING).json_value()
        lcp = self._evaluate(LARGEST_CONTENTFUL_PAINT)
        return NavigationMetrics(
            url=str(nav["url"]),
            time_to_first_byte_ms=float(nav["ttfb"]),
            dom_content_loaded_ms=float(nav["domContentLoaded"]),
            load_ms=float(nav["load"]),
            lcp_ms=None if lcp is None else float(lcp),
        )
