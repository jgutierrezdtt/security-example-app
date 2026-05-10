"""
Modulo de autenticacion — ejemplo para tutorial de seguridad.
"""

import hashlib
import os
import secrets


# ==============================================================================
# EJEMPLO — Almacenamiento seguro de contrasenas
#
# No almacenar contrasenas en texto plano ni con MD5/SHA1.
# Usar bcrypt, argon2 o PBKDF2 con salt aleatorio.
# Este ejemplo usa PBKDF2 con SHA-256 y salt de 32 bytes.
# ==============================================================================

def hash_password(password: str) -> tuple[str, str]:
    """
    Genera un hash seguro de una contrasena.

    Returns:
        (hash_hex, salt_hex) — ambos deben guardarse en la base de datos.
    """
    salt = secrets.token_bytes(32)
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=600_000,  # NIST recomendacion 2023
    )
    return key.hex(), salt.hex()


def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    """Verifica una contrasena contra su hash almacenado."""
    salt = bytes.fromhex(stored_salt)
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=600_000,
    )
    return secrets.compare_digest(key.hex(), stored_hash)


def generate_token(length: int = 32) -> str:
    """Genera un token criptograficamente seguro."""
    return secrets.token_urlsafe(length)
