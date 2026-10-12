# Project A — Status

Last updated: **2026-10-12**

Project A is currently beyond the basic feasibility stage. The major architectural question — whether real Banjo-Kazooie static-world data can be translated into something Banjo-Tooie can render and collide with — has been answered positively for the tested Spiral Mountain assets.

## Working / demonstrated

- BK Spiral Mountain opaque and secondary level models converted into BT candidates.
- Imported terrain rendered inside Tooie's Spiral Mountain map.
- Collision demonstrated on imported terrain.
- Jumping, flight, water traversal, bridge/fence interaction demonstrated.
- At least one Tooie grip-grab demonstrated on BK geometry.
- Secondary bridge/fence corruption traced to incompatible runtime vertex-update metadata; tested candidate fixed by clearing header `+0x24`.
- Return/reload path demonstrated in the active research build.
- Strong BK↔BT structural correspondence established for vertex and collision sections.
- BK compact-sequence bodies shown to be parse-compatible with Tooie's tested generated reader after header conversion in offline verification.
- BK and BT Gruntilda's Lair entrance geometry compared; substantial exact overlap measured.

## Not yet established

- A general-purpose BK→BT model converter for arbitrary levels.
- Safe owned allocation/cache lifetime for imported resources.
- General BT vertex-header derivation instead of the tested Spiral Mountain template.
- Correct integration of BK lair's separate translucent model.
- Setup/object translation for collectibles, enemies, doors, warps, scripted actors, and persistent state.
- Universal collision-flag compatibility.
- Full effect/animation translation.
- Audible BK music playback in Tooie.
- Safe instrument/waveform translation.
- A complete BK campaign running inside BT.

## Current technical bottleneck

The next meaningful integration step is **memory ownership + cache/reload correctness** for large imported world resources, followed by a Gruntilda's Lair entrance-room test using a correctly sized allocation and an explicit translucent-model draw path.

The BK lair primary is much larger than Tooie's native lair primary, so overwriting the native allocation is not acceptable as a durable solution.

## Project maturity

A useful way to think about current progress:

- **Feasibility / architecture discovery:** advanced.
- **Static-world prototype:** demonstrated.
- **Reusable converter/runtime adapter:** early.
- **Object/setup compatibility:** largely unstarted.
- **Campaign-scale integration:** future work.

No percentage is treated as a formal metric. Project A is research-driven; one newly understood subsystem can change the remaining workload substantially.
