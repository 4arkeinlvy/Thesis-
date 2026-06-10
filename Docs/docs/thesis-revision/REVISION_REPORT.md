# REVISION REPORT — Thesis Smart City Reporter

Date: 2026-05-23
Working dir: `/Users/quatumteknologinusantara/Thesis-/Docs`
Build status: **PASS** — `latexmk -pdf main.tex` produced `main.pdf` (177 pages, 3.5 MB).
Baseline: 179 pages → After revision: 177 pages (whole document). Bab 1–5 alone ≈ 138 pages (target 80 — additional manual cuts still required, see PAGE_BUDGET_REPORT.md).

## Files Modified

| File | Change |
|---|---|
| `chapters/Bab2.tex` | Deleted subsections 2.3.5, 2.3.6, 2.4.2, 2.8.3, 2.12.6, 2.19.3, 2.19.4 |
| `chapters/Bab3.tex` | Refactored section 3.16 (Perancangan Layar) — removed 7 placeholder `\fbox` mockups; replaced with concise paragraphs that point to Lampiran A. Renamed section title from "Perancangan Layar (UI Mockup Placeholders)" to "Perancangan Layar Aplikasi". |
| `references/references.bib` | Fixed `vaswaniAttentionAllYou2023` year `2023 → 2017` (original Transformer paper). Fixed `oquabDINOv22024` year `2024 → 2023` (DINOv2 is April 2023 / arXiv:2304.07193). |
| `main.tex` | Wired in appendix: replaced commented `\input{appendix/lampiran1}` with active include, added `\addcontentsline{toc}{chapter}{LAMPIRAN}`, replaced TOC depth hack with chapter name rename so appendix prints as "LAMPIRAN A" instead of "BAB A". |
| `appendix/lampiran1.tex` | **NEW** — Lampiran A: 7 UI mockup placeholder figures consolidated from Bab 3 §3.16.1–3.16.7. |
| `docs/thesis-revision/*.md` | **NEW** — five audit reports. |

## Sections Deleted (7 subsections)

| Old § | Title | Reason | Orphan citations? |
|---|---|---|---|
| 2.3.5 | Pertimbangan Etika dan Hukum (Web Scraping) | Per user request | None |
| 2.3.6 | Tantangan Praktis (Web Scraping) | Per user request | None |
| 2.4.2 | Cabang Utama AI | Per user request | None |
| 2.8.3 | Token Khusus, Padding, dan Attention Mask | Per user request | None |
| 2.12.6 | Inductive Bias dan Skala Data (ViT) | Per user request | None |
| 2.19.3 | Akselerasi Inferensi pada Mobile | Per user request | `appleCoreML2024` is still cited elsewhere (in 2.16 ONNX / 2.17 on-device discussion); no orphan. |
| 2.19.4 | Tantangan Distribusi dan Lifecycle | Per user request | None |

Numbering for the remaining sibling subsections shifts down naturally (e.g., 2.3 now ends at 2.3.4; 2.4 now has 2.4.1 and 2.4.2 — old 2.4.3; 2.8 now has 2.8.1, 2.8.2, 2.8.3 — old 2.8.4; 2.12 ends at 2.12.5; 2.19 ends at 2.19.2). No `\ref{}` or `\autoref{}` pointed at the deleted labels (none of the deleted subsections defined `\label`), so no cross-reference fixes are required.

## Major Wording / LaTeX Changes

1. **Section 3.16 refactor.** The original section contained seven `\fbox`-bordered placeholder figures that took roughly two pages of body and dropped seven entries in the List of Figures. The refactor replaces the figures with one short paragraph per layar, each ending with `Tampilan layar dapat dilihat pada Lampiran~\ref{app:ui-mockup}.` Result: section is concise, mockups consolidated in Lampiran A, methodology pages saved without losing the design rationale.
2. **Appendix wiring.** `\appendix` is now followed by an active `\input{appendix/lampiran1}`. Appendix chapter prints as `LAMPIRAN A`. TOC adds a single `LAMPIRAN` entry.
3. **Reference year corrections.**
   - `vaswaniAttentionAllYou2023` year 2017 (was 2023). The arXiv preprint id `1706.03762` is from June 2017; this is the original "Attention Is All You Need". Citation key left unchanged to avoid touching every `\citep` site.
   - `oquabDINOv22024` year 2023 (was 2024). DINOv2 is arXiv:2304.07193 (April 2023). Citation key left unchanged.

## Remaining Risks / Manual Decisions

| # | Issue | Recommendation |
|---|---|---|
| R1 | Bab 1–5 page count ≈ 138 pp, target 80 pp. The seven deletions saved ~2 pp. The remaining ~58 pp reduction is **content-density work**, not mechanical cleanup. Bab 2 (57 pp) and Bab 3 (51 pp) need the most cuts. | See PAGE_BUDGET_REPORT.md for prioritized cuts. Owner-decision required because each cut removes pedagogical or design content the supervisor may want kept. |
| R2 | Reference audit identified 33 orphan `.bib` entries (never cited) and 12 pre-2021 papers used in the text that have newer replacements. Removing orphans is safe; replacing in-text citations changes argumentation and must be reviewed per case. | See REFERENCE_AUDIT.md "Action" column. |
| R3 | The code/experiment audit found one major thesis–code drift: Bab 3 (and conclusion) describe Supabase persistence + RLS, while the legacy `CLAUDE.md` memory note mentioned "sqflite" — `pubspec.yaml` actually uses `supabase_flutter` + `shared_preferences` and **not** `sqflite`. The thesis text is already consistent with `supabase_flutter`; no change needed in Bab 3. The stale memory note has been corrected mentally; no thesis text refers to sqflite. | No-op for thesis. |
| R4 | The ablation matrix CSV (`artifacts/models/matrix_results.csv`) contains 16+ encoder-pair rows including DINOv3, but the source notebook 06 was run for 12 combos without DINOv3 — DINOv3 rows were added in a later run not committed as a notebook. Bab 4 Tabel 4.5 reports DINOv3 row correctly. | Add a short note in Bab 4 §4.5 that the DINOv3 row was produced by a follow-up run (`scripts/run_dinov3_matrix.py` or similar) once that script is checked in. |
| R5 | All Bab 3 §3.16 figures now sit in Lampiran A. Several other supporting diagrams in Bab 3 (e.g., RunPod activity diagrams `bab_3/activity_runpod_setup.png`, `bab_3/activity_runpod_train_export.png`) are large and partly redundant with `kerangka_*` figures. | See DIAGRAM_UI_APPENDIX_AUDIT.md for the full list of figures recommended for move-to-appendix. |
| R6 | DINOv2 paper year correction (2024 → 2023) is now in `.bib`. The `\bibliographystyle{apalike}` will render the new year in citations; downstream reading of "DINOv2 (Oquab et al., 2023)" is now correct. | None — already fixed. |

## Build Status

```
$ latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
… (no errors)
Output written on main.pdf (177 pages, 3624687 bytes).
Transcript written on main.log.
Latexmk: All targets (main.pdf) are up-to-date
```

No undefined references, no missing citations, no overfull/underfull errors flagged at the halt-on-error level.

## Final Page Count

- **Whole document:** 177 pp.
- **Bab 1–5 only:** ≈ 138 pp (Bab 1 = pp 1–14, Bab 2 = 15–71, Bab 3 = 72–122, Bab 4 = 123–134, Bab 5 = 135–138).
- **Target:** ≤ 80 pp for Bab 1–5.
- **Gap:** ~58 pp over. See PAGE_BUDGET_REPORT.md.

## Generated Reports

- [REVISION_REPORT.md](REVISION_REPORT.md) — this file
- [REFERENCE_AUDIT.md](REFERENCE_AUDIT.md) — bibliography freshness + orphans + suggested new entries
- [CODE_EXPERIMENT_GAP_AUDIT.md](CODE_EXPERIMENT_GAP_AUDIT.md) — thesis claims vs code, file:line evidence
- [DIAGRAM_UI_APPENDIX_AUDIT.md](DIAGRAM_UI_APPENDIX_AUDIT.md) — figure-by-figure move-to-appendix plan
- [PAGE_BUDGET_REPORT.md](PAGE_BUDGET_REPORT.md) — pages-before/after per chapter + concrete cut plan
