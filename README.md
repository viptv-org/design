# VIPTV v2 design

The current design contains 197 boards: TV 37, phone 53, tablet 11, desktop 40, web 30, Simkl 26.
`current/manifest.json` maps stable board IDs to exact HTML and screenshot references.
`current/html/assets` contains the supplied fonts and images. `current/design-tokens.json` describes shared tokens.
The earlier 206 explorations are absent from this experimental tree. Previous repository content remains in Git history.

Application architecture: Rust/Crux engine, KMP native and browser UI, SolidTV and Roku remote clients.
Native apps support local and remote connections; browser/TV-web/Roku require a backend.
Simkl authorization is server-side and linked per profile through the dashboard.
The desktop implementation is KMP rather than the Tauri host mentioned by the source kit.

The current board is the visual reference when a general note describes a different layout.
Implementation coverage is recorded by board ID, with provisional UI recorded in the application design-gap register.
