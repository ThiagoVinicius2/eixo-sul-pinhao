"""Ferramenta ``buscar_catalogo`` — a fronteira que o agente chama para achar produtos.

Valida a entrada (regra de negócio) e delega a consulta ao banco (fonte da
verdade). O agente só pode recomendar entre o que esta função devolver: nada de
inventar modelo, preço ou estoque.
"""

import sqlite3

from pinhao.db.catalogo import buscar_caminhoes
from pinhao.db.connection import conectar
from pinhao.db.schema import Caminhao

APLICACOES_CONHECIDAS = (
    "distribuição urbana",
    "distribuição regional",
    "longa distância",
    "construção",
)
TRACOES_VALIDAS = ("4x2", "6x2", "6x4", "8x4")


def buscar_catalogo(
    *,
    aplicacao: str | None = None,
    preco_max: int | None = None,
    potencia_min: int | None = None,
    tracao: str | None = None,
    limite: int = 5,
    conn: sqlite3.Connection | None = None,
) -> list[Caminhao]:
    """Busca caminhões no catálogo pelos filtros informados.

    Levanta ``ValueError`` para entradas inválidas — o código recusa o pedido
    antes de tocar no banco, em vez de confiar no texto do prompt.
    """
    if preco_max is not None and preco_max <= 0:
        raise ValueError("preco_max deve ser positivo.")
    if potencia_min is not None and potencia_min <= 0:
        raise ValueError("potencia_min deve ser positivo.")
    if not 1 <= limite <= 20:
        raise ValueError("limite deve estar entre 1 e 20.")
    if tracao is not None and tracao.lower() not in TRACOES_VALIDAS:
        raise ValueError(f"tracao inválida: {tracao!r}.")

    conexao_propria = conn is None
    ligacao = conn if conn is not None else conectar()
    try:
        return buscar_caminhoes(
            ligacao,
            aplicacao=aplicacao,
            preco_max=preco_max,
            potencia_min=potencia_min,
            tracao=tracao,
            limite=limite,
        )
    finally:
        if conexao_propria:
            ligacao.close()
