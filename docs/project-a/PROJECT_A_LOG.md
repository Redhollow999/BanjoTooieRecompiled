# Project A — Research Log

This is the curated public research log. It records significant experiments, corrections, and milestones rather than every console dump or temporary file.

## Logging standard

Each substantial investigation should identify:

- **Question** — what was being tested.
- **Evidence** — source files, functions, hashes, captures, or runtime observations.
- **Procedure** — enough detail to reproduce the test.
- **Result** — including negative results.
- **Interpretation** — Observed / Strongly supported / Speculative.
- **Artifact status** — whether the relevant code/tool is committed, local-only, or still proposed.

---

## 2026-10-10 — Map-resource architecture and section crosswalk

### Question
Determine what Tooie's anonymous map-resource header sections contain and whether Banjo-Kazooie's mature decompilation can provide structural guidance.

### Observed

- Current map identity can be traced through `func_800EA05C` / `D_80132DC2`.
- `gcmapDll` searches 14-byte map-configuration records containing primary and optional secondary resource IDs.
- The primary world resource is loaded through `func_800D674C`.
- Whole-resource substitution changes static world geometry while retaining surrounding map state.
- Tooie resource header `+0x10` selects a section whose payload begins at `+0x18` with 16-byte indexed records.
- Header `+0x1C` selects a structure containing a 4-byte-record region followed by 12-byte records.
- The 12-byte records contain three 16-bit values at `+0x00/+0x02/+0x04`, an unresolved 16-bit field at `+0x06`, and a 32-bit flags/mask field at `+0x08`.
- The first three values index the 16-byte records from the `+0x10` section; the selected records contain signed XYZ-like halfwords at `+0x00/+0x02/+0x04` used by spatial/math code.

### BK structural comparison

Public BK source defines a vertex list whose N64 `Vtx` records begin at `+0x18`, plus a collision list containing 4-byte geometry records and 12-byte triangles with three vertex indices, an extra halfword, and flags.

### Interpretation

- `+0x10` is **strongly supported** as vertex-list-like data.
- `+0x1C` is **strongly supported** as collision-list-like data.
- Exact BT field names and byte-for-byte identity with BK remain unproven.

### Correction retained

A neighboring-function scan suggested `section10 + 0x16` might be a count. That semantic interpretation was **not established** because the neighboring functions were not yet proven to operate on the same structure. Do not reuse that assumption as fact.

---

## 2026-10-11 — Milestone 2.0: playable BK Spiral Mountain terrain in Tooie

### Question
Can real BK level-model data be converted into a resource Tooie can render and collide with?

### Procedure / artifacts

- BK Spiral Mountain opaque model: asset `0x14CF`.
- BK Spiral Mountain translucent/secondary model: asset `0x14D0`.
- Tooie target map: Spiral Mountain `0x00AF`.
- Tooie target primary/secondary resources: `0x1CF9` / `0x1CFA`.
- Repository tools include:
  - `tools/project_a_bk_model_probe.py`
  - `tools/project_a_bk_to_bt_model.py`

The converter translates the BK level-model header/texture descriptor layout, relocates root pointers, installs a tested BT-style vertex header/geometry layout, and translates relevant F3DEX commands to F3DEX2 equivalents.

### Observed result

The imported BK terrain became playable in the Tooie engine. Gameplay demonstrated collision, jumping, flight, water traversal, and bridge/fence interaction. A Tooie grip-grab also worked on a BK-only ledge in the tested area.

### Interpretation

**Observed:** a practical BK→BT static-world model transplant is possible for the tested Spiral Mountain assets.

This does **not** establish universal level compatibility, setup/object compatibility, enemy compatibility, warp compatibility, or correct handling of every model-header subsystem.

---

## 2026-10-11 — Secondary model corruption traced to `+0x24` metadata

### Question
Why did the imported bridge/fence stretch or move as though animated while its source geometry was sane?

### Evidence

Two live RAM captures showed runtime changes while draw commands remained unchanged:

- 152 vertices changed position.
- 384 vertices changed UVs.
- 157 vertices changed color.

The candidate secondary model had a nonzero header pointer at `+0x24`, leading to seven mesh/effect groups with UIDs 115, 120, 135, 300, 497, 498, and 499.

### Experiment
Clear the candidate's `+0x24` pointer while leaving the rest of the converted secondary model intact.

### Result
The reported bridge/fence distortion stopped and collision behaved correctly in the tested build.

### Interpretation

**Strongly supported:** incompatible copied mesh/effect metadata was enabling inappropriate runtime vertex updates.

The exact updater function and semantics of the individual group UIDs are still unknown.

### Negative control
Clearing the **primary** candidate's own `+0x24` pointer did not fix the separate invisible obstruction near the lair entrance. That obstruction therefore remains unresolved.

---

## 2026-10-11 — Milestone 2.2: reload/return handling

### Question
Can Project A reapply imported geometry after leaving Spiral Mountain and returning?

### Result
A working research build demonstrated a lair transition followed by a return to Spiral Mountain with per-load injection state reset and the external lair return position corrected from BK setup data.

### Artifact status
The public GitHub branch can lag the newest local runtime experiment. Verify the corresponding runtime patch before assuming the branch reproduces this milestone as-is.

---

## 2026-10-11 — Music format comparison

### Observed

- BK Spiral Mountain main sequence decodes to 16,060 bytes; bridge variant to 4,798 bytes.
- BK compact sequences use 16 track offsets followed by division.
- BT sequences use division `u32`, track-count `u32`, then track offsets.
- Both tested games use timing division 384.
- Tooie's generated sequence readers support compatible note duration, tempo, loop (`FF2E`/`FF2D`), and backward-reference (`FE`) behavior for the tested data.
- BK header-converted candidates matched original first-pass event traces in an isolated harness built from Tooie's generated C readers.

### Correction retained
An earlier extractor assumed a music asset had to pass a specific type-4 guard. Static analysis showed that assumption was wrong; the extraction guard was removed.

### Interpretation

**Observed:** the tested BK sequence bodies can be parsed after a narrow BT header transformation.

**Not established:** audible BK playback in Tooie, waveform identity, full loop behavior, bridge-area switching, or global instrument-bank compatibility.

---

## 2026-10-11 to 2026-10-12 — Gruntilda's Lair comparison

### Source / target

- BK lair primary: asset `0x14F3`, 241,188 decoded bytes.
- BK separate translucent model: asset `0x150B`, 3,668 bytes.
- BK MM-lobby sequence: asset `0x1534`, 6,357 bytes.
- BT native lair primary: asset `0x1CFD`, 79,852 decoded bytes.
- BT lair map: `0x00AD`.

### Geometry comparison

Exact-coordinate comparison found:

- 376 shared vertex positions.
- 743 shared unique collision triangles when collision flags are ignored.
- Those 743 triangles are 61.76% of BT's 1,203 unique collision triangles.
- BK contains 1,697 unique collision triangles and wider bounds.

### Runtime/integration implications

- The BK primary is roughly three times the native BT allocation; it must receive an owned allocation large enough for the converted resource.
- BT's native lair map reports no secondary resource in the tested map configuration, so BK's separate translucent model needs explicit draw/integration work rather than an invented native secondary ID.
- Native setup/Cheato/state should be retained initially; BK doors, spawns, actors, and setup behavior are not yet proven compatible.

### Music observation — 2026-10-12

Repeated lair visits requested main track `0x0034`; using the known BT sequence asset base, this identifies native lair sequence asset `0x1E11` in the tested build. Native BT lair and BK MM-lobby sequences share division 384 and the same observed tempo value, but differ substantially in active-track/event counts.

### Current blocker
Proper allocation/cache lifetime, model-bounds handling, and drawing the separate translucent BK resource are higher priority than further speculative patching.
