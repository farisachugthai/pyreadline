# -*- coding: utf-8 -*-
# *****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************
from __future__ import print_function, unicode_literals, absolute_import

import collections
import io
import os
import sys

from pyreadline.logger import log
from pyreadline.lineeditor import lineobj

from pyreadline.unicode_helper import ensure_str

# this could be neat
# try:
#     from _io import _WindowsConsoleIO
# except ImportError:
#     pass
# else:
#     RawIOBase.register(_WindowsConsoleIO)

# if "pyreadline" in sys.modules:
#     pyreadline = sys.modules["pyreadline"]
# else:
#     import pyreadline


class EscapeHistory(Exception):
    pass


class LineHistory(object):
    def __init__(
        self, _history_cursor=0, _history_length=100, history=None,
    ):
        """Initialize the LineHistory object.

        Parameters
        ----------
        history : list, optional
            An initial value of history lines.
        _history_cursor : int, optional
            Proxy for history_cursor property.
        _history_length : int, optional
            Proxy for history_length property.
        """
        # so hold up i assume this means we don't read in the history file
        # upon initialization. TODO: who does?
        self.history = [] if history is None else history
        self._history_length = _history_length
        self._history_cursor = _history_cursor
        self.history = []
        self._history_length = 100
        self._history_cursor = 0
        self.history_filename = os.path.expanduser(
            ensure_str("~/.history")
        )  # Cannot expand unicode strings correctly on python2.4
        self.lastcommand = None
        self.query = ""
        self.last_search_for = ""

    def get_current_history_length(self):
        """Return the number of lines currently in the history.
        (This is different from get_history_length(), which returns
        the maximum number of lines that will be written to a history file.)"""
        value = len(self.history)
        log("get_current_history_length:%d" % value)
        return value

    def get_history_length(self):
        """Return the desired length of the history file. Negative values imply
        unlimited history file size."""
        value = self._history_length
        log("get_history_length:%d" % value)
        return value

    def get_history_item(self, index):
        """Return the current contents of history item at index (starts with index 1)."""
        item = self.history[index - 1]
        log("get_history_item: index:%d item:%r" % (index, item))
        return item.get_line_text()

    def set_history_length(self, value):
        log("set_history_length: old:%d new:%d" % (self._history_length, value))
        self._history_length = value

    def get_history_cursor(self):
        value = self._history_cursor
        log("get_history_cursor:%d" % value)
        return value

    def set_history_cursor(self, value):
        log("set_history_cursor: old:%d new:%d" % (self._history_cursor, value))
        self._history_cursor = value

    history_length = property(get_history_length, set_history_length)
    history_cursor = property(get_history_cursor, set_history_cursor)

    def clear_history(self):
        """Clear readline history."""
        self.history[:] = []
        self.history_cursor = 0

    def read_history_file(self, filename=None, encoding=None):
        """Load a readline history file."""
        if encoding is None:
            encoding = sys.getdefaultencoding()
        if filename is None:
            filename = self.history_filename
        try:
            with io.open(filename, "rt", encoding="utf-8") as fd:
                for line in fd:
                    self.add_history(line.strip())
        except OSError:
            self.history = []
            self.history_cursor = 0

    def write_history_file(self, filename=None):
        """Save a readline history file."""
        if filename is None:
            filename = self.history_filename
        with io.open(filename, "wb") as fp:
            for line in self.history[-self.history_length:]:
                fp.write(ensure_str(line.get_line_text()))
                fp.write("\n".encode("ascii"))

    def add_history(self, line):
        """Append a line to the history buffer, as if it was the last line typed."""
        self.history.append(line)
        # Jesus christ
        # line = ensure_unicode(line)
        # if not hasattr(line, "get_line_text"):
        #     line = lineobj.ReadLineTextBuffer(line)
        # if not line.get_line_text():
        #     pass
        # elif (
        #     len(self.history) > 0
        #     and self.history[-1].get_line_text() == line.get_line_text()
        # ):
        #     pass
        # else:
        #     self.history.append(line)
        self.history_cursor = len(self.history)

    def previous_history(self, current):  # (C-p)
        """Move back through the history list, fetching the previous command. """
        if self.history_cursor == len(self.history):
            self.history.append(
                current.copy()
            )  # do not use add_history since we do not want to increment cursor

        if self.history_cursor > 0:
            self.history_cursor -= 1
            current.set_line(self.history[self.history_cursor].get_line_text())
            current.point = lineobj.EndOfLine

    def next_history(self, current):  # (C-n)
        """Move forward through the history list, fetching the next command. """
        if self.history_cursor < len(self.history) - 1:
            self.history_cursor += 1
            current.set_line(self.history[self.history_cursor].get_line_text())

    def beginning_of_history(self):  # (M-<)
        """Move to the first line in the history."""
        self.history_cursor = 0
        if len(self.history) > 0:
            self.l_buffer = self.history[0]

    def end_of_history(self, current):  # (M->)
        """Move to the end of the input history, i.e., the line currently
        being entered."""
        self.history_cursor = len(self.history)
        current.set_line(self.history[-1].get_line_text())

    def reverse_search_history(self, searchfor, startpos=None):
        if startpos is None:
            startpos = self.history_cursor
        origpos = startpos

        result = lineobj.ReadLineTextBuffer("")

        for idx, line in list(enumerate(self.history))[startpos:0:-1]:
            if searchfor in line:
                startpos = idx
                break

        # If we get a new search without change in search term it means
        # someone pushed ctrl-r and we should find the next match
        if self.last_search_for == searchfor and startpos > 0:
            startpos -= 1
            for idx, line in list(enumerate(self.history))[startpos:0:-1]:
                if searchfor in line:
                    startpos = idx
                    break

        if self.history:
            result = self.history[startpos].get_line_text()
        else:
            result = ""
        self.history_cursor = startpos
        self.last_search_for = searchfor
        log(
            "reverse_search_history: old:%d new:%d result:%r"
            % (origpos, self.history_cursor, result)
        )
        return result

    def forward_search_history(self, searchfor, startpos=None):
        if startpos is None:
            startpos = min(
                self.history_cursor, max(0, self.get_current_history_length() - 1)
            )
        origpos = startpos

        result = lineobj.ReadLineTextBuffer("")

        for idx, line in list(enumerate(self.history))[startpos:]:
            if searchfor in line:
                startpos = idx
                break

        # If we get a new search without change in search term it means
        # someone pushed ctrl-r and we should find the next match
        if (
            self.last_search_for == searchfor
            and startpos < self.get_current_history_length() - 1
        ):
            startpos += 1
            for idx, line in list(enumerate(self.history))[startpos:]:
                if searchfor in line:
                    startpos = idx
                    break

        if self.history:
            result = self.history[startpos].get_line_text()
        else:
            result = ""
        self.history_cursor = startpos
        self.last_search_for = searchfor
        return result

    def _search(self, direction, partial):
        try:
            if (
                self.lastcommand != self.history_search_forward
                and self.lastcommand != self.history_search_backward
            ):
                self.query = "".join(partial[0: partial.point].get_line_text())
            hcstart = max(self.history_cursor, 0)
            hc = self.history_cursor + direction
            while (direction < 0 and hc >= 0) or (
                direction > 0 and hc < len(self.history)
            ):
                h = self.history[hc]
                if not self.query:
                    self.history_cursor = hc
                    result = lineobj.ReadLineTextBuffer(h, point=len(h.get_line_text()))
                    return result
                elif h.get_line_text().startswith(self.query) and (
                    h != partial.get_line_text()
                ):
                    self.history_cursor = hc
                    result = lineobj.ReadLineTextBuffer(h, point=partial.point)
                    return result
                hc += direction
            else:
                if len(self.history) == 0:
                    pass
                elif hc >= len(self.history) and not self.query:
                    self.history_cursor = len(self.history)
                    return lineobj.ReadLineTextBuffer("", point=0)
                elif (
                    self.history[max(min(hcstart, len(self.history) - 1), 0)]
                    .get_line_text()
                    .startswith(self.query)
                    and self.query
                ):
                    return lineobj.ReadLineTextBuffer(
                        self.history[max(min(hcstart, len(self.history) - 1), 0)],
                        point=partial.point,
                    )
                else:
                    return lineobj.ReadLineTextBuffer(partial, point=partial.point)
                return lineobj.ReadLineTextBuffer(
                    self.query, point=min(len(self.query), partial.point)
                )
        except IndexError:
            raise

    def history_search_forward(self, partial):  # ()
        """Search forward through the history for the string of characters
        between the start of the current line and the point. This is a
        non-incremental search. By default, this command is unbound."""
        q = self._search(1, partial)
        return q

    def history_search_backward(self, partial):  # ()
        """Search backward through the history for the string of characters
        between the start of the current line and the point. This is a
        non-incremental search. By default, this command is unbound."""

        q = self._search(-1, partial)
        return q


class HistoryFile(io.TextIOWrapper):
    def __fspath__(self):
        return str(self.name)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, repr(self.name))

    def touch(self, filename: str) -> os.PathLike:
        return touch(filename)


# on god `self.assertIsInstance(OrderedHistory(), list)` just failed
# class OrderedHistory(collections.UserList):
class OrderedHistory(collections.abc.MutableSequence):
    def __init__(self, history=None, history_buffer=None, filename=None, **kwargs):
        self.history_filename = None
        self.history = history if history is not None else []

        super().__init__()
        try:
            self.filename = (
                filename
                if filename is not None
                else os.path.expanduser("~/.python_history")
            )
        except PermissionError:
            raise
        except OSError:
            self.filename = io.StringIO()

        # self.history_buffer = history_buffer if history_buffer is not None else HistoryFile()
        # self.read_history_file()

    def __repr__(self):
        return " %s " % self.__class__.__name__

    def __eq__(self, other):
        return self.history == other

    def __hash__(self):
        return hash(self.history)

    def __mro__(self):
        mro = getmro(self.__class__)
        ha = ("list", mro)
        return ha

    def add_history(self, line):
        """Append a line to the history buffer, as if it was the last line typed."""
        # Dont add an empty line
        if len(line) == 0:
            return
        # or one that's a duplicate of the previous
        elif len(self.history) > 0 and len(self.history[-1]) == len(line):
            if self.history[-1] != line:
                self.history.append(line)
        else:
            self.history.append(line)

    def __len__(self):
        return len(self.history)

    def __getitem__(self, index):
        return self.history[index]

    def __setitem__(self, idx, line, *args):
        if args:
            self.history[idx] = [line, *args]
        else:
            self.history[idx] = [line]

    def __delitem__(self, idx):
        del self.history[idx]

    def __add__(self, line):
        if isinstance(line, OrderedHistory):
            self.history.extend(line)
            self.write_history_file()
        else:
            self.history.append(line)

    def __iadd__(self, line):
        # So i recognize that this means in place addition is actually quite
        # different. however we don't do that anywhere in the repo so i'm trying
        # this out
        self.history.append(line)

    def insert(self, item, idx=0):
        self.history.insert(idx, item)

    def get_history_item(self, index):
        return self.history.__getitem__(index)

    def get_history_slice(self, start=0, stop=None, step=1):
        return slice(self.history[start], self.history[stop], step)

    def __slice__(self, start=0, stop=None, step=1):
        return self.get_history_slice(start, stop, step)

    def read_history_file(self, filename=None, encoding=None):
        """Load a readline history file."""
        if encoding is None:
            encoding = sys.getdefaultencoding()
        if filename is None:
            filename = self.filename
        try:
            with io.open(filename, "rt", encoding=encoding) as fd:
                for line in fd:
                    self.add_history(dedent(line))
        except PermissionError:
            raise
        except OSError:
            self.history = []
        except UnicodeDecodeError:
            raise  # TODO:

    def reset(self):
        self.history.clear()

    def flush(self):
        """Flush working contents and save to disk."""
        self.write_history_file(full=True)

    def __iter__(self):
        return iter(self.history)

    def __reversed__(self):
        for key in self.history:
            yield key

    def write_history_file(self, filename=None, full: bool = False, line: str = None):
        """Save a readline history file.

        Parameters
        ----------
        full :
        filename :
        line : object
        """
        if filename is None:
            filename = self.history_filename
        with io.open(filename, "ab+") as fp:
            if full:
                for line in self.history:
                    fp.write(line)
            elif line is not None:
                fp.write(line)


def main():
    """

    Returns
    -------
    object
    """
    q = LineHistory()
    r = LineHistory()
    RL = ReadLineTextBuffer()
    q.add_history(RL("aaaa"))
    q.add_history(RL("aaba"))
    q.add_history(RL("aaca"))
    q.add_history(RL("akca"))
    q.add_history(RL("bbb"))
    q.add_history(RL("ako"))
    r.add_history(RL("ako"))


if __name__ == "__main__":
    main()
