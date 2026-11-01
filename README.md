# Swag Labs — Automação de testes front-end com Python + Playwright

[![Testes E2E](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright/actions/workflows/tests.yml)
[![Lint](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright/actions/workflows/lint.yml/badge.svg)](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright/actions/workflows/lint.yml)
[![Performance e Segurança](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright/actions/workflows/security-performance.yml/badge.svg)](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright/actions/workflows/security-performance.yml)
[![Allure Report](https://img.shields.io/badge/Allure-Report-orange)](https://lucasspaula0509.github.io/saucedemo-automation-portfolio_playwright/)

**Allure Report da última execução da `main`:** <https://lucasspaula0509.github.io/saucedemo-automation-portfolio_playwright/>

---

## 1. O que é este projeto

Framework de testes automatizados para o front-end da loja de demonstração **Swag Labs**, em <https://www.saucedemo.com>.

Esta é a **versão Python + Playwright** do projeto [saucedemo-automation-portfolio_java](https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_java) (Java + Selenium). O projeto Java continua existindo e é a referência; também existe uma versão [Cypress](https://github.com/LucasSPaula0509/saucedemo-automation-portifolio_cypress). Os três coexistem: mesmos cenários, mesmas regras, mesmos relatórios e o mesmo CI/CD. Muda só a tecnologia.

Os cenários são escritos em português, no formato BDD (Gherkin), e ficam nos arquivos `.feature`, que são **idênticos** aos do projeto Java. Cada passo é executado em um navegador real pelo Playwright. O resultado é publicado em um relatório Allure.

| Funcionalidade    | Arquivo                                       | Cenários          |
| ----------------- | --------------------------------------------- | ----------------- |
| Login             | `features/login.feature`                      | 9 (CT001–CT009)   |
| Produtos          | `features/produtos.feature`                   | 10 (CT001–CT010)  |
| Carrinho          | `features/carrinho.feature`                   | 13 (CT001–CT013)  |
| Checkout          | `features/checkout.feature`                   | 11 (CT001–CT011)  |
| Performance       | `features/nao_funcionais/performance.feature` | 3                 |
| Segurança passiva | `features/nao_funcionais/seguranca.feature`   | 4                 |

Os cenários usam esta stack:

| Componente          | Ferramenta                                                    |
| ------------------- | ------------------------------------------------------------- |
| Linguagem           | Python 3.14, com type hints                                   |
| Pacotes             | `venv` + `requirements.txt` com versões fixadas               |
| Navegador           | Playwright para Python (API síncrona)                         |
| BDD                 | `pytest` + `pytest-bdd` + `pytest-playwright`                 |
| Asserções           | `expect` do Playwright (com retry) e `assert` do Python       |
| Relatório           | Allure 2 (`allure-pytest-bdd` + Allure CLI)                   |
| Logs                | módulo `logging`                                              |
| Qualidade de código | Ruff (lint e formatação)                                      |
| CI                  | GitHub Actions; Jenkinsfile opcional                          |
| Performance         | Navigation Timing e LCP; Lighthouse CI                        |
| Segurança           | Verificações passivas e OWASP ZAP Baseline                    |

---

## 2. Pré-requisitos

| Ferramenta                         | Para quê                                          | Como instalar                                                                                                                                                                       |
| ---------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python 3.14**                    | rodar os testes (versão em `.python-version`)     | <https://www.python.org/downloads/> ou `winget install Python.Python.3.14` (Windows)                                                                                               |
| **Google Chrome** e/ou **Firefox** | executar os cenários                              | o Chrome e o Edge usam o navegador instalado na máquina; o Firefox vem do Playwright (`playwright install firefox`)                                                                 |
| **Allure CLI 2.46.1**              | abrir o relatório                                 | baixe o zip em <https://github.com/allure-framework/allure2/releases/tag/2.46.1>, descompacte e coloque a pasta `bin` no `PATH`. Precisa de **Java 8+** (JRE ou JDK) instalado. |
| **Git**                            | clonar o repositório                              | <https://git-scm.com/>                                                                                                                                                              |

```bash
git clone https://github.com/LucasSPaula0509/saucedemo-automation-portfolio_playwright.git
cd saucedemo-automation-portfolio_playwright
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install --with-deps chromium firefox
```

> No Windows, o `--with-deps` não é necessário (ele instala bibliotecas do sistema no Linux).

---

## 3. Como rodar

Com o `venv` ativado:

```bash
pytest                                               # tudo, exceto @defeito e @performance (Chrome)
pytest -m smoke                                      # só o smoke
pytest -m "login and negativo"                       # combinação de tags
pytest --browser firefox                             # outro navegador
pytest --browser chromium --browser-channel msedge   # Edge
pytest --headed                                      # com a janela do navegador
pytest -m defeito                                    # defeitos conhecidos (devem falhar)
pytest -m "performance or seguranca"                 # não funcionais
ruff check . && ruff format --check .                # lint e formatação
allure serve allure-results                          # abre o Allure no navegador
```

- As tags do Gherkin viram **markers** do pytest, sem o `@` (`@smoke` → `-m smoke`).
- O filtro padrão (`not defeito and not performance`) está no `addopts` do `pyproject.toml`. Um `-m` na linha de comando **substitui** esse filtro.
- Sem `--browser`, os testes rodam no **Chrome** instalado na máquina (o navegador padrão do projeto Java).
- Os testes rodam sem janela (headless). Use `--headed` para ver o navegador.
- Cada execução apaga os resultados anteriores do Allure (`--clean-alluredir`), como o `mvn clean test` do projeto Java.

### Abrindo o relatório Allure

- `allure serve allure-results` gera o relatório e abre no navegador.
- `allure generate allure-results --clean -o allure-report` gera o HTML em `allure-report/`; `allure open allure-report` abre esse relatório por um servidor local.
- Também há o relatório do Cucumber em `reports/cucumber.json` e o screenshot de cada falha em `test-results/`.

### Configurações

Os valores padrão ficam em [`pyproject.toml`](pyproject.toml), na tabela `[tool.saucedemo]` (equivalente ao `config.properties` do Java). Cada chave pode ser sobrescrita por variável de ambiente, com o nome em maiúsculas e `_` no lugar de `.` (ex.: `TIMEOUT_SECONDS=20`). O arquivo [`.env.example`](.env.example) lista todas; ele é só documentação, e o projeto não carrega `.env` automaticamente.

| Chave                            | Padrão                      | Descrição                                                                    |
| -------------------------------- | --------------------------- | ---------------------------------------------------------------------------- |
| `base.url`                       | `https://www.saucedemo.com` | URL do site (também aceita `--base-url`)                                     |
| navegador                        | Chrome                      | `--browser firefox`, `--browser chromium --browser-channel msedge` (Edge)    |
| headless                         | sim                         | `--headed` abre a janela                                                     |
| `timeout.seconds`                | `10`                        | tempo máximo de cada espera automática e de cada `expect`                    |
| `window.width` / `window.height` | `1920` / `1080`             | tamanho da tela (viewport)                                                   |
| `screenshot.every.step`          | `false`                     | `true` anexa screenshot de todos os passos (padrão: só do passo que falhou) |
| `perf.login.page.max.ms`         | `3000`                      | limite de carregamento da página de login                                    |
| `perf.login.to.inventory.max.ms` | `2000`                      | limite do login até a página de produtos                                     |
| `perf.lcp.max.ms`                | `2500`                      | limite do Largest Contentful Paint                                           |
| `security.fail.on.findings`      | `false`                     | `true` faz achados de segurança reprovarem o cenário                         |

**Execução sequencial:** um cenário por vez, localmente e no CI. Não há paralelismo.

---

## 4. Estrutura do projeto

```text
├── .github/workflows/
│   ├── tests.yml                  # smoke → regressão (chrome, depois firefox) → defeitos → Allure no Pages
│   ├── lint.yml                   # actionlint + Ruff
│   └── security-performance.yml   # @performance, Lighthouse, @seguranca, ZAP (agendado/manual)
├── Jenkinsfile                    # pipeline opcional equivalente
├── features/                      # login, produtos, carrinho, checkout (+ nao_funcionais/)
├── src/saucedemo/
│   ├── config/        # settings.py: leitura do [tool.saucedemo] (variável de ambiente > arquivo)
│   ├── ui/            # SELETORES: só constantes Final[str] e funções que montam seletores
│   ├── pages/         # PAGE OBJECTS: ações e leitura de estado, sem asserções
│   │   └── base_page.py           # helpers de ação e leitura (espera automática do Playwright)
│   ├── data/          # constantes: usuários, senhas, produtos, caminhos, títulos, defeitos
│   ├── context/       # ScenarioContext: estado do cenário (dataclass)
│   ├── utils/         # slug de produto, dinheiro (Decimal), cálculo do pedido
│   ├── hooks/         # Allure: enriquecimento do resultado, ambiente, categorias, evidências
│   ├── performance/   # coletor de métricas de navegação e limites
│   └── security/      # leitura de cookies e cabeçalhos (somente leitura)
├── tests/
│   ├── conftest.py    # fixtures (navegador, pages, contexto), hooks do pytest/pytest-bdd
│   ├── step_defs/     # STEP DEFINITIONS em português: orquestram páginas e fazem as asserções
│   └── test_*.py      # liga cada .feature ao pytest com scenarios(...)
├── allure/categories.json         # categorias do Allure (copiado para allure-results)
├── lighthouserc.json              # configuração do Lighthouse CI
├── zap/rules.tsv                  # severidade das regras do ZAP Baseline
├── pyproject.toml                 # pytest (filtro, markers, Allure), Ruff e [tool.saucedemo]
├── requirements.txt               # dependências com versões fixadas
├── .python-version
└── .env.example
```

### Fluxo de um passo: feature → step → page → ui

Exemplo do cenário `@CT001_Login`:

```gherkin
# features/login.feature
Quando ele se autentica com a senha "secret_sauce"
```

```python
# tests/step_defs/login_steps.py: liga o texto do Gherkin ao código
@when(step('ele se autentica com a senha "{password:string}"'))
def authenticates_with_password(
    scenario_context: ScenarioContext, login_page: LoginPage, password: str
) -> None:
    login_page.login(scenario_context.username, password)
```

```python
# src/saucedemo/pages/login_page.py: ações da página (o Playwright espera o elemento)
def login(self, username: str, password: str) -> None:
    self._type(login_ui.USERNAME, username)
    self._type(login_ui.PASSWORD, password)
    self._click(login_ui.LOGIN_BUTTON)
```

```python
# src/saucedemo/ui/login_ui.py: onde o elemento está na tela
USERNAME: Final = data_test.of("username")  # [data-test='username']
PASSWORD: Final = data_test.of("password")
LOGIN_BUTTON: Final = data_test.of("login-button")
```

A validação fica no step do `Então`:

```python
# tests/step_defs/common_steps.py
@then("a página de produtos é exibida")
def products_page_is_displayed(products_page: ProductsPage, header: HeaderComponent) -> None:
    expect_loaded(products_page, "Página de produtos carregada")
    expect_text(header.page_title(), "Título da página", page_titles.PRODUCTS)
```

As pages e o contexto do cenário chegam aos steps como **fixtures** do pytest (definidas no `conftest.py`), criadas de novo a cada cenário.

---

## 5. Como criar um novo cenário

Exemplo: verificar que o carrinho mostra a quantidade de um produto.

1. **Escreva o cenário** no `.feature` da funcionalidade. Use o próximo ID livre e as tags adequadas:
   ```gherkin
   @CT014_Carrinho @regressivo @positivo
   Cenário: Quantidade do produto no carrinho
     Dado que o carrinho do usuário "standard_user" contém o produto "Sauce Labs Onesie"
     Quando ele acessa o carrinho
     Então a quantidade do produto "Sauce Labs Onesie" é "1"
   ```
2. **Registre o marker do novo ID** em `markers` no `pyproject.toml` (`"CT014_Carrinho: ID de rastreabilidade"`). Com `--strict-markers`, uma tag sem registro é erro, o que pega erros de digitação.
3. **Rode só esse cenário** com `pytest -m CT014_Carrinho`. O pytest-bdd avisa qual passo não tem definição (`StepDefinitionNotFoundError`).
4. **Reaproveite passos existentes** sempre que possível. Busque o texto em `tests/step_defs/`.
5. **Seletor:** se o elemento ainda não estiver mapeado, inspecione a página (F12) e adicione no módulo `ui/` da tela. Use `[data-test='...']` sempre que existir:
   ```python
   ITEM_QUANTITIES: Final = data_test.of("item-quantity")
   ```
6. **Page Object:** crie um método de ação ou de leitura em `pages/`, usando os helpers da `BasePage` (`_click`, `_type`, `_text_of`, `_texts_of`, `_locator`...). Não use `page.locator` com seletor escrito na page e não faça asserção aqui.
7. **Step:** implemente o passo em `tests/step_defs/` com `step('... "{valor:string}"')` (aceita valor vazio, como o `{string}` do Cucumber), recebendo as pages como fixtures e validando com `expect(...)` ou `assert` com mensagem.
8. **Rode de novo**, depois rode a regressão (`pytest`) e confira o código com `ruff check . && ruff format --check .`.

---

## 6. Convenções do projeto

- **Seletores só em `ui/`**, como constantes `Final[str]`. A ordem de preferência é `data-test` → `id` → `name` → CSS → XPath.
- **Nada de** `time.sleep`, `page.wait_for_timeout` ou qualquer espera fixa.
- **Esperas só as automáticas do Playwright** e as asserções com retry do `expect`. Ausência de elemento é validada com `expect(locator).to_have_count(0)`.
- **Pages** recebem o `Page` e têm só ações e leitura de estado, **sem asserções** e sem dados fixos.
- **Steps** só orquestram pages e fazem as **asserções**. Sem `page.locator`, seletores ou esperas. Tabelas e resumos são comparados **inteiros** (`assert atual == esperado`), para mostrar todas as diferenças de uma vez.
- **Estado do cenário na fixture `scenario_context`** (dataclass, escopo de função). Nada de estado global entre cenários.
- **Cenários independentes.** Cada um usa um `BrowserContext` novo (sem cookies nem storage) e monta as próprias pré-condições pela interface.
- **Type hints** em todas as funções (regras `ANN` do Ruff).
- **Não mude um resultado esperado só para o teste passar.** Se o site se comportar diferente, o teste deve falhar e a divergência deve ser reportada (veja [Defeitos conhecidos](#10-defeitos-conhecidos)).
- **Qualidade de código:** `ruff check .` e `ruff format --check .` (use `ruff format .` para formatar).

---

## 7. Tags (markers)

| Tag                                                                          | Significado                                                        |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `@login`, `@produtos`, `@carrinho`, `@checkout`                              | funcionalidade (vira **Feature** no Allure)                        |
| `@CTnnn_<Funcionalidade>`                                                    | ID de rastreabilidade do cenário (ex.: `@CT001_Login`)             |
| `@regressivo`                                                                | faz parte da regressão funcional                                   |
| `@smoke`                                                                     | caminho crítico, rápido; roda primeiro no CI                       |
| `@positivo` / `@negativo`                                                    | fluxo feliz / validação de erro                                    |
| `@ordenacao`, `@detalhe`, `@menu`, `@calculo`, `@cancelamento`, `@validacao` | agrupamentos por assunto                                           |
| `@seguranca`                                                                 | verificação de segurança (funcional no login ou passiva)           |
| `@passivo`                                                                   | verificação de segurança somente leitura (`seguranca.feature`)     |
| `@performance`                                                               | performance percebida; **fora** do filtro padrão                   |
| `@defeito`                                                                   | defeito conhecido; **fora** do filtro padrão, com job próprio no CI |

Todas as tags estão registradas como markers no `pyproject.toml`. O filtro padrão, no `addopts`, é `-m "not defeito and not performance"`.

---

## 8. CI/CD

### `tests.yml`: a cada push/PR na `main`, todo dia às 09:00 (BRT) e sob demanda

```text
smoke (chrome) ──► regressão (chrome) ──► regressão (firefox) ──► defeitos conhecidos ──► Allure Report ──► GitHub Pages (só na main)
```

Tudo roda **em sequência**: um job por vez (encadeados com `needs`), um navegador por vez na matriz (`max-parallel: 1`) e um cenário por vez. Não há `pytest-xdist` nem divisão dos testes.

| Job               | O que faz                                                                                                                                                                                                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **smoke**         | `smoke and not defeito` no Chrome headless. Se falhar, a regressão nem começa.                                                                                                                                                                                                                     |
| **regression**    | `not defeito and not performance` em matriz **Chrome** e depois **Firefox**                                                                                                                                                                                                                        |
| **known-defects** | só `defeito`, com `continue-on-error`. Roda mesmo se a regressão falhar. Deve ficar vermelho enquanto os defeitos existirem; quando ficar verde, o defeito foi corrigido.                                                                                                                         |
| **report**        | roda sempre (`if: always()`): junta os `allure-results` de todos os jobs, recupera o histórico (tendência) do relatório anterior, gera o Allure e publica em <https://lucasspaula0509.github.io/saucedemo-automation-portfolio_playwright/>. Em PR, o relatório fica só como artifact. |

- Cada job instala com `playwright install --with-deps` **só o navegador que usa**.
- **Execução manual:** em _Actions → Testes E2E → Run workflow_, escolha o `browser` e as `tags` (expressão de markers, ex.: `smoke and positivo`).
- **Artifacts** (sempre enviados, mesmo com falha): `allure-results-*`, `evidencias-*` (`reports/cucumber.json` e screenshots de falha em `test-results/`) e `allure-report`.

### `lint.yml`: a cada push/PR

- `actionlint` valida os workflows.
- `ruff check` e `ruff format --check` validam o código Python.

### `security-performance.yml`: só agendado (segunda, 10:00 BRT) ou manual

- Performance (`@performance`), Lighthouse CI, segurança passiva (`@seguranca`) e OWASP ZAP Baseline. Detalhes na próxima seção.

### Jenkins (opcional)

O [`Jenkinsfile`](Jenkinsfile) tem os estágios Instalar → Smoke → Regressão → Defeitos conhecidos e publica com o plugin Allure Jenkins. Cada estágio grava em uma pasta própria de `allure-results`. O estágio de defeitos marca o build como _UNSTABLE_, sem quebrá-lo. Para usar, tenha Python 3.14, os navegadores e um Java no agente e configure a ferramenta Allure.

---

## 9. Performance e segurança

O saucedemo é um **site público de terceiros**, e não temos autorização do dono para testes agressivos. Por isso:

- **Não há teste de carga ou stress** (JMeter, k6, Gatling, Locust). Muitos usuários virtuais seriam, na prática, um ataque de negação de serviço.
- **Não há scan ativo, fuzzing, força bruta ou injeção.** Só verificações **passivas**: ler o que o navegador já recebe numa navegação normal.

### Performance (`@performance`)

Cada cenário faz **uma única navegação**:

| Cenário                                           | Métrica                                                                        | Limite (configurável) |
| ------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------- |
| Carregamento da página de login                   | `loadEventEnd` (Navigation Timing) e **LCP** (`PerformanceObserver`)           | 3000 ms / 2500 ms     |
| Login do `standard_user` até a página de produtos | tempo do clique até a lista visível                                            | 2000 ms               |
| Login do `performance_glitch_user`                | o mesmo tempo, que **deve ficar acima** do limite (o usuário simula lentidão) | 2000 ms               |

As métricas são lidas de `window.performance` com `page.evaluate` (os mesmos scripts do projeto Java) e anexadas ao Allure em JSON.

O tempo do login é medido pelo próprio teste e inclui a latência do Playwright, por isso o limite é folgado.

**Lighthouse CI** ([`lighthouserc.json`](lighthouserc.json), o mesmo do projeto Java):

- faz 3 execuções na página de login (perfil desktop) e usa a execução mediana;
- exige performance ≥ 0.8, acessibilidade ≥ 0.9 e boas práticas ≥ 0.9;
- publica o relatório como artifact `lighthouse-report`.

Para rodar o Lighthouse localmente: `npx @lhci/cli autorun` (precisa de Node.js).

**Achado conhecido (o mesmo do projeto Java):** a nota de boas práticas fica abaixo do mínimo de 0.9 (0.81 no projeto Java e 0.78 no projeto Cypress, em 31/10/2026), porque o site usa _unload event listeners_, descontinuados no Chrome. Por isso o job **Lighthouse CI** fica vermelho. Isso é um achado do site, e o limite não foi reduzido.

### Segurança

| Verificação                                                      | Onde                                                                                                                       | Cobre                                             | **Não** cobre                                              |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------- |
| Senha mascarada, acesso direto sem login, sessão após logout     | `login.feature` (`@seguranca`)                                                                                             | controles de acesso visíveis ao usuário           | autorização no servidor, APIs                              |
| HTTP redireciona para HTTPS                                      | `seguranca.feature`                                                                                                        | redirecionamento do domínio principal             | versões/cifras de TLS, certificados                        |
| Atributos do cookie de sessão (`Secure`, `HttpOnly`, `SameSite`) | `seguranca.feature` (`context.cookies()`)                                                                                  | o cookie `session-username` visto pelo navegador  | outros cookies, roubo ou fixação de sessão                 |
| `autocomplete` do campo de senha                                 | `seguranca.feature`                                                                                                        | se o atributo existe e tem valor adequado         | política de senha do servidor                              |
| Cabeçalhos CSP, X-Frame-Options, X-Content-Type-Options e HSTS   | `seguranca.feature` (resposta da própria navegação, `page.goto`; só Chrome/Edge, no Firefox o cenário é pulado)          | a resposta do documento principal                 | conteúdo da CSP, cabeçalhos de outros recursos             |
| **OWASP ZAP Baseline** (`zap/rules.tsv`, o mesmo do projeto Java) | `security-performance.yml`                                                                                                 | spider de 1 minuto e regras **passivas** do ZAP   | qualquer regra ativa (XSS, SQLi etc.), áreas autenticadas |

- **Achados não reprovam os testes por padrão.** Eles vão para o Allure (anexos "achados" e "evidência") e para o log como `WARNING`. Com `SECURITY_FAIL_ON_FINDINGS=true`, cada achado reprova o cenário.
- O ZAP roda com `fail_action: false` e não abre issues. O relatório HTML fica no artifact `zap-report`.
- **Achados atuais** (os mesmos do projeto Java):
  - o cookie de sessão não tem `Secure` nem `HttpOnly` (o Firefox reporta `SameSite=None`);
  - o campo de senha não tem `autocomplete`;
  - a página de login não envia CSP, X-Frame-Options, X-Content-Type-Options nem HSTS.

---

## 10. Defeitos conhecidos

Cenários marcados com `@defeito` **continuam falhando enquanto o defeito existir**. O resultado esperado do cenário não é alterado. Eles ficam fora da regressão padrão e rodam no job `known-defects`.

No Allure, aparecem na categoria **"Defeitos conhecidos"**, com o link do ID configurado em [`known_defects.py`](src/saucedemo/data/known_defects.py).

| ID      | Cenário                                                           | Comportamento esperado                    | Comportamento observado                                                | Observado em |
| ------- | ----------------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------- | ------------ |
| DEF-001 | `@CT013_Carrinho` Reset App State restaura os botões dos produtos | botões voltam para "Add to cart"          | o contador some, mas o botão continua "Remove" até recarregar a página | 30/10/2026   |
| DEF-002 | `@CT011_Checkout` Checkout bloqueado com carrinho vazio           | o checkout não é iniciado                 | o site vai para `/checkout-step-one.html` com o carrinho vazio         | 30/10/2026   |
| DEF-003 | `@CT009_Produtos` Opções disponíveis no menu lateral              | All Items, About, Logout, Reset App State | aparece também **"Dynamic Catalog"**                                   | 31/10/2026   |

Quando um defeito for corrigido:

1. o job `known-defects` passa a mostrar o cenário como aprovado;
2. remova a tag `@defeito` do cenário e a linha do `known_defects.py` (e faça o mesmo nos projetos Java e Cypress, para os três continuarem iguais).

---

## 11. Decisões técnicas

### Mapeamento Java → Python + Playwright

| Projeto Java                                                       | Projeto Python + Playwright                                                                       | Observação                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Java 21 + Maven Wrapper                                            | Python 3.14 + `venv` + `requirements.txt` fixado + `.python-version`                              |                                                                              |
| Selenium WebDriver 4                                               | Playwright (API síncrona)                                                                         |                                                                              |
| Cucumber 7 + JUnit Platform + `TestRunner`                         | `pytest` + `pytest-bdd` + `tests/test_*.py` com `scenarios(...)`                                  | Gherkin em português lido sem alteração                                      |
| `{string}` do Cucumber                                             | tipo `string` no `parsers.parse` (`step_text.py`)                                                 | o parse padrão não aceita valor vazio                                        |
| AssertJ + SoftAssertions                                           | `expect` com retry; listas e resumos comparados inteiros com `assert ==`                         |                                                                              |
| PicoContainer + `ScenarioContext`/`PerformanceContext`/`SecurityContext` | fixture `scenario_context` (dataclass) e pages como fixtures                                | uma instância nova por cenário                                               |
| `DriverManager` (ThreadLocal) + execução paralela                  | execução sequencial                                                                               | paralelismo fora do escopo                                                   |
| `DriverFactory` (Chrome/Firefox/Edge, modo anônimo)                | fixtures do pytest-playwright; Chrome e Edge pelo `--browser-channel`; `BrowserContext` novo por cenário | o contexto novo equivale à janela anônima                              |
| `config.properties` + `ConfigReader` + `Environment`               | `[tool.saucedemo]` no `pyproject.toml` + variáveis de ambiente (`config/settings.py`)            | mesmas chaves e valores                                                      |
| `junit-platform.properties` (filtro de tags)                       | `addopts` + `markers` + `--strict-markers` no `pyproject.toml`                                    |                                                                              |
| `ui/*Ui.java` (`By`)                                               | `ui/*_ui.py` (`Final[str]`)                                                                       | mesmos seletores; o XPath do título do produto foi mantido                   |
| `BasePage` com `WebDriverWait`                                     | `base_page.py` com a espera automática do Playwright                                             |                                                                              |
| `isLoaded()` booleano                                              | `marker()` + `path`, validados no step (`expect_loaded`)                                          | as pages não fazem asserção                                                  |
| `Money`/`OrderTotals` (`BigDecimal`, HALF_UP)                      | `utils/money.py`/`order_totals.py` com `Decimal` e `ROUND_HALF_UP`                                |                                                                              |
| `Hooks` e `Evidence`                                               | hooks `pytest_bdd_step_error` e `pytest_bdd_after_step` no `conftest.py`                          | console com `page.on("console")`, em todos os navegadores                    |
| `AllureResultEnricher` (SPI `TestLifecycleListener`)               | `hooks/allure_result_enricher.py` (hook `report_result` do `allure_commons`)                     | mesmas regras                                                                |
| `known-defects.properties`                                         | `data/known_defects.py`                                                                           | mesmos IDs                                                                   |
| `allure.properties` (padrões de link)                              | `--allure-link-pattern` no `addopts`                                                              | mesmas URLs                                                                  |
| `AllureEnvironment`                                                | `hooks/allure_files.py`                                                                           | "Java" vira "Python"                                                         |
| `categories.json` (copiado pelo Maven)                             | `allure/categories.json` (copiado no fim da sessão)                                              | arquivo idêntico                                                             |
| SLF4J + Logback                                                    | `logging` com `log_cli` no mesmo formato                                                          |                                                                              |
| CDP (`Network.responseReceived`) para cabeçalhos                   | resposta do `page.goto` (`response.all_headers()`)                                                | sem requisição extra                                                         |
| `System.nanoTime` no login                                         | `time.perf_counter`                                                                               |                                                                              |
| `JavascriptExecutor` (Navigation Timing e LCP)                     | `page.wait_for_function` / `page.evaluate` com os mesmos scripts                                  |                                                                              |
| Spotless (google-java-format)                                      | Ruff (`check` + `format`)                                                                         |                                                                              |
| `setup-java` + cache Maven                                         | `setup-python` + cache pip + `playwright install --with-deps`                                     |                                                                              |
| Allure CLI baixado pelo `allure-maven`                             | Allure CLI 2.46.1 (mesma versão), release oficial                                                 |                                                                              |
| `lighthouserc.json`, `zap/rules.tsv`, `categories.json`, `.feature` | copiados sem alteração                                                                           | conferidos por sha256                                                        |

### Outras decisões

| Decisão                                                                                  | Motivo                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python 3.14                                                                              | a versão estável mais recente que todas as dependências suportam (o Playwright declara suporte até a 3.14)                                                                                       |
| Prova de conceito antes do projeto                                                       | confirmou que o `pytest-bdd` lê o `# language: pt` sem alterar as features, que todas as tags viram markers válidos e que um `-m` na linha de comando substitui o do `addopts`                   |
| Tipo `string` próprio nos steps (com `parse.with_pattern`, do pacote `parse`, dependência do `pytest-bdd`) | o `parsers.parse` e o `cfparse` não casam com `""`, usado nos Exemplos com células vazias                                                                             |
| Todas as 68 tags registradas como markers (inclusive os 50 IDs `@CTnnn`)                 | exigido pelo `--strict-markers`; cada cenário novo precisa registrar o seu ID                                                                                                                     |
| Chrome como canal padrão por fixture (`browser_channel`)                                 | o `--browser` do pytest-playwright acumula valores: fixá-lo no `addopts` faria `pytest --browser firefox` rodar dois navegadores                                                                  |
| Cabeçalhos de segurança só em Chrome/Edge                                                | mesmo padrão do projeto Cypress: mantém o escopo e a contagem do Java (no Firefox o cenário é pulado)                                                                                            |
| Cabeçalhos lidos da resposta do `page.goto`                                              | observa a navegação normal, sem uma requisição a mais                                                                                                                                             |
| `.env.example` só como documentação                                                      | carregar `.env` exigiria o `python-dotenv`, fora da lista de bibliotecas                                                                                                                         |
| Pages e componentes como fixtures; steps importados no `conftest.py`                     | equivalente à injeção do PicoContainer; o `pytest_plugins` só é aceito no `conftest.py` da raiz                                                                                                  |
| `--clean-alluredir` no `addopts`                                                         | equivalente ao `mvn clean`; no Jenkins, cada estágio usa sua própria pasta de resultados                                                                                                         |
| `--screenshot=only-on-failure` e `--cucumberjson`                                        | evidências em arquivo para os artifacts, como o `cucumber.json` e os relatórios do Java                                                                                                          |
| Anexo "log" nos resultados do Allure                                                     | o `allure-pytest-bdd` anexa o log capturado de cada cenário e não tem opção para desligar                                                                                                        |
| `known-defects` com `if: !cancelled()`                                                   | os jobs agora são encadeados; assim os defeitos continuam rodando mesmo se a regressão falhar, como no Java                                                                                      |
| `playwright install --with-deps --force` no CI                                           | o runner já tem Chrome e Edge; o `--force` reinstala o canal pedido sem erro                                                                                                                      |
| Link de issue apontando para o repositório Java                                          | mesmas URLs do projeto original; troque o `--allure-link-pattern` no `pyproject.toml` se os defeitos forem registrados neste repositório                                                         |
| Mesmas decisões de cenário do Java                                                       | "a mensagem {string} é exibida" lê erro ou confirmação; botões pelo rótulo do Gherkin; rótulos do resumo sem ":"; pré-condições de checkout com "Sauce Labs Backpack"; "que o visitante não está autenticado" não executa nada |

---

## 12. Troubleshooting

| Problema                                                                                        | Causa / solução                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`Executable doesn't exist`** / navegador não encontrado                                       | os navegadores do Playwright não foram instalados: rode `playwright install chromium firefox`. Para Chrome e Edge, o navegador precisa estar instalado na máquina. |
| **`pytest: command not found`** ou `ModuleNotFoundError: playwright`                            | o `venv` não está ativado: `source .venv/bin/activate` (Linux/macOS) ou `.venv\Scripts\activate` (Windows)                                                           |
| **Timeout com `performance_glitch_user`**                                                       | esse usuário tem lentidão proposital (~5 s no login). O timeout de 10 s já cobre esse caso; em máquina ou rede lenta, use `TIMEOUT_SECONDS=20`.                    |
| **`'CT014_Carrinho' not found in markers configuration option`**                                | a tag nova não foi registrada em `markers` no `pyproject.toml` (seção 5)                                                                                             |
| **`StepDefinitionNotFoundError`**                                                               | o texto do passo não casa com nenhum step: confira as aspas e use `{valor:string}` para valores entre aspas                                                          |
| **`allure: command not found`** ou erro de Java ao abrir o relatório                            | instale o Allure CLI e um Java (seção 2) e confira o `PATH`                                                                                                          |
| **Cenário de cabeçalhos aparece como "skipped" no Firefox**                                     | esperado: a verificação de cabeçalhos é restrita a Chrome/Edge, como no projeto Java                                                                                 |
| **O job "Defeitos conhecidos" está vermelho**                                                   | esperado enquanto os defeitos existirem; o workflow continua verde (`continue-on-error`)                                                                             |
