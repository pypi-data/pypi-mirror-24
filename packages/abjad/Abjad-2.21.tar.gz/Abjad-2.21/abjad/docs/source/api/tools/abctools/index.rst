abctools
========

.. automodule:: abjad.tools.abctools

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
          subgraph cluster_part {
              graph [label=part];
              "abjad.demos.part.PartCantusScoreTemplate.PartCantusScoreTemplate" [color=3,
                  group=20,
                  label=PartCantusScoreTemplate,
                  shape=box];
          }
          subgraph cluster_abctools {
              graph [label=abctools];
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=black,
                  fontcolor=white,
                  group=0,
                  label=AbjadObject,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=black,
                  fontcolor=white,
                  group=0,
                  label=AbjadValueObject,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abctools.ContextManager.ContextManager" [color=black,
                  fontcolor=white,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abctools.Parser.Parser" [color=black,
                  fontcolor=white,
                  group=0,
                  label=Parser,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.Parser.Parser";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=2,
                  group=1,
                  label=AbjadBookScript,
                  shape=box];
              "abjad.tools.abjadbooktools.CodeBlock.CodeBlock" [color=2,
                  group=1,
                  label=CodeBlock,
                  shape=box];
              "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier" [color=2,
                  group=1,
                  label=CodeBlockSpecifier,
                  shape=box];
              "abjad.tools.abjadbooktools.CodeOutputProxy.CodeOutputProxy" [color=2,
                  group=1,
                  label=CodeOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy" [color=2,
                  group=1,
                  label=GraphvizOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier" [color=2,
                  group=1,
                  label=ImageLayoutSpecifier,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" [color=2,
                  group=1,
                  label=ImageOutputProxy,
                  shape=oval,
                  style=bold];
              "abjad.tools.abjadbooktools.ImageRenderSpecifier.ImageRenderSpecifier" [color=2,
                  group=1,
                  label=ImageRenderSpecifier,
                  shape=box];
              "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler" [color=2,
                  group=1,
                  label=LaTeXDocumentHandler,
                  shape=box];
              "abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock" [color=2,
                  group=1,
                  label=LilyPondBlock,
                  shape=box];
              "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy" [color=2,
                  group=1,
                  label=LilyPondOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.RawLilyPondOutputProxy.RawLilyPondOutputProxy" [color=2,
                  group=1,
                  label=RawLilyPondOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler" [color=2,
                  group=1,
                  label=SphinxDocumentHandler,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy";
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy";
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.RawLilyPondOutputProxy.RawLilyPondOutputProxy";
          }
          subgraph cluster_agenttools {
              graph [label=agenttools];
              "abjad.tools.agenttools.InspectionAgent.InspectionAgent" [color=3,
                  group=2,
                  label=InspectionAgent,
                  shape=box];
              "abjad.tools.agenttools.IterationAgent.IterationAgent" [color=3,
                  group=2,
                  label=IterationAgent,
                  shape=box];
              "abjad.tools.agenttools.LabelAgent.LabelAgent" [color=3,
                  group=2,
                  label=LabelAgent,
                  shape=box];
              "abjad.tools.agenttools.MutationAgent.MutationAgent" [color=3,
                  group=2,
                  label=MutationAgent,
                  shape=box];
              "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent" [color=3,
                  group=2,
                  label=PersistenceAgent,
                  shape=box];
          }
          subgraph cluster_commandlinetools {
              graph [label=commandlinetools];
              "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript" [color=5,
                  group=4,
                  label=AbjDevScript,
                  shape=box];
              "abjad.tools.commandlinetools.BuildApiScript.BuildApiScript" [color=5,
                  group=4,
                  label=BuildApiScript,
                  shape=box];
              "abjad.tools.commandlinetools.CheckClassSections.CheckClassSections" [color=5,
                  group=4,
                  label=CheckClassSections,
                  shape=box];
              "abjad.tools.commandlinetools.CleanScript.CleanScript" [color=5,
                  group=4,
                  label=CleanScript,
                  shape=box];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" [color=5,
                  group=4,
                  label=CommandlineScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.commandlinetools.DoctestScript.DoctestScript" [color=5,
                  group=4,
                  label=DoctestScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript" [color=5,
                  group=4,
                  label=ManageBuildTargetScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript" [color=5,
                  group=4,
                  label=ManageMaterialScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript" [color=5,
                  group=4,
                  label=ManageScoreScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript" [color=5,
                  group=4,
                  label=ManageSegmentScript,
                  shape=box];
              "abjad.tools.commandlinetools.ReplaceScript.ReplaceScript" [color=5,
                  group=4,
                  label=ReplaceScript,
                  shape=box];
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" [color=5,
                  group=4,
                  label=ScorePackageScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.commandlinetools.StatsScript.StatsScript" [color=5,
                  group=4,
                  label=StatsScript,
                  shape=box];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.BuildApiScript.BuildApiScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.CheckClassSections.CheckClassSections";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.CleanScript.CleanScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.DoctestScript.DoctestScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.ReplaceScript.ReplaceScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.StatsScript.StatsScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple" [color=7,
                  group=6,
                  label=CyclicTuple,
                  shape=box];
              "abjad.tools.datastructuretools.Expression.Expression" [color=7,
                  group=6,
                  label=Expression,
                  shape=box];
              "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant" [color=7,
                  group=6,
                  label=OrdinalConstant,
                  shape=box];
              "abjad.tools.datastructuretools.Pattern.Pattern" [color=7,
                  group=6,
                  label=Pattern,
                  shape=box];
              "abjad.tools.datastructuretools.PatternList.PatternList" [color=7,
                  group=6,
                  label=PatternList,
                  shape=box];
              "abjad.tools.datastructuretools.Sequence.Sequence" [color=7,
                  group=6,
                  label=Sequence,
                  shape=box];
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=7,
                  group=6,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=7,
                  group=6,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=7,
                  group=6,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=7,
                  group=6,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=7,
                  group=6,
                  label=TypedFrozenset,
                  shape=box];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=7,
                  group=6,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=7,
                  group=6,
                  label=TypedOrderedDict,
                  shape=box];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=7,
                  group=6,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.datastructuretools.PatternList.PatternList";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.DocumentationManager.DocumentationManager" [color=8,
                  group=7,
                  label=DocumentationManager,
                  shape=box];
              "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph" [color=8,
                  group=7,
                  label=InheritanceGraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=8,
                  group=7,
                  label=ReSTAutodocDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=8,
                  group=7,
                  label=ReSTAutosummaryDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=8,
                  group=7,
                  label=ReSTAutosummaryItem,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=8,
                  group=7,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=8,
                  group=7,
                  label=ReSTDocument,
                  shape=box];
              "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective" [color=8,
                  group=7,
                  label=ReSTGraphvizDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=8,
                  group=7,
                  label=ReSTHeading,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule" [color=8,
                  group=7,
                  label=ReSTHorizontalRule,
                  shape=box];
              "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram" [color=8,
                  group=7,
                  label=ReSTInheritanceDiagram,
                  shape=box];
              "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective" [color=8,
                  group=7,
                  label=ReSTLineageDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective" [color=8,
                  group=7,
                  label=ReSTOnlyDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph" [color=8,
                  group=7,
                  label=ReSTParagraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=8,
                  group=7,
                  label=ReSTTOCDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem" [color=8,
                  group=7,
                  label=ReSTTOCItem,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective";
          }
          subgraph cluster_durationtools {
              graph [label=durationtools];
              "abjad.tools.durationtools.Duration.Duration" [color=9,
                  group=8,
                  label=Duration,
                  shape=box];
              "abjad.tools.durationtools.Multiplier.Multiplier" [color=9,
                  group=8,
                  label=Multiplier,
                  shape=box];
              "abjad.tools.durationtools.Offset.Offset" [color=9,
                  group=8,
                  label=Offset,
                  shape=box];
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Multiplier.Multiplier";
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Offset.Offset";
          }
          subgraph cluster_graphtools {
              graph [label=graphtools];
              "abjad.tools.graphtools.GraphvizEdge.GraphvizEdge" [color=1,
                  group=9,
                  label=GraphvizEdge,
                  shape=box];
              "abjad.tools.graphtools.GraphvizField.GraphvizField" [color=1,
                  group=9,
                  label=GraphvizField,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" [color=1,
                  group=9,
                  label=GraphvizGraph,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGroup.GraphvizGroup" [color=1,
                  group=9,
                  label=GraphvizGroup,
                  shape=box];
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" [color=1,
                  group=9,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.graphtools.GraphvizNode.GraphvizNode" [color=1,
                  group=9,
                  label=GraphvizNode,
                  shape=box];
              "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph" [color=1,
                  group=9,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTable.GraphvizTable" [color=1,
                  group=9,
                  label=GraphvizTable,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableCell.GraphvizTableCell" [color=1,
                  group=9,
                  label=GraphvizTableCell,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=1,
                  group=9,
                  label=GraphvizTableHorizontalRule,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow" [color=1,
                  group=9,
                  label=GraphvizTableRow,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=1,
                  group=9,
                  label=GraphvizTableVerticalRule,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizEdge.GraphvizEdge";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizNode.GraphvizNode";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.Accelerando.Accelerando" [color=2,
                  group=10,
                  label=Accelerando,
                  shape=box];
              "abjad.tools.indicatortools.Arpeggio.Arpeggio" [color=2,
                  group=10,
                  label=Arpeggio,
                  shape=box];
              "abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment" [color=2,
                  group=10,
                  label=ArrowLineSegment,
                  shape=box];
              "abjad.tools.indicatortools.Articulation.Articulation" [color=2,
                  group=10,
                  label=Articulation,
                  shape=box];
              "abjad.tools.indicatortools.BarLine.BarLine" [color=2,
                  group=10,
                  label=BarLine,
                  shape=box];
              "abjad.tools.indicatortools.BendAfter.BendAfter" [color=2,
                  group=10,
                  label=BendAfter,
                  shape=box];
              "abjad.tools.indicatortools.BowContactPoint.BowContactPoint" [color=2,
                  group=10,
                  label=BowContactPoint,
                  shape=box];
              "abjad.tools.indicatortools.BowMotionTechnique.BowMotionTechnique" [color=2,
                  group=10,
                  label=BowMotionTechnique,
                  shape=box];
              "abjad.tools.indicatortools.BowPressure.BowPressure" [color=2,
                  group=10,
                  label=BowPressure,
                  shape=box];
              "abjad.tools.indicatortools.BreathMark.BreathMark" [color=2,
                  group=10,
                  label=BreathMark,
                  shape=box];
              "abjad.tools.indicatortools.Clef.Clef" [color=2,
                  group=10,
                  label=Clef,
                  shape=box];
              "abjad.tools.indicatortools.ColorFingering.ColorFingering" [color=2,
                  group=10,
                  label=ColorFingering,
                  shape=box];
              "abjad.tools.indicatortools.Dynamic.Dynamic" [color=2,
                  group=10,
                  label=Dynamic,
                  shape=box];
              "abjad.tools.indicatortools.Fermata.Fermata" [color=2,
                  group=10,
                  label=Fermata,
                  shape=box];
              "abjad.tools.indicatortools.KeyCluster.KeyCluster" [color=2,
                  group=10,
                  label=KeyCluster,
                  shape=box];
              "abjad.tools.indicatortools.KeySignature.KeySignature" [color=2,
                  group=10,
                  label=KeySignature,
                  shape=box];
              "abjad.tools.indicatortools.LaissezVibrer.LaissezVibrer" [color=2,
                  group=10,
                  label=LaissezVibrer,
                  shape=box];
              "abjad.tools.indicatortools.LilyPondCommand.LilyPondCommand" [color=2,
                  group=10,
                  label=LilyPondCommand,
                  shape=box];
              "abjad.tools.indicatortools.LilyPondComment.LilyPondComment" [color=2,
                  group=10,
                  label=LilyPondComment,
                  shape=box];
              "abjad.tools.indicatortools.LilyPondLiteral.LilyPondLiteral" [color=2,
                  group=10,
                  label=LilyPondLiteral,
                  shape=box];
              "abjad.tools.indicatortools.LineSegment.LineSegment" [color=2,
                  group=10,
                  label=LineSegment,
                  shape=box];
              "abjad.tools.indicatortools.MetricModulation.MetricModulation" [color=2,
                  group=10,
                  label=MetricModulation,
                  shape=box];
              "abjad.tools.indicatortools.MetronomeMark.MetronomeMark" [color=2,
                  group=10,
                  label=MetronomeMark,
                  shape=box];
              "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList" [color=2,
                  group=10,
                  label=MetronomeMarkList,
                  shape=box];
              "abjad.tools.indicatortools.PageBreak.PageBreak" [color=2,
                  group=10,
                  label=PageBreak,
                  shape=box];
              "abjad.tools.indicatortools.RehearsalMark.RehearsalMark" [color=2,
                  group=10,
                  label=RehearsalMark,
                  shape=box];
              "abjad.tools.indicatortools.Repeat.Repeat" [color=2,
                  group=10,
                  label=Repeat,
                  shape=box];
              "abjad.tools.indicatortools.Ritardando.Ritardando" [color=2,
                  group=10,
                  label=Ritardando,
                  shape=box];
              "abjad.tools.indicatortools.Staccatissimo.Staccatissimo" [color=2,
                  group=10,
                  label=Staccatissimo,
                  shape=box];
              "abjad.tools.indicatortools.Staccato.Staccato" [color=2,
                  group=10,
                  label=Staccato,
                  shape=box];
              "abjad.tools.indicatortools.StaffChange.StaffChange" [color=2,
                  group=10,
                  label=StaffChange,
                  shape=box];
              "abjad.tools.indicatortools.StemTremolo.StemTremolo" [color=2,
                  group=10,
                  label=StemTremolo,
                  shape=box];
              "abjad.tools.indicatortools.StringContactPoint.StringContactPoint" [color=2,
                  group=10,
                  label=StringContactPoint,
                  shape=box];
              "abjad.tools.indicatortools.StringNumber.StringNumber" [color=2,
                  group=10,
                  label=StringNumber,
                  shape=box];
              "abjad.tools.indicatortools.SystemBreak.SystemBreak" [color=2,
                  group=10,
                  label=SystemBreak,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignature.TimeSignature" [color=2,
                  group=10,
                  label=TimeSignature,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList" [color=2,
                  group=10,
                  label=TimeSignatureList,
                  shape=box];
              "abjad.tools.indicatortools.Tremolo.Tremolo" [color=2,
                  group=10,
                  label=Tremolo,
                  shape=box];
              "abjad.tools.indicatortools.Tuning.Tuning" [color=2,
                  group=10,
                  label=Tuning,
                  shape=box];
              "abjad.tools.indicatortools.WoodwindFingering.WoodwindFingering" [color=2,
                  group=10,
                  label=WoodwindFingering,
                  shape=box];
              "abjad.tools.indicatortools.LineSegment.LineSegment" -> "abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment";
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.Accordion.Accordion" [color=3,
                  group=11,
                  label=Accordion,
                  shape=box];
              "abjad.tools.instrumenttools.AltoFlute.AltoFlute" [color=3,
                  group=11,
                  label=AltoFlute,
                  shape=box];
              "abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone" [color=3,
                  group=11,
                  label=AltoSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.AltoTrombone.AltoTrombone" [color=3,
                  group=11,
                  label=AltoTrombone,
                  shape=box];
              "abjad.tools.instrumenttools.AltoVoice.AltoVoice" [color=3,
                  group=11,
                  label=AltoVoice,
                  shape=box];
              "abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone" [color=3,
                  group=11,
                  label=BaritoneSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.BaritoneVoice.BaritoneVoice" [color=3,
                  group=11,
                  label=BaritoneVoice,
                  shape=box];
              "abjad.tools.instrumenttools.BassClarinet.BassClarinet" [color=3,
                  group=11,
                  label=BassClarinet,
                  shape=box];
              "abjad.tools.instrumenttools.BassFlute.BassFlute" [color=3,
                  group=11,
                  label=BassFlute,
                  shape=box];
              "abjad.tools.instrumenttools.BassSaxophone.BassSaxophone" [color=3,
                  group=11,
                  label=BassSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.BassTrombone.BassTrombone" [color=3,
                  group=11,
                  label=BassTrombone,
                  shape=box];
              "abjad.tools.instrumenttools.BassVoice.BassVoice" [color=3,
                  group=11,
                  label=BassVoice,
                  shape=box];
              "abjad.tools.instrumenttools.Bassoon.Bassoon" [color=3,
                  group=11,
                  label=Bassoon,
                  shape=box];
              "abjad.tools.instrumenttools.Cello.Cello" [color=3,
                  group=11,
                  label=Cello,
                  shape=box];
              "abjad.tools.instrumenttools.ClarinetInA.ClarinetInA" [color=3,
                  group=11,
                  label=ClarinetInA,
                  shape=box];
              "abjad.tools.instrumenttools.ClarinetInBFlat.ClarinetInBFlat" [color=3,
                  group=11,
                  label=ClarinetInBFlat,
                  shape=box];
              "abjad.tools.instrumenttools.ClarinetInEFlat.ClarinetInEFlat" [color=3,
                  group=11,
                  label=ClarinetInEFlat,
                  shape=box];
              "abjad.tools.instrumenttools.ClefList.ClefList" [color=3,
                  group=11,
                  label=ClefList,
                  shape=box];
              "abjad.tools.instrumenttools.Contrabass.Contrabass" [color=3,
                  group=11,
                  label=Contrabass,
                  shape=box];
              "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet" [color=3,
                  group=11,
                  label=ContrabassClarinet,
                  shape=box];
              "abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute" [color=3,
                  group=11,
                  label=ContrabassFlute,
                  shape=box];
              "abjad.tools.instrumenttools.ContrabassSaxophone.ContrabassSaxophone" [color=3,
                  group=11,
                  label=ContrabassSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.Contrabassoon.Contrabassoon" [color=3,
                  group=11,
                  label=Contrabassoon,
                  shape=box];
              "abjad.tools.instrumenttools.EnglishHorn.EnglishHorn" [color=3,
                  group=11,
                  label=EnglishHorn,
                  shape=box];
              "abjad.tools.instrumenttools.Flute.Flute" [color=3,
                  group=11,
                  label=Flute,
                  shape=box];
              "abjad.tools.instrumenttools.FrenchHorn.FrenchHorn" [color=3,
                  group=11,
                  label=FrenchHorn,
                  shape=box];
              "abjad.tools.instrumenttools.Glockenspiel.Glockenspiel" [color=3,
                  group=11,
                  label=Glockenspiel,
                  shape=box];
              "abjad.tools.instrumenttools.Guitar.Guitar" [color=3,
                  group=11,
                  label=Guitar,
                  shape=box];
              "abjad.tools.instrumenttools.Harp.Harp" [color=3,
                  group=11,
                  label=Harp,
                  shape=box];
              "abjad.tools.instrumenttools.Harpsichord.Harpsichord" [color=3,
                  group=11,
                  label=Harpsichord,
                  shape=box];
              "abjad.tools.instrumenttools.Instrument.Instrument" [color=3,
                  group=11,
                  label=Instrument,
                  shape=box];
              "abjad.tools.instrumenttools.InstrumentList.InstrumentList" [color=3,
                  group=11,
                  label=InstrumentList,
                  shape=box];
              "abjad.tools.instrumenttools.Marimba.Marimba" [color=3,
                  group=11,
                  label=Marimba,
                  shape=box];
              "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice" [color=3,
                  group=11,
                  label=MezzoSopranoVoice,
                  shape=box];
              "abjad.tools.instrumenttools.Oboe.Oboe" [color=3,
                  group=11,
                  label=Oboe,
                  shape=box];
              "abjad.tools.instrumenttools.Percussion.Percussion" [color=3,
                  group=11,
                  label=Percussion,
                  shape=box];
              "abjad.tools.instrumenttools.Performer.Performer" [color=3,
                  group=11,
                  label=Performer,
                  shape=box];
              "abjad.tools.instrumenttools.PerformerList.PerformerList" [color=3,
                  group=11,
                  label=PerformerList,
                  shape=box];
              "abjad.tools.instrumenttools.Piano.Piano" [color=3,
                  group=11,
                  label=Piano,
                  shape=box];
              "abjad.tools.instrumenttools.Piccolo.Piccolo" [color=3,
                  group=11,
                  label=Piccolo,
                  shape=box];
              "abjad.tools.instrumenttools.SopraninoSaxophone.SopraninoSaxophone" [color=3,
                  group=11,
                  label=SopraninoSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.SopranoSaxophone.SopranoSaxophone" [color=3,
                  group=11,
                  label=SopranoSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.SopranoVoice.SopranoVoice" [color=3,
                  group=11,
                  label=SopranoVoice,
                  shape=box];
              "abjad.tools.instrumenttools.TenorSaxophone.TenorSaxophone" [color=3,
                  group=11,
                  label=TenorSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.TenorTrombone.TenorTrombone" [color=3,
                  group=11,
                  label=TenorTrombone,
                  shape=box];
              "abjad.tools.instrumenttools.TenorVoice.TenorVoice" [color=3,
                  group=11,
                  label=TenorVoice,
                  shape=box];
              "abjad.tools.instrumenttools.Trumpet.Trumpet" [color=3,
                  group=11,
                  label=Trumpet,
                  shape=box];
              "abjad.tools.instrumenttools.Tuba.Tuba" [color=3,
                  group=11,
                  label=Tuba,
                  shape=box];
              "abjad.tools.instrumenttools.Vibraphone.Vibraphone" [color=3,
                  group=11,
                  label=Vibraphone,
                  shape=box];
              "abjad.tools.instrumenttools.Viola.Viola" [color=3,
                  group=11,
                  label=Viola,
                  shape=box];
              "abjad.tools.instrumenttools.Violin.Violin" [color=3,
                  group=11,
                  label=Violin,
                  shape=box];
              "abjad.tools.instrumenttools.Xylophone.Xylophone" [color=3,
                  group=11,
                  label=Xylophone,
                  shape=box];
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Accordion.Accordion";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoFlute.AltoFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoTrombone.AltoTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoVoice.AltoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BaritoneVoice.BaritoneVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassClarinet.BassClarinet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassFlute.BassFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassSaxophone.BassSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassTrombone.BassTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassVoice.BassVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Bassoon.Bassoon";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Cello.Cello";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInA.ClarinetInA";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInBFlat.ClarinetInBFlat";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInEFlat.ClarinetInEFlat";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Contrabass.Contrabass";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassSaxophone.ContrabassSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Contrabassoon.Contrabassoon";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.EnglishHorn.EnglishHorn";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Flute.Flute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.FrenchHorn.FrenchHorn";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Glockenspiel.Glockenspiel";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Guitar.Guitar";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Harp.Harp";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Harpsichord.Harpsichord";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Marimba.Marimba";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Oboe.Oboe";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Percussion.Percussion";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Piano.Piano";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Piccolo.Piccolo";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopraninoSaxophone.SopraninoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopranoSaxophone.SopranoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopranoVoice.SopranoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorSaxophone.TenorSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorTrombone.TenorTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorVoice.TenorVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Trumpet.Trumpet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Tuba.Tuba";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Vibraphone.Vibraphone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Viola.Viola";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Violin.Violin";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Xylophone.Xylophone";
          }
          subgraph cluster_lilypondfiletools {
              graph [label=lilypondfiletools];
              "abjad.tools.lilypondfiletools.Block.Block" [color=5,
                  group=13,
                  label=Block,
                  shape=box];
              "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock" [color=5,
                  group=13,
                  label=ContextBlock,
                  shape=box];
              "abjad.tools.lilypondfiletools.DateTimeToken.DateTimeToken" [color=5,
                  group=13,
                  label=DateTimeToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondDimension.LilyPondDimension" [color=5,
                  group=13,
                  label=LilyPondDimension,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile" [color=5,
                  group=13,
                  label=LilyPondFile,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondLanguageToken.LilyPondLanguageToken" [color=5,
                  group=13,
                  label=LilyPondLanguageToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken" [color=5,
                  group=13,
                  label=LilyPondVersionToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.PackageGitCommitToken.PackageGitCommitToken" [color=5,
                  group=13,
                  label=PackageGitCommitToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.Block.Block" -> "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock";
          }
          subgraph cluster_lilypondnametools {
              graph [label=lilypondnametools];
              "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext" [color=6,
                  group=14,
                  label=LilyPondContext,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting" [color=6,
                  group=14,
                  label=LilyPondContextSetting,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver" [color=6,
                  group=14,
                  label=LilyPondEngraver,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob" [color=6,
                  group=14,
                  label=LilyPondGrob,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface" [color=6,
                  group=14,
                  label=LilyPondGrobInterface,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride" [color=6,
                  group=14,
                  label=LilyPondGrobOverride,
                  shape=box];
          }
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic" [color=7,
                  group=15,
                  label=ContextSpeccedMusic,
                  shape=box];
              "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy" [color=7,
                  group=15,
                  label=GuileProxy,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondDuration.LilyPondDuration" [color=7,
                  group=15,
                  label=LilyPondDuration,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondEvent.LilyPondEvent" [color=7,
                  group=15,
                  label=LilyPondEvent,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondFraction.LilyPondFraction" [color=7,
                  group=15,
                  label=LilyPondFraction,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondGrammarGenerator.LilyPondGrammarGenerator" [color=7,
                  group=15,
                  label=LilyPondGrammarGenerator,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition" [color=7,
                  group=15,
                  label=LilyPondLexicalDefinition,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser" [color=7,
                  group=15,
                  label=LilyPondParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition.LilyPondSyntacticalDefinition" [color=7,
                  group=15,
                  label=LilyPondSyntacticalDefinition,
                  shape=box];
              "abjad.tools.lilypondparsertools.Music.Music" [color=7,
                  group=15,
                  label=Music,
                  shape=oval,
                  style=bold];
              "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser" [color=7,
                  group=15,
                  label=ReducedLyParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser" [color=7,
                  group=15,
                  label=SchemeParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.SequentialMusic.SequentialMusic" [color=7,
                  group=15,
                  label=SequentialMusic,
                  shape=box];
              "abjad.tools.lilypondparsertools.SimultaneousMusic.SimultaneousMusic" [color=7,
                  group=15,
                  label=SimultaneousMusic,
                  shape=oval,
                  style=bold];
              "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode" [color=7,
                  group=15,
                  label=SyntaxNode,
                  shape=box];
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic";
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.SequentialMusic.SequentialMusic";
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.SimultaneousMusic.SimultaneousMusic";
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.Markup.Markup" [color=9,
                  group=17,
                  label=Markup,
                  shape=box];
              "abjad.tools.markuptools.MarkupCommand.MarkupCommand" [color=9,
                  group=17,
                  label=MarkupCommand,
                  shape=box];
              "abjad.tools.markuptools.MarkupList.MarkupList" [color=9,
                  group=17,
                  label=MarkupList,
                  shape=box];
              "abjad.tools.markuptools.Postscript.Postscript" [color=9,
                  group=17,
                  label=Postscript,
                  shape=box];
              "abjad.tools.markuptools.PostscriptOperator.PostscriptOperator" [color=9,
                  group=17,
                  label=PostscriptOperator,
                  shape=box];
          }
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=1,
                  group=18,
                  label=BoundedObject,
                  shape=box];
              "abjad.tools.mathtools.Enumerator.Enumerator" [color=1,
                  group=18,
                  label=Enumerator,
                  shape=box];
              "abjad.tools.mathtools.Infinity.Infinity" [color=1,
                  group=18,
                  label=Infinity,
                  shape=box];
              "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity" [color=1,
                  group=18,
                  label=NegativeInfinity,
                  shape=box];
              "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" [color=1,
                  group=18,
                  label=NonreducedFraction,
                  shape=box];
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" [color=1,
                  group=18,
                  label=NonreducedRatio,
                  shape=box];
              "abjad.tools.mathtools.Ratio.Ratio" [color=1,
                  group=18,
                  label=Ratio,
                  shape=box];
              "abjad.tools.mathtools.Infinity.Infinity" -> "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity";
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" -> "abjad.tools.mathtools.Ratio.Ratio";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.Meter.Meter" [color=2,
                  group=19,
                  label=Meter,
                  shape=box];
              "abjad.tools.metertools.MeterFittingSession.MeterFittingSession" [color=2,
                  group=19,
                  label=MeterFittingSession,
                  shape=box];
              "abjad.tools.metertools.MeterList.MeterList" [color=2,
                  group=19,
                  label=MeterList,
                  shape=box];
              "abjad.tools.metertools.MeterManager.MeterManager" [color=2,
                  group=19,
                  label=MeterManager,
                  shape=box];
              "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel" [color=2,
                  group=19,
                  label=MetricAccentKernel,
                  shape=box];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=2,
                  group=19,
                  label=OffsetCounter,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.Accidental.Accidental" [color=4,
                  group=21,
                  label=Accidental,
                  shape=box];
              "abjad.tools.pitchtools.ColorMap.ColorMap" [color=4,
                  group=21,
                  label=ColorMap,
                  shape=box];
              "abjad.tools.pitchtools.CompoundOperator.CompoundOperator" [color=4,
                  group=21,
                  label=CompoundOperator,
                  shape=box];
              "abjad.tools.pitchtools.Duplication.Duplication" [color=4,
                  group=21,
                  label=Duplication,
                  shape=box];
              "abjad.tools.pitchtools.Interval.Interval" [color=4,
                  group=21,
                  label=Interval,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" [color=4,
                  group=21,
                  label=IntervalClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=4,
                  group=21,
                  label=IntervalClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=4,
                  group=21,
                  label=IntervalClassSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=4,
                  group=21,
                  label=IntervalClassVector,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=4,
                  group=21,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=4,
                  group=21,
                  label=IntervalSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=4,
                  group=21,
                  label=IntervalVector,
                  shape=box];
              "abjad.tools.pitchtools.Inversion.Inversion" [color=4,
                  group=21,
                  label=Inversion,
                  shape=box];
              "abjad.tools.pitchtools.Multiplication.Multiplication" [color=4,
                  group=21,
                  label=Multiplication,
                  shape=box];
              "abjad.tools.pitchtools.NamedInterval.NamedInterval" [color=4,
                  group=21,
                  label=NamedInterval,
                  shape=box];
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" [color=4,
                  group=21,
                  label=NamedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass" [color=4,
                  group=21,
                  label=NamedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NamedPitch.NamedPitch" [color=4,
                  group=21,
                  label=NamedPitch,
                  shape=box];
              "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass" [color=4,
                  group=21,
                  label=NamedPitchClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedInterval.NumberedInterval" [color=4,
                  group=21,
                  label=NumberedInterval,
                  shape=box];
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" [color=4,
                  group=21,
                  label=NumberedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass" [color=4,
                  group=21,
                  label=NumberedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitch.NumberedPitch" [color=4,
                  group=21,
                  label=NumberedPitch,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass" [color=4,
                  group=21,
                  label=NumberedPitchClass,
                  shape=box];
              "abjad.tools.pitchtools.Octave.Octave" [color=4,
                  group=21,
                  label=Octave,
                  shape=box];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=4,
                  group=21,
                  label=Pitch,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.PitchClass.PitchClass" [color=4,
                  group=21,
                  label=PitchClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=4,
                  group=21,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=4,
                  group=21,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=4,
                  group=21,
                  label=PitchClassVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchRange.PitchRange" [color=4,
                  group=21,
                  label=PitchRange,
                  shape=box];
              "abjad.tools.pitchtools.PitchRangeList.PitchRangeList" [color=4,
                  group=21,
                  label=PitchRangeList,
                  shape=box];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=4,
                  group=21,
                  label=PitchSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=4,
                  group=21,
                  label=PitchSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=4,
                  group=21,
                  label=PitchVector,
                  shape=box];
              "abjad.tools.pitchtools.Registration.Registration" [color=4,
                  group=21,
                  label=Registration,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent" [color=4,
                  group=21,
                  label=RegistrationComponent,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationList.RegistrationList" [color=4,
                  group=21,
                  label=RegistrationList,
                  shape=box];
              "abjad.tools.pitchtools.Retrograde.Retrograde" [color=4,
                  group=21,
                  label=Retrograde,
                  shape=box];
              "abjad.tools.pitchtools.Rotation.Rotation" [color=4,
                  group=21,
                  label=Rotation,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=21,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=21,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.SetClass.SetClass" [color=4,
                  group=21,
                  label=SetClass,
                  shape=box];
              "abjad.tools.pitchtools.StaffPosition.StaffPosition" [color=4,
                  group=21,
                  label=StaffPosition,
                  shape=box];
              "abjad.tools.pitchtools.Transposition.Transposition" [color=4,
                  group=21,
                  label=Transposition,
                  shape=box];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=4,
                  group=21,
                  label=TwelveToneRow,
                  shape=box];
              "abjad.tools.pitchtools.Vector.Vector" [color=4,
                  group=21,
                  label=Vector,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NamedInterval.NamedInterval";
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NumberedInterval.NumberedInterval";
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass";
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass";
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" -> "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass";
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" -> "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass";
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NamedPitch.NamedPitch";
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NumberedPitch.NumberedPitch";
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass";
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass";
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalSegment.IntervalSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchSegment.PitchSegment";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalSet.IntervalSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchClassSet.PitchClassSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchSet.PitchSet";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalVector.IntervalVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchClassVector.PitchClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchVector.PitchVector";
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" [color=5,
                  group=22,
                  label=AttackPointOptimizer,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema" [color=5,
                  group=22,
                  label=BeatwiseQSchema,
                  shape=box];
              "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem" [color=5,
                  group=22,
                  label=BeatwiseQSchemaItem,
                  shape=box];
              "abjad.tools.quantizationtools.BeatwiseQTarget.BeatwiseQTarget" [color=5,
                  group=22,
                  label=BeatwiseQTarget,
                  shape=box];
              "abjad.tools.quantizationtools.CollapsingGraceHandler.CollapsingGraceHandler" [color=5,
                  group=22,
                  label=CollapsingGraceHandler,
                  shape=box];
              "abjad.tools.quantizationtools.ConcatenatingGraceHandler.ConcatenatingGraceHandler" [color=5,
                  group=22,
                  label=ConcatenatingGraceHandler,
                  shape=box];
              "abjad.tools.quantizationtools.DiscardingGraceHandler.DiscardingGraceHandler" [color=5,
                  group=22,
                  label=DiscardingGraceHandler,
                  shape=box];
              "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic" [color=5,
                  group=22,
                  label=DistanceHeuristic,
                  shape=box];
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" [color=5,
                  group=22,
                  label=GraceHandler,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.Heuristic.Heuristic" [color=5,
                  group=22,
                  label=Heuristic,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.JobHandler.JobHandler" [color=5,
                  group=22,
                  label=JobHandler,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer" [color=5,
                  group=22,
                  label=MeasurewiseAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema" [color=5,
                  group=22,
                  label=MeasurewiseQSchema,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem" [color=5,
                  group=22,
                  label=MeasurewiseQSchemaItem,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget" [color=5,
                  group=22,
                  label=MeasurewiseQTarget,
                  shape=box];
              "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer" [color=5,
                  group=22,
                  label=NaiveAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer" [color=5,
                  group=22,
                  label=NullAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler" [color=5,
                  group=22,
                  label=ParallelJobHandler,
                  shape=box];
              "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent" [color=5,
                  group=22,
                  label=PitchedQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.QEvent.QEvent" [color=5,
                  group=22,
                  label=QEvent,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QEventProxy.QEventProxy" [color=5,
                  group=22,
                  label=QEventProxy,
                  shape=box];
              "abjad.tools.quantizationtools.QEventSequence.QEventSequence" [color=5,
                  group=22,
                  label=QEventSequence,
                  shape=box];
              "abjad.tools.quantizationtools.QGrid.QGrid" [color=5,
                  group=22,
                  label=QGrid,
                  shape=box];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=5,
                  group=22,
                  label=QGridContainer,
                  shape=box];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=5,
                  group=22,
                  label=QGridLeaf,
                  shape=box];
              "abjad.tools.quantizationtools.QSchema.QSchema" [color=5,
                  group=22,
                  label=QSchema,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" [color=5,
                  group=22,
                  label=QSchemaItem,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QTarget.QTarget" [color=5,
                  group=22,
                  label=QTarget,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QTargetBeat.QTargetBeat" [color=5,
                  group=22,
                  label=QTargetBeat,
                  shape=box];
              "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure" [color=5,
                  group=22,
                  label=QTargetMeasure,
                  shape=box];
              "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob" [color=5,
                  group=22,
                  label=QuantizationJob,
                  shape=box];
              "abjad.tools.quantizationtools.Quantizer.Quantizer" [color=5,
                  group=22,
                  label=Quantizer,
                  shape=box];
              "abjad.tools.quantizationtools.SearchTree.SearchTree" [color=5,
                  group=22,
                  label=SearchTree,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler" [color=5,
                  group=22,
                  label=SerialJobHandler,
                  shape=box];
              "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent" [color=5,
                  group=22,
                  label=SilentQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent" [color=5,
                  group=22,
                  label=TerminalQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree" [color=5,
                  group=22,
                  label=UnweightedSearchTree,
                  shape=box];
              "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree" [color=5,
                  group=22,
                  label=WeightedSearchTree,
                  shape=box];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer";
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer";
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer";
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" -> "abjad.tools.quantizationtools.CollapsingGraceHandler.CollapsingGraceHandler";
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" -> "abjad.tools.quantizationtools.ConcatenatingGraceHandler.ConcatenatingGraceHandler";
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" -> "abjad.tools.quantizationtools.DiscardingGraceHandler.DiscardingGraceHandler";
              "abjad.tools.quantizationtools.Heuristic.Heuristic" -> "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic";
              "abjad.tools.quantizationtools.JobHandler.JobHandler" -> "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler";
              "abjad.tools.quantizationtools.JobHandler.JobHandler" -> "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent";
              "abjad.tools.quantizationtools.QSchema.QSchema" -> "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema";
              "abjad.tools.quantizationtools.QSchema.QSchema" -> "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema";
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" -> "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem";
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" -> "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem";
              "abjad.tools.quantizationtools.QTarget.QTarget" -> "abjad.tools.quantizationtools.BeatwiseQTarget.BeatwiseQTarget";
              "abjad.tools.quantizationtools.QTarget.QTarget" -> "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget";
              "abjad.tools.quantizationtools.SearchTree.SearchTree" -> "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree";
              "abjad.tools.quantizationtools.SearchTree.SearchTree" -> "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker" [color=6,
                  group=23,
                  label=AccelerandoRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier" [color=6,
                  group=23,
                  label=BeamSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.BurnishSpecifier.BurnishSpecifier" [color=6,
                  group=23,
                  label=BurnishSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier" [color=6,
                  group=23,
                  label=DurationSpellingSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker" [color=6,
                  group=23,
                  label=EvenDivisionRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker" [color=6,
                  group=23,
                  label=EvenRunRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.InciseSpecifier.InciseSpecifier" [color=6,
                  group=23,
                  label=InciseSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker" [color=6,
                  group=23,
                  label=IncisedRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.InterpolationSpecifier.InterpolationSpecifier" [color=6,
                  group=23,
                  label=InterpolationSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker" [color=6,
                  group=23,
                  label=NoteRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=6,
                  group=23,
                  label=PartitionTable,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=6,
                  group=23,
                  label=RhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=6,
                  group=23,
                  label=RotationCounter,
                  shape=box];
              "abjad.tools.rhythmmakertools.SilenceMask.SilenceMask" [color=6,
                  group=23,
                  label=SilenceMask,
                  shape=box];
              "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker" [color=6,
                  group=23,
                  label=SkipRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.SustainMask.SustainMask" [color=6,
                  group=23,
                  label=SustainMask,
                  shape=box];
              "abjad.tools.rhythmmakertools.Talea.Talea" [color=6,
                  group=23,
                  label=Talea,
                  shape=box];
              "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker" [color=6,
                  group=23,
                  label=TaleaRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TieSpecifier.TieSpecifier" [color=6,
                  group=23,
                  label=TieSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker" [color=6,
                  group=23,
                  label=TupletRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier" [color=6,
                  group=23,
                  label=TupletSpellingSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker";
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=7,
                  group=24,
                  label=RhythmTreeContainer,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=7,
                  group=24,
                  label=RhythmTreeLeaf,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=7,
                  group=24,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser" [color=7,
                  group=24,
                  label=RhythmTreeParser,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          }
          subgraph cluster_schemetools {
              graph [label=schemetools];
              "abjad.tools.schemetools.Scheme.Scheme" [color=8,
                  group=25,
                  label=Scheme,
                  shape=box];
              "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList" [color=8,
                  group=25,
                  label=SchemeAssociativeList,
                  shape=box];
              "abjad.tools.schemetools.SchemeColor.SchemeColor" [color=8,
                  group=25,
                  label=SchemeColor,
                  shape=box];
              "abjad.tools.schemetools.SchemeMoment.SchemeMoment" [color=8,
                  group=25,
                  label=SchemeMoment,
                  shape=box];
              "abjad.tools.schemetools.SchemePair.SchemePair" [color=8,
                  group=25,
                  label=SchemePair,
                  shape=box];
              "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol" [color=8,
                  group=25,
                  label=SchemeSymbol,
                  shape=box];
              "abjad.tools.schemetools.SchemeVector.SchemeVector" [color=8,
                  group=25,
                  label=SchemeVector,
                  shape=box];
              "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant" [color=8,
                  group=25,
                  label=SchemeVectorConstant,
                  shape=box];
              "abjad.tools.schemetools.SpacingVector.SpacingVector" [color=8,
                  group=25,
                  label=SpacingVector,
                  shape=box];
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeColor.SchemeColor";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeMoment.SchemeMoment";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemePair.SchemePair";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVector.SchemeVector";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant";
              "abjad.tools.schemetools.SchemeVector.SchemeVector" -> "abjad.tools.schemetools.SpacingVector.SpacingVector";
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer" [color=9,
                  group=26,
                  label=AcciaccaturaContainer,
                  shape=box];
              "abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer" [color=9,
                  group=26,
                  label=AfterGraceContainer,
                  shape=box];
              "abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer" [color=9,
                  group=26,
                  label=AppoggiaturaContainer,
                  shape=box];
              "abjad.tools.scoretools.Chord.Chord" [color=9,
                  group=26,
                  label=Chord,
                  shape=box];
              "abjad.tools.scoretools.Cluster.Cluster" [color=9,
                  group=26,
                  label=Cluster,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" [color=9,
                  group=26,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=9,
                  group=26,
                  label=Container,
                  shape=box];
              "abjad.tools.scoretools.Context.Context" [color=9,
                  group=26,
                  label=Context,
                  shape=box];
              "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=9,
                  group=26,
                  label=DrumNoteHead,
                  shape=box];
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=9,
                  group=26,
                  label=GraceContainer,
                  shape=box];
              "abjad.tools.scoretools.Leaf.Leaf" [color=9,
                  group=26,
                  label=Leaf,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.LeafMaker.LeafMaker" [color=9,
                  group=26,
                  label=LeafMaker,
                  shape=box];
              "abjad.tools.scoretools.Measure.Measure" [color=9,
                  group=26,
                  label=Measure,
                  shape=box];
              "abjad.tools.scoretools.MeasureMaker.MeasureMaker" [color=9,
                  group=26,
                  label=MeasureMaker,
                  shape=box];
              "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest" [color=9,
                  group=26,
                  label=MultimeasureRest,
                  shape=box];
              "abjad.tools.scoretools.Note.Note" [color=9,
                  group=26,
                  label=Note,
                  shape=box];
              "abjad.tools.scoretools.NoteHead.NoteHead" [color=9,
                  group=26,
                  label=NoteHead,
                  shape=box];
              "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=9,
                  group=26,
                  label=NoteHeadList,
                  shape=box];
              "abjad.tools.scoretools.NoteMaker.NoteMaker" [color=9,
                  group=26,
                  label=NoteMaker,
                  shape=box];
              "abjad.tools.scoretools.Rest.Rest" [color=9,
                  group=26,
                  label=Rest,
                  shape=box];
              "abjad.tools.scoretools.Score.Score" [color=9,
                  group=26,
                  label=Score,
                  shape=box];
              "abjad.tools.scoretools.Skip.Skip" [color=9,
                  group=26,
                  label=Skip,
                  shape=box];
              "abjad.tools.scoretools.Staff.Staff" [color=9,
                  group=26,
                  label=Staff,
                  shape=box];
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=9,
                  group=26,
                  label=StaffGroup,
                  shape=box];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=9,
                  group=26,
                  label=Tuplet,
                  shape=box];
              "abjad.tools.scoretools.Voice.Voice" [color=9,
                  group=26,
                  label=Voice,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Cluster.Cluster";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.GraceContainer.GraceContainer";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Measure.Measure";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Tuplet.Tuplet";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Score.Score";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Staff.Staff";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.StaffGroup.StaffGroup";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Voice.Voice";
              "abjad.tools.scoretools.GraceContainer.GraceContainer" -> "abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer";
              "abjad.tools.scoretools.GraceContainer.GraceContainer" -> "abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Chord.Chord";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Note.Note";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Rest.Rest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Skip.Skip";
              "abjad.tools.scoretools.NoteHead.NoteHead" -> "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead";
          }
          subgraph cluster_selectortools {
              graph [label=selectortools];
              "abjad.tools.selectortools.ContiguitySelectorCallback.ContiguitySelectorCallback" [color=1,
                  group=27,
                  label=ContiguitySelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.CountsSelectorCallback.CountsSelectorCallback" [color=1,
                  group=27,
                  label=CountsSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.DurationInequality.DurationInequality" [color=1,
                  group=27,
                  label=DurationInequality,
                  shape=box];
              "abjad.tools.selectortools.DurationSelectorCallback.DurationSelectorCallback" [color=1,
                  group=27,
                  label=DurationSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.ExtraLeafSelectorCallback.ExtraLeafSelectorCallback" [color=1,
                  group=27,
                  label=ExtraLeafSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.FlattenSelectorCallback.FlattenSelectorCallback" [color=1,
                  group=27,
                  label=FlattenSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.GroupByPitchCallback.GroupByPitchCallback" [color=1,
                  group=27,
                  label=GroupByPitchCallback,
                  shape=box];
              "abjad.tools.selectortools.Inequality.Inequality" [color=1,
                  group=27,
                  label=Inequality,
                  shape=oval,
                  style=bold];
              "abjad.tools.selectortools.ItemSelectorCallback.ItemSelectorCallback" [color=1,
                  group=27,
                  label=ItemSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.LengthInequality.LengthInequality" [color=1,
                  group=27,
                  label=LengthInequality,
                  shape=box];
              "abjad.tools.selectortools.LengthSelectorCallback.LengthSelectorCallback" [color=1,
                  group=27,
                  label=LengthSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.LogicalMeasureSelectorCallback.LogicalMeasureSelectorCallback" [color=1,
                  group=27,
                  label=LogicalMeasureSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.LogicalTieSelectorCallback.LogicalTieSelectorCallback" [color=1,
                  group=27,
                  label=LogicalTieSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.PartitionByRatioCallback.PartitionByRatioCallback" [color=1,
                  group=27,
                  label=PartitionByRatioCallback,
                  shape=box];
              "abjad.tools.selectortools.PatternedSelectorCallback.PatternedSelectorCallback" [color=1,
                  group=27,
                  label=PatternedSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.PitchSelectorCallback.PitchSelectorCallback" [color=1,
                  group=27,
                  label=PitchSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.PrototypeSelectorCallback.PrototypeSelectorCallback" [color=1,
                  group=27,
                  label=PrototypeSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.RunSelectorCallback.RunSelectorCallback" [color=1,
                  group=27,
                  label=RunSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.Selector.Selector" [color=1,
                  group=27,
                  label=Selector,
                  shape=box];
              "abjad.tools.selectortools.SliceSelectorCallback.SliceSelectorCallback" [color=1,
                  group=27,
                  label=SliceSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.WrapSelectionCallback.WrapSelectionCallback" [color=1,
                  group=27,
                  label=WrapSelectionCallback,
                  shape=box];
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.DurationInequality.DurationInequality";
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.LengthInequality.LengthInequality";
          }
          subgraph cluster_spannertools {
              graph [label=spannertools];
              "abjad.tools.spannertools.Beam.Beam" [color=2,
                  group=28,
                  label=Beam,
                  shape=box];
              "abjad.tools.spannertools.BowContactSpanner.BowContactSpanner" [color=2,
                  group=28,
                  label=BowContactSpanner,
                  shape=box];
              "abjad.tools.spannertools.ClefSpanner.ClefSpanner" [color=2,
                  group=28,
                  label=ClefSpanner,
                  shape=box];
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" [color=2,
                  group=28,
                  label=ComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner" [color=2,
                  group=28,
                  label=ComplexTrillSpanner,
                  shape=box];
              "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam" [color=2,
                  group=28,
                  label=DuratedComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam" [color=2,
                  group=28,
                  label=GeneralizedBeam,
                  shape=box];
              "abjad.tools.spannertools.Glissando.Glissando" [color=2,
                  group=28,
                  label=Glissando,
                  shape=box];
              "abjad.tools.spannertools.Hairpin.Hairpin" [color=2,
                  group=28,
                  label=Hairpin,
                  shape=box];
              "abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner" [color=2,
                  group=28,
                  label=HiddenStaffSpanner,
                  shape=box];
              "abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner" [color=2,
                  group=28,
                  label=HorizontalBracketSpanner,
                  shape=box];
              "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam" [color=2,
                  group=28,
                  label=MeasuredComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.MetronomeMarkSpanner.MetronomeMarkSpanner" [color=2,
                  group=28,
                  label=MetronomeMarkSpanner,
                  shape=box];
              "abjad.tools.spannertools.MultipartBeam.MultipartBeam" [color=2,
                  group=28,
                  label=MultipartBeam,
                  shape=box];
              "abjad.tools.spannertools.OctavationSpanner.OctavationSpanner" [color=2,
                  group=28,
                  label=OctavationSpanner,
                  shape=box];
              "abjad.tools.spannertools.PhrasingSlur.PhrasingSlur" [color=2,
                  group=28,
                  label=PhrasingSlur,
                  shape=box];
              "abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner" [color=2,
                  group=28,
                  label=PianoPedalSpanner,
                  shape=box];
              "abjad.tools.spannertools.Slur.Slur" [color=2,
                  group=28,
                  label=Slur,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" [color=2,
                  group=28,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner" [color=2,
                  group=28,
                  label=StaffLinesSpanner,
                  shape=box];
              "abjad.tools.spannertools.StemTremoloSpanner.StemTremoloSpanner" [color=2,
                  group=28,
                  label=StemTremoloSpanner,
                  shape=box];
              "abjad.tools.spannertools.TextSpanner.TextSpanner" [color=2,
                  group=28,
                  label=TextSpanner,
                  shape=box];
              "abjad.tools.spannertools.Tie.Tie" [color=2,
                  group=28,
                  label=Tie,
                  shape=box];
              "abjad.tools.spannertools.TrillSpanner.TrillSpanner" [color=2,
                  group=28,
                  label=TrillSpanner,
                  shape=box];
              "abjad.tools.spannertools.Beam.Beam" -> "abjad.tools.spannertools.ComplexBeam.ComplexBeam";
              "abjad.tools.spannertools.Beam.Beam" -> "abjad.tools.spannertools.MultipartBeam.MultipartBeam";
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" -> "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam";
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" -> "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Beam.Beam";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.BowContactSpanner.BowContactSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.ClefSpanner.ClefSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Glissando.Glissando";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Hairpin.Hairpin";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.MetronomeMarkSpanner.MetronomeMarkSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.OctavationSpanner.OctavationSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.PhrasingSlur.PhrasingSlur";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Slur.Slur";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.StemTremoloSpanner.StemTremoloSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.TextSpanner.TextSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Tie.Tie";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.TrillSpanner.TrillSpanner";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration" [color=3,
                  group=29,
                  label=AbjadConfiguration,
                  shape=box];
              "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker" [color=3,
                  group=29,
                  label=BenchmarkScoreMaker,
                  shape=box];
              "abjad.tools.systemtools.Configuration.Configuration" [color=3,
                  group=29,
                  label=Configuration,
                  shape=oval,
                  style=bold];
              "abjad.tools.systemtools.FilesystemState.FilesystemState" [color=3,
                  group=29,
                  label=FilesystemState,
                  shape=box];
              "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate" [color=3,
                  group=29,
                  label=ForbidUpdate,
                  shape=box];
              "abjad.tools.systemtools.FormatSpecification.FormatSpecification" [color=3,
                  group=29,
                  label=FormatSpecification,
                  shape=box];
              "abjad.tools.systemtools.IOManager.IOManager" [color=3,
                  group=29,
                  label=IOManager,
                  shape=box];
              "abjad.tools.systemtools.ImportManager.ImportManager" [color=3,
                  group=29,
                  label=ImportManager,
                  shape=box];
              "abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper" [color=3,
                  group=29,
                  label=IndicatorWrapper,
                  shape=box];
              "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle" [color=3,
                  group=29,
                  label=LilyPondFormatBundle,
                  shape=box];
              "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager" [color=3,
                  group=29,
                  label=LilyPondFormatManager,
                  shape=box];
              "abjad.tools.systemtools.NullContextManager.NullContextManager" [color=3,
                  group=29,
                  label=NullContextManager,
                  shape=box];
              "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator" [color=3,
                  group=29,
                  label=ProgressIndicator,
                  shape=box];
              "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams" [color=3,
                  group=29,
                  label=RedirectedStreams,
                  shape=box];
              "abjad.tools.systemtools.Signature.Signature" [color=3,
                  group=29,
                  label=Signature,
                  shape=box];
              "abjad.tools.systemtools.SlotContributions.SlotContributions" [color=3,
                  group=29,
                  label=SlotContributions,
                  shape=box];
              "abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent" [color=3,
                  group=29,
                  label=StorageFormatAgent,
                  shape=box];
              "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification" [color=3,
                  group=29,
                  label=StorageFormatSpecification,
                  shape=box];
              "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory" [color=3,
                  group=29,
                  label=TemporaryDirectory,
                  shape=box];
              "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange" [color=3,
                  group=29,
                  label=TemporaryDirectoryChange,
                  shape=box];
              "abjad.tools.systemtools.TestManager.TestManager" [color=3,
                  group=29,
                  label=TestManager,
                  shape=box];
              "abjad.tools.systemtools.Timer.Timer" [color=3,
                  group=29,
                  label=Timer,
                  shape=box];
              "abjad.tools.systemtools.UpdateManager.UpdateManager" [color=3,
                  group=29,
                  label=UpdateManager,
                  shape=box];
              "abjad.tools.systemtools.WellformednessManager.WellformednessManager" [color=3,
                  group=29,
                  label=WellformednessManager,
                  shape=box];
              "abjad.tools.systemtools.Configuration.Configuration" -> "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration";
          }
          subgraph cluster_templatetools {
              graph [label=templatetools];
              "abjad.tools.templatetools.GroupedRhythmicStavesScoreTemplate.GroupedRhythmicStavesScoreTemplate" [color=4,
                  group=30,
                  label=GroupedRhythmicStavesScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate" [color=4,
                  group=30,
                  label=GroupedStavesScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate" [color=4,
                  group=30,
                  label=StringOrchestraScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.StringQuartetScoreTemplate.StringQuartetScoreTemplate" [color=4,
                  group=30,
                  label=StringQuartetScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.TwoStaffPianoScoreTemplate.TwoStaffPianoScoreTemplate" [color=4,
                  group=30,
                  label=TwoStaffPianoScoreTemplate,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=5,
                  group=31,
                  label=AnnotatedTimespan,
                  shape=box];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=5,
                  group=31,
                  label=CompoundInequality,
                  shape=box];
              "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation" [color=5,
                  group=31,
                  label=OffsetTimespanTimeRelation,
                  shape=box];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" [color=5,
                  group=31,
                  label=TimeRelation,
                  shape=oval,
                  style=bold];
              "abjad.tools.timespantools.Timespan.Timespan" [color=5,
                  group=31,
                  label=Timespan,
                  shape=box];
              "abjad.tools.timespantools.TimespanInequality.TimespanInequality" [color=5,
                  group=31,
                  label=TimespanInequality,
                  shape=box];
              "abjad.tools.timespantools.TimespanList.TimespanList" [color=5,
                  group=31,
                  label=TimespanList,
                  shape=box];
              "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation" [color=5,
                  group=31,
                  label=TimespanTimespanTimeRelation,
                  shape=box];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation";
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation";
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent" [color=6,
                  group=32,
                  label=ChordExtent,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion" [color=6,
                  group=32,
                  label=ChordInversion,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality" [color=6,
                  group=32,
                  label=ChordQuality,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension" [color=6,
                  group=32,
                  label=ChordSuspension,
                  shape=box];
              "abjad.tools.tonalanalysistools.Mode.Mode" [color=6,
                  group=32,
                  label=Mode,
                  shape=box];
              "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral" [color=6,
                  group=32,
                  label=RomanNumeral,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=6,
                  group=32,
                  label=RootedChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=6,
                  group=32,
                  label=RootlessChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=6,
                  group=32,
                  label=Scale,
                  shape=box];
              "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree" [color=6,
                  group=32,
                  label=ScaleDegree,
                  shape=box];
              "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent" [color=6,
                  group=32,
                  label=TonalAnalysisAgent,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=4,
                  group=3,
                  label=object,
                  shape=box];
          }
          subgraph cluster_constrainttools {
              graph [label=constrainttools];
              "experimental.tools.constrainttools.AbsoluteIndexConstraint.AbsoluteIndexConstraint" [color=6,
                  group=5,
                  label=AbsoluteIndexConstraint,
                  shape=box];
              "experimental.tools.constrainttools.Domain.Domain" [color=6,
                  group=5,
                  label=Domain,
                  shape=box];
              "experimental.tools.constrainttools.FixedLengthStreamSolver.FixedLengthStreamSolver" [color=6,
                  group=5,
                  label=FixedLengthStreamSolver,
                  shape=box];
              "experimental.tools.constrainttools.GlobalConstraint.GlobalConstraint" [color=6,
                  group=5,
                  label=GlobalConstraint,
                  shape=box];
              "experimental.tools.constrainttools.GlobalCountsConstraint.GlobalCountsConstraint" [color=6,
                  group=5,
                  label=GlobalCountsConstraint,
                  shape=box];
              "experimental.tools.constrainttools.GlobalReferenceConstraint.GlobalReferenceConstraint" [color=6,
                  group=5,
                  label=GlobalReferenceConstraint,
                  shape=box];
              "experimental.tools.constrainttools.RelativeCountsConstraint.RelativeCountsConstraint" [color=6,
                  group=5,
                  label=RelativeCountsConstraint,
                  shape=box];
              "experimental.tools.constrainttools.RelativeIndexConstraint.RelativeIndexConstraint" [color=6,
                  group=5,
                  label=RelativeIndexConstraint,
                  shape=box];
              "experimental.tools.constrainttools.VariableLengthStreamSolver.VariableLengthStreamSolver" [color=6,
                  group=5,
                  label=VariableLengthStreamSolver,
                  shape=box];
              "experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint._AbsoluteConstraint" [color=6,
                  group=5,
                  label=_AbsoluteConstraint,
                  shape=box];
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" [color=6,
                  group=5,
                  label=_Constraint,
                  shape=box];
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" [color=6,
                  group=5,
                  label=_GlobalConstraint,
                  shape=box];
              "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint" [color=6,
                  group=5,
                  label=_RelativeConstraint,
                  shape=box];
              "experimental.tools.constrainttools._SolutionNode._SolutionNode._SolutionNode" [color=6,
                  group=5,
                  label=_SolutionNode,
                  shape=box];
              "experimental.tools.constrainttools._Solver._Solver._Solver" [color=6,
                  group=5,
                  label=_Solver,
                  shape=box];
              "experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint._AbsoluteConstraint" -> "experimental.tools.constrainttools.AbsoluteIndexConstraint.AbsoluteIndexConstraint";
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" -> "experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint._AbsoluteConstraint";
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" -> "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint";
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" -> "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint";
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" -> "experimental.tools.constrainttools.GlobalConstraint.GlobalConstraint";
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" -> "experimental.tools.constrainttools.GlobalCountsConstraint.GlobalCountsConstraint";
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" -> "experimental.tools.constrainttools.GlobalReferenceConstraint.GlobalReferenceConstraint";
              "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint" -> "experimental.tools.constrainttools.RelativeCountsConstraint.RelativeCountsConstraint";
              "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint" -> "experimental.tools.constrainttools.RelativeIndexConstraint.RelativeIndexConstraint";
              "experimental.tools.constrainttools._Solver._Solver._Solver" -> "experimental.tools.constrainttools.FixedLengthStreamSolver.FixedLengthStreamSolver";
              "experimental.tools.constrainttools._Solver._Solver._Solver" -> "experimental.tools.constrainttools.VariableLengthStreamSolver.VariableLengthStreamSolver";
          }
          subgraph cluster_interpolationtools {
              graph [label=interpolationtools];
              "experimental.tools.interpolationtools.BreakPointFunction.BreakPointFunction" [color=4,
                  group=12,
                  label=BreakPointFunction,
                  shape=box];
          }
          subgraph cluster_makertools {
              graph [label=makertools];
              "experimental.tools.makertools.PianoStaffSegmentMaker.PianoStaffSegmentMaker" [color=8,
                  group=16,
                  label=PianoStaffSegmentMaker,
                  shape=box];
              "experimental.tools.makertools.SegmentMaker.SegmentMaker" [color=8,
                  group=16,
                  label=SegmentMaker,
                  shape=box];
              "experimental.tools.makertools.SegmentMaker.SegmentMaker" -> "experimental.tools.makertools.PianoStaffSegmentMaker.PianoStaffSegmentMaker";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.demos.part.PartCantusScoreTemplate.PartCantusScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.InspectionAgent.InspectionAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.IterationAgent.IterationAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.LabelAgent.LabelAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.MutationAgent.MutationAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.DocumentationManager.DocumentationManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.durationtools.Duration.Duration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.indicatortools.WoodwindFingering.WoodwindFingering";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.Block.Block";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.DateTimeToken.DateTimeToken";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondDimension.LilyPondDimension";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondDuration.LilyPondDuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondEvent.LilyPondEvent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondFraction.LilyPondFraction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondGrammarGenerator.LilyPondGrammarGenerator";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition.LilyPondSyntacticalDefinition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.Music.Music";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.MeterManager.MeterManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.GraceHandler.GraceHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.Heuristic.Heuristic";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.JobHandler.JobHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEvent.QEvent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEventProxy.QEventProxy";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEventSequence.QEventSequence";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QGrid.QGrid";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QSchema.QSchema";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTarget.QTarget";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTargetBeat.QTargetBeat";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.Quantizer.Quantizer";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.SearchTree.SearchTree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.NoteHead.NoteHead";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.spannertools.Spanner.Spanner";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.Configuration.Configuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.IOManager.IOManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.ImportManager.ImportManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.SlotContributions.SlotContributions";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.TestManager.TestManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.UpdateManager.UpdateManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.WellformednessManager.WellformednessManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.TimespanInequality.TimespanInequality";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools.Domain.Domain";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools._Constraint._Constraint._Constraint";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools._SolutionNode._SolutionNode._SolutionNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools._Solver._Solver._Solver";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.interpolationtools.BreakPointFunction.BreakPointFunction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.makertools.SegmentMaker.SegmentMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlock.CodeBlock";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeOutputProxy.CodeOutputProxy";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageRenderSpecifier.ImageRenderSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Expression.Expression";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Pattern.Pattern";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Sequence.Sequence";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Accelerando.Accelerando";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Arpeggio.Arpeggio";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Articulation.Articulation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BarLine.BarLine";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BendAfter.BendAfter";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BowContactPoint.BowContactPoint";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BowMotionTechnique.BowMotionTechnique";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BowPressure.BowPressure";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BreathMark.BreathMark";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Clef.Clef";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.ColorFingering.ColorFingering";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Dynamic.Dynamic";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Fermata.Fermata";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.KeyCluster.KeyCluster";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.KeySignature.KeySignature";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LaissezVibrer.LaissezVibrer";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LilyPondCommand.LilyPondCommand";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LilyPondComment.LilyPondComment";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LilyPondLiteral.LilyPondLiteral";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LineSegment.LineSegment";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.MetricModulation.MetricModulation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.MetronomeMark.MetronomeMark";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.PageBreak.PageBreak";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.RehearsalMark.RehearsalMark";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Repeat.Repeat";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Ritardando.Ritardando";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Staccatissimo.Staccatissimo";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Staccato.Staccato";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StaffChange.StaffChange";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StemTremolo.StemTremolo";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StringContactPoint.StringContactPoint";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StringNumber.StringNumber";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.SystemBreak.SystemBreak";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.TimeSignature.TimeSignature";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Tremolo.Tremolo";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Tuning.Tuning";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.instrumenttools.Instrument.Instrument";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.instrumenttools.Performer.Performer";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondfiletools.LilyPondLanguageToken.LilyPondLanguageToken";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondfiletools.PackageGitCommitToken.PackageGitCommitToken";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Markup.Markup";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.MarkupCommand.MarkupCommand";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Postscript.Postscript";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.PostscriptOperator.PostscriptOperator";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.Enumerator.Enumerator";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.Infinity.Infinity";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.Meter.Meter";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MeterFittingSession.MeterFittingSession";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Accidental.Accidental";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.ColorMap.ColorMap";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.CompoundOperator.CompoundOperator";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Duplication.Duplication";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Interval.Interval";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.IntervalClass.IntervalClass";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Inversion.Inversion";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Multiplication.Multiplication";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Octave.Octave";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Pitch.Pitch";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.PitchClass.PitchClass";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.PitchRange.PitchRange";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Retrograde.Retrograde";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Rotation.Rotation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.SetClass.SetClass";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.StaffPosition.StaffPosition";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Transposition.Transposition";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.BurnishSpecifier.BurnishSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.InciseSpecifier.InciseSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.InterpolationSpecifier.InterpolationSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.SilenceMask.SilenceMask";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.SustainMask.SustainMask";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.Talea.Talea";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.TieSpecifier.TieSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.schemetools.Scheme.Scheme";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.LeafMaker.LeafMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.MeasureMaker.MeasureMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.NoteMaker.NoteMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ContiguitySelectorCallback.ContiguitySelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.CountsSelectorCallback.CountsSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.DurationSelectorCallback.DurationSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ExtraLeafSelectorCallback.ExtraLeafSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.FlattenSelectorCallback.FlattenSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.GroupByPitchCallback.GroupByPitchCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Inequality.Inequality";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ItemSelectorCallback.ItemSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LengthSelectorCallback.LengthSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LogicalMeasureSelectorCallback.LogicalMeasureSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LogicalTieSelectorCallback.LogicalTieSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PartitionByRatioCallback.PartitionByRatioCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PatternedSelectorCallback.PatternedSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PitchSelectorCallback.PitchSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PrototypeSelectorCallback.PrototypeSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.RunSelectorCallback.RunSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Selector.Selector";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.SliceSelectorCallback.SliceSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.WrapSelectionCallback.WrapSelectionCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.FormatSpecification.FormatSpecification";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.Signature.Signature";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.GroupedRhythmicStavesScoreTemplate.GroupedRhythmicStavesScoreTemplate";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.StringQuartetScoreTemplate.StringQuartetScoreTemplate";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.TwoStaffPianoScoreTemplate.TwoStaffPianoScoreTemplate";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.timespantools.TimeRelation.TimeRelation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.Mode.Mode";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.FilesystemState.FilesystemState";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.NullContextManager.NullContextManager";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.Timer.Timer";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser";
          "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript";
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
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.metertools.OffsetCounter.OffsetCounter";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.pitchtools.Vector.Vector";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter";
          "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" -> "abjad.tools.pitchtools.Set.Set";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.ClefList.ClefList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.InstrumentList.InstrumentList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.PerformerList.PerformerList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.markuptools.MarkupList.MarkupList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.metertools.MeterList.MeterList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchRangeList.PitchRangeList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.Registration.Registration";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.RegistrationList.RegistrationList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadList.NoteHeadList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.CompoundInequality.CompoundInequality";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.TimespanList.TimespanList";
          "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" -> "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.pitchtools.Segment.Segment";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   ContextManager
   Parser

.. autosummary::
   :nosignatures:

   ContextManager
   Parser

--------

Classes
-------

.. toctree::
   :hidden:

   AbjadObject
   AbjadValueObject

.. autosummary::
   :nosignatures:

   AbjadObject
   AbjadValueObject
