
#ifndef INCLUDE_PACKET_H
#define INCLUDE_PACKET_H

#include <Python.h>
#include <structmember.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "types.h"
#include "utils.h"
#include "docstrings.h"

#define ETHERNET_CAST(x)    ((ethernet *)x)
#define ARP_CAST(x)         ((arp *)x)
#define IP_CAST(x)          ((ip *)x)
#define ICMP_CAST(x)        ((icmp *)x)
#define UDP_CAST(x)         ((udp *)x)
#define TCP_CAST(x)         ((tcp *)x)

typedef struct {
    PyObject_HEAD
} packet;
#define PROTO_IPV4      0x0800
#define PROTO_IPV6      0x86dd

#endif