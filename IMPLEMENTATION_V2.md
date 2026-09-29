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

Initial audit: playback engine is a local crate; managed job sharing and provider
reservations still cross the backend boundary. Providers are server-wide while
add-ons already have account ownership. The VOD matches endpoint materializes
the candidate set before filtering; native direct playback bypasses sharing.
