start:
    xor rax, rax;
    add al, 0xe7;
    push byte 42;
    pop rdi;
    syscall;
