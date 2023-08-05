.. currentmodule:: abjad.tools.metertools

MeterList
=========

.. autoclass:: MeterList

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
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterList.MeterList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>MeterList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.metertools.MeterList.MeterList";
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

      ~abjad.tools.metertools.MeterList.MeterList.append
      ~abjad.tools.metertools.MeterList.MeterList.count
      ~abjad.tools.metertools.MeterList.MeterList.extend
      ~abjad.tools.metertools.MeterList.MeterList.index
      ~abjad.tools.metertools.MeterList.MeterList.insert
      ~abjad.tools.metertools.MeterList.MeterList.item_class
      ~abjad.tools.metertools.MeterList.MeterList.items
      ~abjad.tools.metertools.MeterList.MeterList.keep_sorted
      ~abjad.tools.metertools.MeterList.MeterList.pop
      ~abjad.tools.metertools.MeterList.MeterList.remove
      ~abjad.tools.metertools.MeterList.MeterList.reverse
      ~abjad.tools.metertools.MeterList.MeterList.sort
      ~abjad.tools.metertools.MeterList.MeterList.__contains__
      ~abjad.tools.metertools.MeterList.MeterList.__delitem__
      ~abjad.tools.metertools.MeterList.MeterList.__eq__
      ~abjad.tools.metertools.MeterList.MeterList.__format__
      ~abjad.tools.metertools.MeterList.MeterList.__getitem__
      ~abjad.tools.metertools.MeterList.MeterList.__hash__
      ~abjad.tools.metertools.MeterList.MeterList.__iadd__
      ~abjad.tools.metertools.MeterList.MeterList.__illustrate__
      ~abjad.tools.metertools.MeterList.MeterList.__iter__
      ~abjad.tools.metertools.MeterList.MeterList.__len__
      ~abjad.tools.metertools.MeterList.MeterList.__ne__
      ~abjad.tools.metertools.MeterList.MeterList.__repr__
      ~abjad.tools.metertools.MeterList.MeterList.__reversed__
      ~abjad.tools.metertools.MeterList.MeterList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.MeterList.MeterList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.MeterList.MeterList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.MeterList.MeterList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__iadd__

.. automethod:: abjad.tools.metertools.MeterList.MeterList.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterList.MeterList.__setitem__
