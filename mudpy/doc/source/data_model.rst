============
 data model
============

.. Copyright (c) 2004-2019 mudpy authors. Permission to use, copy,
   modify, and distribute this software is granted under terms
   provided in the LICENSE file distributed with this software.

One of the primary goals for mudpy is to apply a consistent data
model for all information, from configuration and preferences to
user accounts and world data. Individual pieces of information are
called *facets*, and are grouped together into entities called
*elements*. Elements are meant to be treated as loosely-typed
objects (if it walks like a duck and talks like a duck...), while
facets within them have predefined names and are strictly typed.
This combination provides the ability to have facet inheritance
among elements as a layered sieve.

The mudpy data model consists of a mix of persistent data (stored
externally but cached in memory), and ephemeral data
(cross-reference indexes which can be regenerated from it). For now,
persistent data is stored externally in a tree-like hierarchy of
text files starting from a main configuration usually named
mudpy.yaml and cached in memory as a single python dict known as the
*universe*. This default implementation, while memory-hungry, is
planned so as to reduce the number of dict lookup operations
performed to retrieve an individual piece of information, when
compared with a more deeply-nested dict model.

groups
------

The universe is organized with a hierarchical namespace using the
period (``.``) symbol as a separator. It is rooted at ``.`` and
grows to the right with successive nodes. The right-most node must
always be a facet, and the remainder of the series thus denotes the
absolute name of an element within the universe (the second node
from the right being the relative element name and the remaining
nodes to the left are called the *group*). Near the root of the
universal namespace are a number of special elements anchored within
the ``.mudpy`` branch which provide necessary configuration
information and keeps some basic elements from cluttering the rest
of the tree.

.mudpy.actor
~~~~~~~~~~~~

Where new actor elements with no specified storage destination are
kept by default.


.mudpy.archetype
~~~~~~~~~~~~~~~~

Where the default archetype definitions are grouped together.

.mudpy.command
~~~~~~~~~~~~~~

Where the default command definitions are grouped together.

.mudpy.data
~~~~~~~~~~~

Defines default long-term storage locations for various element
groups.

.mudpy.facet
~~~~~~~~~~~~

Defines default values and validation checks for every facet.

.mudpy.filing
~~~~~~~~~~~~~

Defines filesystem-based backend storage meta data.

.mudpy.linguistic
~~~~~~~~~~~~~~~~~

Language specific configuration.

.mudpy.limit
~~~~~~~~~~~~

Various aspects determining mudpy performance.

.mudpy.log
~~~~~~~~~~

Configuration for logging.

.mudpy.menu
~~~~~~~~~~~

Where the default menu definitions are grouped together.

.mudpy.movement
~~~~~~~~~~~~~~~

Defines movement directions.

.mudpy.network
~~~~~~~~~~~~~~

Network socket configuration.

.mudpy.process
~~~~~~~~~~~~~~

Process-specific configuration.

.mudpy.prop
~~~~~~~~~~~

Where new prop elements with no specified storage destination are
kept by default.

.mudpy.room
~~~~~~~~~~~

Where new room elements with no specified storage destination are
kept by default.

.mudpy.timing
~~~~~~~~~~~~~

Timing-specific settings and scheduling for the main loop.

.mudpy.user
~~~~~~~~~~~

User-focused settings such as access controls.

storage
-------

Long-term storage is accomplished with YAML format files, consisting
of an associative array of keys mapped to values of various data
types. The keys can be either absolute (beginning with a ``.``
character) or relative to the anchor specified by the parent file
which loaded it. Special records can also exist to describe a data
file's properties, and always begin with an underscore (``_``).
These are stored in the universe under the ``.mudpy.file`` group
with elements named for escaped versions of the file path (``.`` and
``:`` replaced by ``\.`` and ``\:``) and the underscore stripped
from the beginning of each facet.

_copy
~~~~~

Arbitrary string providing copyright notice and license information.

_desc
~~~~~

Arbitrary string containing a description of the file or any other
useful information worth noting.

_load
~~~~~

List of additional data sources to load and where to anchor their
elements in the universe. The value is prefaced by the storage
medium separated from the remainder by an optional parenthetical
parameter and a colon. The only type implemented so far is ``file``
and the optional parameter is ``p`` to indicate a private file which
should only be readable by the account under which the process is
running rather than created with the default umask (ignored on
unsupported platforms).

_lock
~~~~~

Boolean value indicating read-only status. Any file not protected
with a _lock record will be regenerated and rewritten by mudpy if
its records are changed, so record format will be normalized,
records arbitrarily reordered and YAML comments lost in the process.
