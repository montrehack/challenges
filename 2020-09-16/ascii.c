#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
 * This heap is extremely efficient to store ASCII art.
 *
 * It has been developed by our C experts to have optimal performance compared to standard heaps.
 * Our professional grade benchmarks have shown that for sample sizes N=1 this heap outperforms GLIBC
 * by 10000%, and we know it is bug free because our experts know better than to write buggy software.
 *
 * BUGS:
 * - Fix 1x1 allocs.
 * - Fix Ctrl+D.
 * - Fix empty newline.
 */
#include "heap.h"

/* Canvas maximum dimension (250x250 ASCII characters.) */
#define MAX_CANVAS 250
#define CMD(x) (strncmp(x, c, sizeof(x)) == 0)

void canvas_load(char *);

typedef struct canvas_
{
    char *title;
    uint16_t width, height;
    uint16_t private;
    uint16_t id;
    char *data;
    struct canvas_ *next;
} canvas_t;

/* No one will ever find this one :) */
char flag_two[] = "FLAG-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";

PHEAP g_heap;
canvas_t *gallery = NULL;
int g_id = 1;

canvas_t *canvas_new(int w, int h)
{
    if (w < 1 || w > MAX_CANVAS || h < 1 || h > MAX_CANVAS)
        return NULL;

    canvas_t *c = HeapAlloc(g_heap, sizeof(canvas_t));
    c->width = w;
    c->height = h;
    c->private = 0;
    c->id = g_id++;
    c->next = NULL;
    c->title = HeapAlloc(g_heap, 16);
    /* fgets will add a NUL byte and includes the '\n', so account for that. */
    c->data = HeapAlloc(g_heap, w * h + 2);
    return c;
}

void canvas_del(canvas_t *canvas)
{
    if (!canvas)
        return;
    if (canvas->title)
        HeapFree(g_heap, canvas->title);
    if (canvas->data)
        HeapFree(g_heap, canvas->data);
    HeapFree(g_heap, canvas);
}

void canvas_append(canvas_t *canvas)
{
    if (!gallery)
    {
        gallery = canvas;
    }
    else
    {
        // append to list.
        canvas_t *n = gallery;
        while (n->next)
            n = n->next;
        n->next = canvas;
    }
}

int readint()
{
    char t[10] = {0};
    fgets(t, sizeof(t), stdin);

    int len = strlen(t);
    if (t[len - 1] == '\n')
        t[len - 1] = 0; /* trim newlines */

    return atoi(t);
}

canvas_t *canvas_find(int id, canvas_t **prev)
{
    canvas_t *c = gallery;

    while (c)
    {
        if (c->id == id)
            break;

        if (prev)
            *prev = c;
        c = c->next;
    }

    if (!c)
    {
        printf("[!] Canvas with id %d not found.\n", id);
        return NULL;
    }
    return c;
}

/* ACTION HANDLERS */
void help()
{
    printf("The following commands are supported:\n"
           "help       This help menu\n"
           "list       List the canvases available for perusal in the gallery\n"
           "show <id>  View the given art piece.\n"
           "new        Add a new work of art to the gallery\n"
           "del <id>   Remove a canvas from the gallery\n"
           "edit <id>  Alter the given canvas' art\n"
           "exit       Leave the ASCII Art gallery\n");
}

void list()
{
    printf("-- Gallery --\n");
    canvas_t *c = gallery;

    if (!c)
    {
        printf("    No art found!\n");
        return;
    }

    while (c)
    {
        printf("%8d - %s\n", c->id, c->title);
        c = c->next;
    }
}

void show(int id)
{
    canvas_t *c = canvas_find(id, NULL);
    if (!c)
        return;

    /* printf("-- %s (%dx%d) --\n\n", c->title, c->width, c->height); */

    if (c->private)
    {
        printf("[!] This canvas is part of private exposition, you may not view it at this time.\n");
        return;
    }

    /* Render the ASCII art faithfully */
    uint16_t w, h;
    for (h = 0; h < c->height; ++h)
    {
        for (w = 0; w < c->width; ++w)
        {
            char chr = c->data[h * c->width + w];
            putc(chr, stdout);
        }
        printf("\n");
    }
    printf("\n");
}

void create()
{
    printf("Width?> ");
    int w = readint();
    printf("Height?> ");
    int h = readint();

    canvas_t *c = canvas_new(w, h);

    if (!c)
    {
        printf("[!] Failed to create canvas!\n");
        return;
    }

    printf("Title?> ");
    gets(c->title);

    printf("[+] Canvas created with id %d\n", c->id);

    canvas_append(c);
}

void del(int id)
{
    canvas_t *p;
    canvas_t *c = canvas_find(id, &p);

    if (!c)
        return;

    if (c->private)
    {
        printf("[!] Private canvas deletion is strictly forbidden.\n");
        return;
    }

    if (!p)
    {
        /* This is the first canvas in the gallery. */
        gallery = c->next;
    }
    else
    {
        /* This canvas is somewhere within the rest of the list. */
        p->next = c->next;
    }

    canvas_del(c);
}

void edit(int id)
{
    canvas_t *c = canvas_find(id, NULL);
    if (!c)
        return;

    if (c->private)
    {
        printf("[!] Private canvas alteration is strictly forbidden.\n");
        return;
    }

    printf("[*] Editing Canvas %d. Dimensions are: %dx%d\nNew Data: ", id, c->width, c->height);

    size_t len = c->width * c->height;
    fgets(c->data, len + 2, stdin); /* \n and \0 from fgets */
    c->data[len - 1] = '\0';        /* Strip new line */

    printf("[+] Changes saved\n");
}

/* GALLERY LOOP */
void main()
{
    setvbuf(stdout, NULL, _IONBF, -1);
    setvbuf(stdin, NULL, _IONBF, -1);
    g_heap = HeapCreate();
    canvas_load("./art.txt");

    printf("       ___    ___               ____\n"
           "      / _ |  / _ | ___ _ ___ _ / __/\n"
           "     / __ | / __ |/ _ `// _ `/_\\ \\\n"
           "    /_/ |_|/_/ |_|\\_,_/ \\_,_//___/\n"
           " A S C I I A R T a s a S E R V I C E\n"
           "-------------------------------------\n"
           "                    segv @ Montréhack\n\n");

    int done = 0;
    char cmd[100];

    printf("Welcome to the ASCII gallery!\nType 'help' for a list of commands. Type 'exit' to disconnect.\n");

    do
    {
        printf("\n> ");
        fgets(cmd, sizeof(cmd), stdin);
        int len = strlen(cmd);
        if (cmd[len - 1] == '\n')
            cmd[len - 1] = 0; /* trim newlines */

        /* Command dispatch */
        if (len < 2 || strcmp("exit", cmd) == 0)
            break;

        char *c = strtok(cmd, " ");
        if (CMD("help"))
        {
            help();
        }
        else if (CMD("list"))
        {
            list();
        }
        else if (CMD("show"))
        {
            char *i = strtok(NULL, " ");
            if (!i)
            {
                printf("You need to provide a canvas number!\n");
            }
            else
            {
                int id = atoi(i);
                show(id);
            }
        }
        else if (CMD("new"))
        {
            create();
        }
        else if (CMD("del"))
        {
            char *i = strtok(NULL, " ");
            if (!i)
            {
                printf("You need to provide a canvas number!\n");
            }
            else
            {
                int id = atoi(i);
                del(id);
            }
        }
        else if (CMD("edit"))
        {
            char *i = strtok(NULL, " ");
            if (!i)
            {
                printf("You need to provide a canvas number!\n");
            }
            else
            {
                int id = atoi(i);
                edit(id);
            }
        }
        else
        {
            printf("[!] Unknown command. Try 'help'.\n");
        }
    } while (!done);
    printf("\nGoodbye!\n");
}

/* Utility function to load canvas from disk. */
void canvas_load(char *file)
{
    FILE *fd = fopen(file, "rb");
    char *line, *l;
    size_t len;

    char *t = NULL;
    char buf[0x2000];
    while (!feof(fd))
    {
        line = NULL;
        len = 0;

        char title[16];

        /* Read canvas metadata */
        getline(&line, &len, fd);

        if (!strlen(line))
            break; /* EOF */

        l = line;
        /* Title */
        char *tok = strtok_r(l, "|", &t);
        strncpy(title, tok, sizeof(title));

        /* Width */
        tok = strtok_r(NULL, "|", &t);
        uint16_t w = atoi(tok);

        /* Height */
        tok = strtok_r(NULL, "|", &t);
        uint16_t h = atoi(tok);

        /* Private */
        tok = strtok_r(NULL, "|", &t);
        uint8_t private = atoi(tok);

        free(line);

        /* Read canvas data */
        fgets(buf, sizeof(buf), fd);

        canvas_t *canvas = canvas_new(w, h);
        memcpy(canvas->data, buf, w * h);
        strncpy(canvas->title, title, sizeof(title));

        canvas->private = private;
        canvas_append(canvas);
    }
}