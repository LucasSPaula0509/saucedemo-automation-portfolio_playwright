# language: pt

@performance
Funcionalidade: Performance percebida pelo usuário
  Como cliente da loja Swag Labs
  Quero que as páginas respondam rapidamente
  Para comprar sem esperas perceptíveis

  # Cada cenário faz uma única navegação, sem carga sobre o site.
  # Os limites ficam em config.properties (perf.*) e as medições são anexadas ao Allure.

  @CT001_Performance
  Cenário: Carregamento da página de login dentro do limite
    Quando o visitante abre a página de login medindo o carregamento
    Então a página de login carrega dentro do limite configurado
    E o Largest Contentful Paint fica dentro do limite configurado

  @CT002_Performance
  Cenário: Login do usuário padrão até a página de produtos dentro do limite
    Dado que o usuário "standard_user" está na página de login
    Quando ele se autentica com a senha "secret_sauce" medindo o tempo até a página de produtos
    Então a página de produtos é exibida
    E o tempo até a página de produtos fica dentro do limite configurado

  @CT003_Performance
  Cenário: Usuário com lentidão simulada é sinalizado como lento
    Dado que o usuário "performance_glitch_user" está na página de login
    Quando ele se autentica com a senha "secret_sauce" medindo o tempo até a página de produtos
    Então a página de produtos é exibida
    E o tempo até a página de produtos é sinalizado como acima do limite configurado
