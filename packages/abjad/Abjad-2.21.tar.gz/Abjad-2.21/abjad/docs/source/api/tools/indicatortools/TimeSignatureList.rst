.. currentmodule:: abjad.tools.indicatortools

TimeSignatureList
=================

.. autoclass:: TimeSignatureList

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
              "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>TimeSignatureList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList";
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

      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.append
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.count
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.extend
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.index
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.insert
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.item_class
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.items
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.keep_sorted
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.pop
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.remove
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.reverse
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.sort
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__contains__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__delitem__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__eq__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__format__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__getitem__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__hash__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__iadd__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__illustrate__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__iter__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__len__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__ne__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__repr__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__reversed__
      ~abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__iadd__

.. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList.__setitem__
