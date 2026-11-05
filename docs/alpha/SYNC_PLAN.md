# Reviewed synchronization sequence

1. Preserve the installed verified executable and private compiler-input/resource
   snapshot. Record hashes, the local base commit, dependency pins and patches.
   Keep these backups outside public staging. This was done locally for the audit.
2. Review this preparation commit: accurate status/setup/contribution documents,
   stronger ignore rules, metadata-only manifests, and a read-only publication
   check. It disables the inherited automatic release/build-artifact workflow.
3. Review original gameplay logic and required tools using an explicit path list.
   There are 32 active research includes; copying only `src/` and
   `RecompiledFuncs/` would omit live code. Historical experiments, installer
   fixtures, checkpoints and diagnostic outputs are not the active source tree.
4. Separate embedded game data from algorithms in an isolated integration branch.
   Generate private includes/resources locally. Preserve existing runtime IDs,
   checksums, scene ownership, music masks, pointer lifetimes and stage metadata.
   Do not redesign accepted gameplay while doing this migration.
5. Complete the resource recipes in RESOURCES.md, port required tools without
   personal paths, and resolve authored-material and third-party license questions.
   Missing resources must produce a clear setup error, not a silently reduced demo.
6. Reproduce dependency patches at their pins. Audit found the three stored patches
   reverse-apply to the current dependencies, but that check alone missed extra
   changes. Exact reproduction found an additional N64ModernRuntime overlays.cpp
   change and RT64 interpreter.cpp/rsp.cpp/state.cpp changes. Capture those as
   reviewed patches together with their source-side callers; the missing-function
   diagnostic adds a link dependency. N64Recomp tracked changes are reproduced by
   its stored patch. Do not change pins without explanation.
7. Apply the selected source in a new checkout, generate private resources there,
   configure and build from scratch, then test boot, room returns, MM entrance,
   Ticker fight/reset/reward and pause HUD/music, Cheato cues/rubble/departure,
   Ugger portrait and Jamjars. Test expansion previews separately. Preserve saves.
8. Review the final diff, generated-resource exclusions, license evidence and
   public-history exposure before the owner authorizes publication. Only then open
   a PR/push the agreed branch. No force-push, reset or history rewrite is planned.

The public main, public project-a and local development branch have diverged.
Use current public main as the review base so public concept/status updates are
retained. Do not overwrite public docs with the private working README, which is
an old one-off Ticker installer note. Do not merge the entire private research
directory or blindly cherry-pick unpublished development checkpoints.

This commit is deliberately a preparation commit. It does not claim the private
showcase's gameplay is already synchronized. Keep the full gameplay PR blocked
until the generation, licensing and clean-checkout gates above are satisfied.

Preparation follow-up: manual validation now uses an explicit approved baseline,
empty comparisons fail, forced research additions and non-regular file types are
blocked, and deletions/mode changes are reported. Changes to workflows, validators
or their ownership/policy require the independent review described in
[PUBLICATION_REVIEW.md](PUBLICATION_REVIEW.md). The required GitHub branch rules
have not been configured; this remains a pre-publication gate.
