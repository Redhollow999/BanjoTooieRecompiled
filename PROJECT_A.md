# Project A — Banjo-Kazooie ↔ Banjo-Tooie Compatibility Research

Project A is an experimental reverse-engineering effort exploring how much of **Banjo-Kazooie** can be translated into structures understood by **Banjo-Tooie** and its recompilation runtime.

This is **not a finished mod** and is not presented as a production-ready merge of the two games. The current goal is narrower: document the shared architecture, build reproducible conversion tools, test hypotheses against the games, and leave behind useful technical work even if the runtime prototype changes or disappears.

## Current status — 2026-10-12

Verified experimental results include:

- Banjo-Kazooie's Spiral Mountain level models can be converted into Tooie-compatible candidates and rendered in Tooie's Spiral Mountain map.
- Imported terrain has demonstrated working collision, jumping, flight, water traversal, bridge/fence interaction, and at least one Tooie-only grip-grab on BK geometry.
- A secondary-model corruption issue was traced to incompatible copied mesh/effect metadata at model-header `+0x24`; disabling that metadata stopped the observed runtime vertex mutations and fixed the bridge/fence presentation in the tested candidate.
- Reload/return experiments have demonstrated re-entry to the imported Spiral Mountain environment in the working research build.
- BK and BT model/collision structures show a strong structural relationship, including the `+0x10` vertex-list-like section and `+0x1C` collision-list-like section.
- BK music sequences can be transformed into a BT-compatible header layout and parsed successfully by Tooie's generated C sequence reader in offline verification. Audible BK music playback in the game is **not yet established**.
- BK Gruntilda's Lair and BT's native lair entrance share substantial exact geometry: 376 shared vertex positions and 743 shared unique collision triangles in the current comparison.

The GitHub branch may lag some local/runtime experiments. Documentation therefore distinguishes **observed behavior** from **repository artifact status**. A claim being documented does not automatically mean the corresponding runtime patch is already committed on this branch.

## Documentation

- [Status](docs/project-a/STATUS.md) — quick snapshot of what works and what does not.
- [Roadmap](docs/project-a/ROADMAP.md) — highest-value next technical steps.
- [FAQ](docs/project-a/FAQ.md) — short answers for public/technical questions, including AI use and reproducibility.
- [Research log](docs/project-a/PROJECT_A_LOG.md) — chronological experiments, corrections, and milestones.
- [Current findings](docs/project-a/PROJECT_A_FINDINGS.md) — present best-supported architecture and results.
- [Reproduction guide](docs/project-a/PROJECT_A_REPRODUCTION.md) — how findings should be independently reproduced and recorded.
- [Unknowns and failed experiments](docs/project-a/PROJECT_A_UNKNOWNS.md) — unresolved questions, negative results, and unsafe assumptions.
- [BK ↔ BT architecture crosswalk](docs/project-a/BK_BT_CROSSWALK.md) — side-by-side structural correspondence and confidence levels.
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
6. `PROJECT_A_REPRODUCTION.md`
7. the chronological log/raw extracts only when you need the underlying trail

## Evidence policy

Project A uses three technical confidence levels:

1. **Observed** — directly demonstrated by code, data, or runtime behavior.
2. **Strongly supported** — multiple independent observations agree, but a semantic interpretation is not yet fully proven.
3. **Speculative** — plausible working hypothesis that still needs direct evidence.

Names are kept conservative until evidence earns a semantic label. Failed experiments are retained because they prevent future researchers from repeating dead ends.

## AI assistance

Project A is openly AI-assisted. AI is used for source analysis, hypothesis generation, code generation, experiment planning, and documentation.

**AI output is not treated as evidence.** A technical claim is promoted only when supported by reproducible static analysis, runtime probes, controlled experiments, hashes, source references, or independent implementation tests.

The intended standard is simple: another developer should be able to clone the repository, read the evidence, and understand or reproduce a claim without needing the original operator or the AI conversation that produced it.

## Legal / repository boundary

This repository does not distribute Banjo-Kazooie or Banjo-Tooie ROMs, extracted game assets, music, or other copyrighted game content. Tools operate on user-supplied legally obtained game data and should verify known inputs before extraction or conversion.

The public repository should contain the **recipe and research**, not Rare/Nintendo's game data.

## Runtime independence

Project A intentionally treats the current recompilation as a runtime backend rather than as the research itself. Conversion knowledge, structure documentation, and validation tools should remain useful even if upstream recomp internals, allocation, hooks, or APIs change.
