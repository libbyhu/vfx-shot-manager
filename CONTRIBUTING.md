# Contributing

English | [繁體中文](CONTRIBUTING.zh-TW.md)

> These rules apply to every change in this repository, including work by a single maintainer.

## 1. Python style

| Rule | Details |
| --- | --- |
| Formatting | Leave it to `ruff format`; never format by hand |
| Lint | `ruff check` must report no errors |
| Naming | Variables and functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`, private names start with `_` |
| Type hints | Required on every function's parameters and return value |
| Docstrings | Google-style docstrings on public functions: parameters, return value, exceptions raised |
| Paths | Use `pathlib.Path`; no string concatenation, no `os.path` |
| Output | No `print` in library code — use `logging`; only `cli.py` prints for humans |
| Globals | Don't use them. Pass data in as parameters |
| Entry points | Executable files use `if __name__ == "__main__":` |
| Large lookups | Use a `set`; never search a `list` with `in` |
| Strings | Use f-strings |
| Core restriction | `core/` may import only the standard library |

Example:

```python
def find_missing_frames(found: set[int], start: int, end: int) -> list[int]:
    """Return frames in the inclusive range that are not in ``found``.

    Args:
        found: Frame numbers that exist on disk.
        start: First expected frame, inclusive.
        end: Last expected frame, inclusive.

    Returns:
        Missing frame numbers in ascending order.
    """
    return [frame for frame in range(start, end + 1) if frame not in found]
```

## 2. TypeScript / React style (from M4)

- ESLint + Prettier handle formatting
- Component files and names in `PascalCase` (`ShotPage.tsx`)
- Every API response has a declared `type`; no `any`
- One component, one job; data fetching lives in custom hooks (`useShot(id)`)

## 3. Database naming

- Lowercase plural table names (`render_versions`), `snake_case` columns
- Primary key `id`, foreign keys `<singular_table>_id` (`shot_id`)
- Timestamp columns end in `_at`, type `timestamptz`, stored in UTC
- Every schema change goes through an Alembic migration; never edit the database by hand

## 4. Git workflow

### 4.1 Branches

- `main`: always runnable, tests always pass
- Feature branches start from `main`, named `<type>/<roadmap-id>-<short-description>`:

```text
feat/m1-5-parse-filename
fix/m1-9-empty-dir-status
docs/m0-readme-badge
```

### 4.2 Commit messages (Conventional Commits)

```text
<type>(<scope>): <short description, imperative, lowercase start, no period>

(Optional) explain why the change was made

Refs: M1-5
```

| type | Use for |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `test` | Adding or changing tests only |
| `refactor` | Restructuring without changing behaviour |
| `docs` | Documentation |
| `chore` | Config, dependencies, housekeeping |
| `ci` | CI configuration |

Scope is the module name: `core`, `cli`, `api`, `db`, `worker`, `frontend`, `nuke`.

Examples:

```text
feat(core): parse frame number from EXR filename
test(core): cover bad padding and uppercase extension
fix(core): treat empty directory as failed instead of passed
docs: add system spec and roadmap
```

### 4.3 Commit size

One commit does **one thing**, and tests still pass afterwards. One roadmap item is usually 1–3 commits.

### 4.4 Pull requests

Even alone, use PRs: feature branch → push → open PR → green CI → self-review with the PR template → Squash and merge.

## 5. Definition of Done

A roadmap item is checked off only when all of these hold:

- [ ] The feature behaves as the SPEC describes
- [ ] It has tests and `uv run pytest` passes
- [ ] `uv run ruff check .` and `uv run ruff format --check .` report nothing
- [ ] If the spec changed, SPEC is updated
- [ ] If setup or usage changed, README is updated
- [ ] ROADMAP is checked off and a DEVLOG entry is written
- [ ] CI is green

## 6. When to update documents

| Document | When |
| --- | --- |
| `docs/DEVLOG.md` | **Every** session |
| `docs/ROADMAP.md` | Each finished item |
| `docs/SPEC.md` and `docs/SPEC.zh-TW.md` | When the spec changes — **update both languages together** (docs first, then code) |
| `docs/adr/` | When making or changing an important technical choice |
| `README.md` and `README.zh-TW.md` | When a milestone is done or setup/usage changes |
