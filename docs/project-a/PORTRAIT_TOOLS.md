# Authentic Ugger portrait tools

These Python tools render the owner's extracted Tooie model/animations and pack
the result into a native sprite template. They do not create generative artwork,
modify the ROM or contain game asset bytes. Runtime integration is separate and
is not included in this documentation/tooling update.

## Dependencies and inputs

Python 3 with NumPy and Pillow. Place owner-extracted files at:

`research/project-a/ugger-portrait-reference-20261021/`

| File | Asset | SHA256 |
|---|---|---|
| `0671.ugger-model.bin` | Original Ugger model with embedded textures | `9604b04f7352eaf7e5f6c355178e0c7891aa68871c6e63a9b11a960034655752` |
| `01E7.ugger-idle.bin` | Idle animation | `6acb25fa7823ae421b1d8082f0d7703effa6ebd526441b370a66809c41c510e5` |
| `01E9.ugger-reaction.bin` | Reaction animation used for mouth poses | `6c06e77e7db351dc189d79b8aecba8bb2ad146f10505f5e4f55ef24ce32fec15` |
| `0B89.banjo-portrait.bin` | Native sprite structure template | `d195a5e1172af159b8eefaf160a8955c402dab3468bb602de89496cf30b734b8` |

Inputs and generated output must remain outside version control.

## Run from the repository root

```powershell
python tools/project_a_render_ugger_portrait.py
python tools/project_a_pack_ugger_portrait.py
```

Output directory:
`research/project-a/ugger-portrait-prototype-20261024/`

The renderer provides pose/contact sheets and a full-model preview. The packer
provides transparent frame PNGs, a decoded native-sprite contact sheet, an
illustrative animated GIF, a sprite manifest and `ugger.bt-sprite.bin`.

The native sprite has ten 32x32 CI8 frames and a shared RGBA16 palette. Header,
frame descriptors and geometry sections are retained from the template; only
palette/pixel data change. Frames 0..5 contain mouth poses and final four are
neutral. Final mug is mirrored left/right to face right in the lower NPC box.
The general pose sheet shows canonical model views, before final mug mirroring.

## Limits and runtime requirements

The exporter is focused on this model, not a complete N64 renderer. It uses
linear animation interpolation and approximates native lighting, RDP combiner
behavior and filtering. The outline is provisional. Preview GIF timing does
not establish native dialogue frame timing.

Native portrait slot44 is normally deliberately empty. Integrating a sprite
requires handling its native load/frame-count, draw and headless-layout gates
within the owned Ugger conversation. Merely mapping an asset ID is insufficient.
Retain native cache/refcount/release ownership and silent voice/crossfade guards.
These runtime changes are not shipped by the two offline tools.

## Attribution

Model/animation format and bone transforms were cross-checked against
[noclip.website](https://github.com/magcius/noclip.website), specifically its
BanjoKazooie `geo.ts`, `scenes.ts`, `render.ts` and PokemonSnap `f3dex2.ts`.
Upstream license notice is retained in [NOCLIP_LICENSE.txt](NOCLIP_LICENSE.txt).
