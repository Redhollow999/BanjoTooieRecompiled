# Project A — Roadmap

This roadmap is ordered by technical value, not by hype value. The aim is to reduce unknowns in the order most likely to produce reusable knowledge.

## Priority 0 — Keep the research reproducible

Before expanding scope:

- Tie runtime claims to specific commits or clearly mark them local-only.
- Record hashes for non-distributable inputs/outputs.
- Preserve failed experiments and corrections.
- Keep the runtime adapter separable from conversion/research code.
- Avoid promoting semantic names until consumer behavior supports them.

## Priority 1 — Durable world-resource integration

### Goal
Replace experimental placement with a correctly sized, owned allocation and understood cache lifetime.

### Questions

- Which loader path should own an imported replacement?
- Can the native loader's caller-supplied destination path be used safely?
- What cache layers can bypass replacement on later visits?
- When should Project A state reset on map unload/reload?
- How should primary and secondary imported resources be freed or reused?

### Success criterion
Enter, leave, and re-enter a converted map repeatedly without stale pointers, capacity violations, or one-shot injection assumptions.

## Priority 2 — Gruntilda's Lair entrance room

### Goal
Load the fuller BK entrance-room geometry in BT while initially retaining BT's existing setup/state behavior.

### Required work

- Derive/validate native model bounds instead of using the Spiral Mountain constant template.
- Allocate for the larger BK primary model.
- Integrate BK's separate translucent model despite BT map `0x00AD` having no captured native secondary resource.
- Preserve native Cheato/setup/state at first.
- Test entry, exploration, exit, return, and repeated reload.

### Why this is high value
BT's native lair entrance shares substantial exact geometry with BK, making it an unusually controlled environment for comparing structures and consumers.

## Priority 3 — Setup / object placement architecture

### Goal
Move beyond static terrain.

Start with the simplest independently testable object type and determine:

- record layout,
- coordinate/orientation encoding,
- actor/object ID mapping,
- spawn ownership,
- persistence/state interaction,
- map-transition coupling.

A single correctly translated collectible or simple enemy is more valuable than importing many visually impressive but state-broken objects.

## Priority 4 — Effects, water, sky, and animation

Investigate the systems currently hidden behind model metadata and dedicated render paths:

- `+0x24` mesh/effect groups,
- animated vertices,
- animated textures,
- sky-related data/consumers,
- water/effect surfaces,
- camera-area data at `+0x20`.

Use live before/after memory captures to distinguish draw-list changes from vertex mutation.

## Priority 5 — Music runtime integration

The event/sequence side is already promising. Runtime integration should wait until ownership/cache handling is safer.

### Steps

- Reversible mode-gated sequence replacement.
- Audible playback verification.
- Repeated-loop verification.
- Program remapping only where note-level metadata evidence supports it.
- Separate waveform/sample identity work from sequence-format work.

## Priority 6 — Generalize conversion

Once more than one room/level works without hand-tuned constants:

- derive model-header fields algorithmically,
- formalize supported/unsupported feature detection,
- add fixtures using hashes/metadata rather than copyrighted assets,
- fail closed on unknown structures,
- separate conversion from runtime injection completely.

## Priority 7 — Broader level coverage

Only after the architecture above is stable should Project A scale to additional BK maps/worlds.

Candidate levels should be chosen for diagnostic value: different water, sky, effects, setup complexity, animated surfaces, and object density.

## Long-term outcome

The ideal end state is not merely “BK happens to run in this fork.” It is a documented compatibility layer and body of BK↔BT reverse-engineering knowledge that remains useful even if the current recomp backend changes.
