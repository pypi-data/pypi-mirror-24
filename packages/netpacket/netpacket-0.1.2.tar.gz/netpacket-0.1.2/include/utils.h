
#ifndef INCLUDE_UTILS_H
#define INCLUDE_UTILS_H

#include <Python.h>
#include <structmember.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "types.h"

PyObject *__get_mac_address(u8 *mac);
int __set_mac_address(u8 *mac, PyObject *value);
PyObject *__ipv4_get_addr(u32 addr);
PyObject *__ipv6_get_addr(u8 *addr);
int __ipv4_set_addr(PyObject *value, u32 *addr);
int __ipv6_set_addr(PyObject *value, u8 *addr);

#endif
