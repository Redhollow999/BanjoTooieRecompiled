# Project A — Contributing Research

Project A welcomes technical scrutiny more than agreement. A useful contribution can confirm a hypothesis, falsify it, identify a cleaner upstream analogue, or document why a current approach is fragile.

## What makes a useful contribution

Please include enough information for someone else to verify the claim:

- repository branch and commit SHA,
- game/version identity where relevant,
- exact function/file/address or data structure under discussion,
- reproduction steps or command line,
- hashes for non-distributable extracted inputs/outputs when practical,
- expected result,
- actual result,
- confidence level,
- negative controls or alternative explanations considered.

## Confidence labels

Use these consistently:

- **Observed** — directly demonstrated by code, bytes, or runtime behavior.
- **Strongly supported** — several independent observations agree, but the semantic interpretation is not fully proven.
- **Speculative** — plausible working hypothesis requiring direct evidence.

Do not upgrade a claim because it sounds likely or because BK uses a similarly named structure.

## AI-assisted work

AI-assisted research and code are allowed in Project A, but **AI output is not evidence**.

If an AI system proposes a field meaning, function match, or patch, verify it with one or more of:

- source/consumer tracing,
- byte-structure comparison,
- controlled runtime experiment,
- memory capture,
- independent parser/harness,
- known-good upstream reverse-engineering material.

Document corrections when an AI-generated or human-generated assumption turns out to be wrong.

## Copyrighted material

Do not submit:

- ROMs,
- extracted level/model assets,
- extracted music/audio,
- copyrighted game data that can be regenerated locally from a user's own copy.

Prefer scripts, hashes, offsets, structural descriptions, and reproducible extraction instructions.

## Reverse-engineering style

Good:

```text
header +0x1C → 4-byte records → 12-byte records → three indices into +0x10 vertices
```

Better after consumer evidence:

```text
header +0x1C is strongly supported as collision-list-like data
```

Bad:

```text
+0x1C = collision because BK says so
```

BK's mature decompilation is an excellent guide, not a substitute for validating Tooie.

## Failed experiments

Please report them. Include what changed and what did **not** change. A clean negative result can save the next researcher hours.

## Runtime-backend changes

If upstream recomp architecture changes, prefer adapting the smallest possible runtime layer rather than rewriting conversion logic around the new backend.

The intended separation is:

```text
research / structures
        ↓
conversion + validation
        ↓
BT-compatible data
        ↓
runtime adapter
        ↓
current recomp backend
```

Contributions that improve this separation are especially valuable.
