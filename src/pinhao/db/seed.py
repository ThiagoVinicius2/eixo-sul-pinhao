"""Popula o banco com o catálogo fictício.

Rode com: ``python -m pinhao.db.seed`` (ou ``make seed``). Todos os números são
inventados, para fins educacionais — não são preços ou specs reais.
"""

import sqlite3

from pinhao.db.connection import conectar
from pinhao.db.schema import Caminhao, criar_schema

CATALOGO: list[Caminhao] = [
    Caminhao(
        "VM220-42", "VM", "VM 220 4x2", "distribuição urbana", 220, "4x2", 16.0, 380000, 3, 30
    ),
    Caminhao(
        "VM270-62", "VM", "VM 270 6x2", "distribuição regional", 270, "6x2", 23.0, 450000, 2, 45
    ),
    Caminhao(
        "FM380-62", "FM", "FM 380 6x2", "distribuição regional", 380, "6x2", 29.0, 620000, 1, 60
    ),
    Caminhao("FM460-64", "FM", "FM 460 6x4", "construção", 460, "6x4", 33.0, 720000, 2, 60),
    Caminhao("FMX500-84", "FMX", "FMX 500 8x4", "construção", 500, "8x4", 41.0, 890000, 0, 90),
    Caminhao("FH460-62", "FH", "FH 460 6x2", "longa distância", 460, "6x2", 30.0, 780000, 2, 45),
    Caminhao("FH500-64", "FH", "FH 500 6x4", "longa distância", 500, "6x4", 45.0, 850000, 1, 60),
    Caminhao("FH540-64", "FH", "FH 540 6x4", "longa distância", 540, "6x4", 45.0, 920000, 1, 75),
]


def popular(conn: sqlite3.Connection) -> int:
    """Cria o esquema e insere o catálogo fictício. Devolve o total inserido."""
    criar_schema(conn)
    conn.execute("DELETE FROM caminhoes")
    conn.executemany(
        "INSERT INTO caminhoes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                c.codigo,
                c.modelo,
                c.versao,
                c.aplicacao,
                c.potencia_cv,
                c.tracao,
                c.pbt_ton,
                c.preco_reais,
                c.estoque,
                c.prazo_entrega_dias,
            )
            for c in CATALOGO
        ],
    )
    conn.commit()
    return len(CATALOGO)


def main() -> None:
    conn = conectar()
    try:
        total = popular(conn)
        print(f"Catálogo populado: {total} caminhões (dados fictícios).")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
