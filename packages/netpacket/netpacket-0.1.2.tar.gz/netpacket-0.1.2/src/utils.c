
/*
 * Some routines are not type-based, like
 * calculating the IP address refers to more
 * data types than just IP. Instead of duplicating
 * the definition of these routines in more than one
 * file, they are defined here.
 */
#include "include/utils.h"

PyObject *__get_mac_address(u8 *mac)
{
    char buf[1024];

    snprintf(buf, 1023, "%02x:%02x:%02x:%02x:%02x:%02x",
             mac[0], mac[1], mac[2], mac[3],
             mac[4], mac[5]);
    return PyUnicode_FromStringAndSize(buf, strlen(buf));
}

int __set_mac_address(u8 *mac, PyObject *value)
{
    char buf[PyBytes_GET_SIZE(value) + 1], *p;
    int i;

    memcpy(buf, PyBytes_AsString(value),
           PyBytes_GET_SIZE(value) + 1);
    p = strtok(buf, ":");
    if (p) {
        mac[0] = strtoul(p, NULL, 16);
        for (i = 1; i < 6 && (p = strtok(NULL, ":")); i++)
            mac[i] = strtoul(p, NULL, 16);
    }
    return 0;
}

PyObject *__ipv4_get_addr(u32 addr)
{
    char buf[INET_ADDRSTRLEN + 1];
    struct in_addr in;

    memcpy(&in, &addr, sizeof(struct in_addr));
    if (!inet_ntop(AF_INET, &in, buf, INET_ADDRSTRLEN)) {
        PyErr_Format(PyExc_Exception, "%s", strerror(errno));
        return NULL;
    }
    return PyUnicode_FromStringAndSize(buf, strlen(buf));
}

PyObject *__ipv6_get_addr(u8 *addr)
{
    char buf[INET6_ADDRSTRLEN + 1];
    struct in6_addr in;

    memcpy(&in, addr, sizeof(struct in6_addr));
    if (!inet_ntop(AF_INET6, &in, buf, INET6_ADDRSTRLEN)) {
        PyErr_Format(PyExc_Exception, "%s", strerror(errno));
        return NULL;
    }
    return PyUnicode_FromStringAndSize(buf, strlen(buf));
}

int __ipv4_set_addr(PyObject *value, u32 *addr)
{
    PyObject *obj;
    struct in_addr in;

    if (!inet_pton(AF_INET, PyBytes_AsString(value), &in)) {
        PyErr_SetString(PyExc_Exception, "The string passed is not a"
                        " valid ipv4 address");
        return -1;
    }
    *addr = in.s_addr;

    return 0;
}

int __ipv6_set_addr(PyObject *value, u8 *addr)
{
    PyObject *obj;
    struct in6_addr in;

    if (!inet_pton(AF_INET6, PyBytes_AsString(value), &in)) {
        PyErr_SetString(PyExc_Exception, "The string passed is not a"
                        " valid ipv6 address");
        return -1;
    }
    memcpy(addr, &in, sizeof(struct in6_addr));

    return 0;
}
