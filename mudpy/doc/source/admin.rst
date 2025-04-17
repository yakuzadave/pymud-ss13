=============
 admin guide
=============

.. Copyright (c) 2020 mudpy authors. Permission to use, copy,
   modify, and distribute this software is granted under terms
   provided in the LICENSE file distributed with this software.

This guide provides basic management, configuration and
troubleshooting tips for mudpy administrators.

.. _admin-accounts:

admin accounts
--------------

Either create an account named *admin* or modify the main
configuration file (for example, :file:`etc/mudpy.yaml`) and change
the ``.mudpy.limit.admins`` list to include the name of your initial
admin user. Once you have at least one administrative user, that
user can so something like :command:`set account.someuser
administrator True` to elevate another account's access. It's
probably best to empty or remove the ``.mudpy.limit.admins list``
from the configuration before making the service publicly
accessible.

While the service isn't running you can also edit the accounts.yaml
file (probably :file:`data/accounts.yaml` unless you've changed the
default data path) and add a line like
``account.someuser.administrator: true`` for any already existing
account in that file. In future, a separate system command-line
utility may be provided to make pre-seeding administrator accounts
possible at time of installation so that the service doesn't need to
be started with an initially insecure configuration.

content creation
----------------

Once you've created and awakened an avatar for an an
:ref:`administrator <admin-accounts>`, you can use the interactive
command-line interface to create or destroy elements and set or
delete facets on them. A set of sample elements are available in the
source tree and included by default from the sample configuration
file (specified in its ``_load`` list). You can also just edit those
files with a text editor or create a new directory with your own
YAML file in it to load instead.

See the built-in :command:`help` as an administrator for the
:command:`create`, :command:`destroy`, :command:`set` and
:command:`delete` commands. For example, you can set an arbitrary
value on a facet of any element like::

    set account.someuser myperm True

This would add or update a *myperm* facet to the account element for
the *someuser* user to have the value *True*.

troubleshooting
---------------

The administrative :command:`show` command provides a number of
useful inspection tools. Here's an example testing with the
:command:`evaluate` debug command from an active session with a
couple of avatars awake, comparing with the output from related
:command:`show group` and :command:`show element` invocations::

    > show group actor

    These are the elements in the "actor" group:

       actor.avatar_admin_0
       actor.avatar_luser0_0

    > evaluate actor.universe.groups['actor'].keys()

    dict_keys(['avatar_admin_0', 'avatar_luser0_0'])

    > show element actor.avatar_luser0_0

    These are the properties of the "actor.avatar_luser0_0" element (in
    "/home/fungi/src/mudpy.org/mudpy/data/actor.yaml"):

       gender: female
       inherit: ['archetype.avatar', 'archetype.actor']
       location: area.0,0,0
       name: Keyo

    > evaluate actor.universe.contents['actor.avatar_luser0_0'].get('name')

    'Keyo'

Note that for safety the :command:`evaluate` executes within the context of
a command handler with limited Python :code:`__builtins__`, the
:code:`mudpy` library package, and the active :code:`universe` available,
and also blocks evaluation of any statement containing double-underscores
(:code:`__`) as well as :code:`lambda` functions. For admins to gain access
to unsafe debugging commands, the ``.mudpy.limit.debug`` option must be
enabled in configuration first and the service reloaded or restarted. It
should still be considered unsafe, since the engine's file handling
functions could easily alter accessible files or expressions like
``9**9**9`` could be used to hang the service for indeterminate periods.
