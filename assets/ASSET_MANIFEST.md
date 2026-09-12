# Roku visual asset manifest

These are copied source assets for VIPTV design implementation, not screenshots or exported reference images. They are pinned to [source commit `7d6b413`](https://github.com/vynxc/viptv/tree/7d6b4131a44d87b58edcf12709af5851da387176/roku) (`2026-09-12T02:19:07Z`). The contents are preserved under `roku/` so every source path maps directly to its former Roku package path.

| Design path | Original source path | Git tree/blob hash | Contents |
| --- | --- | --- | --- |
| `roku/images/` | `roku/images/` | `3756ea28e0a3ff37417c2219b93e644c2e9100e4` | 682 tracked PNG/JPEG assets, including V branding, generated chrome, player/rail icons, masks, backgrounds and 624 avatar thumbnails |
| `roku/tools/` | `roku/tools/` | `33ecbe2f0bdfe2a1010830f260db5e01d13f7029` | Six baseline generators/fetchers; three design-local dependency/path adaptations are documented below |
| `roku/data/` | `roku/data/` | `0fdfc8710d01d8f7d2f47345bbb410e6b4e11493` | Avatar catalog/character provenance plus BSLib and Jellyfin notices/licenses |
| `roku/data/avatar-catalog.json` | same | `b9947e448173170e7f15464c7ad0ba94f4c5eb5d` | DiceBear collection metadata |
| `roku/data/character-avatars.json` | same | `2a49c86f10f067ad66e00404ae62cf2d0378b8bd` | Character names, sources and stable selection indices |

The Git object hashes above permit exact baseline verification. For byte-level verification, define checkout locations explicitly; `images` and `data` are byte-identical baseline copies. The three documented generator adaptations intentionally make a whole-directory `tools` diff nonzero.

```text
SOURCE_ROKU=/absolute/path/to/viptv-org/roku/roku
DESIGN_REPO=/absolute/path/to/viptv-org/design
git diff --no-index -- "$SOURCE_ROKU/images" "$DESIGN_REPO/assets/roku/roku/images"
git diff --no-index -- "$SOURCE_ROKU/data" "$DESIGN_REPO/assets/roku/roku/data"
```

## Critical byte checksums (SHA-256)

| Source and design-relative path | SHA-256 |
| --- | --- |
| `roku/images/viptv-mark.png` | `2911d72cee27925cb5b483da60a2222b5590fb048bb27928e00f568d55c82866` |
| `roku/images/viptv-wordmark.png` | `4d6d473c5ba0f9ab6cf7b26a36f8fa85da3abeb543817480a2af6512b47c8f7b` |
| `roku/images/splash-hd.jpg` | `8f764cc0bbc94499b35401c7e0b4285cf9e0671c83c8a56e30609c71d12a8f79` |
| `roku/images/channel-poster-hd.jpg` | `6092f7b9f9a2231b464475816f2efa1f207a8148607d91980b8f951251487477` |
| `roku/images/ui-hero-left.png` | `7a6ad9f8393f641649cb95ede5ce65f2ef69b0d21ee3feb1f79cea842f3756b0` |
| `roku/images/ui-hero-bottom.png` | `06ab2bc1a544e96342148dcb81e1db372163837134fdb217a89c6a530690effb` |
| `roku/images/ui-round-fill.9.png` | `8db709544a064090d64a10b7539ab33e847399712ab0ab55235bb0848a28d60d` |
| `roku/images/ui-round-outline.9.png` | `7cfd78d2371f762ad836febfd8ca1b219d49ea17ad971eeded7b8e2395cc34da` |
| `roku/images/ui-card-focus.png` | `594b1a4f08500cdb0688c2540c7a51c59f6d72f8b6dec0c11eb4fe524b83c585` |
| `roku/images/ui-progress-pill.9.png` | `dbbf9622ff70091c48b4768f74439690bb8029955b3ffd01ec6dcf93ded37e7e` |
| `roku/data/avatar-catalog.json` | `3cdbaa04d6facde49bdd4551d737662bb900816e816a88f24da5e6441ad4a41e` |
| `roku/data/character-avatars.json` | `1a0d91c4b7c669d37b86ec40a4fb8bcaf89e6a3c285865d0052f8cb1886bbc50` |

## Provenance and reuse rules

- `viptv-mark.png`, `viptv-wordmark.png`, `splash-hd.jpg`, and `channel-poster-hd.jpg` are VIPTV branding assets. The checked-in wordmark is the master; [branding instructions](../docs/branding.md) explain reproducible regeneration. Preserve the visual mark and monochrome identity across clients.
- `assets/roku/package.json` pins Node 22-compatible Sharp 0.34.3 and DiceBear 10.6.0. The design copies of `make_brand_assets.cjs`, `make_avatar_catalog.mjs`, and `fetch_character_avatars.py` use that local package layout and only update design-owned Roku assets; their baseline source paths/hashes remain in the table above. `make_theme_assets.py` regenerates neutral nine-patches, masks, hero gradients, spinner, progress pill and rail/player icons. `generate_player_assets.py` is an earlier player-asset generator retained for provenance. Modify a generator and regenerate assets together; do not hand-edit a derived raster without documenting why.
- `avatar-catalog/` contains 576 DiceBear 10.6.0 images (12 styles × 48 deterministic choices), CC0. `avatar-catalog/README.md` includes the generation package versions, seed contract and DiceBear/CC0 links. Show at most 18 at once and never reorder persisted choices.
- `avatar-characters/` contains 48 curated Disney-related thumbnails. Rights remain with respective rights holders; provenance is in `character-avatars.json` and `avatar-characters/README.md`. Keep the stable 1-based category positions; append only.
- `JELLYFIN-LICENSE.txt` and `JELLYFIN-NOTICE.txt` cover the GPLv2-derived Roku caption adaptation. `BSLIB-LICENSE.txt` is MIT for RokuCommunity BSLib 0.1.1. Keep notices and licenses with any copied/redistributed asset or client package where required.

No app should use this design repository as a runtime submodule. Consume a versioned asset release or copy only the required files at build time, keeping this repository as the provenance and visual-contract source of truth. Apps must not add screenshots to this tree.
