# Banjo-KaTooie development preparation

Banjo-KaTooie is an early Banjo-Kazooie / Banjo-Tooie project built on the
Banjo-Tooie Recompiled native PC port. This branch prepares the public repository
for alpha development and community review.

**The public source does not yet reproduce the latest owner-tested showcase.**
The playable development build uses additional uncommitted gameplay code and
private, locally generated resources. See [verified status](docs/alpha/STATUS.md),
[the synchronization plan](docs/alpha/SYNC_PLAN.md) and the
[resource dependency review](docs/alpha/RESOURCES.md). Do not present a successful
base-port build as a completed alpha build.

- [Contributor setup and build requirements](docs/alpha/BUILDING.md)
- [Contribution guidelines](CONTRIBUTING.md)
- [Project concepts and existing progress notes](docs/project-a/)
- [Verified source/resource hash manifest](docs/alpha/verified-build.json)
- [Engineering notes](AGENTS.md)
- [Archived base-port build instructions and credits](docs/BASE_PORT_README.md)

Users supply compatible local ROM inputs themselves. ROMs, extracted game assets,
converted models/sprites/music, sample banks, private backups and game binaries
must not be added to the repository. Hashes and conversion instructions can be
reviewed without redistributing those inputs. Existing public fonts, artwork and
frontend dependency licensing also need review before releases; being present in
history is not permission to redistribute them.

Automatic release publication and packaged build-artifact uploads are disabled in
this preparation branch pending source, resource, license and gameplay review.
The existing GPLv3 COPYING file and upstream notices remain; third-party materials
require their own rights/provenance records. No license claim is made for game
content or unlicensed dependencies.

The project builds on [N64Recomp](https://github.com/N64Recomp/N64Recomp),
[N64ModernRuntime](https://github.com/N64Recomp/N64ModernRuntime),
[RT64](https://github.com/rt64/rt64), and
[RecompFrontend](https://github.com/N64Recomp/RecompFrontend).
