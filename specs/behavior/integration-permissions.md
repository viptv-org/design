# Own-account integration management

Identifier: ACCOUNT-INTEGRATIONS-01.
Status: proposed; owner-requested behavior, implementation qualification pending.

An account session can manage that account's add-ons and source connections
without having the server's global owner role. A separately registered account
does not inherit another account's installations, credentials, profiles or
playback-gateway grants.

This rule takes precedence over global-owner-only integration-write rules in
[account settings](account-and-profile-settings.md) and
[Live empty states](live-empty-state.md). Other administration rules are unchanged.

## Authority

`capabilities.manage_integrations` is an explicit server boolean, carried by
authenticated account identity. It authorizes account integration changes only
within the authenticated account, subject to the active profile's parent/PIN
restrictions. Account sessions with either the owner or member role can receive
it. Paired-device sessions cannot receive this account-management permission.
Unknown authority and failed permission reads do not grant it.

`manage_account` remains separate. Integration management never grants server
administration, role changes, other-account access, device-session administration,
or ownership of a playback gateway.

For older servers that omit `manage_integrations`, clients retain the existing
owner-plus-`manage_account` behavior only. They must not infer member permission.
An explicit false overrides that legacy fallback. Local-engine integration
management retains its existing local authority.

## Operations and presentation

The capability governs installation, removal, configuration, credentials and
refresh of the account's add-ons, VIPTV Sources and IPTV connections, including
owned IPTV metadata matches and the account's live-default selection. Every
mutation still checks the session, account ownership, current parent restriction
and resource revision on the server. Credential encryption and outbound-request
validation are unchanged.

Installed inventories remain readable through their existing authorized routes
even when account writes are unavailable. A failed inventory request displays
its error or retry state; it must not be represented as an empty installation.
“No add-ons installed.” is reserved for a successful, empty inventory response.

Profile-level activation is separate from account installation. Existing
owned-profile activation and parent/PIN checks remain in force, including any
already-supported paired-device toggles. Disabling account management must not
silently remove a valid profile toggle.

The existing settings pages, installation form, row menus, focus restoration,
loading indicators and cancellation behavior are retained across phone, tablet,
desktop and web. TV account-management refusals continue to direct the viewer
to an account session; no new remote hold or navigation behavior is introduced.

## Acceptance

- A normal member account installs and manages its own add-on and custom source
  while `manage_account` remains false and the global owner remains unchanged.
- An integration from another account cannot be read as owned, changed, enabled
  for an unrelated profile or removed by substituting its identifier.
- Paired devices cannot install, delete or change account connections; their
  authorized inventory reads and profile activation behavior remain intact.
- Locked kids profiles cannot use the capability to evade a parent/PIN gate.
- Members with the explicit capability see write controls; an explicit denial
  shows the existing read-only state. Missing capabilities do not promote members.
- An old server's authorized owner retains existing integration controls.
- An installed Cinemeta entry remains visible in read-only mode. A failed list
  request is distinct from a successfully empty list.
- Profile/session changes discard cached capability state before another
  account's controls or records can be used.

Hosted permission and client tests establish the software contract. Physical-TV
behavior and installed browser builds require their own delivery evidence.
