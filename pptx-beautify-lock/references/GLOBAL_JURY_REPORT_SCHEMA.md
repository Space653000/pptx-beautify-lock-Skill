# Global Jury Report Schema / 世界級評審報告格式

`global_design_jury_gate.py` 驗證的是**有證據的 review artifact**，不是一句「我覺得 95 分」。

## Deck-level required fields

```json
{
  "schema": 1,
  "slide_count": 15,
  "render_engine": "PowerPoint / LibreOffice / approved renderer",
  "reviewer": "AI vision reviewer or human reviewer",
  "audience_profile": "external technology customer engineering review",
  "source_render_set": "path/hash/reference for source renders",
  "final_render_set": "path/hash/reference for final renders",
  "review_rounds": 2,
  "review_history": [],
  "jury_lenses": {},
  "deck_identity": {},
  "deck_jury_score": 94,
  "overall_pass": true,
  "slides": []
}
```

## `review_history`

`review_rounds` 不能只是一個數字。必須有等長 history，**而且每一輪都必須逐頁覆蓋整份 deck**：

```json
[
  {
    "round": 1,
    "reviewer": "reviewer-id",
    "render_fingerprint": "candidate-render-hash-or-reference",
    "source_render_reference": "source-render-set",
    "final_render_reference": "candidate-render-set",
    "slides_reviewed": [1, 2, 3, 4, 5],
    "findings_summary": "what failed or what required refinement",
    "actions_or_verification": "what was changed or how the independent verification was performed",
    "verdict": "fail"
  },
  {
    "round": 2,
    "reviewer": "reviewer-id",
    "render_fingerprint": "final-render-hash-or-reference",
    "source_render_reference": "source-render-set",
    "final_render_reference": "final-render-set",
    "slides_reviewed": [1, 2, 3, 4, 5],
    "findings_summary": "no blocking world-class defects",
    "actions_or_verification": "independent second verification completed",
    "verdict": "pass"
  }
]
```

若 `slide_count=15`，每一輪 `slides_reviewed` 必須恰好包含 `1..15`，不可抽樣、漏頁或重複。最後一輪必須 `verdict=pass`。

## `jury_lenses`

```json
{
  "purpose_hierarchy_craft": {
    "pass": true,
    "evidence": "specific observations"
  },
  "executive_communication": {
    "pass": true,
    "evidence": "specific observations"
  },
  "domain_role_fit": {
    "pass": true,
    "evidence": "specific observations"
  }
}
```

## `deck_identity`

必須提供 source/final personality、evidence、量化門檻與 anti-template checks：

```json
{
  "checks": {
    "source_personality_preserved": true,
    "no_template_convergence": true,
    "no_unjustified_cardification": true,
    "no_unjustified_dark_techification": true,
    "no_unjustified_gradientization": true,
    "no_brand_personality_erasure": true
  },
  "source_personality": "...",
  "final_personality": "...",
  "identity_evidence": ["..."],
  "identity_fidelity_score": 97,
  "archetype_fit_score": 95,
  "generic_template_risk": 4
}
```

`DECK_IDENTITY_PASS` 不只看 deck-level 欄位；**任何單頁 `source_identity_is_preserved=false` 或 `source_identity` 分數低於門檻，也必須讓 Deck Identity 失敗。**

## Per-slide required structure

```json
{
  "slide": 4,
  "jury_role": "technical_review",
  "checks": {},
  "scores": {},
  "slide_jury_score": 94,
  "role_scores": {},
  "role_score": 94,
  "evidence": {
    "primary_purpose": "...",
    "focal_point": "...",
    "reading_order": ["..."],
    "grid_or_alignment_logic": ["..."],
    "spacing_logic": "...",
    "source_identity_anchors": ["..."],
    "what_was_removed_or_restrained": "...",
    "why_this_is_not_a_generic_template": "..."
  }
}
```

Valid `jury_role` values：

```text
keynote_launch
executive_strategy
technical_review
research_academic
brand_editorial
agenda_section_closing
comparison
other
```

各 role 的 required role scores 與 world-class floors 以 `GLOBAL_DESIGN_JURY.md` 與 `global_design_jury_gate.py` 為準。

## Anti-self-certification rule

以下都不算有效證據：

- `looks good`
- `professional`
- `world class`
- `Apple-like`
- `clean`

Evidence 必須指向 source-vs-final 的具體關係，例如：

- title / logo / status 哪些 rail 被分開
- 哪些 spacing tier 建立 parent-child 關係
- 哪些 source brand anchors 被保留
- 哪些 decoration 被抑制
- technical data 的 focal evidence 是什麼

若無法提出具體 evidence，應 fail closed。
