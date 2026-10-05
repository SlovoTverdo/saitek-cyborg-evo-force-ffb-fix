.intel_syntax noprefix
.text
.p2align 4
.global patch_1303
patch_1303:
mov rbx,rcx
bt r9d,31
jc p1303_skip
mov r11, [rcx+0x18]
xor rsi, rsi
test edx, edx
jz p1303_bad
p1303_loop:
test r11,r11
jz p1303_done
mov rax,[r11]
cmp eax,edx
jne p1303_next
test rsi,rsi
jnz p1303_bad
mov rsi,rax
p1303_next:
mov r11,[r11+0x10]
jmp p1303_loop
p1303_done:
test rsi,rsi
jz p1303_bad
jmp 0x1000130e
p1303_skip:
mov esi,edx
jmp 0x1000130a
p1303_bad:
mov eax,0x80070057
jmp 0x10001357
.global patch_1303_end
patch_1303_end:
.p2align 4
.global patch_13a0
patch_13a0:
mov esi,r9d
mov r11, [rcx+0x18]
xor rbx, rbx
test edx, edx
jz p13a0_bad
p13a0_loop:
test r11,r11
jz p13a0_done
mov rax,[r11]
cmp eax,edx
jne p13a0_next
test rbx,rbx
jnz p13a0_bad
mov rbx,rax
p13a0_next:
mov r11,[r11+0x10]
jmp p13a0_loop
p13a0_done:
test rbx,rbx
jz p13a0_bad
jmp 0x100013ae
p13a0_bad:
mov eax,0x80070057
jmp 0x100013dd
.global patch_13a0_end
patch_13a0_end:
.p2align 4
.global patch_1400
patch_1400:
mov r11, [rcx+0x18]
xor rcx, rcx
test edx, edx
jz p1400_bad
p1400_loop:
test r11,r11
jz p1400_done
mov rax,[r11]
cmp eax,edx
jne p1400_next
test rcx,rcx
jnz p1400_bad
mov rcx,rax
p1400_next:
mov r11,[r11+0x10]
jmp p1400_loop
p1400_done:
test rcx,rcx
jz p1400_bad
jmp 0x10006b90
p1400_bad:
mov eax,0x80070057
ret
.global patch_1400_end
patch_1400_end:
.p2align 4
.global patch_1426
patch_1426:
mov rbx,r8
test r8,r8
jz p1426_bad
mov r11, [rcx+0x18]
xor rcx, rcx
test edx, edx
jz p1426_bad
p1426_loop:
test r11,r11
jz p1426_done
mov rax,[r11]
cmp eax,edx
jne p1426_next
test rcx,rcx
jnz p1426_bad
mov rcx,rax
p1426_next:
mov r11,[r11+0x10]
jmp p1426_loop
p1426_done:
test rcx,rcx
jz p1426_bad
jmp 0x1000143a
p1426_bad:
mov eax,0x80070057
jmp 0x10001452
.global patch_1426_end
patch_1426_end:
.p2align 4
.global patch_3156
patch_3156:
mov rsi,rcx
mov edi,edx
cmp edx,16
ja p3156_bad
mov eax,edx
imul rax,rax,0x580
lea r11,[rcx+rax+0x2b0]
mov r11, [r11+0x18]
xor rbx, rbx
test r8d, r8d
jz p3156_bad
p3156_loop:
test r11,r11
jz p3156_done
mov rax,[r11]
cmp eax,r8d
jne p3156_next
test rbx,rbx
jnz p3156_bad
mov rbx,rax
p3156_next:
mov r11,[r11+0x10]
jmp p3156_loop
p3156_done:
test rbx,rbx
jz p3156_bad
jmp 0x10003165
p3156_bad:
jmp 0x10003196
.global patch_3156_end
patch_3156_end:
.p2align 4
.global patch_3244
patch_3244:
mov r8,r9
imul rax,rax,0x580
lea rcx,[rax+rcx+0x10]
mov r11, [rcx+0x2b8]
xor rdx, rdx
test r10d, r10d
jz p3244_bad
p3244_loop:
test r11,r11
jz p3244_done
mov rax,[r11]
cmp eax,r10d
jne p3244_next
test rdx,rdx
jnz p3244_bad
mov rdx,rax
p3244_next:
mov r11,[r11+0x10]
jmp p3244_loop
p3244_done:
test rdx,rdx
jz p3244_bad
jmp 0x10003256
p3244_bad:
mov eax,0x80070057
ret
.global patch_3244_end
patch_3244_end:
.section .note.GNU-stack,"",@progbits
