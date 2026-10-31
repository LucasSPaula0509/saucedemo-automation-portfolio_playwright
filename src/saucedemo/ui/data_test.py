"""Fábrica de seletores pelo atributo data-test, o seletor preferencial do projeto."""


def of(value: str) -> str:
    return f"[data-test='{value}']"


def ending_with(suffix: str) -> str:
    return f"[data-test$='{suffix}']"
