.. currentmodule:: abjad.tools.datastructuretools

TreeNode
========

.. autoclass:: TreeNode

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
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=3,
                  group=2,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TreeNode</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=4,
                  group=3,
                  label=ReSTAutosummaryItem,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=4,
                  group=3,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=4,
                  group=3,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=4,
                  group=3,
                  label=ReSTHeading,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule" [color=4,
                  group=3,
                  label=ReSTHorizontalRule,
                  shape=box];
              "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph" [color=4,
                  group=3,
                  label=ReSTParagraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem" [color=4,
                  group=3,
                  label=ReSTTOCItem,
                  shape=box];
          }
          subgraph cluster_graphtools {
              graph [label=graphtools];
              "abjad.tools.graphtools.GraphvizField.GraphvizField" [color=5,
                  group=4,
                  label=GraphvizField,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.graphtools.GraphvizGroup.GraphvizGroup" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.graphtools.GraphvizNode.GraphvizNode" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.graphtools.GraphvizTable.GraphvizTable" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.graphtools.GraphvizTableCell.GraphvizTableCell" [color=5,
                  group=4,
                  label=GraphvizTableCell,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=5,
                  group=4,
                  label=GraphvizTableHorizontalRule,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.graphtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=5,
                  group=4,
                  label=GraphvizTableVerticalRule,
                  shape=box];
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=6,
                  group=5,
                  label=QGridLeaf,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=7,
                  group=6,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=7,
                  group=6,
                  label=RhythmTreeLeaf,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDirective.ReSTDirective";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDocument.ReSTDocument";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizGroup.GraphvizGroup";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizNode.GraphvizNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizTable.GraphvizTable";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHeading.ReSTHeading";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizField.GraphvizField";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizTableCell.GraphvizTableCell";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.graphtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.TreeNode.TreeNode.depth
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.depthwise_inventory
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.graph_order
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.improper_parentage
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.name
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.parent
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.proper_parentage
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.root
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.__copy__
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.__eq__
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.__format__
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.__hash__
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.__ne__
      ~abjad.tools.datastructuretools.TreeNode.TreeNode.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.depth

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.depthwise_inventory

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.graph_order

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.improper_parentage

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.parent

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.proper_parentage

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.root

Read/write properties
---------------------

.. autoattribute:: abjad.tools.datastructuretools.TreeNode.TreeNode.name

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TreeNode.TreeNode.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeNode.TreeNode.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeNode.TreeNode.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeNode.TreeNode.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeNode.TreeNode.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeNode.TreeNode.__repr__
