"""Offline, owner-asset Ugger pose audition. No game or generated artwork.

Focused BT geo/F3DEX2 interpreter and CPU triangle rasterizer. Skeleton and
animation layout cross-checked against magcius/noclip.website (MIT); reference
source/license retained in the output reference directory. This is a portrait
exporter, not a complete N64 renderer. Native interpolation modes, lighting and
RDP filtering are approximated and recorded in the manifest.
"""
from pathlib import Path
import collections
import hashlib
import json
import math
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'research/project-a/ugger-portrait-reference-20261021'
OUT = ROOT/'research/project-a/ugger-portrait-prototype-20261024'

def u16(b,o): return struct.unpack_from('>H',b,o)[0]
def s16(b,o): return struct.unpack_from('>h',b,o)[0]
def u32(b,o): return struct.unpack_from('>I',b,o)[0]

def tracks(data):
    start,end,count,zero=struct.unpack_from('>4H',data)
    assert zero==0
    result={};off=8
    for _ in range(count):
        word,n=struct.unpack_from('>HH',data,off);off+=4
        keys=[]
        for j in range(n):
            time,value=struct.unpack_from('>Hh',data,off);off+=4
            keys.append((time&0x3fff,value/64))
        result[word>>4,(word&15)%9]=keys
    assert off<=len(data)
    return start,end,result

def translate(v):
    m=np.eye(4);m[:3,3]=v;return m

class Model:
    def __init__(self):
        self.b=(SOURCE/'0671.ugger-model.bin').read_bytes();b=self.b
        assert u32(b,0)==11 and u32(b,0x28)==0
        v=u32(b,16);self.v=b[v+24:v+24+u16(b,v+22)//2*16]
        d=u32(b,12);self.dl=b[d+8:d+8+u32(b,d)*8]
        a=u32(b,24);self.scale=struct.unpack_from('>f',b,a)[0]
        self.bones=[struct.unpack_from('>fffHh',b,a+8+i*16) for i in range(u16(b,a+4))]
        t=u16(b,8);count=b[t+5];base=t+8+count*8
        self.textures=[]
        for i in range(count):
            offset,typ,w,h=struct.unpack_from('>IHBB',b,t+8+i*8)
            assert typ==1 # this model uses four CI4/RGBA16-palette textures
            pal=np.frombuffer(b[base+offset:base+offset+32],dtype='>u2').astype(np.uint32)
            rgba=np.stack([((pal>>11)&31)*255//31,((pal>>6)&31)*255//31,((pal>>1)&31)*255//31,(pal&1)*255],axis=-1)
            packed=np.frombuffer(b[base+offset+32:base+offset+32+w*h//2],dtype=np.uint8)
            ix=np.stack([packed>>4,packed&15],axis=1).reshape(h,w)
            self.textures.append((offset+32,rgba[ix].astype(np.uint8)))
        self.tris=[];self.geo_hist=collections.Counter();self.op_hist=collections.Counter()
        self.walk(u32(b,4),-1,-1,self.state())

    @staticmethod
    def state():return {'cache':{},'depth':0,'tex':None,'on':False,'s':.5,'t':.5,'cms':0,'cmt':0}

    def dlrun(self,index,bone,parent,state):
        for i in range(index,len(self.dl)//8):
            w0,w1=struct.unpack_from('>II',self.dl,i*8);op=w0>>24;self.op_hist[op]+=1
            if op==0xdf:return
            if op==1:
                n=(w0>>12)&255;end=(w0&255)//2;first=end-n
                assert w1>>24==1 and first>=0
                for j in range(n):
                    off=(w1&0xffffff)+j*16
                    xyz=struct.unpack_from('>hhh',self.v,off)
                    uv=struct.unpack_from('>hh',self.v,off+8)
                    color=np.array(list(self.v[off+12:off+16]),float)/255
                    state['cache'][first+j]=(np.array([*xyz,1.]),np.array(uv)/32*np.array([state['s'],state['t']]),color,parent if state['depth'] else bone)
            elif op in (5,6):
                inds=[(w0>>16)&255,(w0>>8)&255,w0&255]
                if op==6:inds += [(w1>>16)&255,(w1>>8)&255,w1&255]
                for j in range(0,len(inds),3):
                    verts=[state['cache'][x//2] for x in inds[j:j+3]]
                    self.tris.append((verts,state['tex'] if state['on'] else None,state['cms'],state['cmt'],bone))
            elif op==0xd8:state['depth']=1
            elif op==0xda:state['depth']=(w1&0xffffff)//64
            elif op==0xd7:
                state.update(on=bool(w0&255),s=(w1>>16)/65536,t=(w1&65535)/65536)
            elif op==0xfd:
                addr=w1&0xffffff
                for k,(off,tex) in enumerate(self.textures):
                    if addr==off:state['tex']=k
            elif op==0xf5 and ((w1>>24)&7)==0:
                state.update(cms=(w1>>8)&3,cmt=(w1>>18)&3)
            elif op==0xde:
                if w1>>24==9:self.dlrun((w1&0xffffff)//8,bone,parent,state)
                else:assert w1>>24 in (3,7)
            else:assert op in (0xd9,0xe3,0xe7,0xfc,0xf0,0xf3,0xf2,0xf5), (hex(op),i)
        raise ValueError('No DL terminator')

    def walk(self,o,bone,parent,state):
        b=self.b
        while True:
            cmd,nxt=u32(b,o),u32(b,o+4);self.geo_hist[cmd]+=1
            if cmd==2:
                off,bi=struct.unpack_from('>Bb',b,o+8)
                if off:self.walk(o+off,bi,bone,self.state())
            elif cmd==0x11:self.dlrun(u16(b,o+8),bone,parent,state)
            elif cmd==0x18:
                self.dlrun(u16(b,o+8),bone,parent,state)
                at=o+10
                while u16(b,at):
                    state['depth']=0;self.dlrun(u16(b,at),bone,parent,state);at+=2
            else:raise ValueError(f'Unsupported geo {cmd:X}')
            if not nxt:return
            o+=nxt

    def pose(self,anim,phase):
        start,end,ts=tracks((SOURCE/f'{anim}.bin').read_bytes());frame=start+phase*(end-start)
        mats=[]
        for x,y,z,bi,parent in self.bones:
            values=[0.,0.,0.,1.,1.,1.,0.,0.,0.]
            for typ in range(9):
                if (bi,typ) in ts:
                    ks=ts[bi,typ];values[typ]=float(np.interp(frame,[k[0] for k in ks],[k[1] for k in ks]))
            rx,ry,rz=np.radians(values[:3]);cx,sx=math.cos(rx),math.sin(rx);cy,sy=math.cos(ry),math.sin(ry);cz,sz=math.cos(rz),math.sin(rz)
            mx=np.array([[1,0,0,0],[0,cx,-sx,0],[0,sx,cx,0],[0,0,0,1]])
            my=np.array([[cy,0,sy,0],[0,1,0,0],[-sy,0,cy,0],[0,0,0,1]])
            mz=np.array([[cz,-sz,0,0],[sz,cz,0,0],[0,0,1,0],[0,0,0,1]])
            local=translate(np.array(values[6:])*self.scale)@translate([x,y,z])@mz@my@mx@np.diag([*values[3:6],1])@translate([-x,-y,-z])
            mats.append((np.eye(4) if parent<0 else mats[parent])@local)
        return mats

    def render(self,anim,phase,yaw=20,center=(0,66,0),span=95,size=256,head_only=False):
        mats=self.pose(anim,phase);angle=math.radians(yaw)
        view=np.array([[math.cos(angle),0,-math.sin(angle)],[0,1,0],[math.sin(angle),0,math.cos(angle)]])
        img=np.zeros((size,size,4),dtype=np.uint8);depth=np.full((size,size),-np.inf)
        for verts,ti,cms,cmt,bone in self.tris:
            if head_only and bone not in (0,1):continue
            world=np.array([(mats[bi]@pos)[:3] if bi>=0 else pos[:3] for pos,uv,col,bi in verts])
            p=(world-np.array(center))@view.T
            q=np.stack([size/2+p[:,0]*size/span,size/2-p[:,1]*size/span],axis=1)
            xmin,ymin=np.maximum(np.floor(q.min(axis=0)).astype(int),0);xmax,ymax=np.minimum(np.ceil(q.max(axis=0)).astype(int),size-1)
            if xmin>xmax or ymin>ymax:continue
            a,b,c=q;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-6:continue
            yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
            wa=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
            wb=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;wc=1-wa-wb
            weights=np.stack([wa,wb,wc],axis=-1);z=weights@p[:,2]
            mask=(weights.min(axis=-1)>=-1e-5)&(z>depth[ymin:ymax+1,xmin:xmax+1])
            colors=weights@np.array([v[2] for v in verts])
            if ti is not None:
                tex=self.textures[ti][1];uv=weights@np.array([v[1] for v in verts]);ix=[]
                for axis,mode,n in [(0,cms,tex.shape[1]),(1,cmt,tex.shape[0])]:
                    coords=np.floor(uv[:,:,axis]).astype(int)
                    if mode&2:coords=np.clip(coords,0,n-1)
                    elif mode&1:coords=np.where((coords//n)&1,n-1-coords%n,coords%n)
                    else:coords%=n
                    ix.append(coords)
                colors*=tex[ix[1],ix[0]]/255
            mask &= colors[:,:,3]>.25
            dest=img[ymin:ymax+1,xmin:xmax+1];dest[mask]=np.clip(colors[mask]*255,0,255).astype(np.uint8)
            depth[ymin:ymax+1,xmin:xmax+1][mask]=z[mask]
        return Image.fromarray(img)

def main():
    OUT.mkdir(exist_ok=True);model=Model();sheet=Image.new('RGBA',(6*192,3*220),(35,36,41,255));draw=ImageDraw.Draw(sheet)
    poses=[]
    for row,anim in enumerate(['01E7.ugger-idle','01E9.ugger-reaction']):
        for col,phase in enumerate([0,.15,.3,.45,.6,.85]):
            im=model.render(anim,phase);name=f'{anim[:4]}-{phase:.2f}.png';im.save(OUT/name)
            preview=im.resize((192,192),Image.Resampling.LANCZOS);sheet.alpha_composite(preview,(col*192,row*220))
            draw.text((col*192+5,row*220+194),f'{anim[:4]} phase {phase:.2f}',fill='white');poses.append({'file':name,'animation':anim,'phase':phase})
    # Full body view and the four original textures aid visual diagnosis.
    model.render('01E7.ugger-idle',0,span=180,center=(0,45,0),size=512).save(OUT/'full-model.png')
    for i,(_,tex) in enumerate(model.textures):Image.fromarray(tex).resize((128,128),Image.Resampling.NEAREST).save(OUT/f'texture-{i}.png')
    sheet.crop((0,0,1152,440)).save(OUT/'pose-contact-sheet.png')
    report={'source_model_sha256':hashlib.sha256(model.b).hexdigest(),'triangles':len(model.tris),'bones':len(model.bones),'poses':poses,'camera':{'yaw_degrees':20,'center':[0,66,0],'orthographic_span':95},'limitations':['Linear keyframe interpolation; native tangent modes not reproduced.','Vertex colors/CI4 textures; native software lighting and RDP combiner/filter approximated.','Pose selection and final framing are provisional; not a game capture.'],'reference':'https://github.com/magcius/noclip.website','geo_commands':dict(model.geo_hist),'display_list_commands':dict(model.op_hist)}
    (OUT/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'triangles':len(model.tris),'bones':len(model.bones),'contact_sheet':str(OUT/'pose-contact-sheet.png')}))

if __name__=='__main__':main()
