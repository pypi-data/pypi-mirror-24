
/*
 * The Internet Control Message Protocol datatype
 * implemented here also defines deprecated types.
 * This means that deprecated types may be created
 * from Python, and parsed into memory on input
 * with ppcap (If such a datagram were to arrive).
 * Note that the deprecated types sent will most likely
 * be dropped at the destination host node. Every ICMP
 * type is identified by its own structure, if it is
 * deprecated, the structure is prefixed with a deprecated
 * comment.
 */
#ifndef INCLUDE_ICMP_H
#define INCLUDE_ICMP_H

#include "ip.h"

struct icmp_hdr {
    u8 type;
    u8 code;
    u16 csum;
};

struct icmp_dst_unreach {
    u32 unused;
    PyObject *datagram;
} __attribute__ ((packed));

struct icmp_time_exc {
    u32 unused;
    PyObject *datagram;
} __attribute__ ((packed));

struct icmp_param_prob {
    u8 ptr;
    u8 unused[3];
    PyObject *datagram;
} __attribute__ ((packed));

struct icmp_redirect {
    u32 gw_addr;
    PyObject *datagram;
} __attribute__ ((packed));

struct icmp_echo {
    u16 id;
    u16 seq;
    u64 ts;
    PyObject *payload;
} __attribute__ ((packed));

struct icmp_ts {
    u16 id;
    u16 seq;
    u32 orig;
    u32 recv;
    u32 trans;
};

struct icmp {
    struct icmp_hdr hdr;
    struct icmp_dst_unreach dst_unreach;
    struct icmp_time_exc time_exc;
    struct icmp_param_prob param_prob;
    struct icmp_redirect redirect;
    struct icmp_echo echo;
    struct icmp_ts ts;
};
typedef struct {
    ip base_obj;
    struct icmp __icmp;
    Py_ssize_t (*calc_len)(struct icmp *__icmp);
    u16 (*calc_csum)(struct icmp *__icmp, char *buf);
    char *(*to_bytes)(struct icmp *__icmp, char *buf,
                      Py_ssize_t *size);
} icmp;

#define ICMP_TYPE               (void *)0
#define ICMP_CODE               (void *)1
#define ICMP_CSUM               (void *)2
#define ICMP_PARAM_PROB_PTR     (void *)3
#define ICMP_PARAM_PROB_DGRAM   (void *)4
#define ICMP_REDIRECT_GW_ADDR   (void *)5
#define ICMP_REDIRECT_DGRAM     (void *)6
#define ICMP_ECHO_ID            (void *)7
#define ICMP_ECHO_SEQ           (void *)8
#define ICMP_ECHO_TS            (void *)9
#define ICMP_ECHO_PAYLOAD       (void *)10
#define ICMP_TS_ID              (void *)11
#define ICMP_TS_SEQ             (void *)12
#define ICMP_TS_ORIG            (void *)13
#define ICMP_TS_RECV            (void *)14
#define ICMP_TS_TRANS           (void *)15

#define ICMP_DST_UNREACH    3
#define ICMP_TIME_EXC       11
#define ICMP_PARAM_PROB     12
#define ICMP_REDIRECT       5
#define ICMP_ECHO_REQ       8
#define ICMP_ECHO_REPLY     0
#define ICMP_TS             13
#define ICMP_TS_REPLY       14

PyObject *create_icmp_instance(int caplen,
                               const unsigned char *pkt);
char *icmp_attr_string(void *closure);

Py_ssize_t calc_len_ts(struct icmp *__icmp);
Py_ssize_t calc_len_echo(struct icmp *__icmp);
Py_ssize_t calc_len_redirect(struct icmp *__icmp);
Py_ssize_t calc_len_param_prob(struct icmp *__icmp);
Py_ssize_t calc_len_time_exc(struct icmp *__icmp);
Py_ssize_t calc_len_dst_unreach(struct icmp *__icmp);

u16 calc_csum_ts(struct icmp *__icmp, char *buf);
u16 calc_csum_echo(struct icmp *__icmp, char *buf);
u16 calc_csum_redirect(struct icmp *__icmp, char *buf);
u16 calc_csum_param_prob(struct icmp *__icmp, char *buf);
u16 calc_csum_time_exc(struct icmp *__icmp, char *buf);
u16 calc_csum_dst_unreach(struct icmp *__icmp, char *buf);

char *to_bytes_ts(struct icmp *__icmp, char *buf,
                  Py_ssize_t *size);
char *to_bytes_echo(struct icmp *__icmp, char *buf,
                    Py_ssize_t *size);
char *to_bytes_redirect(struct icmp *__icmp, char *buf,
                        Py_ssize_t *size);
char *to_bytes_param_prob(struct icmp *__icmp, char *buf,
                          Py_ssize_t *size);
char *to_bytes_time_exc(struct icmp *__icmp, char *buf,
                        Py_ssize_t *size);
char *to_bytes_dst_unreach(struct icmp *__icmp, char *buf,
                           Py_ssize_t *size);
#endif