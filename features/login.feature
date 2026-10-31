# language: pt

@login
Funcionalidade: Autenticação de usuários no Swag Labs
  Como cliente da loja Swag Labs
  Quero me autenticar com minhas credenciais
  Para acessar o catálogo de produtos e realizar compras

  @CT001_Login @regressivo @smoke @positivo
  Cenário: Login com credenciais válidas
    Dado que o usuário "standard_user" está na página de login
    Quando ele se autentica com a senha "secret_sauce"
    Então a página de produtos é exibida

  @CT002_Login @regressivo @positivo
  Esquema do Cenário: Login com perfis de usuário aceitos
    Dado que o usuário "<usuario>" está na página de login
    Quando ele se autentica com a senha "secret_sauce"
    Então a página de produtos é exibida

    Exemplos:
      | usuario                 |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |
      | error_user              |
      | visual_user             |

  @CT003_Login @regressivo @negativo
  Cenário: Login com usuário bloqueado
    Dado que o usuário "locked_out_user" está na página de login
    Quando ele se autentica com a senha "secret_sauce"
    Então a mensagem "Epic sadface: Sorry, this user has been locked out." é exibida

  @CT004_Login @regressivo @negativo
  Esquema do Cenário: Login com credenciais inválidas
    Dado que o usuário "<usuario>" está na página de login
    Quando ele se autentica com a senha "<senha>"
    Então a mensagem "Epic sadface: Username and password do not match any user in this service" é exibida

    Exemplos:
      | usuario       | senha        | caso                          |
      | standard_user | senha_errada | senha incorreta               |
      | usuario_falso | secret_sauce | usuário inexistente           |
      | STANDARD_USER | secret_sauce | usuário com caixa diferente   |
      | standard_user | SECRET_SAUCE | senha com caixa diferente     |

  @CT005_Login @regressivo @negativo @validacao
  Esquema do Cenário: Login com campos obrigatórios não preenchidos
    Dado que o visitante está na página de login
    Quando ele tenta se autenticar com usuário "<usuario>" e senha "<senha>"
    Então a mensagem "<mensagem>" é exibida

    Exemplos:
      | usuario       | senha        | mensagem                            |
      |               |              | Epic sadface: Username is required  |
      |               | secret_sauce | Epic sadface: Username is required  |
      | standard_user |              | Epic sadface: Password is required  |

  @CT006_Login @regressivo @seguranca
  Cenário: Campo de senha mascara os caracteres digitados
    Dado que o visitante está na página de login
    Quando ele digita a senha "secret_sauce"
    Então o conteúdo do campo de senha é exibido mascarado

  @CT007_Login @regressivo @seguranca
  Esquema do Cenário: Acesso direto a páginas internas sem autenticação
    Dado que o visitante não está autenticado
    Quando ele acessa diretamente a página "<pagina>"
    Então a mensagem "Epic sadface: You can only access '<pagina>' when you are logged in." é exibida

    Exemplos:
      | pagina                     |
      | /inventory.html            |
      | /cart.html                 |
      | /checkout-step-one.html    |

  @CT008_Login @regressivo @positivo
  Cenário: Logout pelo menu lateral
    Dado que o usuário "standard_user" está autenticado
    Quando ele seleciona a opção "Logout" no menu lateral
    Então a página de login é exibida

  @CT009_Login @regressivo @seguranca
  Cenário: Sessão encerrada após logout impede retorno à área logada
    Dado que o usuário "standard_user" encerrou a sessão pelo menu lateral
    Quando ele tenta retornar à página de produtos pelo histórico do navegador
    Então a mensagem "Epic sadface: You can only access '/inventory.html' when you are logged in." é exibida
