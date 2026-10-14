# Project A — Status

Last updated: **2026-10-14**

Project A is now well beyond the original static-terrain feasibility test. The current prototype demonstrates a growing connected slice of Banjo-Kazooie content hosted by Banjo-Tooie's runtime, while the research continues to separate reusable BK↔BT compatibility findings from temporary runtime-specific hooks.

## Working / demonstrated

### Spiral Mountain

- BK opaque and secondary level models converted into BT-compatible candidates.
- Imported terrain rendered with collision, jumping, flight, water traversal, bridge/fence interaction, and a tested Tooie grip-grab on BK geometry.
- The earlier bridge/fence mutation problem was traced to incompatible copied mesh/effect metadata at model-header `+0x24`; clearing that metadata fixed the tested candidate.
- Reload/return handling has been demonstrated in the working research line.

### Gruntilda's Lair

- Multiple BK lair rooms have been converted and connected as logical rooms inside Tooie's native lair host scene.
- Tooie's native transition backend is used for forward/return travel and room-specific arrival walking/placement.
- Lair 3 secondary water terrain renders and supports swimming.
- The tested Lair 3 vine route was restored through scoped registration with Tooie's native climb system.
- Imported rooms currently inherit portions of native Tooie setup/object behavior; Cheato and egg nests are examples of host-scene actors that can appear where BK did not place them.
- A route toward the Treasure Trove Cove lobby has been converted/integrated as the next logical room; broader lobby/world-door behavior remains under active work.

### Mumbo's Mountain

- BK MM primary and secondary terrain load in a logical hosted room.
- User-confirmed playtesting demonstrated running, jumping, slopes, water entry, underwater swimming, and return to the lair.
- The BK exit-pad model has been rendered as a separate private model resource.
- A stale-pointer failure was localized to native model-cache relocation: a pinned/owned model may still move, so the current guest address must be re-resolved by resource ID before draw use.
- A full-opacity pad and one complete visible MM→Lair roundtrip were confirmed in video.
- The MM doorway trigger was narrowed and user-confirmed to reject side approaches that previously triggered the level from outside the doorway.
- Current visual/presentation issues include the inherited `GRUNTILDA'S LAIR (ENTRANCE)` title, a brief multicolored/striped exit-pad flash, incomplete original landmarks/actors/progression, and host-scene presentation differences.

### Ticker actor research

- BK Ticker model/animations were extracted and structurally validated.
- Geometry traversal, sparse bone-ID mapping, original animation reading, transform lists, native matrix construction, resource ownership, and draw handoff have been tested extensively offline against native BT consumers.
- A live Ticker has now spawned/rendered in Tooie, briefly animated, collided with Banjo, and dealt contact damage.
- The current live actor freezes after a short idle period and does not yet have correct hurt/death/despawn behavior.

### Resource / renderer findings

- Private resource IDs are being used for imported logical-room/model resources instead of blindly overwriting unrelated native assets.
- Native cache ownership/reference-count behavior has been exercised for several imported resources.
- Model-cache ownership does **not** imply a stable guest pointer. Live testing proved resource relocation while the model remained present in native caches.
- CPU-side segment bindings for the MM pad remained correct across captured relocations.
- RT64 consumer tracing captured deferred texture reads from an older pad address after native relocation. This strongly supports a render-consumption/lifetime race as an active MM pad-flash research direction, but no final renderer fix is claimed yet.

## Not yet established / incomplete

- Full BK setup/object translation for every room/world.
- Correct BK note-door, puzzle, collectible, enemy, warp, and progression behavior.
- Removal/replacement of all inherited Tooie host actors in imported logical rooms.
- Universal BK collision/surface-material compatibility; some imported grass/wet/smooth surfaces currently produce incorrect Tooie footstep sounds.
- Full animated-effect translation, including frozen/missing waterfall behavior.
- Correct original BK sky/environment presentation where desired.
- Audible BK music playback in Tooie and safe complete instrument/waveform integration.
- Stable full Ticker animation/combat/AI/death lifecycle.
- A general-purpose campaign-ready converter with no room-specific runtime integration.
- Long-session/stress stability across rapid repeated transitions.

## Current high-value bottlenecks

1. **Lair/TTC expansion and logical-room setup separation** — prove the next route cleanly, then reduce inherited native object/setup leakage.
2. **MM renderer/resource timing** — understand and fix the brief pad texture flash without disabling native cache relocation or making unsupported renderer assumptions.
3. **Rapid-transition lifecycle** — a stress test eventually produced a graphics resource-creation failure; the current finite doorway cooldown can also be crossed before trigger checks resume.
4. **Ticker live lifecycle** — restore looping idle, normal damage cadence, hurt response, lethal death/despawn, then AI/movement.
5. **Surface-material/audio mapping** — translate BK collision/material semantics into the correct Tooie footstep behavior.

## Project maturity

A useful way to describe the current state:

- **Feasibility / architecture discovery:** advanced.
- **Static-world import:** demonstrated across multiple distinct areas.
- **Connected hosted-world prototype:** demonstrated and expanding.
- **Reusable resource/cache integration:** intermediate; major ownership and relocation behavior is now understood, renderer timing still open.
- **Actor import:** first live proof achieved; behavior integration early.
- **Object/setup/progression compatibility:** early.
- **Campaign-scale integration:** future work.

No percentage is treated as a formal progress metric. Project A remains research-driven, and newly understood subsystems can materially change the remaining workload.

## Repository-artifact warning

This status reflects verified research/runtime results through the date above. The `project-a` branch can still lag the exact current laptop runtime, non-distributable converted assets, or experimental installer packages. Documentation should therefore be read together with each experiment's artifact status rather than as a claim that cloning this branch alone reproduces every listed milestone.
