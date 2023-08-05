.. currentmodule:: abjad.tools.instrumenttools

InstrumentList
==============

.. autoclass:: InstrumentList

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
              "abjad.tools.instrumenttools.InstrumentList.InstrumentList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>InstrumentList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.InstrumentList.InstrumentList";
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

      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.append
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.count
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.extend
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.index
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.insert
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.item_class
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.items
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.keep_sorted
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.pop
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.remove
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.reverse
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.sort
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__contains__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__delitem__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__eq__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__format__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__getitem__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__hash__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__iadd__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__iter__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__len__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__ne__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__repr__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__reversed__
      ~abjad.tools.instrumenttools.InstrumentList.InstrumentList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__eq__

.. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__ne__

.. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentList.InstrumentList.__setitem__
