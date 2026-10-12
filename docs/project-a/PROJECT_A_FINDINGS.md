# Project A — Current Findings

Last consolidated: **2026-10-12**.

## Scope

Reverse-engineer Banjo-Tooie's static-world/resource architecture and determine which Banjo-Kazooie data can be translated into valid Tooie structures without pretending unverified fields are understood.

## Confidence vocabulary

- **Observed** — directly demonstrated by code, bytes, or runtime behavior.
- **Strongly supported** — multiple observations agree, but the semantic label is not fully proven.
- **Speculative** — plausible interpretation requiring direct evidence.

## Map/resource loading

### Observed

- Current map ID can be traced through `func_800EA05C` / `D_80132DC2`.
- Known observed map IDs include Jinjo Village `0x142`, Spiral Mountain `0x00AF`, Wooded Hollow `0x14F`, Mayahem Temple `0x00B8`, and Gruntilda's Lair entrance `0x00AD`.
- `gcmapDll` searches 14-byte map configuration records.
- Those records provide primary and optional secondary resource IDs.
- The primary world resource is loaded through `func_800D674C`.
- Whole-resource substitution changes static world geometry while surrounding map state remains, establishing the primary resource as a core static-world payload.

## Resource header / geometry structures

### Observed

- Resource/model header `+0x10` selects a section whose indexed 16-byte records begin at section `+0x18`.
- Resource/model header `+0x1C` selects a structure with a header, a 4-byte-record region, then 12-byte records.
- The 12-byte records have three 16-bit indices at `+0x00/+0x02/+0x04`, an unresolved halfword at `+0x06`, and a 32-bit flags/mask field at `+0x08`.
- Those first three indices select the 16-byte records from the `+0x10` section.
- Selected 16-byte records contain signed spatial halfwords at `+0x00/+0x02/+0x04`.

### Strongly supported

- Header `+0x10` is vertex-list-like data.
- Header `+0x1C` is collision-list-like data.

### BK reference correspondence

The public BK decompilation defines:

- `BKVertexList`: header followed by N64 `Vtx` records beginning at `+0x18`.
- `BKCollisionGeometry`: 4 bytes (`s16 start_tri_index`, `s16 tri_count`).
- `BKCollisionTriangle`: 12 bytes (`s16 vertex_index[3]`, `s16 extra`, `s32 flags`).
- `BKCollisionList`: `geo_count` at `+0x10`, `tri_count` at `+0x14`, payload from `+0x18`.

This is a strong structural match, not permission to assume every Tooie field has the same semantics.

## BK→BT Spiral Mountain model conversion

### Observed

- BK assets `0x14CF` (opaque) and `0x14D0` (secondary/translucent) can be converted into BT candidates using the current Project A tooling.
- Targeted BT map `0x00AF`, resources `0x1CF9` and `0x1CFA`.
- Converted terrain has rendered and supported collision, movement, water traversal, flight, bridge/fence interaction, and a tested Tooie grip-grab.
- The public branch contains the BK model probe and first-pass converter:
  - `tools/project_a_bk_model_probe.py`
  - `tools/project_a_bk_to_bt_model.py`

### Important limitation

The converter contains a **known-good Spiral Mountain vertex-header template** and a simple tested Tooie geometry layout. Those choices are experimental knowledge from the working proof-of-concept, not a universal BT model specification.

## Secondary mesh/effect metadata

### Observed

The imported secondary model originally showed dynamic corruption. Live captures showed position/UV/color mutation while draw commands remained stable.

Clearing header `+0x24` on the tested secondary candidate stopped the bridge/fence corruption and restored correct behavior.

### Strongly supported

`+0x24` points to metadata capable of driving runtime updates to selected vertices; blindly copying BK metadata here can make BT apply the wrong effect behavior.

### Not established

- Exact updater function.
- Meaning of each observed UID.
- Whether all BK `+0x24` structures are incompatible with BT.

## Reload lifecycle

A working research build has demonstrated leaving Spiral Mountain, entering the lair, and returning with Project A load state reset and BK return positioning applied.

**Repository caution:** documentation may be ahead of the currently committed runtime adapter. Reproduce against the exact commit named by an experiment before treating this as guaranteed branch behavior.

## Gruntilda's Lair

### Observed geometry overlap

BK primary `0x14F3` vs BT primary `0x1CFD`:

- 376 exact shared vertex positions.
- 743 exact shared unique collision triangles ignoring flags.
- 743 is 61.76% of BT's 1,203 unique collision triangles.
- BK has 1,697 unique collision triangles and broader bounds.

### Integration facts

- BK primary is 241,188 decoded bytes; BT primary is 79,852 bytes.
- Copying the BK resource into the native BT allocation is therefore unsafe.
- BT map `0x00AD` currently identifies primary `0x1CFD` and no native secondary resource in the captured map configuration.
- BK's separate translucent model therefore requires explicit integration rather than inventing a secondary ID.

## Music

### Observed

- Tested BK and BT compact sequences use compatible event encodings for the examined note, tempo, loop, and backward-reference commands.
- BK and BT sequence headers differ, but a narrow header transformation preserves the BK sequence body.
- Header-converted BK candidates matched their original first-pass event traces when executed through an isolated harness using Tooie's generated C sequence-reader bodies.
- Tested BK and BT material uses division 384.

### Not established

- Audible BK music playback in Tooie.
- Complete repeated-loop correctness.
- Waveform/sample identity merely from matching metadata.
- A safe global instrument-bank remap.

## Things deliberately not promoted to fact

- `section10 + 0x16` as a semantic count field based only on neighboring-function behavior.
- Exact equivalence of BK and BT model structures beyond tested correspondence.
- Universal compatibility of BK collision flags, setup data, actors, warps, effects, sky, or animated geometry.
- The cause of the remaining invisible obstruction near the lair entrance.
- Enemy aggression/deadzones as a proven spatial-system bug.
