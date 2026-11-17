# EPISODE-FILLER-001 — Filler and Mixed labels in episode lists

Status: **proposed**. Source revision: design `e9f2900`; app `edge` `b8a6ff5e`
for the episode rows named below. Refs
[app#1149](https://github.com/viptv-org/app/issues/1149).

## Intent

A viewer browsing an anime season sees which episodes are filler and which mix
canon with filler, so they can choose what to watch. Labels only: nothing is
skipped, hidden, reordered or marked watched, and autoplay is unchanged.

## Where

Every episode row in every layout carries the label:

- Details episode selector: phone and tablet cards, desktop and web rows,
  the browser details dialog in both its compact and wide forms.
- Player Episodes panel: phone, desktop and web picker; TV picker.
- TV Details episode shelf.

## Label

- **Filler** for a filler episode, **Mixed** for mixed canon and filler. Canon
  episodes, episodes with no data and titles with no match carry no label.
- Drawn on the episode still, top-end corner (top-right in left-to-right), so it
  never changes row height or text layout and arrives without shifting the list.
  The TV still's top-start corner keeps its existing art badge.
- Phone, tablet, desktop and web: 11 sp semi-bold, line height 14 sp,
  text-secondary on black at 0.75 alpha, 4 dp radius, 6 dp horizontal and
  2 dp vertical padding, inset 6 dp from the still's edges.
- TV: the existing art-badge metrics: 18 px semi-bold, line height 22 px,
  text-secondary on black at 0.75 alpha, 4 px radius, 10 px horizontal and
  4 px vertical padding, inset 12 px; all scaled with the shelf.
- The label is quiet: no accent colour, no icon, never focusable. It sits under
  the focus outline, the pending spinner and the play affordance, and above the
  artwork and the fallback title.
- Accessibility: the row's accessible content adds **Filler episode** or
  **Mixed canon and filler episode** after the title; no extra focus stop.

## Data

- The backend reads filler classifications from AnimeFillerList, respects its
  `Crawl-delay`, and caches them; see
  [backend#332](https://github.com/viptv-org/backend/issues/332).
- A title matches only when one of its titles (the series title or an
  alternate title) equals an AnimeFillerList show name after normalization
  (case, accents, punctuation and spacing ignored). No match means no labels.
- AnimeFillerList numbers episodes absolutely. A numbered season's episode
  maps to `episodes in earlier numbered seasons + episode number`; Specials
  and unnumbered episodes never carry a label.
- Labels load after the episode list and never delay it. A failed or empty
  lookup draws nothing and shows no error.
- Labels belong to the title, not the profile; switching profile keeps them.

## Credit

Settings › About adds one tertiary line **Filler data: AnimeFillerList.**:
on TV below **Show and episode data from Simkl.**, on phone, tablet, desktop
and web below the notice links. Details shows no credit.

## Acceptance

1. Naruto Shippuden on desktop: episode 26 shows **Filler**, a mixed episode
   shows **Mixed**, a canon episode shows nothing; row heights match.
2. The same title on phone, tablet, web, TV shelf and both player pickers draws
   the same labels on the same episodes.
3. A non-anime series and an anime with no AnimeFillerList entry draw no labels
   and no error.
4. With the backend lookup failing, the episode list renders as before.
5. Settings › About shows the credit line on TV and on the other layouts.
