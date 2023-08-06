
#ifndef INCLUDE_IP_H
#define INCLUDE_IP_H

#include "ethernet.h"

struct ipv4 {
#if __BYTE_ORDER == __LITTLE_ENDIAN
    u32 hlen:4;
    u32 version:4;
#elif __BYTE_ORDER == __BIG_ENDIAN
    u32 version:4;
    u32 hlen:4;
#else
    #error "<bits/endian.h> broken"
#endif
#if __BYTE_ORDER == __LITTLE_ENDIAN
    u32 ecn:2;
    u32 ds:6;
#elif __BYTE_ORDER == __BIG_ENDIAN
    u32 ds:6;
    u32 ecn:2;
#endif
    u16 len;
    u16 identifier;
    u16 frag_flags_off;
    u8 ttl;
    u8 proto;
    u16 csum;
    u32 source;
    u32 dest;
};

struct ipv6 {
    u32 vtf;
    u16 len;
    u8 next_hdr;
    u8 hop_lmt;
    ip_v6_addr source;
    ip_v6_addr dest;
};

typedef struct {
    ethernet base_obj;
    union {
        struct ipv4 __ipv4;
        struct ipv6 __ipv6;
    };
    /*
     * This u16 type is used to distinguish between
     * ipv4 and ipv6. The macros pkt_is_ipv4
     * is used for a simple
     * conditional statement. Note that this
     * symbol is out of reach from the Python
     * language.
     */
     u16 ip_type;
     /*
      * I found it really frustrating to always
      * figure out the size in protocols above IP,
      * so the value will be saved here for use.
      */
     u8 ip_size;
} ip;
#ifdef IP_TTL
#undef IP_TTL
#endif
#define IP_VERSION              (void *)0
#define IP_LEN                  (void *)1
#define IP_PROTO                (void *)2
#define IP_TTL                  (void *)3
#define IP_DS                   (void *)4
#define IP_ECN                  (void *)5
#define IPV4_IDENTIFIER         (void *)6
#define IPV4_FLAGS              (void *)7
#define IPV4_FRAG_OFF           (void *)8
#define IPV4_CSUM               (void *)9
#define IPV4_HLEN               (void *)10
#define IPV6_FLOW_LABEL         (void *)11

#define IPV6_HDR_HBH            0x00000000

#define ipv4_offset(x)    (offsetof(ip, __ipv4) + \
                           offsetof(struct ipv4, x))
#define pkt_is_ipv4(x)    (x->ip_type == PROTO_IPV4)
#define skip_ipv4_opts(x) (x > 20 ? x - 20 : 0) 
int ip_add_type(PyObject *module);
PyObject *create_ip_instance(int caplen,
                             const unsigned char *pkt,
                             u16 _ip_type);
char *ip_attr_string(void *closure);
void __ip_calc_len(ip *self, Py_ssize_t len);
void __ipv4_calc_csum(struct ipv4 *ips);

#endif

