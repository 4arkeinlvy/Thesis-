# Dashboard Home Refinement + FAB Repositioning — Plan

Status: draft. Small-surface change. Touches only [home_dashboard_screen.dart](smartCityReport/smart_city_reporter_app/lib/features/dashboard/home_dashboard_screen.dart) and [app_shell_scaffold.dart](smartCityReport/smart_city_reporter_app/lib/core/widgets/app_shell_scaffold.dart). No new files, no schema, no routing.

---

## 1. What's there today (audit)

Reading [home_dashboard_screen.dart](smartCityReport/smart_city_reporter_app/lib/features/dashboard/home_dashboard_screen.dart):

1. **Header** — `PageHeader` with `variant: PageHeaderVariant.gradient`, an "SMART CITY" eyebrow, "Hi, {firstName}", a one-liner subtitle, and a profile avatar trailing.
2. **Overview** label + "See all" → 4 metrics in a single row (`Submitted / Verified / In Progress / Resolved`), each a count + label + colored icon. Already borderless and clean.
3. **Nearby reports** label + "Open map" → 220px map preview with up to 12 nearby pins.
4. **Recent submissions** label → up to 3 of the user's most recent reports as `ReportListTileCard` rows.
5. **FAB** — extended `FloatingActionButton.extended(label: 'Report', icon: add_a_photo)` pinned at `FloatingActionButtonLocation.endFloat` (bottom-right). Bottom navigation bar has 4 destinations (Home / Map / Reports / Profile).

What's actually wrong:
- The gradient hero is heavy compared to everything else on the screen — it's the visual outlier. Claude/Linear/Apple don't use color blocks for screen headers; they use typography.
- The `eyebrow: 'SMART CITY'` adds nothing the user doesn't already know.
- "Hi, Citizen" with no name (because profile loaded as anonymous) shows often during refresh — UX flicker.
- The FAB position fights the bottom-navigation 4-tab layout: it lands on top of the right tabs and feels disconnected from any of them.
- "See all" / "Open map" right-aligned text buttons in `accentBlue` are slightly competing with the bottom-nav blue selection.

What's actually fine and should NOT change:
- The 4-metric strip is already clean (borderless, typography-driven). Don't redesign.
- The map preview block is already minimal.
- The recent-submissions list shape is fine.
- The bottom navigation 4-tab structure is fine.

---

## 2. Reference apps surveyed (FAB + clean dashboard)

For the **FAB position** question. Researched what mature, popular apps do when the primary action lives alongside a bottom nav:

| App | Primary action placement | Pattern |
|---|---|---|
| **Twitter/X** | Bottom-center embedded in nav bar (Compose) | Center notch, slightly raised button |
| **Instagram** | Bottom-center as the 3rd of 5 tabs (Create) | Tab integrated, monochrome icon |
| **Strava** | Bottom-center as 3rd of 5 tabs (Record) | Filled accent circle inside nav |
| **Google Maps** | Bottom-right floating "Go" button | Classic FAB |
| **Gmail** | Bottom-right "Compose" extended FAB | Classic FAB |
| **Apple Maps / Notes** | Top-right or center, no FAB | Toolbar action |
| **Linear (mobile)** | Bottom-right FAB | Classic FAB |
| **TikTok** | Bottom-center plus-button between tabs | Notched accent button |
| **Threads** | Bottom-center "Create" tab | Tab-integrated |
| **GoJek / Grab / Tokopedia** | Either bottom-right FAB or floating central button raised above nav | Mixed |

The pattern that matches the user's request ("middle bottom, but clean relative") and is used by the most apps in 2024-2025 is the **Twitter/Instagram/TikTok pattern**: a single primary action button **integrated as a center item in the bottom navigation**, slightly raised or styled distinctly, between the existing tabs.

Why this works specifically for a citizen-reporting app:
- The "Lapor" action is the *single most important* thing the user does. It deserves the most thumb-friendly position (center bottom, the easiest reach with one-handed use on a 6"+ phone).
- Bottom-right FAB is fine when you have ≤3 nav tabs. With 4 tabs, the FAB physically obscures the rightmost tab on small screens, which is exactly what's happening today.
- Center-anchored matches government/civic-app conventions in Indonesia (Tokopedia's central play, Gojek's transactions). Familiar gesture.

What we will NOT do:
- Move it to top app bar — primary actions belong at the bottom on mobile (Apple HIG, Material 3).
- Add a notched cutout in the nav bar (Material's `BottomAppBar` notched FAB pattern). That's classic but visually heavy and feels dated next to a Claude-aesthetic app. Cleaner approach: keep the bar flat, place the FAB centered just *above* the bar, no notch.

---

## 3. Concrete changes (small-surface)

### 3a. Header — replace `PageHeaderVariant.gradient` with the plain typographic header

In [home_dashboard_screen.dart](smartCityReport/smart_city_reporter_app/lib/features/dashboard/home_dashboard_screen.dart):

**Before** (lines 31-49):
```dart
AsyncView(
  value: profileAsync,
  loading: const PageHeader(
    title: 'Welcome back',
    subtitle: 'Loading your dashboard…',
    variant: PageHeaderVariant.gradient,
  ),
  data: (profile) => PageHeader(
    eyebrow: 'Smart City',
    title: 'Hi, ${profile?.fullName.split(' ').first ?? 'Citizen'}',
    subtitle: 'Track submissions and nearby incidents at a glance.',
    variant: PageHeaderVariant.gradient,
    trailing: ProfileAvatar(...),
  ),
),
```

**After**: drop the gradient variant, drop the eyebrow, drop the subtitle filler. Keep the greeting (warm) + avatar (functional).

```dart
AsyncView(
  value: profileAsync,
  loading: const _Greeting(name: null),
  data: (profile) => _Greeting(name: profile?.fullName.split(' ').first),
),
```

Where `_Greeting` is a 30-line local widget: small "Selamat datang" / "Welcome back" overline (12px muted), then a single 28px line "Hi, {name}" or just "Hi" if the name isn't loaded yet (no "Citizen" placeholder). Avatar stays right-aligned, sized 40px. No background fill, no card chrome.

This is the single biggest visual win — the screen stops being "gradient block + flat content" and becomes one continuous typographic flow.

### 3b. Section labels — keep, but mute the action

The "See all" / "Open map" right-side actions stay (useful navigation). Tone them down: drop the `accentBlue` color, use `inkMuted` text + a small chevron `›`. Same widget, different style. ~5 lines edited in `_SectionLabel`.

```
Overview                                 See all ›
```

### 3c. Subtle spacing tightening (8-grid)

Today's gaps are 32 / 16 / 24 / 16 / 24 / 16 — a mix. Standardize to 8-grid: **24px between sections, 12px between section label and content**. Only spacing tweaks, no layout reflow.

### 3d. Greet copy — i18n

Add 2 keys to ARB:
```
"greetingFallback": "Selamat datang" / "Welcome"
"greetingNamed": "Hi, {name}"
```

Used by `_Greeting` widget.

### 3e. Nothing else changes on the dashboard

Specifically:
- `_MetricsGrid` — untouched (already clean).
- `ReportMapView` height/zoom — untouched.
- `ReportListTileCard` rows — untouched.
- `EmptyStateCard` text — already i18n'd elsewhere.
- The order of sections — untouched.

---

## 4. FAB repositioning — concrete change

### 4a. Move from bottom-right to bottom-center

In [app_shell_scaffold.dart](smartCityReport/smart_city_reporter_app/lib/core/widgets/app_shell_scaffold.dart):

**Before** (line 30):
```dart
floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
```

**After**:
```dart
floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
```

That's the one-line change for the location. Plus a small visual polish on the FAB itself so it reads as "the primary action" rather than just a button:

- Switch from `FloatingActionButton.extended` → `FloatingActionButton` (compact, circular, single-icon). The "Report" text label was protecting against bottom-right ambiguity; centered, the icon alone is unambiguous (especially `add_a_photo`).
- Size: 56×56dp (Material default, comfortable for thumb).
- Use `palette.accentCyan` background, white icon. No shadow elevation > 4 (Claude-aesthetic prefers shallow shadows).

Optional micro-polish:
- Add `tooltip: 'Lapor'` / `'Report'` for accessibility (TalkBack reads it; long-press shows it).
- The FAB position raises slightly above the nav bar via `extendBody: true` (already set). No notched cutout.

### 4b. Why the bottom navigation bar still works with a centered FAB

The 4 tabs (`Home / Map / Reports / Profile`) remain evenly distributed across the full bar width. The FAB hovers above the bar, centered horizontally, ~6px above the bar's top edge. There's no overlap because the FAB is on its own `floatingActionButton` slot — Flutter's layout already inserts the right safe spacing.

If you want the FAB to feel more "anchored" to the nav (the Twitter/Instagram look), there's a stronger version: replace the 4-tab `NavigationBar` with a 5-slot custom row where the middle slot is the FAB. **Plan rejects that** — too invasive for a "small change" request, and we'd lose Material 3's built-in `NavigationBar` accessibility/animation.

So: keep the standard 4-tab `NavigationBar`, just move the existing FAB from `endFloat` → `centerFloat`. Two lines of code. Clean.

### 4c. What this looks like

```
┌─────────────────────────────────────┐
│                                     │
│           [dashboard content]       │
│                                     │
│                                     │
│                ⊕                    │  ← FAB, centered, 56dp circle
│                                     │
│  🏠      🗺      📋      👤        │  ← nav bar, 4 evenly-spaced tabs
└─────────────────────────────────────┘
```

Matches the Gmail / Google Maps style of "FAB above the bar" but centered for thumb reach. Doesn't try to be Twitter (notched) or TikTok (integrated) — those need bigger structural changes.

---

## 5. What this is NOT (YAGNI fences)

- **Not** a redesign of the bottom nav itself.
- **Not** a redesign of any other screen (Map, Reports list, Profile, Settings, Detail, Review, Create — all untouched).
- **Not** a new theme.
- **Not** a notched FAB or a 5th nav tab.
- **Not** new metrics or new sections on dashboard.
- **Not** a hero illustration / promo banner / news feed.

Total LoC budget: **~80 added, ~40 removed**. Net +40, mostly the new `_Greeting` widget.

---

## 6. Phasing

Single PR. No phases. The change is small enough to ship at once.

| Step | Change |
|---|---|
| 1 | Add `greetingFallback` + `greetingNamed` to both ARB files; regen with `flutter gen-l10n`. |
| 2 | Replace gradient `PageHeader` block with `_Greeting` widget in `home_dashboard_screen.dart`. |
| 3 | Mute "See all" / "Open map" actions (color → `inkMuted`, append `›`). |
| 4 | Standardize gaps to 24/12 grid in `home_dashboard_screen.dart`. |
| 5 | Change `floatingActionButtonLocation` from `endFloat` → `centerFloat` in `app_shell_scaffold.dart`. |
| 6 | Switch `FloatingActionButton.extended` → compact circular FAB with `tooltip`. |

---

## 7. Acceptance checklist

- [ ] No gradient hero anywhere on the dashboard.
- [ ] First content under the app bar is a single greeting line, no eyebrow, no subtitle copy.
- [ ] Profile avatar still rendered, right-aligned, 40dp.
- [ ] FAB sits centered above the bottom navigation, circular, single icon.
- [ ] Bottom-nav 4 tabs still evenly distributed; no overlap with FAB on a 360dp width device.
- [ ] On Indonesian locale: "Hi, {name}" renders; on English: "Hi, {name}".
- [ ] When profile is still loading, header shows just "Welcome" / "Selamat datang" — not "Hi, Citizen".
- [ ] `flutter analyze` clean; tests still pass.

---

## 8. Decisions still open

None. Plan is small enough to execute as-is. Want me to ship it now? Yes/no.
