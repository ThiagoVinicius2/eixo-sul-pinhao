"""Esquema do banco e o modelo Caminhao (fonte da verdade do catálogo)."""

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Caminhao:
    """Um item do catálogo. Dados fictícios, para fins educacionais."""

    codigo: str
    modelo: str
    versao: str
    aplicacao: str
    potencia_cv: int
    tracao: str
    pbt_ton: float
    preco_reais: int
    estoque: int
    prazo_entrega_dias: int


_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS caminhoes (
    codigo TEXT PRIMARY KEY,
    modelo TEXT NOT NULL,
    versao TEXT NOT NULL,
    aplicacao TEXT NOT NULL,
    potencia_cv INTEGER NOT NULL,
    tracao TEXT NOT NULL,
    pbt_ton REAL NOT NULL,
    preco_reais INTEGER NOT NULL,
    estoque INTEGER NOT NULL,
    prazo_entrega_dias INTEGER NOT NULL
)
"""


def criar_schema(conn: sqlite3.Connection) -> None:
    """Cria a tabela do catálogo se ela ainda não existir."""
    conn.execute(_CRIAR_TABELA)
    conn.commit()
