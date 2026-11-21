# ROADMAP｜開發路線圖

> Project progress is tracked in this file only (bilingual, so each item has a single checkbox). An item is checked off in the same commit as its code, once it meets the definition of done in `CONTRIBUTING.md`. Every milestone ends in a runnable, demo-able state.
> 專案進度只記錄在這份檔案（中英對照，每個項目只有一個勾選框）。項目符合 `CONTRIBUTING.md` 的完成定義後，與程式碼在同一個 commit 中打勾。每個里程碑結束時，系統都是可以執行、可以展示的狀態。

## Overview｜總覽

| Milestone 里程碑 | Outcome 成果 | Size 大小 |
| --- | --- | --- |
| M0 Foundation 專案地基 | Standard Python layout, lint, tests, green CI<br>標準 Python 專案結構、lint、測試、CI 綠燈 | S |
| M1 Core + CLI 核心 + CLI | `vfxsm scan` checks real folders and writes JSON<br>`vfxsm scan` 檢查真實資料夾並輸出 JSON | L |
| M2 Database + API 資料庫 + API | Create shots, register versions, (synchronous) checks over HTTP<br>用 API 建立鏡頭、登記版本、（同步）檢查 | L |
| M3 Worker 背景 Worker | Checks run in an async queue with stale-job recovery<br>檢查改成非同步佇列，可以復原卡住的工作 | M |
| M4 Frontend 前端 | Whole workflow in the browser<br>網頁完成整個流程 | L |
| M5 One-command demo 一鍵 Demo | `docker compose up` demo, GIF in README<br>`docker compose up` 就能展示，README 有 GIF | M |
| M6 Nuke integration Nuke 整合（加分） | Check a Write node from inside Nuke<br>Nuke 裡選 Write node 直接檢查 | M |

Size is relative effort: S < M < L.
大小表示相對工作量：S < M < L。

---

## M0 Foundation｜專案地基

**Goal:** turn a single `main.py` into a proper Python project. Every later feature grows on this skeleton.
**目標：** 把一個 `main.py` 變成正式的 Python 專案，之後所有功能都長在這個骨架上。

- [x] **M0-1** Install `uv`; create `pyproject.toml` with `uv init --package` or by hand, Python `>=3.11`\
  安裝 `uv`，用 `uv init --package` 或手寫 `pyproject.toml`，Python 版本設 `>=3.11`
- [x] **M0-2** Create `src/vfx_shot_manager/` and `tests/` (layout in SPEC §6.5)\
  建立 `src/vfx_shot_manager/` 和 `tests/`（結構見 SPEC §6.5）
- [x] **M0-3** Move `find_missing_frames` from `main.py` to `src/vfx_shot_manager/core/validator.py`; delete `main.py`\
  把 `find_missing_frames` 搬到 `core/validator.py`，刪除 `main.py`
- [x] **M0-4** Add type hints: `def find_missing_frames(found: set[int], start: int, end: int) -> list[int]:`\
  加上型別提示
- [ ] **M0-5** First test `tests/core/test_validator.py`; `uv run pytest` passes\
  寫第一個測試，`uv run pytest` 通過
- [ ] **M0-6** Configure `ruff` in `pyproject.toml`; `uv run ruff check .` and `uv run ruff format .` are clean\
  設定 `ruff`，檢查與格式化都沒有錯誤
- [ ] **M0-7** Add `sample_renders/` to `.gitignore`\
  `.gitignore` 加上 `sample_renders/`
- [ ] **M0-8** Create `.github/workflows/ci.yml` running ruff and pytest on push\
  建立 CI：push 時跑 ruff 和 pytest
- [ ] **M0-9** Add the CI badge to both READMEs\
  兩份 README 加上 CI 徽章

**Concepts covered｜涵蓋觀念：** virtual environments, `pyproject.toml`, packages vs modules, how `import` finds files, type hints, pytest basics, `assert`, YAML, what CI is.
虛擬環境、`pyproject.toml`、套件與模組、`import` 怎麼找檔案、型別提示、pytest 基本寫法、`assert`、YAML、CI 的概念。

**Done when｜驗收：** GitHub Actions shows a green check. GitHub 的 Actions 顯示綠勾。

---

## M1 Core + CLI｜核心驗證 + CLI

**Goal:** check a real folder from the terminal with no database and no web app. This is the heart of the system; every later milestone reuses it.
**目標：** 不需要資料庫和網頁，就能在終端機檢查真的資料夾。這是系統的心臟，之後每個里程碑都會重用它。

### Ranges and naming｜範圍與命名

- [ ] **M1-1** `core/errors.py`: custom exception classes (SPEC §13)\
  自訂例外類別
- [ ] **M1-2** `core/frame_range.py`: `FrameRange` dataclass (start, end, `__contains__`, `__len__`, validates start ≤ end)\
  `FrameRange` dataclass，驗證起點 ≤ 終點
- [ ] **M1-3** `parse_range("1001-1006")` → `FrameRange`\
  把字串解析成範圍
- [ ] **M1-4** `compact_frames([1001, 1002, 1003, 1005])` → `"1001-1003,1005"`\
  把影格清單壓縮成業界常見寫法
- [ ] **M1-5** `core/naming.py`: filename regex; `parse_filename()` returns `ParsedName` or `None`\
  檔名 regex，解析成功回傳 `ParsedName`，失敗回傳 `None`
- [ ] **M1-6** Tests for all of the above (use `pytest.mark.parametrize` for many cases at once)\
  上面每個函式的測試（用 `parametrize` 一次測很多案例）

### Scanning and validation｜掃描與驗證

- [ ] **M1-7** `core/scanner.py`: list a folder with `pathlib`; raise `DirectoryUnreadableError` if missing or unreadable\
  用 `pathlib` 列出資料夾；不存在或沒權限時丟出例外
- [ ] **M1-8** `core/report.py`: `Report` dataclass and `to_dict()` in the SPEC §7.4 format\
  `Report` dataclass 與轉成 SPEC §7.4 格式
- [ ] **M1-9** `core/validator.py`: `validate(entries, expected)` → `Report`, classifying every finding (§5.3) and setting the status (§5.4)\
  分類所有 finding、判定狀態
- [ ] **M1-10** `core/paths.py`: `resolve_under_root(root, relative)`, raising `PathOutsideRootError` on escape\
  根目錄解析，跳出根目錄就丟出例外
- [ ] **M1-11** Filesystem tests with `tmp_path` covering the SPEC §15 required cases\
  用 `tmp_path` 寫檔案系統測試，覆蓋必測清單

### CLI

- [ ] **M1-12** `cli.py`: `vfxsm scan` with `argparse`\
  用 `argparse` 做 `vfxsm scan`
- [ ] **M1-13** `--json` writes a report file\
  `--json` 輸出報告檔
- [ ] **M1-14** Exit codes 0 / 1 / 2\
  exit code 0 / 1 / 2
- [ ] **M1-15** `vfxsm make-sample` generates fake sequences (`--skip` chooses missing frames)\
  產生假序列，可以指定缺哪幾格
- [ ] **M1-16** Register the command in `pyproject.toml` so `uv run vfxsm` works\
  在 `pyproject.toml` 註冊指令
- [ ] **M1-17** CLI tests\
  CLI 測試
- [ ] **M1-18** CI adds `mypy src/vfx_shot_manager/core` and coverage\
  CI 加上 mypy 和覆蓋率
- [ ] **M1-19** Update both READMEs: "What works today" shows CLI usage and output\
  更新兩份 README 的「目前可用功能」
- [ ] **M1-20** Tag `v0.1.0` and create a GitHub Release\
  打 tag `v0.1.0` 並建立 Release

**Concepts covered｜涵蓋觀念：** `dataclass`, `set` vs `list` performance, regular expressions, `pathlib`, exceptions (`try/except/raise`), custom exceptions, `argparse`, `sys.exit`, the `json` module, pytest fixtures and parametrize, `tmp_path`.
`dataclass`、`set` 與 `list` 的效能差異、正規表示式、`pathlib`、例外處理、自訂例外、`argparse`、`sys.exit`、`json` 模組、pytest fixture 與 parametrize、`tmp_path`。

**Done when｜驗收：**

```powershell
uv run vfxsm make-sample sample_renders/DEMO/SEQ010/SH010/lighting/beauty/v001 --shot SH010 --task lighting --output beauty --range 1001-1006 --skip 1003,1006
uv run vfxsm scan sample_renders/DEMO/SEQ010/SH010/lighting/beauty/v001 --shot SH010 --task lighting --output beauty --range 1001-1006
# FAILED, Missing: 1003,1006, exit code 1
```

---

## M2 Database + API｜資料庫 + API

**Goal:** store data and operate over HTTP. In this step the API runs the check **synchronously**; M3 moves it to a background job. Make it work first, then make it better.
**目標：** 資料存起來，用 HTTP 操作。這一步先讓 API **同步**執行檢查，M3 再拆成背景工作。先求能動，再求好。

- [ ] **M2-1** `compose.yaml` with only `db` (PostgreSQL 16); `docker compose up -d db`\
  `compose.yaml` 先只放資料庫
- [ ] **M2-2** `.env.example` and `config.py` (pydantic-settings)\
  環境變數範例與設定讀取
- [ ] **M2-3** `db/models.py`: five tables (SPEC §7) with UNIQUE and CHECK constraints\
  五張表，含 UNIQUE 和 CHECK 約束
- [ ] **M2-4** Initialise Alembic, generate the first migration, `alembic upgrade head` succeeds\
  初始化 Alembic，第一個 migration 成功
- [ ] **M2-5** `api/main.py` + `/health`
- [ ] **M2-6** `api/schemas.py`: Pydantic request and response models\
  Pydantic 請求與回應模型
- [ ] **M2-7** GET / POST for projects, sequences, shots\
  專案、場次、鏡頭的 GET / POST
- [ ] **M2-8** `PATCH /shots/{id}` to change the range\
  修改範圍
- [ ] **M2-9** Register versions; validate that `root_key` exists and `relative_path` is neither absolute nor contains `..`\
  登記版本並驗證根目錄與相對路徑
- [ ] **M2-10** Unified error format (SPEC §8.1): 404, 409, 422\
  統一錯誤格式
- [ ] **M2-11** `POST /versions/{id}/validation-runs`: call core **synchronously** for now and store the result\
  暫時同步呼叫 core，直接存結果
- [ ] **M2-12** `GET /validation-runs/{id}`, history list, `report.json` download\
  讀取結果、歷史列表、下載
- [ ] **M2-13** API tests (test database)\
  API 測試（測試用資料庫）
- [ ] **M2-14** CI adds a PostgreSQL service\
  CI 加上 PostgreSQL
- [ ] **M2-15** Write `docs/adr/0002-…` (EN + ZH) for any design change made in this milestone\
  寫第二份 ADR（中英）記錄這階段的設計變更

**Concepts covered｜涵蓋觀念：** HTTP methods and status codes, REST design, Pydantic, SQLAlchemy ORM, database constraints, why migrations exist, dependency injection (FastAPI `Depends`), Docker basics, environment variables.
HTTP 方法與狀態碼、REST 設計、Pydantic、SQLAlchemy ORM、資料庫約束、migration 的意義、依賴注入、Docker 基本操作、環境變數。

**Done when｜驗收：** at `http://localhost:8000/docs`, create project → sequence → shot → version → check, and get a report missing `1003, 1006`.
打開 `http://localhost:8000/docs`，依序建立專案 → 場次 → 鏡頭 → 版本 → 檢查，得到缺 `1003, 1006` 的報告。

---

## M3 Background worker｜背景 Worker

**Goal:** real render folders may hold tens of thousands of files on network storage, so scanning is slow. Move checks out of the API.
**目標：** 真實渲染資料夾可能有上萬個檔案、放在網路磁碟上，掃描很慢。把檢查從 API 拆出去。

- [ ] **M3-1** `POST validation-runs` only creates a `queued` run and returns 202\
  只建立 `queued` 的 run，回 202
- [ ] **M3-2** `worker.py` loop: claim (`FOR UPDATE SKIP LOCKED`) → run → write back\
  worker 迴圈：認領 → 執行 → 寫回
- [ ] **M3-3** Stale recovery: runs stuck in `running` go back to `queued`\
  卡住復原
- [ ] **M3-4** Graceful shutdown (Ctrl+C finishes the current run)\
  優雅關閉
- [ ] **M3-5** Logging with `run_id` on every line\
  每筆 log 帶 `run_id`
- [ ] **M3-6** `compose.yaml` adds `api` and `worker`; the worker mounts `sample_renders` with `:ro`\
  加入 api、worker 服務，唯讀掛載
- [ ] **M3-7** Worker integration tests: two workers never claim the same run; stuck runs recover\
  整合測試：兩個 worker 不搶同一筆、卡住會復原

**Concepts covered｜涵蓋觀念：** sync vs async, processes, database transactions and locks, why `SKIP LOCKED`, the logging module, signal handling.
同步與非同步、行程、資料庫 transaction 與 lock、為什麼要 `SKIP LOCKED`、logging 模組、訊號處理。

**Done when｜驗收：** queuing returns 202 immediately; a few seconds later the status is `failed`. Kill the worker mid-run, restart it, and the run is processed again.
送出檢查立刻回 202，幾秒後狀態變成 `failed`。執行中 kill 掉 worker 再重開，工作會被重新處理。

---

## M4 Frontend｜前端

**Goal:** a coordinator completes the whole workflow without touching a terminal.
**目標：** 協調人員不用碰終端機就能完成整個流程。

- [ ] **M4-1** `npm create vite@latest frontend -- --template react-ts`
- [ ] **M4-2** API client (a thin `fetch` wrapper typed to match backend schemas)\
  API client，型別對應後端
- [ ] **M4-3** React Router + TanStack Query setup\
  路由與 TanStack Query 設定
- [ ] **M4-4** Project list page + create form\
  專案列表與建立表單
- [ ] **M4-5** Project page: sequences and shots\
  專案頁：場次與鏡頭
- [ ] **M4-6** Shot page: versions table, register form, Validate button\
  鏡頭頁：版本表格、登記表單、Validate 按鈕
- [ ] **M4-7** Poll run status (`refetchInterval`, stop when finished)\
  輪詢狀態，完成就停
- [ ] **M4-8** Report page: summary, missing frames, each finding type, download\
  報告頁
- [ ] **M4-9** Loading / empty / error states on every page\
  每頁的讀取中、空資料、錯誤狀態
- [ ] **M4-10** CORS on the backend\
  後端加 CORS
- [ ] **M4-11** CI adds `npm run build`\
  CI 加上前端建置

**Concepts covered｜涵蓋觀念：** TypeScript types, TanStack Query caching and polling, and keeping frontend and backend data shapes aligned.
TypeScript 型別、TanStack Query 的快取與輪詢、前後端資料格式對齊。

**Done when｜驗收：** success criteria 2 and 3 in SPEC §1.4, entirely in the browser.
完全用瀏覽器走完 SPEC §1.4 的成功標準 2 和 3。

---

## M5 One-command demo and docs｜一鍵 Demo 與文件

**Goal:** a first-time visitor understands the project and runs it within five minutes.
**目標：** 讓第一次看到專案的人五分鐘內看懂、跑起來。

- [ ] **M5-1** `compose.yaml` adds `frontend`; all four services start together\
  四個服務一起啟動
- [ ] **M5-2** Seed script: demo project, shot, version, and a sample sequence with missing frames\
  seed 腳本自動建立示範資料
- [ ] **M5-3** Clone into a fresh folder, follow the README from scratch, fix everything that blocks\
  在全新資料夾從頭照 README 做一次
- [ ] **M5-4** Record a demo GIF (missing frames → add files → recheck → passed) for the README\
  錄 demo GIF
- [ ] **M5-5** README: architecture diagram, tech choices, lessons learned\
  README 加上架構圖、技術選擇、開發心得
- [ ] **M5-6** Sync `README.zh-TW.md`\
  同步中文 README
- [ ] **M5-7** Tag `v1.0.0`, GitHub Release\
  打 tag `v1.0.0`
- [ ] **M5-8** GitHub repo settings: About text, topics (`vfx`, `pipeline`, `python`, `fastapi`)\
  repo 的 About 描述與 topics

**Done when｜驗收：** a friend gets it running using only the README.
請一個朋友只看 README 把系統跑起來。

---

## M6 Nuke integration (bonus)｜Nuke 整合（加分）

**Goal:** run the same core inside a DCC, so compositors can check a render without leaving Nuke.
**目標：** 讓同一套核心在 DCC 裡執行，合成師不用離開 Nuke 就能檢查渲染結果。

- [ ] **M6-1** Check Nuke's bundled Python version; confirm core imports there\
  確認 Nuke 內建的 Python 版本，core 能 import
- [ ] **M6-2** `nuke/` folder with a `menu.py` that registers a menu\
  `menu.py` 註冊選單
- [ ] **M6-3** Selected Write node → read its `file` path and frame range → call core\
  選取 Write node → 讀出路徑和範圍 → 呼叫 core
- [ ] **M6-4** Show the result with `nuke.message` or a simple PySide panel\
  用訊息框或 PySide 面板顯示結果
- [ ] **M6-5** (Optional) Call the API instead so results are stored in the system\
  （選做）改成呼叫 API，結果也存進系統
- [ ] **M6-6** Record a GIF of it working inside Nuke\
  錄一段在 Nuke 裡操作的 GIF

**Concepts covered｜涵蓋觀念：** DCC Python APIs, how `menu.py` / `init.py` load, `NUKE_PATH`, PySide (Qt) basics.
DCC 的 Python API、`menu.py` / `init.py` 載入機制、`NUKE_PATH`、PySide 基礎。

---

## Later (after v1, see SPEC §17)｜之後

- [ ] Inspect EXR headers with OpenEXR｜用 OpenEXR 讀 header 檢查內容
- [ ] Mock ShotGrid / Flow integration｜串接 ShotGrid / Flow 的 mock
- [ ] User login｜使用者登入
