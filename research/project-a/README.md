# Project A — Raw Research Material

This directory contains intermediate static-analysis extracts and notes used while tracing Banjo-Tooie's map/static-world architecture.

These files are **evidence inputs**, not polished documentation. Start with [`../../PROJECT_A.md`](../../PROJECT_A.md) and the curated docs under [`../../docs/project-a/`](../../docs/project-a/) before trying to infer meaning from an isolated dump.

## What is here

Current material includes extracts centered on:

- `gcmapDll` and map-configuration/resource selection,
- map-header accessor callers,
- indexed map-section helpers,
- functions around world creation/loading,
- dual-section consumers linking the `+0x10` and `+0x1C` sections,
- overlay/static call-site context.

Names such as `section10` and `section1C` were deliberately conservative during early work. Their current interpretations and confidence levels are maintained in `docs/project-a/PROJECT_A_FINDINGS.md` and `BK_BT_CROSSWALK.md`.

## How to use these files

Treat each extract as context for a specific investigation, not as canonical source code. Before citing a conclusion:

1. identify the exact function/call path,
2. compare against the current findings document,
3. check whether the interpretation was later corrected,
4. reproduce the consumer behavior where possible,
5. keep raw offsets separate from semantic names.

## Why keep raw extracts

They make the investigation auditable. A future contributor can inspect what the original conclusion was based on instead of relying only on a summary written after the fact.

## What should not be added here

Do not commit ROMs or extracted copyrighted game assets. Large transient RAM dumps and generated candidate assets should also stay out of Git unless a small, legally safe fixture is specifically needed for a reproducibility test.
