# DEVLOG｜開發日誌

> Progress notes for each development session, newest first.
> 每次開發的進度紀錄，最新的在最上面。

## Starting a session (5 min)｜每次開工

1. Read **the top entry** below — "Next" / 「下次從這裡開始」\
   看下面**最上面一篇**的「下次從這裡開始」
2. Open `docs/ROADMAP.md` and find the first unchecked item\
   打開 `docs/ROADMAP.md`，找第一個沒打勾的項目
3. In the terminal / 終端機執行：

   ```powershell
   git status          # anything uncommitted? 有沒有沒 commit 的東西
   git log --oneline -5
   uv run pytest       # confirm a good state 確認目前狀態正常
   ```

4. Create a new branch and start｜開一個新分支開始做

## Ending a session (5 min)｜每次收工

Add a new entry at the top of the log below using this template.
在下面日誌最上方新增一篇，使用這個模板。

```markdown
## YYYY-MM-DD

**Done｜做了：** (roadmap ID + one sentence)
**Learned｜學到：** (new concepts, syntax)
**Blocked / questions｜卡住／疑問：** (unresolved issues)
**Next｜下次從這裡開始：** (be specific, e.g. "M1-7, scanner doesn't handle subfolders yet")
```
## 2026-11-26

**Done｜做了：** M1-1 to M1-3 — core exception hierarchy, immutable `FrameRange` dataclass, and `parse_range` for `<start>-<end>` text.
**Learned｜學到：** custom exceptions, dataclasses with `frozen=True`, `__post_init__`, `__contains__` and `__len__`, regular expressions with `fullmatch`, `pytest.raises`, `pytest.mark.parametrize`.
**Blocked / questions｜卡住／疑問：** None
**Next｜下次從這裡開始：** M1-4 — `compact_frames` to display frame lists such as `1001-1003,1005`.

---
## 2026-11-23

**Done｜做了：** M0 complete — uv project, src layout, unit tests, ruff, and GitHub Actions CI on Python 3.11 and 3.12 (PRs #1–#7). Added a ruleset requiring PRs and passing checks on `main`.
**Learned｜學到：** uv and lockfiles, pytest, ruff check vs format, GitHub Actions matrix builds, branch rulesets.
**Blocked / questions｜卡住／疑問：** None
**Next｜下次從這裡開始：** M1-1 and M1-2 — error types and FrameRange.

## 2026-11-18

**Done｜做了：** Wrote the system spec (SPEC, EN + ZH), the bilingual roadmap and dev log, contributing guide (EN + ZH), and ADR 0001 (EN + ZH).
寫好系統規格書（中英）、中英對照的路線圖與開發日誌、開發規範（中英）、第一份架構決策紀錄（中英）。

**Current state｜目前狀態：** `main.py` has `find_missing_frames`, which checks `[1001, 1002, 1004, 1005]` against `1001–1006` and prints `[1003, 1006]`. The `main.py` change, the README updates, and the new docs are not committed yet.
`main.py` 有 `find_missing_frames`，輸出 `[1003, 1006]`。`main.py` 的修改、README 和新文件都還沒 commit。

**Learned｜學到：** Besides frontend, backend, database, environment, and conventions, a system also needs scope, a glossary, a testing strategy, error handling, security, CI, a roadmap, and a progress log.
一個系統除了前後端、資料庫、環境、規範之外，還需要範圍、名詞表、測試策略、錯誤處理、安全、CI、路線圖和進度紀錄。

**Blocked / questions｜卡住／疑問：** None｜無

**Next｜下次從這裡開始：** Commit the current changes and these docs, then start ROADMAP **M0-1** (install uv).
先把目前的修改和這批文件 commit，然後開始 ROADMAP **M0-1** 安裝 uv。
