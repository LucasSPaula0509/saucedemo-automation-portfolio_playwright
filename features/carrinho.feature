# language: pt

@carrinho
Funcionalidade: Carrinho de compras
  Como cliente autenticado no Swag Labs
  Quero adicionar e remover produtos do carrinho
  Para montar o pedido que desejo finalizar

  @CT001_Carrinho @regressivo @smoke @positivo
  Cenário: Adicionar um produto ao carrinho pela lista de produtos
    Dado que o usuário "standard_user" está na página de produtos com o carrinho vazio
    Quando ele adiciona o produto "Sauce Labs Backpack" ao carrinho
    Então o contador do carrinho exibe "1"

  @CT002_Carrinho @regressivo @positivo
  Cenário: Botão do produto muda para "Remove" após adicioná-lo
    Dado que o usuário "standard_user" está na página de produtos com o carrinho vazio
    Quando ele adiciona o produto "Sauce Labs Bike Light" ao carrinho
    Então o botão do produto "Sauce Labs Bike Light" exibe "Remove"

  @CT003_Carrinho @regressivo @positivo
  Cenário: Contador do carrinho acumula vários produtos
    Dado que o usuário "standard_user" está na página de produtos com o carrinho vazio
    Quando ele adiciona ao carrinho os produtos
      | produto                  |
      | Sauce Labs Backpack      |
      | Sauce Labs Bike Light    |
      | Sauce Labs Fleece Jacket |
    Então o contador do carrinho exibe "3"

  @CT004_Carrinho @regressivo @positivo
  Cenário: Remover um produto pela lista de produtos
    Dado que o carrinho do usuário "standard_user" contém os produtos "Sauce Labs Backpack" e "Sauce Labs Bike Light"
    Quando ele remove o produto "Sauce Labs Bike Light" pela lista de produtos
    Então o contador do carrinho exibe "1"

  @CT005_Carrinho @regressivo @positivo
  Cenário: Contador do carrinho some quando o último produto é removido
    Dado que o carrinho do usuário "standard_user" contém apenas o produto "Sauce Labs Backpack"
    Quando ele remove o produto "Sauce Labs Backpack" pela lista de produtos
    Então o contador do carrinho não é exibido

  @CT006_Carrinho @regressivo @positivo @detalhe
  Cenário: Adicionar um produto ao carrinho pela página de detalhe
    Dado que o usuário "standard_user" está no detalhe do produto "Sauce Labs Backpack" com o carrinho vazio
    Quando ele adiciona o produto ao carrinho
    Então o contador do carrinho exibe "1"

  @CT007_Carrinho @regressivo @positivo @detalhe
  Cenário: Estado do carrinho é mantido entre o detalhe e a lista de produtos
    Dado que o usuário "standard_user" adicionou o produto "Sauce Labs Backpack" pela página de detalhe
    Quando ele volta para a lista de produtos
    Então o botão do produto "Sauce Labs Backpack" exibe "Remove"

  @CT008_Carrinho @regressivo @smoke @positivo
  Cenário: Carrinho lista os produtos adicionados
    Dado que o usuário "standard_user" adicionou os produtos "Sauce Labs Backpack" e "Sauce Labs Onesie"
    Quando ele acessa o carrinho
    Então o carrinho exibe os itens
      | quantidade | produto             | preco  |
      | 1          | Sauce Labs Backpack | $29.99 |
      | 1          | Sauce Labs Onesie   | $7.99  |

  @CT009_Carrinho @regressivo @positivo
  Cenário: Remover um produto dentro do carrinho
    Dado que o carrinho do usuário "standard_user" contém os produtos "Sauce Labs Backpack" e "Sauce Labs Onesie"
    Quando ele remove o produto "Sauce Labs Onesie" no carrinho
    Então o carrinho exibe apenas o produto "Sauce Labs Backpack"

  @CT010_Carrinho @regressivo @positivo
  Cenário: Continuar comprando a partir do carrinho
    Dado que o usuário "standard_user" está no carrinho
    Quando ele aciona "Continue Shopping"
    Então a página de produtos é exibida

  @CT011_Carrinho @regressivo @positivo
  Cenário: Carrinho mantém os produtos após recarregar a página
    Dado que o carrinho do usuário "standard_user" contém o produto "Sauce Labs Backpack"
    Quando ele recarrega a página de produtos
    Então o contador do carrinho exibe "1"

  @CT012_Carrinho @regressivo @positivo @menu
  Cenário: Reset App State esvazia o carrinho
    Dado que o carrinho do usuário "standard_user" contém o produto "Sauce Labs Fleece Jacket"
    Quando ele seleciona a opção "Reset App State" no menu lateral
    Então o contador do carrinho não é exibido

  # DEFEITO OBSERVADO em 30/10/2026: após o reset, o botão continua "Remove"
  # até a página ser recarregada.
  @CT013_Carrinho @regressivo @negativo @menu @defeito
  Cenário: Reset App State restaura os botões dos produtos
    Dado que o carrinho do usuário "standard_user" contém o produto "Sauce Labs Fleece Jacket"
    Quando ele seleciona a opção "Reset App State" no menu lateral
    Então o botão do produto "Sauce Labs Fleece Jacket" exibe "Add to cart"
