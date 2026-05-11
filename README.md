# security-example-app

Aplicacion de ejemplo para el tutorial de la plataforma de seguridad de jgutierrezdtt.

Este repositorio muestra como funciona la integracion con [security-platform](https://github.com/jgutierrezdtt/security-platform) en un proyecto real. Puedes usarlo como referencia o como punto de partida para entender que detecta Semgrep y por que.

---

## Que encontraras aqui

### Como funciona la integracion (el archivo clave)

El unico archivo que conecta este repo con la plataforma de seguridad es:

```
.github/workflows/security.yml
```

Su contenido es:

```yaml
jobs:
  semgrep:
    uses: jgutierrezdtt/security-platform/.github/workflows/reusable-semgrep-scan.yml@main

  dependabot:
    uses: jgutierrezdtt/security-platform/.github/workflows/reusable-dependabot-check.yml@main
```

Eso es todo. Las reglas de Semgrep, los umbrales de severidad, la logica de excepciones — todo vive en security-platform. Cuando el security team actualiza algo alli, este repo lo recibe automaticamente sin ninguna accion de tu parte.

---

## Ejemplos comentados en el codigo

### `src/database.py` — Lo que Semgrep detecta y como corregirlo

| Patron inseguro | Regla Semgrep | Patron seguro |
|-----------------|---------------|---------------|
| `api_key = "sk-abc123"` | `no-hardcoded-api-keys` | `os.getenv("API_KEY")` |
| `"SELECT ... WHERE id = " + user_id` | `sql-injection-string-concat` | `db.execute("... WHERE id = ?", (user_id,))` |
| `DEBUG = True` hardcodeado | `debug-mode-production` | `os.getenv("DEBUG", "false") == "true"` |

### `src/auth.py` — Implementacion segura de referencia

Muestra como hacer hash de contrasenas con PBKDF2 + salt y tokens seguros con `secrets`.

### `tests/` — Por que los tests no generan alertas

El archivo `.semgrepignore` excluye el directorio `tests/` del analisis.
Sin esto, Semgrep marcaria las credenciales de fixture como hallazgos.
Ver [tutorial de excepciones](https://github.com/jgutierrezdtt/security-platform/blob/main/docs/tutorials/08-exception-management.md).

---

## Flujo completo de un PR en este repo

```
Developer abre PR
       |
       v
GitHub Actions ejecuta security.yml
       |
       +---> semgrep-scan.yml (en security-platform)
       |           |
       |           |-- Descarga excepciones de security-exceptions
       |           |-- Ejecuta semgrep con las reglas de la plataforma
       |           |-- Filtra hallazgos con excepciones aprobadas
       |           |-- Publica comentario sticky en el PR
       |           `-- Falla si hay hallazgos HIGH sin excepcion
       |
       `---> dependabot-check.yml (en security-platform)
                   |
                   |-- Consulta alertas de Dependabot via API
                   `-- Falla si hay alertas CRITICAL sin resolver
```

Ninguna de esta logica vive en este repo. Todo es mantenido centralmente.

---

## Ejecutar localmente

```bash
pip install semgrep pytest -r requirements.txt

# Tests
pytest tests/

# Semgrep (mismas reglas que en CI)
semgrep scan --config https://raw.githubusercontent.com/jgutierrezdtt/security-platform/main/config/semgrep/rules.yml src/
```

---

## Solicitar una excepcion

Si Semgrep detecta un hallazgo en tu proyecto y crees que es un falso positivo:

[Abrir solicitud de excepcion](https://github.com/jgutierrezdtt/security-platform/issues/new?template=exception-request.yml)

---

## Crear tu propio repo usando esta integracion

Usa la plantilla oficial:

[Crear repositorio desde security-consumer-template](https://github.com/jgutierrezdtt/security-consumer-template/generate)
