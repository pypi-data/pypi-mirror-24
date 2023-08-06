
"""
TCP Socket backend
"""

import re
import select
import socket
import time
import logging

import universal_usbtmc
from universal_usbtmc.exceptions import *

logger = logging.getLogger(__name__)

try:
    clock = time.perf_counter
except:
    clock = time.time

logger = logging.getLogger(__name__)


class Instrument(universal_usbtmc.Instrument):
    """
    Networked usbmtc device
    """

    EOL = ''
    RESOURCE_RE = r'TCPIP::(?P<host>[^:]*)(::(?P<port>\d+))?::(SOCKET|INSTR)'
    DEFAULT_PORT = 5025
    socket_timeout = .005
    min_wait = 0.9
    wait_after_write = 0

    def __init__(self, host_string):
        match = re.match(self.RESOURCE_RE, host_string)
        if match:
            self.host = match.group('host')
            self.port = match.group('port') or self.DEFAULT_PORT
        else:
            self.host = host_string
            self.port = self.DEFAULT_PORT
        self.connect()

    def connect(self):
        try:
            self.s = socket.create_connection((self.host, self.port), self.socket_timeout)
        except (ConnectionRefusedError, socket.gaierror) as e:
            raise UsbtmcError("Connection to host {} could not be established: {}".format(self.host, e))

    def write_raw(self, cmd):
        logger.debug('write_raw(' + str(cmd) + ')')
        self.s.sendall(cmd)
        # I sleep here, because sometimes subsequent messages are being joined on the receiving end...
        time.sleep(self.wait_after_write)


    def read_raw(self, num=-1, timeout=0.0):
        if num == -1: num = 1024*1024+1024
        ret = b""
        start = clock()
        wait = max(self.min_wait, timeout)
        while True:
            try:
                ret += self.s.recv(num)
            except socket.timeout:
                if (clock() - start) > wait: break
                if len(ret): break
        logger.debug('read_raw() returns ' + str(ret))
        if not len(ret): raise UsbtmcReadTimeoutError()
        return ret

