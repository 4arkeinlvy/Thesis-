# Role: Expert UI/UX Designer
You are an expert UI/UX designer with a deep understanding of modern, minimalist, and seamless interface design. Your task is to redesign the "Smart City" mobile dashboard overview screen to dramatically improve its visual hierarchy, clarity, and aesthetic appeal.

## Objective
Revise the current mobile dashboard to be cleaner, highly intuitive, and visually seamless. The design must adhere to strict UI/UX principles, reducing cognitive load and eliminating visual noise.

## Core UI/UX Ideologies to Apply
1.  **Minimalism & High Signal-to-Noise Ratio:** Remove unnecessary borders, redundant backgrounds, and excessive styling. Every pixel must serve a purpose. 
2.  **Gestalt Principles (Proximity & Similarity):** Group related elements logically. Ensure spacing clearly communicates relationships between the header, section titles, and cards.
3.  **Atomic Design:** Think in terms of reusable components. The status cards should follow a strict, scalable pattern.
4.  **Accessibility (WCAG 2.1):** Ensure all text and icons meet contrast ratio requirements (minimum 4.5:1 for normal text).

## Grid, Spacing, and Layout (Topology)
* **Grid System:** Implement a strict **8-point grid system**. All margins, paddings, and heights must be multiples of 8 (e.g., 8, 16, 24, 32) to ensure a mathematically harmonious layout.
* **Screen Padding:** Use a consistent 24px horizontal padding for the main screen layout.
* **Section Spacing:** Maintain a 32px vertical gap between the main header card and the "Overview" section to clearly separate context from actions.

## Typography
* **Typeface:** Use a modern, geometric sans-serif typeface (e.g., Inter, SF Pro, or Roboto). 
* **Hierarchy:**
    * *Overline (SMART CITY):* 12px, uppercase, medium weight, letter-spacing: 1px.
    * *Greeting (Hi, Name):* 24px, bold or semi-bold.
    * *Body/Subtitle:* 14px, regular, muted opacity for lower contrast against the background.
    * *Card Numbers:* 28px - 32px, semi-bold.
    * *Card Labels:* 13px, medium.
* **Rule:** Limit the number of font sizes and weights. Rely on color and weight, rather than just size, to establish hierarchy.

## Color Palette & Contrast
* **Primary Header:** Maintain a cohesive blue but consider a softer, more modern gradient or a solid deep blue with glassmorphism elements. Ensure the Avatar circle (currently "UA") has sufficient contrast—consider a white background with blue text for the avatar, or a distinctly darker/lighter shade of blue.
* **Background:** Use a true off-white or very light grey (e.g., `#F8F9FA`) for the app background to make the white cards pop.
* **Semantic Colors (Cards):** * Instead of full pastel backgrounds for the cards, use **pure white cards** with subtle, soft drop shadows (e.g., `0px 4px 12px rgba(0,0,0,0.05)`).
    * Use the semantic colors (Blue for Submitted, Yellow/Orange for In Progress, Green for Verified/Resolved) *only* on the icons or as a subtle left-border accent. This reduces color fatigue and looks significantly cleaner.
    
    * *Note on the current design:* "Verified" and "Resolved" currently use very similar green backgrounds. Differentiate them either by icon style or by using a distinct color (e.g., a teal or purple for one).

## Component Guidelines

### 1. The Welcome Header
* Adjust the border-radius to 24px for a modern feel.
* Align the text perfectly to the left edge of the internal padding (e.g., 24px padding inside the card).
* Increase the contrast of the "UA" avatar.

### 2. The Overview Section Header
* "Overview" text should be 18px, Semi-Bold, Dark Slate/Charcoal.
* "See all" should be 14px, Medium, Primary Blue.
* Align perfectly with the edges of the grid.

### 3. The 2x2 Status Cards
* **Clean Approach:** White backgrounds, 16px border-radius, subtle shadow.
* **Internal Padding:** 16px or 20px uniform padding.
* **Iconography:** Use a consistent icon set (e.g., Phosphor Icons, Feather Icons). Icons should be housed in a small, subtly tinted circle (using the semantic color at 10-15% opacity).
* **Layout inside Card:** * Top-left: Icon in its circular container.
    * Bottom-left: The large Number, with the Label immediately below it (tight line height).

## Expected Output
Please provide a high-fidelity mockup or the structural code (React/Tailwind) that strictly implements these guidelines, resulting in a premium, seamless, and frictionless user interface.

---

## Flutter Implementation Plan (adapted from the brief above)

The app is Flutter + Riverpod (not React/Tailwind), so the spec is mapped onto our existing
design system in [lib/app/theme/app_theme.dart](smartCityReport/smart_city_reporter_app/lib/app/theme/app_theme.dart)
and [lib/core/widgets/smart_city_ui.dart](smartCityReport/smart_city_reporter_app/lib/core/widgets/smart_city_ui.dart).

### Token changes (`AppPalette` + `TextTheme`)
| Token | Before | After | Reason |
|---|---|---|---|
| `surface` | `#F5F7FB` | `#F8F9FA` | Spec off-white background |
| `accentTeal` (new) | — | `#0D9488` | Differentiate Verified vs Resolved |
| `headlineSmall` (greeting) | 22 / w800 | 24 / w700 | "Hi, Name" at 24px semi-bold |
| `titleLarge` (section) | 18 / w700 | unchanged | Already matches "Overview" spec |
| `labelMedium` (overline) | 12 / w600 | 12 / w500 @ 1.0 tracking | Overline rule |

### Component changes
- **[MetricCard](smartCityReport/smart_city_reporter_app/lib/core/widgets/smart_city_ui.dart)** —
  white `surfaceElevated` background, 16px radius, soft shadow (`0 4 12 rgba(0,0,0,0.05)`),
  no tinted fill, no colored border. Icon in a 40px circle tinted at 12% opacity.
  Number is 28px w700; label is 13px w500.
- **`_GradientHeader`** — internal padding bumped to 24px on all sides.
- **`ProfileAvatar`** — new `onDarkSurface` flag: white background + deep-blue text for
  WCAG 4.5:1 contrast when placed on the gradient header.
- **`_SectionLabel` / "See all"** — uses `accentBlue` at 14px w500.

### Screen-level (`HomeDashboardScreen`)
- Horizontal page padding normalised to 24px (8-grid).
- Vertical gaps snapped to 8-grid: **32px** after gradient header, **16px** between a
  section label and its content, **24px** between sections.
- Resolved card switches to `accentTeal` so Verified (green) and Resolved are visually distinct.

### Backend / non-UI fix bundled with this change
`AuthRepository._uploadProfilePhoto` currently (a) trusts the user-supplied file extension
and (b) uploads without a `contentType`, so the Supabase public URL is served as
`application/octet-stream` (browsers download instead of render). Fix:
- Validate the extension against a `{jpg, jpeg, png, webp, heic}` whitelist and reject
  anything else (stops storing arbitrary file types in the public bucket).
- Pass an explicit `contentType` so the public URL gets the right image MIME type.