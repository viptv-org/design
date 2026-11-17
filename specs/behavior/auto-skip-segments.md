# PLAY-AUTO-SKIP-001 — Skip intros, recaps and credits automatically

Status: **proposed**, owner request ([app#1150](https://github.com/viptv-org/app/issues/1150)).
The KMP app (phone, tablet, desktop, web and TV) implements it. The settings
are the profile preferences `skip_intros` and `skip_credits`; a profile saved
before `skip_credits` existed reads with both on.

## Intent

A marked intro, recap or credits segment skips itself when playback runs into
it, and plays when the viewer goes into it on purpose. Segments come from the
playback's segment markers (AniSkip and the other sources the backend reads:
`GET /api/playback/:id/segments`, kinds `intro`, `recap`, `credits`). An
outro (AniSkip `ed` or `mixed-ed`, other sources' `outro`) is a `credits`
segment. A segment marked `mixed` (AniSkip `mixed-op`, `mixed-ed`) has story
over it: it shows its **Skip intro** or **Skip credits** prompt but never
skips itself.

## Settings

Settings › Playback, saved with the profile like the other playback rows:

| Row | Description | Default |
|---|---|---|
| `Skip intros and recaps automatically` | `Skips them when you play into them. Seek into one to watch it.` | on |
| `Skip credits and outros automatically` | `Jumps to any scene after them. At the end of an episode, Up next takes over.` | on |

Phone and tablet show them as switch rows in the Playback group, desktop and
web on the preferences page, TV in the Playback list. A change saves at once.

## When a segment skips

A segment skips when **all** of these hold:

- its kind's setting is on and it is not marked `mixed`;
- playback is running, not paused, and no seek is in flight;
- the position is inside the segment;
- the playback **ran into it**: the position where the current stretch of
  uninterrupted playback began is before the segment's start, or is the
  segment's start on a fresh open (an episode opened at 0 with an intro at 0);
- the viewer has not undone a skip of this segment in this playback.

A stretch of playback begins where the player opened or where the last seek
landed. So:

| Viewer does | Segment |
|---|---|
| Plays on from before the intro | skips |
| Opens a fresh episode whose intro starts at 0 (including Up next) | skips |
| Drags or taps the timeline, uses −10 / +10, a D-pad scrub or the media keys, and lands inside it | plays |
| Seeks to before it and plays on | skips when playback reaches it |
| Resumes inside it, or chooses **Watch from the beginning** | plays |
| Presses **Undo** | plays, and does not skip again this playback |

Markers that arrive after playback started follow the same rule: playback
that ran from before the segment skips it when the markers arrive.

**Credits.** Credits that end more than 10 s before the media's end (a
post-credits scene or a next-episode preview follows) skip like an intro:
playback jumps to the segment's end and plays on, and Up next opens when the
media ends. Credits that run to the end, end within 10 s of it, or play in
media of unknown length are the end of the title: when a next episode is
known, reaching them opens the Up next panel as today
([next-episode-autoplay.md](next-episode-autoplay.md)) and nothing skips;
without one (a movie, a finale), playback jumps to the segment's end.

With a setting off, its segments only show the **Skip intro**, **Skip recap**
or **Skip credits** prompt, as today. The prompt also shows while a segment
plays on purpose.

## Skipped notice

After an automatic skip, a notice takes the skip prompt's place for 5 s:
`Skipped intro` (`Skipped recap`, `Skipped credits`) and **Undo**.

- **Phone, tablet, desktop, web:** a 44 high bar at the bottom end, 24 from
  the end, in the skip prompt's place: 12 above the timeline and at least 104
  from the bottom, so it never covers the timeline or its times, radius 12,
  `color.surface.2`, 16 horizontal padding: the label in 14 semibold primary
  text, a 12 gap, then **Undo** as a 14 bold accent text button. It shows
  whether the controls are shown or not, and over nothing else: a panel, the
  lock, the track sheet or a failure hides it.
- **TV:** the skip prompt's 72 tall slot at the bottom right (96 from the
  right, 112 from the bottom): the label on glass in 26 bold, then **Undo** as
  a 72 tall primary action. While the controls are hidden **Undo** takes focus;
  Back dismisses the notice. Showing the controls hides it.
- **Undo** seeks to the segment's start, which plays it, and the segment
  never skips again in this playback. The notice closes.
- A new automatic skip replaces the notice. It never pauses or reveals the
  controls.

## Acceptance

1. Setting on, playback from 0:30 runs into an intro at 1:00–2:30: the player
   seeks to 2:30 and shows `Skipped intro` · **Undo**.
2. Setting on, the viewer seeks to 1:10: the intro plays to its end; the
   **Skip intro** prompt shows.
3. Setting on, the episode resumes at 1:40: the intro plays.
4. After an automatic skip, **Undo** seeks to 1:00 and the intro plays; a
   later seek to 0:30 and natural playback into it does not skip it again.
5. Setting off: nothing skips; the **Skip intro** prompt shows.
6. A fresh episode with an intro at 0:00–1:30 starts at 1:30.
7. Credits at 21:30–22:55 in a 23:00 episode with a next episode: Up next
   opens; nothing skips.
8. Credits at 20:00–21:30 in a 23:00 episode, setting on: the player seeks to
   21:30, shows `Skipped credits` · **Undo** and plays the scene after them;
   Up next opens when the media ends.
9. The same credits with the setting off: Up next opens at 20:00 when a next
   episode is known; otherwise the **Skip credits** prompt shows.
10. A `mixed` intro at 1:00–2:30, setting on, playback from 0:30: the intro
    plays and the **Skip intro** prompt shows.
