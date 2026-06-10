# DIAGRAM / UI / APPENDIX AUDIT

Audit of every `\includegraphics` + every UI mockup in `chapters/Bab3.tex` and `chapters/Bab4.tex`, plus recommendation for what stays in the main body and what should move to Lampiran.

## Already Applied

The seven `\fbox` placeholders in former Bab 3 §3.16.1–3.16.7 (Layar Splash, Layar Buat Laporan, Layar Tinjauan AI, Layar Rekomendasi, Layar Riwayat, Layar Peta, Layar Profil) have been moved to **Lampiran A** (`appendix/lampiran1.tex`). Each Bab 3 subsection now points to `Lampiran~\ref{app:ui-mockup}` and runs ~4 lines of body text instead of an 8 cm boxed figure.

## Figure-by-Figure Audit Table

| # | Figure / Diagram | Current Location | Match with Code? | Problem | Action | New Location |
|---|---|---|---|---|---|---|
| 1 | `bab_3/kerangka_berpikir.png` | Bab 3 §3.1 (line 15) | Yes — overview matches code structure | Large, essential | Keep | Bab 3 (main body) |
| 2 | `bab_3/kerangka_akuisisi.png` | Bab 3 §3.1.1 (line 26) | Yes | Large but useful | Keep | Bab 3 |
| 3 | `bab_3/activity_runpod_setup.png` | Bab 3 §3.1.2 (line 37) | Matches `notebooks/00_setup_runpod.ipynb` | **Used twice** — also at line 332. Redundant. | Remove second occurrence at line 332 OR move both to Lampiran B | Lampiran B (cloud setup detail) |
| 4 | `bab_3/activity_runpod_train_export.png` | Bab 3 §3.1.2 (line 44) | Matches `notebooks/06_*` + `notebooks/08_*` | Large activity diagram | Keep one; consider moving to Lampiran B | Bab 3 or Lampiran B |
| 5 | `bab_3/kerangka_deployment.png` | Bab 3 §3.1.3 (line 55) | Yes | Useful | Keep | Bab 3 |
| 6 | `bab_3/app_development_lifecycle.png` | Bab 3 §3.1.3 (line 64) | Generic SDLC, only loosely tied to thesis | Could be cut | Move to Lampiran B or delete | Lampiran B |
| 7 | `sample_row_1.png` | Bab 3 §3.3.2 (line 144) | Sample CRM rows | Useful | Keep one row, drop the other two; or move all three to Lampiran C (dataset samples) | Lampiran C |
| 8 | `sample_row_2.png` | Bab 3 §3.3.2 (line 153) | Sample CRM rows | Repetition | Move to Lampiran C | Lampiran C |
| 9 | `sample_row_3.png` | Bab 3 §3.3.2 (line 162) | Sample CRM rows | Repetition | Move to Lampiran C | Lampiran C |
| 10 | `bab_3/activity_runpod_setup.png` (duplicate) | Bab 3 (line 332) | Duplicate of #3 | Duplicate include | **Remove this duplicate include** | — |
| 11 | `bab_3/flow_inferensi.png` | Bab 3 §3.11 (line 628) | Matches `serve_model.py` flow | Essential for server section | Keep | Bab 3 |
| 12 | `bab_3/component_diagram.png` | Bab 3 §3.11 (line 678) | C4-component view | Essential | Keep | Bab 3 |
| 13 | `schema.png` | Bab 3 §3.12 (line 718) | Supabase ERD overview | Essential | Keep | Bab 3 |
| 14 | `bab_3/usecase_smart_city_reporter.png` | Bab 3 §3.13.1 (line 842) | Use case diagram. Actors match `lib/features/` roles (Warga, Operator, Moderator) | Essential UML | Keep | Bab 3 |
| 15 | `bab_3/activity_pelaporan.png` | Bab 3 §3.13.3 (line 1009) | Matches `create_report_screen.dart` → `ai_result_review_screen.dart` flow | Essential | Keep | Bab 3 |
| 16 | `bab_3/class_diagram_flutter.png` | Bab 3 §3.13.4 (line 1020) | UML class diagram. Should be cross-checked against actual class layout in `lib/` | Verify it still matches code | Keep but verify class names match the current Riverpod providers | Bab 3 |
| 17 | `bab_3/sequence_predict.png` | Bab 3 §3.13.5 (line 1031) | Sequence diagram of `/predict` | Essential | Keep | Bab 3 |
| 18 | 7 × `\fbox` UI placeholders | Bab 3 §3.16.1–3.16.7 | (placeholders, no actual screenshots) | Now moved to Lampiran A | **Already moved** to `appendix/lampiran1.tex` | Lampiran A (done) |
| 19 | `bab_4/class_distribution.png` | Bab 4 §4.2 (line 44) | Matches Tabel 4.2 | Essential | Keep | Bab 4 |
| 20 | `bab_4/modality_ablation.png` | Bab 4 §4.4 (line 122) | Matches Tabel 4.3 | Essential | Keep | Bab 4 |
| 21 | `bab_4/pgs_comparison.png` | Bab 4 §4.5 (line 153) | Matches Tabel 4.4 | Essential | Keep | Bab 4 |
| 22 | `bab_4/encoder_matrix.png` | Bab 4 §4.6 (line 186) | Heatmap matches Tabel 4.5 | Essential | Keep | Bab 4 |
| 23 | `bab_3/erd_supabase.png` | Bab 4 §4.7.1 (line 231) | Detailed ERD | Same diagram referenced twice (once via `schema.png` in Bab 3, once via `erd_supabase.png` in Bab 4)? Verify if duplicate | If `schema.png` and `erd_supabase.png` are the same content, reference the Bab 3 figure instead of re-including | Bab 3 only |

## Recommended Bab 3 / Bab 4 Page-Saving Diagram Moves

1. **Remove duplicate** `bab_3/activity_runpod_setup.png` at Bab 3 line 332 — appears twice in §3.1.2 and again in §3.4 (RunPod). Keep only the §3.1.2 instance.
2. **Move to Lampiran B (Detail Cloud Pelatihan):** `activity_runpod_setup.png`, `activity_runpod_train_export.png`, `app_development_lifecycle.png` — these are operational details that don't affect understanding of the method. Saves ~3 pp in Bab 3.
3. **Move to Lampiran C (Contoh Dataset CRM):** `sample_row_1.png` / `sample_row_2.png` / `sample_row_3.png` — three example rows. Keep one in Bab 3 §3.3.2 as a visual cue; move the other two to Lampiran C. Saves ~1 pp.
4. **Verify Bab 4 §4.7.1** `bab_3/erd_supabase.png` is the same as Bab 3 §3.12 `schema.png`. If yes, in Bab 4 replace the `\includegraphics` with `Gambar~\ref{fig:schema-bab3}` plus a one-line caption restatement. Saves ~1 pp.

Together these moves are roughly **5 pp** of additional Bab 3/4 reduction without losing any methodology content.

## Use-Case Diagram Verification

The actors in `bab_3/usecase_smart_city_reporter.png` (Warga Pelapor, Operator Instansi, Moderator) match the role enum referenced in `lib/features/auth/auth_repository.dart` and the role-gated routes in `lib/features/dashboard/`. The features shown on the diagram (Buat Laporan, Tinjau Hasil AI, Lihat Riwayat, Verifikasi Laporan, Moderasi Lintas Instansi) match Flutter feature folders. **No use-case actors/features should be removed** — the diagram is currently consistent with the implementation.

## Activity / Sequence Diagram Verification

- `bab_3/activity_pelaporan.png` (alur Warga Pelapor): traces `create_report_screen.dart` → `media_service.dart` → `location_service.dart` → `cloud_classification_service.dart` (HTTP to `/predict`) → `ai_result_review_screen.dart` → Supabase write. Matches code.
- `bab_3/sequence_predict.png`: traces the Flutter client ↔ FastAPI `/predict` ↔ ONNX encoders + CatBoost ONNX classifier. Matches `serve_model.py`.

No flow diagram is missing.

## Suggested New Diagram (Optional)

- Add a single small flowchart for **PGS uncertainty calculation** to Bab 3 §3.7.3 — currently the PGS section is text-only and refers to `pgs.py`. A small block diagram of `model.virtual_ensembles_predict → mean/std → confidence` would help the reader. ~½ page; offsets one of the cuts above.
