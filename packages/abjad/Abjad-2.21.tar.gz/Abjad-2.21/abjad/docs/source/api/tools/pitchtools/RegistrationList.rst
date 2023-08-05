.. currentmodule:: abjad.tools.pitchtools

RegistrationList
================

.. autoclass:: RegistrationList

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [background=transparent,
              bgcolor=transparent,
              color=lightslategrey,
              fontname=Arial,
              outputorder=edgesfirst,
              overlap=prism,
              penwidth=2,
              rankdir=LR,
              root="__builtin__.object",
              splines=spline,
              style="dotted, rounded",
              truecolor=true];
          node [colorscheme=pastel19,
              fontname=Arial,
              fontsize=12,
              penwidth=2,
              style="filled, rounded"];
          edge [color=lightsteelblue2,
              penwidth=2];
          subgraph cluster_abctools {
              graph [label=abctools];
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=1,
                  group=0,
                  label=AbjadObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.RegistrationList.RegistrationList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>RegistrationList</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.RegistrationList.RegistrationList";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedList`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.append
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.count
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.extend
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.index
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.insert
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.item_class
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.items
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.keep_sorted
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.pop
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.remove
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.reverse
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.sort
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__contains__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__delitem__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__eq__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__format__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__getitem__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__hash__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__iadd__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__iter__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__len__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__ne__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__repr__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__reversed__
      ~abjad.tools.pitchtools.RegistrationList.RegistrationList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.RegistrationList.RegistrationList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.RegistrationList.RegistrationList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.RegistrationList.RegistrationList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.sort

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationList.RegistrationList.__setitem__
