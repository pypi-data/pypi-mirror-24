durationtools
=============

.. automodule:: abjad.tools.durationtools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
          subgraph cluster_durationtools {
              graph [label=durationtools];
              "abjad.tools.durationtools.Duration.Duration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Duration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Multiplier.Multiplier" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Multiplier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Offset.Offset" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Offset,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Multiplier.Multiplier";
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Offset.Offset";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          subgraph cluster_quicktions {
              graph [label=quicktions];
              "quicktions.Fraction" [color=4,
                  group=3,
                  label=Fraction,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.durationtools.Duration.Duration";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "quicktions.Fraction";
          "quicktions.Fraction" -> "abjad.tools.durationtools.Duration.Duration";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Duration
   Multiplier
   Offset

.. autosummary::
   :nosignatures:

   Duration
   Multiplier
   Offset
