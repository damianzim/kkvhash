#include "kkv_hash.h"

#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    const char *data[] = {
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "some text",
        "some textt",
        "foo",
        "bar",
        "baz",
    };

    size_t len = sizeof(data) / sizeof(data[0]);

    uint32_t temp_hash = 0;
    for (size_t i = 0; i < len; ++i) {
        temp_hash = kkv_hash((byte*)data[i], strlen(data[i]));
        printf("%10d - %08X -", temp_hash, temp_hash);
        for (size_t j = 0; j < strlen(data[i]); ++j)
            printf(" %02X", (uint8_t)data[i][j]);
        printf("\n");
    }

    return 0;
}
