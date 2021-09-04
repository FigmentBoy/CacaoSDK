section .text

%macro defit 2
global %1
%1:
    mov rax, [rel _asmBase]
    add rax, %2
    jmp rax
%endmacro

extern __Z7getBasev
global __Z10setAsmBasev
__Z10setAsmBasev:
    push rbp
    mov rbp, rsp

    call __Z7getBasev
    mov [rel _asmBase], rax

    call __Z13setCommonRTTIv

    mov rax, [rel _asmBase]
    

    pop rbp
    ret

extern _memcpy

__Z13setCommonRTTIv:
    push rbp
    mov rbp, rsp

    lea rdi, [rel __ZTI10CommonRTTI]
    mov rsi, [rel _asmBase]
    add rsi, 0x624f70
    mov rdx, 0x20
    call _memcpy

    lea rdi, [rel __ZTV10CommonRTTI]
    mov rsi, [rel _asmBase]
    add rsi, 0x6247b0
    mov rdx, 0x360
    call _memcpy

    lea rdi, [rel __ZTS10CommonRTTI]
    mov rsi, [rel _asmBase]
    add rsi, 0x50ea90
    mov rdx, 0x12
    call _memcpy

    pop rbp
    ret


global __ZN5GDObj9valOffsetEl
__ZN5GDObj9valOffsetEl:
    lea rax, [rdi+rsi]
    ret

global __ZN5GDObj12setValOffsetElPv
__ZN5GDObj12setValOffsetElPv:
    mov [rdi+rsi], rdx
    ret

global __ZN11GameManager7manFileEv
__ZN11GameManager7manFileEv:
    lea rax, [rdi+0x120]
    ret


global __ZN7cocos2d2ui6MarginC1Ev
__ZN7cocos2d2ui6MarginC1Ev:
    push rbp
    mov rbp, rsp
    pop rbp
    ret

global __ZN11GameManager17setSecondColorIdxEi
__ZN11GameManager17setSecondColorIdxEi:
    mov [rdi+0x260], esi
    mov dword [rdi+0x264], 0
    ret
global __ZN11GameManager16setFirstColorIdxEi
__ZN11GameManager16setFirstColorIdxEi:
    mov [rdi+0x254], esi
    mov dword [rdi+0x258], 0
    ret

%macro thunk 3
global %1
%1:
    add rdi, -%3
    jmp %2
%endmacro

%macro nul 1
    global %1
    %1: 
%endmacro
