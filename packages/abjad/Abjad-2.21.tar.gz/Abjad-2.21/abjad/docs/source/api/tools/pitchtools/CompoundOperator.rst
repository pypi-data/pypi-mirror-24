.. currentmodule:: abjad.tools.pitchtools

CompoundOperator
================

.. autoclass:: CompoundOperator

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.CompoundOperator.CompoundOperator" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>CompoundOperator</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.CompoundOperator.CompoundOperator";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.duplicate
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.invert
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.multiply
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.operators
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.retrograde
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.rotate
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.show_identity_operators
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.transpose
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__add__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__call__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__copy__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__eq__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__format__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__hash__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__ne__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__radd__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__repr__
      ~abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.operators

.. autoattribute:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.show_identity_operators

Methods
-------

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.duplicate

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.invert

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.multiply

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.retrograde

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.rotate

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.transpose

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__add__

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__ne__

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__repr__

.. automethod:: abjad.tools.pitchtools.CompoundOperator.CompoundOperator.__str__
