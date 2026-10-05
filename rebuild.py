"""Rebuild patch code and symbol manifest with GNU binutils; no vendor DLL needed."""
from pathlib import Path
import json,subprocess,tempfile,sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'make_asm.py')],check=True)
with tempfile.TemporaryDirectory(prefix='saitek-ffb-') as tmp:
 obj=Path(tmp)/'patch.o';elf=Path(tmp)/'patch.elf'
 subprocess.run(['as','--64','-o',str(obj),str(root/'patch.S')],check=True)
 subprocess.run(['ld','-Ttext=0x1002e000','-e','patch_1303','-o',str(elf),str(obj)],check=True)
 subprocess.run(['objcopy','-O','binary','--only-section=.text',str(elf),str(root/'patch.bin')],check=True)
 symbols={}
 for line in subprocess.check_output(['nm','-n',str(elf)],text=True).splitlines():
  addr,kind,name=line.split()
  if name.startswith('patch_'):symbols[name]=int(addr,16)-0x10000000
 (root/'symbols.json').write_text(json.dumps(symbols,indent=2)+'\n')
print('Rebuilt patch.S, patch.bin and symbols.json. Vendor DLL not modified.')
