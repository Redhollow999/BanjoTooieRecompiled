# Project A — Current Findings

Last consolidated: **2026-10-14**.

## Scope

Reverse-engineer Banjo-Tooie's world/resource architecture and determine which Banjo-Kazooie data and systems can be translated into valid Tooie structures without pretending unverified fields are understood. A parallel goal is to understand how BK and BT “communicate” across generations: which internal systems are close descendants, which were redesigned, and where a translation layer is required.

## Confidence vocabulary

- **Observed** — directly demonstrated by code, bytes, or runtime behavior.
- **Strongly supported** — multiple observations agree, but the semantic label is not fully proven.
- **Speculative** — plausible interpretation requiring direct evidence.

## Map/resource loading and logical hosted rooms

### Observed

- Current map ID can be traced through `func_800EA05C` / `D_80132DC2`.
- `gcmapDll` searches 14-byte map configuration records providing primary and optional secondary resource IDs.
- The primary world resource is loaded through `func_800D674C`.
- Whole-resource substitution changes static world geometry while surrounding map state remains.
- Project A now uses private resource IDs and logical-room state to host multiple imported BK spaces inside Tooie's native scene machinery rather than assuming BK map IDs are directly valid BT map IDs.
- Multiple imported Gruntilda's Lair rooms and Mumbo's Mountain have been exercised through this hosted-room architecture.
- Native Tooie scene transitions and arrival controllers can be reused while supplying BK-derived position/route evidence.

### Consequence

The host scene's own setup/object/title/environment behavior can remain active unless explicitly replaced or suppressed. This explains inherited native actors such as Cheato/egg nests and inherited map identity text in imported BK spaces. It is not evidence that BK setup data has been translated.

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

This remains a strong structural match, not permission to assume every Tooie field has identical semantics.

## BK→BT static-world conversion

### Spiral Mountain — observed

- BK assets `0x14CF` (opaque) and `0x14D0` (secondary/translucent) can be converted into BT candidates using current Project A tooling.
- Converted terrain has rendered and supported collision, movement, water traversal, flight, bridge/fence interaction, and a tested Tooie grip-grab.
- The public branch contains the first BK model probe/converter work, but later room-specific conversion/runtime packages may still be local or non-distributable because they depend on owner-extracted assets.

### Gruntilda's Lair — observed

- Multiple BK lair rooms have been converted and connected as distinct logical rooms.
- Room-specific forward/return arrivals can coexist within the same native host scene.
- Lair 3's separate secondary water terrain was integrated and supports swimming in the tested build.
- A BK vine route was made climbable by registering the source node pair with Tooie's native climb system under a narrowly scoped room/map predicate.
- The next route toward the Treasure Trove Cove lobby has been converted/integrated as an additional logical room; broader world-door/setup behavior remains incomplete.

### Mumbo's Mountain — observed

- BK MM primary and secondary terrain load as a separate logical hosted room.
- User-confirmed gameplay demonstrated running, jumping, slopes, water entry, underwater swimming, and return to the lair.
- The host scene still supplies native lair identity/presentation, including the inherited `GRUNTILDA'S LAIR (ENTRANCE)` title.
- The MM doorway trigger was narrowed after live evidence showed the earlier region could be activated from beside the rock. The narrower region was user-confirmed to reject side approaches while retaining ordinary entry.

## Secondary mesh/effect metadata

### Observed

The imported Spiral Mountain secondary model originally showed dynamic corruption. Live captures showed position/UV/color mutation while draw commands remained stable.

Clearing header `+0x24` on the tested secondary candidate stopped the bridge/fence corruption and restored correct behavior.

### Strongly supported

`+0x24` points to metadata capable of driving runtime updates to selected vertices; blindly copying BK metadata here can make BT apply inappropriate effect behavior.

### Not established

- Exact updater function for every model.
- Meaning of every observed mesh/effect UID.
- Whether all BK `+0x24` structures are incompatible with BT.
- Whether missing/frozen waterfalls are caused solely by disabling copied mesh/effect metadata.

## Native resource ownership, cache relocation, and guest pointers

### Observed

- Imported resources can be loaded through Tooie's native allocation/cache/model-manager paths using private resource IDs and validated sizes/hashes.
- A native model-cache pin/reference protects ownership/lifetime but **does not guarantee a stable guest address**.
- During MM exit-pad testing, the typed/raw cache continued to contain the pad under its resource ID while the model moved to a new guest address.
- A retained host pointer then pointed into the relocated asset's own display-list bytes; the renderer interpreted `F5000100` from those bytes as a vertex-header offset and faulted.
- Re-resolving the current model address from the native typed cache by resource ID before drawing removed the observed stale-model-header failure across tested relocations/visits.
- Matching scene teardown can release/unpin the private pad model by resource ID.

### Correction

Earlier reasoning treated native ownership/pinning as if it implied pointer stability. That assumption was wrong. Ownership and address stability are separate properties.

## MM exit-pad rendering / RT64 timing

### Observed

- Loading the private pad too early during world setup could disturb native scene/cache sequencing; deferring acquisition until the MM secondary/world initialization had completed avoided the earlier scene-load corruption in repeated tests.
- The converted pad has rendered visibly and at full opacity in gameplay.
- One complete visible MM→Lair return was confirmed in video after the relocation fix.
- CPU-side emitted segment bases for pad vertices/textures matched the current native model address across captured resource relocations.
- Full asset snapshots remained byte-identical to the expected converted pad during the observed visual flash.
- Explicit neutral environment/primitive color state did not eliminate the brief multicolored/striped pad flash.
- RT64 traces show texture operations can be deferred: RDP load operations are recorded and later consume RDRAM/TMEM data during synchronization/upload work.
- In a captured consumer trace, current native cache state pointed at the relocated pad while some texture consumption still referenced the previous pad range, whose contents no longer matched the expected texture payload.

### Strongly supported

There is a real lifetime/timing hazard between native resource relocation and deferred rendering consumption for the tested pad path.

### Not established

- A complete RT64 root cause.
- Whether synchronization, copying, pin semantics, or another renderer-facing lifetime mechanism is the correct final fix.
- Whether every observed blue/striped flash has the same cause.

## Transition lifecycle

### Observed

- Native Tooie transition/arrival ownership can preserve state across imported logical-room changes in the tested paths.
- A rapid-transition stress test eventually ended with a graphics resource-creation failure (`0x80070057`) after repeated MM/Lair transitions.
- Post-arrival cooldown can suppress doorway checks long enough for Banjo to cross a finite trigger volume; on returning through the volume the transition can then fire.

### Interpretation

The normal routes work, but the transition lifecycle is not yet stress-hardened. Do not conflate the rapid-transition resource failure with the earlier stale model-pointer failure.

## Ticker actor import

### Offline/native-consumer findings

- BK Ticker's geometry hierarchy, display-list traversal, skinning nodes, selector nodes, sparse bone IDs, original animation streams, transform lists, and native BT matrix generation have been exercised through controlled native-consumer harnesses.
- Original BK idle/walk/hurt animation streams can be read by the tested native BT animation path without a conversion step in the verified CPU reader/matrix tests.
- Private Ticker model-resource ownership and draw handoff have been tested extensively offline.

### Live observed result

- A Ticker has spawned/rendered in Tooie.
- Its idle animation advances briefly before freezing.
- Banjo can collide with/hit it.
- Ticker contact can damage Banjo.
- The current actor is effectively immortal; correct hurt/death/despawn behavior is not established.

### Next behavioral target

Looping idle, normal contact-damage cadence, hurt animation, lethal death/despawn; movement/AI comes later.

## Surface/material audio

### Observed BK-side evidence

BK surface-selector behavior has been reconstructed for several imported maps, including global and per-map flag classes plus separate walking/landing behavior.

### Current symptom

Some imported grass/wet/smooth-looking surfaces produce metallic/clanking Tooie footsteps.

### Not established

The exact BK→BT surface/material flag mapping. BK collision bytes being preserved does not imply that Tooie interprets every material flag identically.

## Music

### Observed

- Tested BK and BT compact sequences use compatible event encodings for the examined note, tempo, loop, and backward-reference commands.
- BK and BT sequence headers differ, but a narrow header transformation preserves the BK sequence body.
- Header-converted BK candidates matched their original first-pass event traces when executed through isolated harnesses using Tooie's generated sequence-reader bodies.
- Tested BK and BT material uses division 384.
- MM sequence analysis found substantial program/sample-metadata compatibility, but this is still not audible playback evidence.

### Not established

- Audible BK music playback in Tooie.
- Complete repeated/nested-loop correctness.
- Waveform/sample identity merely from matching metadata.
- A safe global instrument-bank remap.

## Things deliberately not promoted to fact

- `section10 + 0x16` as a semantic count field based only on neighboring-function behavior.
- Exact equivalence of BK and BT model structures beyond tested correspondence.
- Universal compatibility of BK collision flags, setup data, actors, warps, effects, sky, or animated geometry.
- A single universal explanation for every imported-map rendering artifact.
- The brief MM pad flash as proven “GPU cache corruption”; current evidence points to a relocation/deferred-consumption hazard, but the final renderer mechanism/fix is still open.
- Rapid-transition crashes as proof that normal route traversal is unstable.
- Live Ticker spawn as proof of complete enemy compatibility.
