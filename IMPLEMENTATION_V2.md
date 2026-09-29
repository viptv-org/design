# BE-002 / ADM-002 implementation ledger

This is an execution checklist, not a completion claim. User decisions are in
[BACKEND_V2.md](BACKEND_V2.md) and [ADMIN_V2.md](ADMIN_V2.md).

- [x] Approved decisions captured; production mutation excluded.
- [ ] Versioned public contracts and migration fixtures executable.
- [x] VOD 10k/100k baseline captured and bounded query implemented.
- [x] Independent engine extraction and container build.
- [ ] Gateway key scopes, jobs, viewer leases and safe media ingress.
- [ ] Backend HTTP gateway selection/affinity and encrypted secrets.
- [ ] Account-owned Xtream, default playlist and catalog paging.
- [ ] Advanced configuration export and reviewed migration tool.
- [ ] Local-only and embedded engine paths removed after cutover tests.
- [ ] Maximum-quality feature removed; actual device limits retained.
- [ ] Admin website rebuilt; VOD matching stays available and bounded.
- [ ] All client logic/contracts updated with unchanged viewing layouts.
- [ ] Cross-repository integration, browser/native checks and packages.
- [ ] Reviewed rollback/cutover instructions ready (no production execution).

## Foundation checkpoint — 2026-09-29

- `playback-gateway` exists locally with extracted engine, independent Rust
  contracts, hashed scoped credentials, logical viewer/job lifecycle and an
  isolated egress proxy. Network and lifecycle components pass unit fixtures;
  the public media service and backend integration are not implemented yet.
- Backend branch `refactor/backend-v2` contains tested account ownership/default
  and bounded VOD storage functions, not activated against a real database.
- Synthetic 100k-title VOD comparison: legacy materializes 100k rows / ~4 MB
  response; v2 materializes 51 rows / 50 returned items. Warm first-page median
  was 0.12 ms versus 145.66 ms in the local Python/SQLite harness. This is not
  a production end-to-end measurement. Backend docs record reproduction.

## Credential boundary checkpoint — 2026-09-29

- Gateway control has bootstrap-authenticated HTTP key issuance/list/revocation
  routes and per-viewer media capability validation. Rotation, lease expiry and
  key revocation deny subsequent authorization without waiting for cleanup.
- Shared-job failure transitions use safe public codes and retain quota
  reservations until worker teardown. Control tests: 15 passing; extracted
  engine default suite: 64 passing, 16 opt-in tests excluded from that count.
- Media routing and workers are still not connected; these checks do not prove
  end-to-end playback, shared upstream counts or readiness for deployment.
- Two opt-in tests additionally passed with installed FFmpeg/ffprobe: real
  remux/transcode/cleanup and rejection of nested local segments/AES keys. This
  is engine evidence only, not verification of the new gateway media routes.

## Engine boundary checkpoint — 2026-09-29

- Extracted gateway engine no longer hands upstream URLs/credentials to native
  clients; backend direct playback remains the product-owned decision.
- Removed remaining original-delivery dimension clamps, with declared-envelope
  4K/8K tests. Existing codec/decoder checks remain in place.
- Media subprocesses clear inherited proxy variables. A real FFmpeg/ffprobe
  fixture verifies explicit proxy use for root/redirect/segment/key requests and
  rejects raw TCP/TLS segment bypasses. Real remux/transcode/cleanup passes too.
- Default workspace suite: 65 engine tests and 15 control tests passing;
  17 opt-in tests are excluded from that default count. Certificate/hostname
  validation, media routing and actual worker sharing are still acceptance gaps.

## Worker integration checkpoint — 2026-09-29

- Engine preparation now returns its own normalized output plan before worker
  startup, with independent inspection/output capacity and drop-safe admission.
- The control worker bridge uses that plan directly, shares compatible workers,
  checks independent viewer credentials for media, and retains quota until
  cancellation/stop cleanup finishes. Reaping is serialized and bounded.
- Five-viewer/single-worker and cancelled-start fixtures pass with scripted
  processes. Default suite: 66 engine tests plus 17 control tests; 17 opt-in
  engine tests excluded. The real FFmpeg remux/transcode fixture also passes and
  verifies prepared-plan versus actual response mode/format consistency.
- Real single-upstream sharing, public session/media routes, service packaging,
  TLS acceptance and the remaining cross-repository cutover are still pending.

## Standalone service checkpoint — 2026-09-29

- Generic session/media HTTP API and standalone executable are implemented;
  control credentials and viewer media capabilities remain independent. Stable
  idempotent URLs, scoped reads, renewal/release and non-cacheable media pass
  route tests. Default suite: 86 tests passing; 20 opt-in fixtures excluded.
- Real plain-HTTP live source: five compatible viewers keep one active upstream
  connection; a separate namespace gets a distinct input. Viewer release does
  not stop the other viewers. This also passes with the container's FFmpeg.
- TLS fixtures accept trusted matching HTTPS media and reject untrusted/wrong-
  hostname certificates and untrusted HTTPS children of HTTP playlists. Native
  and container media binaries pass. HTTP provider inputs remain supported.
- Docker image built and reported healthy under UID 10001, read-only root,
  dropped capabilities and no-new-privileges. Native service TCP readiness,
  exclusive storage locking and graceful shutdown were checked.
- This does not complete gateway acceptance: pending inspection admission,
  detailed upstream errors, all-format network enforcement, multi-output input
  sharing and crash containment remain. Backend/client integration and the
  other unchecked items are still open. No production deployment occurred.

## Backend account-query and migration checkpoint — 2026-09-29

- Startup initializes additive v2 ownership/default/index tables without
  assigning legacy providers. Account-scoped matches GET/PUT and live-default
  GET/PUT routes are compiled into the backend. The existing web/viewing
  consumers have not yet cut over to these endpoints.
- Router tests verify bounded pages, account-bound cursors, protected edits,
  default persistence/fallback, no operator-role ownership bypass, and denial of
  management operations to paired devices or locked kids profiles.
- A separate provider-owners executable inspects read-only and requires explicit
  confirmation plus a complete owner map. SQLite online backup and a versioned,
  streamed private advanced-config export precede transactional assignment.
  WAL, identity/history/match preservation, rollback on invalid maps, duplicate
  owner rejection, non-overwrite and no credential output have fixture coverage.
- Full backend suite: 219 passed, two existing real-media fixtures ignored;
  strict all-target Clippy passed. Three stale assertions from the earlier
  playback-error change now check the existing human messages and stable codes.
- The migration tool currently handles export/ownership, not the entire future
  encrypted-credential and catalog cutover. Legacy routes/modules, source CRUD/
  discovery isolation, client adoption, gateway integration and final rollback
  qualification remain. No production migration, read or deployment occurred.

Initial audit: playback engine is a local crate; managed job sharing and provider
reservations still cross the backend boundary. Providers are server-wide while
add-ons already have account ownership. The VOD matches endpoint materializes
the candidate set before filtering; native direct playback bypasses sharing.
