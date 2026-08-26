# Windows PPTX Beautifier — Offline

從 v0.7.0 起，Windows EXE 與 GitHub Skill 完全分離：

1. **Skill** — canonical source 仍是 `https://github.com/Space653000/pptx-beautify-lock-Skill`，給 Claude Code / Codex / ChatGPT 等 AI Agent 直接閱讀。
2. **PPTX-Beautify-Offline.exe** — 完全離線的本機 deterministic beautifier；執行時不呼叫 Claude、不呼叫 Codex、不讀 GitHub、不需要網路。
3. **BACKUP-pptx-beautify-lock-Skill.bat** — 獨立 Git 備份工具，與 EXE 無關。

## Offline EXE

介面只保留：

1. **輸入 PPTX**
2. **輸出 PPTX**
3. **美化風格**
4. **開始離線美化**

預設風格：Source-faithful、Technical Clean、Executive Minimal、Modern Minimal、Premium Tech。

## Local engine capabilities

離線 engine 目前做：

- semantic Content Lock，任何 protected content 差異即刪除輸出並 FAIL
- 空 placeholder 清理
- generic template placeholder artifact 以幾何方式移出畫布，保留 semantic text
- Traditional Chinese / English 安全字體正規化
- POWER / THD / HOHD 類 sibling table 視覺一致化
- 高信心 data-slide grid：summary + table + L/R evidence panels
- cover 品牌地形保護與 light/dark canvas 判定
- source-faithful accent discovery
- 不覆寫來源檔

## Important limitation

完全離線 EXE 沒有大型語言／視覺模型，因此它是**規則式、可重現、保守的版面與格式引擎**，不是 Claude / Codex 的離線替身。它適合大量工程簡報的結構清理與一致化；需要全新視覺概念、語意層次判斷、世界級 bespoke art direction 時，仍應讓 AI Agent 直接讀 canonical Skill URL。

## Runtime requirements

- Windows 10/11
- 不需要 Claude Code
- 不需要 Codex
- 不需要登入任何雲端 AI
- 不需要 Git
- 不需要另外安裝 Python
- 不需要網路

## Build gate

GitHub Actions 會安裝並封裝 `python-pptx`, Pillow, lxml 與 `pptx_content_lock.py`，建立：

```text
PPTX-Beautify-Offline.exe
```

Windows runner 必須實際執行：

```text
PPTX-Beautify-Offline.exe --portable-self-test
```

Self-test 會建立一份臨時 PPTX、離線美化、Content Lock 驗證並重新開啟輸出；未通過不得上傳 artifact。

## Standalone backup BAT

`BACKUP-pptx-beautify-lock-Skill.bat` 仍是另一個完全獨立工具。放到任意資料夾雙擊後，會把完整 Git repository 抓到 BAT 同層的 `pptx-beautify-lock-Skill\`。這個 BAT 需要 Git for Windows；它與 Offline EXE 沒有執行依賴。
