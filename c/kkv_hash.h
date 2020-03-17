#include <stddef.h>
#include <stdint.h>

#ifndef KKV_HASH_H_
#define KKV_HASH_H_

#define ROTLEFT(i,bits) (((i) << (bits)) | ((i) >> (32-(bits))))
#define ROTRIGHT(i,bits) (((i) >> (bits)) | ((i) << (32-(bits))))

// Byte operations

// Two Extreme Bits
#define TEB(i) ((((i) & 0x80) >> 6) | ((i) & 1))
// Two Extreme Bits Reversed
#define TEBR(i) ((((i) & 0x80) >> 7) | (((i) & 1) << 1))

// Four Extreme Bits
// #define FEB(i) ((((i) & 0xF0) >> 4) | ((i) & 3))
// Four Extreme Bits Reversed Once
// #define FEBRO(i) ((((i) & 0xF0) >> 6) | (((i) & 3) << 2))

// Middles Extreme Bits
#define MEB(i) ((TEB((i) >> 24) << 6) | (TEB((i) >> 16) << 4) | (TEB((i) >> 8) << 2) | TEB(i))

typedef unsigned char byte;

uint32_t kkv_hash(byte *data, size_t len);

#endif  // KKV_HASH_H_
