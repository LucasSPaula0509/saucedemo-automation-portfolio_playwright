# language: pt

@checkout
Funcionalidade: Finalização da compra
  Como cliente autenticado no Swag Labs
  Quero informar meus dados e confirmar o pedido
  Para concluir a compra dos produtos do carrinho

  @CT001_Checkout @regressivo @smoke @positivo
  Cenário: Iniciar o checkout a partir do carrinho
    Dado que o carrinho do usuário "standard_user" contém o produto "Sauce Labs Backpack"
    Quando ele aciona "Checkout" no carrinho
    Então o formulário "Checkout: Your Information" é exibido

  @CT002_Checkout @regressivo @negativo @validacao
  Esquema do Cenário: Validação dos campos obrigatórios do checkout
    Dado que o usuário "standard_user" está no formulário de informações do checkout
    Quando ele continua informando nome "<nome>", sobrenome "<sobrenome>" e CEP "<cep>"
    Então a mensagem "<mensagem>" é exibida

    Exemplos:
      | nome | sobrenome | cep      | mensagem                        |
      |      |           |          | Error: First Name is required   |
      |      | Teste     | 06500000 | Error: First Name is required   |
      | Ana  |           | 06500000 | Error: Last Name is required    |
      | Ana  | Teste     |          | Error: Postal Code is required  |

  @CT003_Checkout @regressivo @positivo
  Cenário: Avançar para o resumo com dados válidos
    Dado que o usuário "standard_user" está no formulário de informações do checkout
    Quando ele continua informando nome "Ana", sobrenome "Teste" e CEP "06500000"
    Então o resumo "Checkout: Overview" é exibido

  @CT004_Checkout @regressivo @positivo
  Cenário: Resumo exibe forma de pagamento e entrega
    Dado que o usuário "standard_user" preencheu os dados do checkout com o produto "Sauce Labs Backpack" no carrinho
    Quando ele visualiza o resumo do pedido
    Então o resumo exibe as informações
      | campo                 | valor                         |
      | Payment Information   | SauceCard #31337              |
      | Shipping Information  | Free Pony Express Delivery!   |

  @CT005_Checkout @regressivo @smoke @positivo @calculo
  Esquema do Cenário: Cálculo de subtotal, imposto de 8% e total
    Dado que o usuário "standard_user" preencheu os dados do checkout com os produtos "<produtos>" no carrinho
    Quando ele visualiza o resumo do pedido
    Então o resumo exibe "Item total: <subtotal>", "Tax: <imposto>" e "Total: <total>"

    Exemplos:
      | produtos                                 | subtotal | imposto | total  |
      | Sauce Labs Bike Light                    | $9.99    | $0.80   | $10.79 |
      | Sauce Labs Backpack, Sauce Labs Onesie   | $37.98   | $3.04   | $41.02 |

  @CT006_Checkout @regressivo @smoke @positivo
  Cenário: Concluir a compra
    Dado que o usuário "standard_user" está no resumo do pedido
    Quando ele aciona "Finish"
    Então a mensagem "Thank you for your order!" é exibida

  @CT007_Checkout @regressivo @positivo
  Cenário: Carrinho é esvaziado após concluir a compra
    Dado que o usuário "standard_user" está no resumo do pedido
    Quando ele aciona "Finish"
    Então o contador do carrinho não é exibido

  @CT008_Checkout @regressivo @positivo
  Cenário: Voltar para os produtos após concluir a compra
    Dado que o usuário "standard_user" está na página "Checkout: Complete!"
    Quando ele aciona "Back Home"
    Então a página de produtos é exibida

  @CT009_Checkout @regressivo @positivo @cancelamento
  Cenário: Cancelar no formulário de informações retorna ao carrinho
    Dado que o usuário "standard_user" está no formulário de informações do checkout
    Quando ele aciona "Cancel"
    Então o carrinho é exibido

  @CT010_Checkout @regressivo @positivo @cancelamento
  Cenário: Cancelar no resumo retorna aos produtos mantendo o carrinho
    Dado que o usuário "standard_user" está no resumo do pedido com o produto "Sauce Labs Bike Light"
    Quando ele aciona "Cancel"
    Então o contador do carrinho exibe "1"

  # DEFEITO OBSERVADO em 30/10/2026: o site permite iniciar o checkout
  # com o carrinho vazio (redireciona para checkout-step-one.html).
  @CT011_Checkout @regressivo @negativo @defeito
  Cenário: Checkout bloqueado com carrinho vazio
    Dado que o usuário "standard_user" está no carrinho vazio
    Quando ele aciona "Checkout"
    Então o checkout não é iniciado
