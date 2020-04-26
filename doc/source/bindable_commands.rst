=====================
Commands to bind to
=====================

.. module:: pyreadline.lineeditor.lineobj
   :synopsis: Commands that users can use to bind to keys

This appendix will contain descriptions of all commands to bind to.

.. For now you have to look in the sourcecode. Check the readline class of the file rlmain.py
   Let's add them! Btw bindable isn't a word.

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

