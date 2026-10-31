# language: pt

@seguranca @passivo
Funcionalidade: Verificações passivas de segurança
  Como responsável pela qualidade da loja Swag Labs
  Quero observar as proteções de transporte, sessão e navegador
  Para registrar riscos sem atacar o site

  # Somente leitura do que o navegador recebe numa navegação normal:
  # nenhum scan ativo, fuzzing, força bruta ou injeção.
  # Achados vão para o Allure; com security.fail.on.findings=true eles reprovam o cenário.

  @CT001_Seguranca
  Cenário: Acesso via HTTP é redirecionado para HTTPS
    Quando o visitante acessa o site pelo protocolo HTTP
    Então a página é servida via HTTPS

  @CT002_Seguranca
  Cenário: Atributos do cookie de sessão após o login
    Dado que o usuário "standard_user" está autenticado
    Então os atributos Secure, HttpOnly e SameSite do cookie de sessão são verificados

  @CT003_Seguranca
  Cenário: Preenchimento automático do campo de senha
    Dado que o visitante está na página de login
    Então o atributo autocomplete do campo de senha é verificado

  @CT004_Seguranca
  Cenário: Cabeçalhos de segurança da página de login
    Quando o visitante abre a página de login registrando os cabeçalhos da resposta
    Então os cabeçalhos de segurança da resposta são verificados
