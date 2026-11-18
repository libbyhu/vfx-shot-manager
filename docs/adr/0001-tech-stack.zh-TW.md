# ADR 0001：技術選擇

[English](0001-tech-stack.md) | 繁體中文

- 日期：2026-11-18
- 狀態：已接受

> ADR（Architecture Decision Record）記錄「為什麼這樣選」。之後有人問「為什麼不用 X」時，答案在這裡。

## 背景

目標是一個涵蓋 Python、檔案系統處理、資料庫與 API 設計的 VFX pipeline 工具，並且能延伸到 DCC 工具。這也是一個學習專案：維護者剛開始學 Python，已經有 Java Spring Boot 和前端的經驗。

## 決定

| 層 | 選擇 | 考慮過的替代方案 | 為什麼 |
| --- | --- | --- | --- |
| 核心語言 | Python | — | VFX 業界與所有主要 DCC 的腳本語言 |
| 核心相容性 | 只用標準函式庫、相容 Python 3.11 | 使用第三方套件（如 `fileseq`） | 可以直接在 Nuke 等 DCC 內建的 Python 裡 import；自己實作序列處理也是學習重點 |
| 套件管理 | uv | pip + venv、Poetry | 快、一個工具處理虛擬環境與依賴、設定集中在 `pyproject.toml` |
| 後端框架 | FastAPI | Flask、Django | 型別提示驅動、自動產生 API 文件、跟 Spring Boot 的概念（路由、DTO、依賴注入）容易對照 |
| 資料庫 | PostgreSQL | SQLite | 需要 `FOR UPDATE SKIP LOCKED` 做工作佇列、JSONB 存報告；業界常用 |
| ORM | SQLAlchemy 2 + Alembic | 直接寫 SQL | Python 業界標準；migration 讓 schema 變更可追蹤 |
| 工作佇列 | PostgreSQL 資料表 + SKIP LOCKED | Celery + Redis、RQ | v1 流量小，少一個服務；佇列原理看得見，容易除錯 |
| 前端 | React + TypeScript | PySide6 桌面程式、伺服器端渲染樣板 | 協調人員不用安裝軟體，用瀏覽器就能操作；PySide 改用在 M6 的 Nuke 面板 |
| 部署 | Docker Compose（本機） | 雲端部署 | 任何人都能用一行指令重現；雲端不在 v1 範圍 |

## 影響

- 好處：核心可在 CLI、worker、DCC 共用；每一層都能單獨測試。
- 代價：Docker 和 PostgreSQL 增加學習量。所以 M1 刻意不需要資料庫，先把 Python 核心做紮實。
- 如果之後流量變大，或需要排程、重試策略，再評估換成 Celery 或 RQ，並新增一份 ADR。
