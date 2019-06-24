#!/usr/bin/env python3

#####################################################
#                                                   #
#       Shellcode dev and testing environment       #
#           Written by Philippe Dugre               #
#                                                   #
#####################################################


import ctypes, struct, binascii, argparse, socket
from keystone import *


def sockaddr(address, port):
    familly = struct.pack('H', socket.AF_INET)
    portbytes = struct.pack('H', socket.htons(port))
    ipbytes = socket.inet_aton(address)
    number = struct.unpack('Q', familly + portbytes + ipbytes)
    number = ~number[0]        #negate
    return "0x" + binascii.hexlify(struct.pack('>q', number)).decode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        type=argparse.FileType('r'),
                        help="File containing the assembly code.")
    parser.add_argument("-a",
                        "--address",
                        type=str,
                        default="127.0.0.1",
                        help="Address to connect back to")
    parser.add_argument("-p",
                        "--port",
                        type=int,
                        default=4444,
                        help="Port to connect back to")

    args = parser.parse_args()
    assembly_code = args.file.read()
    assembly_code = assembly_code.replace("{{address}}", sockaddr(args.address, args.port))

    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    machine_code, count = ks.asm(assembly_code)
    
    print("Number of instructions: " + str(count))
    
    # Packs it and put in in a bytearray...
    buf = b''
    for i in machine_code:
        buf += struct.pack("B", i)
    
    buf = bytearray(buf)
   
    # Print shellcode in a copy-pasteable format
    print("\nShellcode length: %d\n" % len(buf))
    print(format_shellcode(buf) + "\n")

    # Load libraries
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    libpthread = ctypes.cdll.LoadLibrary("libpthread.so.0")
    
    # Put the shellcode into a ctypes valid type.
    buf = (ctypes.c_char * len(buf)).from_buffer(buf)
    
    # Both function returns 64bits pointers
    libc.malloc.restype = ctypes.POINTER(ctypes.c_int64)
    libc.mmap.restype = ctypes.POINTER(ctypes.c_int64)
    
    # Get page size for mmap
    page_size = libc.getpagesize()
    
    # mmap acts like malloc, but can also set memory protection so we can create a Write/Execute buffer
    # void *mmap(void *addr, size_t len, int prot, int flags,
    #   int fildes, off_t off); 
    ptr = libc.mmap(ctypes.c_int64(0),      # NULL
            ctypes.c_int(page_size),        # Pagesize, needed for alignment 
            ctypes.c_int(0x07),             # Read/Write/Execute: PROT_READ | PROT_WRITE | PROT_EXEC 
            ctypes.c_int(0x21),             # MAP_ANONYMOUS | MAP_SHARED
            ctypes.c_int(-1),               # No file descriptor
            ctypes.c_int(0))                # No offset
    
    # Copy shellcode to newly allocated page.
    libc.memcpy(ptr,                        # Destination of our shellcode
                buf,                        # Shellcode location in memory
                ctypes.c_int(len(buf)))     # Nomber of bytes to copy
    
    # Allocate space for pthread_t object.
    # Note that pthread_t is 8 bytes long, so we'll treat it as an opaque int64 for simplicity
    thread = libc.malloc(ctypes.c_int(8))
    
    # Create pthread in the buffer.
    # int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
    #   void *(*start_routine) (void *), void *arg);
    libpthread.pthread_create(thread,       # The pthread_t structure pointer where the thread id will be stored
                            ctypes.c_int(0),# attributes = NULL
                            ptr,            # Our shellcode, which is what we want to execute
                            ctypes.c_int(0))# NULL, as we don't pass arguments
    
    # Wait for the thread.
    # int pthread_join(pthread_t thread, void **retval);
    libpthread.pthread_join(thread.contents,# Here, we pass the actual thread object, not a pointer to it
                        ctypes.c_int(0))# Null, as we don't expect a return value

# Function to format shellcode to a printable output. Modify according to the language you use.
def format_shellcode(shellcode):
    LINE_LENGTH=40
    raw = binascii.hexlify(shellcode)
    escaped = (b"\\x" + b"\\x".join(raw[i:i+2] for i in range (0, len(raw), 2))).decode('utf-8')
    lines = [escaped[i: i+LINE_LENGTH] for i in range(0, len(escaped), LINE_LENGTH)]
    return "shellcode = \tb\"" + "\nshellcode += \tb\"".join(lines) + "\""

if(__name__ == "__main__"):
	main()
