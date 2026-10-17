#!/usr/bin/env python3
"""Linux verification helper: deny Internet sockets for this process and descendants.

Requires Python 3 and libseccomp. Does not modify host network configuration.
Usage: python3 scripts/offline-linux.py node bin/ocr-tb.js doctor
"""
import ctypes
import ctypes.util
import errno
import os
import socket
import sys

library = ctypes.util.find_library('seccomp')
if sys.platform != 'linux' or not library:
    print('Linux libseccomp required for offline verification', file=sys.stderr)
    sys.exit(77)
lib = ctypes.CDLL(library, use_errno=True)

class ArgCompare(ctypes.Structure):
    _fields_ = [('arg', ctypes.c_uint), ('op', ctypes.c_int),
                ('datum_a', ctypes.c_uint64), ('datum_b', ctypes.c_uint64)]

lib.seccomp_init.argtypes = [ctypes.c_uint32]
lib.seccomp_init.restype = ctypes.c_void_p
lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
lib.seccomp_syscall_resolve_name.restype = ctypes.c_int
lib.seccomp_rule_add_array.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int,
                                      ctypes.c_uint, ctypes.POINTER(ArgCompare)]
lib.seccomp_load.argtypes = [ctypes.c_void_p]
lib.seccomp_release.argtypes = [ctypes.c_void_p]
ctx = lib.seccomp_init(0x7fff0000)  # SCMP_ACT_ALLOW
if not ctx:
    raise RuntimeError('seccomp_init failed')
try:
    syscall = lib.seccomp_syscall_resolve_name(b'socket')
    for family in (socket.AF_INET, socket.AF_INET6):
        condition = ArgCompare(0, 4, family, 0)  # SCMP_CMP_EQ
        rc = lib.seccomp_rule_add_array(ctx, 0x00050000 | errno.EPERM, syscall, 1, ctypes.byref(condition))
        if rc != 0:
            raise RuntimeError(f'seccomp rule failed: {rc}')
    if lib.seccomp_load(ctx) != 0:
        raise RuntimeError('seccomp_load failed')
finally:
    lib.seccomp_release(ctx)
for family in (socket.AF_INET, socket.AF_INET6):
    try:
        probe = socket.socket(family, socket.SOCK_STREAM)
    except PermissionError:
        continue
    probe.close()
    raise RuntimeError('Network-denial probe unexpectedly succeeded')
if len(sys.argv) < 2:
    sys.exit('Command required')
print('Verified AF_INET/AF_INET6 denied; executing offline command', file=sys.stderr)
os.execvp(sys.argv[1], sys.argv[1:])
