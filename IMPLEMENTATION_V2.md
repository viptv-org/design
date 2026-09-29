# BE-002 / ADM-002 implementation ledger

This is an execution checklist, not a completion claim. User decisions are in
[BACKEND_V2.md](BACKEND_V2.md) and [ADMIN_V2.md](ADMIN_V2.md).

- [x] Approved decisions captured; production mutation excluded.
- [ ] Versioned public contracts and migration fixtures executable.
- [ ] VOD 10k/100k baseline captured and bounded query implemented.
- [ ] Independent engine extraction and container build.
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

Initial audit: playback engine is a local crate; managed job sharing and provider
reservations still cross the backend boundary. Providers are server-wide while
add-ons already have account ownership. The VOD matches endpoint materializes
the candidate set before filtering; native direct playback bypasses sharing.
