===============
 install guide
===============

.. Copyright (c) 2020-2021 mudpy authors. Permission to use, copy,
   modify, and distribute this software is granted under terms
   provided in the LICENSE file distributed with this software.

This guide provides quick setup instructions for a basic mudpy
installation, sufficient as a starting point for further
configuration and customization.

installation
------------

There's a :ref:`demo` in the :doc:`coder` guide which will get you
up and running right away if you're familiar with the ``tox``
utility, but you can get by with just a supported Python_
interpreter. It's still easiest to do it from a `git clone`_ or
unpacked tarball_ of the source code so you have sample
configuration to work from. As long as your distro doesn't strip the
``venv`` module out of Python's standard library, from the top-level
source directory you could basically install it as a normal shell
user with::

    python3 -m venv mudpy_venv
    mudpy_venv/bin/pip install .

And then you can start the service with::

    mudpy_venv/bin/mudpy

If the ``python3`` command above emits an error like *No module
named venv*, then you're probably on a distribution like Debian
which needs the `python3-venv package`_ installed with your package
manager first.

.. _Python: https://python.org/
.. _git clone: https://mudpy.org/code/mudpy/
.. _tarball: https://mudpy.org/dist/mudpy/
.. _python3-venv package: https://packages.debian.org/python3-venv

initialization
--------------

The mudpy service is self-initializing the first time you start it,
though you need some minimum configuration in its config search
path. The installation_ example above uses the sample
:file:`etc/mudpy.conf` configuration provided in the source tree,
but you can edit this or make a modified copy and pass its name as
the only command-line argument to the executable entrypoint::

    mudpy_venv/bin/mudpy my_config.yaml

By default it'll only listen on the loopback address, but that's
configurable in the `network settings <.mudpy.network>`_ of course.
The basic element definitions are included in the :file:`share`
directory as well as basic archetype, command and menu element
definitions. The default configuration is set so that if anyone
creates a user named "admin" then that account will start with
administrative privileges, configurable in the `admins limit
<.mudpy.limit.admins>`_.

Using ``pip`` to install in a venv or with its ``--user`` option
takes care of making sure the Python package dependencies listed in
the ``options.install_requires`` field of the :file:`setup.cfg` file
are available, but it should be possible to run
:file:`mudpy/daemon.py` as a normal python3 script as long as you've
installed your distro's packages of the dependencies (on
Debian/Ubuntu that's python3-passlib_ and python3-yaml_, they're
probably named something similar on other distros).

.. _python3-passlib: https://packages.debian.org/python3-passlib
.. _python3-yaml: https://packages.debian.org/python3-yaml

platforms
---------

There's a good chance that some of the file handling and socket
routines are not cross-platform compatible and will only work on
Unix derivatives like Linux, \*BSD or GNU Hurd (possibly also Mac OS
X/Darwin since it's essentially a BSD descendant). All changes to
the codebase are tested on Debian GNU/Linux, but it should at least
work reliably on any Linux distribution with a new enough Python
interpreter. It probably also works on Microsoft Windows under the
WSL (Windows Subsystem for Linux) compatibility layer.
