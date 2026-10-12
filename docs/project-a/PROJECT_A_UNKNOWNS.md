# Project A — Unknowns, Risks, and Failed Experiments

This file exists to prevent the research log from turning successful hacks into folklore. Unknowns and negative results are first-class findings.

## High-priority unknowns

### 1. Owned allocation and cache lifetime

The current proof-of-concept has used experimental runtime placement/replacement strategies. For larger resources such as BK Gruntilda's Lair, Project A needs a correctly sized owned allocation whose lifetime and cache behavior are understood.

Do **not** assume the native BT asset allocation is large enough. BK lair primary `0x14F3` is 241,188 decoded bytes versus BT lair primary `0x1CFD` at 79,852 bytes.

### 2. General BT vertex-header semantics

The Spiral Mountain converter uses a known-good Tooie-style vertex-header template. Native lair data already demonstrates that one constant template should not be assumed correct for all models.

Need: identify the native consumers of the remaining bounds/norm/count fields and derive them from source data rather than copying constants.

### 3. `+0x24` mesh/effect system

Clearing secondary model header `+0x24` fixed the tested bridge/fence corruption, strongly implicating incompatible runtime vertex-update metadata.

Still unknown:

- exact updater function(s),
- group UID semantics,
- which BK metadata can be safely translated,
- whether some groups correspond to water, scrolling textures, vertex color animation, or other effects.

### 4. Gruntilda's Lair translucent model

BT map `0x00AD` reports no native secondary resource in the captured map configuration, while BK uses a separate translucent model `0x150B`.

Need: identify the correct draw/integration path rather than guessing a nonexistent native resource slot.

### 5. Setup/object translation

Playable terrain does not establish support for:

- Jiggies,
- notes,
- Jinjos,
- enemies,
- doors,
- warps,
- triggers,
- scripted actors,
- persistent world state.

This is the next major architectural layer after static-world integration stabilizes.

### 6. Enemy aggression deadzones

Native BT enemies have been observed to stop detecting Banjo in some imported-map areas.

Possible spatial/AI partition mismatch is **speculative**. The symptom is real; the cause is not yet established.

### 7. Lair entrance invisible obstruction

There remains an apparent invisible obstruction near the imported/target lair entrance area.

#### Negative experiment
Clearing the primary candidate's `+0x24` metadata pointer produced no observed improvement. Therefore the obstruction should not currently be attributed to that metadata alone.

### 8. Music playback and bank compatibility

Offline parsing compatibility is much further along than runtime audio proof.

Still required:

- safe runtime sequence replacement,
- cache/allocation integration,
- audible verification,
- repeated-loop testing,
- waveform/sample identity work,
- restrained program remapping only where evidence supports it.

Matching metadata or tuning does not prove two compressed waveform samples are identical.

## Corrections / assumptions that must not return

### `section10 + 0x16` semantic count

A neighboring-function scan once suggested a count interpretation. That was not established because those functions were not proven to consume the same structure. Keep the raw observation separate from the semantic claim.

### Music asset type-4 guard

An early extractor treated a metadata type check as a requirement for music assets. Static analysis showed that assumption was wrong. Do not restore the guard without new evidence.

### Universal constant vertex header

A template that worked for Spiral Mountain is not evidence of a universal BT model header. Native lair data already cautions against this generalization.

### `+0x24` means "the bridge bug"

The pointer is not semantically named merely because clearing it fixed one model. The supported claim is narrower: the referenced metadata can enable runtime vertex updates that were incompatible with the tested BK secondary model.

## Runtime/upstream risk

Project A currently uses BanjoTooieRecompiled as a runtime backend. Upstream changes to memory management, generated-function ABI, asset caching, hook points, or recomp architecture may break the adapter.

The mitigation is architectural separation:

```text
BK data / research
       ↓
conversion + validation tools
       ↓
BT-compatible candidate data
       ↓
runtime adapter
       ↓
BanjoTooieRecompiled
```

If the runtime adapter breaks, the research and conversion layers should remain useful.

## Public-branch lag

Some experiments documented here were verified in the active working environment before the corresponding runtime changes were necessarily committed to GitHub. When reproducing a milestone, first verify the exact branch/commit and artifact status in the research log.
