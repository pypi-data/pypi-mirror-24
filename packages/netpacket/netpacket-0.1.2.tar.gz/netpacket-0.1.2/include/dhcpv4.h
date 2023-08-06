
/*
 * Dynamic host configuration protocol (DHCP)
 * implementation.

 * The DHCP implementation is made up of getters
 * and setters, to manipulate the fields of the
 * BOOTP protocol. The implementation doesnt provide
 * you with any means of doing the DORA handshake, but
 * provides you with filling out the header and transmitting
 * it on top of a TCP/UDP header. The implementation doesnt
 * provide getters and setters for options. Instead it
 * defines a buffer of 312 octets and a offset pointer
 * into the buffer. The buffer is explicitly controlled by
 * calling the method set_opt from Python. If the option
 * buffer overflows, the SNAME/SFILE fields may be used to
 * define more options.
 */
#ifndef INCLUDE_DHCP_H
#define INCLUDE_DHCP_H

#include "udp.h"

#define DHCP_STATIC_LEN     240
#define DHCP_MAGIC_COOKIE   0x63825363
#define MAX_OPTLEN          312

#define DHCP_SEG_OPTS   0
#define DHCP_SEG_SNAME  1
#define DHCP_SEG_SFILE  2

typedef u8 DHCP_OPTBUF;

struct dhcp {
    u8 op;
    u8 htype;
    u8 hlen;
    u8 hops;
    u32 xid;
    u16 secs;
    u16 flags;
    u32 ciaddr;
    u32 yiaddr;
    u32 siaddr;
    u32 giaddr;
    char chaddr[16];
    u8 sname[64];
    u8 file[128];
    u32 cookie;
    u8 opts[MAX_OPTLEN];
};

typedef struct {
    packet base_obj;
    struct dhcp __dhcp;
    u32 opt_offset;
    u32 sname_offset;
    u32 sfile_offset;
    u32 segment;
} dhcp;

#define DHCP_OP     (void *)0
#define DHCP_HTYPE  (void *)1
#define DHCP_HLEN   (void *)2
#define DHCP_HOPS   (void *)3
#define DHCP_XID    (void *)4
#define DHCP_SECS   (void *)5
#define DHCP_FLAGS  (void *)6
#define DHCP_CIADDR (void *)7
#define DHCP_YIADDR (void *)8
#define DHCP_SIADDR (void *)9
#define DHCP_GIADDR (void *)10
#define DHCP_CHADDR (void *)11
#define DHCP_SNAME  (void *)12
#define DHCP_FILE   (void *)13
#define DHCP_COOKIE (void *)14

// RFC 2132 DHCP extension options.
#define DHCP_OPT_REQADDR        50
#define DHCP_OPT_LEASE_TIME     51
#define DHCP_OPT_OVERLOAD       52
#define DHCP_OPT_TFTP_SNAME     66
#define DHCP_OPT_BOOTF_NAME     67
#define DHCP_OPT_MSG_TYPE       53
#define DHCP_OPT_SRV_IDENT      54
#define DHCP_OPT_PARAM_REQLIST  55
#define DHCP_OPT_MSG            56
#define DHCP_OPT_MAX_MSG_SIZE   57
#define DHCP_OPT_RENEWAL_TIME   58
#define DHCP_OPT_REBINDING_TIME 59
#define DHCP_OPT_VENDOR_CLASS   60

// RFC 1497 Vendor extensions.
#define DHCP_OPT_PAD            0
#define DHCP_OPT_END            255
#define DHCP_OPT_SUBNET_MASK    1
#define DHCP_OPT_TIME_OFFSET    2
#define DHCP_OPT_ROUTER         3
#define DHCP_OPT_TIME_SRV       4
#define DHCP_OPT_NAME_SRV       5
#define DHCP_OPT_DNS            6
#define DHCP_OPT_LOG_SRV        7
#define DHCP_OPT_COOKIE_SRV     8
#define DHCP_OPT_LPR_SRV        9
#define DHCP_OPT_IMPRESS_SRV    10
#define DHCP_OPT_RES_LOC_SRV    11
#define DHCP_OPT_HOST_NAME      12
#define DHCP_OPT_BOOT_FILE_SIZ  13
#define DHCP_OPT_MERIT_DUMP     14
#define DHCP_OPT_DOMAIN_NAME    15
#define DHCP_OPT_SWAP_SRV       16
#define DHCP_OPT_ROOT_PATH      17
#define DHCP_OPT_EXTS_PATH      18
#define DHCP_OPT_IP_FORWARDING  19
// Non-Local Source Routing.
#define DHCP_OPT_NLSR           20
//#define DHCP_OPT_POLICY_FILTER  21
#define DHCP_OPT_MAX_DGRAM_SIZ  22
#define DHCP_OPT_DEFAULT_IP_TTL 23
#define DHCP_OPT_PATH_MTU       24
#define DHCP_OPT_PATH_MTU_TBL   25
#define DHCP_OPT_INTERFACE_MTU  26
#define DHCP_OPT_ALL_SUBNETS    27
#define DHCP_OPT_BRD_ADDR       28
#define DHCP_OPT_PERF_MASK_DISC 29
#define DHCP_OPT_MASK_SUPPLIER  30
#define DHCP_OPT_ROUTER_DISC    31
#define DHCP_OPT_ROUTER_SOLIC   32
#define DHCP_OPT_STATIC_ROUTE   33
#define DHCP_OPT_TRAILER_ENCAP  34
#define DHCP_OPT_ARP_CACHE_TOUT 35
#define DHCP_OPT_ETHERNET_ENCAP 36

/*
 * Singular in the sense of the option not having
 * anything else than a code.
 */
#define is_singular_opt(code) (code == DHCP_OPT_PAD || \
                               code == DHCP_OPT_END)
char *dhcp_attr_string(void *closure);

#endif /* INCLUDE_DHCP_H */