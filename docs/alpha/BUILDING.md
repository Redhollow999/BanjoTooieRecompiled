# Contributor setup

## Current public foundation

The public foundation builds the base port. It does not yet reproduce the private
Banjo-KaTooie showcase. Follow this distinction when reporting results.

Use Windows x64, Visual Studio 2022 Build Tools with the C++ workload and Windows
SDK, LLVM clang-cl, CMake 3.20+, Ninja, Git and Python 3.11+. New asset tools use
`tomllib`, so the older Python 3.8 recommendation is insufficient for that work.
Sample-generation tools also use NumPy; pin its exact version when the generation
pipeline is promoted. A D3D12 or Vulkan-capable GPU is needed for gameplay.

In a fresh contributor checkout, initialize the pinned dependencies and apply the
stored patches:

```text
python tools/setup_deps.py
python tools/setup_deps.py --check
```

These commands are for a fresh checkout. Do not run dependency updates over a
working development environment with additional patches. The three patched
submodules normally appear dirty. Record changes as patches against their exact
pins; a gitlink alone cannot preserve an uncommitted dependency fix.

From the project root on Windows:

```text
cmake_configure.bat
build_bt.bat
```

Check for the final executable link and inspect the build log for errors. A build
wrapper's successful exit alone does not establish that a new executable exists.
The runtime needs its launcher assets and copied SDL/DXC DLLs alongside the
executable. Supply your own compatible Banjo-Tooie USA ROM through the launcher;
no ROM acquisition, download or distribution is provided here.

The base Linux configuration uses clang/clang++, CMake/Ninja and system SDL2 plus
the GUI dependencies described by the original port. Run from the project root
so asset paths resolve. Linux mod gameplay acceptance is pending.

## Reproducing the private showcase later

Additional Banjo-Kazooie USA 1.0 inputs and locally generated resources are required.
The BK extraction tools expect SHA-1
`1fe1632098865f639e22c11b9a81ee8f29c75d7a`. Verify the supported BT revision
against the existing launcher/ROM tooling; do not silently substitute a region.

The legitimate workflow is to use inputs you are authorized to use locally,
extract required asset IDs, run the published conversion/patch recipes, and compare
the generated outputs with the public hash manifest. Generated game content stays
ignored and local. Possession of a ROM or transformation into a different format
does not itself establish permission to redistribute the result.

That end-to-end pipeline is **not complete**. Several current scripts consume
private construction ZIPs, DLS banks, screenshots or earlier generated resources.
They must be replaced with reproducible extraction/generation stages before a
clean clone can reproduce the showcase. Do not use an unofficial shared asset
pack as a substitute. See [RESOURCES.md](RESOURCES.md) for the concrete gaps.

`python tools/alpha_preflight.py --resources` checks the documented fixed resource
subset. It deliberately fails when resources are absent or different. Passing
does not establish a complete dependency closure, licensing approval or gameplay
correctness. `--source` checks the captured project compiler inputs, which will
also fail on this preparation-only branch until the gameplay sync is completed.
