.. currentmodule:: abjad.tools.instrumenttools

ClefList
========

.. autoclass:: ClefList

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
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.ClefList.ClefList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ClefList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.ClefList.ClefList";
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

      ~abjad.tools.instrumenttools.ClefList.ClefList.append
      ~abjad.tools.instrumenttools.ClefList.ClefList.count
      ~abjad.tools.instrumenttools.ClefList.ClefList.extend
      ~abjad.tools.instrumenttools.ClefList.ClefList.index
      ~abjad.tools.instrumenttools.ClefList.ClefList.insert
      ~abjad.tools.instrumenttools.ClefList.ClefList.item_class
      ~abjad.tools.instrumenttools.ClefList.ClefList.items
      ~abjad.tools.instrumenttools.ClefList.ClefList.keep_sorted
      ~abjad.tools.instrumenttools.ClefList.ClefList.pop
      ~abjad.tools.instrumenttools.ClefList.ClefList.remove
      ~abjad.tools.instrumenttools.ClefList.ClefList.reverse
      ~abjad.tools.instrumenttools.ClefList.ClefList.sort
      ~abjad.tools.instrumenttools.ClefList.ClefList.__contains__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__delitem__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__eq__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__format__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__getitem__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__hash__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__iadd__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__illustrate__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__iter__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__len__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__ne__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__repr__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__reversed__
      ~abjad.tools.instrumenttools.ClefList.ClefList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.ClefList.ClefList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.ClefList.ClefList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.ClefList.ClefList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__iadd__

.. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ClefList.ClefList.__setitem__
