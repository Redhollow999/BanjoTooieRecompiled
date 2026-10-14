# Project A — Banjo-Kazooie ↔ Banjo-Tooie Compatibility Research

Project A is an experimental reverse-engineering effort exploring how much of **Banjo-Kazooie** can be translated into structures understood by **Banjo-Tooie** and its recompilation runtime.

This is **not a finished mod** and is not presented as a production-ready merge of the two games. The goal is to document the shared architecture, build reproducible conversion tools, test hypotheses against the games, and better understand how the two titles “communicate” across generations: which map, model, collision, animation, resource, actor, audio, and state systems remained evolutionary relatives and which require an explicit translation layer.

## Current status — 2026-10-14

Verified experimental results now include:

- Banjo-Kazooie's Spiral Mountain terrain running inside Tooie with collision, movement, flight, water traversal, bridge/fence interaction, and a tested Tooie grip-grab on BK geometry.
- Multiple connected BK Gruntilda's Lair rooms hosted inside Tooie's native lair scene, with native Tooie scene transitions, room-specific arrival handling, return routes, collision, and state-preserving reloads.
- Lair 3 secondary water terrain rendered and swimmable, plus a scoped native climb registration that restored the tested BK vine route.
- A stable Mumbo's Mountain exterior prototype with BK primary/secondary terrain, water/swimming, entry from the imported lair, and return to the lair through Tooie's native transition backend.
- The BK world-exit-pad model rendered inside the MM prototype after resolving load-order, cache-ownership, and stale-pointer problems. Native model-cache entries may relocate while still owned, so host-side draw code must resolve the current address by resource ID rather than retain a guest pointer.
- Live RT64 tracing shows deferred texture consumption can occur after a model resource has moved; in one captured run, texture reads still referenced the prior pad range after the native cache had relocated the model. This is a current renderer/lifetime research issue, not a finished root-cause claim.
- A narrower MM doorway trigger was user-confirmed to reject side approaches while retaining normal center entry.
- The first live imported BK Ticker has spawned/rendered in Tooie, briefly animated, collided with Banjo, and produced contact damage. Stable looping animation, hurt/death behavior, AI, and normal combat remain unfinished.
- The next Gruntilda's Lair route toward the Treasure Trove Cove lobby has been converted and integrated as another logical hosted room; broader world-door/setup behavior remains in progress.
- BK and BT model/collision structures continue to show strong structural correspondence, including vertex-list-like data at header `+0x10` and collision-list-like data at `+0x1C`.
- BK compact music sequences can be transformed into a BT-compatible header layout and parsed successfully by Tooie's generated sequence reader in offline verification. Audible BK music playback in-game is still not established.

## Important architecture note

Much of the current lair/world prototype uses Tooie's native map/scene machinery as a **host** while swapping or privately loading translated BK resources as logical rooms. This is why some native Tooie setup behavior, actors, title text, and scene presentation can remain visible in imported BK spaces. The long-term goal is not to leave every imported area as a remap of one native setup; setup/object/progression integration is a separate research layer.

The public branch may still lag the newest local/runtime experiment. Documentation distinguishes **observed behavior** from **repository artifact status**. A claim being documented does not automatically mean the corresponding runtime patch, owner-supplied asset, or current executable is committed here.

## Documentation

- [Status](docs/project-a/STATUS.md) — quick snapshot of what works and what does not.
- [Roadmap](docs/project-a/ROADMAP.md) — highest-value next technical steps.
- [FAQ](docs/project-a/FAQ.md) — short answers for public/technical questions, including AI use and reproducibility.
- [Research log](docs/project-a/PROJECT_A_LOG.md) — chronological experiments, corrections, and milestones.
- [Current findings](docs/project-a/PROJECT_A_FINDINGS.md) — present best-supported architecture and results.
- [Reproduction guide](docs/project-a/PROJECT_A_REPRODUCTION.md) — how findings should be independently reproduced and recorded.
- [Unknowns and failed experiments](docs/project-a/PROJECT_A_UNKNOWNS.md) — unresolved questions, negative results, and unsafe assumptions.
- [BK ↔ BT architecture crosswalk](docs/project-a/BK_BT_CROSSWALK.md) — side-by-side structural correspondence and confidence levels.
- [Runtime adapter audit](docs/project-a/RUNTIME_ADAPTER.md) — current prototype coupling, fragility, and target backend boundary.
- [Public sources and upstream references](docs/project-a/SOURCES.md) — external decomp/recomp material used to validate the work.
- [Contributing research](docs/project-a/CONTRIBUTING.md) — evidence and contribution standards.
- [Raw research material](research/project-a/README.md) — guide to the static-analysis extracts already in this branch.

## Quick start for technical readers

If you are here to audit the work rather than run the game, read in this order:

1. `STATUS.md`
2. `PROJECT_A_FINDINGS.md`
3. `BK_BT_CROSSWALK.md`
4. `SOURCES.md`
5. `PROJECT_A_UNKNOWNS.md`
6. `RUNTIME_ADAPTER.md`
7. `PROJECT_A_REPRODUCTION.md`
8. the chronological log/raw extracts only when you need the underlying trail

## Evidence policy

Project A uses three technical confidence levels:

1. **Observed** — directly demonstrated by code, data, or runtime behavior.
2. **Strongly supported** — multiple independent observations agree, but a semantic interpretation is not yet fully proven.
3. **Speculative** — plausible working hypothesis that still needs direct evidence.

Names are kept conservative until evidence earns a semantic label. Failed experiments and corrected assumptions are retained because they prevent future researchers from repeating dead ends.

## AI assistance

Project A is openly AI-assisted. AI is used for source analysis, hypothesis generation, code generation, experiment planning, debugging, and documentation.

**AI output is not treated as evidence.** A technical claim is promoted only when supported by reproducible static analysis, runtime probes, controlled experiments, hashes, source references, or independent implementation tests.

The intended standard is simple: another developer should be able to clone the repository, read the evidence, and understand or reproduce a claim without needing the original operator or the AI conversation that produced it.

## Legal / repository boundary

This repository does not distribute Banjo-Kazooie or Banjo-Tooie ROMs, extracted game assets, music, or other copyrighted game content. Tools operate on user-supplied legally obtained game data and should verify known inputs before extraction or conversion.

The public repository should contain the **recipe and research**, not Rare/Nintendo's game data.

## Runtime independence

Project A intentionally treats the current recompilation as a runtime backend rather than as the research itself. Conversion knowledge, structure documentation, and validation tools should remain useful even if upstream recomp internals, allocation, hooks, or APIs change.
