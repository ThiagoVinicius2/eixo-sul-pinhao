"""Acesso de leitura ao catálogo no banco.

Fonte da verdade: o agente só enxerga o que estas consultas devolvem. Nenhum
dado de catálogo existe fora daqui.
"""

import sqlite3

from pinhao.db.schema import Caminhao


def _linha_para_caminhao(linha: sqlite3.Row) -> Caminhao:
    return Caminhao(
        codigo=linha["codigo"],
        modelo=linha["modelo"],
        versao=linha["versao"],
        aplicacao=linha["aplicacao"],
        potencia_cv=linha["potencia_cv"],
        tracao=linha["tracao"],
        pbt_ton=linha["pbt_ton"],
        preco_reais=linha["preco_reais"],
        estoque=linha["estoque"],
        prazo_entrega_dias=linha["prazo_entrega_dias"],
    )


def buscar_caminhoes(
    conn: sqlite3.Connection,
    *,
    aplicacao: str | None = None,
    preco_max: int | None = None,
    potencia_min: int | None = None,
    tracao: str | None = None,
    limite: int = 5,
) -> list[Caminhao]:
    """Consulta o catálogo aplicando os filtros informados (parametrizado)."""
    clausulas: list[str] = []
    parametros: list[object] = []
    if aplicacao is not None:
        clausulas.append("LOWER(aplicacao) LIKE ?")
        parametros.append(f"%{aplicacao.lower()}%")
    if preco_max is not None:
        clausulas.append("preco_reais <= ?")
        parametros.append(preco_max)
    if potencia_min is not None:
        clausulas.append("potencia_cv >= ?")
        parametros.append(potencia_min)
    if tracao is not None:
        clausulas.append("LOWER(tracao) = ?")
        parametros.append(tracao.lower())

    onde = f"WHERE {' AND '.join(clausulas)}" if clausulas else ""
    sql = f"SELECT * FROM caminhoes {onde} ORDER BY preco_reais ASC LIMIT ?"
    parametros.append(limite)

    cursor = conn.execute(sql, parametros)
    return [_linha_para_caminhao(linha) for linha in cursor.fetchall()]
