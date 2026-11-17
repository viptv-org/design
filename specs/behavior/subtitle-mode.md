# PLAY-SUBTITLE-MODE-001 — Subtitles: Always, Foreign audio only, Never

Status: **proposed**, owner requested 2026-10-11. Source revision: design
`4f3a1ea`; shared rule in core `b6ee054` (`subtitleSelection`,
preferences `subtitleMode`). Android adopts it first; TV-web, Roku and the
server-managed output path follow through their own pins. Implementation and
device evidence are recorded per platform.

## Intent

The profile's on/off **Subtitles** preference becomes a three-way choice so
viewers who prefer, say, English audio get subtitles automatically when a title
plays in another language (dual-audio anime played in Japanese, foreign films)
without turning them on for everything.

## Setting

Playback preferences row **Subtitles** opens the existing one-choice dialog:

| Label | Value | Behaviour |
|---|---|---|
| `Always` | `always` | Start with subtitles in the **Subtitle language**. |
| `Foreign audio only` | `foreign` | Start with subtitles only when the audio that plays is not the **Preferred audio** language. |
| `Never` | `never` | Start without subtitles. |

The row shows the chosen label. Saving shows the existing message **`Applies
to your next playback. Manual track choices take priority.`** Profiles that
stored only on/off read as `Always` (on) or `Never` (off).

## Decision

Core `subtitleSelection` decides from the facts a player reports once it knows
its tracks: the mode, preferred audio and subtitle languages, the selected
audio track's reported language and the subtitle tracks.

- Language matching accepts codes and names (`en`, `eng`, `en-US`, `English`).
  An empty preference means English, matching source ranking.
- `foreign`: audio is foreign only when its reported language is known and
  differs from the preferred audio. Missing, `und`, `mul` or `zxx` audio counts
  as not foreign, so subtitles stay off.
- The subtitle track is the first full-dialogue track in the subtitle language
  (or the only full-dialogue track when that preference is empty), preferring
  one the file marks default. If none matches, nothing is selected.
- A track is **signs-only**, never full dialogue, when the file flags it forced
  or its name mentions signs, songs or forced (`Signs & Songs`, `Signs/Songs`,
  `Forced`) without mentioning full or dialogue. Anime releases flag their
  signs track forced and default, and Media3 and mpv would otherwise pick it.
- `Always` uses the same choice: a full-dialogue embedded track in the
  subtitle language wins over the player's own default. A file whose only
  embedded track in that language is signs-only counts as having none, so a
  provider subtitle in that language is used when one exists; otherwise the
  signs track stays on.

## Playback behaviour (native/direct playback)

1. In `Foreign audio only`, playback starts with subtitles off. When the player
   reports its selected audio, the decision runs once and turns on the matching
   subtitle track if the audio is foreign.
2. Choosing another audio track in the player re-runs the decision (for
   example, switching a dual-audio title to Japanese turns English subtitles
   on; switching back to English turns them off).
3. Once the viewer picks a subtitle track or Off in the player, automatic
   choices stop for that playback. Seeking, retry and source-replacement keep
   the current tracks.
4. `Always` and `Never` keep their existing start behaviour.

Server-managed (converted) output and older clients only know on/off; for them
`Foreign audio only` behaves as **on** until they adopt this rule. This favours
readable foreign titles over hiding subtitles on native-language ones.

## KMP settings (owner decision 2026-10-22)

The KMP app adopts this mode on the shared engine preferences used by
`/api/profiles/:id/preferences`. The middle option's visible label names the
preferred audio language: `When audio isn't [language]`, with English when the
preference is **Original language** or empty (value `foreign`, behaviour
unchanged). The row lives on **Subtitles & audio** as **Subtitles**; the TV
Playback page no longer shows **Start with subtitles**.

TV **Subtitles & audio** is one vertical list, moved with Up/Down, in this
order: Audio language, Subtitles, Subtitle language, Subtitle size, Subtitle
background, Subtitle colour. Each row shows its value and opens the standard
one-choice dialog; Left goes to the sidebar; initial focus is the first row.
The live subtitle preview is a non-focusable panel beside the list. This
replaces the canvas board's horizontal choice rows for D-pad use; the canvas
needs the matching board.

## Storage

The profile stores `subtitle_mode` (`always` | `foreign` | `never`) with
`subtitles_enabled` kept equal to `subtitle_mode != never` for older clients.
A request without `subtitle_mode` derives it from `subtitles_enabled`. Until a
server stores the mode, a client may keep `foreign` on the device per profile
while the server's `subtitles_enabled` is on.

## Acceptance

1. **PLAY-SUBTITLE-MODE-01:** choose each option; the row shows its label,
   the message appears, and the choice survives an app restart and a profile
   switch back.
2. **PLAY-SUBTITLE-MODE-02:** `Foreign audio only` with English preferred:
   a dual-audio title playing English audio starts without subtitles; a title
   whose audio is Japanese starts with English subtitles.
3. **PLAY-SUBTITLE-MODE-03:** during playback switch audio English → Japanese
   → English; subtitles turn on, then off. After picking a subtitle track or
   Off manually, a further audio switch leaves it unchanged.
4. **PLAY-SUBTITLE-MODE-04:** audio without a language tag starts without
   subtitles; a title with no subtitle in the subtitle language shows none.
5. **PLAY-SUBTITLE-MODE-05:** `Always` and `Never` behave as before; an older
   client sees `Foreign audio only` as subtitles on.
6. **PLAY-SUBTITLE-MODE-06:** English subtitles preferred, a dual-audio anime
   file with English **Signs & Songs** (forced, default) then **Full
   Subtitles**: `Always`, and `Foreign audio only` with Japanese audio, start
   with **Full Subtitles** on Android and desktop. The viewer can still pick
   **Signs & Songs** in the panel.
