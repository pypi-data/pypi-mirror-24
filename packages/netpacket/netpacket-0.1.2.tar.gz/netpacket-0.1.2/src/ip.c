
#include "include/ip.h"

static int ip_init(ip *self, PyObject *args,
                   PyObject *kwds);
static PyObject *ip_repr(ip *self);
static PyObject *ip_get_attr(ip *self,
                             void *closure);
static int ip_set_attr(ip *self, PyObject *value,
                       void *closure);
static PyObject *ip_get_source(ip *self,
                               void *closure);
static PyObject *ip_get_dest(ip *self,
                             void *closure);
static int ip_set_source(ip *self, PyObject *value,
                         void *closure);
static int ip_set_dest(ip *self, PyObject *value,
                       void *closure);
static PyObject *ip_calc_len(ip *self);
static PyObject *ipv4_calc_csum(ip *self);
static PyObject *ip_to_bytes(ip *self);

static PyMethodDef ip_methods[] = {
    { "calc_len", (PyCFunction)ip_calc_len,
       METH_NOARGS, DOCSTR_IP_CALC_LEN
    },
    { "calc_csum", (PyCFunction)ipv4_calc_csum,
       METH_NOARGS, DOCSTR_IPV4_CALC_CSUM
    },
    { "to_bytes", (PyCFunction)ip_to_bytes,
       METH_NOARGS, DOCSTR_IP_TO_BYTES
    },
    { NULL }
};

static PyGetSetDef ip_gs[] = {
    { "ip_version", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IP_VERSION,
       IP_VERSION
    },
    { "ip_len", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IP_LEN,
       IP_LEN
    },
    { "ip_proto", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IP_PROTO,
       IP_PROTO
    },
    { "ip_ttl", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IP_TTL,
       IP_TTL
    },
    { "ip_ds", (getter)ip_get_attr,
      (setter)ip_set_attr, NULL, IP_DS
    },
    { "ip_ecn", (getter)ip_get_attr,
      (setter)ip_set_attr, NULL, IP_ECN
    },
    { "ip_identifier", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IPV4_IDENTIFIER, IPV4_IDENTIFIER
    },
    { "ip_flags", (getter)ip_get_attr,
       (setter)ip_set_attr, DOCSTR_IPV4_FLAGS, IPV4_FLAGS
    },
    { "ip_frag_off", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IPV4_FRAGMENT_OFF, IPV4_FRAG_OFF
    },
    { "ip_csum", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IPV4_CSUM,
       IPV4_CSUM
    },
    { "ip_hlen", (getter)ip_get_attr,
      (setter)ip_set_attr, DOCSTR_IPV4_HLEN,
       IPV4_HLEN
    },
    { "ip_flow_label", (getter)ip_get_attr,
      (setter)ip_set_attr, NULL, IPV6_FLOW_LABEL
    },
    { "ip_source", (getter)ip_get_source,
      (setter)ip_set_source, DOCSTR_IP_SOURCE,
       NULL
    },
    { "ip_dest", (getter)ip_get_dest,
      (setter)ip_set_dest, DOCSTR_IP_DEST,
       NULL
    },
    { NULL }
};

PyTypeObject ip_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.ip",           /* tp_name */
    sizeof(ip),                /* tp_basicsize */
    0,                         /* tp_itemsize */
    0,                         /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getclosure */
    0,                         /* tp_setclosure */
    0,                         /* tp_reserved */
    (reprfunc)ip_repr,         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getclosureo */
    0,                         /* tp_setclosureo */
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
    ip_methods,                /* tp_methods */
    0,                         /* tp_members */
    ip_gs,                     /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)ip_init,         /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

extern PyTypeObject ethernet_type;

static int ip_init(ip *self, PyObject *args,
                   PyObject *kwds)
{
    self->ip_type = PROTO_IPV4;

    if (!PyArg_ParseTuple(args, "|H", &self->ip_type)) return -1;
    
    if (self->ip_type == PROTO_IPV4)
        self->ip_size = sizeof(struct ipv4);
    else if (self->ip_type == PROTO_IPV6)
        self->ip_size = sizeof(struct ipv6);
    else {
        PyErr_Format(PyExc_ValueError, "Unrecognized ip type (0x%x) passed",
                     self->ip_type);
        return -1;
    }
    return 0;
}

static PyObject *ip_repr(ip *self)
{
    return PyUnicode_FromFormat("<%s%s object at %p>", ip_type.tp_name,
                                pkt_is_ipv4(self) ? "v4" : "v6", self);
}

static PyObject *ip_get_attr(ip *self,
                             void *closure)
{
    u32 bits;

    if (closure == IP_VERSION) {
        if (pkt_is_ipv4(self))
            return PyLong_FromLong(self->__ipv4.version);
        else
#if __BYTE_ORDER == __LITTLE_ENDIAN
            return PyLong_FromLong((self->__ipv6.vtf >> 4) & 0x0f);
#elif __BYTE_ORDER == __BIG_ENDIAN
            return PyLong_FromLong(self->__ipv6.vtf >> 28);
#endif
    }
    if (closure == IP_LEN) {
        if (pkt_is_ipv4(self))
            return PyLong_FromLong(ntohs(self->__ipv4.len));
        else
            return PyLong_FromLong(ntohs(self->__ipv6.len));
    }
    if (closure == IP_PROTO) {
        if (pkt_is_ipv4(self))
            return PyLong_FromLong(self->__ipv4.proto);
        else
            return PyLong_FromLong(self->__ipv6.next_hdr);
    }
    if (closure == IP_TTL) {
        if (pkt_is_ipv4(self))
            return PyLong_FromLong(self->__ipv4.ttl);
        else
            return PyLong_FromLong(self->__ipv6.hop_lmt);
    }
    if (closure == IP_DS) {
        if (pkt_is_ipv4(self))
            return PyLong_FromLong(self->__ipv4.ds);
        else {
#if __BYTE_ORDER == __LITTLE_ENDIAN
            bits = (self->__ipv6.vtf & 0xc000) >> 14 |
            (self->__ipv6.vtf & 0x0f) << 2;
            return PyLong_FromLong(bits);
#elif __BYTE_ORDER == __BIG_ENDIAN
            return PyLong_FromLong((self->__ipv6.vtf & 0xfc00000) >> 22);
#endif
        }
    }
    if (closure == IP_ECN) {
        if (pkt_is_ipv4(self))
            return PyLong_FromLong(self->__ipv4.ecn);
        else
#if __BYTE_ORDER == __LITTLE_ENDIAN
            return PyLong_FromLong((self->__ipv6.vtf & 0x3000) >> 12);
#elif __BYTE_ORDER == __BIG_ENDIAN
            return PyLong_FromLong((self->__ipv6.vtf & 0x300000) >> 20);
#endif
    }
    if (closure == IPV4_IDENTIFIER) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        return PyLong_FromLong(ntohs(self->__ipv4.identifier));
    }
    if (closure == IPV4_FLAGS) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        return PyLong_FromLong(self->__ipv4.frag_flags_off);
    }
    if (closure == IPV4_FRAG_OFF) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        return PyLong_FromLong(self->__ipv4.frag_flags_off);
    }
    if (closure == IPV4_CSUM) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        return PyLong_FromLong(ntohs(self->__ipv4.csum));
    }
    if (closure == IPV4_HLEN) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        return PyLong_FromLong(self->__ipv4.hlen);
    }
    if (closure == IPV6_FLOW_LABEL) {
        if (pkt_is_ipv4(self)) {
            PyErr_Format(PyExc_AttributeError, "'_packet.ipv4' object has no attribute"
                 " '%s'", ip_attr_string(closure));
            return NULL;
        }
#if __BYTE_ORDER == __LITTLE_ENDIAN
        bits = (self->__ipv6.vtf & 0xff000000) >> 24 |
        (self->__ipv6.vtf & 0x00ff0000) >> 8 |
        (self->__ipv6.vtf & 0xf00) << 8;
        return PyLong_FromLong(bits);
#elif __BYTE_ORDER == __BIG_ENDIAN
        return PyLong_FromLong(self->__ipv6.vtf & 0x000fffff);
#endif
    }
    Py_RETURN_NONE;
ipv6_err:
    PyErr_Format(PyExc_AttributeError, "'_packet.ipv6' object has no attribute"
                 " '%s'", ip_attr_string(closure));
    return NULL;
}

static int ip_set_attr(ip *self, PyObject *value,
                       void *closure)
{
    u32 bits;

    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", ip_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' expects"
                     " type 'int'", ip_attr_string(closure));
        return -1;
    }
    if (closure == IP_VERSION) {
        if (pkt_is_ipv4(self))
            self->__ipv4.version = PyLong_AsLong(value);
        else
#if __BYTE_ORDER == __LITTLE_ENDIAN
            self->__ipv6.vtf |= (PyLong_AsLong(value) & 0x0f) << 4;
#elif __BYTE_ORDER == __BIG_ENDIAN
            self->__ipv6.vtf |= (PyLong_AsLong(value) & 0x0f) << 28;
#endif
    }
    else if (closure == IP_LEN) {
        if (pkt_is_ipv4(self))
            self->__ipv4.len = htons(PyLong_AsLong(value));
        else
            self->__ipv6.len = htons(PyLong_AsLong(value));
    }
    else if (closure == IP_PROTO) {
        if (pkt_is_ipv4(self))
            self->__ipv4.proto = PyLong_AsLong(value);
        else
            self->__ipv6.next_hdr = PyLong_AsLong(value);
    }
    else if (closure == IP_TTL) {
        if (pkt_is_ipv4(self))
            self->__ipv4.ttl = PyLong_AsLong(value);
        else
            self->__ipv6.hop_lmt = PyLong_AsLong(value);
    }
    else if (closure == IP_DS) {
        if (pkt_is_ipv4(self))
            self->__ipv4.ds = PyLong_AsLong(value);
        else {
            bits = PyLong_AsLong(value);
#if __BYTE_ORDER == __LITTLE_ENDIAN
            self->__ipv6.vtf |= (bits & 0x03) << 14 | (bits & 0x3c) >> 2;
#elif __BYTE_ORDER == __BIG_ENDIAN
            self->__ipv6.vtf |= (bits & 0x3f) << 22;
#endif
        }
    }
    else if (closure == IP_ECN) {
        if (pkt_is_ipv4(self))
            self->__ipv4.ecn = PyLong_AsLong(value);
        else
#if __BYTE_ORDER == __LITTLE_ENDIAN
            self->__ipv6.vtf |= (PyLong_AsLong(value) & 0x03) << 12;
#elif __BYTE_ORDER == __BIG_ENDIAN
            self->__ipv6.vtf |= (PyLong_AsLong(value) & 0x03) << 20;
#endif
    }
    else if (closure == IPV4_IDENTIFIER) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        self->__ipv4.identifier = htons(PyLong_AsLong(value));
    }
    else if (closure == IPV4_FLAGS) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
#if __BYTE_ORDER == __LITTLE_ENDIAN
        self->__ipv4.frag_flags_off |= (PyLong_AsLong(value) & 0x03) << 5;
#elif __BYTE_ORDER == __BIG_ENDIAN
        self->__ipv4.frag_flags_off |= (PyLong_AsLong(value) & 0x03) << 13;
#endif
    }
    else if (closure == IPV4_FRAG_OFF) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
#if __BYTE_ORDER == __LITTLE_ENDIAN
        bits = PyLong_AsLong(value);
        self->__ipv4.frag_flags_off |= (bits & 0xff) << 8 | (bits & 0x1f00) >> 8;
#elif __BYTE_ORDER == __BIG_ENDIAN
        self->__ipv4.frag_flags_off |= (PyLong_AsLong(value) & 0x1fff);
#endif
    }
    else if (closure == IPV4_CSUM) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        self->__ipv4.csum = htons(PyLong_AsLong(value));
    }
    else if (closure == IPV4_HLEN) {
        if (!pkt_is_ipv4(self)) goto ipv6_err;
        self->__ipv4.hlen = PyLong_AsLong(value) / 4;
    }
    else if (closure == IPV6_FLOW_LABEL) {
        if (pkt_is_ipv4(self)) {
            PyErr_Format(PyExc_AttributeError, "'_packet.ipv4' object has no attribute"
                 " '%s'", ip_attr_string(closure));
            return -1;
        }
#if __BYTE_ORDER == __LITTLE_ENDIAN
        bits = PyLong_AsLong(value);
        self->__ipv6.vtf |= (bits & 0xff) << 24 | (bits & 0xff00) << 8 |
        (bits & 0xf0000) >> 8;
#elif __BYTE_ORDER == __BIG_ENDIAN
        self->__ipv6.vtf |= PyLong_AsLong(value) & 0x000fffff;
#endif
    }
    return 0;
ipv6_err:
    PyErr_Format(PyExc_AttributeError, "'_packet.ipv6' object has no attribute"
                 " '%s'", ip_attr_string(closure));
    return -1;
}

static PyObject *ip_get_source(ip *self,
                               void *closure)
{
    if (pkt_is_ipv4(self))
        return __ipv4_get_addr(self->__ipv4.source);
    else
        return __ipv6_get_addr(self->__ipv6.source);
}

static PyObject *ip_get_dest(ip *self,
                             void *closure)
{
    if (pkt_is_ipv4(self))
        return __ipv4_get_addr(self->__ipv4.dest);
    else
        return __ipv6_get_addr(self->__ipv6.dest);
}

static int ip_set_source(ip *self, PyObject *value,
                         void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'ip_source' "
                        "can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'ip_source' expects "
                        "type 'bytes'");
        return -1;
    }
    if (pkt_is_ipv4(self))
        return __ipv4_set_addr(value, &self->__ipv4.source);
    else
        return __ipv6_set_addr(value, self->__ipv6.source);
}

static int ip_set_dest(ip *self, PyObject *value,
                       void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'ip_dest' "
                        "can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'ip_dest' expects "
                        "type 'bytes'");
        return -1;
    }
    if (pkt_is_ipv4(self))
        return __ipv4_set_addr(value, &self->__ipv4.dest);
    else
        return __ipv6_set_addr(value, self->__ipv6.dest);
}

int ip_add_type(PyObject *module)
{
    ip_type.tp_base = &ethernet_type;
    if (PyType_Ready(&ip_type) < 0)
        return 0;
    Py_INCREF(&ip_type);
    PyModule_AddObject(module, "ip", (PyObject *)&ip_type);

    return 1;
}

PyObject *create_ip_instance(int caplen,
                             const unsigned char *pkt,
                             u16 _ip_type)
{
    PyObject *obj;

    obj = ip_type.tp_new(&ip_type, NULL, NULL);
    memcpy(&ETHERNET_CAST(obj)->__ethernet, pkt,
           sizeof(struct ethernet));
    if (_ip_type == PROTO_IPV4) {
        memcpy(&IP_CAST(obj)->__ipv4,
              (pkt + sizeof(struct ethernet)),
               sizeof(struct ipv4));
        IP_CAST(obj)->ip_size = sizeof(struct ipv4);
    }
    else {
        memcpy(&IP_CAST(obj)->__ipv6,
              (pkt + sizeof(struct ethernet)),
               sizeof(struct ipv6));
        IP_CAST(obj)->ip_size = sizeof(struct ipv6);
    }
    IP_CAST(obj)->ip_type = _ip_type;

    return obj;
}

static PyObject *ip_to_bytes(ip *self)
{
    PyObject *obj;
    int size;
    char *buf;

    size = sizeof(struct ethernet) + self->ip_size;
    buf = (char *)malloc(size);

    memcpy(buf, &ETHERNET_CAST(self)->__ethernet,
           sizeof(struct ethernet));
    if (pkt_is_ipv4(self))
        memcpy(buf + sizeof(struct ethernet),
               &self->__ipv4,
               self->ip_size);
    else
        memcpy(buf + sizeof(struct ethernet),
               &self->__ipv6,
               self->ip_size);
    obj = PyBytes_FromStringAndSize(buf, size);
    free(buf);

    return obj;
}

char *ip_attr_string(void *closure)
{
    if (closure == IP_VERSION)
        return "ip_version";
    if (closure == IP_LEN)
        return "ip_len";
    if (closure == IP_PROTO)
        return "ip_proto";
    if (closure == IP_TTL)
        return "ip_ttl";
    if (closure == IP_DS)
        return "ip_ds";
    if (closure == IP_ECN)
        return "ip_ecn";
    if (closure == IPV4_IDENTIFIER)
        return "ip_identifier";
    if (closure == IPV4_FRAG_OFF)
        return "ip_frag_off";
    if (closure == IPV4_CSUM)
        return "ip_csum";
    if (closure == IPV4_HLEN)
        return "ip_hlen";
    if (closure == IPV6_FLOW_LABEL)
        return "ip_flow_label";

    return NULL;
}

void __ip_calc_len(ip *self, Py_ssize_t _len)
{
    Py_ssize_t len = 0;

    if (_len)
        len += _len;
    if (pkt_is_ipv4(self))
        self->__ipv4.len = htons(len + self->ip_size);
    else
        self->__ipv6.len = htons(len);
}

static PyObject *ip_calc_len(ip *self)
{
    __ip_calc_len(self, 0);

    Py_RETURN_NONE;
}

void __ipv4_calc_csum(struct ipv4 *ips)
{
    int i, sum = 0;

    ips->csum = 0;
    for (i = 0; i < sizeof(struct ipv4) / 2; i++)
        sum += ((unsigned short *)ips)[i];
    while (sum >> 16)
        sum = (sum & 0xffff) + (sum >> 16);

    ips->csum = (unsigned short)~sum; 
}

static PyObject *ipv4_calc_csum(ip *self)
{
    if (!pkt_is_ipv4(self)) {
        PyErr_Format(PyExc_AttributeError, "'_packet.ipv6' object has no attribute"
                     " 'calc_csum'");
        return NULL;
    }
    __ipv4_calc_csum(&self->__ipv4);

    Py_RETURN_NONE;
}

/*
 * These two routines actually belong to the
 * 'packet' type, but since 'packet.h' lacks
 * headers that is required to do the condition
 * statements they are defined here.
 */
PyObject *packet_is_ipv4(packet *self)
{
    if (Py_TYPE(self) == &ip_type &&
        pkt_is_ipv4(IP_CAST(self)))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

PyObject *packet_is_ipv6(packet *self)
{
    if (Py_TYPE(self) == &ip_type &&
        !pkt_is_ipv4(IP_CAST(self)))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}