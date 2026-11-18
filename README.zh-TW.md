# VFX Shot Manager

[English](README.md)

一個 VFX pipeline 工具：在交付前檢查渲染出來的 EXR 序列有沒有缺幀、範圍外的影格、檔名錯誤，並保留每一次檢查的紀錄。

> **狀態：開發初期（里程碑 M0）。** 目前只有下面的缺幀原型可以執行，其餘都是規劃中的設計，進度記錄在[路線圖](docs/ROADMAP.md)。

## 為什麼做這個

VFX 製作時，算圖農場偶爾會少算幾格、輸出到錯的資料夾，或檔名出錯。這些問題常常到合成或交付時才被發現。這個專案把人工打開資料夾檢查的工作，變成一行指令或一個按鈕，並為每次檢查留下報告。

## 目前可以執行的部分

```powershell
python main.py
```

```text
VFX Shot Manager
SH010
[1003, 1006]
```

`find_missing_frames` 用範例影格 `[1001, 1002, 1004, 1005]` 比對包含頭尾的範圍 `1001–1006`。

## 規劃中的系統

```text
Browser (React + TS) ──HTTP──▶ FastAPI ──▶ PostgreSQL ◀── Worker ──▶ 唯讀的渲染儲存空間
Terminal (vfxsm CLI) ─────────────────────────────────────┐   │
Nuke 面板（加分）─────────────────────────────────────────┴───┴──▶ core（純 Python，只用標準函式庫）
```

檢查核心不依賴任何框架或資料庫，所以 CLI、背景 worker 和 Nuke 等 DCC 工具都共用同一套邏輯。

| 里程碑 | 成果 | 狀態 |
| --- | --- | --- |
| M0 專案地基 | 套件結構、ruff、pytest、CI | 🚧 進行中 |
| M1 核心 + CLI | `vfxsm scan` 檢查真實資料夾並輸出 JSON 報告 | 規劃中 |
| M2 資料庫 + API | 用 REST API 管理鏡頭、渲染版本與檢查紀錄 | 規劃中 |
| M3 Worker | 用 PostgreSQL `SKIP LOCKED` 排程檢查、復原卡住的工作 | 規劃中 |
| M4 前端 | 在瀏覽器完成整個流程 | 規劃中 |
| M5 一鍵 Demo | `docker compose up` 加上範例資料 | 規劃中 |
| M6 Nuke 整合 | 在 Nuke 裡直接檢查 Write node 的輸出 | 規劃中 |

## 文件

- [系統規格書](docs/SPEC.zh-TW.md)：範圍、命名規範、架構、資料庫、API、測試與安全
- [路線圖](docs/ROADMAP.md)：里程碑與勾選清單（中英對照）
- [開發規範](CONTRIBUTING.zh-TW.md)：程式風格、Git 流程、完成定義
- [架構決策紀錄](docs/adr/)
- [開發日誌](docs/DEVLOG.md)（中英對照）

所有文件都有英文與繁體中文版本。

## 技術（規劃）

Python 3.12 · uv · ruff · pytest · FastAPI · SQLAlchemy · Alembic · PostgreSQL · React · TypeScript · Docker Compose · GitHub Actions
