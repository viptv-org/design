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

## Encrypted gateway configuration checkpoint — 2026-09-29

- Backend gateway configuration is account-owned, with explicit additional
  grants and no implicit public/family default. Recipient and operator roles
  cannot edit another account's private connection.
- Integration keys are saved in authenticated encryption envelopes bound to
  owner/purpose/record/key ID. An operator-supplied keyring is required; missing,
  incorrect and retired keys fail closed rather than falling back to plaintext.
- HTTPS endpoint/key/scope checks precede persistence. DNS destinations are
  validated and pinned; redirects, inherited proxies and oversized responses
  are rejected. Concurrent checks are bounded and API responses are no-store.
- Backend default suite: 224 passed, three opt-in fixtures skipped; strict Clippy
  passed. The new executable interoperability fixture separately passed against
  the independent gateway. Its capability API now reports operation scopes;
  the gateway default suite remains at 86 passing tests.
- This does not complete gateway playback selection/affinity/session forwarding,
  provider/addon credential migration, private-network operator policy, bulk
  re-encryption or legacy playback removal. No production secrets were provisioned
  and no deployment occurred.

## Backend playback forwarding checkpoint — 2026-09-29

- /api/v2/playback now owns scoped asynchronous startup, status, heartbeat and
  release. It consumes only backend-issued source IDs, rechecks source ownership/
  configuration and returns direct or gateway delivery without backend media relay.
- Roku/Vizio cannot bypass required gateway delivery. Other eligible native
  clients can use direct delivery. Account-authorized active affinity precedes
  healthy priority/capacity selection; the gateway reports per-key capacity hints.
- Tests cover source changes, no private/family fallback, explicit grant
  revocation, independent viewer release, stale/foreign media URL rejection,
  actionable failures, idempotency and release of a late viewer after cancellation.
- Backend default suite: 230 passed, four opt-in fixtures skipped; strict Clippy
  passed. Gateway default suite remains 86 passing. An isolated network-none
  container fixture passed real FFmpeg HLS playback, renewal and revocation via
  the backend and independent gateway while the backend engine stayed idle.
- A fresh gateway image f215fa924b8f was built for that fixture. It is not deployed.
  Clients still use legacy paths; account-owned discovery/catalogs, provider/addon
  encryption, preference/transport parity, restart/stress qualification, gateway
  multi-output accounting and removal of legacy modules remain unfinished.

## Account live-catalog paging checkpoint — 2026-09-29

- Backend `e4cae75` adds account-scoped v2 live channel/category pages, using the
  persisted default or an explicit per-request catalog override. Unowned,
  disabled and absent catalogs do not fall back to another account's provider.
- Additive snapshot storage preserves provider stream/category order and logos,
  including HTTP logos. Catalog replacement and generation changes are atomic;
  failed refreshes retain the previous snapshot. Historical rows use insertion
  order until refresh because their original category order was not stored.
- Pages return at most 200 items (default 50), without a full count. Tokens bind
  account, filters, route, resolved catalog and generation; refresh/default
  changes require a restart instead of silently mixing snapshots.
- Full backend suite: 235 passed, four opt-in fixtures skipped; strict all-target
  Clippy passed. Fixtures cover complete 235-channel traversal, tenant isolation,
  defaults/overrides, original logos, bounds, snapshot invalidation and rollback.
- Paired devices can browse with a selected profile; restricted profiles still
  require parent unlock for raw catalogs. Child-policy migration, source/guide
  integration, owned connection CRUD/encryption, multi-provider VOD discovery and
  client adoption remain open. This does not complete the Xtream checklist item.
  No production database, provider subscription or deployment was used.

## Owned IPTV discovery checkpoint — 2026-09-29

- Backend `228b244` adds v2 incremental source-discovery start/poll routes and
  owned raw-channel Xtream guide reads. Candidate SQL filters account ownership;
  all enabled owned providers participate independently of the live default.
- Ownership and credential freshness are checked before queued detail requests,
  with ownership checks on cache access, enrichment and late publication. Polls
  redact a revoked provider's cached event without changing sequence positions.
  Raw scoped live reads bypass retired family-lineup mappings.
- Full backend suite: 239 passed, four opt-in fixtures skipped; strict all-target
  Clippy passed. The live-source fixture was additionally expanded and passed.
  Synthetic HTTP fixtures verify three-provider movie/exact-episode resolution,
  no requests to foreign/unassigned providers, cross-account job denial, sparse
  limits, revocation during fetch, cached-result redaction and owned guide reads.
- Source cards contain opaque backend IDs rather than provider credentials;
  internal HTTP live/episode URLs are preserved. No production provider was used.
  V2 currently uses polling, and restricted profiles require parent unlock.
- Connection CRUD/encryption, child-policy migration, detailed upstream errors,
  client cutover and legacy route removal are still incomplete. Existing legacy
  global discovery is not claimed to have the v2 isolation guarantees. No deploy
  or production migration occurred; the full Xtream checklist remains open.

## Provider credential migration checkpoint — 2026-09-29

- Backend `423484d` adds an encrypted Xtream tuple reader and an explicit offline
  `provider-owners encrypt` command. The operator keyring seals URL/username/
  password with account/provider/purpose binding. An explicit format marker
  prevents a missing ciphertext record from becoming a plaintext fallback.
- Private SQLite backup and advanced export are durable before transactional
  encryption. Source identities/history/manual matches remain; credential-bearing
  detail caches are invalidated. WAL checkpoint/compaction runs after commit;
  cleanup failure explicitly reports that encryption has already committed.
- Full backend suite: 242 passed, four opt-in fixtures skipped; strict Clippy
  passed. Final focused encryption fixtures also passed. Evidence covers rollback
  after a later invalid provider, preserved backups/history, no fixture plaintext
  in compacted DB/WAL, key/owner failures, restart schema/reader behavior, HTTP
  identity preservation, direct admission and CLI confirmation/keyring gates.
- Legacy connection mutation/pool paths reject migrated providers. Migrated
  native admission no longer uses cross-provider pool policy. Legacy family
  matcher snapshot schema was updated to avoid regressing unmigrated providers.
- This is not production-approved: backups/exports still contain plaintext;
  external copies and storage remnants are not securely erased. New connection
  CRUD, addon encryption, bulk rotation, child policy, client adoption and retired
  module removal remain open. No production data was read, migrated or deployed.

## Xtream connection management checkpoint — 2026-09-29

- Backend `7ccfbde` adds account-owned connection create/list/patch/delete and
  password renewal. Login validation precedes encrypted persistence; password
  renewal compares the prior ciphertext and preserves catalog identity. Server/
  login identity changes require a separate connection rather than guessed remaps.
- Connection pages are bounded and account-cursor scoped. Default assignment and
  fallback are transactional, and duplicate detection is account-local. Legacy
  plaintext rows require reviewed migration before v2 mutation. New registration
  is capped at 64 owned connections; larger existing sets remain readable.
- Scoped/encrypted Xtream fetches support HTTP and HTTPS with public destination
  validation, fresh DNS pinning, bounded responses/timeouts and no redirects or
  inherited proxies. Explicit test-only loopback access is not a production
  private-network policy. Reported native connection limits do not manufacture
  a one-stream allowance when the provider omits that information.
- Encrypted connections also seal cached Xtream detail/EPG payloads, which can
  contain upstream credentials. Missing or invalid encrypted cache entries do
  not become plaintext fallbacks. Deletion removes idle admission bookkeeping
  while existing permits retain their lifetime until playback cleanup.
- Full backend suite: 247 passed, four opt-in fixtures skipped; strict Clippy
  passed. Final management fixtures also passed, covering defaults, duplicates,
  account/device isolation, secret redaction, rejected login/redirect/rate/size
  responses, in-flight account revocation, encrypted offline cache reads and
  deletion while a native permit exists. Fixtures use synthetic HTTP providers.
- Account-scoped background refresh/initial indexing, addon encryption, private
  network operator policy, child policy, detailed playback error parity and all
  client/admin cutover remain open. The Xtream checklist item is not complete.
  No production migration or deployment occurred.

Initial audit: playback engine is a local crate; managed job sharing and provider
reservations still cross the backend boundary. Providers are server-wide while
add-ons already have account ownership. The VOD matches endpoint materializes
the candidate set before filtering; native direct playback bypasses sharing.
