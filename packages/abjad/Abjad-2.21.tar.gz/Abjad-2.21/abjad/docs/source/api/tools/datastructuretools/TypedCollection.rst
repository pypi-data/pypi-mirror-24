.. currentmodule:: abjad.tools.datastructuretools

TypedCollection
===============

.. autoclass:: TypedCollection

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
              "abjad.tools.datastructuretools.PatternList.PatternList" [color=3,
                  group=2,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TypedCollection</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=3,
                  group=2,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=3,
                  group=2,
                  label=TypedFrozenset,
                  shape=box];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=3,
                  group=2,
                  label=TypedOrderedDict,
                  shape=box];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.datastructuretools.PatternList.PatternList";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList" [color=4,
                  group=3,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList" [color=4,
                  group=3,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.ClefList.ClefList" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.instrumenttools.InstrumentList.InstrumentList" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.instrumenttools.PerformerList.PerformerList" [color=5,
                  group=4,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupList.MarkupList" [color=6,
                  group=5,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterList.MeterList" [color=7,
                  group=6,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=7,
                  group=6,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchRangeList.PitchRangeList" [color=8,
                  group=7,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.pitchtools.Registration.Registration" [color=8,
                  group=7,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.pitchtools.RegistrationList.RegistrationList" [color=8,
                  group=7,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.pitchtools.Segment.Segment" [color=8,
                  group=7,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.pitchtools.Set.Set" [color=8,
                  group=7,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.pitchtools.Vector.Vector" [color=8,
                  group=7,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=9,
                  group=8,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=9,
                  group=8,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=1,
                  group=9,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=2,
                  group=10,
                  label=" ",
                  shape=invis,
                  style=transparent];
              "abjad.tools.timespantools.TimespanList.TimespanList" [color=2,
                  group=10,
                  label=" ",
                  shape=invis,
                  style=transparent];
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
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

      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.item_class
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.items
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__contains__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__eq__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__format__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__hash__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__iter__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__len__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__ne__
      ~abjad.tools.datastructuretools.TypedCollection.TypedCollection.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.item_class

.. autoattribute:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.items

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__contains__

.. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__format__

.. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__hash__

.. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__iter__

.. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCollection.TypedCollection.__repr__
