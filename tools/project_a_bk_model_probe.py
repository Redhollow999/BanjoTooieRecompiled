#!/usr/bin/env python3
"""
Project A: Banjo-Kazooie model extractor / structural inspector.

Targets the verified Banjo-Kazooie US v1.0 big-endian (.z64) ROM:
SHA1 1FE1632098865F639E22C11B9A81EE8F29C75D7A

This tool is deliberately read-only with respect to the ROM.  It extracts and
decompresses selected BK assets, writes the decompressed model bins to disk, and
prints the fields we need before attempting a BK -> Tooie conversion.

Default assets:
  0x14CF  Spiral Mountain opaque level model
  0x14D0  Spiral Mountain translucent level model
"""

from __future__ import annotations

import argparse
import hashlib
import struct
import sys
import zlib
from collections import Counter
from pathlib import Path

EXPECTED_SHA1 = "1FE1632098865F639E22C11B9A81EE8F29C75D7A"
ASSETS_ROM_START = 0x5E90

DEFAULT_ASSETS = (0x14CF, 0x14D0)

# F3DEX opcodes that have straightforward F3DEX2 counterparts or are RDP
# commands that remain in the RDP command range.  This is diagnostic only:
# the converter will still validate individual encodings later.
KNOWN_F3DEX = {
    0x01: "MTX",
    0x03: "MOVEMEM",
    0x04: "VTX",
    0x06: "DL",
    0xB1: "TRI2",
    0xB2: "MODIFYVTX",
    0xB3: "RDPHALF_2",
    0xB4: "RDPHALF_1",
    0xB5: "LINE3D/QUAD-family",
    0xB6: "CLEARGEOMETRYMODE",
    0xB7: "SETGEOMETRYMODE",
    0xB8: "ENDDL",
    0xB9: "SETOTHERMODE_L",
    0xBA: "SETOTHERMODE_H",
    0xBB: "TEXTURE",
    0xBC: "MOVEWORD",
    0xBD: "POPMTX",
    0xBE: "CULLDL",
    0xBF: "TRI1",
}


def u16(b: bytes, off: int) -> int:
    return struct.unpack_from(">H", b, off)[0]


def s16(b: bytes, off: int) -> int:
    return struct.unpack_from(">h", b, off)[0]


def u32(b: bytes, off: int) -> int:
    return struct.unpack_from(">I", b, off)[0]


def f32(b: bytes, off: int) -> float:
    return struct.unpack_from(">f", b, off)[0]


def fmt_ptr(v: int) -> str:
    return f"0x{v:08X}" if v else "0"


def in_range(data: bytes, off: int, size: int = 1) -> bool:
    return 0 <= off <= len(data) and 0 <= size and off + size <= len(data)


def decompress_bk_asset(chunk: bytes) -> tuple[bytes, str]:
    """
    BK Rarezip payloads may begin with 0x11 0x72.  After that is a four-byte
    size/header field followed by a raw DEFLATE stream.
    """
    original_len = len(chunk)
    p = 0
    magic = ""
    if chunk[:2] == b"\x11\x72":
        p = 2
        magic = "1172 "
    if len(chunk) < p + 5:
        raise ValueError("compressed asset is too short")

    header = chunk[p:p + 4]
    payload = chunk[p + 4:]
    try:
        out = zlib.decompress(payload, wbits=-15)
    except zlib.error as exc:
        raise ValueError(f"raw-DEFLATE decompression failed: {exc}") from exc

    return out, f"{magic}hdr={header.hex().upper()} comp={original_len} decomp={len(out)}"


def parse_asset_table(rom: bytes):
    if not in_range(rom, ASSETS_ROM_START, 8):
        raise ValueError("ROM is too small for the BK asset table")

    count = u32(rom, ASSETS_ROM_START)
    unk4 = u32(rom, ASSETS_ROM_START + 4)
    table_off = ASSETS_ROM_START + 8
    table_size = count * 8
    data_base = table_off + table_size

    if count < 2 or not in_range(rom, table_off, table_size):
        raise ValueError(f"implausible asset table count: {count}")

    entries = []
    for i in range(count):
        off = u32(rom, table_off + i * 8)
        comp = u16(rom, table_off + i * 8 + 4)
        flags = u16(rom, table_off + i * 8 + 6)
        entries.append((off, comp, flags))

    return count, unk4, data_base, entries


def extract_asset(rom: bytes, asset_id: int, data_base: int, entries):
    if asset_id < 0 or asset_id + 1 >= len(entries):
        raise ValueError(f"asset 0x{asset_id:X} is outside table range")

    off0, comp_flag, flags = entries[asset_id]
    off1, _, _ = entries[asset_id + 1]
    if off1 < off0:
        raise ValueError("asset metadata offsets are not monotonic")

    abs0 = data_base + off0
    abs1 = data_base + off1
    if not in_range(rom, abs0, abs1 - abs0):
        raise ValueError(
            f"asset 0x{asset_id:X} range 0x{abs0:X}-0x{abs1:X} is outside ROM"
        )

    chunk = rom[abs0:abs1]
    if comp_flag & 1:
        data, detail = decompress_bk_asset(chunk)
        compression = f"compressed ({detail})"
    else:
        data = chunk
        compression = f"uncompressed ({len(data)} bytes)"

    return data, {
        "relative_start": off0,
        "relative_end": off1,
        "rom_start": abs0,
        "rom_end": abs1,
        "comp_flag": comp_flag,
        "flags": flags,
        "compression": compression,
    }


def analyze_model(data: bytes, asset_id: int) -> list[str]:
    out: list[str] = []
    out.append("=" * 76)
    out.append(f"ASSET 0x{asset_id:04X}  decompressed size: 0x{len(data):X} ({len(data)} bytes)")

    if len(data) < 0x38:
        out.append("ERROR: too small to contain a BK model header")
        return out

    magic = u32(data, 0x00)
    geo = u32(data, 0x04)
    tex = u16(data, 0x08)
    geo_type = u16(data, 0x0A)
    gfx = u32(data, 0x0C)
    vtx = u32(data, 0x10)
    unk14 = u32(data, 0x14)
    anim = u32(data, 0x18)
    coll = u32(data, 0x1C)
    area = u32(data, 0x20)
    mesh = u32(data, 0x24)
    anim_vtx = u32(data, 0x28)
    anim_tex = u32(data, 0x2C)
    tri_count = u16(data, 0x30)
    header_vtx_count = u16(data, 0x32)
    unk34_bits = u32(data, 0x34)
    unk34_float = f32(data, 0x34)

    out.append("BK root header:")
    out.append(
        f"  magic=0x{magic:08X}  geo={fmt_ptr(geo)}  tex=0x{tex:04X} "
        f"geoType=0x{geo_type:04X}"
    )
    out.append(
        f"  gfx={fmt_ptr(gfx)}  vtx={fmt_ptr(vtx)}  unk14={fmt_ptr(unk14)} "
        f"anim={fmt_ptr(anim)}"
    )
    out.append(
        f"  collision={fmt_ptr(coll)}  area20={fmt_ptr(area)} "
        f"mesh24={fmt_ptr(mesh)}"
    )
    out.append(
        f"  animVtx28={fmt_ptr(anim_vtx)}  animTex2C={fmt_ptr(anim_tex)}"
    )
    out.append(
        f"  hdrTri={tri_count}  hdrVtx={header_vtx_count}  "
        f"+34=0x{unk34_bits:08X} ({unk34_float:g})"
    )

    if magic != 0x0000000B:
        out.append("  WARNING: magic is not the expected 0x0000000B model magic")

    # Texture setup.
    if tex and in_range(data, tex, 8):
        tex_size = u32(data, tex)
        tex_count = u16(data, tex + 4)
        tex_pad = u16(data, tex + 6)
        out.append("Texture setup (BK 16-byte descriptors):")
        out.append(
            f"  offset=0x{tex:X} size=0x{tex_size:X} count={tex_count} "
            f"pad/flag=0x{tex_pad:04X}"
        )
        desc_end = tex + 8 + tex_count * 0x10
        if desc_end > len(data):
            out.append("  WARNING: descriptor table runs beyond model")
        for i in range(min(tex_count, 3)):
            d = tex + 8 + i * 0x10
            if not in_range(data, d, 0x10):
                break
            out.append(
                f"    tex[{i}] off=0x{u32(data,d):08X} type=0x{u16(data,d+4):04X} "
                f"{data[d+8]}x{data[d+9]}"
            )
    else:
        out.append("Texture setup: absent or out of range")

    # Vertex setup.
    if vtx and in_range(data, vtx, 0x18):
        mins = struct.unpack_from(">3h", data, vtx + 0x00)
        maxs = struct.unpack_from(">3h", data, vtx + 0x06)
        center = struct.unpack_from(">3h", data, vtx + 0x0C)
        local_norm = s16(data, vtx + 0x12)
        list_count = u16(data, vtx + 0x14)
        global_norm = s16(data, vtx + 0x16)
        out.append("Vertex setup:")
        out.append(
            f"  min={mins} max={maxs} center={center} "
            f"localNorm={local_norm} count={list_count} globalNorm={global_norm}"
        )
        out.append(
            f"  header-count invariant: root+0x32={header_vtx_count}, "
            f"vtx+0x14={list_count}, match={'YES' if header_vtx_count == list_count else 'NO'}"
        )
        vertex_end = vtx + 0x18 + list_count * 0x10
        out.append(f"  vertex array end predicted: 0x{vertex_end:X}")
        if vertex_end > len(data):
            out.append("  WARNING: vertex array end is outside model")
    else:
        out.append("Vertex setup: absent or out of range")

    # Collision setup.
    if coll and in_range(data, coll, 0x18):
        mins = struct.unpack_from(">3h", data, coll + 0x00)
        maxs = struct.unpack_from(">3h", data, coll + 0x06)
        y_stride = s16(data, coll + 0x0C)
        z_stride = s16(data, coll + 0x0E)
        geo_count = u16(data, coll + 0x10)
        scale = u16(data, coll + 0x12)
        coll_tri_count = u16(data, coll + 0x14)
        tri_start = coll + 0x18 + geo_count * 4
        tri_end = tri_start + coll_tri_count * 12
        out.append("Collision setup:")
        out.append(
            f"  min={mins} max={maxs} yStride={y_stride} zStride={z_stride} "
            f"geoCount={geo_count} scale={scale} triCount={coll_tri_count}"
        )
        out.append(
            f"  4-byte cell table -> triangles start 0x{tri_start:X}; "
            f"12-byte triangle table -> end 0x{tri_end:X}"
        )
        if tri_end > len(data):
            out.append("  WARNING: collision table end is outside model")
    else:
        out.append("Collision setup: absent or out of range")

    # Effects/mesh vertex-group setup.
    if mesh and in_range(data, mesh, 2):
        group_count = s16(data, mesh)
        out.append(f"+0x24 mesh/effects vertex-group setup: count={group_count}")
    else:
        out.append("+0x24 mesh/effects vertex-group setup: absent or out of range")

    # Gfx/display list.
    if gfx and in_range(data, gfx, 8):
        cmd_count = u32(data, gfx)
        gfx_pad = u32(data, gfx + 4)
        max_cmds = max(0, (len(data) - (gfx + 8)) // 8)
        actual_scan = min(cmd_count, max_cmds)
        hist = Counter(data[gfx + 8 + i * 8] for i in range(actual_scan))
        out.append("F3DEX display-list setup:")
        out.append(
            f"  offset=0x{gfx:X} commandCount={cmd_count} pad=0x{gfx_pad:08X} "
            f"scanCount={actual_scan}"
        )
        if cmd_count > max_cmds:
            out.append("  WARNING: command count extends beyond model")

        parts = []
        for op, count in sorted(hist.items()):
            name = KNOWN_F3DEX.get(op)
            if name is None and op >= 0xE4:
                name = "RDP"
            if name:
                parts.append(f"{op:02X}:{count}({name})")
            else:
                parts.append(f"{op:02X}:{count}(?)")
        out.append("  opcode histogram:")
        out.append("    " + " ".join(parts))

        unknown = [
            (op, count) for op, count in sorted(hist.items())
            if op not in KNOWN_F3DEX and op < 0xE4
        ]
        if unknown:
            out.append(
                "  REVIEW NEEDED for non-RDP opcodes: "
                + ", ".join(f"0x{op:02X} x{count}" for op, count in unknown)
            )
        else:
            out.append("  no unknown non-RDP opcodes observed")
    else:
        out.append("F3DEX display-list setup: absent or out of range")

    # First-pass transplant friendliness.
    blockers = []
    if tex != 0x38:
        blockers.append(f"texture setup is 0x{tex:X}, not the common BK level-model 0x38")
    if anim_vtx:
        blockers.append("+0x28 animated-vertex data is present")
    if anim:
        blockers.append("+0x18 animation data is present")
    if magic != 0x0B:
        blockers.append("unexpected model magic")

    out.append("First-pass converter assessment:")
    if blockers:
        for b in blockers:
            out.append(f"  CAUTION: {b}")
    else:
        out.append("  structurally suitable for the conservative level-model conversion path")

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path, help="Banjo-Kazooie US v1.0 .z64 ROM")
    ap.add_argument(
        "--asset",
        action="append",
        type=lambda x: int(x, 0),
        dest="assets",
        help="asset ID (repeatable; default: 0x14CF and 0x14D0)",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path("research/project-a/bk-assets"),
        help="directory for extracted decompressed model bins",
    )
    args = ap.parse_args()

    rom = args.rom.read_bytes()
    sha1 = hashlib.sha1(rom).hexdigest().upper()
    print(f"ROM: {args.rom}")
    print(f"size={len(rom)} SHA1={sha1}")
    if sha1 != EXPECTED_SHA1:
        print(
            f"ERROR: expected BK US v1.0 SHA1 {EXPECTED_SHA1}; refusing to parse a different ROM.",
            file=sys.stderr,
        )
        return 2

    count, unk4, data_base, entries = parse_asset_table(rom)
    print(
        f"asset table: ROM 0x{ASSETS_ROM_START:X}, count={count}, "
        f"unk4=0x{unk4:08X}, dataBase=0x{data_base:X}"
    )

    assets = args.assets or list(DEFAULT_ASSETS)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for asset_id in assets:
        try:
            data, meta = extract_asset(rom, asset_id, data_base, entries)
        except Exception as exc:
            print(f"\nASSET 0x{asset_id:04X}: ERROR: {exc}", file=sys.stderr)
            continue

        out_path = args.out_dir / f"{asset_id:04X}.model.bin"
        out_path.write_bytes(data)

        print()
        print(
            f"asset meta 0x{asset_id:04X}: rel=0x{meta['relative_start']:X}-"
            f"0x{meta['relative_end']:X} ROM=0x{meta['rom_start']:X}-0x{meta['rom_end']:X} "
            f"compFlag=0x{meta['comp_flag']:04X} flags=0x{meta['flags']:04X}"
        )
        print(f"compression: {meta['compression']}")
        print(f"wrote: {out_path}")

        for line in analyze_model(data, asset_id):
            print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
