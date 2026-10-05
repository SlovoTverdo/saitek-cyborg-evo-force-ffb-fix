.intel_syntax noprefix
.text
.global invoke
invoke:
 push rbx
 push rsi
 push rdi
 mov rax,rdi
 mov r9,r8
 mov r8,rcx
 mov rcx,rsi
 call rax
 pop rdi
 pop rsi
 pop rbx
 ret
.section .note.GNU-stack,"",@progbits
