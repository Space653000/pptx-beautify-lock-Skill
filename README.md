# pptx-beautify-lock-Skill

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容鎖定＋來源風格鎖定自動美化 Skill**。

> **Content Lock：內容與 protected semantics 不可變。**  
> **Theme Lock：未授權時不得翻轉來源 light/dark/mixed 主色調。**  
> **Bilingual Typography：繁體中文＋英文都必須 glyph-safe、協調、可讀。**

完整流程：

```text
Content Snapshot
→ Source Theme Discovery / Visual DNA
→ PPTX Linter
→ Auto Formatter
→ Design Agent
→ Content + Theme Guard
→ Render Visual QA
→ Regression Test
```

## v0.4 核心特色

- **Hard Content Lock**：machine-readable protected-semantics manifest/diff
- **Source Theme Discovery**：先辨識原始主色、明暗極性、page-role pattern、theme/master/accent，再設計
- **Theme Guard**：高信心攔截 light→dark、dark→light 與大面積 dark visual-mass drift
- **Bilingual Typography**：繁中＋英文優先使用 CJK-safe family；偵測 Latin-only font 套在 CJK text 的 fallback risk
- **Placeholder Guard**：`presentation title` / `click to add title` 等 template artifact 不得出現在 final
- **PPTX Linter**：geometry、overlap、tiny text、table density、font/title consistency、placeholder、CJK fallback
- **Rendered Visual QA schema 3**：逐頁檢查 source-theme fidelity、bilingual typography、placeholder leakage、clipping、hierarchy 等
- **Regression Test**：Content + Theme + Layout + Visual 四層證據整合
- **URL self-bootstrap**：Claude Code / Codex 共用 `scripts/install_skill.py`
- **GitHub Actions contract tests**

## Authoritative entry points / 權威入口

正式流程：

```text
pptx-beautify-lock/SKILL.md
```

核心 references：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
pptx-beautify-lock/references/THEME_DISCOVERY.md
pptx-beautify-lock/references/TYPOGRAPHY_BILINGUAL.md
pptx-beautify-lock/references/RENDER_VISUAL_QA.md
```

安裝：[`INSTALL.md`](INSTALL.md)  
URL bootstrap：[`AI_BOOTSTRAP.md`](AI_BOOTSTRAP.md)  
品質審查：[`docs/QUALITY_AUDIT_2026-08-25.md`](docs/QUALITY_AUDIT_2026-08-25.md)  
Visual-DNA postmortem：[`docs/POSTMORTEM_2026-08-25_VISUAL_DNA.md`](docs/POSTMORTEM_2026-08-25_VISUAL_DNA.md)

## 最終交付門檻

Fully qualified final PPTX 必須：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

如果不能 render，只能產生 structural candidate，不可宣稱完整 final。

## 最快使用：直接貼 GitHub URL

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

再告訴 Agent：

```text
Read this repository and use pptx-beautify-lock/SKILL.md.
啟用 Content Lock + Theme Lock。
先辨識來源主色調與繁中/英文字體，再美化。
只有 DELIVERY_PASS=true 才交付 final PPTX。
```

若宿主允許本機寫入與程式執行：

```bash
# Claude Code
python scripts/install_skill.py --target claude --force

# Codex
python scripts/install_skill.py --target codex --force

# Both
python scripts/install_skill.py --target both --force
```

成功：

```text
INSTALL_PASS=true
```

> 單純貼 URL 不能繞過宿主安全權限。若禁止下載、執行或寫入 Skills 目錄，Agent 必須直接從 repo 使用 Skill，並明確回報「未持久安裝」。

## Plugin 安裝

### Claude Code

```bash
claude plugin marketplace add https://github.com/Space653000/pptx-beautify-lock-Skill
claude plugin install pptx-beautify-lock@space653000-pptx
```

### Codex / compatible harness

也可直接安裝/連結 `pptx-beautify-lock/` 到 Agent Skills 目錄；詳見 `INSTALL.md`。

## Executable quality gates

```bash
# 1. Content snapshot
python pptx-beautify-lock/scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json

# 2. Source visual DNA
python pptx-beautify-lock/scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json

# 3. Lint
python pptx-beautify-lock/scripts/pptx_lint.py source.pptx --json > lint.before.json

# 4. Content verification
python pptx-beautify-lock/scripts/pptx_content_lock.py verify source.pptx output.pptx

# 5. Theme guard
python pptx-beautify-lock/scripts/pptx_theme_profile.py compare source.pptx output.pptx --json

# 6. Render QA
python pptx-beautify-lock/scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>

# 7. Final release gate
python pptx-beautify-lock/scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

## Source Theme rule / 主色調規則

Beautify ≠ Rebrand。

- source light → final 保持 light
- source dark → final 保持 dark
- source mixed → 保留 page-role pattern
- source 有品牌色 → 沿用 hue family
- 工程圖表的紅色 Limit marker 屬 semantic color，不代表整份 deck 應變紅

除非使用者明確要求換色系，AI 不得因偏好 navy/black 就把原本白底 deck 改 dark。

## Traditional Chinese + English / 繁中英文

預設保守策略：使用一個完整支援繁中的 Sans Serif family，同時承擔中英文，例如實際環境存在的：

- Noto Sans TC
- Microsoft JhengHei / 微軟正黑體
- PingFang TC / 蘋方-繁
- Source Han Sans TC / 思源黑體 TC

Aptos / Inter / Arial / Helvetica 可用於 pure-Latin run，但不得讓含繁中的 mixed run 依賴不可控 fallback。

Render QA 每頁必須：

```text
theme_fidelity_preserved=true
bilingual_typography_clean=true
no_template_placeholder_artifacts=true
```

## Automated tests

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

目前 contract tests 至少驗證：

- visual-only change → Content Lock PASS
- text/table/hyperlink/hidden-state mutation → FAIL
- template placeholder leakage → Linter ERROR
- CJK text + Latin-oriented explicit font → fallback WARNING
- light source → dark candidate → Theme Guard FAIL
- light source + small accent → Theme Guard PASS
- Visual QA schema 3 必須逐頁含 theme/bilingual/placeholder checks
- 完整 Content + Theme + Layout + Visual QA → `DELIVERY_PASS=true`
- Claude Code / Codex installer 指向同一份 Skill

## Important v0.3 correction

先前五份真實 deck 的 `DELIVERY_PASS=true` 是依舊 v0.3 contract 產生。實際人工檢查後發現 placeholder leakage 與 source-theme drift，因此那些輸出在 v0.4 下視為**需要重新處理的 candidate，不是 v0.4 final**。

詳見 postmortem。

Prompt-only promises are not proof.
