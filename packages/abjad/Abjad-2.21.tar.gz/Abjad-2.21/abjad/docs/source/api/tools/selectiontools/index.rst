selectiontools
==============

.. automodule:: abjad.tools.selectiontools

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
          subgraph cluster_selectiontools {
              graph [label=selectiontools];
              "abjad.tools.selectiontools.Descendants.Descendants" [color=black,
                  fontcolor=white,
                  group=1,
                  label=Descendants,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Lineage.Lineage" [color=black,
                  fontcolor=white,
                  group=1,
                  label=Lineage,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.LogicalTie.LogicalTie" [color=black,
                  fontcolor=white,
                  group=1,
                  label=LogicalTie,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Parentage.Parentage" [color=black,
                  fontcolor=white,
                  group=1,
                  label=Parentage,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" [color=black,
                  fontcolor=white,
                  group=1,
                  label=Selection,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.VerticalMoment.VerticalMoment" [color=black,
                  fontcolor=white,
                  group=1,
                  label=VerticalMoment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Descendants.Descendants";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Lineage.Lineage";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.LogicalTie.LogicalTie";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Parentage.Parentage";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.VerticalMoment.VerticalMoment";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.selectiontools.Selection.Selection";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Descendants
   Lineage
   LogicalTie
   Parentage
   Selection
   VerticalMoment

.. autosummary::
   :nosignatures:

   Descendants
   Lineage
   LogicalTie
   Parentage
   Selection
   VerticalMoment
