"""Expressões dos steps com o mesmo comportamento do {string} do Cucumber.

O parse padrão ("{valor}") exige ao menos um caractere e não casa com "", usado nos Exemplos
com células vazias. O tipo "string" aceita qualquer texto entre aspas, inclusive vazio.
"""

from parse import with_pattern
from pytest_bdd import parsers


@with_pattern(r'[^"]*')
def _quoted_text(text: str) -> str:
    return text


def step(text: str) -> parsers.parse:
    """Ex.: step('ele digita a senha "{password:string}"')."""
    return parsers.parse(text, extra_types={"string": _quoted_text})


def table_rows(datatable: list[list[str]]) -> list[dict[str, str]]:
    """Linhas da tabela do Gherkin indexadas pelo cabeçalho (primeira linha)."""
    header, *rows = datatable
    return [dict(zip(header, row, strict=True)) for row in rows]
