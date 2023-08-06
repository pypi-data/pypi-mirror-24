
#ifndef INCLUDE_UDP_H
#define INCLUDE_UDP_H

#include "ip.h"

struct udp {
    u16 src;
    u16 dst;
    u16 len;
    u16 csum;
};

typedef struct {
    ip base_obj;
    struct udp __udp;
    PyObject *payload;
} udp;

struct udp_v4_pseudo {
    u32 source;
    u32 dest;
    u8 zero;
    u8 proto;
    u16 len;
    struct udp udp_hdr;
};
struct udp_v6_pseudo {
    ip_v6_addr source;
    ip_v6_addr dest;
    u32 len;
    u32 zero:24;
    u32 next_hdr:8;
    struct udp udp_hdr;
};

#define UDP_SRC         (void *)0
#define UDP_DST         (void *)1
#define UDP_LEN         (void *)2
#define UDP_CSUM        (void *)3
#define UDP_PAYLOAD     (void *)4

#define udp_offset(x) (offsetof(udp, __udp) + \
                       offsetof(struct udp, x))
int udp_add_type(PyObject *module);
PyObject *create_udp_instance(int caplen,
                              const unsigned char *pkt,
                              u16 _ip_type);
char *udp_attr_string(void *closure);

#endif