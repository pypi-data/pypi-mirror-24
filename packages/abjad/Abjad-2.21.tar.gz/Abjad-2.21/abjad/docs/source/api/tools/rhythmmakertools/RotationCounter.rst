.. currentmodule:: abjad.tools.rhythmmakertools

RotationCounter
===============

.. autoclass:: RotationCounter

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
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=3,
                  group=2,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>RotationCounter</B>>,
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
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedCounter`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.autoincrement
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.clear
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.copy
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.default
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.elements
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.item_class
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.items
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.keys
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.most_common
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.subtract
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.update
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.values
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.viewitems
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.viewkeys
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.viewvalues
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__add__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__and__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__contains__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__delitem__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__eq__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__format__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__getitem__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__hash__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__iter__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__len__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__ne__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__or__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__radd__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__repr__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__setitem__
      ~abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.autoincrement

.. autoattribute:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.default

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.elements

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.viewvalues

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__format__

.. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RotationCounter.RotationCounter.__sub__
