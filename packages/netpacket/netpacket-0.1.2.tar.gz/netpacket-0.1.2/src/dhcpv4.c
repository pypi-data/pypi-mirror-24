
#include "include/dhcpv4.h"

static int dhcp_init(dhcp *self, PyObject *value,
                     PyObject *kwds);
static PyObject *dhcp_get_attr(dhcp *self, void *closure);
static int dhcp_set_attr(dhcp *self, PyObject *value,
                         void *closure);
static int dhcp_set_ip(dhcp *self, PyObject *value,
                       void *closure);
static int dhcp_set_chaddr(dhcp *self, PyObject *value,
                           void *closure);
static int dhcp_set_sname_file(dhcp *self, PyObject *value,
                               void *closure);
static PyObject *dhcp_get_opt(dhcp *self, PyObject *args);
static PyObject *dhcp_set_opt(dhcp *self, PyObject *args);
static PyObject *dhcp_get_opts(dhcp *self, PyObject *args);
static PyObject *dhcp_to_bytes(dhcp *self);

static PyMethodDef dhcp_methods[] = {
    { "get_opt", (PyCFunction)dhcp_get_opt,
       METH_VARARGS, DOCSTR_DHCP_GET_OPT
    },
    { "set_opt", (PyCFunction)dhcp_set_opt,
       METH_VARARGS, DOCSTR_DHCP_SET_OPT
    },
    { "get_opts", (PyCFunction)dhcp_get_opts,
       METH_VARARGS, DOCSTR_DHCP_GET_OPTS,
    },
    { "to_bytes", (PyCFunction)dhcp_to_bytes,
       METH_NOARGS, DOCSTR_DHCP_TO_BYTES
    },
    { NULL }
};

static PyGetSetDef dhcp_gs[] = {
    { "op", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_GET_OPT,
       DHCP_OP
    },
    { "htype", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_HTYPE,
       DHCP_HTYPE
    },
    { "hlen", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_HLEN,
       DHCP_HLEN
    },
    { "hops", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_HOPS,
       DHCP_HOPS
    },
    { "xid", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_XID,
       DHCP_XID
    },
    { "secs", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_SECS,
       DHCP_SECS
    },
    { "flags", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_FLAGS,
       DHCP_FLAGS
    },
    { "ciaddr", (getter)dhcp_get_attr,
      (setter)dhcp_set_ip, DOCSTR_DHCP_CIADDR,
       DHCP_CIADDR
    },
    { "yiaddr", (getter)dhcp_get_attr,
      (setter)dhcp_set_ip, DOCSTR_DHCP_YIADDR,
       DHCP_YIADDR
    },
    { "siaddr", (getter)dhcp_get_attr,
      (setter)dhcp_set_ip, DOCSTR_DHCP_SIADDR,
       DHCP_SIADDR
    },
    { "giaddr", (getter)dhcp_get_attr,
      (setter)dhcp_set_ip, DOCSTR_DHCP_GIADDR,
       DHCP_GIADDR
    },
    { "chaddr", (getter)dhcp_get_attr,
      (setter)dhcp_set_chaddr, DOCSTR_DHCP_CHADDR,
       DHCP_CHADDR
    },
    { "sname", (getter)dhcp_get_attr,
      (setter)dhcp_set_sname_file, DOCSTR_DHCP_SNAME,
       DHCP_SNAME
    },
    { "file", (getter)dhcp_get_attr,
      (setter)dhcp_set_sname_file, DOCSTR_DHCP_FILE,
       DHCP_FILE
    },
    { "cookie", (getter)dhcp_get_attr,
      (setter)dhcp_set_attr, DOCSTR_DHCP_COOKIE,
       DHCP_COOKIE
    },
    { NULL }
};

PyTypeObject dhcp_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.dhcpv4",       /* tp_name */
    sizeof(dhcp),              /* tp_basicsize */
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
    dhcp_methods,              /* tp_methods */
    0,                         /* tp_members */
    dhcp_gs,                   /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)dhcp_init,       /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

extern PyTypeObject packet_type;

static int dhcp_init(dhcp *self, PyObject *args,
                     PyObject *kwds)
{
    PyObject *obj = NULL;
    Py_ssize_t size;
    int max_size;
    char *buf;

    if (!PyArg_ParseTuple(args, "O", &obj))
        return -1;
    if (PyBytes_AsStringAndSize(obj, &buf, &size) == -1)
        return -1;
    if (size < DHCP_STATIC_LEN) {
        PyErr_Format(PyExc_ValueError, "byte object passed is"
                     " missing length. Minimum (%d), got (%d)",
                     DHCP_STATIC_LEN, size);
        return -1;
    }
    max_size = DHCP_STATIC_LEN + MAX_OPTLEN;
    if (size > max_size)
        size = max_size;
    memcpy(&self->__dhcp, buf, size);
    
    return 0;
}

static PyObject *dhcp_get_attr(dhcp *self, void *closure)
{
    if (closure == DHCP_OP)
        return PyLong_FromLong(self->__dhcp.op);
    if (closure == DHCP_HTYPE)
        return PyLong_FromLong(self->__dhcp.htype);
    if (closure == DHCP_HLEN)
        return PyLong_FromLong(self->__dhcp.hlen);
    if (closure == DHCP_HOPS)
        return PyLong_FromLong(self->__dhcp.hops);
    if (closure == DHCP_XID)
        return PyLong_FromLong(ntohl(self->__dhcp.xid));
    if (closure == DHCP_SECS)
        return PyLong_FromLong(ntohs(self->__dhcp.secs));
    if (closure == DHCP_FLAGS)
        return PyLong_FromLong(ntohs(self->__dhcp.flags));
    if (closure == DHCP_CHADDR)
        return __get_mac_address(self->__dhcp.chaddr);
    if (closure == DHCP_CIADDR)
        return __ipv4_get_addr(self->__dhcp.ciaddr);
    if (closure == DHCP_YIADDR)
        return __ipv4_get_addr(self->__dhcp.yiaddr);
    if (closure == DHCP_SIADDR)
        return __ipv4_get_addr(self->__dhcp.siaddr);
    if (closure == DHCP_GIADDR)
        return __ipv4_get_addr(self->__dhcp.giaddr);
    if (closure == DHCP_SNAME)
        return PyBytes_FromString(self->__dhcp.sname);
    if (closure == DHCP_FILE)
        return PyBytes_FromString(self->__dhcp.file);
    if (closure == DHCP_COOKIE)
        return PyLong_FromLong(ntohl(self->__dhcp.cookie));

    Py_RETURN_NONE;
}

static int dhcp_set_attr(dhcp *self, PyObject *value,
                         void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can"
                     " not be deleted", dhcp_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'int'", dhcp_attr_string(closure));
        return -1;
    }
    if (closure == DHCP_OP)
        self->__dhcp.op = PyLong_AsLong(value);
    else if (closure == DHCP_HTYPE)
        self->__dhcp.htype = PyLong_AsLong(value);
    else if (closure == DHCP_HLEN)
        self->__dhcp.hlen = PyLong_AsLong(value);
    else if (closure == DHCP_HOPS)
        self->__dhcp.hops = PyLong_AsLong(value);
    else if (closure == DHCP_XID)
        self->__dhcp.xid = htonl(PyLong_AsLong(value));
    else if (closure == DHCP_SECS)
        self->__dhcp.secs = htons(PyLong_AsLong(value));
    else if (closure == DHCP_FLAGS)
        self->__dhcp.flags = htons(PyLong_AsLong(value));
    else if (closure == DHCP_COOKIE)
        self->__dhcp.cookie = htonl(PyLong_AsLong(value));
    return 0;
}

static int dhcp_set_ip(dhcp *self, PyObject *value,
                       void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can"
                     " can not be deleted", dhcp_attr_string(closure));
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'bytes'", dhcp_attr_string(closure));
        return -1;
    }
    if (closure == DHCP_CIADDR)
        return __ipv4_set_addr(value, &self->__dhcp.ciaddr);
    if (closure == DHCP_YIADDR)
        return __ipv4_set_addr(value, &self->__dhcp.yiaddr);
    if (closure == DHCP_SIADDR)
        return __ipv4_set_addr(value, &self->__dhcp.siaddr);
    if (closure == DHCP_GIADDR)
        return __ipv4_set_addr(value, &self->__dhcp.giaddr);

    return -1;
}

static int dhcp_set_chaddr(dhcp *self, PyObject *value,
                           void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'chaddr'"
                        " can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'chaddr' only"
                        " accepts a type of 'bytes'");
        return -1;
    }
    __set_mac_address(self->__dhcp.chaddr, value);

    return 0;
}

static int dhcp_set_sname_file(dhcp *self, PyObject *value,
                               void *closure)
{
    char *buf;
    Py_ssize_t size;

    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can"
                     " can not be deleted", dhcp_attr_string(closure));
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' only accepts"
                     " a type of 'bytes'", dhcp_attr_string(closure));
        return -1;
    }
    if (PyBytes_AsStringAndSize(value, &buf, &size) == -1)
        return -1;
    if (closure == DHCP_SNAME) {
        if (size > 64)
            size = 64;
        memcpy(self->__dhcp.sname, buf, size);
    }
    else if (closure == DHCP_FILE) {
        if (size > 128)
            size = 128;
        memcpy(self->__dhcp.file, buf, size);
    }
    return 0;
}

static int __set_opt(u8 *segment, u32 seg_size, u32 *seg_off,
                     u32 code, u32 len, void *data)
{
    int req_size;

    if (is_singular_opt(code))
        req_size = 1;
    else
        req_size = len + 2;
    if (*seg_off + req_size > seg_size) {
        PyErr_SetString(PyExc_ValueError,
                        "maximum option length exceeded");
        return -1;
    }
    segment[(*seg_off)++] = code;
    if (data) {
        segment[(*seg_off)++] = len;
        memcpy((segment + *seg_off), data, len);
        *seg_off += len;
    }
    return 0;
}

static int set_opt(dhcp *self, u32 code, u32 len,
                   void *data)
{
    switch(self->segment) {
        case DHCP_SEG_OPTS:
            return __set_opt(self->__dhcp.opts, MAX_OPTLEN,
                             &self->opt_offset, code, len,
                             data);
        break;
        case DHCP_SEG_SNAME:
            return __set_opt(self->__dhcp.sname, 64,
                             &self->sname_offset, code, len,
                             data);
        break;
        case DHCP_SEG_SFILE:
            return __set_opt(self->__dhcp.file, 128,
                             &self->sfile_offset, code, len,
                             data);
        break;
    }
    return -1;
}

static int set_opt_u8(dhcp *self, u32 code,
                      PyObject *data)
{
    u8 value;

    if (!PyLong_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'int' for the data", code);
        return -1;
    }
    value = PyLong_AsLong(data);
    return set_opt(self, code, 1, &value);
}

static int set_opt_u16(dhcp *self, u32 code,
                       PyObject *data)
{
    u16 value;

    if (!PyLong_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'int' for the data", code);
        return -1;
    }
    value = htons(PyLong_AsLong(data));
    return set_opt(self, code, 2, &value);
}

static int set_opt_s32(dhcp *self, u32 code,
                       PyObject *data)
{
    s32 value;

    if (!PyLong_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'int' for the data", code);
        return -1;
    }
    value = htonl(PyLong_AsLong(data));
    return set_opt(self, code, 4, &value);
}

static int set_opt_u32(dhcp *self, u32 code,
                       PyObject *data)
{
    u32 value;

    if (!PyLong_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'int' for the data", code);
        return -1;
    }
    value = htonl(PyLong_AsLong(data));
    return set_opt(self, code, 4, &value);
}

static int set_opt_addr(dhcp *self, u32 code,
                        PyObject *data)
{
    u32 addr;

    if (!PyBytes_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'bytes' for the data", code);
        return -1;
    }
    if (__ipv4_set_addr(data, &addr) == -1)
        return -1;
    return set_opt(self, code, 4, &addr);
}

static int set_opt_bytes(dhcp *self, u32 code,
                         PyObject *data)
{
    char *buf;
    Py_ssize_t len;

    if (!PyBytes_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'bytes' for the data", code);
        return 1;
    }
    if (PyBytes_AsStringAndSize(data, &buf, &len) == -1)
        return -1;
    return set_opt(self, code, len, buf);
}

static int set_opt_param_reqlist(dhcp *self, u32 code,
                                 PyObject *data)
{
    s32 i, retval;
    Py_ssize_t size;
    DHCP_OPTBUF *obuf;
    PyObject *item;

    if (!PyTuple_Check(data)) {
        PyErr_SetString(PyExc_TypeError, "code '55' expects"
                        " type 'tuple' for the data");
        return -1;
    }
    size = PyTuple_GET_SIZE(data);
    obuf = (DHCP_OPTBUF *)malloc(size);
    for (i = 0; i < size; i++) {
        item = PyTuple_GET_ITEM(data, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "tuple items must"
                            " be of type 'int'");
            free(obuf);
            return -1;
        }
        obuf[i] = PyLong_AsLong(item);
    }
    retval = set_opt(self, code, size, obuf);
    free(obuf);

    return retval;
}

/*
 * This subroutine is used to handle a sequence
 * of ipv4 addresses. It is used as a generic
 * dispatcher for allot of the Vendor extensions.
 */
static int set_opt_seq_addr(dhcp *self, u32 code,
                            PyObject *data)
{
    s32 i, retval;
    Py_ssize_t size;
    DHCP_OPTBUF *obuf;
    PyObject *item;

    if (!PyTuple_Check(data)) {
        PyErr_Format(PyExc_TypeError, "code '%d' expects"
                     " type 'tuple' for the data", code);
        return -1;
    }
    size = PyTuple_GET_SIZE(data);
    obuf = (DHCP_OPTBUF *)malloc(sizeof(u32) * size);
    for (i = 0; i < size; i++) {
        item = PyTuple_GET_ITEM(data, i);
        if (!PyBytes_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "tuple items must"
                            " be of type 'bytes'");
            free(obuf);
            return -1;
        }
        if (__ipv4_set_addr(item, (u32 *)(obuf + i * sizeof(u32))) == -1) {
            free(obuf);
            return -1;
        }
    }
    retval = set_opt(self, code, size * sizeof(u32), obuf);
    free(obuf);

    return retval;
}

static int set_opt_path_mtu_tbl(dhcp *self, u32 code,
                                PyObject *data)
{
    s32 i, retval;
    Py_ssize_t size;
    DHCP_OPTBUF *obuf;
    PyObject *item;
    u16 value;

    if (!PyTuple_Check(data)) {
        PyErr_SetString(PyExc_TypeError, "code '55' expects"
                        " type 'tuple' for the data");
        return -1;
    }
    size = PyTuple_GET_SIZE(data);
    obuf = (DHCP_OPTBUF *)malloc(sizeof(u16) * size);
    for (i = 0; i < size; i++) {
        item = PyTuple_GET_ITEM(data, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "tuple items must"
                            " be of type 'int'");
            free(obuf);
            return -1;
        }
        value = htons(PyLong_AsLong(item));
        memcpy((obuf + i * sizeof(u16)), &value, sizeof(u16));
    }
    retval = set_opt(self, code, sizeof(u16) * size,
                     obuf);
    free(obuf);
    return retval;
}

/*
 * The main subroutine for setting options. The arguments
 * are: one int that specifies the optcode, one int that
 * specifies the optlen, and the data conforming to the
 * option in question.
 */
static PyObject *dhcp_set_opt(dhcp *self, PyObject *args)
{
    u32 code, retval;
    PyObject *data;

    if (!PyArg_ParseTuple(args, "IO|I", &code, &data,
                          &self->segment))
        return NULL;

    if (self->segment < 0 || self->segment > DHCP_SEG_SFILE) {
        PyErr_Format(PyExc_ValueError, "invalid segment type"
                     " (%d)", self->segment);
        return NULL;
    }
    switch(code) {
        case DHCP_OPT_REQADDR:
            retval = set_opt_addr(self, code, data);
        break;
        case DHCP_OPT_LEASE_TIME:
            retval = set_opt_u32(self, code, data);
        break;
        case DHCP_OPT_OVERLOAD:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_TFTP_SNAME:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_BOOTF_NAME:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_MSG_TYPE:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_SRV_IDENT:
            retval = set_opt_addr(self, code, data);
        break;
        case DHCP_OPT_PARAM_REQLIST:
            retval = set_opt_param_reqlist(self, code, data);
        break;
        case DHCP_OPT_MSG:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_MAX_MSG_SIZE:
            retval = set_opt_u16(self, code, data);
        break;
        case DHCP_OPT_RENEWAL_TIME:
            retval = set_opt_u32(self, code, data);
        break;
        case DHCP_OPT_REBINDING_TIME:
            retval = set_opt_u32(self, code, data);
        break;
        case DHCP_OPT_VENDOR_CLASS:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_PAD:
            retval = set_opt(self, code, 0, NULL);
        break;
        case DHCP_OPT_END:
            retval = set_opt(self, code, 0, NULL);
        break;
        case DHCP_OPT_SUBNET_MASK:
            retval = set_opt_addr(self, code, data);
        break;
        case DHCP_OPT_TIME_OFFSET:
            retval = set_opt_s32(self, code, data);
        break;
        case DHCP_OPT_ROUTER:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_TIME_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_NAME_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_DNS:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_LOG_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_COOKIE_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_LPR_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_IMPRESS_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_RES_LOC_SRV:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_HOST_NAME:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_BOOT_FILE_SIZ:
            retval = set_opt_u16(self, code, data);
        break;
        case DHCP_OPT_MERIT_DUMP:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_DOMAIN_NAME:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_SWAP_SRV:
            retval = set_opt_addr(self, code, data);
        break;
        case DHCP_OPT_ROOT_PATH:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_EXTS_PATH:
            retval = set_opt_bytes(self, code, data);
        break;
        case DHCP_OPT_IP_FORWARDING:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_NLSR:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_MAX_DGRAM_SIZ:
            retval = set_opt_u16(self, code, data);
        break;
        case DHCP_OPT_DEFAULT_IP_TTL:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_PATH_MTU:
            retval = set_opt_u32(self, code, data);
        break;
        case DHCP_OPT_PATH_MTU_TBL:
            retval = set_opt_path_mtu_tbl(self, code, data);
        break;
        case DHCP_OPT_INTERFACE_MTU:
            retval = set_opt_u16(self, code, data);
        break;
        case DHCP_OPT_ALL_SUBNETS:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_BRD_ADDR:
            retval = set_opt_addr(self, code, data);
        break;
        case DHCP_OPT_PERF_MASK_DISC:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_MASK_SUPPLIER:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_ROUTER_DISC:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_ROUTER_SOLIC:
            retval = set_opt_addr(self, code, data);
        break;
        /*
         * This option takes a endpoint-router pair, and
         * as of now it calls into set_opt_seq_addr. This
         * might be a bit misleading and error prone, since
         * the logical thing would be to parse a sequence of
         * tuple objects containing endpoint-router byte
         * objects. Just keep in mind to pass the router address
         * after the endpoint address from Python.
         */
        case DHCP_OPT_STATIC_ROUTE:
            retval = set_opt_seq_addr(self, code, data);
        break;
        case DHCP_OPT_TRAILER_ENCAP:
            retval = set_opt_u8(self, code, data);
        break;
        case DHCP_OPT_ARP_CACHE_TOUT:
            retval = set_opt_u32(self, code, data);
        break;
        case DHCP_OPT_ETHERNET_ENCAP:
            retval = set_opt_u8(self, code, data);
        break;
        default:
            PyErr_Format(PyExc_ValueError, "code '%d' is not"
                         " recognized as a valid option", code);
            retval = -1;
        break;
    }
    if (retval == 0) {
        Py_RETURN_NONE;
    }
    return NULL;
}

/*
 * get_opt searches through the opts, sname and file segment
 * for options. If it finds the option in question but
 * the option is bogus (i.e, the bytes are missing), it
 * returns Py_RETURN_NONE.

 * Since DHCP responses are mostly used to configure net
 * interfaces, the returned data is still in its original
 * big-endian format. Its up to the programmer to change
 * the endian from Python before configurating an interface
 * with the data.
 */
static PyObject *get_opt(u32 code, u8 *segment, u32 size)
{
    u32 pos;
    u8 len;
    PyObject *obj;

    for (pos = 0; pos < size;) {
        if (is_singular_opt(code)) {
            if (segment[pos] == code) {
                return PyBytes_FromString("");
            }
            pos++; continue;
        }
        else {
            if (pos + 1 >= size) 
                goto bogus_opt;
            len = segment[pos + 1];
        }
        if (segment[pos] == code) {
            pos += 2;
            if (pos + len >= size)
                goto bogus_opt;
            return PyBytes_FromStringAndSize((segment + pos), len);
        }
        pos += 2 + len;
    }
    Py_RETURN_NONE;
bogus_opt:
#ifdef DHCP_DEBUG
    fprintf(stderr, "DHCP option data is missing, or"
            " is exceeding the length of the option segment"
            " for code (%d)\n", code);
#endif
    Py_RETURN_NONE;
}

static PyObject *dhcp_get_opt(dhcp *self, PyObject *args)
{
    u32 code, segment = DHCP_SEG_OPTS;

    if (!PyArg_ParseTuple(args, "I|I", &code, &segment))
        return NULL;
    switch(segment) {
        case DHCP_SEG_OPTS:
            return get_opt(code, self->__dhcp.opts,
                           MAX_OPTLEN);
        break;
        case DHCP_SEG_SNAME:
            return get_opt(code, self->__dhcp.sname, 64);
        break;
        case DHCP_SEG_SFILE:
            return get_opt(code, self->__dhcp.file, 128);
        break;
        default:
            PyErr_Format(PyExc_ValueError, "invalid segment type"
                         " (%d)", segment);
            return NULL;
        break;
    }
}

static PyObject *dhcp_get_opts(dhcp *self, PyObject *args)
{
    u32 segment = DHCP_SEG_OPTS;

    if (!PyArg_ParseTuple(args, "|I", &segment))
        return NULL;
    if (segment == DHCP_SEG_OPTS)
        return PyBytes_FromStringAndSize(self->__dhcp.opts,
                                         self->opt_offset);
    if (segment == DHCP_SEG_SNAME)
        return PyBytes_FromStringAndSize(self->__dhcp.sname,
                                         self->sname_offset);
    if (segment == DHCP_SEG_SFILE)
        return PyBytes_FromStringAndSize(self->__dhcp.file,
                                         self->sfile_offset);
    PyErr_Format(PyExc_ValueError, "invalid segment type",
                 " (%d)", segment);
    return NULL;
}

static PyObject *dhcp_to_bytes(dhcp *self)
{
    PyObject *obj;
    Py_ssize_t size;
    Py_ssize_t offset = 0;
    char *buf;

    size = DHCP_STATIC_LEN;
    if (self->opt_offset)
        size += self->opt_offset;
    buf = (char *)malloc(size);
    
    memcpy(buf, &self->__dhcp, DHCP_STATIC_LEN);
    offset += DHCP_STATIC_LEN;
    if (self->opt_offset) {
        memcpy((buf + offset), self->__dhcp.opts,
                self->opt_offset);
        offset += self->opt_offset;
    }
    obj = PyBytes_FromStringAndSize(buf, size);
    free(buf);
    return obj;
}

int dhcp_add_type(PyObject *module)
{
    dhcp_type.tp_base = &packet_type;
    if (PyType_Ready(&dhcp_type) < 0)
        return 0;
    Py_INCREF(&dhcp_type);
    PyModule_AddObject(module, "dhcpv4", (PyObject *)&dhcp_type);
    
    return 1;
}

char *dhcp_attr_string(void *closure)
{
    if (closure == DHCP_OP)
        return "op";
    if (closure == DHCP_HTYPE)
        return "htype";
    if (closure == DHCP_HLEN)
        return "hlen";
    if (closure == DHCP_HOPS)
        return "hops";
    if (closure == DHCP_XID)
        return "xid";
    if (closure == DHCP_SECS)
        return "secs";
    if (closure == DHCP_FLAGS)
        return "flags";
    if (closure == DHCP_CIADDR)
        return "ciaddr";
    if (closure == DHCP_YIADDR)
        return "yiaddr";
    if (closure == DHCP_SIADDR)
        return "siaddr";
    if (closure == DHCP_GIADDR)
        return "giaddr";
    if (closure == DHCP_SNAME)
        return "sname";
    if (closure == DHCP_FILE)
        return "file";

    return NULL;
}