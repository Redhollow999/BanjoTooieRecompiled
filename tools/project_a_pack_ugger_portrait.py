"""Pack model-rendered Ugger poses into the retail BT Banjo CI8 template.

Retains the complete native header/frame table/geometry sections. Only shared
RGBA16 palette and ten 32x32 pixel arrays are replaced. No ROM is modified.
"""
import hashlib
import json
import struct
import zlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from project_a_render_ugger_portrait import Model, OUT, SOURCE

def main():
    model=Model()
    # First six are mouth positions. Native gczoombox reserves the final four
    # of a ten-frame sprite for its alternate/idle frame range. Keep those
    # neutral rather than putting the shocked reaction there.
    phases=[0,.10,.14,.16,.18,.20,0,0,0,0]
    renders=[model.render('01E9.ugger-reaction',p,span=180,center=(0,55,0),size=384,head_only=True) for p in phases]
    boxes=[im.getbbox() for im in renders]
    bbox=(min(x[0] for x in boxes)-5,min(x[1] for x in boxes)-5,max(x[2] for x in boxes)+5,max(x[3] for x in boxes)+5)
    edge=max(bbox[2]-bbox[0],bbox[3]-bbox[1]);cx=(bbox[0]+bbox[2])/2;cy=(bbox[1]+bbox[3])/2
    crop=(round(cx-edge/2),round(cy-edge/2),round(cx+edge/2),round(cy+edge/2))
    frames=[]
    for i,im in enumerate(renders):
        frame=im.crop(crop).resize((30,30),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(32,32));canvas.alpha_composite(frame,(1,1))
        a=canvas.getchannel('A').point(lambda n:255 if n>=100 else 0)
        outline=a.filter(ImageFilter.MaxFilter(3))
        border=Image.new('RGBA',(32,32),(10,18,5,255));border.putalpha(outline)
        canvas.putalpha(a);border.alpha_composite(canvas);frames.append(border)
        # NPCs occupy the lower box: mirror across the vertical axis to face
        # the opposite way. Quantize the canonical view before reversing its
        # index rows, preserving the shared palette exactly.
        border.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(OUT/f'portrait-frame-{i:02}.png')
    atlas=Image.new('RGB',(320,32))
    for i,im in enumerate(frames):atlas.paste(im.convert('RGB'),(i*32,0))
    quant=atlas.quantize(colors=255,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    palette=quant.getpalette();palwords=[0]
    for i in range(255):
        r,g,b=palette[i*3:i*3+3];palwords.append(((r*31+127)//255<<11)|((g*31+127)//255<<6)|((b*31+127)//255<<1)|1)
    data=bytearray((SOURCE/'0B89.banjo-portrait.bin').read_bytes())
    base=struct.unpack_from('>h',data,18)[0];assert base==152
    data[base:base+512]=struct.pack('>256H',*palwords)
    arr=np.array(quant)
    for i,im in enumerate(frames):
        desc=28+i*12;off=base+struct.unpack_from('>I',data,desc+8)[0]
        assert off+struct.unpack_from('>h',data,desc+6)[0]==base
        indices=arr[:,i*32:(i+1)*32].astype(np.uint16)+1
        indices[np.array(im)[:,:,3]==0]=0
        data[off:off+1024]=indices[:,::-1].astype(np.uint8).tobytes()
    original=(SOURCE/'0B89.banjo-portrait.bin').read_bytes();tail=struct.unpack_from('>I',data,20)[0]
    assert len(data)==13304 and data[:base]==original[:base] and data[tail:]==original[tail:]
    path=OUT/'ugger.bt-sprite.bin';path.write_bytes(data)
    # Decode the actual candidate bytes for the preview, including RGBA16 loss.
    words=np.array(palwords,dtype=np.uint32)
    rgba=np.stack([((words>>11)&31)*255//31,((words>>6)&31)*255//31,((words>>1)&31)*255//31,(words&1)*255],axis=-1).astype(np.uint8)
    sheet=Image.new('RGBA',(10*112,140),(35,36,41,255));draw=ImageDraw.Draw(sheet)
    decoded=[]
    for i in range(10):
        off=base+struct.unpack_from('>I',data,28+i*12+8)[0]
        pixels=np.frombuffer(data[off:off+1024],dtype=np.uint8).reshape(32,32)
        im=Image.fromarray(rgba[pixels]);decoded.append(im)
        sheet.alpha_composite(im.resize((96,96),Image.Resampling.NEAREST),(i*112+8,4))
        draw.text((i*112+8,108),f'{i}: '+('mouth' if i<6 else 'neutral'),fill='white')
    sheet.save(OUT/'native-sprite-contact-sheet.png')
    animation=[decoded[i].resize((192,192),Image.Resampling.NEAREST) for i in [0,1,2,3,4,5,4,3,2,1,0,0]]
    animation[0].save(OUT/'ugger-talking-preview.gif',save_all=True,append_images=animation[1:],duration=110,loop=0,disposal=2)
    manifest={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc32':f'{zlib.crc32(data):08x}','format':'native BT CI8/shared RGBA16 palette','frames':10,'dimensions':[32,32],'orientation':'Mirrored across vertical axis (left/right) for lower NPC textbox.','source_animation':'01E9','normalized_phases':phases,'fixed_crop_384':crop,'template_sha256':hashlib.sha256(original).hexdigest(),'preserved':'All 152 header/frame-table bytes and both geometry sections after offset 10904, byte-for-byte.','frame_policy':'0..5 mouth progression; 6..9 neutral for native alternate/idle frame range. No fabricated blink.','status':'Offline candidate; game acceptance pending.'}
    (OUT/'sprite-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))

if __name__=='__main__':main()
