.. currentmodule:: abjad.tools.scoretools

LeafMaker
=========

.. autoclass:: LeafMaker

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.LeafMaker.LeafMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LeafMaker</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.LeafMaker.LeafMaker";
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

      ~abjad.tools.scoretools.LeafMaker.LeafMaker.decrease_durations_monotonically
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.forbidden_written_duration
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.is_diminution
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.metrical_hierarchy
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.skips_instead_of_rests
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.use_messiaen_style_ties
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.use_multimeasure_rests
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__call__
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__copy__
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__eq__
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__format__
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__hash__
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__ne__
      ~abjad.tools.scoretools.LeafMaker.LeafMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.decrease_durations_monotonically

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.forbidden_written_duration

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.is_diminution

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.metrical_hierarchy

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.skips_instead_of_rests

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.use_messiaen_style_ties

.. autoattribute:: abjad.tools.scoretools.LeafMaker.LeafMaker.use_multimeasure_rests

Special methods
---------------

.. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.LeafMaker.LeafMaker.__repr__
