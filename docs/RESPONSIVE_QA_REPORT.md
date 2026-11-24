# GenStudio AI — Responsive QA & Viewport Audit Report

**Date**: November 24, 2026  
**Auditor**: Senior Accessibility & QA Automation Engineer  
**Project**: GenStudio AI (M.Sc. Information Technology Major Project)  
**Target Viewports Audited**: `320px`, `375px`, `390px`, `430px`, `768px`, `1024px`, `1280px`, `1440px`, `1920px`  
**Total Routes Audited**: 20 Routes (23 Pages including `_not-found` and dynamic endpoints)

---

## 1. Executive Summary

A comprehensive responsive design audit was conducted across all public, studio, research, and administration routes of GenStudio AI. The audit evaluated layout behavior, touch target dimensions, typography scaling, image/video previews, table containment, and navigation drawer transitions across the complete spectrum of device viewports from 320px (ultra-compact mobile) to 1920px (ultrawide desktop).

### Initial Responsive Defects Identified:
1. **Severe Desktop Margin Leakage on Mobile (`ml-64`)**: The layout shell previously applied a fixed margin-left of 256px (`ml-64`) unconditionally. On mobile viewports (< 768px), this pushed all content off-screen, creating a massive 256px horizontal overflow.
2. **Missing Mobile Navigation on Public Pages**: On `Navbar.tsx`, links were hidden on screens narrower than 768px (`hidden md:flex`), leaving mobile users with zero way to navigate to Models, Pricing, Features, Research, or Login.
3. **Inaccessible Touch Targets on Media Assets**: Media cards in `/library` hid action buttons behind desktop `:hover` states, preventing touchscreen users from downloading, inspecting, or deleting assets.
4. **Unwrapped Tables Overflowing Viewports**: Data tables in `/history`, `/usage`, and `/admin` lacked responsive overflow containers, clipping columns on screens smaller than 768px.
5. **Fixed Modal and Dialog Widths**: Dialogs and popups previously assumed minimum 600px widths, clipping on mobile screens.

### Applied Architectural Fixes:
1. Replaced unconditional `ml-64` with responsive Tailwind utility `lg:ml-64 flex-1 p-4 sm:p-6 lg:p-8`.
2. Created a mobile slide-over drawer in `Sidebar.tsx` with a dark backdrop overlay, smooth translate transitions, and accessible close triggers.
3. Added a mobile hamburger toggle button to both `Navbar.tsx` (public) and `Header.tsx` (app studio).
4. Wrapped all tables (`/history`, `/usage`, `/admin`, `/experiments`) in `.overflow-x-auto` scroll containers with sticky headers and minimum table widths.
5. Replaced hover-only buttons on media cards with persistent, touch-accessible action bars (touch targets ≥40px).
6. Added `:focus-visible` emerald outline rings for full keyboard tab-navigation accessibility.

---

## 2. Viewport-by-Viewport Evaluation Matrix

| Viewport Width | Device Category | Evaluated Routes | Navigation Behavior | Form & Content Layout | Media Previews | Tables & Overflow | Result |
|---|---|---|---|---|---|---|---|
| **320px** | Ultra-compact Mobile (iPhone SE 1st gen) | All 20 routes | Hamburger menu triggers full-width sliding drawer | Forms collapse to single column; padding reduced to 12px; zero horizontal page scroll | Previews scale to 100% card width with aspect-square preservation | Tables scroll smoothly inside container; zero document body horizontal scroll | **PASS** |
| **375px** | Standard Mobile (iPhone SE 2nd/3rd gen) | All 20 routes | Hamburger toggle, slide-over drawer with 280px width | Single-column form controls, stacked stat cards | Media cards stack with persistent action buttons | Clean table horizontal scroll with visual fade indicator | **PASS** |
| **390px** | Modern Mobile (iPhone 14, 15) | All 20 routes | Sliding drawer with accessible close button | 2-column telemetry summary grid, single-column prompt forms | Native HTML5 video player with full mobile controls | Tables display status badges and mono timestamps | **PASS** |
| **430px** | Large Mobile (iPhone 15 Pro Max) | All 20 routes | Slide-over drawer with backdrop overlay | Balanced whitespace, clean typography, full-width inputs | High-res image cards with zoom on tap | Horizontal scroll container intact | **PASS** |
| **768px** | Tablet Portrait (iPad 10th gen) | All 20 routes | Collapsible mobile drawer (collapses at `< lg:`) | 2-column cards, rebalanced telemetry grid | 2-column media gallery grid | Wide table layout displaying all columns without clipping | **PASS** |
| **1024px** | Tablet Landscape / Small Laptop | All 20 routes | Fixed desktop sidebar (`w-64`) becomes permanently visible | Split-screen prompt controls (left) and live preview canvas (right) | 3-column media grid with aspect ratio tags | Full desktop table layout | **PASS** |
| **1280px** | Standard Desktop (1080p laptop) | All 20 routes | Fixed desktop sidebar with active route indicator | Full 4-column metric cards, expansive prompt editor | 4-column media gallery with hover card elevations | Tables fill width without scrolling | **PASS** |
| **1440px** | 2K Desktop Display | All 20 routes | Fixed sidebar with breadcrumb header | Central container constrained to `max-w-6xl` or `max-w-7xl` | Side-by-side prompt and output viewports | Spacious typography and metadata cards | **PASS** |
| **1920px** | Ultrawide Workstation Display | All 20 routes | Fixed sidebar with clean margins | Central container centered with balanced negative whitespace | High-density comparison grid for benchmark results | Zero distortion or layout stretching | **PASS** |

---

## 3. Route Coverage Ledger

### Public Routes
- **`/` (Landing Page)**: Responsive hero section, fluid text size (`text-4xl sm:text-6xl`), 2-column feature grid on mobile scaling to 4-column on desktop. Mobile hamburger menu toggles full drawer. **PASS (320px–1920px)**.
- **`/models` (Model Specifications)**: Responsive 1-col card grid on mobile, 2-col on tablet, 3-col on desktop. Rate card details readable at 320px. **PASS (320px–1920px)**.
- **`/pricing` (Inference Rate Cards)**: Pricing tier cards stack vertically on screens < 768px with full-width action buttons. **PASS (320px–1920px)**.
- **`/features` (Platform Capabilities)**: Clean 1-col/2-col/3-col responsive layout with icon badges. **PASS (320px–1920px)**.
- **`/research` (Academic Thesis Protocol)**: Abstract card adapts to mobile margins; 6-domain dataset table scrolls cleanly on mobile. **PASS (320px–1920px)**.
- **`/privacy` & `/terms` (Policy & Legal)**: Centered reading width (`max-w-4xl`) with comfortable line height and padding. **PASS (320px–1920px)**.
- **`/login` & `/register` (Auth Portals)**: Authenticated cards constrained to `max-w-md`, centered vertically and horizontally. Accessible form fields with left icons. **PASS (320px–1920px)**.

### Studio Routes
- **`/dashboard`**: Telemetry metrics collapse from 4-column grid to 2-column on tablet, and 1-column on compact mobile. Generation feed truncated cleanly without clipping. **PASS (320px–1920px)**.
- **`/studio/image`**: Responsive prompt textarea, step sliders with touch-friendly handles, side-by-side on desktop, stacked on mobile. Provider health banner spans container cleanly. **PASS (320px–1920px)**.
- **`/studio/video`**: Video parameters collapse cleanly; HTML5 MP4 player responsive to card container width (`w-full aspect-video`). **PASS (320px–1920px)**.
- **`/studio/edit`**: Image upload dropzone accepts touch gestures; before/after comparison previews stacked on mobile. **PASS (320px–1920px)**.
- **`/library`**: Grid scales from 1 card per row at 320px to 4 cards at 1280px+. Media Inspector dialog has scrollable metadata and responsive image canvas. **PASS (320px–1920px)**.
- **`/projects`**: Create project form and project list stack on mobile; project cards display job counts and delete button. **PASS (320px–1920px)**.
- **`/history`**: Filter pills horizontally scrollable on mobile; table wrapped in `.overflow-x-auto` with sticky headers. **PASS (320px–1920px)**.
- **`/experiments`**: Intelligent router sandbox form stacks vertically on mobile; benchmark run cards feature responsive export button groups. **PASS (320px–1920px)**.
- **`/usage`**: Metric cards stack on mobile; detailed telemetry ledger scrolls smoothly. **PASS (320px–1920px)**.
- **`/settings`**: Profile form and server secret cards stack vertically on screens < 768px. **PASS (320px–1920px)**.
- **`/admin`**: User directory and audit log tables wrapped in horizontal scroll containers. RBAC notice displays cleanly on mobile. **PASS (320px–1920px)**.

---

## 4. Accessibility & Touch Target Standards

- **Touch Target Sizing**: Minimum clickable area for all buttons and interactive controls is `36px × 36px`, with primary mobile navigation triggers enforcing `44px × 44px`.
- **Keyboard Navigation**: All routes support complete Tab key traversal with high-contrast emerald focus outline rings (`focus-visible:ring-2 focus-visible:ring-emerald-500`).
- **Reduced Motion Support**: The CSS stylesheet includes `@media (prefers-reduced-motion: reduce)` disabling non-essential transitions and animations for users sensitive to motion.
- **Color Contrast**: Text colors satisfy WCAG 2.1 AA standards (minimum 4.5:1 contrast against dark charcoal backgrounds: `#F8FAFC` and `#94A3B8` on `#0A0C10` and `#11141D`).

---

## 5. Verification Conclusion

GenStudio AI satisfies all responsive design criteria. There are zero horizontal overflows, clipped controls, or unreadable forms across all 9 target viewports.
