#ifndef HEAP_H
#define HEAP_H

#include <stddef.h>
#include <stdint.h>

#ifdef DEBUG
#define dbg printf
#else
#define dbg if (0) printf
#endif

// #pragma push(pack, 1)

#define HEAP_CHUNK_SIZE (1024 * 1024 * 4) /* 4 MB */

struct heap_;
struct alloc_;
struct chunk_;

/* Allocator typedefs */
typedef void *(*new_f)(size_t, struct heap_*);
typedef void (*free_f)(void *, struct heap_*);


/**
 * Heap chunk metadata.
 *
 * A chunk of heap is a contiguous portion of memory
 * in which allocations can be made. Chunks are dynamically
 * allocated when the heap fills.
 **/
typedef struct chunk_
{
    struct heap_ *heap;
    struct alloc_ *allocs;
    struct chunk_ *next;
} chunk_t;

/**
 * An allocation header.
 *
 **/
typedef struct alloc_
{
    chunk_t *chunk;      /*< The chunk this allocation belongs to. */
    size_t size;         /*< Total size of the allocation excluding the header. */
    uint8_t free;        /*< Whether this allocation is free. */
    struct alloc_ *next; /*< Pointer to the next allocation. (Used for free lists) */
} alloc_t;

/**
 * Heap descriptor.
 *
 * This type stores metadata about a heap.
 *
 * Our heaps are too good to support realloc() because PROgrammers
 * never need to resize a buffer.
 **/
typedef struct heap_
{
    chunk_t *chunks; /*< Chunk list. */
    free_f free;     /*< The Allocator's free() function. */
    new_f alloc;     /*< The Allocator's malloc() function. */

} HEAP, heap_t;
typedef HEAP *PHEAP;

/** Create a new heap to work on. **/
PHEAP HeapCreate();

/**
 * Allocates memory on the given heap.
 * @param heap The heap to perform the allocation on.
 * @param size The number of bytes to allocate.
 *
 * @return A pointer to the allocated memory or NULL if allocation failed.
 **/
void *HeapAlloc(PHEAP heap, size_t size);

/**
 *  Frees allocated memory on the given heap.
 *
 *  @param heap The heap that owns the allocated data.
 *  @param data Pointer to the data to free.
 **/
void HeapFree(PHEAP heap, void *data);

// #pragma pop(pack)

#endif /* HEAP_H */