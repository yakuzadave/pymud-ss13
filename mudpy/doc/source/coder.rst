=============
 coder guide
=============

.. Copyright (c) 2004-2021 mudpy authors. Permission to use, copy,
   modify, and distribute this software is granted under terms
   provided in the LICENSE file distributed with this software.

This guide attempts to embody a rudimentary set of rules for developer
submissions of source code and documentation targeted for inclusion
within the mudpy project, as well as pointers to useful resources for
those attempting to obtain a greater understanding of the software.

source
------

As with any project, the mudpy source code could always be better
documented, and contributions to that end are heartily welcomed.

version control system
~~~~~~~~~~~~~~~~~~~~~~

Git_ is used for version control on the project, and the archive can
be browsed or cloned anonymously from the official
https://mudpy.org/code/mudpy repository location. For now, detailed
commits can be E-mailed to fungi@yuggoth.org, but there will most
likely be a developer mailing list for more open presentation and
discussion of patches eventually.

A :file:`ChangeLog` is generated automatically from repository
commit logs, and is included automatically in all sdist_ tarballs. It
can be regenerated easily by running :command:`tox -e dist` from the
top level directory of the Git repository in a working `developer
environment`_.

.. _Git: https://git-scm.com/
.. _sdist: https://packaging.python.org/glossary
           /#term-source-distribution-or-sdist

developer environment
~~~~~~~~~~~~~~~~~~~~~

Basic developer requirements are a POSIX Unix derivative (such as
Linux), a modern Python 3 interpreter (any of the minor revisions
mentioned in the ``metadata.classifier`` section of
:file:`setup.cfg`) and a recent release of the tox_ utility (at least
the ``tox.minversion`` mentioned in :file:`tox.ini`).

.. _tox: https://tox.readthedocs.io/

application program interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :doc:`api` API documentation is maintained within docstrings in
the mudpy source code.

regression testing
~~~~~~~~~~~~~~~~~~

All new commits are tested using an included
:mod:`mudpy.test.selftest` script, to help ensure the software is
continually usable. Any new features should be accompanied by
suitable regression tests so that their functionality can be
maintained properly through future releases. The selftest can be
invoked with :command:`tox -e py3` which will automatically start
the daemon with the :file:`mudpy/tests/fixtures/test_daemon.yaml`
test configuration.

style
-----

This project follows Guido van Rossum and Barry Warsaw's `Style
Guide`_ for Python Code (a.k.a. "PEP-8"). When in need of sample
code or other examples, any common source code file or text document
file distributed as part of mudpy should serve as a suitable
reference. Testing of all new patches with the flake8_ utility
should be performed by running :command:`tox -e flake8` from the
repository working directory to ensure adherence to preferred style
conventions.

.. _Style Guide: :pep:`0008`
.. _flake8: https://pypi.org/project/flake8

.. _demo:

test and demo walk-through
--------------------------

The included tox configuration provides testenv definitions for a
variety of analyzers, regression tests, documentation builds and
package generation. It also has a ``demo`` testenv which will run
the server using the provided :file:`etc/mudpy.yaml` and other
sample files. By default it listens on TCP port 4000 at the IPv6
loopback address, streams its logging to the terminal via stdout,
and grants administrative rights automatically to an account named
``admin`` (once created).

Because all the dependencies besides the :command:`python3`
interpreter itself are available from PyPI, installing them should
be fairly similar across most GNU/Linux distributions. For example,
on Debian 10 (a.k.a. *Buster*) you need to expressly install the
``pip`` and ``venv`` modules since they're packaged separately from
the rest of the Python standard library. Once that's done, you can
perform a local install of ``tox`` as a normal non-root user. We're
also going to install system packages for the ``git`` revision
control toolset and an extensible console-based MUD client called
``tf5`` (TinyFugue version 5)::

    sudo apt install git python3-pip python3-venv tf5
    pip install --user tox
    exit

The reason for exiting is that, if this is the first time you've
ever used pip's ``--user`` option, when you log back in your
``~/.profile`` should see that there's now a ``~/.local/bin``
directory and add it to your ``$PATH`` environment variable
automatically from that point on. Next, retrieve the project source
code and switch your current working directory to where you've
cloned it::

    git clone https://mudpy.org/code/mudpy
    cd mudpy

Now you should be able to invoke any tox testenv you like. Just
running :command:`tox` without any additional options will go
through the default battery of checks and is a good way to make sure
everything is installed and working. Once you're ready to try out
the server interactively, launch it like this::

    tox -e demo

Now in another terminal/session (because the one you've been using
is busy displaying the server's logs) connect using a MUD client
(such as :command:`tf5` which we installed above)::

    tf5 ip6-localhost 4000

Log in as ``admin`` creating an account and then an avatar and
awaken it. Try out the :command:`help` command and make sure you see
some command words in red (you're using a color terminal, right?)
since those are admin-only commands and being able to see them
confirms you're an administrator. When you're ready to terminate the
service you can either give the :command:`halt` command in your MUD
client terminal or press the ``control`` and ``c`` keys together in
the terminal where you ran tox. To exit the tf5 MUD client, give it
the :command:`/quit` command.

miscellanea
-----------

This section is a collection of various coding-related discussions
and treatises, mostly here because there's not a better place, and
so they don't get lost in random E-mail threads.

avatar names
~~~~~~~~~~~~

It comes up fairly often, so bears mentioning, **there is no
assumption avatar names will be globally unique**. This is part of
the reason the default :code:`choose_name` menu just runs
:func:`mudpy.misc.random_name`, to make impersonation a bit harder.
The idea is to make sure to be able to support realistic settings
where multiple people are often given the same names and don't
really have much choice as to what their parents decided to name
them at birth, but can still choose a name they like later (perhaps
through some cultural rite of passage quest, attaining a particular
guild rank, or just through a command they're allowed to run as soon
as they awaken that avatar for the first time).

It may be possible to force globally-unique avatar names, but the
need to treat avatars similarly to non-player characters (actors
which aren't associated with an account and may be driven by
scripted routines instead) means it may also be desirable to prevent
a user from choosing an avatar name which duplicates the name of any
existing actor (whether or not that actor is a user's avatar). This
would entail scanning the full dataset to identify actors with
similar names so they could be rejected or excluded for a new
avatar, but then raises the question as to what to do when some new
content adds NPCs with a name which is already in use.

The best way to side-step this challenge is to not rely on avatar
names for programmatic interaction and instead reference the
corresponding ID for an avatar's element in the universe contents.
IDs **are** already guaranteed to be globally unique, so there is no
ambiguity when using them (an avatar's element ID is constructed
from the owning account name plus an index integer). Exactly what
variables you have to work from will depend on the context where
your hypothetical routine is called.

Taking as an example, let's say what you want is to be able to have
an area's owner permit a specific avatar to pass through the portals
(doorways, gates, whatever) which connect it to other areas. This is
similar to how *guild houses* work in some classical MUDs. Here's
how I'd go about implementing it:

1. Extend the area element to have two new facets: *owners* (type
   list) and *visitors* (type list). The first will contain
   references to the element IDs for the avatars who are allowed to
   alter the entries of both lists, while the second will be the
   element IDs for avatars who are allowed to enter the area (maybe
   also allow owners to enter an area so they don't need to be
   duplicated in both lists).

2. Implement a command which allows someone to see the corresponding
   ID for an element (alternatively make it an acquirable ability,
   skill, spell, item, or however finding that information would
   best fit into your setting). This is stored in the element's
   :code:`.key` attribute, and you can play around with it on the
   command line with :command:`evaluate` like this::

    > look
    Center Sample Location
    This is the Center Sample Location. It is merely provided as an
    example of what an area might look like.
    [ Exits: down, east, north, south, up, west ]
    A sample prop sits here.
    Utso is here.

    > evaluate [
          a.key.split('_', 1)[1]
          for a in actor.universe.contents[
              actor.get('location')
          ].contents.values()
          if a.key.startswith('actor.avatar_')
          and a.get('name') == 'Utso'
      ][0]

    'luser0_0'

   [Put the command on one line, It's merely wrapped here for
   readability.] In short, this list comprehension takes the
   internal IDs for elements present in the calling actor's current
   location, filtered by whether they're avatars and a specific
   actor name, then splits the group and prefix off (relying on the
   fact that it uses ``_`` as a prefix separator) and returns the
   first result. In a non-prototype implementation, the command
   would probably include a routine which looked something like:

   .. code-block:: python

    location_id = actor.get("location")
    also_here = actor.universe.contents[location_id].contents
    for who in also_here.values():
        if (who.key.startswith("actor.avatar_")
                and who.get("name") == parameters[0]:
            message += "Avatar ID: %s" % .key.split("_", 1)[1]
            break

   That's a rough approximation, and not terribly immersive, but
   hopefully you get the idea. We could also improve the element
   attributes with pre-populated backlink references for some of
   these relationships to reduce code complexity.

3. Implement a command which allows a user to add and remove entries
   in the owners and visitors lists for their current location,
   which takes this avatar ID as a parameter.

4. Hook in the :meth:`mudpy.misc.Element.go_to` method to test the
   owners and visitors lists for the area parameter to make sure
   self is in one of those lists. Probably also stick in an override
   to make sure that if the actor's owner account is flagged as
   administrative then they're also allowed even if they're not on
   the allowed list.

The resulting workflow this would enable is that after an avatar *A*
has been set as an owner for area *X* (perhaps by an admin or a
world builder), *A* when in another area *Y* at the same time as
some avatar *B* whom they would like to be allowed to visit *X*
could run the identification command from part #2 above, then they
would later travel to *X* and run the safe passage command from part
#3 adding *B* to the visitors list for *X*. After that, *B* is able
freely enter *X* until *A* runs a similar command to remove them
from the visitors list for *X* again.

To tackle the immersion problem, an optional substitution cipher
could be implemented to (reversibly) turn those IDs into something
more mystical-looking. Also the identification command (or ability,
skill, spell, tool, whatever) could be limited to only work when the
area you're running it in is flagged a certain way. Taking this
concept further, all sorts of elements could have access lists for
which avatars own them and which avatars are allowed to interact
with them (in which case maybe the term *visitor* for the latter is
too area-specific and it needs a slightly more general term?).

However, a far more immersive solution would be to get closable and
lockable elements (and inventory management) implemented, have a
means of crafting keys which unlock specific elements, and then when
creating an area you want to restrict to specific avatars, put
locked doors for all its portals and give keys for them to anyone
you want to be able to visit. Or implement non-avatar actors, then
create guards you can hire or summon or construct to police your
doorways and check whether visitors are on a list. That list itself
could even be a piece of paper or a book (a prop), created with
appropriate materials and some skill which allows the actor to write
and edit paper notes, given to the guard and held by it as an
inventory item.

custom commands
~~~~~~~~~~~~~~~

Command definitions are split into metadata and procedure. The
metadata needs to be in an element like the basic ones shipped in
the :file:`share/command.yaml` file, and then a handler function
added to the :mod:`mudpy.command` module. There's not yet a plugin
layer to allow those to be added to a separate module. The function
name needs to match the element base name, or you have to add an
action facet to the element indicating the name of the function you
want it to call; the ``command.set`` element has an example of this,
so that we avoid shadowing Python's built-in :func:`set` function
and call :func:`mudpy.command.c_set` instead.

The :meth:`mudpy.misc.Element.set` method takes two parameters, the
name of the facet and the value to pass into it. An example of it in
action is :meth:`mudpy.misc.User.authenticate` where the user's
*administrator* facet is set to the value *True* if their username
is in the ``.mudpy.limit.admins`` list used to bootstrap
administrators:

.. code-block:: python
    :emphasize-lines: 9

    def authenticate(self):
        """Flag the user as authenticated and disconnect duplicates."""
        if self.state != "authenticated":
            self.authenticated = True
            log("User %s authenticated for account %s." % (
                    self, self.account.subkey), 2)
            if ("mudpy.limit" in universe.contents and self.account.subkey in
                    universe.contents["mudpy.limit"].get("admins")):
                self.account.set("administrator", True)
                log("Account %s is an administrator." % (
                        self.account.subkey), 2)
