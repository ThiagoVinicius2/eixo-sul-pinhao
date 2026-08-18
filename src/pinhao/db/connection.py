"""Conexão com o banco (fonte única da verdade)."""

import os
import sqlite3

_PREFIXO_SQLITE = "sqlite:///"
_PADRAO = "sqlite:///./eixo_sul.sqlite3"


def caminho_banco() -> str:
    """Caminho do arquivo SQLite, lido de DATABASE_URL (ou o padrão local)."""
    url = os.environ.get("DATABASE_URL", _PADRAO)
    if url.startswith(_PREFIXO_SQLITE):
        return url[len(_PREFIXO_SQLITE) :]
    return url


def conectar() -> sqlite3.Connection:
    """Abre uma conexão com o banco, com linhas acessíveis por nome de coluna."""
    conn = sqlite3.connect(caminho_banco())
    conn.row_factory = sqlite3.Row
    return conn
