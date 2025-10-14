# 🎨 SH Parts Theme & UI Guide

_Updated: 14 Oct 2025_

This guide captures the shared design language for SH Parts so every page stays readable, consistent, and adaptable across dark, light, day-blue, camel-dune, and olive-sage modes.

---

## 1. Color System

All colors are exposed as CSS custom properties inside `static/css/style.css` and switch automatically per theme.

| Token | Dark Blue | Light | Day Blue | Camel Dune | Olive Sage | Purpose |
|-------|-----------|-------|----------|------------|------------|---------|
| `--bg` | `#0f172a` | `#f8fafc` | `#e9f2ff` | `#f2e2c4` | `#f5f5dc` | App background |
| `--card-bg` | `#111c2f` | `#ffffff` | `#ffffff` | `#fbf1dc` | `#fafaf5` | Cards, panels, modals |
| `--text` | `#f8fbff` | `#0f172a` | `#10203e` | `#3f2f1c` | `#2d3319` | Primary text |
| `--text-secondary` | `#9aa6bf` | `#475569` | `#536480` | `#8c6f4a` | `#6b7c59` | Secondary text |
| `--border-color` | `rgba(148, 163, 184, 0.25)` | `rgba(15, 23, 42, 0.12)` | `rgba(16, 32, 62, 0.16)` | `rgba(114, 89, 58, 0.18)` | `rgba(45, 51, 25, 0.16)` | Dividers, table lines |
| `--primary` | `#3b82f6` | `#2563eb` | `#2563eb` | `#c08457` | `#6b8e23` | Buttons & highlights |
| `--primary-600` | `#2563eb` | `#1d4ed8` | `#1e40af` | `#a5663d` | `#556b2f` | Hover/active state |
| `--accent-color` | `#22d3ee` | `#0ea5e9` | `#1b4ed4` | `#d8a368` | `#9acd32` | Accent elements |
| `--success` | `#22c55e` | `#16a34a` | `#15803d` | `#3f7f4c` | `#4d7c0f` | Positive states |
| `--warning` | `#f97316` | `#ea580c` | `#c2410c` | `#c9772d` | `#d97706` | Warnings |
| `--danger` | `#ef4444` | `#dc2626` | `#b91c1c` | `#b94a37` | `#b91c1c` | Errors |
| `--info` | `#0ea5e9` | `#0284c7` | `#0369a1` | `#0f5f66` | `#0f766e` | Informational |

> ✅ Don’t hard-code colors in templates. Always use the CSS variables or utility classes that reference them.

Supporting surface tokens:

- `--input-bg`, `--input-border`, `--input-ring` — control field backgrounds, borders, and focus rings.
- `--table-header-bg`, `--table-row-hover` — provide accessible table contrast.
- `--shadow-soft`, `--shadow-card` — depth presets for flyouts and cards.

### Theme presets

| Theme key | Use-case | Primary | Background | Notes |
|-----------|----------|---------|------------|-------|
| `dark-blue` | Default immersive dashboard | `#3b82f6` | `#0f172a` | High-contrast dark shell |
| `light` | Bright neutral UI | `#2563eb` | `#f8fafc` | Matches standard Bootstrap light mode |
| `day-blue` | Daytime blue accented palette with deep navy highlights | `#2563eb` | `#e9f2ff` | Keeps cards white while typography remains navy for readability |
| `camel-dune` | Desert-inspired warm tone with gentle motion | `#c08457` | `#f2e2c4` | Animated sand gradient; honors `prefers-reduced-motion` |
| `olive-sage` | Alternative earthy tone | `#6b8e23` | `#f5f5dc` | Subtle muted palette |

### Elevation
- `--shadow-soft`: `0 16px 40px rgba(15, 23, 42, 0.35)`
- `--shadow-card`: `0 12px 32px rgba(15, 23, 42, 0.25)`

---

## 2. Typography

- **Font stack** (already loaded): `"Cairo", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif`.
- **Base font size**: 16px (`1rem`).
- **Line height**: 1.55 for body copy, 1.2 for headings.
- **Heading scale**
  - h1: 2rem / 32px
  - h2: 1.75rem / 28px
  - h3: 1.5rem / 24px
  - h4: 1.25rem / 20px
  - h5: 1.125rem / 18px

> ✨ Use `fw-semibold` (500) for labels and secondary headings. Keep body text at weight 400.

---

## 3. Spacing & Layout

- **Grid spacing units**: 4px (xxs), 8px (xs), 12px (sm), 16px (md), 24px (lg), 32px (xl), 48px (xxl).
- **Card padding**: `24px` horizontal, `20px` vertical.
- **Section spacing**: `32px` top/bottom between major blocks.
- **Border radius**: `16px` for cards & modals, `10px` for inputs, `50%` for circular badges.

---

## 4. Component Guidelines

### Cards & Panels
- Use `.card-theme` helper (added in CSS) or `card` inside `.content-area`.
- Background: `var(--card-bg)`.
- Text: `var(--text)` with muted copy using `var(--text-secondary)`.
- Apply `box-shadow: var(--shadow-card)` sparingly—only for dashboard stats.

### Tables
- Header row: uppercase, medium weight, `color: var(--text)`.
- Row hover: `background: rgba(59, 130, 246, 0.08)`.
- Zebra striping optional; if used, rely on `rgba(148, 163, 184, 0.08)`.

### Forms
- Inputs: `background: rgba(255,255,255,0.04)` in dark mode, `#ffffff` in light, using tokens via a `.form-control-theme` class.
- Placeholder text: `color: var(--text-secondary)` with `opacity: 0.85`.
- Focus state: `outline: none; box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25)`.

### Buttons
- `.btn-primary`: use `--primary` tokens; `.btn-outline-*` rely on `var(--border-color)`.
- Provide `.btn-soft-{state}` utilities for secondary/tertiary emphasis.

### Badges & Pills
- Use `.badge-state` helpers: `.badge-success`, `.badge-warning`, `.badge-danger`, `.badge-info`.
- Badge text is forced to a light color (`#fff`) so ensure backgrounds leverage the state tokens for contrast.
- Keep text bold with `letter-spacing: 0.02em` for readability.

### Modals
- No hard-coded white backgrounds; inherit tokens.
- Internal forms follow the same input rules as global forms.

---

## 5. Accessibility Checklist

- **Contrast**: Maintain ≥ 4.5:1 on body text, ≥ 3:1 on large text (18px+).
- **Focus states**: All interactive elements must have visible focus (CSS already provides focus ring via tokens).
- **RTL/LTR**: Layout is direction-aware; prefer logical properties (`margin-inline-end`) when adding CSS.
- **Motion**: Transitions capped at 200ms; avoid large movement animations that could trigger motion sickness.
- **Camel Dune motion**: Animated sand gradient loops every 28–40s and pauses when `prefers-reduced-motion` is enabled.

---

## 6. Implementation files

- `static/css/style.css` — theme tokens, layout, component styling.
- `static/css/color-improvements.css` — legacy overrides; consolidate into `style.css` while refactoring.
- `templates/base/base.html` — layout shell; avoid inline colors.

When creating new UI elements, extend the helpers in `style.css` and update this guide if new patterns are introduced.
