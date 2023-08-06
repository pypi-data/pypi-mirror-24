
/*
 * File represents the datatype 'packet'.
 * It works as the base class for all protocols.
 * It is a simple type which contains methods that
 * can decipher what type of packet it is; whether
 * it is a tcp packet, udp packet, arp packet, etc.
 */
#include "include/packet.h"

static PyObject *packet_is_ethernet(packet *self);
static PyObject *packet_is_arp(packet *self);
static PyObject *packet_is_icmp(packet *self);
static PyObject *packet_is_tcp(packet *self);
static PyObject *packet_is_udp(packet *self);
static PyObject *packet_is_dhcp(packet *self);
PyObject *packet_is_ipv4(packet *self);
PyObject *packet_is_ipv6(packet *self);

static PyMethodDef packet_methods[] = {
    { "is_ethernet", (PyCFunction)packet_is_ethernet,
       METH_NOARGS, DOCSTR_PACKET_IS_ETH
    },
    { "is_arp", (PyCFunction)packet_is_arp,
       METH_NOARGS, DOCSTR_PACKET_IS_ARP
    },
    { "is_ipv4", (PyCFunction)packet_is_ipv4,
       METH_NOARGS, DOCSTR_PACKET_IS_IPV4
    },
    { "is_ipv6", (PyCFunction)packet_is_ipv6,
       METH_NOARGS, DOCSTR_PACKET_IS_IPV6
    },
    { "is_icmp", (PyCFunction)packet_is_icmp,
       METH_NOARGS, DOCSTR_PACKET_IS_ICMP
    },
    { "is_tcp", (PyCFunction)packet_is_tcp,
       METH_NOARGS, DOCSTR_PACKET_IS_TCP
    },
    { "is_udp", (PyCFunction)packet_is_udp,
       METH_NOARGS, DOCSTR_PACKET_IS_UDP
    },
    { "is_dhcp", (PyCFunction)packet_is_dhcp,
       METH_NOARGS, DOCSTR_PACKET_IS_DHCP
    },
    { NULL }
};

PyTypeObject packet_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.packet",       /* tp_name */
    sizeof(packet),            /* tp_basicsize */
    0,                         /* tp_itemsize */
    0,                         /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
    Py_TPFLAGS_BASETYPE,       /* tp_flags */
    0,                         /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    packet_methods,            /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    PyType_GenericNew,         /* tp_new */
};

extern PyTypeObject ethernet_type;
extern PyTypeObject arp_type;
extern PyTypeObject ip_type;
extern PyTypeObject icmp_type;
extern PyTypeObject tcp_type;
extern PyTypeObject udp_type;
extern PyTypeObject dhcp_type;

static PyObject *packet_is_ethernet(packet *self)
{
    if (Py_TYPE(self) == &ethernet_type)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *packet_is_arp(packet *self)
{
    if (Py_TYPE(self) == &arp_type)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *packet_is_icmp(packet *self)
{
    if (Py_TYPE(self) == &icmp_type)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *packet_is_tcp(packet *self)
{
    if (Py_TYPE(self) == &tcp_type)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *packet_is_udp(packet *self)
{
    if (Py_TYPE(self) == &udp_type)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *packet_is_dhcp(packet *self)
{
    if (Py_TYPE(self) == &dhcp_type)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

int packet_add_type(PyObject *module)
{
    if (PyType_Ready(&packet_type) < 0)
        return 0;
    Py_INCREF(&packet_type);
    PyModule_AddObject(module, "packet", (PyObject *)&packet_type);

    return 1;
}