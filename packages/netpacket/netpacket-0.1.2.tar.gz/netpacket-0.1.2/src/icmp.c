
/*
 * The ICMP implementation aims to be as modular
 * as possible, which means you are granted freedom.
 * Instead of jailing the programmer within one type
 * the programmer is free to cache values through
 * attributes that is not connected to the type which is
 * active. Every ICMP type has its own getters and setters,
 * and they all share a calc_len, to_bytes and calc_csum
 * implementation. Instead of doing allot of type = X expressions,
 * these subroutines is contained as pointers nested
 * within a ICMP type structure, and initialized in
 * icmp_set_attr_hdr once a type is assigned.
 */
#include "include/icmp.h"

static int icmp_init(icmp *self, PyObject *args,
                     PyObject *kwds);
static void icmp_dealloc(icmp *self);
static PyObject *icmp_repr(icmp *self);
static PyObject *icmp_get_attr_hdr(icmp *self,
                                   void *closure);
static int icmp_set_attr_hdr(icmp *self,
                             PyObject *value,
                             void *closure);
static PyObject *icmp_get_attr_dst_unreach(icmp *self,
                                           void *closure);
static int icmp_set_attr_dst_unreach(icmp *self,
                                     PyObject *value,
                                     void *closure);
static PyObject *icmp_get_attr_time_exc(icmp *self,
                                        void *closure);
static int icmp_set_attr_time_exc(icmp *self,
                                  PyObject *value,
                                  void *closure);
static PyObject *icmp_get_attr_param_prob(icmp *self,
                                          void *closure);
static int icmp_set_attr_param_prob(icmp *self,
                                    PyObject *value,
                                    void *closure);
static PyObject *icmp_get_attr_redirect(icmp *self,
                                        void *closure);
static int icmp_set_attr_redirect(icmp *self,
                                  PyObject *value,
                                  void *closure);
static PyObject *icmp_get_attr_echo(icmp *self,
                                    void *closure);
static int icmp_set_attr_echo(icmp *self,
                              PyObject *value,
                              void *closure);
static int icmp_set_attr_echo_pload(icmp *self,
                                    PyObject *value,
                                    void *closure);
static PyObject *icmp_get_attr_ts(icmp *self,
                                  void *closure);
static int icmp_set_attr_ts(icmp *self,
                            PyObject *value,
                            void *closure);
static PyObject *icmp_calc_len(icmp *self);
static PyObject *icmp_calc_csum(icmp *self);
static PyObject *icmp_to_bytes(icmp *self);

static PyMethodDef icmp_methods[] = {
    { "calc_len", (PyCFunction)icmp_calc_len,
       METH_NOARGS, NULL
    },
    { "calc_csum", (PyCFunction)icmp_calc_csum,
       METH_NOARGS, NULL
    },
    { "to_bytes", (PyCFunction)icmp_to_bytes,
       METH_NOARGS, NULL
    },
    { NULL }
};

static PyGetSetDef icmp_gs[] = {
    { "icmp_type", (getter)icmp_get_attr_hdr,
      (setter)icmp_set_attr_hdr, NULL,
       ICMP_TYPE
    },
    { "icmp_code", (getter)icmp_get_attr_hdr,
      (setter)icmp_set_attr_hdr, NULL,
       ICMP_CODE
    },
    { "icmp_csum", (getter)icmp_get_attr_hdr,
      (setter)icmp_set_attr_hdr, NULL,
       ICMP_CSUM
    },
    { "icmp_dst_unreach_dgram", (getter)icmp_get_attr_dst_unreach,
      (setter)icmp_set_attr_dst_unreach, NULL,
       NULL
    },
    { "icmp_time_exc_dgram", (getter)icmp_get_attr_time_exc,
      (setter)icmp_set_attr_time_exc, NULL,
       NULL
    },
    { "icmp_param_prob_ptr", (getter)icmp_get_attr_param_prob,
      (setter)icmp_set_attr_param_prob, NULL,
       ICMP_PARAM_PROB_PTR
    },
    { "icmp_param_prob_dgram", (getter)icmp_get_attr_param_prob,
      (setter)icmp_set_attr_param_prob, NULL,
       ICMP_PARAM_PROB_DGRAM
    },
    { "icmp_redirect_gwaddr", (getter)icmp_get_attr_redirect,
      (setter)icmp_set_attr_redirect, NULL,
       ICMP_REDIRECT_GW_ADDR
    },
    { "icmp_redirect_dgram", (getter)icmp_get_attr_redirect,
      (setter)icmp_set_attr_redirect, NULL,
       ICMP_REDIRECT_DGRAM
    },
    { "icmp_echo_id", (getter)icmp_get_attr_echo,
      (setter)icmp_set_attr_echo, NULL,
       ICMP_ECHO_ID
    },
    { "icmp_echo_seq", (getter)icmp_get_attr_echo,
      (setter)icmp_set_attr_echo, NULL,
       ICMP_ECHO_SEQ
    },
    { "icmp_echo_ts", (getter)icmp_get_attr_echo,
      (setter)icmp_set_attr_echo, NULL,
       ICMP_ECHO_TS
    },
    { "icmp_echo_payload", (getter)icmp_get_attr_echo,
      (setter)icmp_set_attr_echo_pload, NULL,
       ICMP_ECHO_PAYLOAD
    },
    { "icmp_ts_id", (getter)icmp_get_attr_ts,
      (setter)icmp_set_attr_ts, NULL,
       ICMP_TS_ID
    },
    { "icmp_ts_seq", (getter)icmp_get_attr_ts,
      (setter)icmp_set_attr_ts, NULL,
       ICMP_TS_SEQ
    },
    { "icmp_ts_orig", (getter)icmp_get_attr_ts,
      (setter)icmp_set_attr_ts, NULL,
       ICMP_TS_ORIG
    },
    { "icmp_ts_recv", (getter)icmp_get_attr_ts,
      (setter)icmp_set_attr_ts, NULL,
       ICMP_TS_RECV
    },
    { "icmp_ts_trans", (getter)icmp_get_attr_ts,
      (setter)icmp_set_attr_ts, NULL,
       ICMP_TS_TRANS
    },
    { NULL }
};

PyTypeObject icmp_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.icmpv4",       /* tp_name */
    sizeof(icmp),              /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)icmp_dealloc,  /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    (reprfunc)icmp_repr,       /* tp_repr */
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
    icmp_methods,              /* tp_methods */
    0,                         /* tp_members */
    icmp_gs,                   /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)icmp_init,       /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

extern PyTypeObject ip_type;

static int icmp_init(icmp *self, PyObject *args,
                     PyObject *kwds)
{
    if (!PyArg_ParseTuple(args, ""))
        return -1;
    ip_type.tp_init((PyObject *)self, args, kwds);

    /*
     * Calling calc_len, calc_csum or to_bytes on a object
     * that has not been initialized (by setting the type)
     * will cause a segfault. Easy fix by defaulting the
     * object to ICMP_ECHO_REPLY.
     */
    self->calc_len = calc_len_echo;
    self->calc_csum = calc_csum_echo;
    self->to_bytes = to_bytes_echo;

    return 0; 
}

static void icmp_dealloc(icmp *self)
{
    Py_XDECREF(self->__icmp.dst_unreach.datagram);
    Py_XDECREF(self->__icmp.time_exc.datagram);
    Py_XDECREF(self->__icmp.param_prob.datagram);
    Py_XDECREF(self->__icmp.redirect.datagram);
    Py_XDECREF(self->__icmp.echo.payload);

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *icmp_repr(icmp *self)
{
    return PyUnicode_FromFormat("<%s object at %p>", icmp_type.tp_name);
}

static PyObject *icmp_get_attr_hdr(icmp *self,
                                   void *closure)
{
    if (closure == ICMP_TYPE)
        return PyLong_FromLong(self->__icmp.hdr.type);
    if (closure == ICMP_CODE)
        return PyLong_FromLong(self->__icmp.hdr.code);
    if (closure == ICMP_CSUM)
        return PyLong_FromLong(ntohs(self->__icmp.hdr.csum));

    Py_RETURN_NONE;
}

static int icmp_set_attr_hdr(icmp *self,
                             PyObject *value,
                             void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", icmp_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'int'", icmp_attr_string(closure));
        return -1;
    }
    /*
     * If the field is type, some if checks needs to be
     * made to initialize the correct subroutine pointers
     * nested within self->__icmp. These subroutine pointers
     * will take care of calculating both the length and the
     * checksum. It will also take care of creating a proper
     * to_bytes object.
     */
    if (closure == ICMP_TYPE) {
        self->__icmp.hdr.type = PyLong_AsLong(value);
        switch(self->__icmp.hdr.type) {
            case ICMP_DST_UNREACH:
                self->calc_len = calc_len_dst_unreach;
                self->calc_csum = calc_csum_dst_unreach;
                self->to_bytes = to_bytes_dst_unreach;
            break;
            case ICMP_TIME_EXC:
                self->calc_len = calc_len_time_exc;
                self->calc_csum = calc_csum_time_exc;
                self->to_bytes = to_bytes_time_exc;
            break;
            case ICMP_PARAM_PROB:
                self->calc_len = calc_len_param_prob;
                self->calc_csum = calc_csum_param_prob;
                self->to_bytes = to_bytes_param_prob;
            break;
            case ICMP_REDIRECT:
                self->calc_len = calc_len_redirect;
                self->calc_csum = calc_csum_redirect;
                self->to_bytes = to_bytes_redirect;
            break;
            case ICMP_ECHO_REQ:
            case ICMP_ECHO_REPLY:
                self->calc_len = calc_len_echo;
                self->calc_csum = calc_csum_echo;
                self->to_bytes = to_bytes_echo;
            break;
            case ICMP_TS:
            case ICMP_TS_REPLY:
                self->calc_len = calc_len_ts;
                self->calc_csum = calc_csum_ts;
                self->to_bytes = to_bytes_ts;
            break;
            default:
                PyErr_Format(PyExc_ValueError, "attribute 'icmp_type' were"
                             " given an invalid value or an unimplemented"
                             " type value");
                return -1;
            break;
        }
    }
    else if (closure == ICMP_CODE)
        self->__icmp.hdr.code = PyLong_AsLong(value);
    else if (closure == ICMP_CSUM)
        self->__icmp.hdr.csum = htons(PyLong_AsLong(value));

    return 0;
}

static PyObject *icmp_get_attr_dst_unreach(icmp *self,
                                           void *closure)
{
    if (self->__icmp.dst_unreach.datagram) {
        Py_INCREF(self->__icmp.dst_unreach.datagram);
        return self->__icmp.dst_unreach.datagram;
    }
    Py_RETURN_NONE;
}

static int icmp_set_attr_dst_unreach(icmp *self,
                                     PyObject *value,
                                     void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'icmp_dst_unreach_dgram'"
                        " can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'icmp_dst_unreach_dgram'"
                        " only accepts a type of 'bytes'");
        return -1;
    }
    Py_XDECREF(self->__icmp.dst_unreach.datagram);
    Py_INCREF(value);
    self->__icmp.dst_unreach.datagram = value;

    return 0;
}

static PyObject *icmp_get_attr_time_exc(icmp *self,
                                        void *closure)
{
    if (self->__icmp.time_exc.datagram) {
        Py_INCREF(self->__icmp.time_exc.datagram);
        return self->__icmp.time_exc.datagram;
    }
    Py_RETURN_NONE;
}

static int icmp_set_attr_time_exc(icmp *self,
                                  PyObject *value,
                                  void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'icmp_time_exc_dgram'"
                        " can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'icmp_time_exc_dgram'"
                        " only accepts a type of 'bytes'");
        return -1;
    }
    Py_XDECREF(self->__icmp.time_exc.datagram);
    Py_INCREF(value);
    self->__icmp.time_exc.datagram = value;

    return 0;
}

static PyObject *icmp_get_attr_param_prob(icmp *self,
                                          void *closure)
{
    if (closure == ICMP_PARAM_PROB_PTR)
        return PyLong_FromLong(self->__icmp.param_prob.ptr);
    if (closure == ICMP_PARAM_PROB_DGRAM) {
        if (self->__icmp.param_prob.datagram) {
            Py_INCREF(self->__icmp.param_prob.datagram);
            return self->__icmp.param_prob.datagram;
        }
    }
    Py_RETURN_NONE;
}

static int icmp_set_attr_param_prob(icmp *self,
                                    PyObject *value,
                                    void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", icmp_attr_string(closure));
        return -1;
    }
    if (closure == ICMP_PARAM_PROB_PTR) {
        if (!PyLong_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "attribute 'icmp_param_prob_ptr'"
                            " only accepts a type of 'int'");
            return -1;
        }
        self->__icmp.param_prob.ptr = PyLong_AsLong(value);
    }
    else if (closure == ICMP_PARAM_PROB_DGRAM) {
        if (!PyBytes_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "attribute 'icmp_param_prob_datagram'"
                            " only accepts a type of 'bytes'");
            return -1;
        }
        Py_XDECREF(self->__icmp.param_prob.datagram);
        Py_INCREF(value);
        self->__icmp.param_prob.datagram = value;
    }
    return 0;
}

static PyObject *icmp_get_attr_redirect(icmp *self,
                                        void *closure)
{
    if (closure == ICMP_REDIRECT_GW_ADDR)
        return __ipv4_get_addr(self->__icmp.redirect.gw_addr);
    if (closure == ICMP_REDIRECT_DGRAM) {
        if (self->__icmp.redirect.datagram) {
            Py_INCREF(self->__icmp.redirect.datagram);
            return self->__icmp.redirect.datagram;
        }
    }
    Py_RETURN_NONE;
}

static int icmp_set_attr_redirect(icmp *self,
                                  PyObject *value,
                                  void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", icmp_attr_string(closure));
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'bytes'", icmp_attr_string(closure));
        return -1;
    }   
    if (closure == ICMP_REDIRECT_GW_ADDR) {
        return __ipv4_set_addr(value, &self->__icmp.redirect.gw_addr);
    }
    else if (closure == ICMP_REDIRECT_DGRAM) {
        Py_XDECREF(self->__icmp.redirect.datagram);
        Py_INCREF(value);
        self->__icmp.redirect.datagram = value;
    }
    return 0;
}

static PyObject *icmp_get_attr_echo(icmp *self,
                                    void *closure)
{
    if (closure == ICMP_ECHO_ID)
        return PyLong_FromLong(ntohs(self->__icmp.echo.id));
    if (closure == ICMP_ECHO_SEQ)
        return PyLong_FromLong(ntohs(self->__icmp.echo.seq));
    if (closure == ICMP_ECHO_TS)
        return PyLong_FromLong(ntohl(self->__icmp.echo.ts));
    if (closure == ICMP_ECHO_PAYLOAD) {
        if (self->__icmp.echo.payload) {
            Py_INCREF(self->__icmp.echo.payload);
            return self->__icmp.echo.payload;
        }
    }
    Py_RETURN_NONE;
}

static int icmp_set_attr_echo(icmp *self,
                              PyObject *value,
                              void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", icmp_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'int'", icmp_attr_string(closure));
        return -1;
    }
    if (closure == ICMP_ECHO_ID)
        self->__icmp.echo.id = htons(PyLong_AsLong(value));
    else if (closure == ICMP_ECHO_SEQ)
        self->__icmp.echo.seq = htons(PyLong_AsLong(value));
    else if (closure == ICMP_ECHO_TS)
        self->__icmp.echo.ts = htonl(PyLong_AsLong(value));

    return 0;
}

static int icmp_set_attr_echo_pload(icmp *self,
                                    PyObject *value,
                                    void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'icmp_echo_payload'"
                        " can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'icmp_echo_payload' only"
                        " accepts a type of 'bytes'");
        return -1;
    }
    Py_XDECREF(self->__icmp.echo.payload);
    Py_INCREF(value);
    self->__icmp.echo.payload = value;

    return 0;
}

static PyObject *icmp_get_attr_ts(icmp *self,
                                  void *closure)
{
    if (closure == ICMP_TS_ID)
        return PyLong_FromLong(ntohs(self->__icmp.ts.id));
    if (closure == ICMP_TS_SEQ)
        return PyLong_FromLong(ntohs(self->__icmp.ts.seq));
    if (closure == ICMP_TS_ORIG)
        return PyLong_FromLong(ntohl(self->__icmp.ts.orig));
    if (closure == ICMP_TS_RECV)
        return PyLong_FromLong(ntohl(self->__icmp.ts.recv));
    if (closure == ICMP_TS_TRANS)
        return PyLong_FromLong(ntohl(self->__icmp.ts.trans));

    Py_RETURN_NONE;
}

static int icmp_set_attr_ts(icmp *self,
                            PyObject *value,
                            void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", icmp_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'int'", icmp_attr_string(closure));
        return -1;
    }
    if (closure == ICMP_TS_ID)
        self->__icmp.ts.id = htons(PyLong_AsLong(value));
    else if (closure == ICMP_TS_SEQ)
        self->__icmp.ts.seq = htons(PyLong_AsLong(value));
    else if (closure == ICMP_TS_ORIG)
        self->__icmp.ts.orig = htonl(PyLong_AsLong(value));
    else if (closure == ICMP_TS_RECV)
        self->__icmp.ts.recv = htonl(PyLong_AsLong(value));
    else if (closure == ICMP_TS_TRANS)
        self->__icmp.ts.trans = htonl(PyLong_AsLong(value));

    return 0;
}

static PyObject *icmp_calc_len(icmp *self)
{
    Py_ssize_t len = sizeof(struct icmp_hdr);

    len += self->calc_len(&self->__icmp);
    __ip_calc_len(IP_CAST(self), len);

    Py_RETURN_NONE;
}

u16 __icmp_calc_csum(char *buf, Py_ssize_t buflen,
                     char *data, Py_ssize_t datalen)
{
    int i, sum = 0;

    for (i = 0; i < buflen / 2; i++)
        sum += ((unsigned short *)buf)[i];
    if (data)
        for (i = 0; i < datalen / 2; i++)
            sum += ((unsigned short *)data)[i];
    while (sum >> 16)
        sum = (sum & 0xffff) + (sum >> 16);
    
    return (u16)~sum;
}

static PyObject *icmp_calc_csum(icmp *self)
{
    char *buf;

    buf = (char *)malloc(sizeof(struct icmp_hdr));
    memcpy(buf, &self->__icmp.hdr, sizeof(struct icmp_hdr));
    self->__icmp.hdr.csum = 0;
    self->__icmp.hdr.csum = self->calc_csum(&self->__icmp, buf);
    __ipv4_calc_csum(&IP_CAST(self)->__ipv4);

    free(buf);

    Py_RETURN_NONE;
}

PyObject *create_icmp_instance(int caplen,
                               const unsigned char *pkt)
{
    PyObject *obj, *dgram;
    icmp *self;
    int size = 0;

    obj = icmp_type.tp_new(&icmp_type, NULL, NULL);
    memcpy(&ETHERNET_CAST(obj)->__ethernet, pkt,
           sizeof(struct ethernet));
    size += sizeof(struct ethernet);
    memcpy(&IP_CAST(obj)->__ipv4, (pkt + size),
           sizeof(struct ipv4));
    size += sizeof(struct ipv4);
    IP_CAST(obj)->ip_type = PROTO_IPV4;
    memcpy(&ICMP_CAST(obj)->__icmp.hdr, (pkt + size),
           sizeof(struct icmp_hdr));
    size += sizeof(struct icmp_hdr);
    /*
     * We have now filled the ethernet, ipv4 and icmp
     * headers. The next step is to fill the substructures
     * of the icmp object based on the type field.
     */
    self = ICMP_CAST(obj);
    switch(self->__icmp.hdr.type) {
        case ICMP_DST_UNREACH:
            memcpy(&self->__icmp.dst_unreach, (pkt + size),
                   sizeof(u32));
            size += sizeof(u32);
            if (size < caplen) {
                dgram = PyBytes_FromStringAndSize((pkt + size),
                                                  caplen - size);
                self->__icmp.dst_unreach.datagram = dgram;
            }
            self->calc_len  = calc_len_dst_unreach;
            self->calc_csum = calc_csum_dst_unreach;
            self->to_bytes  = to_bytes_dst_unreach;
        break;
        case ICMP_TIME_EXC:
            memcpy(&self->__icmp.time_exc, (pkt + size),
                   sizeof(u32));
            size += sizeof(u32);
            if (size < caplen) {
                dgram = PyBytes_FromStringAndSize((pkt + size),
                                                  caplen - size);
                self->__icmp.time_exc.datagram = dgram;
            }
            self->calc_len  = calc_len_time_exc;
            self->calc_csum = calc_csum_time_exc;
            self->to_bytes  = to_bytes_time_exc;
        break;
        case ICMP_PARAM_PROB:
            memcpy(&self->__icmp.param_prob, (pkt + size),
                   sizeof(u32));
            size += sizeof(u32);
            if (size < caplen) {
                dgram = PyBytes_FromStringAndSize((pkt + size),
                                                  caplen - size);
                self->__icmp.param_prob.datagram = dgram;
            }
            self->calc_len  = calc_len_param_prob;
            self->calc_csum = calc_csum_param_prob;
            self->to_bytes  = to_bytes_param_prob;
        break;
        case ICMP_REDIRECT:
            memcpy(&self->__icmp.redirect, (pkt + size),
                   sizeof(u32));
            size += sizeof(u32);
            if (size < caplen) {
                dgram = PyBytes_FromStringAndSize((pkt + size),
                                                  caplen - size);
                self->__icmp.redirect.datagram = dgram;
            }
            self->calc_len  = calc_len_redirect;
            self->calc_csum = calc_csum_redirect;
            self->to_bytes  = to_bytes_redirect;
        break;
        case ICMP_ECHO_REQ:
        case ICMP_ECHO_REPLY:
            memcpy(&self->__icmp.echo, (pkt + size),
                   sizeof(u32));
            size += sizeof(u32);
            if (caplen - size >= 8) {
                memcpy(&self->__icmp.echo.ts, (pkt + size),
                       sizeof(u64));
                size += sizeof(u64);
            }
            if (size < caplen) {
                dgram = PyBytes_FromStringAndSize((pkt + size),
                                                  caplen - size);
                self->__icmp.echo.payload = dgram;
            }
            self->calc_len  = calc_len_echo;
            self->calc_csum = calc_csum_echo;
            self->to_bytes  = to_bytes_echo;
        break;
        case ICMP_TS:
        case ICMP_TS_REPLY:
            memcpy(&self->__icmp.ts, (pkt + size),
                   sizeof(struct icmp_ts));
            self->calc_len  = calc_len_ts;
            self->calc_csum = calc_csum_ts;
            self->to_bytes  = to_bytes_ts;
        break;
        default:
#ifdef ICMP_DEBUG
            fprintf(stderr, "icmp error during object parsing"
                    " in create_icmp_instance: icmp type (%d)"
                    " not supported\n", self->__icmp.hdr.type);
#endif
            // Default callbacks to echo.
            self->calc_len  = calc_len_echo;
            self->calc_csum = calc_csum_echo;
            self->to_bytes  = to_bytes_echo;
        break;       
    }
    return obj;
}

static PyObject *icmp_to_bytes(icmp *self)
{
    PyObject *obj;
    Py_ssize_t size;
    int offset = 0;
    char *buf;

    size = sizeof(struct ethernet) + sizeof(struct ipv4) +
           sizeof(struct icmp_hdr);
    buf = (char *)malloc(size);

    memcpy(buf, &ETHERNET_CAST(self)->__ethernet,
           sizeof(struct ethernet));
    offset += sizeof(struct ethernet);
    memcpy((buf + offset), &IP_CAST(self)->__ipv4,
            sizeof(struct ipv4));
    offset += sizeof(struct ipv4);
    memcpy((buf + offset), &self->__icmp.hdr,
            sizeof(struct icmp_hdr));
    /*
     * Delegate the task for generating the rest of the
     * object to the to_bytes pointer field, nested within
     * icmp.
     */
    buf = self->to_bytes(&self->__icmp, buf, &size);
    obj = PyBytes_FromStringAndSize(buf, size);
    free(buf);

    return obj;
}

/*
 * calc_len, calc_csum and to_bytes implementation for
 * Destination Unreachable.
 */
Py_ssize_t calc_len_dst_unreach(struct icmp *__icmp)
{
    Py_ssize_t len;

    len = sizeof(struct icmp_dst_unreach) -
          sizeof(void *);
    if (__icmp->dst_unreach.datagram) {
        len += PyBytes_Size(__icmp->dst_unreach.datagram);
    }
    return len;
}

u16 calc_csum_dst_unreach(struct icmp *__icmp, char *buf)
{
    Py_ssize_t len, dlen = 0;
    char *data = NULL;

    len = sizeof(struct icmp_dst_unreach) -
          sizeof(void *);
    buf = (char *)realloc(buf, sizeof(struct icmp_hdr) +
                          len);
    memcpy((buf + sizeof(struct icmp_hdr)), &__icmp->dst_unreach,
            len);
    len += sizeof(struct icmp_hdr);
    if (__icmp->dst_unreach.datagram) {
        PyBytes_AsStringAndSize(__icmp->dst_unreach.datagram, &data,
                                &dlen);
    }
    return __icmp_calc_csum(buf, len, data, (dlen % 2) ?
                            dlen + 1 : dlen);
}

char *to_bytes_dst_unreach(struct icmp *__icmp, char *buf,
                           Py_ssize_t *size)
{
    Py_ssize_t len, dlen = 0;
    char *dbuf;

    len = sizeof(struct icmp_dst_unreach) - sizeof(void *);
    if (__icmp->dst_unreach.datagram) {
        PyBytes_AsStringAndSize(__icmp->dst_unreach.datagram, &dbuf,
                                &dlen);
    }
    buf = (char *)realloc(buf, *size + len + dlen);
    memcpy((buf + *size), &__icmp->dst_unreach,
            len);
    *size += len;
    if (__icmp->dst_unreach.datagram) {
        memcpy((buf + *size), dbuf, dlen);
        *size += dlen;
    }
    return buf;
}

/*
 * calc_len, calc_csum and to_bytes implementation for
 * Time Exceeded.
 */
Py_ssize_t calc_len_time_exc(struct icmp *__icmp)
{
    Py_ssize_t len;

    len = sizeof(struct icmp_time_exc) -
          sizeof(void *);
    if (__icmp->time_exc.datagram) {
        len += PyBytes_Size(__icmp->time_exc.datagram);
    }
    return len;
}

u16 calc_csum_time_exc(struct icmp *__icmp, char *buf)
{
    Py_ssize_t len, dlen = 0;
    char *data = NULL;

    len = sizeof(struct icmp_time_exc) -
          sizeof(void *);
    buf = (char *)realloc(buf, sizeof(struct icmp_hdr) +
                          len);
    memcpy((buf + sizeof(struct icmp_hdr)), &__icmp->time_exc,
            len);
    len += sizeof(struct icmp_hdr);
    if (__icmp->time_exc.datagram) {
        PyBytes_AsStringAndSize(__icmp->time_exc.datagram, &data,
                                &dlen);
    }
    return __icmp_calc_csum(buf, len, data, (dlen % 2) ?
                            dlen + 1 : dlen);
}

char *to_bytes_time_exc(struct icmp *__icmp, char *buf,
                        Py_ssize_t *size)
{
    Py_ssize_t len, dlen = 0;
    char *dbuf;

    len = sizeof(struct icmp_time_exc) - sizeof(void *);
    if (__icmp->time_exc.datagram) {
        PyBytes_AsStringAndSize(__icmp->time_exc.datagram, &dbuf,
                                &dlen);
    }
    buf = (char *)realloc(buf, *size + len + dlen);
    memcpy((buf + *size), &__icmp->time_exc,
            len);
    *size += len;
    if (__icmp->time_exc.datagram) {
        memcpy((buf + *size), dbuf, dlen);
        *size += dlen;
    }
    return buf;
}

/*
 * calc_len, calc_csum and to_bytes implementation for
 * Parameter Problem.
 */
Py_ssize_t calc_len_param_prob(struct icmp *__icmp)
{
    Py_ssize_t len;

    len = sizeof(struct icmp_param_prob) -
          sizeof(void *);
    if (__icmp->param_prob.datagram) {
        len += PyBytes_Size(__icmp->param_prob.datagram);
    }
    return len;
}

u16 calc_csum_param_prob(struct icmp *__icmp, char *buf)
{
    Py_ssize_t len, dlen = 0;
    char *data = NULL;

    len = sizeof(struct icmp_param_prob) -
          sizeof(void *);
    buf = (char *)realloc(buf, sizeof(struct icmp_hdr) +
                          len);
    memcpy((buf + sizeof(struct icmp_hdr)), &__icmp->param_prob,
            len);
    len += sizeof(struct icmp_hdr);
    if (__icmp->param_prob.datagram) {
        PyBytes_AsStringAndSize(__icmp->param_prob.datagram, &data,
                                &dlen);
    }
    return __icmp_calc_csum(buf, len, data, (dlen % 2) ?
                            dlen + 1 : dlen);
}

char *to_bytes_param_prob(struct icmp *__icmp, char *buf,
                          Py_ssize_t *size)
{
    Py_ssize_t len, dlen = 0;
    char *dbuf;

    len = sizeof(struct icmp_param_prob) - sizeof(void *);
    if (__icmp->param_prob.datagram) {
        PyBytes_AsStringAndSize(__icmp->param_prob.datagram, &dbuf,
                                &dlen);
    }
    buf = (char *)realloc(buf, *size + len + dlen);
    memcpy((buf + *size), &__icmp->param_prob,
            len);
    *size += len;
    if (__icmp->param_prob.datagram) {
        memcpy((buf + *size), dbuf, dlen);
        *size += dlen;
    }
    return buf;
}

/*
 * calc_len, calc_csum and to_bytes implementation for
 * Redirect Message.
 */
Py_ssize_t calc_len_redirect(struct icmp *__icmp)
{
    Py_ssize_t len;

    len = sizeof(struct icmp_redirect) - sizeof(void *);
    if (__icmp->redirect.datagram) {
        len += PyBytes_Size(__icmp->redirect.datagram);
    }
    return len;
}

u16 calc_csum_redirect(struct icmp *__icmp, char *buf)
{
    Py_ssize_t len, dlen = 0;
    char *data = NULL;

    len = sizeof(struct icmp_redirect) -
          sizeof(void *);
    buf = (char *)realloc(buf, sizeof(struct icmp_hdr) +
                          len);
    memcpy((buf + sizeof(struct icmp_hdr)), &__icmp->redirect,
            len);
    len += sizeof(struct icmp_hdr);
    if (__icmp->redirect.datagram) {
        PyBytes_AsStringAndSize(__icmp->redirect.datagram, &data,
                                &dlen);
    }
    return __icmp_calc_csum(buf, len, data, (dlen % 2) ?
                            dlen + 1 : dlen);
}

char *to_bytes_redirect(struct icmp *__icmp, char *buf,
                        Py_ssize_t *size)
{
    Py_ssize_t len, dlen = 0;
    char *dbuf;

    len = sizeof(struct icmp_redirect) - sizeof(void *);
    if (__icmp->redirect.datagram) {
        PyBytes_AsStringAndSize(__icmp->redirect.datagram, &dbuf,
                                &dlen);
    }
    buf = (char *)realloc(buf, *size + len + dlen);
    memcpy((buf + *size), &__icmp->redirect,
            len);
    *size += len;
    if (__icmp->redirect.datagram) {
        memcpy((buf + *size), dbuf, dlen);
        *size += dlen;
    }
    return buf;
}

/*
 * calc_len, calc_csum and to_bytes implementation for
 * Echo/Echo reply message.
 */
Py_ssize_t calc_len_echo(struct icmp *__icmp)
{
    Py_ssize_t len;

    len = sizeof(struct icmp_echo) - sizeof(void *);
    if (!__icmp->echo.ts)
        len -= sizeof(u64);
    if (__icmp->echo.payload)
        len += PyBytes_Size(__icmp->echo.payload);
    
    return len;
}

u16 calc_csum_echo(struct icmp *__icmp, char *buf)
{
    Py_ssize_t len, plen = 0;
    char *data = NULL;

    len = sizeof(struct icmp_echo) - sizeof(void *);
    if (!__icmp->echo.ts)
        len -= sizeof(u64);
    buf = (char *)realloc(buf, sizeof(struct icmp_hdr) + len);
    memcpy((buf + sizeof(struct icmp_hdr)), &__icmp->echo,
            len);
    len += sizeof(struct icmp_hdr);

    if (__icmp->echo.payload) {
        PyBytes_AsStringAndSize(__icmp->echo.payload, &data,
                                &plen);
    }
    return __icmp_calc_csum(buf, len, data, (plen % 2) ?
                            plen + 1 : plen);
}

char *to_bytes_echo(struct icmp *__icmp, char *buf,
                    Py_ssize_t *size)
{
    Py_ssize_t len, plen = 0;
    char *pbuf;

    len = sizeof(struct icmp_echo) - sizeof(void *);
    if (!__icmp->echo.ts)
        len -= sizeof(u64);
    if (__icmp->echo.payload)
        plen = PyBytes_Size(__icmp->echo.payload);
    
    buf = (char *)realloc(buf, *size + len + plen);
    memcpy((buf + *size), &__icmp->echo, len);
    *size += len;
    if (__icmp->echo.payload) {
        PyBytes_AsStringAndSize(__icmp->echo.payload, &pbuf,
                                &plen);
        memcpy((buf + *size), pbuf, plen);
        *size += plen;
    }
    return buf;
}

/*
 * calc_len, calc_csum and to_bytes implementation for
 * Timestamp/Timestamp Reply message.
 */
Py_ssize_t calc_len_ts(struct icmp *__icmp)
{
    return sizeof(struct icmp_ts);
}

u16 calc_csum_ts(struct icmp *__icmp, char *buf)
{
    Py_ssize_t len = sizeof(struct icmp_hdr);

    buf = (char *)realloc(buf, len + 
                          sizeof(struct icmp_ts));
    memcpy((buf + len), &__icmp->ts,
            sizeof(struct icmp_ts));
    len += sizeof(struct icmp_ts);

    return __icmp_calc_csum(buf, len, NULL, 0);
}

char *to_bytes_ts(struct icmp *__icmp, char *buf,
                  Py_ssize_t *size)
{
    buf = (char *)realloc(buf, *size +
                          sizeof(struct icmp_ts));
    memcpy((buf + *size), &__icmp->ts,
            sizeof(struct icmp_ts));
    *size += sizeof(struct icmp_ts);

    return buf;
}

char *icmp_attr_string(void *closure)
{
    if (closure == ICMP_TYPE)
        return "icmp_type";
    if (closure == ICMP_CODE)
        return "icmp_code";
    if (closure == ICMP_CSUM)
        return "icmp_csum";
    if (closure == ICMP_REDIRECT_GW_ADDR)
        return "icmp_redirect_gwaddr";
    if (closure == ICMP_REDIRECT_DGRAM)
        return "icmp_redirect_dgram";
    if (closure == ICMP_ECHO_ID)
        return "icmp_echo_id";
    if (closure == ICMP_ECHO_SEQ)
        return "icmp_echo_seq";
    if (closure == ICMP_ECHO_TS)
        return "icmp_echo_ts";
    if (closure == ICMP_TS_ID)
        return "icmp_ts_id";
    if (closure == ICMP_TS_SEQ)
        return "icmp_ts_seq";
    if (closure == ICMP_TS_ORIG)
        return "icmp_ts_orig";
    if (closure == ICMP_TS_RECV)
        return "icmp_ts_recv";
    if (closure == ICMP_TS_TRANS)
        return "icmp_ts_trans";

    return NULL;      
}

int icmp_add_type(PyObject *module)
{
    icmp_type.tp_base = &ip_type;
    if (PyType_Ready(&icmp_type) < 0)
        return 0;
    Py_INCREF(&icmp_type);
    PyModule_AddObject(module, "icmp", (PyObject *)&icmp_type);

    return 1;
}