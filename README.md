# pptx-beautify-lock-Skill

**繁體中文 / English**

一個給 AI Agent 使用的 **PowerPoint 自動美化 Skill**，核心是「**內容 100% 凍結，只重新設計視覺層**」。

A cross-agent **PowerPoint visual redesign skill with a hard content lock**.

> **內容完全不改，視覺可以大幅重做。**  
> **Preserve presentation content exactly. Redesign only the visual layer.**

主要目標平台：

- Claude Code
- ChatGPT / Codex
- 其他支援 Agent Skills 或能讀取 `SKILL.md` 的 coding agents

---

## 核心契約 / Core contract

來源 `.pptx` 是唯一真實來源。

The source `.pptx` is the single source of truth.

### 內容凍結 — 絕對不能改 / Frozen content — MUST NOT change

- 投影片頁數與順序 / slide count and slide order
- 所有文字、標點、數字、單位、公式、符號與語言 / all visible text and symbols
- 表格結構、合併關係、列欄順序、cell values / table structure and values
- 圖表 categories、series、source values、formulas、embedded workbook data
- 圖片與媒體 payload、crop state / image/media bytes and crop state
- Speaker Notes / 備註文字
- embedded files / 嵌入檔案

AI 不得為了排版方便而：

- 改寫
- 摘要
- 翻譯
- 校正文法或拼字
- 新增或刪除
- 合併或拆頁
- 重排頁面

The agent must never rewrite, summarize, translate, spell-correct, add, delete, merge, split, or reorder source content.

### 視覺層 — 可以改 / Visual layer — MAY change

- 字型、字級、粗細、顏色 / typography
- 文字框位置、尺寸、內距 / text-box geometry
- 行距、段距、對齊 / spacing and alignment
- 物件位置與大小 / object position and size
- 留白、grid / whitespace and grid
- 表格欄寬、列高、padding、fill、border
- 圖表配色、字型、legend、axis、plot-area 等「不碰資料」的 styling
- 背景、陰影、border、accent、visual hierarchy
- 圖片位置與顯示尺寸；不得換圖或改 crop
- 修復 overlap、overflow、clipping、out-of-bounds

---

## 最重要的 Fail-closed 原則

如果內容塞不下，**不能改字或刪字**。

If content does not fit, **do not rewrite it**.

AI 應改用：

1. 重排 layout
2. 擴大可用區域
3. 減少 padding / margins
4. 重分配 whitespace
5. 移動或縮放其他物件
6. 調整 table geometry
7. 最後才在可讀範圍內降低字級

最終只有在驗證器輸出：

```text
CONTENT_LOCK_PASS=true
```

才可以交付。

---

## Repo 結構 / Repository layout

```text
.
├── README.md
├── INSTALL.md
├── AGENTS.md
├── CLAUDE.md
├── AI_BOOTSTRAP.md
├── requirements.txt
└── pptx-beautify-lock/
    ├── SKILL.md
    ├── references/
    │   ├── CONTENT_LOCK.md
    │   ├── DESIGN_RULES.md
    │   └── QA_RULES.md
    └── scripts/
        ├── pptx_content_lock.py
        └── verify_layout.py
```

---

## 最簡單用法 / Fastest use

未來只要：

1. 把 PPTX 給 AI
2. 貼上這個 GitHub repo URL
3. 下這段指令

```text
Read this repository and follow pptx-beautify-lock/SKILL.md.

啟用 CONTENT LOCK：內容 100% 凍結，只重新設計視覺層。
不要修改任何文字、數字、表格資料、圖表資料、圖片內容、備註、頁數或頁面順序。

可以全面修正：
字型、字級、位置、大小、留白、對齊、表格尺寸、色彩、背景、視覺階層、overlap、overflow、clipping。

完成後必須執行 content verification、layout QA 與可用時的 visual render QA。
只有 CONTENT_LOCK_PASS=true 才能交付。
```

---

## Claude Code / Codex 安裝

真正可安裝的 Skill 目錄是：

```text
pptx-beautify-lock/
```

詳細安裝方式請看：

```text
INSTALL.md
```

Typical patterns:

```text
~/.claude/skills/pptx-beautify-lock/
~/.codex/skills/pptx-beautify-lock/
```

若版本路徑不同，以當前 Claude Code / Codex 官方機制為準。

---

## 強制流程 / Mandatory pipeline

```text
input.pptx
   ↓
immutable backup / 保留原檔
   ↓
content snapshot / 內容快照
   ↓
render + inspect original slides
   ↓
visual-only redesign / 只改視覺
   ↓
layout QA + render QA
   ↓
content verification / 內容驗證
   ↓
PASS → final.pptx
FAIL → reject and repair
```

只靠 Prompt 說「不要改內容」不夠。這個 repo 內建 Python verifier，會以機器方式比對美化前後的 frozen content。

Prompt-only promises are not proof. The bundled verifier performs machine-readable semantic comparison.

---

## 設計目標 / Design objective

不是「沒有重疊」就算完成。

目標是：

- executive-ready / 可直接上台
- clean, modern, restrained
- clear visual hierarchy
- consistent typography and spacing
- readable tables and charts
- no unintended overlap / overflow / clipping
- consistent cross-slide design language
- native PowerPoint editability whenever possible

有效的輸出必須同時滿足：

1. **內容完全一致 / semantically identical**
2. **視覺顯著改善 / materially better designed**

---

## 重要限制 / Important limitation

只貼 GitHub URL 並不會自動賦予 AI 檔案系統、PowerPoint 編輯或程式執行能力。

Pasting the repo URL does not itself grant an AI file-system or PowerPoint-editing capabilities.

AI 仍然必須能：

- 讀取輸入 `.pptx`
- 修改或重新建立 `.pptx`
- 執行驗證腳本
- 最好能 render 投影片做 visual QA

如果環境做不到，AI 應明確說明限制，而不是假裝已安全完成。
