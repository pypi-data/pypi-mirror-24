mir.termdbg
===========

.. image:: https://circleci.com/gh/darkfeline/mir.termdbg.svg?style=shield
   :target: https://circleci.com/gh/darkfeline/mir.termdbg
   :alt: CircleCI
.. image:: https://codecov.io/gh/darkfeline/mir.termdbg/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/darkfeline/mir.termdbg
   :alt: Codecov
.. image:: https://badge.fury.io/py/mir.termdbg.svg
   :target: https://badge.fury.io/py/mir.termdbg
   :alt: PyPi Release

Terminal debugging tools.

Commands
--------

mir.termdbg includes two commands.

::

   $ python3.6 -m mir.termdbg

Simple terminal key press debugger.

termdbg echoes the bytes received directly from the terminal for debugging
exactly what bytes or escape sequences a particular terminal is sending.  The
terminal is set to raw mode if possible.

termdbg's output is intended for human consumption; the output format is not
guaranteed and should not be parsed.

To exit, send the byte value 3.  This is the ASCII encoding for ``^C``
(End Of Text), which is sent by pressing CTRL-C for most terminals.
If you are unable to exit, you can send SIGINT from a separate
terminal.

Example usage::

  $ python3.6 -m mir.termdbg
   97, 0o141, 0x61, a                             # a pressed
    1, 0o001, 0x01, SOH, ␁, ^A, Start of Heading  # Ctrl-A pressed
   27, 0o033, 0x1B, ESC, ␛, ^[, Escape            # F1 pressed
   79, 0o117, 0x4F, O
   80, 0o120, 0x50, P
    3, 0o003, 0x03, ETX, ␃, ^C, End of Text       # Ctrl-C pressed
  $

::

   $ python3.6 -m mir.termdbg.ccr

Control code revealer.

Run a program with arguments and pretend to be a terminal, teeing output
to a file.

This can be used to debug what control codes a troublesome program is
emitting when it thinks it's talking to a terminal.

Example usage::

   $ python3.6 -m mir.termdbg.ccr logfile bad_program arg1 arg2
