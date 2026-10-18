# Project A — Banjo-Kazooie content in Banjo-Tooie

> **Status:** active experimental development  
> **Last synchronized:** 2026-10-18

Project A is an experimental compatibility layer for running selected **Banjo-Kazooie** world content inside the **Banjo-Tooie** recompilation/runtime.

The long-term goal is not to replace Banjo-Tooie with Banjo-Kazooie. It is to understand how the two games' world, collision, actor, animation, audio, camera and transition systems relate closely enough that BK content can be translated forward and then used as the basis for new Tooie-era gameplay.

Project A.1 is the proposed gameplay expansion built on top of that compatibility layer. See [A1_CONCEPT.md](A1_CONCEPT.md).

## Evidence standard

Project A documentation uses three confidence levels:

1. **Observed** — directly demonstrated in code or a live game run.
2. **Strongly supported** — multiple independent observations agree.
3. **Speculative** — plausible design or implementation direction that has not yet been established.

A successful offline harness is not described as a successful gameplay feature until it has been tested in the actual game.

## Current live progress

### World / terrain integration

**Observed:**

- BK Spiral Mountain terrain has been made playable inside Tooie's engine.
- Multiple Gruntilda's Lair rooms have been imported and connected through Tooie's native transition lifecycle.
- State-preserving room transitions have been demonstrated without intentionally resetting the Tooie game state.
- Mumbo's Mountain exterior is playable and has been traversed with ordinary movement and swimming.
- Treasure Trove Cove exterior and its Lair lobby can be entered and exited repeatedly.
- Lair Room 3 water/swimming and a BK vine translated into Tooie's climb system have been demonstrated.
- BK terrain collision structures are close enough to Tooie's corresponding structures that large portions can be reused after bounded compatibility work.

Project A does **not** yet claim that every BK world is imported, nor that every imported map is content-complete.

### TTC water

The first converted BK water surface was unstable under some camera/player states. A replacement based on Tooie's native Jolly Roger's Lagoon water rendering/material path resolved the disappearing-water behavior in live testing while preserving the intended TTC water surface/collision.

The exact original rendering-state defect was not isolated to one register or command; the working solution replaces the problematic rendering setup rather than claiming a single proven root cause.

### Transitions and arrivals

Project A now routes imported logical rooms through Tooie's native map-transition lifecycle rather than implementing a parallel scene system.

A major early bug used the wrong transition path and reset Tooie's game state. That path was removed. Later work corrected guest-address-width handling in the arrival code and consolidated arrival ownership around Tooie's native movement/controller boundary.

This history is intentionally retained because it explains why current transition code is conservative about state ownership and lifecycle.

### Imported actors

Ticker research has progressed beyond static model conversion.

**Observed live:**

- imported Ticker model appears in-game;
- skeletal animation begins correctly;
- Banjo can collide with and strike the actor;
- traditional enemy contact damage occurs.

**Still required for a reusable enemy pipeline:**

- robust looping animation;
- normal aggression/movement;
- hurt reaction;
- lethal damage/death/despawn;
- generalized actor registration and ownership suitable for additional BK enemies.

The Ticker work has also produced reusable knowledge about BK/BT skeleton hierarchy, sparse bone IDs, animation streams, matrix construction and native actor resource ownership.

### Music

BK music sequences have been decoded and translated far enough to be consumed by Tooie's native sequence reader.

**Observed live:**

- automatic TTC/Lair-lobby music switching now works in the current development line.

**Still open:**

- Mumbo's Mountain / first-Lair-room integration is being finalized;
- original BK cross-map musical phase continuity is not yet reproduced;
- positional channel mixes and underwater arrangements remain incomplete;
- several BK instruments do not map perfectly onto Tooie's existing bank, so faithful instrument import/substitution remains later work.

### Camera / presentation

A preferred TTC entry camera has been retained. A separate Lair camera-zoom regression currently cycles close → medium → close instead of exposing the expected farther third step. This is nonfatal and is tracked separately from world integration.

### Current active integration priorities

1. finish the current MM music / Lair doorway coverage pass;
2. decide whether the Lair camera zoom regression is fixed now or explicitly parked;
3. finish a complete killable Ticker lifecycle;
4. freeze one canonical Project A gameplay baseline;
5. consolidate the current one-off integration code into a reusable data-driven Project A layer;
6. add persistent Project A.1 state;
7. build Mumbo's Mountain as the first complete A.1 vertical slice.

See [ROADMAP.md](ROADMAP.md) for the production plan.

## What Project A.1 is

Project A.1 is a proposed optional expansion campaign that uses imported BK areas as compact Tooie-era challenge spaces rather than recreating the original BK campaign.

The current design direction includes:

- existing Tooie Cheato Pages as the Lair-progression currency;
- surviving Grey Jinjos hidden through BK areas;
- bonus Jiggies;
- remixed encounters using imported and native enemies;
- limited, clearly signposted backtracking;
- Lair-only fast travel replacing the role of BK's Cauldrons;
- Advanced Techniques that upgrade existing Tooie moves instead of creating an entirely separate move set.

Current flagship move concepts:

- **Rapid Fire** — deliberate high-rate egg/grenade firing;
- **Drill Barge** — a horizontal, combat-focused evolution of Beak Barge using Bill Drill-style spinning language;
- **Padless Flight** — field flight using Red Feathers as fuel, paired with FALLPROOF so running out of fuel can drop Banjo and Kazooie without immediately killing them;
- **Free Split** — a 25-Page completion reward allowing split-up without a pad outside blacklisted unsafe/boss/script contexts.

See [A1_CONCEPT.md](A1_CONCEPT.md) for the working design.

## Public repository policy

This repository must not become a distribution point for Nintendo/Rare game data.

Project A's intended public packaging model is:

1. user supplies their own supported Banjo-Tooie ROM;
2. user supplies their own supported Banjo-Kazooie ROM;
3. Project A verifies the ROM revisions;
4. Project A locally extracts/converts only the assets required by the mod;
5. generated ROM-derived assets remain local and are not committed to GitHub.

Publicly appropriate material includes Project A source, converters, manifests, tests, documentation and installer code.

Do **not** commit ROMs, extracted music, textures, models, collision payloads, converted game assets, save files or private development captures.

## Internal vs public logs

The development project maintains a much larger forensic log containing exact package hashes, local paths, private storage identifiers, raw test references and superseded experiments.

That internal log is intentionally **not** mirrored verbatim here.

Public history should be curated into reproducible technical notes that preserve:

- the question being investigated;
- the observed evidence;
- failed approaches when they teach something important;
- the final implementation direction;
- remaining uncertainty.

Raw multi-megabyte stderr logs, memory captures and temporary packages belong in the private development archive unless they are specifically needed to reproduce a public issue.
