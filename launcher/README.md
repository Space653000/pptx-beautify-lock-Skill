# Windows PPTX Beautifier — Offline-first v0.7.1

Windows EXE、GitHub Skill、Backup BAT 維持三個完全分離的產品邊界：

1. **Skill** — canonical source 仍是 `https://github.com/Space653000/pptx-beautify-lock-Skill`，給 Claude Code / Codex / ChatGPT 等 AI Agent 直接閱讀。
2. **PPTX-Beautify-Offline.exe** — 本機 deterministic beautifier。美化本身不依賴網路或雲端 AI；若有網路，只做可選的 GitHub engine 更新檢查。
3. **BACKUP-pptx-beautify-lock-Skill.bat** — 獨立 Git 備份工具，與 EXE 無關。

## EXE 介面

只保留：

1. **輸入 PPTX**
2. **輸出 PPTX**
3. **美化風格**
4. **開始美化**

預設風格：Source-faithful、Technical Clean、Executive Minimal、Modern Minimal、Premium Tech。

## v0.7.1：成功必須等於真的有檔案

舊版可能出現 Log 已寫 `OFFLINE_BEAUTIFY_PASS=true`，但使用者在指定位置找不到輸出檔的假成功風險。v0.7.1 改成兩階段交付：

```text
source.pptx
→ 產生同資料夾 temporary candidate
→ Content Lock
→ candidate reopen / slide-count verification
→ atomic os.replace(candidate, final)
→ final exists / size / reopen verification
→ SHA-256
→ 才允許 OFFLINE_BEAUTIFY_PASS=true
```

成功 Log 至少必須看到：

```text
FINAL_OUTPUT_EXISTS=true
FINAL_OUTPUT_REOPEN_PASS=true
FINAL_OUTPUT_BYTES=<positive integer>
FINAL_OUTPUT_SHA256=<sha256>
FINAL_OUTPUT_PATH=<exact path>
OFFLINE_BEAUTIFY_PASS=true
```

只要 final output 不存在、為 0 bytes、無法重新開啟、slide count 不符，全部 FAIL CLOSED，不顯示成功。

## Optional update channel

美化引擎仍可完全離線工作；網路不是必要條件：

```text
BEAUTIFY_OFFLINE=true
CLOUD_AI_ENABLED=false
NETWORK_REQUIRED=false
OPTIONAL_UPDATE_CHECK=true
```

當有網路時，EXE 會依使用者指定的 stable update branch 檢查：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill/tree/fix/separate-skill-exe-backup-v062
```

實際流程會先透過 GitHub branch API 取得該 branch 的 commit SHA，再從同一 SHA 讀取：

```text
launcher/update_manifest.json
launcher/pptx_offline_engine.py
```

規則：

- remote engine version **高於**目前有效版本：下載到 `%LOCALAPPDATA%\PPTXBeautifyOffline\engine_updates\`，下次即使離線也可使用已快取版本。
- remote version 相同或更舊：不更新，**禁止降級**。
- 沒網路、DNS/Proxy/Firewall 阻擋：`UPDATE_CHECK=offline_skip`，立即使用內建或已快取 engine，正常美化。
- remote engine 要求更高 launcher version：不硬套，Log `UPDATE_STATUS=new_exe_required`，繼續使用相容版本。

Windows 執行中的 EXE 不直接覆寫自己；自動更新的是 **beautification engine / rules package**。若未來 launcher/UI 本身需要升級，manifest 會要求新版 EXE，避免把不相容 Python engine 強塞進舊 shell。

`fix/separate-skill-exe-backup-v062` 已被定義為 stable update channel；GitHub Action `sync-update-channel` 會在 `main` 正式更新後 fast-forward 該 branch，避免舊 branch 造成降級。

## Local engine capabilities

離線 engine 目前做：

- semantic Content Lock，任何 protected content 差異即 FAIL
- 空 placeholder 清理
- generic template placeholder artifact 以幾何方式移出畫布，保留 semantic text
- Traditional Chinese / English 安全字體正規化
- POWER / THD / HOHD 類 sibling table 視覺一致化
- 高信心 data-slide grid：summary + table + L/R evidence panels
- cover 品牌地形保護與 light/dark canvas 判定
- source-faithful accent discovery
- 不覆寫來源檔

## Important limitation

本機 EXE 沒有大型語言／視覺模型，因此它是**規則式、可重現、保守的版面與格式引擎**，不是 Claude / Codex 的離線替身。它適合大量工程簡報的結構清理與一致化；需要全新視覺概念、語意層次判斷、世界級 bespoke art direction 時，仍應讓 AI Agent 直接讀 canonical Skill URL。

## Runtime requirements

- Windows 10/11
- 不需要 Claude Code
- 不需要 Codex
- 不需要登入任何雲端 AI
- 不需要 Git
- 不需要另外安裝 Python
- **不需要網路即可美化**；有網路時只做可選更新檢查

## Build gate

GitHub Actions 會安裝並封裝 `python-pptx`, Pillow, lxml、Content Lock、offline runtime 與 updater，建立：

```text
PPTX-Beautify-Offline.exe
```

Windows runner 必須實際執行：

```text
PPTX-Beautify-Offline.exe --portable-self-test
```

Self-test 會建立一份臨時 PPTX、停用網路更新、執行本機美化、Content Lock、atomic finalization，然後確認 final output 真實存在並可重新開啟；未通過不得上傳 artifact。

## Standalone backup BAT

`BACKUP-pptx-beautify-lock-Skill.bat` 仍是另一個完全獨立工具。放到任意資料夾雙擊後，會把完整 Git repository 抓到 BAT 同層的 `pptx-beautify-lock-Skill\`。這個 BAT 需要 Git for Windows；它與 Offline EXE 沒有執行依賴。
