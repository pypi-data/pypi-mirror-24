.. currentmodule:: abjad.tools.markuptools

MarkupList
==========

.. autoclass:: MarkupList

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
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupList.MarkupList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>MarkupList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.markuptools.MarkupList.MarkupList";
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

      ~abjad.tools.markuptools.MarkupList.MarkupList.append
      ~abjad.tools.markuptools.MarkupList.MarkupList.center_column
      ~abjad.tools.markuptools.MarkupList.MarkupList.column
      ~abjad.tools.markuptools.MarkupList.MarkupList.combine
      ~abjad.tools.markuptools.MarkupList.MarkupList.concat
      ~abjad.tools.markuptools.MarkupList.MarkupList.count
      ~abjad.tools.markuptools.MarkupList.MarkupList.extend
      ~abjad.tools.markuptools.MarkupList.MarkupList.index
      ~abjad.tools.markuptools.MarkupList.MarkupList.insert
      ~abjad.tools.markuptools.MarkupList.MarkupList.item_class
      ~abjad.tools.markuptools.MarkupList.MarkupList.items
      ~abjad.tools.markuptools.MarkupList.MarkupList.keep_sorted
      ~abjad.tools.markuptools.MarkupList.MarkupList.left_column
      ~abjad.tools.markuptools.MarkupList.MarkupList.line
      ~abjad.tools.markuptools.MarkupList.MarkupList.overlay
      ~abjad.tools.markuptools.MarkupList.MarkupList.pop
      ~abjad.tools.markuptools.MarkupList.MarkupList.remove
      ~abjad.tools.markuptools.MarkupList.MarkupList.reverse
      ~abjad.tools.markuptools.MarkupList.MarkupList.right_column
      ~abjad.tools.markuptools.MarkupList.MarkupList.sort
      ~abjad.tools.markuptools.MarkupList.MarkupList.__contains__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__delitem__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__eq__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__format__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__getitem__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__hash__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__iadd__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__illustrate__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__iter__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__len__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__ne__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__repr__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__reversed__
      ~abjad.tools.markuptools.MarkupList.MarkupList.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.markuptools.MarkupList.MarkupList.item_class

.. autoattribute:: abjad.tools.markuptools.MarkupList.MarkupList.items

.. autoattribute:: abjad.tools.markuptools.MarkupList.MarkupList.keep_sorted

Methods
-------

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.append

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.center_column

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.column

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.combine

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.concat

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.count

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.extend

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.index

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.insert

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.left_column

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.line

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.overlay

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.pop

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.reverse

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.right_column

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.sort

Special methods
---------------

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__eq__

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__hash__

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__iadd__

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__reversed__

.. automethod:: abjad.tools.markuptools.MarkupList.MarkupList.__setitem__
