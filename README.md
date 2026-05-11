# gea

Gestión de Expedientes de Agrimensores.

**gea** es una aplicación web para gestionar expedientes de agrimensura siguiendo la estructura del SCIT (Sistema Catastral Informático Territorial) de la provincia de Santa Fe, Argentina.

## Stack

- Python 3.14 + Django 5
- PostgreSQL · Redis · Bootstrap 4.6
- Deploy: [Railway](https://railway.app) (Nixpacks + gunicorn)

## Desarrollo local

**Requisitos:** [Poetry](https://python-poetry.org) y [Docker](https://www.docker.com).

```bash
# 1. Clonar e instalar dependencias
git clone https://github.com/quijot/gea-rw.git
cd gea-rw
poetry install

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con los valores locales

# 3. Levantar PostgreSQL y Redis
docker compose up -d

# 4. Migrar
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py collectstatic

# 5. Correr
poetry run python manage.py runserver
```

Ingresar en [http://127.0.0.1:8000/gea/](http://127.0.0.1:8000/gea/).

## Variables de entorno

Ver `.env.example`. Las principales:

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en desarrollo, `False` en producción |
| `DATABASE_URL` | URL de conexión a PostgreSQL |
| `REDIS_URL` | URL de conexión a Redis |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por coma) |

## Actualizar dependencias

`pyproject.toml` es la fuente de verdad. Después de cualquier cambio (p.ej. `poetry add <paquete>`), regenerar `requirements.txt` antes del push — Railway lo usa para el deploy:

```bash
poetry lock
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Deploy

Railway detecta automáticamente el entorno desde `pyproject.toml`. El deploy se activa con cada push a `main`. Las variables de entorno se configuran en el panel de Railway.

## Licencia

[MIT](LICENSE)
