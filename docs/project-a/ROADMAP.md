# Project A — Roadmap

This roadmap is ordered by technical value, not by hype value. The aim is to reduce unknowns in the order most likely to produce reusable knowledge while preserving the currently working Spiral Mountain, Lair, and Mumbo's Mountain checkpoints.

Last updated: **2026-10-14**

## Priority 0 — Keep the research reproducible

Before expanding scope:

- Tie runtime claims to specific source/checkpoints or clearly mark them local-only.
- Record hashes for non-distributable inputs/outputs.
- Preserve failed experiments, negative controls, and corrected assumptions.
- Keep the runtime adapter separable from conversion/research code.
- Avoid promoting semantic names until consumer behavior supports them.
- Never commit ROMs, extracted game assets, or other copyrighted game data.
- Preserve known-good user-tested checkpoints before every invasive runtime experiment.

## Priority 1 — Continue the connected Lair route toward TTC

### Goal
Extend the currently demonstrated logical-room architecture beyond Lair 3 and establish a stable Gruntilda's Lair → TTC-lobby route using translated BK geometry plus Tooie's native transition backend.

### Current state

- Lair rooms 1–3 are already part of the connected prototype.
- Lair 3 water/swimming and a scoped climbable-vine route have been demonstrated.
- The GL Treasure Trove Cove lobby primary terrain has been converted and integrated as the next logical hosted room.

### Next work

- Verify repeatable forward/return traversal and arrival ownership.
- Keep room identity/resources distinct in the native cache.
- Add only the minimum world-door/transition behavior required to continue toward TTC.
- Preserve rollback to the known-good Lair 1–3/MM checkpoints.
- Treat the Red Cauldron room as a separate route rather than conflating it with the TTC lobby.

### Success criterion
A repeatable Lair 3 ↔ TTC-lobby route with correct terrain, collision, arrival, return, and resource cleanup, without breaking existing rooms.

## Priority 2 — Separate logical-room setup/object population from the native host

### Goal
Stop imported rooms from unintentionally inheriting inappropriate native Lair-1-style object placement while retaining native systems we intentionally still need.

### Current symptom

The logical-room architecture deliberately reuses Tooie's native scene machinery. As a result, host actors such as Cheato and egg nests can appear in imported rooms where BK did not place them. Some have already been relocated as a temporary safety/presentation measure.

### Questions

- Which setup/actor requests belong to the native host versus the translated logical room?
- Can specific inherited actors be suppressed without breaking scene controllers or ownership?
- Which native actors should remain temporarily because they provide useful state/progression behavior?
- What is the smallest path toward actual BK setup/object translation rather than permanent manual relocation?

### Success criterion
Each logical room can explicitly define which native setup actors are retained, relocated, suppressed, or replaced, without global side effects.

## Priority 3 — Finish the MM exit-pad renderer/lifetime investigation

### Established

- Deferring pad acquisition until the MM scene is initialized prevents the earlier scene-load corruption.
- Model-cache pin/reference ownership does not guarantee a stable guest address.
- Live testing showed the pad resource relocate while remaining valid in native caches.
- Re-resolving the current typed-cache address before draw fixed the stale-model-header crash.
- CPU-side model/texture segment bindings remain correct across captured relocations.
- RT64 tracing captured deferred texture consumption from an older pad range after the native cache had moved the model.

### Open problem
A brief multicolored/striped pad flash remains. Asset bytes, tint state, and CPU-emitted segment bases were stable/correct in the reviewed captures.

### Next work

- Trace RT64/RDP consumption across model relocation with minimal instrumentation.
- Determine whether already-submitted work can retain an address into memory that is later reused.
- Prefer a synchronization/lifetime fix over disabling native cache compaction unless evidence requires otherwise.
- Keep the working cache-current-address lookup and scene-owned release behavior.

### Success criterion
Stable exit-pad presentation across entry, exit, re-entry, and native resource relocation with no flash, stale pointer, or resource leak.

## Priority 4 — Harden transition lifecycle and doorway triggering

### Current findings

- The narrowed MM doorway trigger is user-confirmed to reject side approaches while retaining normal entry.
- A finite post-arrival cooldown can allow Banjo to cross the doorway volume before trigger checks resume, leaving him inside the mountain until he returns through the volume.
- Aggressive rapid transition stress eventually produced a graphics resource-creation failure; this is tracked separately from the old stale-model-header failure.

### Next work

- Gate doorway triggering on scene readiness rather than a blindly timed cooldown where practical.
- Preserve arrival-walk ownership and avoid immediate retrigger loops.
- Reproduce the rapid-transition failure only when needed for diagnosis; it is not the current top blocker.

## Priority 5 — Advance Ticker from first live spawn to a real enemy

### Established

- Model hierarchy, geometry traversal, sparse bone-ID lookup, original animation decoding, transform lists, native matrices, resource ownership, and draw handoff have extensive offline verification.
- A live Ticker has spawned/rendered, briefly animated, collided with Banjo, and produced contact damage.

### Next target

1. Loop idle reliably.
2. Normalize contact-damage cadence/cooldown.
3. Play the BK hurt animation when attacked.
4. Support lethal damage and clean death/despawn.
5. Only then add movement/targeting/AI.

### Success criterion
A stable, killable imported Ticker with correct basic idle/contact/hurt/death behavior in a controlled scene.

## Priority 6 — Setup / object / progression architecture

### Goal
Move from hosted terrain plus inherited Tooie setup toward actual BK gameplay structure.

Candidate first systems:

- simple collectibles,
- basic enemy placement,
- note-door/puzzle state,
- world-entry/exit objects,
- persistent flags,
- room/world-specific actor spawning.

A single correctly translated object with persistence is more valuable than many visually imported but state-broken objects.

## Priority 7 — Surface-material and collision-audio translation

Imported maps can produce incorrect footsteps (for example grass sounding metallic/clanky).

BK's surface selector behavior has been reconstructed for several imported maps, but the corresponding Tooie mapping is not yet established.

### Success criterion
A narrow, evidence-backed translation that preserves distinct grass/stone/wet/metal/etc. behavior instead of applying a blanket sound replacement.

## Priority 8 — Effects, sky, water, camera and animated environment

Investigate systems currently outside the static-terrain core:

- mesh/effect groups at model header `+0x24`,
- animated vertices/textures,
- waterfalls and other dynamic surfaces,
- sky/environment presentation,
- camera-area data and obstruction behavior.

The current dark/night MM presentation is an accepted project art direction, so environment work should distinguish intentional presentation from actual compatibility bugs.

## Priority 9 — Music runtime integration

The event/sequence side remains promising.

### Steps

- reversible room/mode-gated sequence replacement,
- audible playback verification,
- repeated-loop verification,
- program remapping only where note-level metadata evidence supports it,
- keep sequence-format work separate from waveform/sample identity.

No global instrument-bank substitution should be performed merely because metadata looks similar.

## Priority 10 — Generalize conversion and runtime boundaries

As additional rooms/worlds succeed:

- derive model-header fields algorithmically where possible,
- formalize supported/unsupported feature detection,
- add fixtures using hashes/metadata rather than copyrighted assets,
- fail closed on unknown structures,
- separate conversion from runtime injection,
- reduce direct coupling to generated-function bodies,
- document the minimum runtime backend contract needed by Project A.

## Long-term outcome

The ideal end state is not merely “BK happens to run in this fork.” It is a documented compatibility layer and body of BK↔BT reverse-engineering knowledge that explains how the two games' world, model, collision, actor, animation, audio, and state systems relate — knowledge that remains useful even if the current recomp backend changes.
