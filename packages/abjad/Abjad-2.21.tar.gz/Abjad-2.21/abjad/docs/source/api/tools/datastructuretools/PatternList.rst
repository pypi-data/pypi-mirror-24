.. currentmodule:: abjad.tools.datastructuretools

PatternList
===========

.. autoclass:: PatternList

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
              "abjad.tools.datastructuretools.PatternList.PatternList" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PatternList</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.datastructuretools.PatternList.PatternList";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedTuple`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.PatternList.PatternList.count
      ~abjad.tools.datastructuretools.PatternList.PatternList.get_matching_pattern
      ~abjad.tools.datastructuretools.PatternList.PatternList.get_matching_payload
      ~abjad.tools.datastructuretools.PatternList.PatternList.index
      ~abjad.tools.datastructuretools.PatternList.PatternList.item_class
      ~abjad.tools.datastructuretools.PatternList.PatternList.items
      ~abjad.tools.datastructuretools.PatternList.PatternList.__add__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__contains__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__eq__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__format__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__getitem__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__hash__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__iter__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__len__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__mul__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__ne__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__radd__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__repr__
      ~abjad.tools.datastructuretools.PatternList.PatternList.__rmul__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.PatternList.PatternList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.PatternList.PatternList.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.count

.. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.get_matching_pattern

.. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.get_matching_payload

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.index

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PatternList.PatternList.__rmul__
