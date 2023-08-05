.. currentmodule:: abjad.tools.scoretools

NoteHeadList
============

.. autoclass:: NoteHeadList

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>NoteHeadList</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadList.NoteHeadList";
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

      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.append
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.client
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.count
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.extend
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.get
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.index
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.insert
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.item_class
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.items
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.keep_sorted
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.pop
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.remove
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.reverse
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.sort
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__contains__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__delitem__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__eq__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__format__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__getitem__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__hash__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__iadd__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__iter__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__len__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__ne__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__repr__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__reversed__
      ~abjad.tools.scoretools.NoteHeadList.NoteHeadList.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.client

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.count

.. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.extend

.. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.get

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.insert

.. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.pop

.. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadList.NoteHeadList.__setitem__
