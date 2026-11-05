# Contributing to Banjo-KaTooie

Read [alpha status](docs/alpha/STATUS.md) and
[setup requirements](docs/alpha/BUILDING.md) before choosing a task. Public source
and the owner-tested private showcase currently differ; identify which one you ran.

Use a small topic branch and a reviewable PR. Explain the player-visible problem,
the change, how it was tested and what remains uncertain. Preserve native ownership
and lifecycle rules; do not replace accepted fixes with broad reset/reload behavior.
Generated C is maintained source here: if you edit it, record any regeneration
requirements. Dependency changes need patches against the exact pinned commit.

Do not submit ROMs, extracted/converted models, sprites, textures, sample banks,
audio bytes embedded in source, game binaries, saves, recordings, personal paths,
credentials, or private checkpoints. Supply local generation instructions, asset
IDs and hashes instead. Use only original contributions or material you have
permission to contribute, and document its provenance. The existing COPYING file
does not grant rights to third-party game content or unclear dependency assets.

For a bug, include the public commit or verified build hash, operating system,
reproduction steps, expected/actual behavior and whether the save was new. Review
logs before attaching them; remove personal information and do not upload memory
dumps. Compile success and mocked offline tests must not be described as gameplay
acceptance. Do not use the only copy of a valuable save for testing.

Useful initial work includes reviewing resource generation, documenting exact
recipes, completing rights/attribution records, small reproducible bugs and clean
setup validation. CC/BGS and FKEM are incomplete systems; coordinate their behavior
before inventing new progression or encounter design.

Release publication is disabled in this preparation branch. A PR is not permission
to publish packaged game content. The maintainer reviews source, provenance and
playable acceptance before enabling a release process.
