.. currentmodule:: abjad.tools.mathtools

Enumerator
==========

.. autoclass:: Enumerator

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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.Enumerator.Enumerator" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Enumerator</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.Enumerator.Enumerator";
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

      ~abjad.tools.mathtools.Enumerator.Enumerator.sequence
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_combinations
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_outer_product
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_pairs
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_partitions
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_permutations
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_set_partitions
      ~abjad.tools.mathtools.Enumerator.Enumerator.yield_subsequences
      ~abjad.tools.mathtools.Enumerator.Enumerator.__copy__
      ~abjad.tools.mathtools.Enumerator.Enumerator.__eq__
      ~abjad.tools.mathtools.Enumerator.Enumerator.__format__
      ~abjad.tools.mathtools.Enumerator.Enumerator.__hash__
      ~abjad.tools.mathtools.Enumerator.Enumerator.__ne__
      ~abjad.tools.mathtools.Enumerator.Enumerator.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.mathtools.Enumerator.Enumerator.sequence

Methods
-------

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_combinations

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_outer_product

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_pairs

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_partitions

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_permutations

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_set_partitions

.. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.yield_subsequences

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Enumerator.Enumerator.__repr__
