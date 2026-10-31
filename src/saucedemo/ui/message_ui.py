"""Mensagens de retorno ao usuário: erros de validação e confirmação do pedido."""

from typing import Final

from saucedemo.ui import data_test

ERROR: Final = data_test.of("error")
ANY_FEEDBACK: Final = f"{data_test.of('error')}, {data_test.of('complete-header')}"
