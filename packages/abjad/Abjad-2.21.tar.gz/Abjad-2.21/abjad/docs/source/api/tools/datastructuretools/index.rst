datastructuretools
==================

.. automodule:: abjad.tools.datastructuretools

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple" [color=black,
                  fontcolor=white,
                  group=2,
                  label=CyclicTuple,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Enumeration.Enumeration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Enumeration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Expression.Expression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Expression,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant" [color=black,
                  fontcolor=white,
                  group=2,
                  label=OrdinalConstant,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Pattern.Pattern" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Pattern,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.PatternList.PatternList" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PatternList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Sequence.Sequence" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Sequence,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.SortedCollection.SortedCollection" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SortedCollection,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.String.String" [color=black,
                  fontcolor=white,
                  group=2,
                  label=String,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TreeContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TreeNode,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedCounter,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedFrozenset,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedOrderedDict,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedTuple,
                  shape=box,
                  style="filled, rounded"];
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
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=4,
                  group=3,
                  label=ReSTAutodocDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=4,
                  group=3,
                  label=ReSTAutosummaryDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=4,
                  group=3,
                  label=ReSTAutosummaryItem,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=4,
                  group=3,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=4,
                  group=3,
                  label=ReSTDocument,
                  shape=box];
              "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective" [color=4,
                  group=3,
                  label=ReSTGraphvizDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=4,
                  group=3,
                  label=ReSTHeading,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule" [color=4,
                  group=3,
                  label=ReSTHorizontalRule,
                  shape=box];
              "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram" [color=4,
                  group=3,
                  label=ReSTInheritanceDiagram,
                  shape=box];
              "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective" [color=4,
                  group=3,
                  label=ReSTLineageDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective" [color=4,
                  group=3,
                  label=ReSTOnlyDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph" [color=4,
                  group=3,
                  label=ReSTParagraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=4,
                  group=3,
                  label=ReSTTOCDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem" [color=4,
                  group=3,
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
          subgraph cluster_graphtools {
              graph [label=graphtools];
              "abjad.tools.graphtools.GraphvizField.GraphvizField" [color=6,
                  group=5,
                  label=GraphvizField,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" [color=6,
                  group=5,
                  label=GraphvizGraph,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGroup.GraphvizGroup" [color=6,
                  group=5,
                  label=GraphvizGroup,
                  shape=box];
              "abjad.tools.graphtools.GraphvizNode.GraphvizNode" [color=6,
                  group=5,
                  label=GraphvizNode,
                  shape=box];
              "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph" [color=6,
                  group=5,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTable.GraphvizTable" [color=6,
                  group=5,
                  label=GraphvizTable,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableCell.GraphvizTableCell" [color=6,
                  group=5,
                  label=GraphvizTableCell,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=6,
                  group=5,
                  label=GraphvizTableHorizontalRule,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow" [color=6,
                  group=5,
                  label=GraphvizTableRow,
                  shape=box];
              "abjad.tools.graphtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=6,
                  group=5,
                  label=GraphvizTableVerticalRule,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList" [color=7,
                  group=6,
                  label=MetronomeMarkList,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList" [color=7,
                  group=6,
                  label=TimeSignatureList,
                  shape=box];
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.ClefList.ClefList" [color=8,
                  group=7,
                  label=ClefList,
                  shape=box];
              "abjad.tools.instrumenttools.InstrumentList.InstrumentList" [color=8,
                  group=7,
                  label=InstrumentList,
                  shape=box];
              "abjad.tools.instrumenttools.PerformerList.PerformerList" [color=8,
                  group=7,
                  label=PerformerList,
                  shape=box];
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupList.MarkupList" [color=9,
                  group=8,
                  label=MarkupList,
                  shape=box];
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterList.MeterList" [color=1,
                  group=9,
                  label=MeterList,
                  shape=box];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=1,
                  group=9,
                  label=OffsetCounter,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=2,
                  group=10,
                  label=IntervalClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=2,
                  group=10,
                  label=IntervalClassSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=2,
                  group=10,
                  label=IntervalClassVector,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=2,
                  group=10,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=2,
                  group=10,
                  label=IntervalSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=2,
                  group=10,
                  label=IntervalVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=2,
                  group=10,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=2,
                  group=10,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=2,
                  group=10,
                  label=PitchClassVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchRangeList.PitchRangeList" [color=2,
                  group=10,
                  label=PitchRangeList,
                  shape=box];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=2,
                  group=10,
                  label=PitchSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=2,
                  group=10,
                  label=PitchSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=2,
                  group=10,
                  label=PitchVector,
                  shape=box];
              "abjad.tools.pitchtools.Registration.Registration" [color=2,
                  group=10,
                  label=Registration,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationList.RegistrationList" [color=2,
                  group=10,
                  label=RegistrationList,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=2,
                  group=10,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" [color=2,
                  group=10,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=2,
                  group=10,
                  label=TwelveToneRow,
                  shape=box];
              "abjad.tools.pitchtools.Vector.Vector" [color=2,
                  group=10,
                  label=Vector,
                  shape=oval,
                  style=bold];
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
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=3,
                  group=11,
                  label=QGridContainer,
                  shape=box];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=3,
                  group=11,
                  label=QGridLeaf,
                  shape=box];
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=4,
                  group=12,
                  label=PartitionTable,
                  shape=box];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=4,
                  group=12,
                  label=RotationCounter,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=5,
                  group=13,
                  label=RhythmTreeContainer,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=5,
                  group=13,
                  label=RhythmTreeLeaf,
                  shape=box];
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=6,
                  group=14,
                  label=NoteHeadList,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=7,
                  group=15,
                  label=CompoundInequality,
                  shape=box];
              "abjad.tools.timespantools.TimespanList.TimespanList" [color=7,
                  group=15,
                  label=TimespanList,
                  shape=box];
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=8,
                  group=16,
                  label=RootedChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=8,
                  group=16,
                  label=RootlessChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=8,
                  group=16,
                  label=Scale,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.int" [color=2,
                  group=1,
                  label=int,
                  shape=box];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
              "builtins.str" [color=2,
                  group=1,
                  label=str,
                  shape=box];
              "builtins.object" -> "builtins.int";
              "builtins.object" -> "builtins.str";
          }
          subgraph cluster_enum {
              graph [label=enum];
              "enum.Enum" [color=5,
                  group=4,
                  label=Enum,
                  shape=box];
              "enum.IntEnum" [color=5,
                  group=4,
                  label=IntEnum,
                  shape=box];
              "enum.Enum" -> "enum.IntEnum";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Expression.Expression";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Pattern.Pattern";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Sequence.Sequence";
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
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "builtins.int" -> "enum.IntEnum";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "abjad.tools.datastructuretools.SortedCollection.SortedCollection";
          "builtins.object" -> "enum.Enum";
          "builtins.str" -> "abjad.tools.datastructuretools.String.String";
          "enum.IntEnum" -> "abjad.tools.datastructuretools.Enumeration.Enumeration";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   TypedCollection

.. autosummary::
   :nosignatures:

   TypedCollection

--------

Classes
-------

.. toctree::
   :hidden:

   CyclicTuple
   Enumeration
   Expression
   OrdinalConstant
   Pattern
   PatternList
   Sequence
   SortedCollection
   String
   TreeContainer
   TreeNode
   TypedCounter
   TypedFrozenset
   TypedList
   TypedOrderedDict
   TypedTuple

.. autosummary::
   :nosignatures:

   CyclicTuple
   Enumeration
   Expression
   OrdinalConstant
   Pattern
   PatternList
   Sequence
   SortedCollection
   String
   TreeContainer
   TreeNode
   TypedCounter
   TypedFrozenset
   TypedList
   TypedOrderedDict
   TypedTuple
