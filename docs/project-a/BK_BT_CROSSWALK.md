# Project A — Banjo-Kazooie ↔ Banjo-Tooie Architecture Crosswalk

This crosswalk records structural correspondence useful for Tooie reverse engineering. BK names come from the mature public BK reverse-engineering/decompilation work; BT names remain conservative where Project A has not independently earned a semantic label.

Public BK reference used heavily here: [`n64decomp/banjo-kazooie`](https://github.com/n64decomp/banjo-kazooie), especially [`include/core2/model.h`](https://github.com/n64decomp/banjo-kazooie/blob/master/include/core2/model.h) and [`src/core2/mapModel.c`](https://github.com/n64decomp/banjo-kazooie/blob/master/src/core2/mapModel.c).

## Confidence key

- **Observed** — directly seen in Project A BT code/data/runtime.
- **Strong** — BK and BT structures/behavior align closely, but exact semantic identity is not completely proven.
- **Provisional** — working interpretation only.

## Model/resource header

The BK decompilation names the following `BKModelBin` fields directly. Project A uses those names as a comparison target, not as automatic BT names.

| Offset | Banjo-Kazooie interpretation | Banjo-Tooie / Project A | Confidence |
|---|---|---|---|
| `+0x00` | model magic | tested BT model resources use compatible model-root handling | Provisional outside tested resources |
| `+0x04` | geometry-command list offset | converter treats as geometry/layout root | Provisional outside tested converter |
| `+0x08` | texture-list offset; adjacent `+0x0A` geo type | BT candidate uses repacked texture setup at `0x50` in current converter | Observed for tested conversion |
| `+0x0C` | display-list offset | display-list-like root consumed by converter/runtime | Strong |
| `+0x10` | vertex-list offset | `section10`; 16-byte indexed records from `+0x18` | Strong |
| `+0x14` | unknown-list offset | corresponding root exists/relocates in tested models | Provisional |
| `+0x18` | animation-list offset | corresponding root exists/relocates in tested models | Provisional |
| `+0x1C` | collision-list offset | `section1C`; 4-byte records then 12-byte records | Strong |
| `+0x20` | camera-area-list offset | `section20`; exact Tooie semantics still provisional | Provisional |
| `+0x24` | mesh-list offset | metadata capable of driving runtime vertex mutation in tested BT path | Strong behavior; exact BT name provisional |
| `+0x28` | animated-vertex-list offset | corresponding root retained/relocated by converter | Provisional |
| `+0x2C` | animated-texture-list offset | corresponding root retained/relocated by converter | Provisional |
| `+0x30` | rendered triangle count | BT candidate stores tested triangle-count metadata elsewhere in the expanded header | Provisional across formats |
| `+0x32` | vertex count | related count behavior observed in conversion work | Provisional across formats |

## Vertex lists

### BK reference

`BKVertexList` contains:

```text
+0x00 minCoord[3]
+0x06 maxCoord[3]
+0x0C centerCoord[3]
+0x12 local_norm
+0x14 count
+0x16 global_norm
+0x18 Vtx[]
```

The N64 `Vtx` records are 16 bytes each.

### BT observation

Tooie `section10 + 0x18` is used as the base of 16-byte indexed records. Their first three signed halfwords are consumed as spatial XYZ-like values.

### Assessment

**Strong structural match.** Treat these as N64 vertex records for current analysis, while continuing to validate BT header-field semantics independently.

### Important limit

The current Spiral Mountain converter uses a known-good BT-style 24-byte vertex-header template. Native lair data differs, so the BK field layout above should guide tests, not justify copying one constant BT header to arbitrary models.

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

`BKCollisionList` places:

```text
+0x00 min[3]
+0x06 max[3]
+0x0C y_stride
+0x0E z_stride
+0x10 geo_count
+0x12 scale
+0x14 tri_count
+0x16 padding
+0x18 payload
```

The BK source documents the 4-byte geometry entries as collision-grid cells and the 12-byte entries as triangles. `scale` is the cell width; the stride fields select cells in the spatial grid.

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

### High-value next collision test

Probe BT `section1C` header fields at `+0x00..+0x14` across maps and test whether BK's documented `min/max`, `y_stride`, `z_stride`, `geo_count`, and `scale` relationships predict the actual 4-byte-cell addressing used by Tooie's consumers.

## Display lists / microcode

BK level models in the tested path contain F3DEX commands. Tooie expects F3DEX2-style command encodings.

The current converter translates the relevant command family, including vertex loads, display-list calls, triangle commands, geometry mode, texture/move-word operations, and end-of-list handling. The converter also rejects unsupported non-RDP opcodes rather than silently guessing.

### Known correction

Palette-related `SETOTHERMODE_H` handling required a targeted translation correction during the Spiral Mountain work. Display-list conversion should therefore remain opcode/encoding-aware rather than relying only on opcode-number substitution.

## Texture descriptors

The BK source names a `BKTextureList` containing a size, count, and 16-byte `BKTextureInfo` descriptors. The tested BK level-model path uses texture setup at `0x38`.

The current BT candidate path repacks those descriptors into the compact form used by the tested Tooie model layout and relocates following roots.

### Assessment

**Observed for the Spiral Mountain proof-of-concept.** Do not yet present the converter's layout as the complete BT texture specification for every resource class.

## Opaque / translucent map-model split and water

BK's `src/core2/mapModel.c` has a per-map description table containing both an opaque level-model asset and an optional translucent level-model asset. The source comment explicitly says the translucent model holds **water surfaces and other see-through parts**.

For BK Spiral Mountain this table selects:

- opaque `0x14CF`,
- translucent `0x14D0`.

Project A independently imported those same two models into Tooie's Spiral Mountain primary/secondary resource path and demonstrated water traversal in the resulting environment.

### Assessment

- BK opaque/translucent level split: **direct BK source evidence**.
- Project A's primary/secondary BT use for the tested Spiral Mountain transplant: **Observed**.
- General claim that every BT secondary world resource is exactly equivalent to BK's translucent/water model: **not established**.

This is a strong lead for future water/render-path work, especially when comparing maps that have no secondary resource in BT but do have a separate BK translucent model.

## Mesh/effect vertex groups

BK `model.h` names header `+0x24` as `mesh_list_offset`. `BKMeshList` contains mesh groups with a `uid`, vertex count, and vertex indices; the runtime model structures are used to transform meshes.

In the imported BK secondary Spiral Mountain candidate, copied `+0x24` metadata caused Tooie's runtime to mutate vertex positions, UVs, and colors while display commands stayed unchanged. Clearing the pointer stopped the tested corruption.

### Assessment

- Shared architectural concept involving grouped vertex updates: **Strong**.
- Byte-for-byte compatibility: **not established**.
- Exact BT UID/effect semantics: **provisional/unknown**.

This strengthens the interpretation that the bridge/fence bug was not random memory corruption: the copied metadata points at a structure class that BK itself uses to group vertices for runtime transformation. It still does not prove Tooie interprets every field identically.

## Camera-area data

BK names header `+0x20` as a camera-area list. Its entries contain bounding boxes and an in-bounds flag, and BK comments describe them as controlling which map parts are rendered based on camera position.

Project A currently calls Tooie's corresponding header root `section20` because BT semantics have not yet been independently proven.

### Assessment

BK semantic reference: **direct source evidence**.  
BT equivalence: **Provisional** until a Tooie consumer is traced.

## Map/resource selection

BK's `mapModel.c` maps game map IDs to opaque and optional translucent level-model asset IDs plus bounds offsets and scale.

Tooie's `gcmapDll` independently searches 14-byte map configuration records that select primary and optional secondary resources. Whole-resource replacement of the selected primary changes the static world while retaining other map state.

### Assessment

Both games clearly separate **map identity** from **selected static-world model resources**, but the map-description record layouts are not claimed to be identical.

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
- water/effect metadata beyond the coarse opaque/translucent split,
- animated vertices/textures,
- setup/object placement and actor records,
- map transitions/warps,
- BT camera-area behavior at `+0x20`,
- collision flag semantics,
- spatial partitioning used by enemy AI/detection.

When a new correspondence is added, record whether the BT side is **matched**, **inferred**, or **provisional**, and include the consumer/function evidence that justified the label.
