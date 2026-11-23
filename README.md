# VFX Shot Manager

[![CI](https://github.com/libbyhu/vfx-shot-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/libbyhu/vfx-shot-manager/actions/workflows/ci.yml)
[繁體中文](README.zh-TW.md)

A pipeline tool that checks rendered EXR sequences for missing frames, out-of-range frames, and naming errors before delivery, and keeps a history of every check.

> **Status: early development (Milestone 0 complete).** Only the missing-frame prototype below runs today. Everything else is the planned design, tracked in the [roadmap](docs/ROADMAP.md).

## Why

On a VFX show, render farms occasionally drop frames, write to the wrong folder, or produce misnamed files. These problems are often found late, in comp or at delivery. This project turns that manual folder check into one command or one button, with a stored report for each run.

## What works today

Requires [uv](https://docs.astral.sh/uv/).

```powershell
uv run vfx-shot-manager
```

```text
SH010 missing frames: [1003, 1006]
```

`find_missing_frames` in `src/vfx_shot_manager/core/validator.py` compares sample frames `[1001, 1002, 1004, 1005]` against the inclusive range `1001–1006`.
## Planned system

```text
Browser (React + TS) ──HTTP──▶ FastAPI ──▶ PostgreSQL ◀── Worker ──▶ read-only render storage
Terminal (vfxsm CLI) ─────────────────────────────────────┐   │
Nuke panel (bonus) ───────────────────────────────────────┴───┴──▶ core (pure Python, stdlib only)
```

The validation core has no framework or database dependencies, so the CLI, the background worker, and DCC tools such as Nuke all reuse the same logic.

| Milestone | Outcome | Status |
| --- | --- | --- |
| M0 Foundation | Package layout, ruff, pytest, CI | ✅ Done |
| M1 Core + CLI | `vfxsm scan` validates real folders and writes JSON reports | Planned |
| M2 Database + API | Shots, render versions, and validation runs over REST | Planned |
| M3 Worker | Queued scans using PostgreSQL `SKIP LOCKED`, stale-job recovery | Planned |
| M4 Frontend | Full workflow in the browser | Planned |
| M5 One-command demo | `docker compose up` with seeded sample data | Planned |
| M6 Nuke integration | Validate a Write node's output from inside Nuke | Planned |

## Documentation

- [System spec](docs/SPEC.md): scope, pipeline naming conventions, architecture, data model, API, testing, and security
- [Roadmap](docs/ROADMAP.md): milestones and task checklist (bilingual)
- [Contributing](CONTRIBUTING.md): code style, Git workflow, definition of done
- [Architecture decisions](docs/adr/)
- [Dev log](docs/DEVLOG.md) (bilingual)

Every document is available in English and Traditional Chinese.

## Tech stack (planned)

Python 3.12 · uv · ruff · pytest · FastAPI · SQLAlchemy · Alembic · PostgreSQL · React · TypeScript · Docker Compose · GitHub Actions
