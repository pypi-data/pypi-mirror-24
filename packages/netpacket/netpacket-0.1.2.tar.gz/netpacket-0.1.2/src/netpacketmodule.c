
#include "include/packetmodule.h"

static PyModuleDef netpacket_module = {
    PyModuleDef_HEAD_INIT,
    "_netpacket", NULL,
    -1,
    NULL, NULL, NULL, NULL,
    NULL
};

PyObject *PyExc_Ppcap;

PyMODINIT_FUNC PyInit__netpacket(void)
{
    PyObject *module;

    module = PyModule_Create(&netpacket_module);
    if (!module)
        return NULL;
    if (!ppcap_add_type(module))
        return NULL;
    if (!packet_add_type(module))
        return NULL;
    if (!ethernet_add_type(module))
        return NULL;
    if (!arp_add_type(module))
        return NULL;
    if (!ip_add_type(module))
        return NULL;
    if (!icmp_add_type(module))
        return NULL;
    if (!tcp_add_type(module))
        return NULL;
    if (!udp_add_type(module))
        return NULL;
    if (!dhcp_add_type(module))
        return NULL;
    /*
     * Create the Ppcap exception.
     */
    PyExc_Ppcap = PyErr_NewException("netpacket.PpcapException", NULL,
                                     NULL);
    
    return module;
}
