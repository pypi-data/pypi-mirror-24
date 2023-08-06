
#include "include/ethernet.h"

static PyObject *ethernet_get_dst(ethernet *self,
                                  void *closure);
static int ethernet_set_dst(ethernet *self,
                            PyObject *value,
                            void *closure);
static PyObject *ethernet_get_src(ethernet *self,
                                  void *closure);
static int ethernet_set_src(ethernet *self,
                            PyObject *value,
                            void *closure);
static PyObject *ethernet_get_type(ethernet *self,
                                   void *closure);
static int ethernet_set_type(ethernet *self,
                             PyObject *value,
                             void *closure);
static PyObject *ethernet_to_bytes(ethernet *self);

static PyMethodDef ethernet_methods[] = {
    { "to_bytes", (PyCFunction)ethernet_to_bytes,
       METH_NOARGS, DOCSTR_ETHERNET_TO_BYTES
    },
    { NULL }
};

static PyGetSetDef ethernet_gs[] = {
    { "ether_dst", (getter)ethernet_get_dst,
      (setter)ethernet_set_dst, DOCSTR_ETHERNET_DST,
       NULL
    },
    { "ether_src", (getter)ethernet_get_src,
      (setter)ethernet_set_src, DOCSTR_ETHERNET_SRC,
       NULL
    },
    { "ether_type", (getter)ethernet_get_type,
      (setter)ethernet_set_type, DOCSTR_ETHERNET_TYPE,
       NULL
    },
    { NULL }
};

PyTypeObject ethernet_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_netpacket.ethernet",     /* tp_name */
    sizeof(ethernet),          /* tp_basicsize */
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
    ethernet_methods,          /* tp_methods */
    0,                         /* tp_members */
    ethernet_gs,               /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

extern PyTypeObject packet_type;

static PyObject *ethernet_get_dst(ethernet *self,
                                  void *closure)
{
    return __get_mac_address(self->__ethernet.dst);
}

static PyObject *ethernet_get_src(ethernet *self,
                                  void *closure)
{
    return __get_mac_address(self->__ethernet.src);
}

static int ethernet_set_dst(ethernet *self,
                            PyObject *value,
                            void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'ether_dst' can"
                        " not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'ether_dst' expects"
                        " type 'bytes'");
        return -1;
    }
    return __set_mac_address(self->__ethernet.dst, value);
}

static int ethernet_set_src(ethernet *self,
                            PyObject *value,
                            void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'ether_src' can"
                        " not be deleted");
        return -1;
    }
    if (!PyBytes_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'ether_src' expects"
                        " type 'bytes'");
        return -1;
    }
    return __set_mac_address(self->__ethernet.src, value);
}

static PyObject *ethernet_get_type(ethernet *self,
                                   void *closure)
{
    return PyLong_FromLong(ntohs(self->__ethernet.type));
}

static int ethernet_set_type(ethernet *self,
                             PyObject *value,
                             void *closure)
{
    if (!value) {
        PyErr_SetString(PyExc_AttributeError, "attribute 'ether_type'"
                        " can not be deleted");
        return -1;
    }
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "attribute 'ether_type' expects"
                        " type 'int'");
        return -1;
    }
    self->__ethernet.type = htons(PyLong_AsLong(value));

    return 0;
}

int ethernet_add_type(PyObject *module)
{
    ethernet_type.tp_base = &packet_type;
    if (PyType_Ready(&ethernet_type) < 0)
        return 0;
    Py_INCREF(&ethernet_type);
    PyModule_AddObject(module, "ethernet", (PyObject *)&ethernet_type);

    return 1;
}

PyObject *create_ethernet_instance(int caplen,
                                   const unsigned char *pkt)
{
    PyObject *obj;

    obj = ethernet_type.tp_new(&ethernet_type, NULL, NULL);
    memcpy(&ETHERNET_CAST(obj)->__ethernet, pkt,
           sizeof(struct ethernet));
    return obj;
}

static PyObject *ethernet_to_bytes(ethernet *self)
{
    PyObject *obj;
    int size;
    char *buf;

    size = sizeof(struct ethernet);
    buf = (char *)malloc(size);

    memcpy(buf, &self->__ethernet, size);
    obj = PyBytes_FromStringAndSize(buf, size);
    free(buf);

    return obj;
}