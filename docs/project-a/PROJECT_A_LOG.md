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
Clearing the **primary** candidate's own `+0x24` pointer did not fix the separate invisible obstruction near the lair entrance. That obstruction therefore remained unresolved at this stage.

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

---

## 2026-10-12 — First playable BK Lair room and actor-factory evidence

### Result

The converted BK Lair entrance primary became playable in Tooie's native lair scene. Native Tooie setup behavior remained active, including Cheato.

A live actor-factory capture identified the requested Cheato actor through Tooie's native factory path and confirmed that native actor-info/constructor pointers execute inside the imported room.

### Interpretation

**Observed:** static BK world geometry and native BT setup/actor behavior can coexist in the hosted scene.

This was useful for bootstrapping, but it also established an important limitation: imported terrain does not automatically import BK setup/object placement.

---

## 2026-10-12 to 2026-10-13 — Connected Lair rooms and native transition ownership

### Goal
Move beyond a single replaced room and make multiple imported BK Lair spaces behave as distinct logical rooms while preserving Tooie's scene/load lifecycle.

### Result

Project A introduced private resource identities and logical-room routing for additional BK Lair terrain. Forward/return routes use Tooie's native transition backend plus room-specific arrival placement/walking.

Live testing demonstrated repeated travel between imported rooms while retaining player control/state. Different arrival contexts into the same hosted map can select different coordinates and walk targets.

### Important implementation lesson

A pending logical-room request must not be allowed to contaminate unrelated native prefetch/cache loads. Delegation/scoping guards were added after one experiment showed that a pending room replacement could populate the wrong native cache identity.

### Interpretation

**Observed:** multiple distinct BK spaces can be hosted inside one Tooie scene identity if resource identity, cache scope, arrival ownership, and transition state are explicitly separated.

---

## 2026-10-13 — Lair 3 water and climb route

### Water

BK Lair 3's separate secondary water terrain was loaded through a private secondary resource path. User testing confirmed visible water, swimming, and access to the CCW puzzle-area terrain.

### Vine

The BK vine data was not directly equivalent to Tooie's native climb registration. A scoped adapter registered the BK source vine endpoints/radius with Tooie's native climb system only for the intended logical room. User testing confirmed the vine route worked.

### Interpretation

**Observed:** some BK environmental gameplay data can be made functional by translating it into the corresponding Tooie runtime subsystem rather than merely copying source bytes.

---

## 2026-10-13 — Milestone: stable Mumbo's Mountain exterior prototype

### Goal
Test whether the increasingly reusable static-world/hosted-room architecture could support a full BK world exterior rather than another Lair room.

### Result

A user-confirmed playtest demonstrated:

- BK MM primary and secondary terrain loaded in a logical hosted room.
- Running/jumping across hills, stumps, and central terrain.
- Lake entry and underwater swimming.
- Entry from the imported Lair and return to the Lair through Tooie's native transition backend.

The initial playable run used a temporary SDL HIDAPI environment workaround for a separate controller-enumeration startup fault. That workaround is not a claim that MM itself caused the SDL fault.

### Presentation limitations

- Host scene identity still supplies `GRUNTILDA'S LAIR (ENTRANCE)` text.
- Original MM actors/items/progression/interiors/music are not yet imported.
- The dark/night presentation is currently accepted as an intentional Project A interpretation rather than automatically treated as a bug.

### Interpretation

**Observed:** the world-resource pipeline is no longer limited to Spiral Mountain/Lair geometry; it supports a distinct BK world exterior with water and two-way hosted traversal in the tested build.

---

## 2026-10-13 to 2026-10-14 — MM exit-pad integration exposes cache/lifetime rules

### Initial problem

The separately converted BK world-exit-pad model initially caused scene corruption or later crashes depending on when/how it was loaded and drawn.

### Load-order finding

Loading the private pad model too early during world initialization interfered with native cache/resource sequencing. Deferring pad acquisition until MM secondary/world initialization completed avoided the earlier load-time corruption in repeated live tests.

### Ownership finding

The private model was pinned/owned through Tooie's native cache, but a later crash showed the stored host guest pointer had become stale.

Live integrity logging proved:

- the cache still contained the pad under the correct resource ID,
- the cached current address had changed,
- the old address now pointed into the relocated model's own display-list data,
- the renderer read `F5000100` from that stale location as if it were the model's vertex-header offset.

### Correction

Native cache ownership/pinning does **not** imply guest-address stability.

The runtime was changed to resolve the current typed-cache address by resource ID before each pad draw and before related model comparisons.

### Result

User testing confirmed two visits with resource relocation and no bad-header warning, followed by matching scene release. A full-opacity pad was then visibly confirmed in gameplay with a complete MM→Lair return.

### Interpretation

**Observed:** Project A runtime code must distinguish ownership lifetime from pointer lifetime.

---

## 2026-10-14 — MM pad flash narrowed to deferred render-consumption/lifetime research

### Symptom

The visible MM exit pad can briefly flash multicolored/striped during entry/transition despite otherwise correct geometry and stable gameplay.

### Negative controls / observations

- Full converted asset snapshots remained byte-identical through the captured flash period.
- Texture/palette and display-list hashes remained unchanged.
- Explicit neutral environment/primitive color state did not eliminate the flash.
- CPU-emitted vertex/texture segment bases matched the **current** model address across captured native relocations.

### RT64 consumer trace

RT64 source inspection showed that RDP texture operations can be recorded and consume RDRAM/TMEM data later during synchronization/upload work.

A live consumer trace captured a case where native cache state already pointed to the relocated pad while texture consumption referenced the **previous** pad range, whose payload no longer matched the expected pad texture bytes.

### Interpretation

**Strongly supported:** the tested path contains a relocation/deferred-consumption lifetime hazard.

**Not yet established:** the complete RT64 root cause or final synchronization/lifetime fix. Do not summarize this as proven “GPU cache corruption.”

---

## 2026-10-14 — MM doorway trigger correction and stress-test notes

### Doorway correction

The first MM entrance region extended far enough outside the doorway to trigger from a side approach. A narrower/deeper predicate was prepared and user-confirmed to reject the side approach while preserving center-door entry.

### Remaining lifecycle edge case

The post-arrival cooldown can temporarily suppress trigger checks; Banjo can cross the finite doorway volume during that interval and only trigger MM after moving back through the region.

### Stress test

Rapid repeated MM/Lair transitions eventually ended with a graphics resource-creation failure (`0x80070057`). This is tracked as a separate stress/lifecycle issue and is **not** treated as proof that normal traversal is unstable or as the same failure as the earlier stale-model-pointer crash.

---

## 2026-10-14 — First live imported Ticker

### Prior offline work

Ticker research had already established:

- hierarchy-preserving model conversion,
- native Tooie geometry-tree traversal,
- sparse BK bone-ID lookup into dense matrix slots,
- direct native reading of the original BK idle/walk/hurt animation streams in the tested CPU path,
- transform-list and matrix generation agreement,
- private model-resource ownership,
- draw callback/pose handoff.

### Live result

A controlled live Ticker spawn rendered in Tooie and idled briefly before its animation froze. Banjo could collide with/hit the actor; Ticker contact dealt damage to Banjo. The current actor did not die correctly.

### Interpretation

**Observed:** Project A has crossed from static actor-format compatibility into a real live imported actor proof.

**Not established:** stable animation ticking, full combat callbacks, death/despawn, movement, targeting, or AI.

The next bounded behavior target is looping idle, normal contact-damage cadence, hurt animation, and lethal death/despawn before AI work.

---

## 2026-10-14 — GL Treasure Trove Cove lobby route prepared/integrated

### Source route

BK source/setup evidence distinguishes the Lair 3 → Treasure Trove Cove lobby route from the separate Red Cauldron branch.

### Implementation

The TTC-lobby primary terrain was converted as another private logical-room resource. The runtime gained distinct loader scope, model identity, forward/return arrival ports, transition triggers, and fall-recovery handling without reusing the older three-row arrival shortcut.

Offline verification covered resource staging/capacity/copy/cache identity and repeated native arrival-controller paths while preserving existing Lair/MM/Ticker work.

### Current status

The lobby is the active next expansion point. World-door behavior, original setup population, translucent secondary handling where unsupported, and TTC proper remain separate work.

---

## Public artifact status note

The chronological findings above are deliberately more current than some committed runtime code. Several successful tests depend on:

- user-owned/extracted BK assets that cannot be redistributed,
- generated candidate files,
- local guarded installer packages,
- laptop builds/checkpoints that are not appropriate to commit wholesale.

The public repository should therefore be treated as the **research record, tooling base, and reproducibility recipe**, not as a guarantee that every current experimental runtime milestone can be reproduced by cloning the branch with no additional owner-supplied inputs.
