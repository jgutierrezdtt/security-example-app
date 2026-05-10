"""
Modulo de base de datos — ejemplo para tutorial de seguridad.

Este archivo contiene ejemplos EDUCATIVOS de patrones que Semgrep detecta.
Ver README.md para explicacion detallada de cada hallazgo.
"""

import os
import sqlite3
from typing import Optional


# ==============================================================================
# EJEMPLO 1 — Credencial hardcodeada (detectado por: no-hardcoded-api-keys)
#
# Semgrep marca esta linea porque la variable tiene "key" en el nombre
# y su valor es una cadena literal. En produccion, los secretos se leen
# de variables de entorno o de un gestor como Azure Key Vault.
# ==============================================================================

# MAL — esto lo detecta Semgrep:
# api_key = "sk-prod-abc123xyz"

# BIEN — leer del entorno:
api_key: Optional[str] = os.getenv("API_KEY")


# ==============================================================================
# EJEMPLO 2 — SQL injection por concatenacion (detectado por: sql-injection-string-concat)
#
# Semgrep detecta que se construye una query SQL concatenando una variable
# directamente. Un atacante puede manipular `user_id` para extraer datos.
# La solucion es usar parametros enlazados (placeholders).
# ==============================================================================

def get_user_insecure(db: sqlite3.Connection, user_id: str) -> Optional[dict]:
    """NO USAR en produccion — ejemplo de SQL injection."""
    # MAL — concatenacion directa:
    # query = "SELECT * FROM users WHERE id = " + user_id
    # cursor = db.execute(query)

    # BIEN — parametros enlazados:
    cursor = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_user_by_name(db: sqlite3.Connection, name: str) -> list:
    """Busqueda segura por nombre."""
    cursor = db.execute(
        "SELECT id, name, email FROM users WHERE name LIKE ?",
        (f"%{name}%",)
    )
    return [dict(row) for row in cursor.fetchall()]


# ==============================================================================
# EJEMPLO 3 — Configuracion de debug en produccion
#
# Una variable DEBUG=True puede exponer trazas de error con informacion
# sensible sobre la infraestructura. Semgrep busca este patron.
# ==============================================================================

# Leer del entorno — nunca hardcodear True en produccion
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


def connect(db_path: str = ":memory:") -> sqlite3.Connection:
    """Crea una conexion a la base de datos."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
