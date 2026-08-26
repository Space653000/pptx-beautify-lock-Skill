# Windows PPTX Beautifier / Windows 投影片美化介面

v0.6.2 起，產品邊界固定拆成三件互不混合的東西：

1. **Skill** — 永遠以 GitHub repository 為 canonical source：
   `https://github.com/Space653000/pptx-beautify-lock-Skill`
2. **PPTX-Beautify.exe** — 只負責美化 PowerPoint；不安裝 Skill、不更新 Skill、不備份 GitHub。
3. **BACKUP-pptx-beautify-lock-Skill.bat** — 獨立雙擊備份工具，只負責把 GitHub repository 抓到 BAT 所在資料夾。

## PPTX-Beautify.exe

GUI 只保留三個使用者設定：

1. **輸入 PPTX** — 可選任意 `.pptx`。
2. **輸出 PPTX** — 可另存到任意資料夾、任意檔名；禁止覆寫來源檔。
3. **美化風格** — 可從預設值選擇，也可直接輸入自訂風格。

然後按 **開始美化**。

EXE 會自動尋找可用的 AI Agent：

- 優先 Claude Code CLI (`claude`)
- 若沒有 Claude Code，改用 Codex CLI (`codex`)

EXE 不安裝或複製 Skill。它會在工作 prompt 中要求 AI **直接開啟並閱讀 canonical GitHub Skill URL**，再依最新版 main 規則處理簡報。

## Style presets

- 自動（忠於原稿 / Source-faithful）
- 專業技術（Technical Clean）
- 商務簡潔（Executive Minimal）
- 現代極簡（Modern Minimal）
- 高階科技簡報（Premium Tech, preserve source palette）

Combobox 可直接輸入其他自訂風格。

## Requirements

- Windows 10/11
- 已安裝並登入至少一個 AI Agent：Claude Code 或 Codex CLI
- Agent 執行時需要能存取 canonical GitHub Skill URL

EXE 本身不要求 Git，也不要求另外安裝 Python。

## Build

GitHub Actions workflow：

```text
build-windows-launcher
```

會產生：

```text
PPTX-Beautify.exe
```

Build 必須先實際執行：

```text
PPTX-Beautify.exe --portable-self-test
```

確認 EXE 內沒有 Skill installer、GitHub backup、repo bootstrap 等混合責任，才允許 artifact upload。

## Standalone backup BAT

把：

```text
BACKUP-pptx-beautify-lock-Skill.bat
```

放到任何 Windows 資料夾並雙擊。

它會在 BAT 同層建立或更新：

```text
pptx-beautify-lock-Skill\
```

來源固定是：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill.git
```

BAT 使用完整 `git clone`，所以會保留 Git repository 與 history；再次執行時採 `fetch --all --tags --prune` + `pull --ff-only`，不會強制覆寫本地修改。
