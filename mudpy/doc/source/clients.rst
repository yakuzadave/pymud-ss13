=========
 clients
=========

.. Copyright (c) 2004-2018 mudpy authors. Permission to use, copy,
   modify, and distribute this software is granted under terms
   provided in the LICENSE file distributed with this software.

mudpy handles input, output and formatting of UTF-8 encoded,
multi-byte and wide characters, when coupled with a supporting
client. By default, however, only printable single-byte ASCII
characters are accepted or displayed unless the client negotiates
IETF RFC 856 *binary mode* first. If mudpy needs to send text
containing extended characters to a non-binary (7-bit) client, it
will first replace those characters with a question mark (``?``).

For example, the following is the recommended ``.telnetrc`` file for
interacting with mudpy in binary mode with the Netkit and Inetutils
Telnet clients::

  example.mudpy.org set binary
  example.mudpy.org unset echo
  example.mudpy.org unset escape
  example.mudpy.org unset flushoutput
  example.mudpy.org unset interrupt
  example.mudpy.org unset quit
  example.mudpy.org unset eof
  example.mudpy.org unset localchars
