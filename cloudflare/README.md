# Cloudflare Preparation

This project currently ships as a FastAPI + SQLite application for fast local delivery and Docker-first demos.

Recommended migration path to Cloudflare free tier:

1. replace SQLite calls with a storage adapter abstraction
2. implement D1 adapter for events, alerts, metrics and CVE cache
3. keep `frontend/` as static Pages asset bundle
4. expose API endpoints through Workers or a Python-compatible edge/runtime split
5. optionally use KV for lightweight UI preferences and cached dictionaries

This directory exists to keep the Cloudflare path documented without forcing the current MVP into premature complexity.
