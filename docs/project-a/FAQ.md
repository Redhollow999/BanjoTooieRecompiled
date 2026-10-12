# Project A — FAQ

## What is Project A?

Project A is an experimental reverse-engineering effort asking how much Banjo-Kazooie data can be translated into structures Banjo-Tooie understands, with the current BT recompilation serving as a convenient runtime test bed.

It is not currently a finished mod, release, or promise that all of BK will run inside BT.

## What has actually been demonstrated?

The strongest public proof-of-concept so far is a playable BK Spiral Mountain terrain transplant inside Tooie's Spiral Mountain map, including working imported collision and several normal gameplay interactions. The documentation also records offline music-format compatibility work and substantial exact geometry overlap between the BK and BT Gruntilda's Lair entrance rooms.

See `STATUS.md` and `PROJECT_A_FINDINGS.md` for the current evidence-backed list.

## Is the project AI-assisted?

Yes. Project A is intentionally transparent about that.

AI tools are used for source analysis, hypothesis generation, experiment planning, code generation, and documentation. The human operator defines the project goals, runs the builds/tests, supplies captures and game behavior, makes project decisions, and accepts or rejects proposed changes.

The important rule is that **AI output is not treated as evidence**. Claims are promoted only after static analysis, runtime behavior, controlled probes, hashes, source references, or independent harness tests support them.

## Why keep all this documentation?

Because a working video is not enough for reverse engineering.

The project should remain useful to another developer even if:

- the current recomp backend changes,
- the runtime prototype stops working,
- the original operator is unavailable,
- an AI-generated interpretation turns out to be wrong.

That requires preserving procedures, corrections, negative results, confidence levels, and upstream source references.

## Does Project A distribute Banjo-Kazooie or Banjo-Tooie assets?

No. The repository is intended to contain tools, source code, hashes, offsets, reports, and documentation — not ROMs or extracted copyrighted game data.

Extraction/conversion tools operate on a user's own legally obtained game data.

## Why use Banjo-Kazooie's decompilation when researching Tooie?

BK's public decompilation is far more semantically mature. Many model and collision structures are already named and have readable consumers.

Project A uses BK as a high-confidence architectural reference **only after observing a corresponding pattern in Tooie**. A BK name is not automatically assigned to a BT field just because the offsets look similar.

## How reliable are the Tooie names in the docs?

They vary. The docs deliberately label findings as:

- **Observed**
- **Strongly supported**
- **Speculative / provisional**

Early anonymous labels such as `section10`, `section1C`, and `section20` are retained where the BT semantics have not yet been fully earned.

## Could upstream recomp changes break Project A?

Yes, especially the runtime adapter: hook locations, generated-function ABI, cache behavior, and memory ownership can change.

That is why Project A now separates game-format/conversion knowledge from recomp-specific integration. Ideally an upstream change should require replacing the adapter, not rediscovering the BK↔BT structures from scratch.

## Why doesn't the GitHub branch always match the newest video or experiment?

Some tests are first performed in the active working environment and documented before the corresponding runtime patch is cleaned up and committed publicly.

Every serious result should increasingly record its artifact status so readers can distinguish:

- committed and reproducible from the public branch,
- verified locally but not yet committed,
- proposed but untested.

## Is the current converter universal?

No.

The Spiral Mountain converter contains choices proven for that test case, including a known-good BT-style vertex-header template. Native BT lair data already shows that blindly reusing the same constants for every model would be unsafe.

Generalization is a future milestone, not a current claim.

## Can other developers use Project A findings without using AI?

Absolutely. The point of the documentation is to make the findings independently inspectable. A contributor can ignore the AI workflow entirely and verify the same offsets, structures, loaders, hashes, and runtime behavior from the documented evidence.

## How can someone help?

The most useful contributions are technical and falsifiable:

- confirm or disprove a field interpretation,
- identify a matched BT source function,
- reproduce a runtime result on another machine,
- improve a converter without relying on hard-coded constants,
- document a failed experiment,
- map setup/object placement,
- trace sky/water/effect consumers,
- help isolate the runtime adapter from upstream recomp internals.

See `CONTRIBUTING.md` for the expected evidence format.
