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
