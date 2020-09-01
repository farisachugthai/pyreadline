# -*- coding: utf-8 -*-
# *****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************
from __future__ import print_function, unicode_literals, absolute_import

import logging
import logging.handlers
import socket
from typing import Callable

from pyreadline.unicode_helper import ensure_str

# Was there something called sock_silent that used to be here?
# Asking from test/test_history


class CallableLogger(logging.Logger):  # type: Callable
    def __call__(self, msg, lvl=logging.WARNING, exc_info=0, stack_info=None):
        return self.log(msg, lvl=lvl, exc_info=exc_info, stack_info=stack_info)


def init_logger(log_level: int = logging.DEBUG, propagate: bool = False, fmt_msg: str = None, date_fmt: str = None) -> object:
    """Returns the pyreadline_logger used throughout the rest of the repo.

    Parameters
    ----------

    Returns
    -------
    `logging.Logger`.

    """
    logger = logging.getLogger("PYREADLINE")
    logger.setLevel(log_level)
    logger.propagate = propagate
    if fmt_msg is None:
        fmt_msg = "%(message)s"
    if date_fmt is None:
        datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt_msg, datefmt)
    handler = logging.StreamHandler()
    handler.setLevel(level=log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addFilter(logging.Filter())

    return logger


# Globals:


# TODO the actual version check
# why did adding a type annotation make this global statement raise an error?
# global pyreadline_logger

pyreadline_logger: logging.Logger = init_logger(
    log_level=logging.WARNING,
    fmt_msg="[ %(funcName)s : %(created)f - %(relativeCreated)d :] %(levelname)s : --- %(message)s ",
)

# socket_handler = None
# pyreadline_logger.addHandler(NullHandler())


class SocketStream(object):
    def __init__(self, host=None, port=None):
        self.logsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host if host is not None else "localhost"
        self.port = (
            port if port is not None else logging.handlers.DEFAULT_TCP_LOGGING_PORT
        )

    def write(self, s):
        self.logsocket.sendto(ensure_str(s), (self.host, self.port))

    def flush(self):
        pass

    def close(self):
        pass


def start_socket_log(formatter=None, log_level=30):
    socket_handler = logging.StreamHandler(
        SocketStream("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    )
    if formatter is None:
        formatter = logging.Formatter()
    socket_handler.setFormatter(formatter)
    socket_handler.setLevel(log_level)
    pyreadline_logger.addHandler(socket_handler)


def stop_socket_log(socket_handler):
    if socket_handler:
        pyreadline_logger.removeHandler(socket_handler)
        socket_handler = None


def start_file_log(filename, log_level=30):
    file_handler = logging.FileHandler(filename, "w")
    file_handler.setLevel(log_level)
    pyreadline_logger.addHandler(file_handler)


def stop_file_log(file_handler):
    if file_handler:
        pyreadline_logger.removeHandler(file_handler)
        file_handler.close()
        file_handler = None


def stop_logging():
    log("STOPING LOG")
    stop_file_log()
    stop_socket_log()


def log(s, log_level=30, exc_info=0):
    """Log a string. Allow for variable log levels."""
    pyreadline_logger.log(level=int(log_level), msg=str(s), exc_info=exc_info)
