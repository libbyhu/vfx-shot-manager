# 開發規範（CONTRIBUTING）

[English](CONTRIBUTING.md) | 繁體中文

> 本專案的所有修改都遵守這份規範，即使只有一位維護者也一樣。

## 1. Python 程式風格

| 規則 | 說明 |
| --- | --- |
| 格式 | 交給 `ruff format`，不手動排版 |
| Lint | `ruff check` 不能有錯誤 |
| 命名 | 變數與函式 `snake_case`、類別 `PascalCase`、常數 `UPPER_SNAKE_CASE`、私有用 `_` 開頭 |
| 型別提示 | 所有函式的參數和回傳值都要寫 |
| Docstring | 公開函式寫 Google 風格 docstring，說明參數、回傳、會丟的例外 |
| 路徑 | 用 `pathlib.Path`，不用字串拼接，不用 `os.path` |
| 輸出 | 函式庫裡不用 `print`，用 `logging`；只有 `cli.py` 可以印給人看 |
| 全域變數 | 不用。需要的資料用參數傳進去 |
| 執行入口 | 可執行的檔案用 `if __name__ == "__main__":` |
| 比對大量資料 | 用 `set`，不在 `list` 裡用 `in` 找 |
| 字串 | 用 f-string |
| core 的限制 | `core/` 只能 import 標準函式庫 |

範例：

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

## 2. TypeScript / React 風格（M4 之後）

- ESLint + Prettier 交給工具處理
- 元件檔名與元件名稱 `PascalCase`（`ShotPage.tsx`）
- API 回應一律定義 `type`，不用 `any`
- 一個元件負責一件事；資料請求放在自訂 hook（`useShot(id)`）

## 3. 資料庫命名

- 表名小寫複數（`render_versions`）、欄位 `snake_case`
- 主鍵 `id`、外鍵 `<表單數>_id`（`shot_id`）
- 時間欄位 `_at` 結尾、型別 `timestamptz`、存 UTC
- 任何 schema 變更都要透過 Alembic migration，不手動改資料庫

## 4. Git 工作流程

### 4.1 分支

- `main`：永遠可以執行、測試通過
- 功能分支從 `main` 開，名稱 `<類型>/<roadmap 編號>-<簡述>`：

```text
feat/m1-5-parse-filename
fix/m1-9-empty-dir-status
docs/m0-readme-badge
```

### 4.2 Commit 訊息（Conventional Commits）

```text
<type>(<scope>): <簡短描述，英文、祈使句、小寫開頭、不加句點>

（可選）說明為什麼要這樣改

Refs: M1-5
```

| type | 用途 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 修 bug |
| `test` | 只加或改測試 |
| `refactor` | 不改變行為的重構 |
| `docs` | 文件 |
| `chore` | 設定、依賴、雜項 |
| `ci` | CI 設定 |

scope 用模組名：`core`、`cli`、`api`、`db`、`worker`、`frontend`、`nuke`。

範例：

```text
feat(core): parse frame number from EXR filename
test(core): cover bad padding and uppercase extension
fix(core): treat empty directory as failed instead of passed
docs: add system spec and roadmap
```

### 4.3 Commit 的大小

一個 commit 做**一件事**、而且做完之後測試還是過的。ROADMAP 的一個項目通常是 1–3 個 commit。小 commit 沒有問題，問題是沒有地圖；現在地圖在 `docs/ROADMAP.md`。

### 4.4 Pull Request

就算自己一個人，也走 PR：功能分支 → push → 開 PR → CI 綠燈 → 自己照 PR 模板檢查 → Squash and merge。

## 5. 完成定義（Definition of Done）

一個 ROADMAP 項目要全部符合才能打勾：

- [ ] 功能照 SPEC 的規格運作
- [ ] 有測試，`uv run pytest` 全過
- [ ] `uv run ruff check .` 和 `uv run ruff format --check .` 沒有錯誤
- [ ] 如果改了規格，SPEC 已經更新
- [ ] 如果改了安裝或使用方式，README 已經更新
- [ ] ROADMAP 打勾、DEVLOG 寫了一筆
- [ ] CI 綠燈

## 6. 文件什麼時候更新

| 文件 | 更新時機 |
| --- | --- |
| `docs/DEVLOG.md` | **每次**收工 |
| `docs/ROADMAP.md` | 每完成一個項目 |
| `docs/SPEC.md` 與 `docs/SPEC.zh-TW.md` | 規格改變時，**兩個語言一起改**（先改文件再改程式） |
| `docs/adr/` | 做了重要的技術選擇或改變 |
| `README.md` 與 `README.zh-TW.md` | 里程碑完成、或安裝與使用方式改變時 |
