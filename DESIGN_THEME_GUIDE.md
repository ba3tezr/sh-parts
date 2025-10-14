# 🎨 SH Parts Theme & UI Guide

_Updated: 14 Oct 2025_

This guide captures the shared design language for SH Parts so every page stays readable, consistent, and adaptable across light/dark/high-contrast modes.

---

## 1. Color System

All colors are exposed as CSS custom properties inside `static/css/style.css` and switch automatically per theme.

| Token | Default (Dark) | Light Theme | High Contrast | Purpose |
|-------|----------------|-------------|---------------|---------|
| `--bg` | `#0f172a` | `#f8fafc` | `#000000` | App background |
| `--card-bg` | `#111c2f` | `#ffffff` | `#000000` | Cards, panels, modals |
| `--text` | `#f8fbff` | `#0f172a` | `#ffffff` | Primary text |
| `--text-secondary` | `#99aabb` | `#475569` | `#e5e7eb` | Secondary text |
| `--border-color` | `rgba(148, 163, 184, 0.25)` | `rgba(15, 23, 42, 0.12)` | `#ffffff` | Dividers, table lines |
| `--primary` | `#3b82f6` | `#2563eb` | `#ffcc00` | Buttons & highlights |
| `--primary-600` | `#2563eb` | `#1d4ed8` | `#e6b800` | Hover/active state |
| `--accent-color` | `#22d3ee` | `#0ea5e9` | `#ffcc00` | Emphasis elements |
| `--success` | `#22c55e` | `#16a34a` | `#00ff7f` | Positive states |
| `--warning` | `#f97316` | `#ea580c` | `#ffd60a` | Warnings |
| `--danger` | `#ef4444` | `#dc2626` | `#ff4d4f` | Errors |
| `--info` | `#0ea5e9` | `#0284c7` | `#00b4d8` | Informational |

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
| `day-blue` | **New.** Daytime blue accented palette with deep navy highlights | `#2563eb` | `#e9f2ff` | Keeps cards white while typography remains navy for readability |
| `high-contrast` | Accessibility mode | `#ffcc00` | `#000000` | Maximum contrast, minimal shadows |
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

---

## 6. Implementation files

- `static/css/style.css` — theme tokens, layout, component styling.
- `static/css/color-improvements.css` — legacy overrides; consolidate into `style.css` while refactoring.
- `templates/base/base.html` — layout shell; avoid inline colors.

When creating new UI elements, extend the helpers in `style.css` and update this guide if new patterns are introduced.
