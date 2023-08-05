.. currentmodule:: abjad.tools.instrumenttools

PerformerList
=============

.. autoclass:: PerformerList

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
              "abjad.tools.instrumenttools.PerformerList.PerformerList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PerformerList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.PerformerList.PerformerList";
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

      ~abjad.tools.instrumenttools.PerformerList.PerformerList.append
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.count
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.extend
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.get_instrument
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.index
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.insert
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.item_class
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.items
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.keep_sorted
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.pop
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.remove
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.reverse
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.sort
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__contains__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__delitem__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__eq__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__format__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__getitem__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__hash__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__iadd__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__iter__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__len__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__ne__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__repr__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__reversed__
      ~abjad.tools.instrumenttools.PerformerList.PerformerList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.PerformerList.PerformerList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.PerformerList.PerformerList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.PerformerList.PerformerList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.extend

.. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.get_instrument

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerList.PerformerList.__setitem__
