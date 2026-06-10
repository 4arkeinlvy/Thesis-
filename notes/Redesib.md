# UI/UX Redesign Prompt: Refinement & Alignment

**Role:** Expert UI/UX Designer  
**Inspiration:** Claude iOS App, Apple Human Interface Guidelines (Clean, Minimalist, High-Typography Focus)

## Objective
Refine the current dashboard layout. The horizontal metric row is a great structural improvement, but the header color feels disconnected, and the horizontal alignment (margins and padding) is inconsistent. Elevate the design to feel like a premium, top-tier application.

## 1. Header Aesthetic (Color & Contrast)
The current dark purple gradient is too heavy and clashes with the clean white background. We need a modern, sophisticated aesthetic.
* **Color Palette:** Replace the heavy gradient with a signature minimalist approach inspired by apps like Claude. 
    * *Option A (Soft & Warm):* Use a very soft, warm off-white or cream (e.g., `#FAF9F7`) for the header card with a delicate 1px border (`#EAEAEA`) and crisp, dark charcoal typography.
    * *Option B (Sleek Dark):* Use a solid, premium dark gray (`#222222`)—no gradients—with stark white text for high contrast.
* **Mockup Data Update:** Ensure the prototype uses the correct details. Update the header greeting to **"Hi, Umam"** and change the avatar text to **"UA"**. 

## 2. Strict Horizontal Alignment (Grid System)
The left and right spacing ("kanan kirinya") is currently floating and misaligned. You must establish a rigid layout axis.
* **Global Margins:** Define a strict global horizontal margin (e.g., **24px**) for the entire screen.
* **The Left Axis:** The following elements MUST perfectly align on the exact same invisible vertical line (24px from the left screen edge):
    * The internal padding of the header text ("SMART CITY" and "Hi, Umam").
    * The "Overview" and "Nearby reports" section titles.
    * The left edge of the first metric icon (Submitted).
    * The exact left edge of the map component.
* **The Right Axis:** Similarly, align the right-side elements (Avatar, "See all", "Open map", and the right edge of the map) precisely 24px from the right screen edge.

## 3. Metric Row Distribution
* Instead of letting the metrics float, use a strict grid or flexbox layout (e.g., `justify-content: space-between`). 
* Anchor the first metric perfectly to the left margin and the fourth metric perfectly to the right margin, distributing the remaining space equally between them so they feel anchored and deliberate.

## Expected Output
Provide the updated mockup or structural UI code (React/Tailwind) that strictly enforces these horizontal alignment rules and implements the new, refined minimalist header palette.