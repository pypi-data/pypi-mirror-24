
from _netpacket import ethernet, arp, ip, icmp, tcp, \
    udp, dhcpv4
from netpacket.defines import *
from netpacket import utils
from random import randint

PROTO_ARP  = 0x0806
PROTO_IPV4 = 0x0800
PROTO_IPV6 = 0x86dd
PROTO_TCP  = 0x0006
PROTO_UDP  = 0x0011
PROTO_ICMP = 0x0001

class ARP(arp, utils.DatagramUtilities):
    def __init__(self, opcode):
        utils.DatagramUtilities.__init__(self)
        utils.init_ethernet(self, PROTO_ARP)
        utils.init_arp(self, opcode)

class TCP(tcp, utils.DatagramUtilities):
    def __init__(self, ip_type=PROTO_IPV4):
        tcp.__init__(self, ip_type)
        utils.DatagramUtilities.__init__(self)
        if ip_type == PROTO_IPV4:
            utils.init_ethernet(self, PROTO_IPV4)
            utils.init_ip(self, PROTO_TCP)
        elif ip_type == PROTO_IPV6:
            utils.init_ethernet(self, PROTO_IPV6)
            utils.init_ipv6(self, PROTO_TCP)
        utils.init_tcp(self)

class UDP(udp, utils.DatagramUtilities):
    def __init__(self, ip_type=PROTO_IPV4):
        udp.__init__(self, ip_type)
        utils.DatagramUtilities.__init__(self)
        if ip_type == PROTO_IPV4:
            utils.init_ethernet(self, PROTO_IPV4)
            utils.init_ip(self, PROTO_UDP)
        elif ip_type == PROTO_IPV6:
            utils.init_ethernet(self, PROTO_IPV6)
            utils.init_ipv6(self, PROTO_UDP)

class ICMP(icmp, utils.DatagramUtilities):
    def __init__(self):
        icmp.__init__(self)
        utils.DatagramUtilities.__init__(self)
        utils.init_ethernet(self, PROTO_IPV4)
        utils.init_ip(self, PROTO_ICMP)

class ICMPDstUnreachable(ICMP):
    def __init__(self, code, datagram=None):
        ICMP.__init__(self)
        self.icmp_type = ICMP_DST_UNREACH
        self.icmp_code = code
        if datagram:
            self.icmp_dst_unreach_dgram = datagram

class ICMPTimeExceeded(ICMP):
    def __init__(self, code, datagram=None):
        ICMP.__init__(self)
        self.icmp_type = ICMP_TIME_EXC
        self.icmp_code = code
        if datagram:
            self.icmp_time_exc_dgram = datagram

class ICMPParamProblem(ICMP):
    def __init__(self, code, ptr=0, datagram=None):
        ICMP.__init__(self)
        self.icmp_type = ICMP_PARAM_PROB
        self.icmp_code = code
        self.icmp_param_prob_ptr = ptr
        if datagram:
            self.icmp_param_prob_dgram = datagram

class ICMPRedirect(ICMP):
    def __init__(self, code, gwaddr, datagram=None):
        ICMP.__init__(self)
        self.icmp_type = ICMP_REDIRECT
        self.icmp_code = code
        self.icmp_redirect_gwaddr = gwaddr
        if datagram:
            self.icmp_redirect_dgram = datagram

class ICMPEcho(ICMP):
    def __init__(self, icmp_type=ICMP_ECHO_REQ, ts=0,
                 payload=None):
        ICMP.__init__(self)
        self.icmp_type = icmp_type
        self.icmp_echo_id = randint(1, 65535)
        self.icmp_echo_seq = 1
        self.icmp_echo_ts = ts
        if payload:
            self.icmp_echo_payload = payload

class ICMPTimestampRequest(ICMP):
    def __init__(self, orig):
        ICMP.__init__(self)
        self.icmp_type = ICMP_TS
        self.icmp_ts_id = random.randint(1, 65535)
        self.icmp_ts_seq = 1
        self.icmp_ts_orig = orig

class ICMPTimestampReply(ICMP):
    def __init__(self, orig, recv, transmit):
        ICMP.__init__(self)
        self.icmp_type = ICMP_TS_REPLY
        self.icmp_ts_id = random.randint(1, 65535)
        self.icmp_ts_seq = 1
        self.icmp_ts_orig = orig
        self.icmp_ts_recv = recv
        self.icmp_ts_trans = transmit

class DHCPv4(dhcpv4):
    def __init__(self, dhcp_dgram=None, op=DHCP_MSG_REQUEST,
                 flags=DHCP_BROADCAST):
        if dhcp_dgram:
            return dhcpv4.__init__(self, dhcp_dgram)
        self.op = op
        self.htype = DHCP_ETHERNET
        self.hlen = 6
        self.hops = 0
        self.xid = randint(1, 0xffffffff)
        self.secs = 0
        self.flags = DHCP_BROADCAST
        self.cookie = 0x63825363

    def set_opt(self, code, data=0):
        dhcpv4.set_opt(self, code, data)
