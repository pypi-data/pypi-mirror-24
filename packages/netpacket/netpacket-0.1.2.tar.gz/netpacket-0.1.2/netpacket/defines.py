
'''
    All the constants packet uses are defined here.
    This is because there is allot of constants that
    some protocols make use of heavily, and its easier
    to open this file and read them over than to pad
    them within the implementation files.
'''

# ARP header constants.
ARP_HW_ETH     = 0x0001
ARP_OPCODE_REQ = 0x0001
ARP_OPCODE_REP = 0x0002

# ICMP types supported by packet.
ICMP_DST_UNREACH = 3
ICMP_TIME_EXC    = 11
ICMP_PARAM_PROB  = 12
ICMP_REDIRECT    = 5
ICMP_ECHO_REQ    = 8
ICMP_ECHO_REPLY  = 0
ICMP_TS          = 13
ICMP_TS_REPLY    = 14


# ICMP Destination Unreachable codes.
ICMP_DST_UNREACH_NET_UNR  = 0
ICMP_DST_UNREACH_HOST     = 1
ICMP_DST_UNREACH_PROTO    = 2
ICMP_DST_UNREACH_PORT     = 3
ICMP_DST_UNREACH_FRAG     = 4
ICMP_DST_UNREACH_SOURCE   = 5
ICMP_DST_UNREACH_HOST_ADM = 10
ICMP_DST_UNREACH_COMMUNIC = 13


# ICMP Time Exceeded codes.
ICMP_TIME_EXC_TTL      = 0
ICMP_TIME_EXC_FRAGMENT = 1


# ICMP Parameter Problem codes.
ICMP_PARAM_PROB_PTR     = 0
ICMP_PARAM_PROB_MISSING = 1
ICMP_PARAM_PROB_BADLEN  = 2

# ICMP Redirect Message codes.
ICMP_REDIRECT_NET      = 0
ICMP_REDIRECT_HOST     = 1
ICMP_REDIRECT_TOS_NET  = 2
ICMP_REDIRECT_TOS_HOST = 3

# DHCP header constants.
DHCP_MSG_REQUEST = 1 
DHCP_MSG_REPLY   = 2
DHCP_ETHERNET    = 1
DHCP_BROADCAST   = 1
DHCP_UNICAST     = 0

# DHCP Message Type constants.
DHCP_DISCOVER = 1
DHCP_OFFER    = 2
DHCP_REQUEST  = 3
DHCP_DECLINE  = 4
DHCP_ACK      = 5
DHCP_NACK     = 6
DHCP_RELEASE  = 7
DHCP_INFORM   = 8

'''
    List of RFC 2132 DHCP extension options. These
    are mostly the options you will use with addition
    to some from the Vendor extensions.
'''
DHCP_OPT_REQADDR        = 50
DHCP_OPT_LEASE_TIME     = 51
DHCP_OPT_OVERLOAD       = 52
DHCP_OPT_TFTP_SNAME     = 66
DHCP_OPT_BOOTF_NAME     = 67
DHCP_OPT_MSG_TYPE       = 53
DHCP_OPT_SRV_IDENT      = 54
DHCP_OPT_PARAM_REQLIST  = 55
DHCP_OPT_MSG            = 56
DHCP_OPT_MAX_MSG_SIZE   = 57
DHCP_OPT_RENEWAL_TIME   = 58
DHCP_OPT_REBINDING_TIME = 59
DHCP_OPT_VENDOR_CLASS   = 60

'''
    List of RFC 1497 Vendor extension options. A few
    are missing, but the most important are added.
'''
DHCP_OPT_PAD            = 0
DHCP_OPT_END            = 255
DHCP_OPT_SUBNET_MASK    = 1
DHCP_OPT_TIME_OFFSET    = 2
DHCP_OPT_ROUTER         = 3
DHCP_OPT_TIME_SRV       = 4
DHCP_OPT_NAME_SRV       = 5
DHCP_OPT_DNS            = 6
DHCP_OPT_LOG_SRV        = 7
DHCP_OPT_COOKIE_SRV     = 8
DHCP_OPT_LPR_SRV        = 9
DHCP_OPT_IMPRESS_SRV    = 10
DHCP_OPT_RES_LOC_SRV    = 11
DHCP_OPT_HOST_NAME      = 12
DHCP_OPT_BOOT_FILE_SIZ  = 13
DHCP_OPT_MERIT_DUMP     = 14
DHCP_OPT_DOMAIN_NAME    = 15
DHCP_OPT_SWAP_SRV       = 16
DHCP_OPT_ROOT_PATH      = 17
DHCP_OPT_EXTS_PATH      = 18
DHCP_OPT_IP_FORWARDING  = 19
DHCP_OPT_NLSR           = 20
DHCP_OPT_MAX_DGRAM_SIZ  = 22
DHCP_OPT_DEFAULT_IP_TTL = 23
DHCP_OPT_PATH_MTU       = 24
DHCP_OPT_PATH_MTU_TBL   = 25
DHCP_OPT_INTERFACE_MTU  = 26
DHCP_OPT_ALL_SUBNETS    = 27
DHCP_OPT_BRD_ADDR       = 28
DHCP_OPT_PERF_MASK_DISC = 29
DHCP_OPT_MASK_SUPPLIER  = 30
DHCP_OPT_ROUTER_DISC    = 31
DHCP_OPT_ROUTER_SOLIC   = 32
DHCP_OPT_STATIC_ROUTE   = 33
DHCP_OPT_TRAILER_ENCAP  = 34
DHCP_OPT_ARP_CACHE_TOUT = 35
DHCP_OPT_ETHERNET_ENCAP = 36