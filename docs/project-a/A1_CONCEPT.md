# Project A.1 — Gruntilda's Lair Expansion Concept

> **Status:** design candidate / optional follow-on to Project A  
> **Last synchronized:** 2026-10-18

Project A.1 is the proposed game built on top of Project A's BK-in-BT compatibility work.

It is **not** intended to recreate Banjo-Kazooie inside Banjo-Tooie. Imported BK worlds should act as compact, remixed challenge spaces visited during a normal Tooie playthrough.

Target loop:

> Play Tooie → recover Cheato Pages → return to Gruntilda's Lair → Cheato opens deeper BK territory → rescue surviving Grey Jinjos / clear remixed encounters → earn Jiggies and advanced versions of existing techniques.

Each BK world should ideally contain at least one interaction that could not have happened in the original BK.

---

## Cheato as the progression spine

Tooie's existing Cheato Pages remain in their original locations. A.1 gives them a second purpose: restoring Cheato's magic so he can remove barriers inside Gruntilda's Lair.

Working progression:

| Pages | A.1 consequence |
|---:|---|
| **1** | Open Mumbo's Mountain / begin Grey Jinjo sidequest |
| **5** | Open the first larger Lair tranche |
| **10** | Open the next tranche; activate Lair fast travel; Rapid Fire milestone candidate |
| **15** | FALLPROOF-era tranche; Padless Flight milestone candidate |
| **20** | Final major Lair/world access |
| **25** | Completion rewards; Free Split Anywhere |

Exact thresholds remain provisional until every required Page is checked against Tooie's real ability/progression dependencies.

### Opening setup

1. Banjo collects the first Spiral Mountain Cheato Page.
2. Cheato explains that his restored magic is reacting to Grunty's old Lair.
3. Cheato removes the rocks blocking Mumbo's Mountain.
4. Kazooie questions why reopening an old world is useful.
5. Cheato says he can faintly sense Jinjo magic inside.
6. Banjo finds battered surviving Grey Jinjos and empowered Tickers.
7. After the rescue, Cheato says he can sense more survivors deeper in the Lair but needs more Pages to break the remaining seals.

Cheato's existing/provisional presence in multiple imported Lair rooms can be reframed as **magical projections** rather than treated as a defect.

The entrance Cheato remains the normal cheat-unlock location. Projections can handle A.1 progression, hints and presentation.

---

## Cheato reward synergy

A.1 should reuse Tooie's existing five-Page rhythm rather than create a second invisible progression ladder.

| Pages | Vanilla BT reward | A.1 synergy |
|---:|---|---|
| 5 | **FEATHERS** | Larger feather reserve becomes future Padless Flight fuel reserve |
| 10 | **EGGS** | Natural point for Rapid Fire / advanced egg handling; activate Lair fast travel |
| 15 | **FALLPROOF** | Preferred Padless Flight pairing; fuel failure can drop the duo without making the new move a death trap |
| 20 | **HONEYBACK** | Strong survival reward before final mastery content; no extra move required |
| 25 | **JUKEBOX** | Keep it, ideally expanded with BK music, but add the real completion prize: Free Split Anywhere |

A.1 milestone state should be based on **Pages actually collected**, not merely on whether a vanilla cheat code is active.

---

## Grey Jinjos

The Grey Jinjo family was believed destroyed in Tooie, but A.1 reveals scattered survivors.

Working structure:

- roughly 3 Grey Jinjos per BK area;
- rescuing a full area's group awards 1 bonus Jiggy;
- target approximately 10 A.1 Jiggies total, potentially bringing Tooie's 90 to 100;
- exact total and final-game requirements are not locked until save/UI/Jiggy handling is audited.

Grey Jinjos are the recurring connective objective. Everything around them should vary so the expansion does not become formulaic.

---

# Advanced Technique philosophy

Prefer upgraded versions of existing Tooie mechanics over entirely new player-state architectures.

Lore explanation: Jamjars' military techniques are being magically enhanced through Cheato's restored power.

Design rule:

> Pads provide the strong / intended version. Advanced training can provide a weaker portable version.

## Rapid Fire

Inspired by existing Tooie behavior where grenade eggs can be made to fire at blue-egg-like cadence.

Candidate behavior:

- deliberate double-tap / activation while egg aiming or in Breegull Blaster;
- accelerated egg/grenade firing;
- useful against tougher A.1 encounters;
- ammo economy remains meaningful.

## Drill Barge

Upgrade to **Beak Barge**.

Identity:

- horizontal Bill Drill-like combat technique;
- reuse Bill Drill spinning visual/animation pieces where practical;
- Kazooie's head rotates through Banjo's forward charge;
- damaging hitbox moves horizontally with the attack;
- significantly higher combat damage than ordinary Beak Barge;
- Bill Drill remains the downward puzzle/platforming/breaker move.

The two moves should not fully replace one another. Drill Barge is the combat drill; Bill Drill is the utility drill.

## Padless Flight

Preferred milestone: **15 Pages / FALLPROOF**.

Input candidate:

> Hold Z, double-tap A from valid ground.

Preferred paired-flight version:

- Banjo + Kazooie enter field flight together;
- Red Feathers act as fuel;
- Pad flight remains more efficient / superior;
- when the feather supply reaches zero, powered flight ends immediately and the duo falls;
- FALLPROOF makes fuel failure funny and survivable;
- no direct launch from swimming.

Exact feather drain/range should be tuned against actual BK geometry rather than locked on paper.

### Alternate drone-Kazooie prototype

Possible later variant:

- Kazooie leaves Banjo's backpack;
- player controls her in independent flight for a limited duration;
- she automatically returns to Banjo when the timer/fuel expires.

This is deliberately **not** the preferred first implementation because it requires control/camera ownership transfer, independent collision and forced reunification. Keep it as an optional later prototype.

## Free Split Anywhere

Preferred **25-Page completion reward**.

- Banjo and Kazooie may split without a Split-Up Pad;
- disable only in blacklisted boss arenas or other scripted states proven unsafe;
- sequence breaks are allowed unless they softlock or corrupt progression.

This is intentionally powerful because it arrives after the core A.1 campaign is complete.

---

# Moderate backtracking, not extreme backtracking

A.1 does not need to be strictly linear.

Acceptable backtracking:

- a world can be entered before every objective is completable;
- the player should clearly understand *why* something is currently unreachable;
- the first visit must still contain meaningful exploration, encounters or rewards;
- later abilities should make the return feel like payoff rather than cleanup;
- use a small number of memorable dependencies, not dense Tooie-style chains across every world.

## Clanker's Cavern reference case

CC can open early.

Clanker is gone, having been sent to the scrapyard, so the original giant mechanical stepping-stone/routes no longer exist. Lower/reachable content can be completed, while upper Jinjos remain visible but inaccessible.

### Locked early-visit dialogue

**Jamjars:** "I think we've located the Jinjos, unfortunately the ground is too unstable for me to install silos and flight pads."

**Banjo:** "Flight pads? Isn't it all mostly under water?"

**Jamjars:** "Gruntilda had Clanker sent to the scrap yard, so we can't access the higher levels anymore. Come find me later, I'll figure something out by then."

Later, after FALLPROOF, Jamjars teaches Padless Flight.

### Locked Padless Flight lesson

**Jamjars:** "Alright you filthy maggots, here's the plan! We'll have birdbrain fly from where you stand! Press and hold Z, then double tap A. You'll reach those Jinjos and save the day!"

**Kazooie:** "Wait... you mean I can fly from wherever?!"

**Jamjars:** "Hold your horses, you runt. You won't be able to fly as efficiently as you can on a pad. But with this pad flight should be even easier! DISMISSED!"

The exact limits should be learned through play rather than a long tutorial.

---

# Lair fast travel

Do **not** put warp pads throughout the BK worlds by default.

The BK worlds are compact and should generally take around 10–15 minutes of A.1 exploration/encounters rather than being converted into large backtracking hubs.

Fast travel belongs in **Gruntilda's Lair**.

Preferred options:

1. reuse/repurpose Tooie's silo/warp-pad presentation and route through Project A logical-room transitions;
2. if native silo behavior is awkward to extend, use an A.1-specific pad/menu backed by the same routing layer;
3. Cheato projections remain a fallback presentation mechanism, but they do not have to become the primary taxis.

Fast travel should arrive around the **10-Page milestone**, when enough Lair territory exists for repeated traversal to become irritating.

Do not save fast travel for 25 Pages; by then most of the BK expansion is already complete.

---

# Possible one-way BK → BT connections

Keep these rare so world topology still matters.

Candidate shortcuts:

### Click Clock Wood → Cloud Cuckooland

Reach a high cloud trigger using Padless Flight / late mobility and transition one-way into CCL.

### Rusty Bucket Bay → Jolly Roger's Lagoon

Use the open harbor/ocean boundary as an optional one-way connection into JRL.

These are optional late conveniences/secrets, not mandatory progression paths.

---

# Working world concepts

| Area | Core idea | Candidate reward / mechanic |
|---|---|---|
| Spiral Mountain | A.1 prologue | First Page points back to the Lair |
| Mumbo's Mountain | Grey Jinjo tutorial; empowered Tickers | First complete A.1 vertical slice |
| Treasure Trove Cove | Ranged/combat remix | Rapid Fire setup / combat challenge |
| Clanker's Cavern | Early partial visit; Clanker removed; later return | Main Padless Flight payoff |
| Bubblegloop Swamp | Hazard / movement combat | Drill Barge candidate encounter space |
| Freezeezy Peak | Character/event-driven visit | Biggafoot continuity gag after Hailfire Peaks |
| Gobi's Valley | Pyramid/trap remix | Breegull Blaster challenge |
| Mad Monster Mansion | Horror-flavored compact remix | Solo/split-style puzzles without unrestricted Free Split yet |
| Rusty Bucket Bay | Industrial combat/traversal | Drill Barge use; optional JRL shortcut |
| Click Clock Wood | Mastery challenge | Multiple Advanced Techniques; optional CCL shortcut |
| Gruntilda's Lair | Expansion hub | Cheato gates, warp network, Grey Jinjo story |

Not every world needs a new move. Rewards can instead be Jiggies, story beats, shortcuts, unusual encounters or completion progress.

---

# Enemy / mini-boss philosophy

Avoid nine bespoke bosses unless tooling later makes that cheap.

Preferred approach:

- reuse existing actors;
- alter HP/aggression/placement when safe;
- combine enemies with arena scripting/restrictions;
- use Cheato magic as the lore explanation for abnormal strength/behavior.

Mumbo's Mountain reference encounter:

- roughly five empowered Tickers;
- increased survivability/aggression;
- staged or synchronized encounter;
- guarding or surrounding the Grey Jinjo objective.

Later worlds should escalate through encounter design before demanding entirely new boss architectures.

---

# Completion / legacy features

These are attractive **post-1.0 or bonus-mode candidates**, not core A.1 dependencies:

- Bottles' Revenge restoration/polish;
- Stop 'n' Swop-inspired connection to Project C;
- seamless launcher/runtime switching between Project A and Project C once both architectures actually exist;
- drone-Kazooie flight;
- additional portable pad techniques.

The v1.0 scope should remain finishable before any of these are promoted.

---

# Distribution goal

A.1 should ultimately be installable without redistributing copyrighted game data.

Ideal public flow:

1. user installs/runs Project A setup;
2. selects their own supported Banjo-Tooie ROM;
3. selects their own supported Banjo-Kazooie USA 1.0 ROM;
4. installer verifies both;
5. required BK content is extracted/converted locally;
6. Project A/A.1 code and generated local data are installed;
7. Play.

The repository may contain our source, tools, manifests, documentation and tests. ROM-derived models, textures, music, collision data and other copyrighted payloads must not be committed.
