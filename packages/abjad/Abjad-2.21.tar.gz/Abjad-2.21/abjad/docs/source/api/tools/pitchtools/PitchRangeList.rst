.. currentmodule:: abjad.tools.pitchtools

PitchRangeList
==============

.. autoclass:: PitchRangeList

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
              "abjad.tools.pitchtools.PitchRangeList.PitchRangeList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchRangeList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchRangeList.PitchRangeList";
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

      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.append
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.count
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.extend
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.index
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.insert
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.item_class
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.items
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.keep_sorted
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.pop
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.remove
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.reverse
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.sort
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__contains__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__delitem__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__eq__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__format__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__getitem__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__hash__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__iadd__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__illustrate__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__iter__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__len__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__ne__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__repr__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__reversed__
      ~abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.keep_sorted

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.sort

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__iadd__

.. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeList.PitchRangeList.__setitem__
