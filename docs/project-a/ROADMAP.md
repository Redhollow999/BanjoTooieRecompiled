# Project A / A.1 — Production Roadmap

> **Planning baseline:** 2026-10-18  
> Ranges below are focused engineering/design hours, not promised dates.

Project A has moved far enough beyond a terrain-import proof that future work should be organized as a production project rather than as a sequence of isolated experiments.

## Product split

### Project A — platform

The technical compatibility layer:

- BK terrain/assets loaded inside BT;
- imported-room routing and scene lifecycle;
- collision/water/props;
- actor/model/animation translation;
- audio/camera integration;
- persistent mod state;
- owner-ROM extraction/conversion;
- public packaging.

### Project A.1 — game

The expansion built on that platform:

- Cheato Page-gated Gruntilda's Lair expansion;
- surviving Grey Jinjos;
- bonus Jiggies;
- remixed BK encounters;
- moderate backtracking;
- Lair fast travel;
- Rapid Fire, Drill Barge, Padless Flight and Free Split.

### Post-1.0 candidates

Do not make A.1 v1.0 depend on:

- Bottles' Revenge;
- Stop 'n' Swop → Project C integration;
- drone-Kazooie flight;
- a large suite of entirely new moves;
- extensive bespoke bosses.

Those can become later modules if A.1 reaches a stable 1.0.

---

# Workstreams

## W1 — World integration

Terrain, secondary geometry, collision, water, entrances, routing, arrivals, camera, titles and scene lifecycle.

## W2 — Actor integration

Imported models, animation, matrices, AI, collision, damage, death, drops, ownership and cleanup.

## W3 — Audio / presentation

Music, positional arrangements, underwater mixes, phase continuity, camera behavior, HUD and environment presentation.

## W4 — Progression / save

Cheato milestones, Grey Jinjos, A.1 Jiggies, gates, move unlocks, warp activation and persistence.

## W5 — Advanced Techniques

Rapid Fire, Drill Barge, Padless Flight, Free Split and only the small support mechanics required by those moves.

## W6 — Campaign content

Dialogue, encounters, Jinjo placement, compact world remixes, controlled backtracking, rewards and balancing.

## W7 — Release engineering

Repository structure, deterministic build, ROM verification/extraction, installer, version compatibility, rollback, diagnostics and documentation.

---

# Milestones

## P0 — Stabilize and freeze the current Project A baseline

**Estimate:** 20–45 focused hours

Work:

- finish the active MM music / Lair doorway integration pass;
- fix or explicitly park the Lair far-camera zoom regression;
- finish a complete Ticker enemy lifecycle: loop, aggression/contact damage, hurt, lethal hit and despawn;
- verify inventory / learned-move / save preservation through representative imported routes;
- establish one canonical runtime/source checkpoint.

**Exit gate:** a cold-launch regression route can traverse representative imported areas, kill an imported Ticker, return to normal BT content, save/reload and preserve progression without a repeatable crash or state reset.

---

## P1 — Turn Project A into a reusable platform

**Estimate:** 30–70 focused hours

Create a data-driven room/world definition layer. A simple imported area should be describable primarily through data such as:

- logical room ID;
- source BK assets;
- private BT resource IDs;
- primary/secondary geometry;
- collision/water policy;
- entrances/exits;
- arrival XYZ/yaw;
- title/music identity;
- props/actors;
- compatibility flags.

Consolidate common implementations for:

- private resource loading;
- scene ownership/release;
- native transition queueing;
- arrival control;
- imported actor ownership;
- shared diagnostics.

**Exit gate:** adding one previously unintegrated simple BK room should mostly require asset conversion plus a manifest/definition, not another bespoke patch across many generated C files.

---

## P2 — Persistence and A.1 progression framework

**Estimate:** 20–45 focused hours

Persistent A.1 state should cover:

- Page milestones 1 / 5 / 10 / 15 / 20 / 25;
- Lair gate state;
- Grey Jinjos rescued per area;
- A.1 Jiggies awarded;
- Advanced Technique unlock flags;
- Lair warp nodes;
- one-time dialogue/event flags;
- optional shortcut flags.

The state format should be versioned so later updates can migrate it safely.

**Exit gate:** earn a test flag, quit the application entirely, relaunch, load the same save and recover the exact A.1 state without altering unrelated BT progress.

---

## P3 — A.1 vertical slice: Mumbo's Mountain

**Estimate:** 30–65 focused hours after P0–P2

Complete the whole A.1 loop rather than simply making MM prettier:

1. collect the first Spiral Mountain Cheato Page;
2. Cheato activates the sidequest;
3. the MM obstruction is removed;
4. enter MM;
5. discover battered Grey Jinjos;
6. fight enhanced Tickers;
7. rescue the required Jinjos;
8. receive a bonus Jiggy;
9. report back / advance Cheato's dialogue;
10. save/reload and retain completion.

Systems proven here:

- quest dialogue;
- persistent gate state;
- Grey Jinjo collectible logic;
- imported enemy combat;
- bonus Jiggy award;
- compact remixed BK-world pacing;
- clean return to Tooie.

**Exit gate:** someone who did not build Project A can complete the whole MM sidequest without developer commands.

This is the preferred first public-quality A.1 demonstration.

---

## P4 — Campaign skeleton / Lair hub

**Estimate:** 30–65 focused hours

Before fully decorating every world:

- make the intended Lair rooms traversable;
- establish world entrances;
- install Page-threshold Cheato obstacles;
- implement Cheato projections;
- implement Lair-only fast travel;
- enable fast travel around the 10-Page milestone;
- clearly block future content that is not yet reachable.

Later BK worlds may still contain placeholder/minimal content at this stage.

**Exit gate:** a developer save can advance through every intended Page threshold and legitimately reach every planned BK world without manual room commands.

---

## P5 — Advanced Technique framework

**Estimate:** 35–80 focused hours total, developed alongside content that needs the moves.

### Rapid Fire

- deliberate activation;
- normal aiming + Breegull Blaster compatibility;
- faster egg/grenade cadence;
- sensible ammunition behavior;
- no accidental activation.

### Drill Barge

Upgrade **Beak Barge** into a horizontal combat drill:

- reuse Bill Drill visual/spin language where practical;
- Kazooie's head rotates through the charge;
- forward-moving damage volume;
- high combat damage;
- Bill Drill remains the downward puzzle/platforming tool.

### Padless Flight

- Z + double-tap A from valid ground;
- field flight consumes Red Feathers;
- pad flight remains superior;
- reaching zero feathers ends powered flight and drops the duo;
- campaign unlock paired with FALLPROOF;
- supports the planned early/late Clanker's Cavern loop.

### Free Split

- 25-Page completion reward;
- split without a pad;
- blacklisted only in unsafe boss/script contexts;
- sequence breaks are acceptable unless they can softlock or corrupt progression.

**Exit gate:** every technique has a persistent unlock, safe death/map-transition behavior, ordinary BT regression coverage and at least one A.1 challenge that meaningfully uses it.

---

# Content waves

After P1–P4 are stable, world content can be produced in waves. A rough planning assumption is **10–25 focused hours per BK world** once common systems are reusable, with outliers for unusually complex areas.

## Wave A — early expansion

### Mumbo's Mountain

P3 vertical slice.

### Treasure Trove Cove

- compact ranged/combat remix;
- Grey Jinjos;
- groundwork for later Rapid Fire interactions.

### Clanker's Cavern — first visit

- Clanker has been scrapped;
- meaningful lower/reachable content;
- visible inaccessible upper Jinjo objectives;
- Jamjars explicitly tells the player he needs time to solve the traversal problem.

This is the model for moderate, signposted backtracking.

## Wave B — midgame

### Bubblegloop Swamp

Movement/hazard combat; candidate Drill Barge encounter space.

### Freezeezy Peak

Lighter character/story visit, including the proposed Biggafoot continuity gag after Hailfire Peaks.

### Gobi's Valley

Breegull Blaster pyramid/maze challenge.

### Clanker's Cavern — return

After FALLPROOF, Jamjars teaches Padless Flight and the upper Grey Jinjo objectives become reachable.

## Wave C — late game

### Mad Monster Mansion

Horror-flavored compact remix with solo-character/split-style ideas, but not unrestricted Free Split yet.

### Rusty Bucket Bay

Industrial combat/traversal, Drill Barge opportunities and an optional RBB → JRL one-way connection if transition work remains stable.

## Wave D — mastery

### Click Clock Wood

Final BK-world challenge combining multiple A.1 techniques. Optional CCW → CCL route if it proves fun and safe.

### 25 Pages

- retain JUKEBOX, ideally with locally extracted BK music if practical;
- unlock Free Split Anywhere;
- completion dialogue/reward presentation.

---

## P6 — Content-complete balance pass

**Estimate:** 25–60 focused hours

Lock and tune:

- real Page accessibility / anti-circular progression;
- Grey Jinjo placements;
- enemy HP/damage;
- Padless Flight fuel rate;
- Drill Barge damage and hitbox;
- Jiggy totals / late-game requirements;
- intended sequence breaks;
- softlock prevention;
- amount of backtracking;
- dialogue and presentation.

**Exit gate:** one clean save can complete the intended BT + A.1 progression through the 25-Page / proposed 100-Jiggy target without developer intervention.

---

## P7 — Public packaging

**Estimate:** 30–65 focused hours

Target end-user flow:

1. download `Project-A-Setup.exe`;
2. select a supported BT ROM;
3. select a supported BK USA 1.0 ROM;
4. installer verifies hashes;
5. installer verifies/obtains the supported BTRecomp base;
6. required BK assets are extracted/converted locally;
7. Project A/A.1 code and locally generated data are installed;
8. Play.

The repository may contain Project A source, converters, manifests, installer code, tests, docs and hashes. ROMs and ROM-derived asset payloads must remain local.

**Exit gate:** successful fresh-machine installation by someone who did not develop the project.

---

## P8 — Beta / release candidate

**Estimate:** 40–90 focused hours

Regression matrix should include:

- fresh save;
- existing midgame save;
- every Page threshold;
- every A.1 world entry/exit;
- death in imported areas;
- save/quit/reload in imported areas;
- clockwork restrictions;
- transformations;
- boss arenas;
- Free Split blacklist;
- all Advanced Techniques;
- cheat-code interaction vs true collected-Page milestones;
- fast travel;
- one-way shortcuts;
- Jiggy totals / final progression;
- pause/menu/game-over;
- long sessions with repeated world switching;
- audio transitions;
- camera / first person;
- installer/update/rollback.

**Exit gate:** no known progression-loss, save-corruption, repeatable crash or campaign-blocking bug.

---

# Scope estimate from the current state

These are planning ranges, not a measured completion percentage:

| Category | Focused hours |
|---|---:|
| Stabilize + platformize Project A | 50–115 |
| Persistence/progression + MM vertical slice | 50–110 |
| Campaign hub + Advanced Techniques | 65–145 |
| Remaining world content | 105–250 |
| Balance/polish | 25–60 |
| Packaging + beta QA | 70–155 |
| **Total rough remaining range** | **365–835** |

A first public A.1 vertical-slice alpha (MM quest rather than the full campaign) is deliberately targeted much earlier: approximately **100–225 focused hours** from the current planning baseline.

Do not convert these figures into promised calendar dates.

---

# Development discipline

## One active gameplay baseline

Only one package/runtime is the current integration baseline.

## Separate research branches

Actor, audio, move and packaging research may happen separately, but each merges only after its exit gate.

## Every milestone should have

- immutable pre-change checkpoint;
- exact hashes;
- reversible installation/patching;
- focused regression coverage;
- durable documentation;
- explicit Observed / Strongly supported / Speculative classification where relevant.

## Feature-freeze rule

Once full campaign content production is underway, a new idea does not automatically enter v1.0.

A new feature belongs in v1.0 only if it materially improves the agreed campaign, has a bounded implementation path and does not threaten the next exit gate. Otherwise it belongs in post-1.0 work.
