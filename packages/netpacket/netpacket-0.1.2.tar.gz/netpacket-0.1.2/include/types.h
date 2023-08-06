
#ifndef INCLUDE_TYPES_H
#define INCLUDE_TYPES_H
/*
 * File declares several integer datatypes.
 * These are used to declare the proper fields
 * in the protocol datatypes.
 */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
#ifdef __LP64__
 typedef unsigned long u64;
#else
 typedef unsigned long long u64;
#endif

typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#ifdef __LP64__
 typedef signed long s64;
#else
 typedef signed long long s64;
#endif

/*
 * Datatype below is used to reference
 * IPv6 addresses which is of size 120 bits.
 */
typedef u8 ip_v6_addr[16];

#endif /* INCLUDE_TYPES_H */