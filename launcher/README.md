# Windows PPTX Beautifier — Offline-first v0.7.3

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

## v0.7.3：Source-faithful = Safe-only / No-Degradation

過去的離線 formatter 會先套 generic normalization，再用 guard 修回部分字級。這仍可能造成「原稿本來比較好，美化後反而變差」。

v0.7.3 改變策略：

> **Source-faithful 不再先改再修，而是預設不改。Original wins ties.**

當選擇：

```text
自動（忠於原稿 / Source-faithful）
```

以下視覺層全部鎖定：

- shape geometry / z-order / rotation
- font family / size / bold / italic / underline
- word-wrap / auto-fit / vertical anchor
- table geometry / text scale / visual style
- picture/media geometry and crop
- theme/master/layout/background/brand terrain
- slide count/order

預設只允許一種低風險變更：

```text
proofing metadata only
```

也就是關閉編輯器紅色拼字底線所需的非渲染 metadata；不為了「看起來有做事」而放大標題、重排 References、重染表格、加 card/panel 或換配色。

### Package-level proof

Source-faithful 完成後不是只比字級，而是直接驗證 PPTX ZIP package：

- package member/order 必須一致；
- 除 slide XML 的 `noProof` metadata 外，其他 package part 必須 byte-identical；
- slide XML 移除 `noProof` 後 canonical XML 必須與來源一致；
- semantic Content Lock 再跑一次。

因此成功 Log 會包含：

```text
SOURCE_FAITHFUL_SAFE_ONLY=true
SOURCE_CHANGE_POLICY=proofing_metadata_only
SOURCE_PACKAGE_STRUCTURE_PASS=true
SOURCE_VISUAL_XML_LOCK_PASS=true
SOURCE_GEOMETRY_LOCK_PASS=true
SOURCE_TYPOGRAPHY_LOCK_PASS=true
SOURCE_TABLE_STYLE_LOCK_PASS=true
SOURCE_MEDIA_LOCK_PASS=true
SOURCE_THEME_IDENTITY_LOCK_PASS=true
SAFE_CHANGE_BUDGET_PASS=true
NO_DEGRADATION_GATE_PASS=true
CONTENT_LOCK_PASS=true
```

任何一項不成立：刪除 candidate，FAIL CLOSED。

## Transformative styles

`Technical Clean / Executive Minimal / Modern Minimal / Premium Tech` 是使用者明確 opt-in 的 transformation，不等於 Source-faithful。

本機規則引擎沒有大型視覺模型，因此 transformative style 的能力上限低於 AI Skill；需要 bespoke art direction 時，請使用 canonical Skill URL 交給 AI Agent。

## 成功必須等於真的有檔案

交付仍採兩階段：

```text
source.pptx
→ 產生 temporary candidate
→ engine guards / Content Lock
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

## Optional update channel

美化引擎完全可以離線工作；網路不是必要條件：

```text
BEAUTIFY_OFFLINE=true
CLOUD_AI_ENABLED=false
NETWORK_REQUIRED=false
OPTIONAL_UPDATE_CHECK=true
```

有網路時才檢查 stable update branch：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill/tree/fix/separate-skill-exe-backup-v062
```

流程會讀取該 branch 的 commit SHA，再讀：

```text
launcher/update_manifest.json
```

manifest 指定目前 engine path，例如 v0.7.3：

```text
launcher/pptx_offline_engine_v073.py
```

規則：

- remote engine version 高於目前有效版本：下載到 `%LOCALAPPDATA%\PPTXBeautifyOffline\engine_updates\`。
- remote version 相同或更舊：不更新，禁止降級。
- 沒網路 / DNS / Proxy / Firewall 阻擋：`UPDATE_CHECK=offline_skip`，正常使用內建或 cache engine。
- remote engine 要求更高 launcher version：Log `UPDATE_STATUS=new_exe_required`，不強塞不相容 engine。

## Runtime requirements

- Windows 10/11
- 不需要 Claude Code
- 不需要 Codex
- 不需要登入雲端 AI
- 不需要 Git
- 不需要另外安裝 Python
- 不需要網路即可美化

## Build gate

GitHub Actions 建立：

```text
PPTX-Beautify-Offline.exe
```

Windows runner 必須真的執行：

```text
PPTX-Beautify-Offline.exe --portable-self-test
```

未通過不得上傳 artifact。

## Standalone backup BAT

`BACKUP-pptx-beautify-lock-Skill.bat` 是另一個完全獨立工具。放到任意資料夾雙擊後，把完整 Git repository 抓到 BAT 同層的 `pptx-beautify-lock-Skill\`。此 BAT 需要 Git for Windows；它與 Offline EXE 無執行依賴。
