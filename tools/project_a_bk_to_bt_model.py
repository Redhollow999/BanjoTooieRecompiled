#!/usr/bin/env python3
from __future__ import annotations
import argparse, struct
from pathlib import Path
from collections import Counter

BK_HEADER_SIZE = 0x38
BT_TEXTURE_OFFSET = 0x50
ROOT_PTR_FIELDS = (0x04,0x0C,0x10,0x14,0x18,0x1C,0x20,0x24,0x28,0x2C)
ALLOWED_F3DEX = {0x01,0x03,0x04,0x06,0xB1,0xB2,0xB3,0xB4,0xB5,0xB6,0xB7,0xB8,0xB9,0xBA,0xBB,0xBC,0xBD,0xBE,0xBF}

def u16(b,o): return struct.unpack_from('>H',b,o)[0]
def u32(b,o): return struct.unpack_from('>I',b,o)[0]
def p16(b,o,v): struct.pack_into('>H',b,o,v & 0xFFFF)
def p32(b,o,v): struct.pack_into('>I',b,o,v & 0xFFFFFFFF)

def check_range(b,o,n,label):
    if o < 0 or n < 0 or o+n > len(b):
        raise ValueError(f'{label} range 0x{o:X}+0x{n:X} exceeds file size 0x{len(b):X}')

def write_cmd(buf,off,w0,w1):
    p32(buf,off,w0); p32(buf,off+4,w1)

def translate_f3dex2(buf,gfx_off):
    check_range(buf,gfx_off,8,'gfx header')
    count=u32(buf,gfx_off)
    check_range(buf,gfx_off+8,count*8,'gfx commands')
    hist=Counter()
    for i in range(count):
        off=gfx_off+8+i*8; op=buf[off]; hist[op]+=1
        if op < 0xE4 and op not in ALLOWED_F3DEX:
            raise ValueError(f'unsupported non-RDP F3DEX opcode 0x{op:02X} at command {i}')
        if op >= 0xE4:
            if op in (0xF0,0xF5) and buf[off+4] == 0x01: buf[off+4]=0x06
            continue
        if op==0x01: buf[off]=0xDA
        elif op==0x03: buf[off]=0xDC
        elif op==0x04:
            n=buf[off+2]//4
            if n==0: raise ValueError(f'VTX command {i} decoded zero vertices')
            buf[off]=0x01; buf[off+1]=(n>>4)&0xFF; buf[off+2]=(n<<4)&0xFF; buf[off+3]=(n*2)&0xFF
        elif op==0x06: buf[off]=0xDE
        elif op==0xB1: buf[off]=0x06
        elif op==0xB2: buf[off]=0x02
        elif op==0xB3: buf[off]=0xF1
        elif op==0xB4: buf[off]=0xE1
        elif op==0xB5: buf[off]=0x07
        elif op==0xB6:
            clear_bits=u32(buf,off+4)
            write_cmd(buf,off,0xD9000000|((~clear_bits)&0x00FFFFFF),0)
        elif op==0xB7:
            set_bits=u32(buf,off+4)
            write_cmd(buf,off,0xD9FFFFFF,set_bits)
        elif op==0xB8: write_cmd(buf,off,0xDF000000,0)
        elif op==0xB9: buf[off]=0xE2
        elif op==0xBA: buf[off]=0xE3
        elif op==0xBB:
            buf[off]=0xD7
            if buf[off+3]==0x01: buf[off+3]=0x02
        elif op==0xBC: buf[off]=0xDB
        elif op==0xBD: buf[off]=0xD8
        elif op==0xBE: buf[off]=0x03
        elif op==0xBF:
            a,b,c=buf[off+5],buf[off+6],buf[off+7]
            buf[off]=0x05; buf[off+1]=a; buf[off+2]=b; buf[off+3]=c
            buf[off+5]=buf[off+6]=buf[off+7]=0
    return hist

def convert(inp: bytes):
    if len(inp)<BK_HEADER_SIZE: raise ValueError('input too small')
    if u32(inp,0)!=0x0B: raise ValueError(f'unexpected magic 0x{u32(inp,0):08X}')
    if u16(inp,0x08)!=0x38: raise ValueError(f'expected BK texture setup 0x38, got 0x{u16(inp,0x08):04X}')
    tex_old=0x38; check_range(inp,tex_old,8,'texture header')
    tex_size_old=u32(inp,tex_old); tex_count=u16(inp,tex_old+4); tex_flag=u16(inp,tex_old+6)
    if tex_flag!=0: raise ValueError(f'external/special texture flag 0x{tex_flag:04X} unsupported in first pass')
    old_desc_start=tex_old+8; old_desc_end=old_desc_start+tex_count*0x10
    check_range(inp,old_desc_start,tex_count*0x10,'texture descriptors')
    old_ptrs={f:u32(inp,f) for f in ROOT_PTR_FIELDS}
    tri_count=u16(inp,0x30); root_vtx_count=u16(inp,0x32)
    header=bytearray(BT_TEXTURE_OFFSET); header[:0x30]=inp[:0x30]
    p16(header,0x08,0x50); p16(header,0x44,tri_count); p16(header,0x46,root_vtx_count)
    tex_hdr=bytearray(inp[tex_old:tex_old+8]); compact=bytearray()
    for i in range(tex_count):
        d=old_desc_start+i*0x10; compact+=inp[d:d+6]+inp[d+8:d+10]
    shrink=tex_count*8; delta=(BT_TEXTURE_OFFSET-BK_HEADER_SIZE)-shrink
    if tex_size_old<shrink: raise ValueError('texture size field smaller than descriptor shrink')
    p32(tex_hdr,0,tex_size_old-shrink)
    out=header+tex_hdr+compact+inp[old_desc_end:]
    for field,old in old_ptrs.items():
        if old==0: p32(out,field,0); continue
        if old<old_desc_end: raise ValueError(f'root +0x{field:02X} points inside texture descriptor area')
        p32(out,field,old+delta)
    vtx=u32(out,0x10); check_range(out,vtx,0x18,'vertex header')
    bk_count=u16(out,vtx+0x14); bk_global=u16(out,vtx+0x16)
    if bk_count*2>0xFFFF: raise ValueError('vertex count too large for BT count*2 encoding')
    p16(out,vtx+0x14,bk_global); p16(out,vtx+0x16,bk_count*2)
    gfx=u32(out,0x0C); hist=translate_f3dex2(out,gfx)
    if u16(out,0x08)!=0x50 or u16(out,0x44)!=tri_count or u16(out,0x46)!=bk_count: raise ValueError('post-conversion header validation failed')
    if u16(out,vtx+0x16)!=bk_count*2: raise ValueError('post-conversion vertex header validation failed')
    for field in (0x04,0x0C,0x10,0x1C):
        ptr=u32(out,field)
        if ptr==0 or ptr>=len(out): raise ValueError(f'candidate +0x{field:02X} pointer invalid: 0x{ptr:X}')
    return bytes(out), {
        'input_size':len(inp),'output_size':len(out),'texture_count':tex_count,'shrink':shrink,'delta':delta,
        'tri_count':tri_count,'vertex_count':bk_count,'gfx_commands':u32(out,gfx),'old_ptrs':old_ptrs,
        'new_ptrs':{f:u32(out,f) for f in ROOT_PTR_FIELDS},'hist':dict(sorted(hist.items()))
    }

def report(src,dst,r):
    print('='*76); print(f'converted: {src}'); print(f'       -> {dst}')
    print(f"size: 0x{r['input_size']:X} -> 0x{r['output_size']:X}")
    print(f"textures={r['texture_count']} shrink=0x{r['shrink']:X} net relocation={r['delta']:+#x}")
    print(f"triangles(root)={r['tri_count']} vertices={r['vertex_count']} gfxCommands={r['gfx_commands']}")
    print('root pointer relocation:')
    for f in ROOT_PTR_FIELDS:
        a,b=r['old_ptrs'][f],r['new_ptrs'][f]
        if a or b: print(f'  +0x{f:02X}: 0x{a:08X} -> 0x{b:08X}')
    print('source F3DEX opcode histogram:'); print('  '+' '.join(f'{k:02X}:{v}' for k,v in r['hist'].items()))
    print('validation: PASS')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('inputs',nargs='+',type=Path)
    ap.add_argument('--out-dir',type=Path,default=Path('research/project-a/bt-candidates'))
    args=ap.parse_args(); args.out_dir.mkdir(parents=True,exist_ok=True); failures=0
    for src in args.inputs:
        try:
            converted,r=convert(src.read_bytes()); dst=args.out_dir/(src.stem+'.btcandidate.bin'); dst.write_bytes(converted); report(src,dst,r)
        except Exception as exc:
            failures+=1; print('='*76); print(f'FAILED: {src}'); print(f'reason: {exc}')
    return 1 if failures else 0

if __name__=='__main__': raise SystemExit(main())
