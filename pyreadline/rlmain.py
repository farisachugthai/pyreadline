# -*- coding: utf-8 -*-
"""An attempt to implement readline for Python in Python using ctypes."""
# *****************************************************************************
#       Copyright (C) 2003-2006 Gary Bishop.
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************
from __future__ import print_function, unicode_literals, absolute_import

import abc
import logging
import os
import re
import sys
import time
import traceback
import warnings
from glob import glob
from typing import AnyStr, Union

from pyreadline.lineeditor import lineobj
from pyreadline.lineeditor import history
from pyreadline import clipboard, logger
from pyreadline.console.console import Console

from pyreadline.keysyms.common import make_KeyPress_from_keydescr
from pyreadline.unicode_helper import ensure_unicode, ensure_str
from pyreadline.logger import log
from pyreadline.modes import editingmodes
from pyreadline.error import ReadlineError, GetSetError

# from pyreadline import release
from pyreadline.py3k_compat import callable, execfile

config_path = warnings.warn(DeprecationWarning('Stop using this'))

class MockConsole(object):
    """Object used during refactoring.

    Should raise errors when someone tries to use it.
    """

    def __setattr__(self, x):
        from pyreadline.error import MockConsoleError

        raise MockConsoleError("Should not try to get attributes from MockConsole")

    def cursor(self, size=50):
        pass


# class BaseReadlineABC(abc.ABC):
#     """Standard readline library call, not available for all implementations."""

#     @abc.abstractmethod
#     def readline(self, prompt=""):
#         raise NotImplementedError

#     @abc.abstractmethod
#     def redisplay(self):
#         raise NotImplementedError

#     # @abc.abstractproperty
#     def console(self):
#         raise NotImplementedError

#     # @abc.abstractproperty
#     def mode(self):
#         # One of the most important properties in the repo
#         raise NotImplementedError

#     # @abc.abstractproperty
#     def l_buffer(self):  # type: Union[AnyStr, ReadLineTextBuffer]
#         raise NotImplementedError

#     # @abc.abstractproperty
#     # def ctrl_c_timeout(self):  # type: int
#     #     raise NotImplementedError

# abc.ABC.register(BaseReadlineABC)


class BaseReadline(object):
    def __init__(
        self,
        _allow_ctrl_c=False,
        debug=False,
        callback=None,
        bell_style="none",
        mark=-1,
        **kwargs
    ):
        self._allow_ctrl_c = _allow_ctrl_c
        self.debug = debug
        self.bell_style = bell_style
        self.mark = mark
        self.callback = callback
        self._ctrl_c_timeout = time.time()
        self.disable_readline = False
        # this code needs to follow l_buffer and history creation
        self.editingmodes = [mode(self) for mode in editingmodes]
        self.console = Console(**kwargs)
        self.mode = self.editingmodes[0]
        self.l_buffer = "" if self.mode.l_buffer is None else self.mode.l_buffer
        self.mode.init_editing_mode()

    def parse_and_bind(self, string):
        """Parse and execute single line of a readline init file."""
        log('parse_and_bind("%s")' % string, logging.DEBUG)
        if string.startswith("#"):
            return
        try:
            if string.startswith("set"):
                m = re.compile(r"set\s+([-a-zA-Z0-9]+)\s+(.+)\s*$").match(string)
                if m:
                    var_name = m.group(1)
                    val = m.group(2)
                    try:
                        setattr(self.mode, var_name.replace("-", "_"), val)
                    except AttributeError:
                        log('unknown var="%s" val="%s"' % (var_name, val))
                else:
                    log('bad set "%s"' % string)
                return
            m = re.compile(r"\s*(.+)\s*:\s*([-a-zA-Z]+)\s*$").match(string)
            if m:
                key = m.group(1)
                func_name = m.group(2)
                py_name = func_name.replace("-", "_")
                try:
                    func = getattr(self.mode, py_name)
                except AttributeError:
                    log('unknown func key="%s" func="%s"' % (key, func_name))
                    if self.debug:
                        print(
                            'pyreadline parse_and_bind error, unknown function to bind: "%s"'
                            % func_name
                        )
                    return
                self.mode._bind_key(key, func)
        except Exception:
            log("error")
            raise

    @property
    def prompt(self):
        return self.mode.prompt

    @prompt.setter
    def _set_prompt(self, prompt):
        self.mode.prompt = prompt

    def get_line_buffer(self):
        """Return the current contents of the line buffer."""
        return self.l_buffer.get_line_text()

    def insert_text(self, string):
        """Insert text into the command line."""
        self.mode.insert_text(string)

    def read_init_file(self, filename=None):
        """Parse a readline initialization file. The default filename is the last filename used."""
        log('read_init_file("%s")' % filename)

    # History file book keeping methods (non-bindable)

    @property
    def _history(self):
        return self.mode._history

    def add_history(self, line):
        """Append a line to the history buffer, as if it was the last line typed."""
        self.mode._history.add_history(line)

    def get_current_history_length(self):
        """Return the number of lines currently in the history.

        (This is different from get_history_length(), which returns
        the maximum number of lines that will be written to a history file).

        """
        return self.mode._history.get_current_history_length()

    def get_history_length(self):
        """Return the desired length of the history file.

        Negative values imply unlimited history file size.
        """
        return self.mode._history.get_history_length()

    def set_history_length(self, length):
        """Set the number of lines to save in the history file.

        `write_history_file` uses this value to truncate the history file
        when saving. Negative values imply unlimited history file size.
        """
        self.mode._history.set_history_length(length)

    def get_history_item(self, index):
        """Return the current contents of history item at index."""
        return self.mode._history.get_history_item(index)

    def clear_history(self):
        """Clear readline history"""
        self.mode._history.clear_history()

    def read_history_file(self, filename=None):
        """Load a readline history file. The default filename is ~/.history."""
        if filename is None:
            filename = self.mode._history.history_filename
        log("read_history_file from %s" % ensure_unicode(filename))
        self.mode._history.read_history_file(filename)

    def write_history_file(self, filename=None):
        """Save a readline history file. The default filename is ~/.history."""
        self.mode._history.write_history_file(filename)

    # Completer functions

    def set_completer(self, function=None):
        """Set or remove the completer function.

        If function is specified, it will be used as the new completer
        function; if omitted or None, any completer function already
        installed is removed. The completer function is called as
        function(text, state), for state in 0, 1, 2, ..., until it returns a
        non-string value. It should return the next possible completion
        starting with text.
        """
        log("set_completer")
        self.mode.completer = function

    def get_completer(self):
        """Get the completer function."""
        log("get_completer")
        return self.mode.completer

    def get_begidx(self):
        """Get the beginning index of the readline tab-completion scope."""
        return self.mode.begidx

    def get_endidx(self):
        """Get the ending index of the readline tab-completion scope."""
        return self.mode.endidx

    def set_completer_delims(self, string):
        """Set the readline word delimiters for tab-completion."""
        self.mode.completer_delims = string

    def get_completer_delims(self):
        """Get the readline word delimiters for tab-completion."""
        if sys.version_info[0] < 3:
            return self.mode.completer_delims.encode("ascii")
        else:
            return self.mode.completer_delims

    def set_startup_hook(self, function=None):
        """Set or remove the startup_hook function.

        If function is specified, it will be used as the new startup_hook
        function; if omitted or None, any hook function already installed is
        removed. The startup_hook function is called with no arguments just
        before readline prints the first prompt.

        """
        self.mode.startup_hook = function

    def set_pre_input_hook(self, function=None):
        """Set or remove the pre_input_hook function.

        If function is specified, it will be used as the new pre_input_hook
        function; if omitted or None, any hook function already installed is
        removed. The pre_input_hook function is called with no arguments
        after the first prompt has been printed and just before readline
        starts reading input characters.

        """
        self.mode.pre_input_hook = function

    # Functions that are not relevant for all Readlines but should at least have a NOP

    def _bell(self):
        pass

    #
    # Callback interface
    #
    def process_keyevent(self, keyinfo):
        return self.mode.process_keyevent(keyinfo)

    def keyboard_poll(self):
        return self.mode._readline_from_keyboard_poll()

    def callback_handler_install(self, prompt, callback):
        """Erhm?

        bool readline_callback_handler_install ( string prompt, callback callback)
        Initializes the readline callback interface and terminal, prints the prompt and returns immediately
        """
        self.callback = callback
        self.readline_setup(prompt)

    def callback_handler_remove(self):
        """Removes a callback handler and restores terminal settings."""
        self.callback = None

    def callback_read_char(self):
        """Reads a character and informs when a line is received."""
        if self.keyboard_poll():
            line = self.get_line_buffer() + "\n"
            # however there is another newline added by
            # self.mode.readline_setup(prompt) which is called by callback_handler_install
            # this differs from GNU readline
            self.add_history(self.mode.l_buffer)
            # TADA:
            self.callback(line)

    def _color_trtable(self):
        return {
            "black": 0,
            "darkred": 4,
            "darkgreen": 2,
            "darkyellow": 6,
            "darkblue": 1,
            "darkmagenta": 5,
            "darkcyan": 3,
            "gray": 7,
            "red": 4 + 8,
            "green": 2 + 8,
            "yellow": 6 + 8,
            "blue": 1 + 8,
            "magenta": 5 + 8,
            "cyan": 3 + 8,
            "white": 7 + 8,
        }

    def bind_key(self, key, name):
        import types

        if callable(name):
            self.mode._bind_key(key, types.MethodType(name, self.mode))
        else:
            self.mode._bind_key(key, getattr(self.mode, name))
            log("Trying to bind unknown command '%s' to key '%s'" % (name, key))

    def un_bind_key(self, key):
        keyinfo = make_KeyPress_from_keydescr(key).tuple()
        if keyinfo in self.mode.key_dispatch:
            del self.mode.key_dispatch[keyinfo]

    def bind_exit_key(self, key):
        self.mode._bind_exit_key(key)

    def un_bind_exit_key(self, key):
        keyinfo = make_KeyPress_from_keydescr(key).tuple()
        if keyinfo in self.mode.exit_dispatch:
            del self.mode.exit_dispatch[keyinfo]

    def set_prompt_color(self, color):
        self.prompt_color = self._color_trtable.get(color.lower(), 7)

    def set_input_color(self, color):
        self.command_color = self._color_trtable.get(color.lower(), 7)

    def setmode(self, name):
        self.mode = name

    def setkill_ring_to_clipboard(self, killring):
        pyreadline.lineeditor.lineobj.kill_ring_to_clipboard = killring

    def sethistoryfilename(self, filename):
        self.mode._history.history_filename = os.path.expanduser(ensure_str(filename))

    def setbellstyle(self, mode):
        """Update `bell_style`. Allowable options are 'none' and 'audible'."""
        # so idk if mode is a str but if it is we should allow it to be case-insensitive
        if hasattr(mode, "lower"):
            mode = mode.lower()
        self.bell_style = mode

    def disable_readline(self, mode):
        """This method exists but arguably doesn't make sense.

        Since we have to initialize the main class of the module to run this
        it doesn't really do anything.
        Even if it did, we don't get the chance to "disable" anything until
        after the user's config file is read.
        As a matter of fact that should be what we follow to figure out how
        to refactor.

        So let's see. We need to establish a ConfigFile class. Or a fileclass
        that both that and HistoryFile can subclass.

        Then FileReader. Maybe a Context class though that could get hard.
        Then Executor/Compiler. Compile the file and then figure out, should
        we be disabled??
        Oh shit we should actually figure that shit out though.
        Can we import site or will that be circular? Because I'd like to
        check if we're turned on through site.ENABLERLCOMPLETER or w/e it is.

        """
        self.disable_readline = mode

    def sethistorylength(self, length):
        """Set the length of the history in the config file.

        See Also
        --------
        :mod:`pyreadline.lineeditor.history`
        """
        selfmode.history_length = int(length)

    def allow_ctrl_c(self, mode):
        log("allow_ctrl_c:%s:%s" % (self.allow_ctrl_c, mode))
        self.allow_ctrl_c = mode

    def setbellstyle(self, mode):
        self.bell_style = mode

    def show_all_if_ambiguous(self, mode):
        self.mode.show_all_if_ambiguous = mode

    def ctrl_c_tap_time_interval(self, mode):
        self.ctrl_c_tap_time_interval = mode

    def mark_directories(self, mode):
        self.mode.mark_directories = mode

    def completer_delims(self, delims):
        self.mode.completer_delims = delims

    def complete_filesystem(self, delims):
        self.mode.complete_filesystem = delims.lower()

    def enable_ipython_paste_for_paths(self, boolean):
        self.mode.enable_ipython_paste_for_paths = boolean

    def debug_output(self, on, filename="pyreadline_debug_log.txt"):
        """Initialize the loggers used through the repository.

        Parameters
        ----------
        on : str
            One of 'on' or 'on_nologfile'. If is any other value, the
            global logger instance will be stopped.
        filename : str (pathlike)
            Path of the logfile

        """

        if on in ["on", "on_nologfile"]:
            self.debug = True

        if on == "on":
            logger.start_file_log(filename)
            logger.start_socket_log()
            logger.log("STARTING LOG")
        elif on == "on_nologfile":
            logger.start_socket_log()
            logger.log("STARTING LOG")
        else:
            logger.log("STOPING LOG")
            logger.stop_file_log()
            logger.stop_socket_log()

    def read_inputrc(self, inputrcpath=None):
        """In this method we `exec` `compile` the inputrc.

        As a result, it's a bit meaningless that it's an ini file.
        It's treated as a python file.

        The context it's executed in is in all the methods of this class.
        """
        if inputrcpath is None:
            inputrcpath = os.path.expanduser(ensure_str("~/pyreadlineconfig.ini"))

        loc = {
            # "branch": release.branch,
            # "version": release.version,
            "mode": self.editingmodes[0].mode,
            "modes": dict([(x.mode, x) for x in self.editingmodes]),
            "set_mode": self.setmode,
            "bind_key": self.bind_key,
            "disable_readline": self.disable_readline,
            "bind_exit_key": self.bind_exit_key,
            "un_bind_key": self.un_bind_key,
            "un_bind_exit_key": self.un_bind_exit_key,
            "bell_style": self.setbellstyle,
            "mark_directories": self.mark_directories,
            "show_all_if_ambiguous": self.show_all_if_ambiguous,
            "completer_delims": self.completer_delims,
            "complete_filesystem": self.complete_filesystem,
            "debug_output": self.debug_output,
            "history_filename": self.sethistoryfilename,
            "history_length": self.sethistorylength,
            "set_prompt_color": self.set_prompt_color,
            "set_input_color": self.set_input_color,
            "allow_ctrl_c": self.allow_ctrl_c,
            "ctrl_c_tap_time_interval": self.ctrl_c_tap_time_interval,
            "kill_ring_to_clipboard": self.setkill_ring_to_clipboard,
            "enable_ipython_paste_for_paths": self.enable_ipython_paste_for_paths,
        }
        if os.path.isfile(inputrcpath):
            try:
                execfile(inputrcpath, loc, loc)
            except Exception as x:
                log("Error reading .pyinputrc")
                log(x)
                # old line. wtf
                # filepath, lineno = traceback.extract_tb(sys.exc_traceback)[1][:2]
                # raise ReadlineError("Error reading .pyinputrc")
                raise

    def redisplay(self):
        """`_update_line`."""
        self._update_line()

class Readline(BaseReadline):
    """Main class for readline based on a console."""

    def __init__(self, command_color=None, prompt_color=None, prompt=None, _ctrl_c_tap_time_interval=None, _allow_ctrl_c=None, **kwargs):
        self.ctrl_c_time = time.time()
        self.command_color = command_color
        # So there is a set_prompt_color method so we could make this a property
        self.prompt_color = prompt_color
        self.editingmodes = [mode(self) for mode in editingmodes]
        self.mode = self.editingmodes[0]
        self.l_buffer = "" if self.mode.l_buffer is None else self.mode.l_buffer
        self._ctrl_c_tap_time_interval= _ctrl_c_tap_time_interval
        self.size = self.console.size()
        self.selection_color = self.console.saveattr << 4

    @property
    def ctrl_c_timeout(self):
        if not hasattr(self, '_ctrl_c_timeout'):
            self._ctrl_c_timeout = time.time()
        return self._ctrl_c_timeout

    @ctrl_c_timeout.setter
    def ctrl_c_timeout_setter(self, value):
        self._ctrl_c_timeout = value

    @ctrl_c_timeout.deleter
    def ctrl_c_timeout_deleter(self):
        del self._ctrl_c_timeout

    @property
    def console(self, **kwargs):
        if not hasattr(self, '_console'):
            self._console = Console(**kwargs)

        return self._console

    @console.setter
    def jeez(self, value):
        print('Good luck.')
        self._console = value

    @console.deleter
    def delete_console(self):
        del self._console

    @property
    def ctrl_c_tap_time_interval(self):
        return self._ctrl_c_tap_time_interval

    @ctrl_c_tap_time_interval.setter
    def set_ctrl_c_tap_time_interval(self, value):
        self._ctrl_c_tap_time_interval = value

    @ctrl_c_tap_time_interval.deleter
    def set_ctrl_c_tap_time_interval(self):
        del self._ctrl_c_tap_time_interval

    def _bell(self):
        """Ring the bell if requested. See `setbellstyle`.

        Raises
        ------
        NotImplementedError
            If bell_style is set to visible in the config file.
        ReadlineError
            If bell_style not in 'none', 'visible', or 'audible'.
        """
        if self.bell_style == "none":
            pass
        elif self.bell_style == "visible":
            raise NotImplementedError("Bellstyle visible is not implemented yet.")
        elif self.bell_style == "audible":
            self.console.bell()
        else:
            raise ReadlineError("Bellstyle %s unknown." % self.bell_style)

    def _clear_after(self):
        c = self.console
        x, y = c.pos()
        w, h = c.size()
        c.rectangle((x, y, w + 1, y + 1))
        c.rectangle((0, y + 1, w, min(y + 3, h)))

    def _set_cursor(self):
        c = self.console
        xc, yc = self.prompt_end_pos
        w, h = c.size()
        xc += self.mode.l_buffer.visible_line_width()
        while xc >= w:
            xc -= w
            yc += 1
        c.pos(xc, yc)

    def _print_prompt(self):
        c = self.console
        x, y = c.pos()

        n = c.write_scrolling(self.prompt, self.prompt_color)
        self.prompt_begin_pos = (x, y - n)
        self.prompt_end_pos = c.pos()
        self.size = c.size()

    def _update_prompt_pos(self, n):
        if n != 0:
            bx, by = self.prompt_begin_pos
            ex, ey = self.prompt_end_pos
            self.prompt_begin_pos = (bx, by - n)
            self.prompt_end_pos = (ex, ey - n)

    def _update_line(self):
        c = self.console
        l_buffer = self.mode.l_buffer
        c.cursor(0)  # Hide cursor avoiding flicking
        c.pos(*self.prompt_begin_pos)
        self._print_prompt()
        ltext = l_buffer.quoted_text()
        if l_buffer.enable_selection and (l_buffer.selection_mark >= 0):
            start = len(l_buffer[: l_buffer.selection_mark].quoted_text())
            stop = len(l_buffer[: l_buffer.point].quoted_text())
            if start > stop:
                stop, start = start, stop
            n = c.write_scrolling(ltext[:start], self.command_color)
            n = c.write_scrolling(ltext[start:stop], self.selection_color)
            n = c.write_scrolling(ltext[stop:], self.command_color)
        else:
            n = c.write_scrolling(ltext, self.command_color)

        x, y = c.pos()  # Preserve one line for Asian IME(Input Method Editor) statusbar
        w, h = c.size()
        if (y >= h - 1) or (n > 0):
            c.scroll_window(-1)
            c.scroll((0, 0, w, h), 0, -1)
            n += 1

        self._update_prompt_pos(n)
        if hasattr(c, "clear_to_end_of_window"):
            # Work around function for ironpython due to System.Console's lack of FillFunction
            c.clear_to_end_of_window()
        else:
            self._clear_after()

        # Show cursor, set size vi mode changes size in insert/overwrite mode
        c.cursor(1, size=self.mode.cursor_size)
        self._set_cursor()

    def callback_read_char(self):
        """Reads a character and notify when a line is received."""
        # Override base to get automatic newline
        if self.keyboard_poll():
            # I think there's an error here which is messing up python2 for me
            line = self.get_line_buffer() + "\n"
            self.console.write("\r\n")
            # however there is another newline added by
            # self.mode.readline_setup(prompt) which is called by callback_handler_install
            # this differs from GNU readline
            self.add_history(self.mode.l_buffer)
            # TADA:
            self.callback(line)

    def event_available(self):
        return self.console.peek() or (len(self.paste_line_buffer) > 0)

    def _readline_from_keyboard(self):
        while 1:
            if self._readline_from_keyboard_poll():
                break

    def _readline_from_keyboard_poll(self):
        pastebuffer = self.mode.paste_line_buffer
        if len(pastebuffer) > 0:
            # paste first line in multiline paste buffer
            self.l_buffer = lineobj.ReadLineTextBuffer(pastebuffer[0])
            self._update_line()
            self.mode.paste_line_buffer = pastebuffer[1:]
            return True

        c = self.console

        try:
            event = c.getkeypress()
        except KeyboardInterrupt:
            event = self.handle_ctrl_c()

        try:
            result = self.mode.process_keyevent(event.keyinfo)
        except EOFError:
            # logger.stop_logging()
            raise
        self._update_line()
        return result

    def nop(self, e):
        pass

    def readline_setup(self, prompt=""):
        self._print_prompt()
        self._update_line()
        return self.mode.readline_setup(prompt)

    def handle_ctrl_c(self):
        from pyreadline.keysyms.common import KeyPress
        from pyreadline.console.event import Event

        log("KBDIRQ")
        event = Event(0, 0)
        event.char = "c"
        event.keyinfo = KeyPress(
            "c", shift=False, control=True, meta=False, keyname=None
        )
        if self.allow_ctrl_c:
            now = time.time()
            if (now - self.ctrl_c_timeout) < self.ctrl_c_tap_time_interval:
                log("Raise KeyboardInterrupt")
                raise KeyboardInterrupt
            else:
                self.ctrl_c_timeout = now
        else:
            raise KeyboardInterrupt
        return event

    def readline(self, prompt=""):
        """Callback that returns after every line is sent by the user.

        Returns
        -------
        `get_line_buffer` with a newline after.

        Notes
        -----
        Updates 'ctrl_c_timeout'.

        """
        self.readline_setup(prompt)
        self._readline_from_keyboard()
        self.console.write("\r\n")
        line = self.get_line_buffer()
        if line != "":
            log("Returning. Line Buffer: (%s) " % line)

        return line + "\n"
