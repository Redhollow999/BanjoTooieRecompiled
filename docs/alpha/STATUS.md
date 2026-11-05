# Public alpha readiness

Audited 2026-11-05. This preparation branch is based on public `main` at
`f017902a90252c276107ce177ccc12c75d297482`. It is not the full playable mod sync.

The latest owner-verified Windows executable has SHA-256
`ff1359063aefa9136d178ba45522287263fce8c2e97494c725ff9ac2025e640c`.
The owner confirmed the Cheato cue and ending pitches after the October 30 fix.
That identifies a local build, not a public Git commit or verification of every
area. Its source was based on local commit
`9a1d074a30dd2ffc97687b063eee015766d20dbb` plus uncommitted changes.

The audit captured 131 project compiler inputs, including 32 includes under
`research/`, and 1,795 compiler inputs including dependencies. The existing
build reports no pending work. Those observations support the captured source
snapshot; a clean rebuild and playable regression pass remain release gates.
See `verified-build.json` for hashes without asset content or personal paths.

## What is established

- The owner-tested opening showcase includes the Ticker mission, Cheato rubble
  sequence and music handoff, corrected ending instrument ranges, and Jamjars.
- The latest repair preserves all 287 notes in the supplied composition.
- Ugger portrait registration was corrected and accepted in earlier testing.
- Dedicated resource lifetimes and existing native music ownership are important
  regression boundaries. Avoid replacing these with unconditional reloads.

## Incomplete or deferred

- Jamjars' repeat hatch animation still needs polish; preserve the accepted
  functional implementation during the source migration.
- Mumbo's Skull uses a separate logical room hosted on native map AD. Its earlier
  crash was resolved in owner testing, but camera/presentation remains awkward.
- CC and BGS main terrain and routes, plus GV/FFP developer previews, are integrated
  locally. Do not describe these as completed or fully play-tested worlds.
- Imported rooms currently reuse native map AD with logical room ownership;
  these are not newly allocated native map IDs.
- Water/rendering, return transitions and expansion music need dedicated tests.
- FKEM is an offline model concept, not a functional boss. The floating platforms,
  Jinjo placements, boss stages and late-game gating are incomplete.
- Brief audio crackles were reported. Three host queue defects were reproduced
  offline, but a direct causal link and an accepted repair are not established.
- Some progress/reward systems remain session-only. Save persistence and migration
  must be documented and tested before claiming a persistent alpha campaign.
- Linux builds of the base port exist; this mod snapshot has no equivalent live
  Linux acceptance. Do not infer parity from upstream CI success.

## Synchronization gates

Do not release the private showcase executable or its resource folders. The
current runtime embeds ROM-derived sample bytes in C includes and consumes
converted models, sprites, music and other external files. Omitting those files
would produce an inaccurate source sync, and publishing the folders would expose
game content. See [RESOURCES.md](RESOURCES.md) and [SYNC_PLAN.md](SYNC_PLAN.md).

This first review commit changes preparation documentation and publication
checks only. The verified development directory and existing checkpoints are
preserved. No claim is made that the public branch reproduces the showcase yet.
