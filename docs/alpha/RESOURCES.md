# Resource provenance and local generation

The manifest records hashes and paths, not the content. Fixed runtime references
are only a subset: dynamic audition paths, diagnostics, mode files, optional
features, launcher assets and native ROM-backed assets require separate handling.

| Resource family | Current private dependency | Required public workflow |
| --- | --- | --- |
| BK terrain, lobbies, Skull, props and animations | Converted model/animation binaries and construction ZIPs | Extract exact BK asset IDs from a supported local ROM; convert with the reviewed static/model converter; apply recorded terrain, water-state, doorway and rubble edits; verify each final hash. |
| CC/BGS/GV/FFP | `bk-*-construction.zip` inputs to `prepare_worlds.py` | Replace private ZIP prerequisites with ROM extraction; preserve source asset IDs, opaque/XLU conversion, setup metadata and final patch recipes. The current preparation script alone is insufficient. |
| BK/native music | Extracted sequence binaries and BT bank/descriptors | Publish extraction and header-conversion tools only. Generate bank/sequence data locally; preserve track programs, channel masks and cue timings. |
| Extended trumpet/string ranges | Sample/descriptor arrays in `trumpet_resources.inc`, `score_range_resources.inc`, `v2_high_resources.inc` | Extract native BT samples/descriptors locally; run the existing antialias/ADPCM/range preparation with pinned tools; generate ignored includes; test pitch and native cache lifetimes. |
| Other embedded audio | Steelpan, seagull and Ticker waves embedded in `lair_two_way_runtime.inc`; `thunder_assets.inc` | Separate algorithms and metadata from payloads; locally extract/generate wave and descriptor includes. C text containing sample bytes is still content. |
| Ugger/Grey/Ticker portraits and logo/page/honeycomb models | Derived sprite/texture/model binaries | Generate from locally extracted assets plus reviewed original edit instructions. A PNG or model preview does not establish redistribution rights. |
| Authored Cheato/boss music and dialogue | Owner MIDI, arrangements, dialogue and concept notes | Obtain explicit contribution/licensing permission for the authored material; generate sequence data from licensed source. SoundFont/DLS instrument samples require their own provenance and must not be bundled with a composition merely because the MIDI is original. |
| Launcher fonts, icons, wallpaper and dependencies | Assets already present in public history; unlicensed/unclear notices were documented by the base port | Inventory exact licenses and attribution, replace unclear items if necessary, and resolve RecompFrontend's missing license before release. Do not assume public availability grants permission. |

## Existing tools to promote after review

The private tree already contains ROM-reading/model-conversion tools such as
`tools/project_a_bk_model_probe.py`, `project_a_bk_to_bt_model.py`,
`project_a_prepare_batch1_cc_bgs.py`, `project_a_extract_bk_music.py`,
`project_a_extract_bt_music.py`, `project_a_convert_bk_music.py`,
`project_a_build_trumpet_zones.py`, and `project_a_build_score_ranges.py`.
These are a starting point, not a completed installation command.

For example, the existing BK music extractor accepts `--rom <local-ROM>` and
`--out <ignored-output-directory>` and validates the supported ROM hash. The model
probe accepts a local ROM and selected `--assets` with `--out-dir`. Outputs must
remain local. The combined world preparation still reads private ZIPs, so running
one of these tools does not reproduce all patched world resources.

Each promoted recipe must declare input ROM/version/asset IDs, algorithm and
parameters, original authored inputs with permission, Python/native tool versions,
output paths and hashes. Reject unsupported input or output drift before replacing
accepted files. Run generators in a separate staging directory; compare first,
then copy verified results into a contributor checkout.

Until those recipes exist and reproduce the verified manifest in a clean checkout,
the full gameplay sync remains blocked. Hash verification cannot replace rights
review. Existing public history is outside the protection of a new `.gitignore`;
any actual credential finding would require revocation and a separately approved
response, not an unrequested history rewrite.
