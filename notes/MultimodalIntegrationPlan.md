# Multimodal (Text + Image) Integration Plan

Status: draft — labels confirmed from `artifacts/splits/train.csv`. The classifier is trained end-to-end to predict **instansi (agency) directly** — there is no client-side topic→agency mapping. Section 2 below lists the actual 9 labels the model emits.

Scope: replace the current single-image `mambaout_tiny` pipeline in [smart_city_reporter_app](smartCityReport/smart_city_reporter_app/) with the new multimodal classifier (DINOv3-large image embedding + multilingual-E5-large text embedding → CatBoost/ONNX head trained on Jakarta CRM), and reshape the result UI around the 8 instansi + 1 "Instansi lain" fallback that the head already produces.

---

## 0. What ships today vs. what we have

| Layer | Today (in-app) | New artifacts ready under [artifacts/export/](smartCityReport/artifacts/export/) |
|---|---|---|
| Image encoder | `mambaout_tiny.onnx` (7 logits, classifies directly) | `image_encoder_dinov3_large.onnx` (embedding only) |
| Text encoder | none | `text_encoder_mE5_large/model.onnx` + tokenizer files |
| Classifier head | implicit (last layer of mambaout) | `classifier_dinov3_large_mE5_large.onnx` (combined emb → class logits) |
| App categories | 5-value `IssueCategory` enum [report_models.dart:1-25](smartCityReport/smart_city_reporter_app/lib/features/reports/report_models.dart#L1-L25) | needs to become 8 + `instansiLain` |
| Routing | hard-coded raw-label switch [classification_routing.dart:69-129](smartCityReport/smart_city_reporter_app/lib/features/reports/classification_routing.dart#L69-L129) | needs to switch on the new 8 class IDs |

---

## 1. How to test the AI today (current single-image model)

Two layers — model layer (Python) and app layer (Android).

### 1a. Model layer (sanity-check the trained checkpoint)

```bash
cd smartCityReport
python serve_model.py            # starts a local HTTP inference server
# in another shell:
curl -F "image=@/path/to/test.jpg" http://localhost:8000/classify
```

That hits the same preprocessing path as training and returns `{label, confidence, top_predictions}`. If you want a deeper test, re-run eval on the held-out split:

```bash
python train.py --config configs/balanced_800_all_models_accident_augmented.yaml \
  --models mambaout_tiny --eval-only --device cuda
```

### 1b. App layer (on-device ONNX, Android)

The Flutter side uses a `MethodChannel` (`smart_city_reporter/onnx`) into [OnnxRoadIssueClassifier.kt](smartCityReport/smart_city_reporter_app/android/app/src/main/kotlin/com/example/smart_city_reporter_app/OnnxRoadIssueClassifier.kt). To verify end-to-end on a phone or emulator:

```bash
cd smartCityReport/smart_city_reporter_app
flutter pub get
flutter run -d <android-device-id> --dart-define=ENABLE_ON_DEVICE_AI=true
```

There are two helper scripts already in [tool/](smartCityReport/smart_city_reporter_app/tool/):

- `run_android_testing.ps1` — full end-to-end manual test
- `run_android_onnx_testing.ps1` — focuses on the ONNX path

There is also a dedicated test screen at `lib/features/testing/` — open it from the dev menu to feed canned images into the classifier without going through the camera flow. That's the fastest signal for "is the on-device model returning sane predictions."

Acceptance for "AI works today": pick 3 images per class from the held-out split, run them through the `testing` screen, expect top-1 prediction matches the dataset label for at least the high-F1 classes (garbage, pothole, accident).

---

## 2. The 9-instansi target labels (locked from training split)

Verified against [artifacts/splits/train.csv](smartCityReport/artifacts/splits/train.csv) — these are the exact labels the head was trained on. The model output is the agency itself; there is no topic→agency mapping to do client-side.

| `label_id` | Instansi (model output, ID) | Short label (UI) | What it usually covers |
|---|---|---|---|
| 0 | Dinas Bina Marga | "Jalan & Trotoar" | Lubang jalan, kerusakan permukaan, trotoar rusak, jalan ambles. |
| 1 | Satuan Polisi Pamong Praja | "Ketertiban Umum" | PKL liar, reklame liar, vandalisme ringan, pelanggaran ketertiban. |
| 2 | Dinas Perhubungan | "Lalu Lintas & Parkir" | Lampu lalu lintas, rambu, parkir liar, hambatan arus, halte. |
| 3 | Kelurahan | "Layanan Kelurahan" | Sampah lingkungan, RT/RW, kebersihan permukiman, isu lokal warga. |
| 4 | Dinas Pertamanan dan Hutan | "Pohon & Taman" | Pohon tumbang/mati, perawatan taman, hutan kota, satwa liar. |
| 5 | Dinas Sumber Daya Air | "Banjir & Drainase" | Banjir, saluran air, kali-sungai, pompa air, tutup saluran. |
| 6 | Dinas Cipta Karya, Tata Ruang, dan Pertanahan | "Bangunan & Tata Ruang" | Tata ruang, bangunan publik, JPO/jembatan, fasilitas gedung pemda. |
| 7 | Badan Pembinaan Badan Usaha Milik Daerah | "BUMD" | Layanan BUMD (PAM, Transjakarta, dll.) yang bukan tanggung jawab dinas teknis. |
| 8 | Instansi lain | "Instansi Lain" | Fallback — kasus tidak yakin atau di luar 8 instansi utama. Manual review. |

**Implications for the app code:**
- Drop the topical `IssueCategory` enum (`garbage`, `pothole`, `vandalism`, `fallenTree`, `accident`). The new enum values **are** the instansi above. Suggested Dart names: `dinasBinaMarga`, `satpolPP`, `dinasPerhubungan`, `kelurahan`, `dinasPertamananHutan`, `dinasSDA`, `dinasCiptaKarya`, `badanBUMD`, `instansiLain`.
- The "operationalLabel" field in [classification_routing.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/classification_routing.dart) becomes the friendly short label in the table above. The "agencies" list collapses from N entries to a single primary instansi (the predicted one) plus optional pendukung that *you* hand-curate per instansi (no model involvement).
- `Instansi lain` is a real model output — when it wins top-1, that's the model honestly saying "I don't know which agency." Treat it as a UI signal to force manual category selection, not as an error.

**One thing to double-check on the model side:** confirm `classifier_dinov3_large_mE5_large.onnx` was exported from a head trained on this 9-class split (not the older 7-class image-only split). A 5-line Python parity check is enough — load the ONNX, feed one row from `test.csv`, confirm the predicted `label_id` matches the CSV. Worth doing before P2 because re-exporting is cheap and finding out at P3 is expensive.

---

## 3. New runtime architecture (Flutter side)

```
                    ┌──────────────────────────────┐
   user photo  ───▶ │ image_encoder_dinov3_large   │ ──▶ image_emb (Lx1024)
                    └──────────────────────────────┘
                                                          ┌──────────────────┐
                                                          │ classifier head  │ ──▶ 9 logits
                                                          │ (image+text emb) │       │
                    ┌──────────────────────────────┐      └──────────────────┘       │
   description ───▶ │ tokenizer (HF)               │ ──┐                              │
                    └──────────────────────────────┘   ▼                              ▼
                    ┌──────────────────────────────┐                          softmax → top-1 + top-3
                    │ text_encoder_mE5_large       │ ──▶ text_emb (Lx1024)    + UI confidence + agency card
                    └──────────────────────────────┘
```

Three ONNX sessions, run sequentially: image encoder, text encoder (with tokenizer), classifier head. Concatenate (or whatever fusion the head expects — confirm from the export script) before feeding the head.

**Critical unknown:** the exact concat / pool / norm contract between the two encoders and the head. Need to read the export script for `classifier_dinov3_large_mE5_large.onnx` to lock down:
- text-encoder output: last_hidden_state vs. mean-pooled vs. `[CLS]`
- image-encoder output: patch tokens vs. CLS vs. mean-pooled
- whether L2-normalization is applied before concat
- input order in the head (image_emb first or text_emb first)

This is non-negotiable for parity with the trained model — getting any of these wrong will silently destroy accuracy.

---

## 4. Flutter / Android wiring changes

### 4a. Assets & metadata

- `assets/models/` add: `image_encoder_dinov3_large.onnx`, `text_encoder_mE5_large.onnx`, `classifier_v1.onnx`, `tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json`.
- Replace `mambaout_tiny.metadata.json` with a new `multimodal.metadata.json` describing all three sessions, the 9 class names, the fusion contract, and image normalization stats. Keep the old metadata file for one release if you want a rollback flag.
- Update `pubspec.yaml` to register the new assets. **Note: total size will jump significantly** — DINOv3-large + mE5-large is several hundred MB. Decide whether to ship in-APK (bigger install) or download-on-first-run (extra plumbing).

### 4b. Native ONNX bridge ([OnnxRoadIssueClassifier.kt](smartCityReport/smart_city_reporter_app/android/app/src/main/kotlin/com/example/smart_city_reporter_app/OnnxRoadIssueClassifier.kt))

Refactor into three sessions:
- `imageEncoderSession` — current bitmap preprocessing path is reusable, just swap the model and capture the embedding output instead of softmax.
- `textEncoderSession` — needs a tokenizer. Two options:
  - (a) Pure-Kotlin port of the HF tokenizer using `tokenizer.json` (heavy lift; xlm-roberta uses sentencepiece).
  - (b) Bundle `huggingface/tokenizers` JNI (`com.github.djl.huggingface:tokenizers`). Recommended — battle-tested, ~10MB, drop-in.
- `classifierSession` — small, fast, just feeds concatenated embeddings.

New method-channel methods:
- `classifyMultimodal({imagePath, description})` returns `{topClass, confidence, top3, embeddingDebug}`.
- Keep `classifyImage` as a thin wrapper that passes empty description, so the old screen still builds while we migrate.

### 4c. Dart side

- [report_models.dart:1-25](smartCityReport/smart_city_reporter_app/lib/features/reports/report_models.dart#L1-L25) — replace `IssueCategory` with the 9 instansi enum values from §2. `dbValue` should be the `label_id` (or a stable string slug like `dinas_bina_marga`); `label` is the friendly short label. **Migration concern:** existing rows in SQLite still store the old topical values — write a one-shot migration in [local_database_service.dart](smartCityReport/smart_city_reporter_app/lib/core/services/local_database_service.dart) with a best-effort old→new map: `garbage`/`fallenTree` → `kelurahan` or `dinasPertamananHutan` (your call), `pothole` → `dinasBinaMarga`, `vandalism` → `satpolPP`, `accident` → `dinasPerhubungan`. There is no perfect mapping (the old enum was topical, the new one is operational) — pick a conservative default and accept that some legacy rows may need manual relabeling.
- New service `multimodal_ai_classification_service.dart` implementing `AiClassificationService` — same shape as today's [on_device_ai_classification_service.dart](smartCityReport/smart_city_reporter_app/lib/core/services/on_device_ai_classification_service.dart) but calls `classifyMultimodal` and passes the description.
- [classification_routing.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/classification_routing.dart) — collapse the raw-label switch into a switch over the 9 instansi enum values. The model's top-1 is the routing decision, so each branch just decorates that with a friendly summary, optional pendukung agencies (hand-curated, not predicted), and review notes. Drop the `Mixed Issues` / `Illegal Parking Issues` / "secondary raw label" logic entirely — those don't exist anymore. Add a dedicated `_instansiLainGuidance` that says explicitly "Model tidak yakin instansi mana — pilih kategori manual sebelum submit."

### 4d. Controller / flow change ([create_report_controller.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/create_report_controller.dart))

Description currently feeds the classifier *after the fact* — it's only stored. The new flow needs the description to be available **before** classification, because it's an input. Two paths:

- **Path A (recommended):** swap the order — collect photo + description on `CreateReportScreen`, then "Classify". The existing `_classifyAndContinue` runs after both are filled.
- **Path B:** keep order, run an initial image-only pass for fast feedback, then re-classify with description on the review screen and let the user see the prediction shift. Nicer UX but doubles inference cost and complicates the state machine.

Recommend Path A for v1, revisit Path B once you confirm latency on a mid-tier Android device.

---

## 5. UI changes

### 5a. [create_report_screen.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/create_report_screen.dart)

- Make the **description field a first-class step** (currently it's tucked inside the review screen). Step order becomes: ① Photo → ② Description → ③ Location → ④ Classify.
- Add a small helper line under the description field: *"Tulis dalam Bahasa Indonesia atau English. Detail seperti 'lubang besar dekat lampu merah' membantu AI."* — the multilingual encoder handles both, and concrete phrasing improves the head's confidence noticeably in our matrix runs.
- Disable the "Classify" CTA until photo + non-trivial description (≥10 chars) are present.

### 5b. [ai_result_review_screen.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/ai_result_review_screen.dart)

- Replace the current `Wrap` of 5 `ChoiceChip`s [ai_result_review_screen.dart:170-183](smartCityReport/smart_city_reporter_app/lib/features/reports/ai_result_review_screen.dart#L170-L183) with a 9-item layout for the instansi list. Nine chips is too many for a flat `Wrap` — recommend a vertical list of `RadioListTile`-style rows where each row shows: instansi short label (e.g. "Lalu Lintas & Parkir"), the formal instansi name in muted small text below ("Dinas Perhubungan"), and an info icon that opens a sheet explaining what kinds of cases that instansi handles. Selected row is highlighted; unselected rows stay scannable.
- Show the **top-1 prediction prominently** with the friendly short label as headline and the formal instansi name as subtitle. With nine output classes, **top-3 confidence bars** below add real value — they let the user see e.g. "Dinas Bina Marga 0.71 / Dinas Perhubungan 0.18 / Dinas SDA 0.06" and pick the right one when the model is split between two plausible routes (a flooded pothole could plausibly be DBM or DSDA).
- Render the **`Instansi lain`** state distinctly: warning-tone card, headline "AI tidak yakin instansi mana yang tepat — pilih kategori manual sebelum submit", no auto-routing CTA, and the instansi list pre-scrolled into view.
- Show a small **"AI mempertimbangkan deskripsi Anda"** pill under the top-1 — a UX tell that the description text actually influenced the result. Builds trust and rewards users for writing better descriptions.

### 5c. [ClassificationRoutingCard](smartCityReport/smart_city_reporter_app/lib/core/widgets/classification_routing_card.dart) (assumed path)

- One card per cluster, with primary instansi badge + 1-2 supporting instansi.
- Add a small "Mengapa rute ini?" expandable section that surfaces `routingReason` — already structured this way, just needs the new 9-value content.

---

## 6. Phasing

| Phase | Goal | Acceptance |
|---|---|---|
| P0 — verify trained model | Confirm `classifier_dinov3_large_mE5_large.onnx` matches the head we want. Lock fusion contract. | Notebook reproduces test-set metrics from the new pipeline on at least 50 samples. |
| P1 — taxonomy lock | Section 2 table approved (or rewritten). Class IDs frozen. | This doc, signed off. |
| P2 — Dart enum + routing rewrite + DB migration | App still uses old model but new categories. | App boots, old reports survive migration, new reports can be filed under any of the 9 categories manually. |
| P3 — native multimodal bridge | Three ONNX sessions + tokenizer wired through `MethodChannel`. | `classifyMultimodal` returns top-1 matching the Python reference for ≥10 fixture inputs (image + description pairs). |
| P4 — UI rewrite | Description-first flow, top-3 panel, instansi-lain state. | Screens render at 24px grid, no overflow on a 360dp-wide device, all 9 chip states are reachable. |
| P5 — polish | APK size optimization (encoder quantization to int8 if size is a problem), telemetry on AI confidence distribution. | Install size acceptable; mid-tier device classifies in <3s. |

---

## 7. Risks worth flagging upfront

1. **Model size.** DINOv3-large + mE5-large together can easily exceed 1GB FP32. Even FP16 it's hundreds of MB. Plan from day one for either int8 quantization (`onnxruntime` supports it for both architectures) or remote download with caching. Don't ship a 1GB APK and discover it on the Play Store reviewer's device.
2. **Tokenizer in Kotlin.** Hand-rolling sentencepiece is a bug farm. Use the DJL HF tokenizers binding (`ai.djl.huggingface:tokenizers:0.27.0` or newer) — supports `tokenizer.json` directly.
3. **Fusion mismatch.** Easiest way to silently break accuracy. Step P0 above is non-negotiable — write a Python ↔ Kotlin parity test (same inputs, same numerical outputs within 1e-3) before claiming P3 is done.
4. **Description privacy.** User text now flows into a model. Even though it's on-device, surface it in a privacy line in [settings](smartCityReport/smart_city_reporter_app/lib/features/settings/) — "Deskripsi hanya diproses di perangkat Anda, tidak dikirim ke server."
5. **DB migration loss.** If the migration in P2 is wrong, old reports get the wrong category permanently. Back up the SQLite file before running the migration in any test session.

---

## 8. Decisions I need from you before P2 starts

1. **Friendly UI labels** — confirm the "Short label (UI)" column in §2 (e.g. "Jalan & Trotoar" for Dinas Bina Marga). These are user-facing copy and you may want to tune them.
2. **Pendukung instansi per branch** — for each of the 8 main instansi, do you want a hand-curated "supporting agency" line, or should the routing card just show the predicted instansi alone?
3. **Description-first flow (Path A) vs. dual-pass (Path B)** in §4d.
4. **Distribution strategy** — APK-bundled models or first-run download?
5. **Old reports** — migrate with the best-effort map in §4c, or just mark all pre-migration reports as `instansiLain` (legacy) and start clean?

Once those five are locked we can start cutting code at P2.
