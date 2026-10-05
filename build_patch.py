"""Offline, exact-version patcher. Never installs or overwrites input files."""
import argparse,hashlib,json,struct
from pathlib import Path
EXPECTED='fbf17423e5cd778cd8d59768c5cbb71d3a24447eb7c34fbca8379b0f11dcaf5e'
ROOT=Path(__file__).resolve().parent
align=lambda n,a:(n+a-1)&-a

def patch(source):
 b=bytearray(source)
 if hashlib.sha256(b).hexdigest()!=EXPECTED:raise ValueError('Unsupported DLL SHA-256; refusing to patch')
 pe=struct.unpack_from('<I',b,60)[0];opt=pe+24;n=struct.unpack_from('<H',b,pe+6)[0];st=opt+struct.unpack_from('<H',b,pe+20)[0]
 sections=[struct.unpack_from('<IIII',b,st+40*i+8) for i in range(n)]
 def off(rva):
  for vs,va,sz,p in sections:
   if va<=rva<va+sz:return p+rva-va
  raise ValueError('RVA outside file')
 blob=bytearray((ROOT/'patch.bin').read_bytes());symbols=json.loads((ROOT/'symbols.json').read_text());base=0x2e000
 hooks=[(0x1303,'patch_1303','8bf2488bd9'),(0x13a0,'patch_13a0','418bf18bda'),(0x1400,'patch_1400','85d28bca75'),(0x1426,'patch_1426','85d2498bd88bca'),(0x3156,'patch_3156','418bd8488bf1'),(0x3244,'patch_3244','4d8bc1418bd2')]
 er,esz=struct.unpack_from('<II',b,opt+112+3*8);old=[struct.unpack_from('<III',b,off(er)+i) for i in range(0,esz,12)];new=[]
 for addr,name,h in hooks:
  expected=bytes.fromhex(h);pos=off(addr)
  if b[pos:pos+len(expected)]!=expected:raise ValueError('Unexpected hook bytes')
  target=symbols[name];b[pos:pos+len(expected)]=b'\xe9'+struct.pack('<i',target-addr-5)+b'\x90'*(len(expected)-5)
  blob.extend(b'\x00'*(align(len(blob),4)-len(blob)));urva=base+len(blob)
  original=next((t for t in old if t[0]<=addr<t[1]),None)
  if original is None:blob.extend(b'\x01\x00\x00\x00')
  else:
   blob.extend(b'\x21\x00\x00\x00'+struct.pack('<III',*original))
  new.append((target,symbols[name+'_end'],urva))
 blob.extend(b'\x00'*(align(len(blob),4)-len(blob)));pdata=base+len(blob);entries=sorted(old+new)
 blob.extend(b''.join(struct.pack('<III',*t) for t in entries))
 if st+40*(n+1)>0x400:raise ValueError('No room for section header')
 raw=align(len(b),512);b.extend(b'\x00'*(raw-len(b)));sz=align(len(blob),512);b.extend(blob);b.extend(b'\x00'*(raw+sz-len(b)))
 header=b'.ffbfix\x00'+struct.pack('<IIIIIIHHI',len(blob),base,sz,raw,0,0,0,0,0x60000020)
 b[st+40*n:st+40*(n+1)]=header
 struct.pack_into('<H',b,pe+6,n+1);struct.pack_into('<I',b,opt+4,struct.unpack_from('<I',b,opt+4)[0]+sz)
 struct.pack_into('<I',b,opt+56,align(base+len(blob),4096));struct.pack_into('<II',b,opt+112+3*8,pdata,len(entries)*12);struct.pack_into('<I',b,opt+64,0)
 # Standard PE checksum; field is currently zero.
 padded=b+b'\x00'*(len(b)%2);total=0
 for i in range(0,len(padded),2):total+=int.from_bytes(padded[i:i+2],'little');total=(total&65535)+(total>>16)
 total=(total&65535)+(total>>16);struct.pack_into('<I',b,opt+64,total+len(b))
 return bytes(b)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');args=ap.parse_args();out=Path(args.output)
 if out.exists():raise SystemExit('Output exists; refusing to overwrite')
 data=patch(Path(args.input).read_bytes());out.write_bytes(data);print('Created experimental DLL:',out);print('SHA-256:',hashlib.sha256(data).hexdigest())
