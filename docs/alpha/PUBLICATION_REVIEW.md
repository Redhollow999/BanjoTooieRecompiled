# Publication-control review

The approved public synchronization baseline for this preparation series is
`f017902a90252c276107ce177ccc12c75d297482`. The manual workflow defaults to this
full SHA. It never defaults to the commit being screened. A maintainer may select
another earlier, independently approved full commit SHA after review. Do not set
the baseline to a candidate just to obtain a passing check.

Pull-request validation uses GitHub's PR base SHA. Manual validation uses the
required `approved_baseline` input. Both screen the committed checkout with
`--head HEAD`, require an ancestor baseline, and reject empty comparisons.
For local work before committing, omit `--head` to include working changes and
untracked files. Ignored files are not scanned unless force-added; a force-added
file under `research/` is rejected regardless of `.gitignore`.

## Change handling

- Additions and modifications are screened for private directories, payloads,
  personal paths and common credential patterns.
- Renames are deliberately represented as deletion plus addition, so an old safe
  name cannot exempt a new private destination. Both sides remain in the report.
- Deletions are explicitly reported with no content scan. Deleting a publication
  control requires maintainer review, even though there is no new payload.
- Symlinks, gitlinks and unsupported/unmerged changes are blocked. Regular-file
  mode changes, including executable-bit changes, require maintainer review.
- Workflow files, CODEOWNERS, ignore/attribute policy, the three preparation
  scripts and this policy document are protected review controls. Changing or
  deleting them cannot receive ordinary content approval from the validator.

Exit status `0` means content checks pass with no protected changes. Status `1`
means blocked content, invalid scope, or an empty comparison. Status `2` means
content checks passed but publication-control or file-mode changes require
independent maintainer review. There is no command-line bypass flag. This
correction itself changes controls, so status `2` against the prior baseline is
expected and must not be described as approval to publish.

## Repository settings required before publication

CODEOWNERS assigns the controls to `@Redhollow999`. Before relying on this process,
the owner must configure the target branch/ruleset to require pull requests,
code-owner approval, dismissal of stale approvals when commits change, approval
of the most recent push by someone other than its author where available, and
the publication-boundary check. Restrict direct pushes and control who can bypass
these rules. Changes to the controls require an explicit maintainer decision;
any use of a ruleset override must be recorded rather than masking status `2`.

These settings have **not** been changed on GitHub. No push is authorized. The
maintainer must independently inspect the final commit/diff and rerun trusted
checks, because scripts and workflow definitions in a proposed branch can be
edited by that branch. CODEOWNERS plus required server-side review protects that
trust boundary; a candidate running its own validator cannot establish trust in
itself. Do not use `pull_request_target` to run untrusted candidate code with
elevated permissions. This workflow remains read-only and publishes no artifacts.

The full gameplay synchronization remains blocked by resource-generation,
dependency-patch, licensing and clean-build requirements independently of these
preparation controls.
