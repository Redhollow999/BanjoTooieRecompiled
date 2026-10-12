# Project A — Banjo-Kazooie ↔ Banjo-Tooie Architecture Crosswalk

This crosswalk records structural correspondence useful for Tooie reverse engineering. BK names come from the mature public BK reverse-engineering/decompilation work; BT names remain conservative where Project A has not independently earned a semantic label.

## Confidence key

- **Observed** — directly seen in Project A BT code/data/runtime.
- **Strong** — BK and BT structures/behavior align closely, but exact semantic identity is not completely proven.
- **Provisional** — working interpretation only.

## Model/resource header

| Offset | Banjo-Kazooie interpretation | Banjo-Tooie / Project A | Confidence |
|---|---|---|---|
| `+0x04` | geometry/layout-related root | converter treats as geometry/layout root | Provisional outside tested converter |
| `+0x08` | texture-list/setup offset / adjacent type field | BT candidate uses repacked texture setup at `0x50` in current converter | Observed for tested conversion |
| `+0x0C` | display-list root | display-list-like root consumed by converter/runtime | Strong |
| `+0x10` | vertex-list offset | `section10`; 16-byte indexed records from `+0x18` | Strong |
| `+0x1C` | collision-list offset | `section1C`; 4-byte records then 12-byte records | Strong |
| `+0x20` | camera-area-list offset | `section20`; exact Tooie semantics still provisional | Provisional |
| `+0x24` | mesh/effect-related list | metadata capable of driving runtime vertex mutation in tested BT path | Strong behavior; exact name provisional |
| `+0x28` | animated-vertex data | corresponding root retained/relocated by converter | Provisional |
| `+0x2C` | animated-texture data | corresponding root retained/relocated by converter | Provisional |

## Vertex lists

### BK reference

BK vertex-list payload begins at header `+0x18` and contains N64 `Vtx` records of 16 bytes each.

### BT observation

Tooie `section10 + 0x18` is used as the base of 16-byte indexed records. Their first three signed halfwords are consumed as spatial XYZ-like values.

### Assessment

**Strong structural match.** Treat these as N64 vertex records for current analysis, while continuing to validate BT header-field semantics independently.

## Collision lists

### BK reference

`BKCollisionGeometry`:

```text
s16 start_tri_index
s16 tri_count
```

Size: 4 bytes.

`BKCollisionTriangle`:

```text
+0x00 s16 vertex_index[0]
+0x02 s16 vertex_index[1]
+0x04 s16 vertex_index[2]
+0x06 s16 extra
+0x08 s32 flags
```

Size: 12 bytes.

BK collision-list header places `geo_count` at `+0x10`, `tri_count` at `+0x14`, with payload beginning at `+0x18`.

### BT observation

Project A independently traced Tooie `section1C` and found:

- a meaningful field at `+0x10`,
- 4-byte-stride records,
- then 12-byte records,
- three 16-bit values at offsets `0/2/4`,
- an unresolved halfword at `+6`,
- 32-bit flags/mask data at `+8`,
- those first three values indexing the 16-byte records from `section10 + 0x18`.

### Assessment

**Very strong structural match.** This correspondence has already reduced anonymous Tooie collision analysis substantially. Exact BT field names should still be earned from BT consumers rather than copied wholesale from BK.

## Display lists / microcode

BK level models in the tested path contain F3DEX commands. Tooie expects F3DEX2-style command encodings.

The current converter translates the relevant command family, including vertex loads, display-list calls, triangle commands, geometry mode, texture/move-word operations, and end-of-list handling. The converter also rejects unsupported non-RDP opcodes rather than silently guessing.

### Known correction

Palette-related `SETOTHERMODE_H` handling required a targeted translation correction during the Spiral Mountain work. Display-list conversion should therefore remain opcode/encoding-aware rather than relying only on opcode-number substitution.

## Texture descriptors

The tested BK level-model path uses texture setup at `0x38` with 16-byte descriptors. The current BT candidate path repacks them into the compact form used by the tested Tooie model layout and relocates following roots.

### Assessment

**Observed for the Spiral Mountain proof-of-concept.** Do not yet present the converter's layout as the complete BT texture specification for every resource class.

## Mesh/effect vertex groups

BK and BT both expose model metadata through header `+0x24`, but direct compatibility is not established.

In the imported BK secondary Spiral Mountain candidate, copied `+0x24` metadata caused Tooie's runtime to mutate vertex positions, UVs, and colors while display commands stayed unchanged. Clearing the pointer stopped the tested corruption.

### Assessment

- Shared architectural concept: **Strong**.
- Byte-for-byte compatibility: **not established**.
- Exact UID/effect semantics: **provisional/unknown**.

## Map/resource selection

Tooie's `gcmapDll` searches 14-byte map configuration records that select primary and optional secondary resources. Whole-resource replacement of the selected primary changes the static world while retaining other map state.

This separation is important for Project A: model conversion can be studied independently from setup/actor/state systems.

## Gruntilda's Lair geometry overlap

Exact comparison between BK primary lair asset `0x14F3` and BT native lair asset `0x1CFD` found:

- 376 shared vertex positions.
- 743 shared unique collision triangles ignoring flags.
- 61.76% of BT's 1,203 unique collision triangles match BK exactly under that comparison.

### Assessment

**Observed data overlap.** This supports shared lineage/reuse of the room geometry, but does not imply setup, triggers, actors, doors, collision flags, or state machines are interchangeable.

## Compact music sequences

The games use different sequence-header layouts but share compatible event-level behavior in the tested readers.

### BK tested layout

```text
16 track offsets
then timing division
then sequence bodies
```

### BT tested layout

```text
u32 timing division
u32 track count
track offsets...
then sequence bodies
```

A narrow conversion that reorders/adds header information while leaving the BK body unchanged produced traces matching the original BK first pass when consumed by Tooie's generated C reader harness.

### Assessment

- Event-format relationship: **Strong/Observed for tested commands**.
- Header conversion: **Observed offline**.
- Runtime audio compatibility: **not established**.
- Instrument waveform equivalence: **not established**.

## Areas still needing a crosswalk

Highest-value remaining architecture comparisons:

- model-bounds fields and their consumers,
- sky resource/renderer data,
- water/effect metadata,
- animated vertices/textures,
- setup/object placement and actor records,
- map transitions/warps,
- camera-area data at `+0x20`,
- collision flag semantics,
- spatial partitioning used by enemy AI/detection.

When a new correspondence is added, record whether the BT side is **matched**, **inferred**, or **provisional**, and include the consumer/function evidence that justified the label.
