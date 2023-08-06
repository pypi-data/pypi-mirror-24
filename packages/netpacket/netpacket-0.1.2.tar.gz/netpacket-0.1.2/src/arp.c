
#include "include/arp.h"

static PyObject *arp_get_attr(arp *self,
                              void *closure);
static int arp_set_attr(arp *self, PyObject *value,
                        void *closure);
static PyObject *arp_get_src_mac(arp *self,
                                 void *closure);
static int arp_set_src_mac(arp *self, PyObject *value,
                           void *closure);
static PyObject *arp_get_src_ip(arp *self,
                                void *closure);
static int arp_set_src_ip(arp *self, PyObject *value,
                          void *closure);
static PyObject *arp_get_dst_mac(arp *self,
                                 void *closure);
static int arp_set_dst_mac(arp *self, PyObject *value,
                           void *closure);
static PyObject *arp_get_dst_ip(arp *self,
                                void *closure);
static int arp_set_dst_ip(arp *self, PyObject *value,
                          void *closure);
static PyObject *arp_to_bytes(arp *self);

static PyMethodDef arp_methods[] = {
    { "to_bytes", (PyCFunction)arp_to_bytes,
       METH_NOARGS, DOCSTR_ARP_TO_BYTES
    },
    { NULL }
};

static PyMemberDef arp_members[] = {
    { "arp_hw_size", T_UBYTE, arp_offset(hw_size),
       0, DOCSTR_ARP_HW_SIZE
    },
    { "arp_proto_size", T_UBYTE, arp_offset(proto_size),
       0, DOCSTR_ARP_PROTO_SIZE
    },
    { NULL }
};

static PyGetSetDef arp_gs[] = {
    { "arp_hw_type", (getter)arp_get_attr,
      (setter)arp_set_attr, DOCSTR_ARP_HW_TYPE,
       ARP_HW_TYPE
    },
    { "arp_proto_type", (getter)arp_get_attr,
      (setter)arp_set_attr, DOCSTR_ARP_PROTO_TYPE,
       ARP_PROTO_TYPE
    },
    { "arp_opcode", (getter)arp_get_attr,
      (setter)arp_set_attr, DOCSTR_ARP_OPCODE,
       ARP_OPCODE
    },
    { "arp_src_mac", (getter)arp_get_src_mac,
      (setter)arp_set_src_mac, DOCSTR_ARP_SRC_MAC,
       NULL
    },
    { "arp_src_ip", (getter)arp_get_src_ip,
      (setter)arp_set_src_ip, DOCSTR_ARP_SRC_IP,
       NULL
    },
    { "arp_dst_mac", (getter)arp_get_dst_mac,
      (setter)arp_set_dst_mac, DOCSTR_ARP_DST_MAC,
       NULL
    },
    { "arp_dst_ip", (getter)arp_get_dst_ip,
      (setter)arp_set_dst_ip, DOCSTR_ARP_DST_IP,
       NULL
    },
    { NULL }
};

PyTypeObject arp_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.arp",          /* tp_name */
    sizeof(arp),               /* tp_basicsize */
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
    arp_methods,               /* tp_methods */
    arp_members,               /* tp_members */
    arp_gs,                    /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

extern PyTypeObject ethernet_type;

static PyObject *arp_get_attr(arp *self,
                              void *closure)
{
    if (closure == ARP_HW_TYPE)
        return PyLong_FromLong(ntohs(self->__arp.hw_type));
    if (closure == ARP_PROTO_TYPE)
        return PyLong_FromLong(ntohs(self->__arp.proto_type));
    if (closure == ARP_OPCODE)
        return PyLong_FromLong(ntohs(self->__arp.opcode));

    Py_RETURN_NONE;
}

static int arp_set_attr(arp *self,
                        PyObject *value,
                        void *closure)
{
    if (!value) {
        PyErr_Format(PyExc_AttributeError, "attribute '%s' can not"
                     " be deleted", arp_attr_string(closure));
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_Format(PyExc_TypeError, "attribute '%s' expects"
                     " a type of 'int'", arp_attr_string(closure));
        return -1;
    }
    if (closure == ARP_HW_TYPE)
        self->__arp.hw_type = htons(PyLong_AsLong(value));
    else if (closure == ARP_PROTO_TYPE)
        self->__arp.proto_type = htons(PyLong_AsLong(value));
    else if (closure == ARP_OPCODE)
        self->__arp.opcode = htons(PyLong_AsLong(value));

    return 0;
}

static PyObject *arp_get_src_ip(arp *self, void *closure)
{
    return __ipv4_get_addr(self->__arp.src_ip);
}

static PyObject *arp_get_dst_ip(arp *self, void *closure)
{
    return __ipv4_get_addr(self->__arp.dst_ip);
}

static int arp_set_src_ip(arp *self, PyObject *value,
                          void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'arp_src_ip' "
                        "can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'arp_src_ip' expects "
                        "type 'bytes'");
        return -1;
    }
    return __ipv4_set_addr(value, &self->__arp.src_ip);
}

static int arp_set_dst_ip(arp *self, PyObject *value,
                          void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'arp_dst_ip' "
                        "can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'arp_dst_ip' expects "
                        "type 'bytes'");
        return -1;
    }
    return __ipv4_set_addr(value, &self->__arp.dst_ip);
}

static PyObject *arp_get_src_mac(arp *self, void *closure)
{
    return __get_mac_address(self->__arp.src_mac);
}

static PyObject *arp_get_dst_mac(arp *self, void *closure)
{
    return __get_mac_address(self->__arp.dst_mac);
}

static int arp_set_src_mac(arp *self, PyObject *value,
                           void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'arp_src_mac' "
                        "can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'arp_src_mac' "
                        "must be of type 'bytes'");
        return -1;
    }
    return __set_mac_address(self->__arp.src_mac, value);
}

static int arp_set_dst_mac(arp *self, PyObject *value,
                           void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'arp_dst_mac' "
                        "can not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'arp_dst_mac' "
                        "must be of type 'bytes'");
        return -1;
    }
    return __set_mac_address(self->__arp.dst_mac, value);
}

int arp_add_type(PyObject *module)
{
    arp_type.tp_base = &ethernet_type;
    if (PyType_Ready(&arp_type) < 0)
        return 0;
    Py_INCREF(&arp_type);
    PyModule_AddObject(module, "arp", (PyObject *)&arp_type);

    return 1;
}

PyObject *create_arp_instance(int caplen,
                              const unsigned char *pkt)
{
    PyObject *obj;

    obj = arp_type.tp_new(&arp_type, NULL, NULL);
    memcpy(&ETHERNET_CAST(obj)->__ethernet, pkt,
           sizeof(struct ethernet));
    memcpy(&ARP_CAST(obj)->__arp,
           (pkt + sizeof(struct ethernet)),
            sizeof(struct arp));
    return obj; 
}

static PyObject *arp_to_bytes(arp *self)
{
    PyObject *obj;
    int size;
    char *buf;

    size = sizeof(struct ethernet) + sizeof(struct arp);
    buf = (char *)malloc(size);

    memcpy(buf, &ETHERNET_CAST(self)->__ethernet,
           sizeof(struct ethernet));
    memcpy((buf + sizeof(struct ethernet)),
           &self->__arp,
           sizeof(struct arp));
    obj = PyBytes_FromStringAndSize(buf, size);
    free(buf);
    
    return obj;
}

char *arp_attr_string(void *closure)
{
    if (closure == ARP_HW_TYPE)
        return "arp_hw_type";
    if (closure == ARP_PROTO_TYPE)
        return "arp_proto_type";
    if (closure == ARP_OPCODE)
        return "arp_opcode";

    return NULL;
}