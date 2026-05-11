# CLAUDE.md — gea-rw

## Descripción del proyecto

**gea** es una aplicación web Django para gestionar Expedientes de trabajo de un
Estudio de Agrimensura en Santa Fe, Argentina. Permite registrar expedientes,
emitir notas, relacionar trabajos entre sí y confeccionar carátulas de plano.

Corre en producción en Railway (Nixpacks). Docker solo para servicios locales (ver abajo).

## Stack

- **Backend:** Python 3.14, Django 5, PostgreSQL (psycopg2)
- **Frontend:** Templates Django + Bootstrap 4.6 (diseño propio)
- **Config:** `django-environ` (`.env` local, env vars en Railway)
- **Deploy:** Railway (Nixpacks), gunicorn, whitenoise
- **Dependencias:** Poetry (`pyproject.toml` es la fuente de verdad)
- **Linting/formato:** `ruff` (reemplaza flake8 + black)
- **Otros:** django-nested-admin (formularios anidados), Redis (cache Select2)

## Estructura del repo

    gea-rw/
    ├── estudio/          # Proyecto Django (settings, urls, wsgi)
    ├── gea/              # App principal
    │   ├── models.py     # Modelo de datos central
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── templates/
    │   └── ...
    ├── docker-compose.yml  # PostgreSQL 17 + Redis 7 para dev local
    ├── .env.example        # Plantilla de variables de entorno
    ├── manage.py
    ├── pyproject.toml
    └── Procfile          # Railway: web: gunicorn estudio.wsgi

## Modelo de datos

Ver diagrama `gea_models_v2.6.png` en la raíz del repo. Las entidades principales
son Expediente (trabajo de agrimensura), Profesional, Persona, Objeto (tipo de
trabajo), Partida inmobiliaria, entre otras.

Antes de modificar modelos: revisar migraciones existentes y el diagrama. Toda
migración debe ser reversible salvo casos excepcionales documentados.

## Convenciones de código

- Python: seguir PEP 8. Sin type hints obligatorios, pero bienvenidos en código nuevo.
- Linting y formato: `poetry run ruff check .` y `poetry run ruff format .`
- Django: class-based views preferidas sobre FBV para vistas complejas.
- Templates: Bootstrap 4.6. No agregar dependencias JS adicionales sin consultar.
- Nombres en español para modelos y campos que reflejen terminología catastral/registral
  de Santa Fe (ej: `partida`, `nomenclatura`, `inscripcion`).

## Comandos frecuentes

```bash
# Entorno local — iniciar servicios primero
docker compose up -d          # PostgreSQL + Redis en contenedores
poetry run python manage.py runserver
docker compose down           # al terminar

# Migraciones
poetry run python manage.py makemigrations gea
poetry run python manage.py migrate

# Linting y formato
poetry run ruff check .
poetry run ruff format .
poetry run ruff check --fix .

# Deploy (Railway lo hace automático en push a main)
railway up   # solo si deploy manual
```

## Variables de entorno necesarias

Copiar `.env.example` → `.env` (gitignored) y completar. En Railway se definen directamente:

- `SECRET_KEY` — clave secreta larga y aleatoria
- `DEBUG` — `False` en producción
- `DATABASE_URL` — Railway lo provee automáticamente
- `REDIS_URL` — Railway lo provee automáticamente
- `ALLOWED_HOSTS` — ej: `gea.up.railway.app,gea.pestarini.com.ar`

## Contexto de dominio

- Agrimensura en Santa Fe.
  DUDAS DE TERMINOLOGÍA: consultar al desarrollador antes de asumir.
- Los expedientes pueden ser: mensuras, subdivisiones, unificaciones, relevamientos,
  constitución de servidumbres, etc.
- "Comitente" = cliente que solicita el trabajo
- "Propietario" = dueño de la propiedad sobre la cual se hace el trabajo.
- "Nomenclatura catastral" identifica una parcela en el sistema provincial.
- "Partida inmobiliaria" identifica una finca en el sistema provincial.
  Formato: `DP-DS-SD PII/SubPII-DV` (ej: `11-08-00 001234/0001-5`)
- Una finca puede estar formada por 1 o más parcelas, es decir, una Partida
  inmobiliaria puede contener 1 o más Nomenclaturas catastrales.

## Lo que NO hacer

- No reemplazar Bootstrap 4.6 sin una decisión explícita.
- No cambiar el ORM por queries raw salvo casos de performance demostrada.
- No tocar `requirements.txt` directamente: se genera desde Poetry.
- No hardcodear strings de dominio (expediente tipos, estados) que ya estén como
  choices en los modelos.
- No commitear `.env` al repo.

## Historial de decisiones relevantes

- Docker solo para servicios locales (PostgreSQL, Redis). Django corre con Poetry local.
  Railway usa Nixpacks directamente desde `pyproject.toml`.
- `django-environ` para configuración: un solo `settings.py`, todo via env vars.
  Settings de seguridad y LOGGING solo activos cuando `DEBUG=False`.
- `CONN_MAX_AGE=500` en DATABASES para reutilizar conexiones entre requests.
- `nested_admin` para formularios de expediente con inlines anidados.
- Bootstrap 4.6 (no 5) por compatibilidad con templates existentes.
- `ruff` como linter y formatter (reemplaza flake8 + black). Config en `pyproject.toml`.
- `Partida.identificador` es un campo denormalizado pre-calculado en `save()`.
  Evita recorrer la cadena `Partida → Sd → Ds → Dp` en cada acceso.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- ALWAYS read graphify-out/GRAPH_REPORT.md before reading any source files, running grep/glob searches, or answering codebase questions. The graph is your primary map of the codebase.
- IF graphify-out/wiki/index.md EXISTS, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code, run `poetry run graphify update .` to keep the graph current (AST-only, no API cost).
