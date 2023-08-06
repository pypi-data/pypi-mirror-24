
/*
 * File is used to define docstrings to explain
 * the usage of the module, and every data contained
 * within the module. Every docstring is prefixed by
 * DOCSTR_
 */
#ifndef INCLUDE_DOCSTRINGS_H
#define INCLUDE_DOCSTRINGS_H

/*
 * ppcap docstrings.
 */
#define DOCSTR_PPCAP_CREATE         "create(device)\n\n" \
                                    "Creates a pcap handle that will use the passed 'device' string\n" \
                                    "for capturing packets. Raises a PpcapException on error."
#define DOCSTR_PPCAP_ACTIVATE       "activate()\n\n" \
                                    "Activates a pcap handle to look at packets on the network. Some Options\n" \
                                    "needs to be set before activating the handle for them to take effect,\n" \
                                    "like snaplen. The handle also needs to be created before calling this.\n" \
                                    "Raises PpcapException on error."
#define DOCSTR_PPCAP_OPEN_LIVE      "open_live(device, snaplen, promisc, ms)\n\n" \
                                    "Creates a pcap handle that will use the passed 'device' string\n" \
                                    "for capturing packets. a 'device' argument of 'any' or 'NULL' can be\n" \
                                    "used to capture packets from all interfaces. This routine works as a\n" \
                                    "shortcut for setting up a device with a few options and activating it.\n\n" \
                                    "'snaplen' specifies the maximum size of the packets to be buffered.\n\n" \
                                    "'promisc' specifies if the interface is to be put into promiscuous mode.\n" \
                                    "Refer to hubs for more information.\n\n" \
                                    "'ms' specifies the read timeout in milliseconds.\n\n" \
                                    "The minimum snaplen accepted is '100', since those bytes are required\n" \
                                    "for returning a Python protocol object. Raises PpcapException on error."
#define DOCSTR_PPCAP_FINDALLDEVS    "findalldevs()\n\n" \
                                    "Returns a list of devices that can be used for capturing. If no devices\n" \
                                    "were found, it returns an empty list. Raises PpcapException on error."
#define DOCSTR_PPCAP_LOOKUPDEV      "lookupdev()\n\n" \
                                    "Returns a string giving the name of a network device suitable for use\n" \
                                    "with the create() and activate() chain, or with open_live(), and with\n" \
                                    "lookupnet(). Raises PpcapException on error."
#define DOCSTR_PPCAP_SET_SNAPLEN    "set_snaplen(snaplen)\n\n" \
                                    "Sets the snaplen of a pcap handle that has been created prior to this call\n" \
                                    "with create(). The minimum snaplen accepted is '100'. Raises PpcapException\n" \
                                    "on error."
#define DOCSTR_PPCAP_SET_PROMISC    "set_promisc(promisc)\n\n" \
                                    "Sets promisc mode on a pcap handle that has been created prior to this call\n" \
                                    "with create(). The promisc argument should either be True or False. Raises\n" \
                                    "PpcapException on error."
#define DOCSTR_PPCAP_SET_TIMEOUT    "set_timeout(ms)\n\n" \
                                    "Sets a read timeout on the handle created prior to this call with create()\n" \
                                    "This is only being used by the next() routine, where the\n" \
                                    "loop() routine will ignore this value. Raises PpcapException on error."
#define DOCSTR_PPCAP_LOOKUPNET      "lookupnet(device)\n\n" \
                                    "Find the IPV4 network number and netmask for a device. This has to be called\n" \
                                    "before compiling a filter with compile(). Raises PpcapException on error."
#define DOCSTR_PPCAP_COMPILE        "compile(filter, [optimize])\n\n" \
                                    "Compiles a filter expression on a handle that has been created prior to this\n" \
                                    "call with create() or open_live. Use man 7 pcap-filter for the syntax of the\n" \
                                    "'filter' argument. Raises PpcapException on error."
#define DOCSTR_PPCAP_SETFILTER      "setfilter()\n\n" \
                                    "Activates a filter specified with compile() on a handle created prior to this\n" \
                                    "call with create() or open_live(). Raises PpcapException on error."
#define DOCSTR_PPCAP_LOOP           "loop(num_packets, callback)\n\n" \
                                    "Process packets from a live capture.\n\n" \
                                    "'num_packets' specifies how many packets to process. A value of -1 is specified\n" \
                                    "for an endless stream.\n\n" \
                                    "'callback' specifies a callback routine that should receive a protocol type.\n" \
                                    "The definition is as follows: def my_callback(packet, length). Raises\n" \
                                    "PpcapException on error."
#define DOCSTR_PPCAP_NEXT           "next()\n\n" \
                                    "Returns a protocol type and raises a PpcapException on error. The routine\n" \
                                    "blocks by default, but can be changed with setnonblock()."
#define DOCSTR_PPCAP_SETNONBLOCK    "setnonblock(value)\n\n" \
                                    "Sets nonblock on the pcap handle if 'value' is 1. This is only usefull with\n" \
                                    "the next() routine, it is ignored with loop(). Raises PpcapException on error."
#define DOCSTR_PPCAP_CLOSE          "close()\n\n" \
                                    "Close a pcap handle created prior with create() or open_live(), and free all\n" \
                                    "the resources."
/*
 * Datatype 'packet' docstrings.
 */
#define DOCSTR_PACKET_IS_ETH        "is_ethernet()\n\n" \
                                    "Returns True if object is of type ethernet. Otherwise False."
#define DOCSTR_PACKET_IS_ARP        "is_arp()\n\n" \
                                    "Returns True if object is of type arp. Otherwise False."
#define DOCSTR_PACKET_IS_IPV4       "is_ipv4()\n\n" \
                                    "Returns True if object is of type ipv4. Otherwise False."
#define DOCSTR_PACKET_IS_IPV6       "is_ipv6()\n\n" \
                                    "Returns True if object is of type ipv6. Otherwise False."
#define DOCSTR_PACKET_IS_ICMP       "is_icmp()\n\n" \
                                    "Returns True if object is of type icmp. Otherwise False."
#define DOCSTR_PACKET_IS_TCP        "is_tcp()\n\n" \
                                    "Returns True if object is of type tcp. Otherwise False."
#define DOCSTR_PACKET_IS_UDP        "is_udp()\n\n" \
                                    "Returns True if object is of type udp. Otherwise False."
#define DOCSTR_PACKET_IS_DHCP       "is_dhcp()\n\n" \
                                    "Returns True if object is of type dhcp. Otherwise False."
/*
 * Datatype 'ethernet' docstrings.
 */
#define DOCSTR_ETHERNET_SRC         "The source MAC address. It accepts a bytes object in the format\n" \
                                    "xx:xx:xx:xx:xx:xx, where 'xx' is of base '16'."
#define DOCSTR_ETHERNET_DST         "The destination MAC address. It accepts a bytes object in the format\n" \
                                    "xx:xx:xx:xx:xx:xx, where 'xx' is of base '16'."
#define DOCSTR_ETHERNET_TYPE        "Type for the upper-layer protocol. Valid values\n" \
                                    "are IPV4(0x0800) and IPV6(0x86dd)."
#define DOCSTR_ETHERNET_TO_BYTES    "to_bytes()\n\n" \
                                    "Allocates and returns a bytes object that consists of\n" \
                                    "the ethernet header."
/*
 * Datatype 'arp' docstrings.
 */
#define DOCSTR_ARP_HW_TYPE          "The format of the MAC addresses. Currently accepted values are\n" \
                                    "Ethernet(0x01)."
#define DOCSTR_ARP_PROTO_TYPE       "The format of the IP addresses. Currently accepted values are\n" \
                                    "IPV4(0x0800) and IPV6(0x86dd)."
#define DOCSTR_ARP_HW_SIZE          "The size of the MAC addresses. This should be set to '6'."
#define DOCSTR_ARP_PROTO_SIZE       "The size of the IP addresses. This should be set to '4' for IPV4."
#define DOCSTR_ARP_OPCODE           "The opcode field says whether the ARP packet is a request or a reply.\n" \
                                    "Accepted values are request(0x01) and reply(0x02)."
#define DOCSTR_ARP_SRC_MAC          "The source MAC address. It accepts a bytes object in the format\n" \
                                    "xx:xx:xx:xx:xx:xx, where 'xx' is of base '16'."
#define DOCSTR_ARP_DST_MAC          "The destination MAC address. It accepts a bytes object in the format\n" \
                                    "xx:xx:xx:xx:xx:xx, where 'xx' is of base '16'."
#define DOCSTR_ARP_SRC_IP           "The source IP address. It accepts a bytes object of a IPV4 address\n" \
                                    "notation."
#define DOCSTR_ARP_DST_IP           "The destination IP address. It accepts a bytes object of a IPV4 address\n" \
                                    "notation."
#define DOCSTR_ARP_TO_BYTES         "to_bytes()\n\n" \
                                    "Allocates and returns a bytes object that consists of\n" \
                                    "the ethernet header + ARP header."
/*
 * Datatype 'ipv4/ipv6' docstrings.
 */
#define DOCSTR_IP_CALC_LEN          "calc_len()\n\n" \
                                    "Calculates the length field of the IP header. The final\n" \
                                    "sum is the IPV4 header + upper-layer protocol length for IPV4.\n" \
                                    "For IPV6 the final sum is IPV6 header + extension headers\n+ upper-protocol " \
                                    "length."
#define DOCSTR_IPV4_CALC_CSUM       "calc_csum()\n\n" \
                                    "Calculates the checksum field of the IPV4 header. Note,\nthis is only for " \
                                    "IPV4, IPV6 does not contain a checksum field. Calling \nthis on a IPV6 packet " \
                                    "will raise an AttributeError."
#define DOCSTR_IP_TO_BYTES          "to_bytes()\n\n" \
                                    "Allocates and returns a bytes object that consists of\n" \
                                    "the ethernet header + IPV4/IPV6 header."
#define DOCSTR_IP_VERSION           "Version field of a IPV4/IPV6 header. For IPV4 it should be '4'.\n" \
                                    "For IPV6 it should be '6'."
#define DOCSTR_IP_LEN               "Length field of a IPV4/IPV6 header. Refer to the 'ip.calc_len' method\n" \
                                    "for auto-filling this field."
#define DOCSTR_IP_PROTO             "Protocol field of a IPV4/IPV6 header. For IPV4 this refers to the\n" \
                                    "upper-layer protocol. For IPV6 this refers to either an extension header\n" \
                                    "or the upper-layer protocol."
#define DOCSTR_IP_TTL               "Time to live field of a IPV4/IPV6 header. It specifies the lifetime\n" \
                                    "of a datagram."
#define DOCSTR_IPV4_IDENTIFIER      "Identification field of a IPV4 header. It is a value assigned by the\n" \
                                    "sender to aid in assembling the fragments of a datagram."
#define DOCSTR_IPV4_CSUM            "Checksum field of a IPV4 header. Refer to the 'ip.calc_csum' method\n" \
                                    "for auto-filling this field."
#define DOCSTR_IPV4_HLEN            "Header length field of a IPV4 header. The field is interpreted in 32 bit\n" \
                                    "units (4 bytes). A default value corresponds to '5' which is interpreted\n" \
                                    "as 20 bytes."
#define DOCSTR_IP_SOURCE            "Source IP address field of a IPV4/IPV6 header which expects a bytes\n" \
                                    "object of either a IPV4 address notation or a IPV6 address notation."
#define DOCSTR_IP_DEST              "Destination IP address field of a IPV4/IPV6 header which expects a bytes\n" \
                                    "object of either a IPV4 address notation or a IPV6 address notation."
#define DOCSTR_IPV4_FLAGS           "Various control flags used in conjunction with fragmentation.\n" \
                                    "Value 0x01: More fragments.\n" \
                                    "Value 0x02: Dont fragment.\n" \
                                    "Value 0x04: Reserved (packet will ignore this value)."
#define DOCSTR_IPV4_FRAGMENT_OFF    "The fragment offset indicates where in the datagram this fragment\n" \
                                    "belongs. The fragment offset is measured in units of 8 bytes (64 bits).\n" \
                                    "The first fragment should have offset zero."
/*
 * Datatype 'tcp' docstrings.
 */
#define DOCSTR_TCP_CALC_LEN         "calc_len()\n\n" \
                                    "TCP does not contain a length field, so this subroutine only passes\n" \
                                    "the TCP header length + payload size to IP's calc_len method."
#define DOCSTR_TCP_CALC_CSUM        "calc_csum()\n\n" \
                                    "Calculates the checksum field of the TCP header + (IPV4 header if the\n" \
                                    "underlying protocol is IPV4)."
#define DOCSTR_TCP_GET_FLAGS        "tcp_get_flags()\n\n" \
                                    "Returns a dictionary holding all the TCP flags. The flag identifiers are\n" \
                                    "listed below:\n\n" \
                                    "nonce, cwr, echo, urg, ack, push, rst, syn, fin."
#define DOCSTR_TCP_SET_FLAGS        "tcp_set_flags(keywords*)\n\n" \
                                    "Sets tcp flags. Accepted flag keywords are listed below:\n\n" \
                                    "nonce, cwr, echo, urg, ack, push, rst, syn, fin."
#define DOCSTR_TCP_TO_BYTES         "tcp_to_bytes()\n\n" \
                                    "Allocates and returns a bytes object that consists of the ethernet header +\n" \
                                    "IPV4/IPV6 header + TCP header + payload (if set)."
#define DOCSTR_TCP_CSUM             "Checksum field of the TCP header. Refer to the 'tcp.calc_csum' method\n" \
                                    "for auto-filling this field."
#define DOCSTR_TCP_DST              "Destination port field of the TCP header."
#define DOCSTR_TCP_HLEN             "The length of the TCP header. The field is interpreted in units of 4 bytes.\n" \
                                    "The only supported value to set right now is 0x05 (20 bytes), in other words\n" \
                                    "without options. Options will be added later. If using ppcap as a packet\n" \
                                    "capturer, the hlen field will be adjusted to 20 bytes."
#define DOCSTR_TCP_PAYLOAD          "Sets the payload of a TCP packet. It might be forgotten, so remember\n" \
                                    "to set this before calculating the length of the TCP packet with\n" \
                                    "'tcp.calc_len', not after."
#define DOCSTR_TCP_SEQ              "The sequence number of the TCP stream. This is used in conjunction with\n" \
                                    "the ACK number to repair a broken TCP stream. The value will be\n" \
                                    "ISN (Initial sequence number) + amount of data sent. The ISN is an arbitrary\n" \
                                    "number picked by the kernel. For more information about a 'broken TCP stream'\n" \
                                    "read https://tools.ietf.org/html/rfc793"
#define DOCSTR_TCP_SEQ_ACK          "The ACK number of the TCP stream. This should not be set unless the ACK bit in\n" \
                                    "the TCP flags is set. It represents the next sequence number the sender of the\n" \
                                    "segment is expecting to receive."
#define DOCSTR_TCP_SRC              "Source port field of the TCP header."
#define DOCSTR_TCP_URG_PTR          "The urgent pointer is used in conjunction with the URG flag bit. This field\n" \
                                    "should point to where in the payload the urgent data ends."
#define DOCSTR_TCP_WIN              "The window size indicates the size of the TCP receive buffer."
/*
 * Datatype 'udp' docstrings.
 */
#define DOCSTR_UDP_CALC_LEN         "calc_len()\n\n" \
                                    "Calculates the length field of the UDP header. The final sum is\n" \
                                    "the UDP header + payload size."
#define DOCSTR_UDP_CALC_CSUM        "calc_csum()\n\n" \
                                    "Calculates the checksum field of the UDP header + (IPV4 header if the underlying\n" \
                                    "protocol is IPV4.)"
#define DOCSTR_UDP_TO_BYTES         "to_bytes()\n\n" \
                                    "Allocates and returns a bytes object that consists of the ethernet header +\n" \
                                    "IPV4/IPV6 header + UDP header + payload (if set)."
#define DOCSTR_UDP_SRC              "Source port field of the UDP header."
#define DOCSTR_UDP_DST              "Destination port field of the UDP header."
#define DOCSTR_UDP_LEN              "Length field of a UDP header. Refer to the 'udp.calc_len' method\n" \
                                    "for auto-filling this field."
#define DOCSTR_UDP_CSUM             "Checksum field of the UDP header. Refer to the 'udp.calc_csum' method\n" \
                                    "for auto-filling this field."
#define DOCSTR_UDP_PAYLOAD          "Sets the payload of a UDP packet. It might be forgotten, so remember\n" \
                                    "to set this before calculating the length of the UDP packet with\n" \
                                    "'udp.calc_len', not after."
/*
 * Datatype 'dhcpv4' docstrings.
 */
#define DOCSTR_DHCP_GET_OPT         "get_opt(code, [segment])\n\n" \
                                    "Try to get an option out of a segment using 'code'.\n" \
                                    "Segments: 0(options), 1(sname), 2(file). The segment is cached\n" \
                                    "until get_opt() is called with a new one."
#define DOCSTR_DHCP_SET_OPT         "set_opt(code, data, [segment])\n\n" \
                                    "Set an option into a segment using 'code' and 'data'. The behaviour\n" \
                                    "of the segment is described above."
#define DOCSTR_DHCP_GET_OPTS        "get_opts([segment])\n\n" \
                                    "Get the entire option segment as a bytes object. The segment defaults\n" \
                                    "to options."
#define DOCSTR_DHCP_TO_BYTES        "to_bytes()\n\n" \
                                    "Allocates and returns a bytes object that consists of the DHCPv4 header\n" \
                                    "plus options if they are present."
#define DOCSTR_DHCP_OP              "The message type. Supported values are 1(BOOTREQUEST) and 2(BOOTREPLY)."
#define DOCSTR_DHCP_HTYPE           "Hardware address type. In the DHCP context, the value should\n" \
                                    "be 1(10mb ethernet)."
#define DOCSTR_DHCP_HLEN            "Hardware address length. In the DHCP context, the value should\n" \
                                    "be 6(10mb ethernet)."
#define DOCSTR_DHCP_HOPS            "Optionally used by relay agents when booting via a relay agent."
#define DOCSTR_DHCP_XID             "Random number chosen by the client. Used to distinguish a stream\n" \
                                    "of messages from one-another."
#define DOCSTR_DHCP_SECS            "Filled in by client, seconds elapsed since client began address\n" \
                                    "acquisition or renewal process."
#define DOCSTR_DHCP_FLAGS           "1(broadcast) or 0(unicast)."
#define DOCSTR_DHCP_CIADDR          "Client IP address. Only filled in if client is in BOUND, RENEW\n" \
                                    "or REBINDING state and can respond to ARP requests."
#define DOCSTR_DHCP_YIADDR          "The IP address the client is given. Filled in by the DHCP server on\n" \
                                    "DHCPOFFER and DHCPACK."
#define DOCSTR_DHCP_SIADDR          "IP address of next server to use in boostrap. Returned in DHCPOFFER\n" \
                                    "and DHCPACK by server."
#define DOCSTR_DHCP_GIADDR          "Relay agent IP address, used in booting via a relay agent."
#define DOCSTR_DHCP_CHADDR          "Client hardware address. It accepts a bytes object in the format\n" \
                                    "xx:xx:xx:xx:xx:xx, where 'xx' is of base '16'."
#define DOCSTR_DHCP_SNAME           "Server host name that contains a TFTP server."
#define DOCSTR_DHCP_FILE            "The filename of a boot image on a TFTP server."
#define DOCSTR_DHCP_COOKIE          "The magic cookie as is defined in RFC 1497. Should be set to 0x63825363."

#endif