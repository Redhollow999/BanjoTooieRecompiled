# Project A — Public Sources and Upstream References

Project A builds on public reverse-engineering work rather than treating the current recompilation as the only source of truth. This page records the external repositories that are especially useful when validating BK↔BT structural hypotheses.

## Banjo-Kazooie decompilation

**Repository:** https://github.com/n64decomp/banjo-kazooie

The mature BK decompilation is the highest-confidence semantic reference currently used by Project A. It is especially valuable because many model, collision, map, texture, rendering, and animation structures already have stable names and source-level consumers.

High-value files include:

- `include/core2/model.h`
  - `BKModelBin` model header
  - `BKVertexList`
  - `BKCollisionGeometry`
  - `BKCollisionTriangle`
  - `BKCollisionList`
  - camera-area, mesh, animated-vertex, and animated-texture structures
- `src/core2/modelRender.c`
  - geometry-command consumers and rendering behavior
- `src/core2/mapModel.c`
  - per-map opaque/translucent level-model selection, map-model loading, and collision-facing map-model logic

Important rule: BK names are a guide for Tooie, not automatic proof that Tooie kept identical semantics.

## Banjo-Tooie decompilation

**Repository:** https://github.com/Mr-Wiseguy/banjo-tooie

This is a WIP Tooie decompilation and is less semantically mature than the BK project, but it is an important direct source for BT addresses, overlays, symbol work, and emerging source matches.

Particularly useful repository artifacts include:

- `symbol_addrs.us.txt`
- `syscall_symbol_addrs.us.txt`
- `ovl_symbol_addrs.us.txt`
- `reloc_addrs.us.txt`
- `ovl_reloc_addrs.us.txt`
- `baserom.us.yaml`

When BT names are provisional or unmatched, Project A should say so explicitly rather than presenting a BK-derived name as native BT terminology.

## Banjo: Recompiled

**Repository:** https://github.com/BanjoRecomp/BanjoRecomp

This project is a useful public reference for how Banjo-Kazooie is handled through N64: Recompiled/RT64. It is not treated as evidence that a Tooie structure is identical, but it can provide valuable context for runtime behavior, graphics handling, and recomp-facing integration patterns.

Project A's AI-assistance policy differs from Banjo: Recompiled's project policy; that difference does not reduce the technical value of its public source as a reference.

## Banjo-Tooie recompilation used by Project A

Project A currently lives in the `project-a` branch of this Banjo-Tooie recompilation fork. Runtime hook points, generated C bodies, loader behavior, and diagnostic instrumentation from this codebase are direct evidence about the current backend.

Because the recomp backend may change, claims should separate:

1. game-format / game-logic findings that should survive backend changes, from
2. runtime-adapter details that are specific to the current recomp architecture.

## N64: Recompiled

**Repository:** https://github.com/N64Recomp/N64Recomp

Useful for understanding the generated-code environment, guest-memory conventions, patches/hooks, and assumptions introduced by static recompilation rather than by Banjo-Tooie itself.

## RT64

**Repository:** https://github.com/rt64/rt64

Useful when Project A needs to distinguish original N64 display-list/model behavior from rendering-backend behavior.

## Source hierarchy used by Project A

When sources disagree or naming maturity differs, prefer evidence in roughly this order:

1. Direct BT runtime behavior / bytes / consumer code.
2. Matched or clearly traced BT decomp source.
3. BT symbol/relocation material and generated recomp code.
4. Mature BK source when a structural analogue is independently observed in BT.
5. Historical converters/tools/community findings, after independent validation.
6. AI or human hypothesis alone — never sufficient as evidence.

## Citation discipline for future findings

A public finding should ideally name the exact upstream repository path and, when stability matters, the commit used during the investigation.

For example:

```text
BK reference:
  n64decomp/banjo-kazooie
  include/core2/model.h
  BKCollisionList / BKCollisionTriangle

BT evidence:
  local/generated consumer function(s)
  runtime capture / exact offset behavior

Interpretation:
  Strongly supported structural analogue; BT semantic names still provisional
```

This makes it possible for another researcher to distinguish what Project A observed directly from what it borrowed as terminology or architectural guidance.
