# pptx-beautify-lock-Skill v0.6.1

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容 100% 凍結＋來源風格鎖定＋版面骨骼智慧＋世界級 Global Design Jury＋全簡報回歸防護** Skill。

核心原則：

> **Fix A without breaking B.** 任何 repair 後都要重新 render / review 全部 slides，不能修好一頁又弄壞另一頁。

## 1. 只貼中央 Skill Catalog URL

未來只需要貼：

```text
https://github.com/Space653000/Claude-code-ChatGPT-Codex---SKILL
```

安裝中央 Catalog 後，Claude Code / Codex 會自動看到 `pptx-beautify-lock` wrapper；遇到 PPTX 任務時它會自動 bootstrap/update 這個 canonical repo，不需要再記第二個網址。

Canonical Source of Truth 仍是：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

## 2. Windows 一鍵檔案介面

原始碼版：

```text
PPTX-Beautify-Lock.cmd
```

GUI 可直接：

- 選擇本機 `.pptx`
- 選輸出資料夾
- Claude Code only / Codex only
- **Dual: Claude → Codex**（建議）
- Dual: Codex → Claude
- 安裝 / 更新 Skill
- 執行頂級美化
- 全面備份

詳細說明：[`launcher/README.md`](launcher/README.md)

GitHub Actions `build-windows-launcher` 會在 Windows runner 建立：

```text
PPTX-Beautify-Lock.exe
```

下載 Actions artifact `PPTX-Beautify-Lock-Windows` 即可使用，不需自己打包 PyInstaller。

## 3. v0.6.1 Strict Production Contract

```text
Content Snapshot
→ Source Theme + Deck Identity + Brand Terrain
→ full source render
→ Linter
→ Auto Formatter
→ Layout Intelligence
→ Design Agent
→ Content / Theme / Spatial Guards
→ full render
→ Visual QA
→ Composition QA
→ Global Design Jury
→ repair / refine
→ full-deck rerender
→ independent full-deck review
→ final full-deck rerender
→ Regression
```

Production workflow 至少三輪完整審查：

```text
Pass 1 = Soul / 靈魂
Pass 2 = Skeleton + Muscle / 骨骼＋肌肉
Pass 3 = Skin + Regression / 表皮＋回歸
```

每一輪都必須覆蓋 **所有 slides**。

## 4. 特別強化的 release blockers

- **Empty placeholder purge** — 空 title/body placeholder、`presentation title`、`Speaker name or subtitle` 等不得擋有效內容。
- **Font portability** — 繁中＋英文要在 Windows/PowerPoint 實際可用；serif fallback、巨大字體、裁切、換行漂移直接 FAIL。
- **Sibling data-slide parity** — POWER / THD / HOHD、6σ / 5σ / 4σ、L/R 等同族頁要共享成熟 table/chart visual grammar。
- **Brand terrain isolation** — logo、department identity、tagline、master chrome 不被新 panel 壓住。
- **Full-deck regression** — 修任何一頁後重新 render / review 全簡報，確認先前通過頁面沒退化。

完整規則：[`pptx-beautify-lock/references/REGRESSION_GUARDRAILS.md`](pptx-beautify-lock/references/REGRESSION_GUARDRAILS.md)

## 5. Final Gates

Fully qualified final 必須至少：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
REGRESSION_V06_PASS=true
DELIVERY_V06_PASS=true
```

另外 v0.6.1 production evidence 要證明：

```text
EMPTY_PLACEHOLDER_PASS=true
FONT_PORTABILITY_PASS=true
SIBLING_STYLE_PARITY_PASS=true
FULL_DECK_REGRESSION_PASS=true
THREE_PASS_REVIEW_PASS=true
```

任一無法證明：FAIL CLOSED。

## 6. 獨立安裝 canonical Skill

```bash
python scripts/install_skill.py --target both --force
```

成功：

```text
INSTALL_PASS=true
```

## 7. Windows 全面備份

```powershell
powershell -ExecutionPolicy Bypass -File scripts\backup_to_windows.ps1
```

預設完整備份到：

```text
C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil
```

中央 Catalog 同步備份到：

```text
C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil\_catalog\Claude-code-ChatGPT-Codex---SKILL
```

採 fast-forward only；有本地修改就停止，不強制覆寫。
