# Project A — Runtime Adapter Audit

This document separates **Project A's game-format research** from the **current BanjoTooieRecompiled injection prototype**.

That distinction matters because upstream recomp changes may invalidate hook points or memory assumptions without invalidating the BK↔BT conversion findings.

## Current public-branch prototype

At the time of this audit, Project A runtime injection code is embedded directly in `src/recomp_api.cpp`, primarily inside the general `tooie_probe` diagnostic path.

The committed prototype includes behavior such as:

- hard-coded candidate paths under `research/project-a/bt-candidates/`,
- hard-coded expected candidate sizes,
- direct byte copies into guest RDRAM,
- a secondary-model scratch address computed as `resA_asset + 0x60000`,
- process-lifetime `static bool` guards for one-shot injection attempts,
- map/resource conditions mixed into the generic probe handler.

These choices were useful for proving feasibility quickly. They are **not** the desired long-term Project A architecture.

The public branch can also lag the newest verified local experiment, so this document describes the committed prototype rather than claiming it is the latest working runtime state.

## Why this layer is fragile

### 1. Allocation ownership

A pointer being inside RDRAM does not establish that enough memory is owned by the loaded resource.

The primary proof-of-concept currently copies candidate bytes at the address returned by the native load path. For larger imports, capacity must be established or a correctly sized owned allocation must be supplied.

### 2. Secondary scratch placement

`resA + 0x60000` was an expedient experimental location for the Spiral Mountain secondary model. An RDRAM-bounds check proves only that the address is inside RDRAM; it does not prove the region is unowned or safe for the required lifetime.

### 3. Lifecycle coupling

One-shot `static bool` guards are incompatible with a robust map unload/reload lifecycle. Newer local experiments have already moved toward per-load reset behavior, but the public prototype should not be treated as the final lifecycle design.

### 4. Probe/runtime mixing

Diagnostic probes and actual compatibility-layer behavior currently share a large source file. This makes it harder to distinguish:

- instrumentation,
- experimental patches,
- durable runtime behavior,
- generic recomp infrastructure.

### 5. Upstream sensitivity

Changes to any of the following may break this layer:

- generated-function ABI,
- hook/patch locations,
- RDRAM helper conventions,
- asset-loader/cache behavior,
- recomp memory-management facilities,
- overlay or syscall implementation details.

None of those changes automatically invalidate the model/collision/music research.

## Target architecture

The desired boundary is:

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

Only the bottom two boxes should need significant work when the recomp backend changes.

## Recommended source split

A future no-behavior-change cleanup should move Project A-specific runtime code out of `recomp_api.cpp` into a small adapter module, for example:

```text
src/project_a/
├── project_a_runtime.cpp
├── project_a_runtime.hpp
├── project_a_assets.cpp
└── project_a_state.hpp
```

Suggested responsibilities:

### `project_a_assets`

- load local candidate files,
- validate expected size/hash/manifest,
- perform no map-specific injection by itself.

### `project_a_state`

- requested mode,
- active/verified mode,
- current map/resource identity,
- per-load injection status,
- owned primary/secondary allocation handles once established.

### `project_a_runtime`

- receive narrow events from the recomp/backend layer,
- decide whether a Project A replacement applies,
- request/own correctly sized memory,
- perform replacement,
- reset state on unload/reload.

### `recomp_api.cpp`

Should eventually know as little as possible about BK asset IDs, candidate filenames, or Project A-specific policy.

## Refactor rule

Do **not** combine this architectural cleanup with new memory-allocation behavior in the same experiment.

First perform a behavior-preserving extraction of the existing prototype behind a narrow interface. Verify that the same known Spiral Mountain test still behaves identically. Only then change allocation/cache behavior.

That gives us a clean control and makes future upstream migration far less ambiguous.

## Minimum adapter contract to aim for

Conceptually, the runtime backend should only need to provide events/capabilities such as:

```text
on_world_resource_request(map_id, resource_id, native_ptr, native_capacity?)
on_world_resource_loaded(...)
on_map_unload(map_id)
allocate_guest_bytes(size, alignment)
release_guest_bytes(handle)
```

The exact API is not established yet. This is a design target, not a claim about facilities the current recomp already provides.

## Next runtime experiments

Highest value:

1. Trace ownership/capacity around the native primary loader and its caller-supplied destination path.
2. Establish which cache layer can bypass the loader on repeat visits.
3. Tie replacement state to map-resource load lifetime rather than process lifetime.
4. Only after those are understood, replace scratch placement with owned allocations.
5. Then test the larger BK lair primary and separate translucent model.

## What survives an upstream rewrite

Even if every current hook in `recomp_api.cpp` becomes unusable, these Project A outputs should remain valid unless separately disproven:

- BK model extraction/inspection tooling,
- BK→BT model conversion findings,
- vertex/collision structural correspondence,
- display-list translation findings,
- exact lair geometry comparison,
- compact-sequence format comparison,
- documented failed experiments and corrections.

That is the primary reason to keep the runtime adapter intentionally small.
