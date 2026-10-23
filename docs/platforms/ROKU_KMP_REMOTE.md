# ROK-REMOTE-001 — KMP TV presentation, remote authority

Status: owner-approved implementation, 2026-10-23. This contract supersedes the
legacy Roku rail, Home composition and client-owned playback selection for the
remote rebuild. The owner selected the current KMP TV working tree, rather than
the older canvas boards, as the visual reference.

The adopting Roku repository records the KMP commit, source hashes and private
reference archive hash in `docs/KMP_REFERENCE.json`. Those source bytes define
the reference: later edits by another agent do not silently change this target.
Existing KMP source is read-only during this adoption.

`assets/roku/roku/images/design/remote-entry.jpg` is the byte-identical KMP
`composeApp/src/commonMain/composeResources/files/entry/feature.jpg`, verified
against that reference ledger before import. The `remote-*.png` scrims/masks
come from `make_kmp_assets.py`, which records their KMP component provenance.

## Presentation and input

Use the KMP 1920×1080 TV coordinate system, Onest and Bricolage fonts, 96px side
safe area, fixed-size focus treatment, top navigation and profile menu. Scale
uniformly for 720p. Match the recorded TvNavigation, TvHome, TvDetails,
TvSources, TvSearch, TvLive, TvLibrary, TvHistory, TvCalendar, TvProfiles,
TvSettings and TvPlayer sources, including loading/error/empty variants.

One remote focus target is active. Left/Right traverse a row; Up/Down change
rows; boundaries return to navigation. Back dismisses the topmost overlay,
restores its opener, then returns to the prior route/card/scroll position.
Late responses must not move focus. Source drawers use the KMP 300ms entry and
200ms exit motion. Repeated input cannot submit duplicate mutations. Text input
uses the KMP TV keyboard layout; passwords are masked and cleared on dismissal.

Supported controls retain their labels and actions. Omit local mode, local
torrent controls, downloads, unsupported authentication and controls with no
real server/platform implementation. Do not copy KMP preview-only values or
unavailable placeholder actions. Empty configured capabilities remain usable
through their supported configuration flow, rather than inventing media.

## Authority

The server owns identity, permissions, catalogs, discovery, ordering, artwork
roles, source eligibility/ranking, resume, next episode and persistent settings.
Roku owns presentation, focus, animation, transient drafts, transport and the
native decoder. It sends observed capabilities and user intent; it does not
derive business rules from titles, source names, filenames or cached history.
Use the same current API as web-TV; its agent owns backend implementation.

## Acceptance

ROK-R01: bootstrap/profile changes never expose stale account content.
ROK-R02: server source order, target episode and resume decision survive unchanged.
ROK-R03: every supported screen covers entry/success/empty/failure/Back focus.
ROK-R04: unavailable features have no selectable dead-end controls.
ROK-R05: visible-window loading bounds nodes/images/tasks during long browsing.
ROK-R06: cancellation and refresh cannot resurrect retired playback sessions.
ROK-R07: inspect equivalent reference/renderer states at 1080p and 720p.
ROK-R08: record actual TCL 50S435 frame time, input latency and memory; 60fps
and p95 focus response below 100ms are targets, not unmeasured claims.

Functional, visual and physical-device acceptance are separate. App captures
stay private; durable evidence contains measurements and source references.

## Entry reconstruction corrections (2026-10-23)

Private captures of TvWelcome, TvSignInChoice and TvPairingSignIn exposed omitted
entry states in the initial Roku adoption. Entry starts at TvWelcome: the same
40 poster placements (-60 + column*252, -100 + row*372; 236x354; radius10), alpha
.32, with a 500px horizontal drift over 60 seconds reversing, and the same
elliptical scrim (.92/.75/.45 alpha at 0/.55/1). Center the 80px brand mark and
92px wordmark in the y336 band. Tagline at y474, 34/42 typography. A single
360x72 Sign in action is centered at [780,584]; omit the unsupported local action.

Sign in opens Choice. Heading [96,96], 56/64; options [96,250], 900x100, gap16,
radius16, 32px horizontal padding, 32px icons and 26px icon/text gap. Titles
30/36 bold; subtitles22/30 medium. Keep phone, browser and password in that order;
omit unsupported email/local options. Feature art [1120,250],704x396,radius18,
alpha.6, with the 64px brand mark/72px wordmark at the bottom-left32px inset.
Explanation [1120,668],704 wide,26/38. Lists retain fixed geometry under focus;
never use the native wrapping-list default for these choices.

Pairing retains the KMP heading and columns: left [96,250],760 wide with
30/43.5 heading,26/37.7 instruction and 340px white QR surface at y424. Right
[1064,250],760 wide with numbered44px instructions, address at x1126, code
surface [1126,534],640x120 and refresh/expiry row at y676. Divider x959,y250,
2x560 with60px 'or' circle. Waiting state at[96,900]. Omit unsupported email
switch. QR image remains server supplied; transport must support its current
origin and TLS requirements. Back cancels pairing ownership and returns to
Choice; Back from Choice returns to Welcome. No email placeholder dialog.

Capture these three states at 1080p and scaled720p, compare native TCL renders,
and report differences before claiming parity. Source: recorded KMP entry files
and private `kmp-entry-reference-20261023` captures; not screenshot assets.

## Settings row reconstruction

`TvSettingsRow` fixes rows at96px, corner14, background#191919 and focused
#F4F2EE, with28px horizontal padding. Labels are26/32 semibold; optional
server-provided descriptions are20/26 medium, separated by4px. Choice values
are24/30 medium at the right with an8px gap before a24px chevron. Boolean
controls use a68x38 pill and30px thumb with4px inset, accent on and#494949 off.
Use only choices supplied by the current preference contract. Selecting a boolean
row sends the other supplied boolean choice; focus does not mutate state and
accepted server responses own the displayed value. Non-boolean rows open their
server-supplied choices. Do not synthesize skip-intro, frame-rate or other absent
controls. Row pitch108px; content starts[640,220],width1184. Heading40/48 at
[640,93] with -.8 tracking; profile explanation24/30 at[640,152].

## Detail reconstruction corrections

TvDetailHero exposes Play/Resume, saved-title and (only for a server resume
intent) Restart. Do not add a separate Sources circle to that row. Movie actions
start[96,668]; series actions[96,648]. Logos fit their existing bounding box but
align to its left, using decoded bitmap dimensions rather than centering a
letterboxed Poster. Missing/failed art keeps the server title readable.

TvRecommendationShelf uses232x348 poster art,16px gaps,12px corners,3px focus
outline and no labels. Heading is `More Like This` at the existing y836 shelf
origin (poster top888). Episode cards are448px wide with252px landscape art,
24px gaps,12px corners and3px focus outline. Captions24/29 semibold, subtitles
20/26, descriptions20/28 up to2lines. Use the server's episode identity and
progress; never infer completion, episode order or a next episode locally.

## History and calendar reconstruction

History retains top navigation, a40/48 heading at[96,228],24/32 explanation,
and a260x64 Clear history action at[1564,236]. Rows start at y340 and are
1728x148,corner16,gap12, with232x124 landscape thumbnails at12px inset/radius10.
Text starts268px from the row origin: title28/34 semibold and subtitle22/28.
The right edge can display the server progress fraction as a percentage. Only
`completed_at_millis` marks completion. Preserve server order; do not deduplicate,
reorder, or manufacture day groups. Day headers require server presentation.
The empty state says `Nothing watched yet` / `Titles you play show up here.`
and offers `Browse Home`; clear remains unavailable with no entries.

Calendar's content rows are1100x132 at[96,250],gap18. Its preview uses landscape
art at[1240,250],584x329, then title32 at y598 and description24/32 at y656.
Use supplied landscape art, with the supplied poster as the KMP missing-landscape
fallback; never replace this preview with a300x450 portrait. Airing labels,
personal progress narrative and Watch target must come from the producer.

## Profile menu

The current KMP `DropdownMenu` capture is a compact popup anchored at[1768,94],
117px wide,8px vertical padding and48px rows. Its text is14px medium with12px
horizontal inset; surface#161618,4px corners, no full-screen scrim. Roku uses
this popup instead of a960px source-style drawer. Keep Switch profile and
Settings in KMP order. Append History as the required supported Roku route
(the KMP navigation popup currently has no entry to its History screen).
Back restores the avatar focus. Entry/exit use a120ms opacity transition.

## Platform launch artwork

Retire the old white-V launcher and splash artwork from the Roku package.
`make_remote_branding.py` uses the pinned Bricolage glyphs, current yellow mark,
-.04em wordmark tracking and KMP background. The1280x720 platform splash scales
TvSplash's88px mark/104px wordmark/22px gap and y492 center from1920x1080.
The runtime startup state uses the same brand, at y440 in its104px box, and a
240x4 progress track at[840,600] with96px indicator moving over1.2seconds.

## Remote library header

Use the current remote `LibraryHeader`, not the local preview controls. Header
origin[96,140],width1728,height64. Preserve the server type-control choice order
and labels. Type group has6px inset,32px outer radius,#212124 background; each
choice is140x52 when more than3 choices, otherwise168x52,26px radius,24px regular
Onest text. Accepted query type owns the selected #0B0B0C fill; focus uses
#F4F2EE and dark text. Filters stays at the far right,64px high,32px radius,
24px icon,12px gap,24px horizontal padding. Hide list picker for one source.
Type activation resets the server offset, retires the prior request and waits
for the accepted response. Up returns to navigation, Down enters the grid;
return from detail restores query and focus. Empty results keep controls usable.

## Server-projected metadata and resume

Consume `Card.view.metadata_parts` for detail and `hero_metadata_parts` for
Home; show `hero_badges` in supplied order. Do not sort, alias or deduplicate.
Metadata uses24px medium Onest,32px line box,12px gaps on each side of the dot.
Badges follow after28px,30px tall,18px bold text with .36px tracking,8px horizontal inset,
5px corners,1.5px white55% outline and12px gaps. Tile state comes from
`view.tile_badge`, never from raw capability tokens. Source rows consume
`source.view.title/body/quality_label/format_label/addon_label/provider_label`.
Resume button consumes viewing-action `remaining_label` and `progress` exactly;
remaining text26px bold follows the action label with54px gap. Progress is4px
high,28px horizontal inset,12px from the button bottom. No resume threshold or
remaining-time calculation belongs in the renderer. Library focus outlines are
4px outside the pill bounds, following KMP `tvFocusOutline`.

Tile `view.tile_badge.role=watched` renders the KMP34px circle/check at10px
inset from the upper-right; never infer watched from progress. A `new_episodes`
role renders the supplied label at[10,10],18px bold,22px line height,10x4px
padding,6px corners,light fill/dark ink. Other supplied tile labels use dark80%
fill and light ink. Compact captions and progress consume `view` fields without
raw metadata fallbacks. Episode subtitles remain the supplied episode subtitle.

## Password entry reconstruction

`TvPasswordPanel` has a24/34.8 eyebrow at[96,96] and52/60 bold heading
`Sign in with your password` at[96,140.8],tracking-1.04. Form origin[96,230],
width1130. Username and Password each have24/30 labels,10px gap,84px-high
fields with14px corners,28px horizontal inset,34/41 text. Active field has2px
light border; inactive1px white14% border; fill white8%. Fields are separated
by16px; keyboard begins at y540 after46px gap. Four ten-key rows are104x76
with10px gaps. Final row: Shift104,Symbols104,Space332,.com218,@gmail.com332,
10px gaps. Keys have10px corners,white9% fill (suffix18%),28px semibold text.
Focus uses the existing4px outer white outline. Initial focus is `q`.

Actions occupy[1290,270],width534,height72,gap16: Sign in, Show/Hide password,
then the explanatory text and Delete character / Use another server. Omit
Forgot password because the current server does not offer that authentication
flow. Retain its discoverable phone/browser alternatives on the choice screen.
The explanation keeps KMP copy. Password is masked initially; Show/Hide is a
transient renderer choice. Username max320, password max512, no persistence.
Selecting either field changes the editing target. Keyboard Up enters the
Password field; Up again enters Username. Right from the keyboard reaches the
actions; Left returns to the retained key. Back cancels login ownership, clears
both drafts and returns to choice. Errors preserve username, clear password,
and leave the form usable; retry requires a new password submission. Server
address edits preserve form drafts until accepted; acceptance clears credentials
and reopens the form against the new origin. Never synthesize authentication.

Native password verification: KMP heading ink begins at[99,149]. Roku's native
Label baseline requires the tracked heading group at y137.8 (3px above the
nominal line-box origin) to align that ink. Reopening the form resets the
keyboard to lowercase `q`, while field/action round trips retain the current
key. Keyboard-to-field/action transfer explicitly focuses the target Group;
focusing only the enclosing form leaves the previous child focused on the TCL.

## Browse filter page

`TvFiltersPage` replaces the catalog screen with#0B0B0C,96px top/side and54px
bottom padding. Heading52/60 bold,tracking-1.04,then catalog label24/32 and28px
gap. Left facet column640px wide;64px gap to the choice column at x800.
Facet rows80px high,12px gaps,14px corners,26px horizontal padding;26px bold
labels,22px selected value right aligned (max300px),18px Required indicator.
Unfocused active facet fill white16%,other facets white4%; focus light fill/dark
ink and4px outer ring. Choices preserve producer order in three-column rows,
14px horizontal/vertical gaps,minimum200px width,64px height,32px radius,
24px semibold labels and24px horizontal padding. Checked choices include a22px
check with12px gap. Only producer maximum_selections limits drafts. Single choice
replaces; multichoice toggles; no quality/provider policy is allowed.

Bottom actions at y954: Show results340x72,Clear all220x72,Cancel220x72,
16px gaps. Back/Cancel discard the entire draft and restore the trigger focus.
Show results retires old request ownership and submits the whole draft once.
Clear all clears the draft and selected catalog; it does not issue a request.
The current Library filter is a separate800px right sheet, not this full page.
Toggle choices must be supplied by the server; do not manufacture On/Off values.

Browse choices disabled by a full server maximum_selections cap are skipped by
remote focus. Removing a selected choice makes the remaining choices reachable
again. Entering a capped group focuses its first enabled choice; never leave the
remote focused on a disabled item.

Text/number/date controls with no choices use `TvFacetText`: value field at
[800,312],819.2x84,14px corners,28px inset,30px text; the inline entry keyboard
starts at[800,412],width1024,76px key height and10px gaps. Its four ten-key rows
use equal widths; the final suffix key uses the remaining row width. Drafts are
bounded to64 characters, matching the KMP input control. A200x64 Clear action
appears16px below the keyboard when nonempty. Text input remains on the filter
page; Back cancels the page, Left returns to facets, and Down reaches Clear or
the page actions. Submitting text never issues an independent catalog request.
