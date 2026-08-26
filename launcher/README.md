# Windows GUI / 一鍵選檔介面

`PPTX Beautify Lock` 提供 Windows 檔案選擇 GUI，讓使用者不用每次手打 prompt。

## Recommended production mode / 建議模式

**Dual: Claude → Codex**

1. Claude Code 執行主要 layout/design/refactor。
2. Codex 做獨立 full-deck release review，必要時修復。
3. Launcher 再跑本機 Content/Theme/Layout/Lint guards。
4. `final_report.txt` 缺任何 v0.6 Gate 就不宣稱成功。

也可以單獨選 Claude Code 或 Codex。

## Requirements

- Windows 10/11
- Git for Windows
- Python 3.11+，或下載 GitHub Actions 產出的 `PPTX-Beautify-Lock.exe`
- 已登入至少一個：
  - Claude Code CLI (`claude`)
  - Codex CLI (`codex`)
- Dual mode 需要兩者都已登入
- PowerPoint 或 LibreOffice/其他可信 renderer 可提升實際 render fidelity

## Run from source

雙擊：

```text
PPTX-Beautify-Lock.cmd
```

或：

```powershell
python launcher\pptx_beautify_gui.py
```

## Portable EXE

GitHub Actions workflow：

```text
build-windows-launcher
```

會在 Windows runner 產生：

```text
PPTX-Beautify-Lock.exe
```

從 Actions 的 `PPTX-Beautify-Lock-Windows` artifact 下載即可。

## UI workflow

1. **選擇來源 PPTX** — source 永不覆寫。
2. 選擇輸出資料夾。
3. 選擇 Agent 模式。
4. 點 **安裝 / 更新 Skill**。
5. 點 **頂級美化**。
6. Final 預設命名：

```text
<原檔名>__TOP_TIER_FINAL.pptx
```

QA evidence 放在：

```text
<輸出資料夾>\.pptx_beautify_work\...
```

## Quality policy

Production launcher 會要求：

- Content Lock
- Theme / Deck Identity
- empty placeholder removal
- Traditional Chinese + English font portability
- sibling data-slide parity（例如 POWER / THD / HOHD）
- full-deck rerender after every repair
- three complete full-deck review passes
- Global Design Jury
- no-regression release

核心原則：

> **Fix A without breaking B.**

任何局部改善造成其他已通過頁面退化，整份 deck 不得 release。

## Backup

執行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\backup_to_windows.ps1
```

預設備份到：

```text
C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil
```

中央 Skill Catalog 會同步備份到：

```text
C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil\_catalog\Claude-code-ChatGPT-Codex---SKILL
```

備份採 fast-forward only；遇到本地未提交變更會停止，不會強制覆蓋。
