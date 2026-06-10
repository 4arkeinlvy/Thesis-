# UI Refinement + Monitoring Audit — Plan

Status: draft. Needs sign-off on §3 before code changes.

Scope: address the redundancy you spotted on the Review screen, raise the rest of the app to a Claude-app aesthetic (calm, typographic, minimal chrome), and audit whether the laporan-monitoring side already exists in the schema (spoiler: it does — most "missing" features are already there but underused).

Principles applied throughout:
- **DRY** — one piece of information appears in one place. Today's screen has the predicted instansi rendered three times in three different cards; that's the bug.
- **KISS** — fewer cards, fewer borders, fewer pastel fills. Hierarchy comes from typography and spacing, not from boxes.
- **YAGNI** — don't add features (notifications, moderator dashboards, lookup tables) that the thesis doesn't need. Surface what already exists.
- **SRP (the S in SOLID)** — each screen has one job. Review screen = "confirm and submit." It is *not* "explain routing logic."

---

## 1. Audit of what already exists (so we stop re-inventing it)

| Concern | Already in code? | Where |
|---|---|---|
| Predicted instansi shown to user | Yes | [`_PredictionHeadline`](smartCityReport/smart_city_reporter_app/lib/features/reports/ai_result_review_screen.dart) on review screen |
| User can override prediction | Yes | [`_InstansiPicker`](smartCityReport/smart_city_reporter_app/lib/features/reports/ai_result_review_screen.dart) |
| Top-3 candidate confidences | Yes | `_TopPredictionsPanel` on review screen |
| Submitted reports list | Yes | [`my_reports_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/my_reports_screen.dart) — filter chips per status, pull-to-refresh |
| Single report status timeline | Yes | [`report_detail_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/report_detail_screen.dart) reads `report_history` table |
| Status enum (submitted / verified / in_progress / resolved / rejected) | Yes | [`ReportStatus`](smartCityReport/smart_city_reporter_app/lib/features/reports/report_models.dart) |
| Supabase tables `reports` + `report_history` | Yes | wired in [`reports_repository.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/reports_repository.dart) |
| Home dashboard with status counts | Yes | [`home_dashboard_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/dashboard/home_dashboard_screen.dart) |

**Conclusion:** the monitoring story is *already complete* end-to-end. No new tables, no new columns, no new screens. The work is purely visual + de-duplication.

What is genuinely missing (and YAGNI says skip):
- Push notifications when status changes — would need FCM, app review, server-side trigger. Skip.
- Moderator-side status updater — your thesis is the citizen-facing app. Skip.
- Status-change webhook to email — out of scope. Skip.

---

## 2. The duplication problem on the Review screen

What today's screen renders, top to bottom:

1. Big photo
2. **Prediction headline card** (blue): "Banjir & Drainase / Dinas Sumber Daya Air / 87.3%" ← shows instansi #1
3. "AI mempertimbangkan deskripsi Anda" pill
4. **Top kandidat panel** with confidence bars ← shows instansi #2 (and #3 if model is split)
5. Divider
6. **Instansi picker** (9 radio rows) — selected row highlighted ← lets user *change* instansi
7. **Routing card** ("Rute pelaporan") with: instansi pill, formal name pill, summary paragraph, "Mengapa rute ini?", and a "Dinas yang disarankan" tile ← shows instansi #3 (the same one already chosen above)

Steps 2, 6, and 7 all answer the same question: *which instansi will this go to?* Step 7 is pure duplication and adds visual noise without adding information. The picker (6) already commits the choice; once the user has picked, restating the choice in a third card is filler.

**Decision: delete the routing card from the review screen.** Keep the routing-card *widget itself* alive — it's still useful in the `/model-test` screen as an explanation aid for examiners. But on the review screen, the picker IS the routing decision.

This is the DRY fix the user called out, and it removes ~80 lines of visual real estate.

---

## 3. Concrete UI changes (per screen)

### 3a. Review screen — [`ai_result_review_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/ai_result_review_screen.dart)

**Remove:**
- The `ClassificationRoutingCard` block (lines that build the "Rute pelaporan" section). Drop the `import` for `classification_routing_card.dart`.
- The "Pilih instansi tujuan" header + helper subtitle (visually noisy; the picker is self-explanatory).
- The big `GradientHeroHeader` at the top — replace with a plain title + one-line subtitle in regular text.
- All the nested `SectionCard` chrome around photo / picker / map / description. Use plain spacing instead.

**Restructure to a single vertical flow:**

```
[ small back arrow + "Review" title in app bar ]

[ photo, full-width, 16px radius, no card around it ]

24px gap

  Diteruskan ke
  Banjir & Drainase                                  (24px / w700)
  Dinas Sumber Daya Air                              (15px / muted)
  Tingkat keyakinan 87.3%                            (13px / muted)

  ┌──────────────────────────────────────────┐
  │ Banjir & Drainase             87.3% ███▌ │     ← inline top-3, no card
  │ Lalu Lintas & Parkir           8.1% ▍   │
  │ Layanan Kelurahan              2.4%      │
  └──────────────────────────────────────────┘

24px gap

  Ganti instansi (opsional)                          (15px / w600)

  ○ Jalan & Trotoar — Dinas Bina Marga
  ● Banjir & Drainase — Dinas Sumber Daya Air        (selected, deep border)
  ○ Layanan Kelurahan — Kelurahan
  …                                                   (full list, vertical)

24px gap

  Lokasi
  [ map, 16px radius, no card around it ]
  Jl. Sudirman No. 123, Jakarta Pusat                (single muted line)

24px gap

  Deskripsi
  [ multiline text field, no card ]

24px gap

  [ primary button: Submit laporan ]
  [ checklist banner only if something missing ]
```

Concrete deletions and simplifications:
- `_DescriptionUsedPill` — remove. The "AI used your description" message is reassuring once but clutters every review. Move that copy to the create-report screen as a one-liner under the description field (already there, actually).
- `_PredictionHeadline` — drop the colored background container. Use plain typography, no boxes. The instansi-lain warning state stays as its own variant (yellow accent on a single row, not a giant box).
- `_TopPredictionsPanel` — drop the "Top kandidat" heading; keep the three rows. If only one prediction is reported, hide the panel entirely.
- `_InstansiPicker` — keep the radio-row layout but drop the selected-row tinted fill and reduce border weight to 1px always; selection shown via a left-edge color bar (4px) and a slight bg darken on tap. This matches the Claude-app vibe.
- Submission checklist (`_SubmissionChecklist`) — only render when something is missing (already does this); when shown, drop the `SectionCard` wrapper and use plain text rows.

**Net effect:** the screen goes from ~7 stacked cards with rounded borders + colored fills to one continuous scroll of typography and spacing. About 200 fewer LoC.

### 3b. Detail screen — [`report_detail_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/report_detail_screen.dart)

This is where users monitor a single report. Today it has GradientHeroHeader + 4 SectionCards. Restructure:

```
[ photo, full-width ]

  Banjir & Drainase                                   (28px / w700)
  Dinas Sumber Daya Air                               (15px / muted)

  [ status pill: ● Verified ]   12 Apr 2026, 11:19    (single inline row)

24px gap

  Status laporan                                      (heading)
  ● Submitted          12 Apr, 11:19  — by you
  ● Verified           12 Apr, 14:22  — Dinas SDA confirmed
  ○ In progress        —              — pending
  ○ Resolved           —              — pending
                                                       (vertical list, no card)

24px gap

  Deskripsi
  [ description text in body size, no card ]

24px gap

  Lokasi
  [ map, 16px radius ]
  Jl. Sudirman No. 123, Jakarta Pusat

24px gap

  Detail laporan                                      (collapsible, optional)
  - Reporter, email, AI prediction, AI confidence, created/updated  
                                                       (a thin metadata table,
                                                        not 6 separate dividers)
```

Status-laporan timeline is the *primary* monitoring surface. Today it's the *fourth* card on the screen, hidden behind metadata. Promote it.

The reporter-metadata block with 6 `_DetailRow`s separated by `Divider`s is too heavy. Replace with a small two-column table — same data, half the vertical space.

### 3c. My-reports list — [`my_reports_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/my_reports_screen.dart)

Keep structure. Tighten:
- Drop the `eyebrow: 'History'` overline on the `PageHeader` — overlines are decorative; they don't carry information.
- Status filter chip strip is fine — just reduce horizontal padding and use the same neutral pill style as everywhere else.
- `ReportListTileCard` (in [`smart_city_ui.dart`](smartCityReport/smart_city_reporter_app/lib/core/widgets/smart_city_ui.dart)) — switch from outlined card with rounded border to a borderless row with a 4px left-edge color accent matching the report status. Same atomic component reused on the detail screen for consistency (DRY).

### 3d. Create-report screen — [`create_report_screen.dart`](smartCityReport/smart_city_reporter_app/lib/features/reports/create_report_screen.dart)

Mostly fine, two tweaks:
- The numbered step-headers (`_StepHeader` with circular "1/2/3") are decorative. Replace with a simple section heading at section weight; the order is obvious from the form layout.
- The "Add a photo" empty-state has a gradient + icon + double label. Reduce to a single dashed-border box with one centered "Tap to add photo" label. Less aspiration, more clarity.

### 3e. Design tokens — [`app_theme.dart`](smartCityReport/smart_city_reporter_app/lib/app/theme/app_theme.dart)

Convergence to a Claude-style palette (no code yet, just the targets):

| Token | Current | Target | Reason |
|---|---|---|---|
| `surface` (page bg) | `#F8F9FA` | `#FAF9F7` | warmer off-white, matches Claude/Apple feel |
| `surfaceElevated` | white card | `#FFFFFF` | unchanged |
| Card border | colored `#E2E8F0` | drop where possible; use 16px radius + invisible boundary via spacing | reduces "boxy" feel |
| Body text | `inkBody` | `#1C1B1A` | near-black, not pure black; warmer |
| Muted text | `inkMuted` | `#6B6962` | warm gray, not cool slate |
| Accent | `accentCyan` `#0E7490` | keep, but use sparingly — only for primary CTAs and selected states | reduce color fatigue |
| Status colors | scattered | one mapping table, consumed by both list rows and detail timeline | DRY |

Section dividers that currently use `Divider(height: 26)` become 24px of empty space. Quieter.

Typography: keep the existing Inter/SF Pro stack but use `fontFeatures: [FontFeature.disable('liga')]` off (default), and explicit `letterSpacing` only on the 28px title (-0.3) and the 12px overlines (+1.0). Everything else inherits.

### 3f. Routing card — [`classification_routing_card.dart`](smartCityReport/smart_city_reporter_app/lib/core/widgets/classification_routing_card.dart)

**Don't delete the file.** It still has a job: the `/model-test` screen uses it as a reference card for examiners ("here is *why* the model picked this instansi"). On the review screen — which is task-focused, not pedagogical — it's noise. So:

- Keep widget definition.
- Remove all references from `ai_result_review_screen.dart`.
- The model-test screen keeps using it as-is.

This is the SRP application: same widget, different screen, different purpose.

---

## 4. Monitoring laporan — gap analysis

You asked whether the schema supports tracking submitted/handled reports. Walking through:

| Question | Already supported | Where |
|---|---|---|
| "Which reports have I submitted?" | Yes | `my_reports_screen` — filter chips, pull-to-refresh |
| "What is the current status of report X?" | Yes | `report_detail_screen` shows status badge in header |
| "Who changed the status, when, with what note?" | Yes | `report_history` table → rendered as timeline on detail screen |
| "Across all my reports, how many submitted vs in-progress vs resolved?" | Yes | Counts already computed in `_StatusFilterBar` (line 45-48) |
| "Did the assigned instansi accept the AI's prediction or override?" | **Not surfaced** | Both `category` and `ai_prediction` columns are stored, but the detail screen doesn't visually compare them |

That last row is the only real gap, and it's a UI gap, not a schema gap. Add one row in the report-detail metadata table:

```
Prediksi AI          Banjir & Drainase (87.3%)
Diteruskan ke        Banjir & Drainase            ← same → no override
                     —or—
Diteruskan ke        Layanan Kelurahan • diubah pelapor
```

That's one comparison line. No new column, no new query, no new screen.

**Genuine YAGNI calls — do not build:**
- A separate "Tracking" screen distinct from "My reports" (it would duplicate `my_reports_screen`).
- A normalized `instansi` lookup table in Supabase (the 9 values are stable; we already have an enum source-of-truth in Dart).
- A websocket/realtime status push (Supabase realtime works automatically through the existing `stream` queries — already enabled).
- A "moderator-side" status updater UI (this is the citizen-facing app; status updates happen server-side via SQL or Supabase Studio).

---

## 5. Phasing

| Phase | What ships | LOC budget | Risk |
|---|---|---|---|
| P0 — review screen DRY fix | Drop routing card; restructure layout per §3a | -200 | low — no schema, no new behavior |
| P1 — detail screen monitoring polish | Promote timeline; metadata table; AI vs assigned row | +30 / -80 | low |
| P2 — list-row + filter-chip restyle | New `ReportListTileCard` shape; reuse on detail screen | -40 | low |
| P3 — design tokens migration | Update palette and typography in `app_theme.dart` | +20 | medium — touches every screen visually; sanity-check on 3 device widths |
| P4 — create-report polish | Drop `_StepHeader`, simplify empty photo state | -60 | low |

Total expected: **~330 LoC removed, ~50 added**. Fewer files grow than shrink — the goal is less code, not more.

Each phase is independently shippable and reviewable. Suggest landing P0 first as a single PR — it's the highest-value, lowest-risk change and it's the one you specifically asked for.

---

## 6. Acceptance checklist

- [ ] Review screen no longer renders any "Rute pelaporan" / `ClassificationRoutingCard` content.
- [ ] Predicted instansi appears exactly **twice** on the review screen: once as the headline ("Diteruskan ke …"), once as the highlighted row in the picker. Not three times.
- [ ] Report detail screen surfaces the `report_history` timeline as the *first* content block under the photo, not the last.
- [ ] AI-vs-assigned comparison line shows on detail screen when the user overrode the prediction.
- [ ] No screen renders more than one `SectionCard` deep — top-level `Column` with spacing, no nested cards.
- [ ] Page background is the warm off-white target (`#FAF9F7`), not the cool gray.
- [ ] On a 360dp-wide device, no text is clipped, no horizontal scroll appears.

---

## 7. Locked decisions (post-review)

1. **Routing card removed from review screen.** Widget kept alive only for `/model-test`. ✅
2. **Headline copy: "Diteruskan ke" (ID) / "Directed to" (EN)**, with i18n via Flutter's official ARB workflow. Default locale = `id`; toggle in Settings. See §8 for the i18n plan. ✅
3. **Status timeline promoted to first content block on detail screen.** Photo shrinks to a compact band; metadata (reporter, email, AI confidence, timestamps) collapsed behind a "Detail teknis" disclosure. Pattern matches every tracking-style UI surveyed (GoSend, Tokopedia order detail, Stripe Dashboard, Linear, LAPOR!). ✅
4. **AI-vs-assigned shown as a single inline line, not a section.** Hidden when there's no override; one muted line "↳ AI semula menyarankan X (62%)" when there is. No new column, no new component. ✅

---

## 8. i18n plan (locked)

Stack: `flutter_localizations` (SDK) + `intl` (already in [pubspec.yaml](smartCityReport/smart_city_reporter_app/pubspec.yaml)) + ARB files. **Zero new dependencies.**

### File layout

```
lib/
  l10n/
    app_en.arb         # English strings, plus @-metadata (descriptions, placeholders)
    app_id.arb         # Indonesian strings (default locale)
    app_localizations.dart        # generated, not hand-edited
    app_localizations_en.dart     # generated
    app_localizations_id.dart     # generated
```

`l10n.yaml` at project root configures codegen (`flutter pub get` re-runs it). The `AppLocalizations` class is auto-generated and consumed via `AppLocalizations.of(context).directedTo` (or just `context.l10n.directedTo` with a small extension).

### Settings wiring

`SettingsController` gets a new field:

```dart
class SettingsState {
  final Locale locale;          // defaults to const Locale('id')
  final bool autoUseCurrentLocation;
}
```

Persisted in `SharedPreferences` under key `settings.locale`. The settings screen gains one new row: a segmented toggle [ Indonesia | English ] that calls `SettingsController.setLocale(...)`.

`MaterialApp.router` reads the locale from the controller:

```dart
MaterialApp.router(
  locale: ref.watch(settingsControllerProvider).locale,
  supportedLocales: const [Locale('id'), Locale('en')],
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  ...
)
```

### Migration approach

- Move strings out screen-by-screen, not all at once. P0 covers the review + detail screens (the two with the most user-visible copy and the screens being redesigned anyway).
- Each ARB key is named by what the string *means*, not where it appears: `directedTo`, `submitReport`, `aiOriginallySuggested`, `statusTimeline`. Reusable across screens (DRY).
- Strings that contain user data (instansi name, dates) use ICU placeholders: `"directedTo": "Diteruskan ke {instansi}"` with `@directedTo: { "placeholders": { "instansi": { "type": "String" } } }`.

### Initial copy table (ID + EN, locked)

| Key | id | en |
|---|---|---|
| `directedTo` | Diteruskan ke | Directed to |
| `aiOriginallySuggested` | AI semula menyarankan {instansi} ({confidence}) | AI originally suggested {instansi} ({confidence}) |
| `statusTimeline` | Status laporan | Report status |
| `technicalDetails` | Detail teknis | Technical details |
| `submitReport` | Submit laporan | Submit report |
| `addPhoto` | Tambahkan foto | Add a photo |
| `addDescription` | Tulis deskripsi | Add a description |
| `descriptionMin` | Minimal 10 karakter | Minimum 10 characters |
| `confirmLocation` | Konfirmasi lokasi | Confirm location |
| `runAiClassification` | Klasifikasi dengan AI | Run AI classification |
| `aiUncertain` | AI tidak yakin instansi yang tepat — pilih kategori manual | AI is uncertain — pick a category manually |
| `instansiPickerHint` | Ganti instansi (opsional) | Change instansi (optional) |
| `confidence` | Tingkat keyakinan {percent} | Confidence {percent} |
| `descriptionUsedHint` | Bahasa Indonesia atau English. Detail spesifik bantu AI. | Indonesian or English. Specific details help the AI. |
| `instansiLain.label` | Instansi Lain | Other agency |

(More keys land in subsequent phases as screens get migrated.)

### Acceptance for the i18n piece

- [ ] Toggling Settings → Language flips every visible string on Review + Detail + Create-Report screens without restart.
- [ ] App boots in Indonesian when no preference is set (first install).
- [ ] No string lives in `String` literals on screens covered by P0; all flow through `context.l10n.<key>`.
- [ ] `flutter analyze` clean; ARB files are valid (codegen runs on `flutter pub get`).

---

## 9. Decisions still open

None for P0–P1. Everything in §7 is locked. Cutting code next.
