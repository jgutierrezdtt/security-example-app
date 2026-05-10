"""
Tests de la aplicacion de ejemplo.

Los archivos en tests/ estan listados en .semgrepignore para que
Semgrep no los analice (evita falsos positivos en fixtures de prueba).
"""

import sqlite3
import pytest

from src.database import connect, get_user_insecure, get_user_by_name
from src.auth import hash_password, verify_password, generate_token


# Fixture: datos de prueba — estas credenciales son SOLO para tests
TEST_DB_USER = "test_user"
TEST_DB_PASSWORD = "test_password_only_for_tests"  # noqa: S105


@pytest.fixture
def db():
    conn = connect(":memory:")
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@example.com')")
    conn.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()
    yield conn
    conn.close()


def test_get_user_by_id(db):
    user = get_user_insecure(db, "1")
    assert user is not None
    assert user["name"] == "Alice"


def test_get_users_by_name(db):
    users = get_user_by_name(db, "b")
    assert len(users) == 1
    assert users[0]["name"] == "Bob"


def test_password_hash_and_verify():
    password = "my-secure-password"
    hash_hex, salt_hex = hash_password(password)

    assert verify_password(password, hash_hex, salt_hex)
    assert not verify_password("wrong-password", hash_hex, salt_hex)


def test_token_generation():
    token = generate_token()
    assert len(token) > 30  # urlsafe base64 de 32 bytes

    # Cada token debe ser unico
    assert generate_token() != generate_token()
