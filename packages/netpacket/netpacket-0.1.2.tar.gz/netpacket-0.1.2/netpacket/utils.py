
'''
    File contains utilities that may help with
    datagram construction and devices.
'''
from socket import socket, AF_INET, AF_PACKET, SOCK_DGRAM, \
    SOCK_RAW, IPPROTO_RAW, inet_ntop
from netpacket import protocols
from netpacket import defines
import fcntl
import struct
import random

SIOCGIFHWADDR = 0x8927
SIOCGIFADDR   = 0x8915

class DatagramUtilities:
    def __init__(self):
        self.sock = socket(AF_PACKET, SOCK_RAW, IPPROTO_RAW)

    def sendto(self, packet, dest):
        self.sock.sendto(packet, dest)

    def set_local_mac(self, iface):
        if hasattr(self, "ether_src"):
            self.ether_src = get_ethernet_addr(iface)
        if hasattr(self, "arp_src_mac"):
            self.arp_src_mac = get_ethernet_addr(iface)

    def finish(self):
        if hasattr(self, "calc_len"):
            self.calc_len()
        if hasattr(self, "calc_csum"):
            self.calc_csum()

'''
    These helper routines initializes a protocol
    object to default values which makes sending
    raw packets way more trivial for the programmer.
'''
def init_ethernet(packet, proto):
    packet.ether_type = proto

def init_arp(packet, opcode):
    packet.arp_hw_type = defines.ARP_HW_ETH
    packet.arp_proto_type = protocols.PROTO_IPV4
    packet.arp_hw_size = 6
    packet.arp_proto_size = 4
    packet.arp_opcode = opcode

def init_ip(packet, proto):
    packet.ip_version = 4
    packet.ip_hlen = 20
    packet.ip_ds = 0
    packet.ip_ecn = 0
    packet.ip_len = 0
    packet.ip_identifier = random.randint(1, 65535)
    packet.ip_flags = 2
    packet.ip_frag_off = 0
    packet.ip_ttl = 255
    packet.ip_proto = proto
    packet.ip_csum = 0

def init_ipv6(packet, proto):
    packet.ip_version = 6
    packet.ip_ds = 0
    packet.ip_ecn = 0
    packet.ip_flow_label = 0
    packet.ip_len = 0
    packet.ip_proto = proto
    packet.ip_ttl = 255

def init_tcp(packet):
    packet.tcp_seq = 0
    packet.tcp_seq_ack = 0
    packet.tcp_hlen = 20
    packet.tcp_win = 1444
    packet.tcp_csum = 0
    packet.tcp_urg_ptr = 0

'''
    Get the ethernet address of an interface.
'''
def get_ethernet_addr(iface):
    iface = iface.encode("utf-8")
    ret = fcntl.ioctl(socket(AF_INET, SOCK_DGRAM, 0),
                      SIOCGIFHWADDR, struct.pack("40s", iface[0:15]))
    return bytes(":".join(["%02x" % byte for byte in ret[18:24]]),
                 "utf-8")

'''
    Get the IPv4 address of an interface.
'''
def get_ipv4_addr(iface):
    iface = iface.encode("utf-8")
    ret = fcntl.ioctl(socket(AF_INET, SOCK_DGRAM, 0),
                      SIOCGIFADDR, struct.pack("40s", iface[0:15]))
    return bytes(inet_ntop(AF_INET, ret[20:24]), "utf-8")

'''
    For use when attaching a IP datagram to a ICMP
    packet. It strips the ethernet header which is 14
    bytes in size.
'''
def strip_ethernet(dgram):
    if type(dgram) != bytes:
        raise TypeError("Expected bytes. Found " + 
                         str(type(dgram)))
    return dgram[14:]

