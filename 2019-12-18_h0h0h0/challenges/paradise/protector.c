#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>

#define LEN 12

char sbox[] = {0x32, 0x44, 0x16, 0x37, 0x76, 0xf1, 0xba, 0xbb, 0x45, 0xa0, 0xf7, 0x12, 0x1a, 0x77};

void GeneratePassword(char* out_pass, char* hostname, int64_t time) {
  int i = 0;
  int l = strlen(hostname);
  char *p = hostname; for (; *p; ++p) *p = tolower(*p);

  struct tm* t = gmtime(&time);

  for (;i<LEN;++i) {
    char c = hostname[i%l];
    c *= t->tm_year;
    c += t->tm_mday;
    c *= t->tm_min;
    c ^= t->tm_wday;
    c = (c >> 4 & 0xf) | (c & 0xf) << 4;

    c ^= sbox[i];

    while (!isalnum(c)) c = c * (c & 0xf) + ((0xf0 & c) >> 4) + 1;
    out_pass[i] = c;
  }
}
