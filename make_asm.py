from pathlib import Path
s=['.intel_syntax noprefix','.text']
def lookup(tag,dst,low,head,fail):
 return f'''mov r11, {head}
xor {dst}, {dst}
test {low}, {low}
jz {fail}
{tag}_loop:
test r11,r11
jz {tag}_done
mov rax,[r11]
cmp eax,{low}
jne {tag}_next
test {dst},{dst}
jnz {fail}
mov {dst},rax
{tag}_next:
mov r11,[r11+0x10]
jmp {tag}_loop
{tag}_done:
test {dst},{dst}
jz {fail}
'''
def stub(name,code):
 s.extend(['.p2align 4',f'.global {name}',f'{name}:',code,f'.global {name}_end',f'{name}_end:'])
stub('patch_1303','''mov rbx,rcx
bt r9d,31
jc p1303_skip
'''+lookup('p1303','rsi','edx','[rcx+0x18]','p1303_bad')+'''jmp 0x1000130e
p1303_skip:
mov esi,edx
jmp 0x1000130a
p1303_bad:
mov eax,0x80070057
jmp 0x10001357''')
stub('patch_13a0','mov esi,r9d\n'+lookup('p13a0','rbx','edx','[rcx+0x18]','p13a0_bad')+'''jmp 0x100013ae
p13a0_bad:
mov eax,0x80070057
jmp 0x100013dd''')
stub('patch_1400',lookup('p1400','rcx','edx','[rcx+0x18]','p1400_bad')+'''jmp 0x10006b90
p1400_bad:
mov eax,0x80070057
ret''')
stub('patch_1426','''mov rbx,r8
test r8,r8
jz p1426_bad
'''+lookup('p1426','rcx','edx','[rcx+0x18]','p1426_bad')+'''jmp 0x1000143a
p1426_bad:
mov eax,0x80070057
jmp 0x10001452''')
stub('patch_3156','''mov rsi,rcx
mov edi,edx
cmp edx,16
ja p3156_bad
mov eax,edx
imul rax,rax,0x580
lea r11,[rcx+rax+0x2b0]
'''+lookup('p3156','rbx','r8d','[r11+0x18]','p3156_bad')+'''jmp 0x10003165
p3156_bad:
jmp 0x10003196''')
stub('patch_3244','''mov r8,r9
imul rax,rax,0x580
lea rcx,[rax+rcx+0x10]
'''+lookup('p3244','rdx','r10d','[rcx+0x2b8]','p3244_bad')+'''jmp 0x10003256
p3244_bad:
mov eax,0x80070057
ret''')
(Path(__file__).resolve().parent / 'patch.S').write_text('\n'.join(s)+'\n.section .note.GNU-stack,"",@progbits\n')
