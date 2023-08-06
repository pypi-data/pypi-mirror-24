
#include "include/tcp.h"

static PyObject *tcp_repr(tcp *self);
static PyObject *tcp_get_attr(tcp *self,
                              void *closure);
static int tcp_set_attr(tcp *self, PyObject *value,
                        void *closure);
static int tcp_set_payload(tcp *self, PyObject *value,
                           void *closure);
static PyObject *tcp_get_flags(tcp *self);
static PyObject *tcp_set_flags(tcp *self, PyObject *args,
                               PyObject *kwds);
static PyObject *tcp_calc_len(tcp *self);
static PyObject *tcp_calc_csum(tcp *self);
static PyObject *tcp_to_bytes(tcp *self);
static void tcp_dealloc(tcp *self);

static PyMethodDef tcp_methods[] = {
    { "tcp_get_flags", (PyCFunction)tcp_get_flags,
       METH_NOARGS, DOCSTR_TCP_GET_FLAGS
    },
    { "tcp_set_flags", (PyCFunction)tcp_set_flags,
       METH_VARARGS | METH_KEYWORDS, DOCSTR_TCP_SET_FLAGS
    },
    { "calc_len", (PyCFunction)tcp_calc_len,
       METH_NOARGS, DOCSTR_TCP_CALC_LEN
    },
    { "calc_csum", (PyCFunction)tcp_calc_csum,
       METH_NOARGS, DOCSTR_TCP_CALC_CSUM
    },
    { "to_bytes", (PyCFunction)tcp_to_bytes,
       METH_NOARGS, DOCSTR_TCP_TO_BYTES
    },
    { NULL }
};

static PyGetSetDef tcp_gs[] = {
    { "tcp_src", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_SRC, TCP_SRC
    },
    { "tcp_dst", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_DST, TCP_DST
    },
    { "tcp_seq", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_SEQ, TCP_SEQ
    },
    { "tcp_seq_ack", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_SEQ_ACK, TCP_SEQ_ACK
    },
    { "tcp_hlen", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_HLEN, TCP_HLEN
    },
    { "tcp_win", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_WIN, TCP_WIN
    },
    { "tcp_csum", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_CSUM, TCP_CSUM
    },
    { "tcp_urg_ptr", (getter)tcp_get_attr,
      (setter)tcp_set_attr, DOCSTR_TCP_URG_PTR, TCP_URG_PTR
    },
    { "tcp_payload", (getter)tcp_get_attr,
      (setter)tcp_set_payload, DOCSTR_TCP_PAYLOAD, TCP_PAYLOAD
    },
    { NULL }
};

PyTypeObject tcp_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.tcp",          /* tp_name */
    sizeof(tcp),               /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)tcp_dealloc,   /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    (reprfunc)tcp_repr,        /* tp_repr */
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
    tcp_methods,               /* tp_methods */
    0,                         /* tp_members */
    tcp_gs,                    /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

extern PyTypeObject ip_type;

static PyObject *tcp_repr(tcp *self)
{
    return PyUnicode_FromFormat("<%s%s object at %p>", tcp_type.tp_name,
                                (pkt_is_ipv4(IP_CAST(self))) ? "v4" : "v6",
                                self);
}

static PyObject *tcp_get_attr(tcp *self,
                              void *closure)
{
    if (closure == TCP_SRC)
        return PyLong_FromLong(ntohs(self->__tcp.src));
    if (closure == TCP_DST)
        return PyLong_FromLong(ntohs(self->__tcp.dst));
    if (closure == TCP_SEQ)
        return PyLong_FromLong(ntohl(self->__tcp.seq));
    if (closure == TCP_SEQ_ACK)
        return PyLong_FromLong(ntohl(self->__tcp.seq_ack));
    if (closure == TCP_HLEN)
        return PyLong_FromLong(self->__tcp.hlen << 2);
    if (closure == TCP_WIN)
        return PyLong_FromLong(ntohs(self->__tcp.win_size));
    if (closure == TCP_CSUM)
        return PyLong_FromLong(ntohs(self->__tcp.csum));
    if (closure == TCP_URG_PTR)
        return PyLong_FromLong(ntohs(self->__tcp.urg_ptr));
    if (closure == TCP_PAYLOAD)
        if (self->payload) {
            Py_INCREF(self->payload);
            return self->payload;
        }

    Py_RETURN_NONE;
}

static int tcp_set_attr(tcp *self, PyObject *value,
                        void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not be"
                     " deleted", tcp_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'int'", tcp_attr_string(closure));
        return -1;
    }
    if (closure == TCP_SRC)
        self->__tcp.src = htons(PyLong_AsLong(value));
    else if (closure == TCP_DST)
        self->__tcp.dst = htons(PyLong_AsLong(value));
    else if (closure == TCP_SEQ)
        self->__tcp.seq = htonl(PyLong_AsLong(value));
    else if (closure == TCP_SEQ_ACK)
        self->__tcp.seq_ack = htonl(PyLong_AsLong(value));
    else if (closure == TCP_HLEN)
        self->__tcp.hlen = PyLong_AsLong(value) >> 2;
    else if (closure == TCP_WIN)
        self->__tcp.win_size = htons(PyLong_AsLong(value));
    else if (closure == TCP_CSUM)
        self->__tcp.csum = htons(PyLong_AsLong(value));
    else if (closure == TCP_URG_PTR)
        self->__tcp.urg_ptr = htons(PyLong_AsLong(value));

    return 0;
}

static int tcp_set_payload(tcp *self, PyObject *value,
                           void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'tcp_payload'"
                        " can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'tcp_payload' only"
                        " accepts a type of 'bytes'");
        return -1;
    }
    Py_XDECREF(self->payload);
    Py_INCREF(value);
    self->payload = value;
    
    return 0;
}

static PyObject *tcp_get_flags(tcp *self)
{
    PyObject *obj, *flag;

    obj = PyDict_New();
    if (!obj)
        return NULL;
    flag = PyLong_FromLong(self->__tcp.nonce);
    if (PyDict_SetItemString(obj, "nonce", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.cwr);
    if (PyDict_SetItemString(obj, "cwr", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.echo);
    if (PyDict_SetItemString(obj, "echo", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.urg);
    if (PyDict_SetItemString(obj, "urg", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.ack);
    if (PyDict_SetItemString(obj, "ack", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.push);
    if (PyDict_SetItemString(obj, "push", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.rst);
    if (PyDict_SetItemString(obj, "rst", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.syn);
    if (PyDict_SetItemString(obj, "syn", flag) == -1)
        goto err;

    flag = PyLong_FromLong(self->__tcp.fin);
    if (PyDict_SetItemString(obj, "fin", flag) == -1)
        goto err;

    return obj;
err:
    Py_DECREF(obj);
    return NULL;
}

static PyObject *tcp_set_flags(tcp *self, PyObject *args,
                               PyObject *kwds)
{
    u8 nonce = 0, cwr = 0, echo = 0, urg = 0;
    u8 ack = 0, push = 0, rst = 0, syn = 0, fin = 0;
    static char *kw[] = { "nonce", "cwr", "echo", "urg",
                          "ack", "push", "rst", "syn", "fin" };

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|BBBBBBBBB", kw,
                                     &nonce, &cwr, &echo, &urg,
                                     &ack, &push, &rst, &syn, &fin))
        return NULL;
    self->__tcp.nonce = nonce;
    self->__tcp.cwr = cwr;
    self->__tcp.echo = echo;
    self->__tcp.urg = urg;
    self->__tcp.ack = ack;
    self->__tcp.push = push;
    self->__tcp.rst = rst;
    self->__tcp.syn = syn;
    self->__tcp.fin = fin;

    Py_RETURN_NONE;
}

static void tcp_dealloc(tcp *self)
{
    Py_XDECREF(self->payload);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

int tcp_add_type(PyObject *module)
{
    tcp_type.tp_base = &ip_type;
    if (PyType_Ready(&tcp_type) < 0)
        return 0;
    Py_INCREF(&tcp_type);
    PyModule_AddObject(module, "tcp", (PyObject *)&tcp_type);

    return 1;
}

PyObject *create_tcp_instance(int caplen,
                              const unsigned char *pkt,
                              u16 _ip_type)
{
    PyObject *obj;
    int offset = 0;
    const unsigned char *payload;

    obj = tcp_type.tp_new(&tcp_type, NULL, NULL);
    IP_CAST(obj)->ip_type = _ip_type;

    memcpy(&ETHERNET_CAST(obj)->__ethernet, pkt,
           sizeof(struct ethernet));
    offset += sizeof(struct ethernet);
    if (_ip_type == PROTO_IPV4) {
        memcpy(&IP_CAST(obj)->__ipv4, (pkt + offset),
               sizeof(struct ipv4));
        offset += sizeof(struct ipv4);
        offset += skip_ipv4_opts((IP_CAST(obj)->__ipv4.hlen << 2));
        IP_CAST(obj)->ip_size = sizeof(struct ipv4);
    }
    else {
        memcpy(&IP_CAST(obj)->__ipv6, (pkt + offset),
               sizeof(struct ipv6));
        offset += sizeof(struct ipv6);
        IP_CAST(obj)->ip_size = sizeof(struct ipv6);
    }
    memcpy(&TCP_CAST(obj)->__tcp, (pkt + offset),
           sizeof(struct tcp));
    /*
     * TCP options will be available in the future. For now
     * we jump the options if they are found.
     */
    offset += (TCP_CAST(obj)->__tcp.hlen << 2) -
               sizeof(struct tcp);
    payload = (pkt + offset);
    TCP_CAST(obj)->payload = PyBytes_FromStringAndSize(payload,
                                                       caplen - offset);
    return obj;
}

static PyObject *tcp_to_bytes(tcp *self)
{
    PyObject *obj;
    Py_ssize_t size, psize;
    int offset = 0;
    char *buf, *pbuf;

    size = sizeof(struct ethernet) + IP_CAST(self)->ip_size +
           sizeof(struct tcp);
    if (self->payload)
        size += PyBytes_Size(self->payload);
    buf = (char *)malloc(size);

    memcpy(buf, &ETHERNET_CAST(self)->__ethernet,
           sizeof(struct ethernet));
    offset += sizeof(struct ethernet);
    if (pkt_is_ipv4(IP_CAST(self))) {
        memcpy((buf + offset), &IP_CAST(self)->__ipv4,
                IP_CAST(self)->ip_size);
    }
    else {
        memcpy((buf + offset), &IP_CAST(self)->__ipv6,
                IP_CAST(self)->ip_size);
    }
    offset += IP_CAST(self)->ip_size;
    memcpy((buf + offset), &self->__tcp, sizeof(struct tcp));
    offset += sizeof(struct tcp);
    if (self->payload) {
        if (PyBytes_AsStringAndSize(self->payload,
                                    &pbuf, &psize) == -1) {
            free(buf);
            return NULL;
        }
        memcpy((buf + offset), pbuf, psize);
    }
    obj = PyBytes_FromStringAndSize(buf, size);
    free(buf);
    
    return obj;
}

char *tcp_attr_string(void *closure)
{
    if (closure == TCP_SRC)
        return "tcp_src";
    if (closure == TCP_DST)
        return "tcp_dst";
    if (closure == TCP_SEQ)
        return "tcp_seq";
    if (closure == TCP_SEQ_ACK)
        return "tcp_seq_ack";
    if (closure == TCP_HLEN)
        return "tcp_hlen";
    if (closure == TCP_WIN)
        return "tcp_win";
    if (closure == TCP_CSUM)
        return "tcp_csum";
    if (closure == TCP_URG_PTR)
        return "tcp_urg_ptr";
    if (closure == TCP_PAYLOAD)
        return "tcp_payload";

    return NULL;
}

/*
 * TCP doesnt contain a length field, so to
 * minimize the required code in '__ip_calc_len'
 * we use this routine to just pass the hlen of
 * the TCP header which is '20' + payload.
 */
static PyObject *tcp_calc_len(tcp *self)
{
    Py_ssize_t len = 20;

    if (self->payload)
        len += PyBytes_Size(self->payload);
    __ip_calc_len(IP_CAST(self), len);

    Py_RETURN_NONE;
}

/*
 * High order bits are checked at the end
 * of the subroutine. I felt like its faster this
 * way instead of checking for a high bit while
 * iterating. As long as the packet is <= MTU
 * 32 bits should be enough to hold the calculations
 * until the end. If above, the checksum calculation
 * will overflow 'sum' in the long run. If you plan on
 * sending > MTU on the lo interface, you should probably
 * add a: if (sum > 0xffff) sum = (sum & 0xffff) + (sum >> 16)
 * line in the data section, or check for 0x80000000 using the AND
 * operator ( Less usage of the CPU ).
 */
u16 __tcp_calc_csum(void *pseudo, u16 pseudo_len,
                    char *data, Py_ssize_t len)
{
    int i, sum = 0;

    for (i = 0; i < pseudo_len / 2; i++)
        sum += ((unsigned short *)pseudo)[i];
    if (data)
        for (i = 0; i < len / 2; i++)
            sum += ((unsigned short *)data)[i];
    while (sum >> 16)
        sum = (sum & 0xffff) + (sum >> 16);

    return (u16)~sum;
}

u16 tcp_calc_csum_v4(tcp *self, char *data,
                     Py_ssize_t len)
{
    struct tcp_v4_pseudo pseudo;

    pseudo.source = IP_CAST(self)->__ipv4.source;
    pseudo.dest = IP_CAST(self)->__ipv4.dest;
    pseudo.zero = 0;
    pseudo.proto = IP_CAST(self)->__ipv4.proto;
    pseudo.len = htons((self->__tcp.hlen << 2) + len);
    memcpy(&pseudo.tcp_hdr, &self->__tcp,
           sizeof(struct tcp));

    return __tcp_calc_csum(&pseudo, sizeof(struct tcp_v4_pseudo),
                           data, len);
}

u16 tcp_calc_csum_v6(tcp *self, char *data,
                     Py_ssize_t len)
{
    struct tcp_v6_pseudo pseudo;

    memcpy(pseudo.source, IP_CAST(self)->__ipv6.source,
           sizeof(ip_v6_addr));
    memcpy(pseudo.dest, IP_CAST(self)->__ipv6.dest,
           sizeof(ip_v6_addr));
    pseudo.len = htons((self->__tcp.hlen << 2) + len);
    pseudo.zero = 0;
    pseudo.next_hdr = IP_CAST(self)->__ipv6.next_hdr;
    memcpy(&pseudo.tcp_hdr, &self->__tcp,
           sizeof(struct tcp));

    return __tcp_calc_csum(&pseudo, sizeof(struct tcp_v6_pseudo),
                           data, len);
}

static PyObject *tcp_calc_csum(tcp *self)
{
    Py_ssize_t len;
    char *data = NULL;

    if (self->payload)
        PyBytes_AsStringAndSize(self->payload, &data, &len);
    
    self->__tcp.csum = 0;
    if (pkt_is_ipv4(IP_CAST(self))) {
        self->__tcp.csum = tcp_calc_csum_v4(self, data, (len % 2) ?
                                            len + 1 : len);
        __ipv4_calc_csum(&IP_CAST(self)->__ipv4);
    }
    else {
        self->__tcp.csum = tcp_calc_csum_v6(self, data, (len % 2) ?
                                            len + 1 : len);
    }
    Py_RETURN_NONE;
}