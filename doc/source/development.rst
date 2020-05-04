===========
Development
===========

Code Layout
===========

.. code-block:: none

   pyreadline
      rlmain      #contains Readline class
      clipboard   #clipboard functions
      console     #console interface
      keysyms     #key symbol mappings
      logger      #logging
      release     #release info

      lineeditor
         history     #implement history buffer
         lineobj     #implement lineeditor interface
         wordmatcher #functions for finding word boundaries

      modes       #editor modes
         emacs       #emacs mode
         notemacs    #crippled emacs for testing of mode selection functionality
         vi          #you can't spell evil without vi


Testing
========

The test suite is included with the pyreadline library.

.. automodule:: pyreadline.test.common
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.test.test_emacs
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.test.test_vi
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.test.test_history
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.test.test_lineeditor
   :members:
   :undoc-members:
   :show-inheritance:

