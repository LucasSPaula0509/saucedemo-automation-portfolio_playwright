# language: pt

@produtos
Funcionalidade: Catálogo de produtos
  Como cliente autenticado no Swag Labs
  Quero visualizar, ordenar e detalhar os produtos
  Para escolher o que desejo comprar

  @CT001_Produtos @regressivo @smoke @positivo
  Cenário: Exibição do catálogo após autenticação
    Dado que o usuário "standard_user" está autenticado
    Quando ele acessa a página de produtos
    Então os produtos são exibidos com nome e preço
      | produto                           | preco  |
      | Sauce Labs Backpack               | $29.99 |
      | Sauce Labs Bike Light             | $9.99  |
      | Sauce Labs Bolt T-Shirt           | $15.99 |
      | Sauce Labs Fleece Jacket          | $49.99 |
      | Sauce Labs Onesie                 | $7.99  |
      | Test.allTheThings() T-Shirt (Red) | $15.99 |

  @CT002_Produtos @regressivo @positivo
  Cenário: Ordenação padrão do catálogo
    Dado que o usuário "standard_user" está autenticado
    Quando ele acessa a página de produtos
    Então a ordenação "Name (A to Z)" está selecionada

  @CT003_Produtos @regressivo @positivo @ordenacao
  Cenário: Ordenação por nome de Z a A
    Dado que o usuário "standard_user" está na página de produtos
    Quando ele ordena os produtos por "Name (Z to A)"
    Então os produtos são exibidos na ordem
      | produto                           |
      | Test.allTheThings() T-Shirt (Red) |
      | Sauce Labs Onesie                 |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Bike Light             |
      | Sauce Labs Backpack               |

  @CT004_Produtos @regressivo @positivo @ordenacao
  Cenário: Ordenação por menor preço
    Dado que o usuário "standard_user" está na página de produtos
    Quando ele ordena os produtos por "Price (low to high)"
    Então os produtos são exibidos na ordem
      | produto                           | preco  |
      | Sauce Labs Onesie                 | $7.99  |
      | Sauce Labs Bike Light             | $9.99  |
      | Sauce Labs Bolt T-Shirt           | $15.99 |
      | Test.allTheThings() T-Shirt (Red) | $15.99 |
      | Sauce Labs Backpack               | $29.99 |
      | Sauce Labs Fleece Jacket          | $49.99 |

  @CT005_Produtos @regressivo @positivo @ordenacao
  Cenário: Ordenação por maior preço
    Dado que o usuário "standard_user" está na página de produtos
    Quando ele ordena os produtos por "Price (high to low)"
    Então os produtos são exibidos na ordem
      | produto                           | preco  |
      | Sauce Labs Fleece Jacket          | $49.99 |
      | Sauce Labs Backpack               | $29.99 |
      | Sauce Labs Bolt T-Shirt           | $15.99 |
      | Test.allTheThings() T-Shirt (Red) | $15.99 |
      | Sauce Labs Bike Light             | $9.99  |
      | Sauce Labs Onesie                 | $7.99  |

  @CT006_Produtos @regressivo @positivo @ordenacao
  Cenário: Ordenação volta ao padrão ao retornar do detalhe do produto
    Dado que o usuário "standard_user" ordenou os produtos por "Price (low to high)"
    Quando ele abre o detalhe de um produto e volta para a lista com "Back to products"
    Então a ordenação "Name (A to Z)" está selecionada

  @CT007_Produtos @regressivo @positivo @detalhe
  Esquema do Cenário: Detalhe do produto exibe as mesmas informações do catálogo
    Dado que o usuário "standard_user" está na página de produtos
    Quando ele abre o detalhe do produto "<produto>"
    Então o detalhe exibe o nome "<produto>" com o preço "<preco>"

    Exemplos:
      | produto                  | preco  |
      | Sauce Labs Backpack      | $29.99 |
      | Sauce Labs Fleece Jacket | $49.99 |
      | Sauce Labs Onesie        | $7.99  |

  @CT008_Produtos @regressivo @positivo @detalhe
  Cenário: Retorno do detalhe para a lista de produtos
    Dado que o usuário "standard_user" está no detalhe do produto "Sauce Labs Backpack"
    Quando ele aciona "Back to products"
    Então a página de produtos é exibida

  @CT009_Produtos @regressivo @positivo @menu @defeito
  Cenário: Opções disponíveis no menu lateral
    Dado que o usuário "standard_user" está na página de produtos
    Quando ele abre o menu lateral
    Então as opções do menu são exibidas
      | opcao           |
      | All Items       |
      | About           |
      | Logout          |
      | Reset App State |

  @CT010_Produtos @regressivo @positivo @menu
  Cenário: Link "About" direciona para o site da Sauce Labs
    Dado que o usuário "standard_user" está com o menu lateral aberto
    Quando ele seleciona a opção "About"
    Então o site "https://saucelabs.com/" é exibido
