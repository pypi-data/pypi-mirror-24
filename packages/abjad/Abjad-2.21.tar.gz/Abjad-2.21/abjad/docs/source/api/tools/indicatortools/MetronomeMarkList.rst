.. currentmodule:: abjad.tools.indicatortools

MetronomeMarkList
=================

.. autoclass:: MetronomeMarkList

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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>MetronomeMarkList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList";
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

      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.append
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.count
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.extend
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.index
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.insert
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.item_class
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.items
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.keep_sorted
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.pop
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.remove
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.reverse
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.sort
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__contains__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__delitem__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__eq__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__format__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__getitem__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__hash__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__iadd__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__illustrate__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__iter__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__len__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__ne__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__repr__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__reversed__
      ~abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.keep_sorted

Methods
-------

.. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.sort

Special methods
---------------

.. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__eq__

.. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__iadd__

.. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList.__setitem__
