# Project A — Runtime Adapter Audit

This document separates **Project A's game-format research** from the **current BanjoTooieRecompiled runtime prototype**.

That distinction matters because upstream recomp/runtime changes may invalidate hook points or memory assumptions without invalidating the BK↔BT conversion findings.

Last updated: **2026-10-14**

## Public branch versus current experimental runtime

The public `project-a` branch contains the documented research base and some early conversion/runtime tooling, but the newest verified gameplay experiments can still exist only as guarded local installer packages, user-owned extracted assets, or laptop checkpoints.

Do **not** assume that a documented runtime milestone is already committed as a directly runnable branch state. Artifact status remains part of the evidence record.

## How the runtime architecture has evolved

The earliest public prototype used direct injection from `src/recomp_api.cpp`, hard-coded candidate paths/sizes, scratch placement, and process-lifetime guards. Those techniques were useful for proving feasibility but are not a durable architecture.

The later Project A line has moved toward a more disciplined model:

- private resource IDs for imported BK world/model resources,
- native Tooie allocation/cache/model-manager ownership where practical,
- explicit logical-room identity separate from native host-map identity,
- room/resource staging scopes to prevent prefetch/cache contamination,
- native Tooie scene transitions and arrival-controller ownership,
- guarded per-scene lifetime/release hooks,
- exact hashes/size validation for owner-supplied converted resources,
- checkpoint/restore installers rather than irreversible source replacement.

The current experimental implementation is still highly coupled to generated/native function bodies and should not be mistaken for the final compatibility-layer API.

## Major runtime lessons now established

### 1. Capacity and ownership must be explicit

A pointer being inside RDRAM proves neither capacity nor ownership.

Larger imported models require verified capacity before copy/allocation. The Lair and MM work moved away from blindly copying into smaller native allocations and toward private resource identities using the native loader/cache stack.

### 2. Cache identity must be scoped

A logical-room request cannot simply remain globally pending while unrelated native prefetches occur.

An earlier Lair-room experiment showed that pending replacement state could populate a native cache identity with the wrong room's geometry. Delegation/staging scopes now restrict replacement to the exact private resource load being serviced.

### 3. Ownership does not mean pointer stability

This is one of the most important corrections to the earlier runtime model.

The MM exit-pad resource remained present and pinned in Tooie's native model/raw caches while its guest address changed. Host code retained the old guest pointer; after relocation, that old address pointed into the moved model's own display-list bytes.

The resulting renderer fault interpreted a graphics-command word (`F5000100`) as a model vertex-header offset.

**Rule:** if the native cache may relocate a resource, store/own it by resource identity and resolve its current guest address when needed. Do not treat a cached guest pointer as permanently stable merely because the resource remains owned.

### 4. Scene load order matters even with correct ownership

The MM pad initially caused corruption when loaded too early during native world setup.

Source tracing identified native world-loader/cache state that is consumed after primary/secondary resource requests. A nested Project A model load can perturb that state if inserted at the wrong moment.

Deferring the pad acquisition until the MM secondary/world initialization completed eliminated the earlier load-time corruption in repeated live tests.

**Rule:** replacement/private loads must respect the host engine's ordering contracts, not merely its allocation APIs.

### 5. Draw-time CPU pointers are only part of the lifetime problem

After the stale host pointer was fixed, a brief multicolored/striped MM exit-pad flash remained.

The following were checked in live captures:

- full converted asset bytes remained intact,
- texture/palette and display-list hashes remained stable,
- CPU-emitted segment bases used the current relocated model address,
- explicit neutral draw tint did not eliminate the flash.

RT64 source tracing shows that texture load operations can be recorded and consume RDRAM/TMEM data later during synchronization/upload processing.

A live consumer trace captured texture reads from the **previous** pad address after Tooie's native cache had already relocated the model. This is strong evidence of a renderer-facing lifetime/synchronization hazard, but the final root cause/fix is still open.

### 6. Logical-room identity is not native map identity

Many imported Lair rooms and MM currently run inside native Tooie map/scene machinery.

Project A therefore tracks at least two concepts:

- **host scene/map identity** — what Tooie believes is loaded,
- **logical Project A room/world identity** — which translated BK resource/route is active.

This architecture enables fast experimentation, but it also explains inherited native actors, title text, music, environment state, and setup behavior.

Long-term setup/object translation should reduce this leakage rather than indefinitely accumulating manual actor relocations.

## Current fragility / technical debt

### Generated-function coupling

Several experiments patch or wrap specific generated/native functions. Upstream recomp regeneration can move or rewrite these bodies.

Every such patch should:

- validate exact expected body/source hashes,
- fail closed on drift,
- preserve unrelated functions,
- create rollback/checkpoint state,
- distinguish reusable game-format knowledge from backend-specific hook locations.

### Cross-cutting runtime code

Project A behavior still spans host C++ runtime code and generated/native C patches. This is harder to audit than a narrow dedicated adapter.

### Non-distributable resources

Current working room/model candidates are generated from owner-supplied BK data. The public repository can distribute extraction/conversion recipes, manifests, hashes, and verification code, but not the copyrighted outputs themselves.

### Host-scene setup leakage

Because the logical-room design reuses native scene machinery, imported terrain can inherit Tooie actors/setup/title/music. This is currently intentional scaffolding, not a completed compatibility result.

### Rapid-transition lifecycle

Ordinary Lair/MM traversal works in tested runs, but aggressive repeated-transition stress has produced a graphics resource-creation failure. Post-arrival cooldown can also interact badly with finite trigger volumes. Lifecycle hardening remains incomplete.

## Target architecture

The desired boundary remains:

```text
BK ROM / extracted user-owned data
              ↓
      extraction + validation
              ↓
       BK → BT conversion
              ↓
    BT-compatible candidate data
              ↓
      Project A runtime adapter
              ↓
     current recomp backend
```

The runtime adapter should eventually depend on stable capabilities rather than many specific generated-function bodies.

## Recommended source split

A future behavior-preserving cleanup should move Project A-specific host/runtime policy out of generic recomp plumbing, for example:

```text
src/project_a/
├── project_a_runtime.cpp
├── project_a_runtime.hpp
├── project_a_assets.cpp
├── project_a_rooms.cpp
└── project_a_state.hpp
```

Suggested responsibilities:

### `project_a_assets`

- validate local candidate files/manifests,
- request/release private resource identities,
- expose resource IDs/metadata rather than long-lived guest pointers,
- perform no room-specific route policy itself.

### `project_a_state`

- requested/active mode,
- native host map identity,
- logical Project A room identity,
- pending transition/arrival context,
- resource ownership IDs,
- per-scene generation/lifetime state.

### `project_a_rooms`

- logical room definitions,
- private resource IDs,
- route/arrival evidence,
- setup-retain/suppress/replace policy,
- world-specific transition regions.

### `project_a_runtime`

- receive narrow lifecycle events from the recomp/backend layer,
- decide whether a Project A resource/route applies,
- request/release native resources,
- resolve current guest addresses only when needed,
- coordinate transition/scene teardown state.

### generic recomp layer

Should eventually know as little as possible about BK asset IDs, Project A room numbers, candidate filenames, or gameplay policy.

## Minimum backend contract to aim for

Conceptually, Project A wants capabilities such as:

```text
on_scene_begin(native_map_id, scene_generation)
on_world_resource_request(resource_id, role)
on_world_resource_ready(resource_id)
on_scene_teardown(native_map_id, scene_generation)

load_private_resource(resource_id, expected_size, expected_hash)
pin_resource(resource_id)
unpin_resource(resource_id)
resolve_current_resource_address(resource_id)
release_resource(resource_id)

queue_native_transition(...)
register_arrival_context(...)
```

Renderer-facing resources may also need an explicit contract preventing relocation/reuse until deferred render consumption is finished, or an equivalent safe-copy/synchronization mechanism. The exact API is **not established** yet.

## Near-term runtime priorities

1. Complete/verify the Lair 3 ↔ TTC-lobby route while preserving existing logical-room/cache identity rules.
2. Add explicit policy for inherited native setup actors (retain/relocate/suppress/replace) instead of letting every logical room inherit the host population accidentally.
3. Finish the MM pad renderer-lifetime investigation using actual RT64 consumer evidence; do not solve it by disabling compaction without proof.
4. Replace fixed post-arrival trigger cooldown assumptions with scene-readiness/transition-state logic where practical.
5. Continue Ticker live behavior work without coupling its resource/actor ownership to unrelated map hooks.
6. Only then undertake a larger behavior-preserving adapter refactor.

## Refactor rule

Do **not** combine architectural cleanup with a new behavioral/memory model in the same experiment.

First extract the known working behavior behind a narrower interface and verify the same gameplay checkpoint. Then change ownership/lifetime/backend semantics in a separate experiment.

## What survives an upstream rewrite

Even if every current hook becomes unusable, these Project A outputs should remain valuable unless separately disproven:

- BK extraction/inspection tooling,
- BK→BT static-model conversion findings,
- vertex/collision structural correspondence,
- display-list translation findings,
- exact Lair geometry comparison,
- compact-sequence format comparison,
- Ticker geometry/animation/matrix cross-game findings,
- logical-room/arrival evidence derived from BK source/setup data,
- native cache relocation/pointer-lifetime findings,
- documented failed experiments and corrections.

That is the primary reason to keep the runtime adapter conceptually smaller than the reverse-engineering knowledge it consumes.
