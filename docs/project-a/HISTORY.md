# Project A — Sanitized Milestone History

> This is the public development history. The private forensic log is much larger and contains raw logs, package hashes, local paths and private storage references that are intentionally not mirrored here.

Confidence language:

- **Observed** — directly demonstrated in code or live gameplay.
- **Strongly supported** — multiple independent observations agree.
- **Speculative** — plausible but not yet established.

---

## 2026-10-10 — Tooie map-resource architecture identified

Project A began by tracing Banjo-Tooie's static map-loading path.

Key findings:

- the current-map accessor and map configuration records were identified;
- major static world resources were traced through Tooie's resource manager;
- collision/grid structures showed a strong structural relationship to Banjo-Kazooie's public decompilation structures;
- a destructive Tooie-world resource substitution proved that the primary resource contains core static-world data.

This was the first indication that a BK→BT translation layer might be practical rather than requiring total format recreation.

---

## 2026-10-11 — Playable BK Spiral Mountain inside Tooie

BK Spiral Mountain primary/secondary world data was converted far enough to render and collide inside Tooie's playable Spiral Mountain host.

**Observed:**

- BK terrain and textures render through Tooie's renderer;
- imported collision supports ordinary movement;
- Tooie movement can interact with BK-only geometry;
- Tooie's Grip Grab worked on at least one BK-authored ledge;
- water traversal and bridge/fence interaction were demonstrated.

A major visual defect came from copied BK mesh/effect metadata being interpreted through Tooie's runtime update systems. Disabling incompatible metadata fixed moving/stretching bridge/fence geometry.

An apparent invisible wall near Gruntilda's Lair was later isolated to specific imported collision triangles and removed in a bounded compatibility test.

---

## 2026-10-11 to 2026-10-12 — Music format and first Lair import

BK compact-sequence music data was compared against Tooie's native sequence reader.

Important result:

- after header translation, BK sequence bodies could be consumed by Tooie's native event reader;
- many BK program/keymap/sample-metadata relationships correspond closely to Tooie's bank, although some important instruments differ.

The first Gruntilda's Lair room was extracted and converted.

**Observed live:** imported Lair terrain became playable inside Tooie's host map.

This also exposed the next generation of integration problems: allocation size, repeated loads, scene setup, unsupported corridors and correct transition/arrival ownership.

---

## 2026-10-12 — Ticker actor research begins

Rather than treating BK enemies as simple static models, Project A traced the relationship between BK and BT skeletal actor formats.

Findings included:

- Ticker model hierarchy and sparse bone IDs translate into Tooie's geometry traversal model surprisingly well;
- original BK Ticker animation streams can be consumed by Tooie's native animation functions;
- Tooie's native transform and matrix builders reproduce the expected BK animation poses under bounded verification;
- Tooie's actor factory, model cache and animation resource ownership paths were traced for later live integration.

This work became a reusable actor-research foundation rather than a one-off enemy hack.

---

## 2026-10-12 to 2026-10-13 — Multi-room Lair routing

A second and then third Gruntilda's Lair room were converted and hosted as logical rooms through Tooie's existing scene/map lifecycle.

Several important failures occurred here and remain useful design history.

### Failure: incomplete transition start

An early helper queued a destination but did not fully start the native transition lifecycle.

### Failure: wrong native transition wrapper reset Tooie's game state

A later wrapper successfully transitioned but used the game-reset path. This removed in-memory Tooie progression and demonstrated that successful visual map changes are not enough: the correct lifecycle flags matter.

The transition backend was changed to the state-preserving native path.

### Failure: arrival writes fought native scripted movement

Applying coordinates after load was insufficient because Tooie's own entrance movement retained ownership of its target.

### Fix: guest-address-width / native-boundary arrival ownership

A production-ABI addressing defect was discovered in indexed guest writes. After correction and moving placement ownership to the appropriate native movement boundary, the Lair arrival behavior was user-confirmed working.

This became the basis for later Project A room transitions.

---

## 2026-10-13 — Lair Room 3 water and climbing

The third Lair room gained its secondary/water geometry through a private resource path.

**Observed live:**

- water renders;
- swimming works;
- the CCW puzzle terrain is reachable.

The original BK vine was not automatically usable because BK setup climb nodes are not Tooie climb registrations. A scoped translation registered the vine into Tooie's native climbing system.

**Observed live:** the vine became climbable and usable as the intended escape route.

This is an important Project A pattern: preserve the authored geometry, but translate gameplay metadata into Tooie's corresponding native system.

---

## 2026-10-13 — Mumbo's Mountain exterior becomes playable

Mumbo's Mountain primary/secondary terrain was converted and connected to the imported Lair through Tooie's native transition system.

**Observed live:**

- stable exterior traversal;
- running/jumping/slopes;
- lake entry and underwater swimming;
- successful return routing to the Lair.

The dark/night presentation was accepted as an interesting abandoned Tooie-era interpretation rather than treated automatically as a defect.

Missing landmarks (exit pad, molehills, Conga's tree) were identified as separate actors/props rather than terrain-loss bugs.

---

## 2026-10-14 — Exit-pad resource work exposes cache/lifecycle hazards

Importing the BK world-exit-pad model caused severe scene corruption even when helper drawing was bypassed.

This proved that successful standalone conversion was not sufficient: loading a private resource at the wrong moment could disturb native cache/world initialization.

Follow-up work isolated timing and ownership hazards rather than masking the resulting renderer/collision faults.

Later relocation/cache handling was corrected, and the solid exit pad was visually confirmed in MM with a successful entry/return cycle.

Lesson retained for Project A platformization: imported resources need a common lifecycle layer, not per-feature ad hoc loads.

---

## 2026-10-14 — First live imported Ticker

**Observed live:**

- Ticker appears in-game;
- skeletal animation initially advances;
- Banjo collides with and can strike it;
- enemy contact damage works.

The first live version eventually stopped animating and could not die. The next accepted behavior target became:

- looping idle;
- normal contact-damage profile/cooldown;
- hurt animation;
- lethal damage/death/despawn;
- later movement/aggression.

The important milestone is that imported BK skeletal actors are no longer purely an offline theory.

---

## 2026-10-15 — Treasure Trove Cove exterior / Lair lobby

TTC exterior terrain and secondary water were connected to a Lair lobby through Project A's logical-room routing.

**Observed live:** repeated TTC ↔ lobby traversal.

Additional work restored or approximated important TTC presentation/gameplay pieces:

- ship-area scenery and climb registrations;
- flight/spring pads using Tooie's native actors;
- feather nests;
- an adapted sky;
- imported world-exit behavior.

### Water failure

Converted BK water disappeared in first person and in several camera/player states. Firing an egg could temporarily restore it.

Rather than continuing to patch symptoms, Project A replaced the water rendering/material setup with Tooie's native Jolly Roger's Lagoon water path while preserving TTC's surface intent.

**Observed live:** the disappearing-water behavior was resolved across the requested first-person, underwater, climbing, high-flight and egg tests.

The exact single original rendering-state defect remains unclaimed.

---

## 2026-10-16 — TTC host-exit and Clockwork transition policy

An inherited/native host transition inside TTC could unexpectedly send the player to Spiral Mountain.

A first late-stage destination guard stopped the map request but left camera ownership in a bad state, producing a live failure.

The correction moved the rejection earlier to the native setup/section dispatch boundary.

Clockwork Kazooie also exposed a design rule: Project A transitions should not transport the remote Clockwork state or leave stationary Banjo behind.

A Lair-wide policy was added to block Project A travel during active Clockwork control while preserving normal Banjo travel.

**Observed live:** the revised exit behavior passed.

---

## 2026-10-16 to 2026-10-17 — BK music integration

A first broad custom-music implementation destabilized transitions because its ownership/lifetime model did not match Tooie's native audio lifecycle.

It was withdrawn and native audio restored before continuing.

A later approach kept Tooie's native sequence asset identity/cache ownership and staged larger BK-derived data through the native loader. Live testing exposed another race: the native music controller could consider playback stopped and cancel an in-flight logical-room restart.

That controller ordering was reproduced and a scoped hold was implemented.

**Observed live by 2026-10-17:** automatic TTC/Lair-lobby music entry switching works.

Still pending:

- MM and first-Lair-room final integration;
- cross-map phase continuity;
- underwater/positional channel mixes;
- faithful handling of unmatched BK instruments such as TTC's steelpan.

---

## 2026-10-17 to 2026-10-18 — Project A.1 becomes a structured expansion concept

With world loading, routing, water, actor research and audio all substantially de-risked, the project scope was split deliberately:

- **Project A:** compatibility/platform work;
- **Project A.1:** an optional expansion campaign built on that platform.

A.1's current design pillars are:

- Tooie's existing Cheato Pages gate deeper Lair access;
- Grey Jinjo survivors create a recurring rescue objective;
- compact BK-world visits are remixed around Tooie mechanics rather than recreating BK;
- Lair-only fast travel reduces hub friction;
- limited backtracking is allowed when clearly signposted;
- existing moves are upgraded into Advanced Techniques.

Current flagship technique concepts:

- Rapid Fire;
- Drill Barge;
- Padless Flight;
- Free Split Anywhere as the 25-Page completion reward.

The production roadmap now prioritizes a stable Project A baseline, reusable world/actor infrastructure, persistent A.1 state and a complete Mumbo's Mountain vertical slice before broad campaign expansion.

See [README.md](README.md), [ROADMAP.md](ROADMAP.md) and [A1_CONCEPT.md](A1_CONCEPT.md).
