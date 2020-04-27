=====================
Commands to bind to
=====================

.. module:: pyreadline.lineeditor.lineobj
   :synopsis: Commands that users can use to bind to keys

This appendix will contain descriptions of all commands to bind to.

Configuration file
==================

The configuration file is read from the users home directory and is named
pyreadlineconfig.ini. The files syntax is not the same as for GNU readline but
a python syntax is used instead. The available commands are:


    bind_exit_key
      is used to bind the keys that are used to exit the interpreter. (Ctrl-d,
      ctrl-z)

    bind_key
      is used to bind keys to editor functions

    un_bind_key
      is used to unbind keys can be useful to unbind default bindings the user
      does not like

    bell_style
      is used to set bell style. (none|visible|audible)

    show_all_if_ambiguous
      is used to enable the showing of a list of all alternative for tab
      completion (on|off)

    mark_directories
      show directories (on|off)

    completer_delims
      Which delimeters should be used to separate words for tab completion

    debug_output
      Turn on debug output (on|off). Not implemented yet.

    disable_readline
      Disable pyreadline completely (True|False).

    allow_ctrl_c
      Allows use of ctrl-c as copy key, still propagate keyboardinterrupt when not waiting for input.

    ctrl_c_tap_time_interval
      Set the ctrl-c double tap time interval to be used before issuing a KeyboadInterupt. Used
      to be able to have ctrl-c bound to copy.

    history_filename
      Set name of history file. Default is %USERPROFILE%/.pythonhistory

    history_length
      Set max length of history file default 200
      

.. For now you have to look in the sourcecode. Check the readline class of the file rlmain.py
   Let's add them! Btw bindable isn't a word.

Line Editor API
===============

.. autoclass:: TextLine
   :members:

Many commands are contained therein.

Methods as defined by the ReadLineTextBuffer
--------------------------------------------

.. class:: ReadLineTextBuffer(txtstr, point=None, mark=None, kwargs)

   An instance of the line buffer the user is currently editing.
   Can be initialized with many more keywords.

   The following commands are associated with the class.

   **Movement**

   .. method:: beginning_of_line

   .. method:: end_of_line

   .. method:: forward_char

   .. method:: backward_char

   .. method:: forward_word

   .. method:: backward_word

   .. method:: forward_word_end

   .. method:: backward_word_end(argument=1)

   .. method:: beginning_of_line_extend_selection()
    
   .. method:: end_of_line_extend_selection()

   .. method:: forward_char_extend_selection(argument=1)

   .. method:: backward_char_extend_selection(argument=1)

   .. method:: forward_word_extend_selection(argument=1)

   .. method:: backward_word_extend_selection(argument=1)

   .. method:: forward_word_end_extend_selection(argument=1)

   .. method:: backward_word_end_extend_selection(argument=1)

   .. method:: delete_selection()

   .. method:: delete_char(argument=1)

   .. method:: backward_delete_char(argument=1)

   .. method:: forward_delete_word(argument=1)

   .. method:: backward_delete_word(argument=1)

   .. method:: delete_current_word()

   .. method:: delete_horizontal_space()

   .. method:: upcase_word()

   .. method:: downcase_word()

History
========

.. automodule:: pyreadline.lineeditor.history
   :members:
   :undoc-members:
   :show-inheritance:

