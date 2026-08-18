"""Testes da ferramenta buscar_catalogo e do acesso ao catálogo."""

import sqlite3

import pytest

from pinhao.db.seed import popular
from pinhao.tools.buscar_catalogo import buscar_catalogo


@pytest.fixture
def conn() -> sqlite3.Connection:
    ligacao = sqlite3.connect(":memory:")
    ligacao.row_factory = sqlite3.Row
    popular(ligacao)
    return ligacao


def test_seed_popula_catalogo(conn: sqlite3.Connection) -> None:
    total = conn.execute("SELECT COUNT(*) FROM caminhoes").fetchone()[0]
    assert total >= 5


def test_busca_por_aplicacao_longa_distancia(conn: sqlite3.Connection) -> None:
    resultado = buscar_catalogo(aplicacao="longa distância", conn=conn)
    assert resultado
    assert all("longa" in c.aplicacao.lower() for c in resultado)


def test_busca_respeita_preco_max(conn: sqlite3.Connection) -> None:
    resultado = buscar_catalogo(preco_max=500000, conn=conn)
    assert resultado
    assert all(c.preco_reais <= 500000 for c in resultado)


def test_busca_por_tracao(conn: sqlite3.Connection) -> None:
    resultado = buscar_catalogo(tracao="6x4", conn=conn)
    assert resultado
    assert all(c.tracao == "6x4" for c in resultado)


def test_preco_max_invalido_da_erro() -> None:
    with pytest.raises(ValueError):
        buscar_catalogo(preco_max=-1)


def test_limite_invalido_da_erro() -> None:
    with pytest.raises(ValueError):
        buscar_catalogo(limite=0)


def test_tracao_invalida_da_erro() -> None:
    with pytest.raises(ValueError):
        buscar_catalogo(tracao="9x9")
