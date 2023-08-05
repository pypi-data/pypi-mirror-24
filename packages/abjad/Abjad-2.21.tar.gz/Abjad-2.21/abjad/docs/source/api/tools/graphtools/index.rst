graphtools
==========

.. automodule:: abjad.tools.graphtools

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=3,
                  group=2,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_graphtools {
              graph [label=graphtools];
              "abjad.tools.graphtools.GraphvizEdge.GraphvizEdge" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizEdge,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizField.GraphvizField" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizField,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizGraph,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizGroup.GraphvizGroup" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizGroup,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizMixin,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizNode.GraphvizNode" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizNode,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizSubgraph,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizTable.GraphvizTable" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTable,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizTableCell.GraphvizTableCell" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableCell,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableHorizontalRule,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableRow,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableVerticalRule,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizEdge.GraphvizEdge";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizNode.GraphvizNode";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizGroup.GraphvizGroup";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizNode.GraphvizNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizTable.GraphvizTable";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizField.GraphvizField";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizTableCell.GraphvizTableCell";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Graphviz
--------

.. toctree::
   :hidden:

   GraphvizEdge
   GraphvizField
   GraphvizGraph
   GraphvizGroup
   GraphvizMixin
   GraphvizNode
   GraphvizSubgraph
   GraphvizTable
   GraphvizTableCell
   GraphvizTableHorizontalRule
   GraphvizTableRow
   GraphvizTableVerticalRule

.. autosummary::
   :nosignatures:

   GraphvizEdge
   GraphvizField
   GraphvizGraph
   GraphvizGroup
   GraphvizMixin
   GraphvizNode
   GraphvizSubgraph
   GraphvizTable
   GraphvizTableCell
   GraphvizTableHorizontalRule
   GraphvizTableRow
   GraphvizTableVerticalRule
