# PAGE BUDGET REPORT

Target: **Bab 1–5 ≤ 80 pages**.
Whole-document baseline before this revision: **179 pages**.
Whole-document after this revision: **177 pages**.

## Pages Before / After (Bab 1–5 only)

Pulled from `chapters/*.aux` after `latexmk` compile:

| Chapter | Start page | Pages Before | Pages After (this revision) | Target | Delta to Target |
|---|---:|---:|---:|---:|---:|
| Bab 1 — Pendahuluan | 1 | 14 | 14 | 8–12 | +2 to +6 |
| Bab 2 — Tinjauan Pustaka | 15 | 59 | 57 | 18–25 | +32 to +39 |
| Bab 3 — Metode Penelitian | 72 | 51 | 51 | 18–24 | +27 to +33 |
| Bab 4 — Hasil dan Pembahasan | 123 | 12 | 12 | 18–24 | −6 to −12 (under) |
| Bab 5 — Simpulan dan Saran | 135 | ~4 | ~4 | 4–6 | within range |
| **Total Bab 1–5** | | **≈ 140** | **≈ 138** | **80** | **+58** |

## What This Revision Already Saved

- Section deletions (2.3.5, 2.3.6, 2.4.2, 2.8.3, 2.12.6, 2.19.3, 2.19.4) — ~2 pp from Bab 2.
- Bab 3 §3.16 figure-to-Lampiran refactor — 7 placeholder figures collapsed into one paragraph each. Visible whole-document saving is ~0 pp because the placeholders moved to the appendix; the **methodology section** of Bab 3 is now ~1 pp shorter, while the appendix added ~3 pp. Net Bab 1–5 saving: ~1 pp.

Cumulative Bab 1–5 saving so far: **~3 pp** of the ~58 pp needed.

## Remaining Action Plan to Hit 80 pp

Cuts are listed roughly in order of low-risk → higher-risk. Owner approval recommended at each rung.

### Tier 1 — mechanical, ~10–14 pp (low risk)

1. **Remove duplicate figure** `bab_3/activity_runpod_setup.png` at Bab 3 line 332. — ~½ pp.
2. **Move three Bab 3 large supporting diagrams to a new Lampiran B** (`activity_runpod_setup.png`, `activity_runpod_train_export.png`, `app_development_lifecycle.png`). — ~3 pp.
3. **Move two of three CRM sample-row figures to Lampiran C** (keep one in §3.3.2). — ~1 pp.
4. **Verify Bab 4 §4.7.1 ERD figure** is the same image as Bab 3 §3.12 `schema.png`; if so, replace re-include with a cross-reference. — ~1 pp.
5. **Remove the 33 orphan `.bib` entries** flagged in REFERENCE_AUDIT.md. This shaves the bibliography by ~1 pp (out of the body of the thesis, not Bab 1–5 — see note below).
6. **Bab 2 §2.5 (Machine Learning) — compress** the formula-only introduction. Move equations 2.1–2.2 into one paragraph; remove the Bias-Variance subsection if it isn't referenced in Bab 3. — ~2 pp.
7. **Bab 2 §2.6 (Deep Learning) — compress** the MLP / backprop walkthrough; readers of this thesis are expected to know MLPs. Drop figure if any, keep one paragraph. — ~2 pp.
8. **Bab 2 §2.9 (Ekstraksi Fitur Hand-Crafted: SIFT, HOG)** — already largely peripheral after the deletions. Compress to one paragraph or remove unless §3.x uses HOG/SIFT (it does not). — ~1 pp + remove `dalalHOG2005`, `lowesift2004` citations.

**Subtotal Tier 1: ~10–14 pp.**

### Tier 2 — content compression, ~25–30 pp (medium risk)

9. **Bab 2 §2.10 (PCA / Reduksi Dimensi)** — code does not perform PCA on the fusion vector (see Bab 3 §3.5 "Pertimbangan Reduksi Dimensi"). Section can be reduced to a single paragraph that acknowledges PCA was considered and rejected; drop the formula block. — ~3 pp.
9. **Bab 2 §2.11 (Mekanisme Attention)** — keep the QKV equation and one paragraph on intuition; drop multi-head detail, cross-attention discussion. — ~3 pp.
10. **Bab 2 §2.12 (Transformer)** — keep §2.12.1 Encoder–Decoder + §2.12.5 ViT in one short pair of paragraphs; drop positional encoding, layer norm, pre-norm vs post-norm specifics. Reader can refer to vaswani 2017. — ~3 pp.
11. **Bab 2 §2.13 (Backbone Visual)** — compress DINO genealogy / self-distillation mechanism; keep one paragraph for each of DINOv3, EVA-02, Hiera (the three encoders that appear in the ablation). — ~3 pp.
12. **Bab 2 §2.14 (Text Encoder)** — keep only the encoders that actually appear in Bab 4 Tabel 4.5 (mE5, BGE-M3, IndoBERT, Cendol-mT5). Drop BERT, mBERT background paragraphs. — ~2 pp.
13. **Bab 2 §2.15 (Fusi Multimodal)** — compress taxonomy of fusion schemes; the thesis only uses early-concat fusion. One paragraph max. — ~2 pp.
14. **Bab 2 §2.18 (UML)** — compress; the actual UML diagrams sit in Bab 3 §3.13. Background to UML can be ~½ page. — ~3 pp.
15. **Bab 2 §2.21 (Supabase)** — compress to its essentials (auth, Postgres, storage, RLS). Drop Realtime Subscriptions subsection if the app does not use realtime. — ~2 pp.
16. **Bab 2 §2.23 (Docker)** — compress to one paragraph on `Dockerfile` + Compose. Drop multi-stage / layer-caching detail. — ~2 pp.
17. **Bab 2 §2.26 (Penelitian Terkait)** — currently lists five related works with three subsections each (Gambaran Umum / Analisis / Kesimpulan). Compress each related work into 4–5 sentences in one paragraph. — ~4 pp.

**Subtotal Tier 2: ~25–30 pp.**

### Tier 3 — methodology compression in Bab 3, ~10–15 pp (higher risk)

18. **Bab 3 §3.4 (RunPod environment)** — large amount of operational detail (pod config, SSH workflow, env management). Move most of it to Lampiran B. Keep one paragraph in Bab 3. — ~3 pp.
19. **Bab 3 §3.7.1 (Justifikasi CatBoost)** — currently 8 subsubsections justifying CatBoost. Consolidate to one short subsection with 4 bullet points (ordered boosting, oblivious trees, posterior sampling, ONNX export). — ~2 pp.
20. **Bab 3 §3.12 (Supabase schema)** — three tables described in detail with all columns. Move the column-level description to Lampiran D (Supabase schema reference). Keep ERD figure + 1 paragraph per table in Bab 3. — ~3 pp.
21. **Bab 3 §3.13 (Flutter)** — Use-Case Description subsection is currently long. Compress each use case to title + 2 lines (actor, goal, success). — ~3 pp.
22. **Bab 3 §3.15 (Skenario Pengujian)** — currently mostly redundant with Bab 3 §3.8 (Metrik Evaluasi). Merge the two and drop one. — ~2 pp.

**Subtotal Tier 3: ~13 pp.**

### Tier 4 — additions needed in Bab 4 (offset the cuts)

Bab 4 is **under** target (currently 12 pp, target 18–24). The audit (CODE_EXPERIMENT_GAP_AUDIT.md) recommends:
- Adding the concrete hyperparameter table (~½ pp).
- Adding ONNX `|Δp|_max` numerics from `artifacts/export/parity.json` (~½ pp).
- Adding a confusion matrix figure for the best config (~1 pp).
- Adding a brief per-class precision/recall table (~1 pp).

These additions are ~3 pp **expansion** in Bab 4 — they offset cuts elsewhere but stay within the 18–24 pp target.

## Net Projection

| Step | Δ Bab 1–5 pp | Cumulative pp |
|---|---:|---:|
| Baseline (this revision) | — | ≈138 |
| Tier 1 (mechanical) | −12 | 126 |
| Tier 2 (Bab 2 compression) | −27 | 99 |
| Tier 3 (Bab 3 compression) | −13 | 86 |
| Tier 4 (Bab 4 additions) | +3 | 89 |
| Final stretch (tighten Bab 1 to 10pp, trim Bab 5 to 4pp, remove a few smaller diagrams) | −9 | **80** |

A realistic 80-page result requires **all four tiers**. Tier 1 alone is not enough.

## Action Taken in This Revision

| Chapter | Pages Before | Pages After | Action Taken |
|---|---:|---:|---|
| Bab 1 | 14 | 14 | No content change |
| Bab 2 | 59 | 57 | Deleted §2.3.5, §2.3.6, §2.4.2, §2.8.3, §2.12.6, §2.19.3, §2.19.4 |
| Bab 3 | 51 | 51 | §3.16 collapsed to point to Lampiran A (net 0 pp in Bab 3 because content density similar) |
| Bab 4 | 12 | 12 | No content change |
| Bab 5 | 4 | 4 | No content change |
| Front matter + Bibliography + Lampiran | 39 | 39 | +3 pp Lampiran A, −2 pp body, net ≈ 0 visible |

**Remaining work to hit ≤ 80 pp for Bab 1–5: ~58 pp of cuts (Tiers 1–4 above), each requiring per-section owner approval.**
