# Design changes

## Initial extraction — 2026-09-12
Captured the Roku baseline at vynxc/viptv@7d6b413 and established design-first cross-platform governance. This changes repository ownership, not Roku behavior. Android-only imports and proposed platform adapters are tracked separately from current Roku behavior.

## Baseline precision audit
Added exact dynamic guide geometry, search debounce/focus/partial-failure behavior and server-owned queue completion/cache rules. These clarify existing behavior without changing it. Source citations use the published split runtime snapshots.
