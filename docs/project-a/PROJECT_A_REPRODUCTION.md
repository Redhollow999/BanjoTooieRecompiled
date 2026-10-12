# Project A — Reproduction Guide

The goal of this document is not merely to make Project A run on one machine. It defines the minimum information a Project A result should provide so another developer can independently verify it.

## Rule zero

**Do not distribute ROMs or extracted copyrighted game assets.**

A reproduction recipe should accept a researcher's own legally obtained game data, verify expected input identity, and generate temporary/extracted artifacts locally.

## Recommended environment record

Every reproducible experiment should record:

- Git commit SHA.
- Branch name.
- OS / architecture.
- Tool/script path and command line.
- Input ROM/version hash where legally appropriate.
- Input extracted-asset hashes when the asset itself cannot be distributed.
- Output hashes.
- Runtime map/resource IDs.
- Whether the result is static analysis, offline harness verification, or live gameplay behavior.

## Build the recomp

Use the repository's main `README.md` for dependency setup, build, and ROM-selection instructions. Project A work is currently developed on branch `project-a`.

Because upstream recomp internals may change, runtime-hook instructions should always be tied to a specific commit rather than copied forward indefinitely.

## Reproduce BK Spiral Mountain extraction

The public branch contains a read-only BK model extractor/inspector:

```bash
python tools/project_a_bk_model_probe.py /path/to/Banjo-Kazooie-USA-v1.0.z64
```

The tool expects BK USA v1.0 big-endian ROM SHA-1:

```text
1FE1632098865F639E22C11B9A81EE8F29C75D7A
```

By default it extracts and inspects:

- `0x14CF` — Spiral Mountain opaque level model.
- `0x14D0` — Spiral Mountain translucent/secondary model.

Default output location:

```text
research/project-a/bk-assets/
```

To inspect another model asset:

```bash
python tools/project_a_bk_model_probe.py /path/to/game.z64 --asset 0x14F3
```

The probe is intended to fail closed on an unexpected ROM and prints the model sections relevant to the current conversion research.

## Reproduce first-pass model conversion

After extracting one or more BK model bins:

```bash
python tools/project_a_bk_to_bt_model.py \
  research/project-a/bk-assets/14CF.model.bin \
  research/project-a/bk-assets/14D0.model.bin
```

Default converted output location:

```text
research/project-a/bt-candidates/
```

The current converter performs several validated-but-still-experimental operations:

- BK→BT header/texture descriptor repacking.
- Root-pointer relocation.
- A known-good Tooie-style vertex-header transformation used by the Spiral Mountain proof-of-concept.
- A simple tested Tooie geometry-layout replacement.
- Translation of relevant F3DEX commands to F3DEX2 forms.
- Post-conversion pointer/count validation.

### Important

A successful converter exit means the candidate passed the converter's structural checks. It does **not** prove the candidate is safe or semantically correct for every Tooie map.

The vertex-header template in the current converter is specifically known to work for the tested Spiral Mountain case. Do not generalize it to Gruntilda's Lair or arbitrary models without validating the native consumer behavior first.

## Runtime experiment standard

For each live replacement/injection test, capture at minimum:

```text
map ID
primary resource ID
secondary resource ID, if present
candidate file SHA-256
target allocation/capacity if known
injection point / hook function
result after first load
result after leaving and re-entering the map
rollback procedure
```

If memory ownership or target capacity is not established, label the experiment unsafe/temporary rather than presenting it as a durable integration method.

## Comparing mutable geometry

The secondary bridge/fence investigation demonstrated why a visual symptom alone is insufficient. The useful evidence was a pair of live memory captures showing vertex position/UV/color changes while draw commands stayed unchanged.

Future effect/animation investigations should likewise separate:

1. source model bytes,
2. post-conversion bytes,
3. live loaded bytes,
4. live bytes after several frames,
5. display-list changes vs vertex-data changes.

## Offline reader/harness tests

When claiming format compatibility from generated C code:

- preserve the original generated function bodies,
- hash the source inputs,
- use bounds-checked guest-memory emulation,
- compare complete traces rather than one or two output values,
- include negative controls,
- run ASan/UBSan when practical,
- explicitly state what was **not** tested (for example audio synthesis or repeated loops).

## Evidence template

Use this for new public log entries:

```markdown
## Investigation X.Y — short title

### Question
What exactly are we trying to establish?

### Evidence
- commit / source file / function
- input hashes
- captured bytes or runtime observation

### Procedure
Exact commands or patch steps.

### Result
What happened, including failures.

### Interpretation
Observed / Strongly supported / Speculative.

### Artifact status
Committed / local-only / proposed / superseded.

### Next falsifying test
What experiment could prove this interpretation wrong?
```

That last field is intentional: Project A should document how a belief can be challenged, not just how it was reached.
