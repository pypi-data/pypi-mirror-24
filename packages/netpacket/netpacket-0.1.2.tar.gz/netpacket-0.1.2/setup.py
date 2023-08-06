
import os
from distutils.core import setup, Extension

FILES = ["src/netpacketmodule.c", "src/ppcap.c",
         "src/packet.c", "src/ethernet.c",
         "src/arp.c", "src/ip.c",
         "src/icmp.c", "src/tcp.c",
         "src/udp.c", "src/dhcpv4.c",
         "src/utils.c"]

def read(fname):
    return open(fname).read()

module = Extension("_netpacket", include_dirs=["/usr/include", "."],
                   library_dirs=["/usr/lib/"],
                   libraries=["pcap"],
                   extra_compile_args=["-Wno-unused-variable",
                                       "-Wno-pointer-sign",
                                       "-Wno-maybe-uninitialized",
                                       "-Wno-sign-compare"],
                   extra_objects="include/arp.h",
                   sources=FILES)

setup(name="netpacket", version="0.1.2",
      author="Magnus Stieglitz",
      author_email="mstieglitz@protonmail.com",
      description="Network packet-creator and packet-capturer module",
      long_description=read("README.rst"),
      url="https://github.com/Magnus9/netpacket",
      download_url="https://github.com/Magnus9/netpacket",
      platforms="Linux",
      license="BSD-2-Clause",
      ext_modules=[module],
      packages=["netpacket"])