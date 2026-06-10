# CODE / EXPERIMENT GAP AUDIT

Compares thesis claims in `chapters/Bab1.tex`, `chapters/Bab3.tex`, and `chapters/Bab4.tex` against the actual code, notebooks, scripts, and artifacts under `/Users/quatumteknologinusantara/Thesis-/smartCityReport/`.

## Executive Summary

Implementation fidelity is **strong**. All major claims — early-fusion DINOv3-large + multilingual-E5-large + CatBoost+PGS, 9-class stratified 70/15/15 split with seed 42, balanced accuracy 0.8074 and macro F1 0.7747 on the test set, ONNX export of all three components — match the code, notebooks, and artifacts directly. Two **major** items need attention: (a) the ablation-matrix notebook checked into `notebooks/06_fusion_catboost_pgs.ipynb` lists 12 of the 16 encoder pairs reported in Bab 4 Tabel 4.5; the four DINOv3 rows were produced by an out-of-notebook run whose script is not visible in the audit and should be added to the repo for reproducibility, and (b) the ONNX parity check in `notebooks/08_export_onnx.ipynb` has a validation section but the numeric delta is not captured in the committed cell output. No **critical** gaps.

## Gap Table

| # | Area | Thesis Claim | Code Evidence | Gap | Severity | Suggested Fix |
|---|---|---|---|---|---|---|
| 1 | Pipeline architecture | Bab 3 §3.4/§3.5: early-fusion of frozen DINOv3-large image encoder + multilingual-E5-large text encoder + CatBoost head | `src/crm/encoders/image.py:80-84` (DINOv3 load), `src/crm/encoders/text.py:30-36` (mE5 load), `src/crm/fusion.py:7-27` (concat fusion), `serve_model.py:59-60` (best encoders hardcoded) | None — fully verified | — | — |
| 2 | Encoder freezing | Bab 3 §3.5 and Bab 1 §1.5.2 claim encoders are frozen | `notebooks/06_fusion_catboost_pgs.ipynb` consumes cached embeddings; no `requires_grad=True` anywhere on encoder modules | None — embeddings are computed once via `notebooks/04_image_embeddings.ipynb` and `notebooks/05_text_embeddings.ipynb`, then cached; de-facto frozen | — | — |
| 3 | Dataset stats (9 classes) | Bab 3 §3.3.6: 9 target instansi after consolidating 487 raw SKPD | `src/crm/__init__.py:1-11` defines `TARGET_CLASSES = [...]` with exactly 9 entries; `notebooks/01_dataset_exploration.ipynb` loads `artifacts/crm_jakarta/metadata.csv` | None — verified | — | — |
| 4 | Train/val/test split | Bab 3 §3.3.7 and Bab 4 §4.2: stratified 70/15/15 with sizes 43,242 / 9,267 / 9,267 (Bab 3) and 43,241 / 9,266 / 9,266 (Bab 4) | `notebooks/03_split.ipynb` sets `TRAIN_FRAC = 0.70`, `VAL_FRAC = 0.15`, `TEST_FRAC = 0.15`, `RANDOM_SEED = 42`; reports Train 43,241 / Val 9,266 / Test 9,266 | Minor numeric typo: Bab 3 §3.3.7 states 43,242 / 9,267 / 9,267 while Bab 4 §4.2 says 43,241 / 9,266 / 9,266 (latter matches code) | minor | Make Bab 3 §3.3.7 match Bab 4 §4.2 (off-by-one rounding) |
| 5 | CatBoost hyperparameters | Bab 3 §3.7.2 lists `iterations`, `depth`, `learning_rate`, `l2_leaf_reg`, `bagging_temperature` (general list, no specific table) | `notebooks/06_fusion_catboost_pgs.ipynb`: `iterations=1500`, `depth=6`, `learning_rate=0.05`, `posterior_sampling=True`, `early_stopping_rounds=200` | Bab 3 lists the parameter names but no concrete table of values; reader cannot reproduce without notebook | minor | Add a single small Tabel 3.x with the concrete hyperparameter values used for the best run (the same five-row list above) |
| 6 | PGS (Posterior Gaussian Sampling) | Bab 3 §3.7.3 and Bab 4 §4.5 | `src/crm/pgs.py:14-53` implements `pgs_predict_proba` via `model.virtual_ensembles_predict`; notebook uses `n_virtual_ensembles=30` | None — verified | — | — |
| 7 | Ablation matrix (encoder pairs) | Bab 4 Tabel 4.5: 4 × 4 = 16 pairs, DINOv3+mE5 best at 0.7747 | `notebooks/06_fusion_catboost_pgs.ipynb` shows 12 pairs (DINOv2/EVA-02/Hiera × mE5/BGE/IndoBERT/Cendol). The 4 DINOv3 rows exist in `artifacts/models/matrix_results.csv` but the script that produced them is not visible in the audit | Reproducibility gap — DINOv3 rows present in CSV but no committed notebook/script generates them | major | Add `scripts/run_dinov3_matrix.py` (or rerun notebook 06 with DINOv3 added to `IMAGE_ENCODERS`) and commit; document in Bab 4 §4.5 |
| 8 | Best-config metrics | Bab 4 §4.3: balanced accuracy 0.8074, macro F1 0.7747 (PGS on) | `artifacts/models/matrix_results.csv` row 1: `acc_pgs=0.8073602417440103`, `f1_pgs=0.7747086007881747` | None — exact match | — | — |
| 9 | Modality ablation | Bab 4 Tabel 4.3 lists Citra-saja / Teks-saja / Fusi-awal | Notebook 06 also computes these three columns | None — verified | — | — |
| 10 | ONNX export | Bab 3 §3.10 and Bab 4 §4.6 | `notebooks/08_export_onnx.ipynb` exports `image_encoder_dinov3_large.onnx`, `text_encoder_mE5_large/`, `classifier_dinov3_large_mE5_large.onnx`. Files present in `artifacts/export/` | None — verified | — | — |
| 11 | ONNX numerical parity validation | Bab 3 §3.10.4 and Bab 4 Tabel 4.6: `|Δp|_max < 1e-5` for image, text, classifier, end-to-end | `notebooks/08_export_onnx.ipynb` has a "Validation on test set" section comparing PyTorch vs ONNX on 500 samples; the committed cell output does not contain the explicit `|Δp|_max` number — only "accuracy + F1" deltas | The Bab 4 claim of `< 1e-5` is stated; the value cannot be re-read from committed notebook output | major | Re-run notebook 08 validation cells, persist the `|Δp|_max` numbers to a JSON in `artifacts/export/parity.json`, and reference it in Bab 4 |
| 12 | Flutter: Riverpod + GoRouter | Bab 3 §3.13 / Bab 4 §4.7 | `smart_city_reporter_app/pubspec.yaml:39-40`: `flutter_riverpod: ^3.3.1`, `go_router: ^17.1.0` | None — verified | — | — |
| 13 | Flutter: Supabase | Bab 3 §3.12 details `profiles`, `reports`, `report_history` tables + RLS; Bab 4 §4.7.1 also discusses | `smart_city_reporter_app/pubspec.yaml:52`: `supabase_flutter: ^2.8.0`; `lib/core/config/app_config.dart` configures the client; `lib/features/auth/auth_repository.dart` uses Supabase auth | Supabase tables/RLS are described in detail in Bab 3 but the SQL/migration files are not in the repo — schema lives in Supabase project console | major | Add SQL migration files under `smartCityReport/supabase/migrations/` so the schema in Bab 3 is reproducible. If owner declines, add one short paragraph in Bab 4 §4.7 noting the schema is deployed manually via the Supabase dashboard |
| 14 | Flutter: persistence (local cache) | Bab 1 §1.5.4 and Bab 3 §3.13 mention local persistence via Supabase + lightweight client-side cache | `pubspec.yaml`: `shared_preferences: ^2.x` is present; **no `sqflite`** dependency | None — thesis does not actually claim sqflite (the stale memory note that mentioned sqflite is wrong) | — | — |
| 15 | Use case actors | Bab 3 §3.13.1 lists actors: Warga Pelapor, Operator Instansi, Moderator | `lib/features/`: `reports/`, `auth/`, `dashboard/`, `onboarding/`, `profile/`, `settings/`, `testing/` — feature folder layout aligns with the three actor roles | Minor: no per-folder evidence of a dedicated Moderator/Admin sub-feature; moderator workflow likely shares the dashboard | minor | If a separate moderator surface is intended, add `lib/features/moderation/` or document that moderator and operator share the dashboard with role-gating |
| 16 | ONNX model file sizes | Bab 1 §1.5.4 quotes 1.15 GB for the image encoder | `artifacts/export/image_encoder_dinov3_large.onnx` ≈ 1.1 GB; `classifier_dinov3_large_mE5_large.onnx` ≈ 31 MB | None — within rounding | — | — |
| 17 | Deterministic routing engine | Bab 3 §3.14 and Bab 4 §4.7.4 | `lib/features/reports/classification_routing.dart` defines the static mapping | None — verified | — | — |

## Critical Items

None.

## Major Items (3)

- **#7** — DINOv3 ablation row in the matrix needs a reproducible script committed.
- **#11** — ONNX parity numeric delta needs to be persisted to an artifact rather than only quoted in the thesis.
- **#13** — Supabase schema described in Bab 3 needs migration SQL committed, or a sentence acknowledging it lives only in the Supabase console.

## Minor Items (3)

- **#4** — Train/val/test counts off-by-one between Bab 3 and Bab 4. Fix Bab 3 to 43,241 / 9,266 / 9,266 to match code.
- **#5** — Add a concrete hyperparameter table to Bab 3 §3.7.2.
- **#15** — Document moderator/operator UI split or unify it explicitly.

## Notes on Thesis ↔ Memory Consistency

A pre-existing auto-memory note `(memory/project_thesis_context.md)` claimed the active pipeline had been an image-only TIMM benchmark with `mambaout_tiny` as the winner at F1 = 0.9917. That memory is **stale** with respect to the current code and current Bab 3/4. The current thesis matches the code (multimodal early-fusion, DINOv3 + mE5, F1 = 0.7747 on 9 classes). The memory file should be rewritten — but no thesis change is needed.
