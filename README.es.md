<p align="center">
  <img src="https://raw.githubusercontent.com/Garcez7R/heimdall-gatekeeper/main/logo.png" alt="Logotipo de Heimdall Gatekeeper" width="220" />
</p>

# ᚺ Heimdall Gatekeeper

<p align="center">
  <strong>Seleccionar idioma:</strong>
  <a href="./README.pt-BR.md">Português (BR)</a> |
  <a href="./README.md">English</a> |
  <a href="./README.es.md">Español</a>
</p>

![Python](https://img.shields.io/badge/Python-3.11%2B-0f172a?style=for-the-badge&logo=python&logoColor=ffd43b)
![FastAPI](https://img.shields.io/badge/FastAPI-Security%20API-0f172a?style=for-the-badge&logo=fastapi&logoColor=22c55e)
![SQLite](https://img.shields.io/badge/SQLite-Lightweight%20Storage-0f172a?style=for-the-badge&logo=sqlite&logoColor=7dd3fc)
![Docker](https://img.shields.io/badge/Docker-Ready-0f172a?style=for-the-badge&logo=docker&logoColor=60a5fa)
![CI](https://img.shields.io/github/actions/workflow/status/Garcez7R/heimdall-gatekeeper/ci.yml?branch=main&style=for-the-badge&label=CI)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Pages%20%2B%20Functions%20%2B%20D1-0f172a?style=for-the-badge&logo=cloudflare&logoColor=f59e0b)

Heimdall Gatekeeper es una demostración práctica de SIEM con una consola visual clara, instalación sencilla y comportamiento real de seguridad. Está pensado para que cualquier persona pueda ver rápidamente cómo entran los eventos, cómo actúan las reglas y cómo aparece el contexto de vulnerabilidades en el panel. No hace falta experiencia previa en seguridad: solo ejecuta la aplicación y explora el tablero.

## Qué Demuestra Este Proyecto

- ingestión normalizada de eventos estructurados
- reglas YAML con escalado de severidad
- ciclo de vida de alertas con reconocimiento y resolución
- enriquecimiento con contexto de vulnerabilidades ligadas a CVEs
- métricas operativas y vista general de consola de seguridad
- ejecución local, con Docker y con ruta preparada para Cloudflare

Es un proyecto compacto, pero ya se comporta como un producto orientado a seguridad, y no como un CRUD simple.

## Capacidades Principales

- backend FastAPI con rutas modulares
- persistencia en SQLite para eventos, alertas, métricas y rule hits
- ruta preparada para Cloudflare con Pages Functions + D1
- dashboard en vivo con resumen, alertas, eventos y estado
- bootstrap automático de datos demo para presentación inmediata
- tema dark/light, control de densidad, alto contraste y reducción de movimiento
- interfaz multilingüe: `pt-BR`, `en`, `es`
- pipeline CI con lint, formateo, SAST, auditoría de dependencias, pruebas y build Docker

## Acceso Rápido

### Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
# requirements-dev.txt incluye herramientas de prueba y calidad, pero la app funciona con requirements.txt sola
cp .env.example .env
uvicorn backend.api.main:app --reload
```

Abrir:

- `http://127.0.0.1:8000`

### Bootstrap demo

- navegador: `http://127.0.0.1:8000/api/demo/bootstrap`
- terminal:

```bash
curl http://127.0.0.1:8000/api/demo/bootstrap
```

### Cloudflare

1. Crear el D1:

```bash
npx wrangler d1 create heimdall-gatekeeper
```

2. Aplicar el schema:

```bash
npx wrangler d1 execute heimdall-gatekeeper --remote --file=cloudflare/d1/0001_init.sql
```

3. En Pages usar:
- Framework preset: `None`
- Build command: vacío
- Build output directory: `frontend`

4. Confirmar binding D1:
- Binding name: `DB`

## Documentación Completa

- [Português (BR)](./README.pt-BR.md)
- [English](./README.md)
- [Español](./README.es.md)

## Por Qué Importa en el Portafolio

Este proyecto fue construido para demostrar capacidad práctica en:

- flujo de trabajo y pensamiento Blue Team
- procesamiento de eventos estilo SecOps
- UX de producto de seguridad y dashboards operativos
- organización de backend Python con pruebas y CI
- pensamiento de despliegue en entorno local, contenedor y nube

## Licencia

Uso educativo y de portafolio.
