#include "heap.h"

#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

#define max(a, b) (a > b ? a : b)

/* NOTES

  We are actually cheating slightly in these challenges to make them
  easier: The heap works on top of glibc memory, meaning that it cannot
  replace the standard libc allocator (as that would cause recursion)

  This makes the heap a lot easier to understand, predict, and manipulate.

**/

/* -------------- */
/* Forward decl   */
/* -------------- */
void *heap_alloc(size_t needed, heap_t *heap);
void heap_free(void *data, heap_t *heap);

/* -------------- */
/* API            */
/* -------------- */
PHEAP HeapCreate()
{
    PHEAP heap = malloc(sizeof(HEAP));
    heap->chunks = NULL;

    heap->alloc = heap_alloc;
    heap->free = heap_free;
    return heap;
}

void *HeapAlloc(PHEAP heap, size_t size)
{
    if (!size || !heap)
        return NULL;
    return heap->alloc(size, heap);
}

void HeapFree(PHEAP heap, void *data)
{
    if (!data || !heap)
        return;
    heap->free(data, heap);
}

/* ---------------------- */
/* PRIVATE IMPLEMENTATION */
/* ---------------------- */
chunk_t *heap_grow(heap_t *heap, size_t size)
{
    chunk_t *chunk = malloc(sizeof(chunk_t));

    /* Alignment wastes precious RAMs. Our PROgrammers say that it's sub-optimal. */
    alloc_t *alloc = malloc(size + sizeof(alloc_t));
    dbg("GROW: chunk=%p alloc=%p\n", chunk, alloc);

    /* Setup first freelist entry. */
    alloc->chunk = chunk;
    alloc->size = size;
    alloc->free = 1;
    alloc->next = NULL;

    /* Setup the chunk with a single allocation. */
    chunk->heap = heap;
    chunk->allocs = alloc;
    chunk->next = NULL;

    return chunk;
}

void heap_coalesce(chunk_t *chunk)
{
    /* Merge all consecutive freed up allocs into a single big alloc. */
    for (alloc_t *alloc = chunk->allocs; alloc ; alloc = alloc->next)
    {
        if (!alloc->free)
            continue;

        alloc_t *next = alloc->next;
        while (next && next->free)
        {
            size_t size = next->size + sizeof(alloc_t);
            dbg("COALESCE: alloc=%p before=%ld after=%ld\n", alloc, alloc->size, alloc->size + size);
            alloc->size += size;
            next = next->next;
            alloc->next = next;
        }
    }
}

void *heap_alloc(size_t needed, heap_t *heap)
{
    dbg("ALLOC: heap=%p size=%ld\n", heap, needed);
    if (!heap)
        return NULL;

    /* Look for the first chunk with enough free space to satisfy the allocation. */
    chunk_t *chunk = heap->chunks;
    chunk_t *prev = NULL;
    alloc_t *f = NULL;

    while (chunk)
    {
        for (f = chunk->allocs; f && (!f->free || f->size < needed); f = f->next)
            ;

        if (f)
            break;
        prev = chunk;
        chunk = chunk->next;
    }
    dbg("ALLOC: chunk=%p\n free=%p prev=%p\n", chunk, f, prev);

    /* No chunk with enough free space. Add a new chunk. */
    if (!f)
    {
        assert(chunk == NULL);

        chunk = heap_grow(heap, max(needed, HEAP_CHUNK_SIZE));

        /* Enroll the chunk in the heap. */
        if (prev)
            prev->next = chunk;
        else
            heap->chunks = chunk;

        f = chunk->allocs;
    }

    /* Use the required space and mark the allocation as taken. */
    assert(f != NULL);

    if (f->size - needed > sizeof(alloc_t))
    {
        /*
         * Split the free block so that the unneeded bytes make up a new block
         * between this allocation and the next.
         *
         * This is only done if there are enough bytes left for an alloc_t header,
         * Otherwise the bytes are kept in the new allocation as padding.
         */

        alloc_t *next = (alloc_t*)(((uint8_t *)(f + 1)) + needed);
        next->chunk = chunk;
        next->size = f->size - needed - sizeof(alloc_t); // TODO: Off by one?
        next->free = 1;
        next->next = f->next;

        f->next = next;
        f->size = needed;
        dbg("SPLIT: alloc=%p alloc->size=%ld next=%p next->size=%ld\n", f, f->size, next, next->size);
    }

    f->free = 0;

    /* Skip past alloc_t header. */
    return (void *)(f + 1);
}

void heap_free(void *data, heap_t *heap)
{
    if (!heap || !data)
        return;

    alloc_t *alloc = ((alloc_t *)(data)) - 1;
    alloc->free = 1;

    heap_coalesce(alloc->chunk);
}