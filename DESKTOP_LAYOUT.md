# Desktop layout

Status: accepted specification — implementation tracked separately
Date: 2026-09-18

The desktop (Tauri) app currently renders the responsive web layout inside
its window: a max-width column, a hero that mirrors the selected row item,
and cards without pointer affordance. That layout was designed for phone,
tablet, and TV. The desktop shell is a desktop-first layout that still
shares tv-web's components, per the shared-platform matrix in
`docs/adr/0003-shared-platform-matrix-and-playback-consolidation.md`.

## Decisions

1. **Left sidebar, never expanding.** Navigation is a fixed-width icon rail
   (Home, Search, Library, Settings). It does not collapse, expand, or open
   a drawer; there is no hamburger.
2. **No max width.** Content fills the window. There is no centered column
   cap; rows and grids stretch to the frame.
3. **No mobile UI at small sizes.** The desktop layout never switches to
   the responsive breakpoints. Instead the window enforces a minimum size
   (Tauri min-width/min-height) so the desktop layout is always viable.
4. **Hover and focus on cards.** Cards respond to hover and keyboard focus
   with the same visible effect (outline, elevation, or scale with a short
   transition); pointer and keyboard affordances match.
5. **The hero has its own data.** The hero is decoupled from Continue
   Watching: it renders a mix of the catalogs (rotating or promoted items),
   never the resume row.
6. **Selecting a card opens its info page.** Card selection never mutates
   the hero. One interaction: card → detail page.
7. **Shared components, desktop-only shell.** tv-web's card, row, hero, and
   detail components are reused; only the shell (sidebar, grid, sizing,
   window minimum) is desktop-specific. The responsive web, Tizen, and
   Vizio layout is untouched.
8. **Integrated frameless titlebar (30px).** Full-width dark header (`#141618`)
   at the top of the desktop shell containing the VIPTV brandmark, draggable
   spacer, search pill, bookmarks icon, profile avatar, and window controls
   (minimize, maximize, close). The window drag region is constrained to
   non-interactive areas, with interactive controls explicitly isolated from
   drag events.
9. **Thinner fixed left sidebar (54px).** Positioned directly beneath the 30px
   titlebar, reduced from 72px to 54px for a compact footprint, with centered
   icon buttons and profile avatar.
10. **Scrollbar containment.** The main content scrollable track begins at
    `top: 30px` directly beneath the titlebar, preventing scrollbars from
    overlapping or starting above the window titlebar.

