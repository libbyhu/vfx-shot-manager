# ADR 0001: Technology choices

English | [繁體中文](0001-tech-stack.zh-TW.md)

- Date: 2026-11-18
- Status: Accepted

> An ADR (Architecture Decision Record) records why a choice was made. When someone later asks "why not X?", the answer is here.

## Context

The goal is a VFX pipeline tool covering Python, filesystem handling, database and API design, with a natural path into DCC tools. It is also a learning project: the maintainer is new to Python and has experience with Java Spring Boot and frontend work.

## Decision

| Layer | Choice | Alternatives considered | Why |
| --- | --- | --- | --- |
| Core language | Python | — | The scripting language of the VFX industry and every major DCC |
| Core compatibility | Standard library only, Python 3.11 compatible | Third-party packages (e.g. `fileseq`) | Importable directly inside the Python bundled with DCCs such as Nuke; implementing sequence handling is also a learning goal |
| Package management | uv | pip + venv, Poetry | Fast; one tool for environments and dependencies; config centralised in `pyproject.toml` |
| Backend framework | FastAPI | Flask, Django | Driven by type hints, auto-generated API docs, concepts map easily from Spring Boot (routes, DTOs, dependency injection) |
| Database | PostgreSQL | SQLite | Needs `FOR UPDATE SKIP LOCKED` for the job queue and JSONB for reports; common in industry |
| ORM | SQLAlchemy 2 + Alembic | Raw SQL | Python industry standard; migrations make schema changes traceable |
| Job queue | PostgreSQL table + SKIP LOCKED | Celery + Redis, RQ | Small v1 traffic, one fewer service; the queue mechanics stay visible and easy to debug |
| Frontend | React + TypeScript | PySide6 desktop app, server-rendered templates | Coordinators need no install, only a browser; PySide is used for the M6 Nuke panel instead |
| Deployment | Docker Compose (local) | Cloud | Anyone can reproduce it with one command; cloud is out of v1 scope |

## Consequences

- Benefits: the core is shared by the CLI, worker, and DCCs; every layer can be tested on its own.
- Cost: Docker and PostgreSQL add learning load. That is why M1 deliberately needs no database — the Python core gets solid first.
- If traffic grows, or scheduling and retry policies are needed, evaluate Celery or RQ and write a new ADR.
