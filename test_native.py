"""Run actual patch x64 instructions against synthetic owner lists on Linux.
Landing points are mocks: this does NOT load the Windows driver or test USB.
"""
import ctypes as c,mmap,struct,json
from pathlib import Path
root=Path(__file__).resolve().parent
symbols=json.loads((root/'symbols.json').read_text())
m=mmap.mmap(-1,0x31000,prot=mmap.PROT_READ|mmap.PROT_WRITE|mmap.PROT_EXEC)
m[0x2e000:0x2e000+len((root/'patch.bin').read_bytes())]=(root/'patch.bin').read_bytes()
landings={0x130e:'4889f0c3',0x130a:'31c0c3',0x1357:'c3',0x13ae:'4889d8c3',0x13dd:'c3',0x6b90:'4889c8c3',0x143a:'4889c8c3',0x1452:'c3',0x3165:'4889d8c3',0x3196:'b857000780c3',0x3256:'4889d0c3'}
for addr,h in landings.items():m[addr:addr+len(bytes.fromhex(h))]=bytes.fromhex(h)
base=c.addressof(c.c_char.from_buffer(m));bridge=c.CDLL(str(root/'test_bridge.so')).invoke
bridge.argtypes=[c.c_void_p,c.c_void_p,c.c_uint64,c.c_uint64,c.c_uint64];bridge.restype=c.c_uint64
class Node(c.Structure):_fields_=[('effect',c.c_uint64),('prev',c.c_uint64),('next',c.c_uint64)]
owner=c.create_string_buffer(0x30);device=c.create_string_buffer(0x6000);out=c.c_uint32()
def head(ptr):
 struct.pack_into('<Q',owner,0x18,ptr);struct.pack_into('<Q',device,0x2c8,ptr)
ptr=0x1234567812345678;n=Node(ptr,0,0);head(c.addressof(n));count=0
for name in [k for k in symbols if not k.endswith('_end')]:
 for case in ['valid','missing','empty','collision','zero']:
  n.effect=ptr;n.next=0;other=Node(ptr+(1<<32),0,0);head(c.addressof(n));handle=ptr&0xffffffff
  expected=ptr
  if case=='missing':handle+=8;expected=0x80070057
  if case=='empty':head(0);expected=0x80070057
  if case=='collision':n.next=c.addressof(other);expected=0x80070057
  if case=='zero':handle=0;expected=0x80070057
  if name=='patch_3156':o=c.addressof(device);a=0;b=handle;d=0
  elif name=='patch_3244':o=c.addressof(device);a=0;b=0;d=c.addressof(out)
  else:o=c.addressof(owner);a=handle;b=c.addressof(out);d=0
  # 3244 is entered after original mov r10d,r8d, and eax=slot.
  if name=='patch_3244':
   prefix=b'\x45\x89\xc2\x31\xc0'+b'\xe9'+struct.pack('<i',symbols[name]-0x2d100-10)
   m[0x2d100:0x2d100+len(prefix)]=prefix;b=handle;a=0;fn=base+0x2d100
  else:fn=base+symbols[name]
  got=bridge(fn,o,a,b,d);assert got==expected,(name,case,hex(got),hex(expected));count+=1
# Preserve pre-existing no-download path even without a handle.
head(0);assert bridge(base+symbols['patch_1303'],c.addressof(owner),0,0,0x80000000)==0;count+=1
# Reject invalid device indices before reading outside owner storage.
assert bridge(base+symbols['patch_3156'],c.addressof(device),17,ptr&0xffffffff,0)==0x80070057;count+=1
print(f'PASS: {count} native machine-code cases across six patch stubs')
