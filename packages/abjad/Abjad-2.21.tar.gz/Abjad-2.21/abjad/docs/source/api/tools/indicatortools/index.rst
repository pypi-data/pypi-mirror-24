indicatortools
==============

.. automodule:: abjad.tools.indicatortools

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
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.Accelerando.Accelerando" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Accelerando,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Arpeggio.Arpeggio" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Arpeggio,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ArrowLineSegment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Articulation.Articulation" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Articulation,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.BarLine.BarLine" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BarLine,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.BendAfter.BendAfter" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BendAfter,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.BowContactPoint.BowContactPoint" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BowContactPoint,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.BowMotionTechnique.BowMotionTechnique" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BowMotionTechnique,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.BowPressure.BowPressure" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BowPressure,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.BreathMark.BreathMark" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BreathMark,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Clef.Clef" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Clef,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.ColorFingering.ColorFingering" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ColorFingering,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Dynamic.Dynamic" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Dynamic,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Fermata.Fermata" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Fermata,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.KeyCluster.KeyCluster" [color=black,
                  fontcolor=white,
                  group=3,
                  label=KeyCluster,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.KeySignature.KeySignature" [color=black,
                  fontcolor=white,
                  group=3,
                  label=KeySignature,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LaissezVibrer.LaissezVibrer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LaissezVibrer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LilyPondCommand.LilyPondCommand" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LilyPondCommand,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LilyPondComment.LilyPondComment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LilyPondComment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LilyPondLiteral.LilyPondLiteral" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LilyPondLiteral,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LineSegment.LineSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LineSegment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.MetricModulation.MetricModulation" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MetricModulation,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.MetronomeMark.MetronomeMark" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MetronomeMark,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MetronomeMarkList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.PageBreak.PageBreak" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PageBreak,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.RehearsalMark.RehearsalMark" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RehearsalMark,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Repeat.Repeat" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Repeat,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Ritardando.Ritardando" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Ritardando,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Staccatissimo.Staccatissimo" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Staccatissimo,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Staccato.Staccato" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Staccato,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.StaffChange.StaffChange" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StaffChange,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.StemTremolo.StemTremolo" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StemTremolo,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.StringContactPoint.StringContactPoint" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StringContactPoint,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.StringNumber.StringNumber" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StringNumber,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.SystemBreak.SystemBreak" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SystemBreak,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.TimeSignature.TimeSignature" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TimeSignature,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TimeSignatureList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Tremolo.Tremolo" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Tremolo,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.Tuning.Tuning" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Tuning,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.WoodwindFingering.WoodwindFingering" [color=black,
                  fontcolor=white,
                  group=3,
                  label=WoodwindFingering,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LineSegment.LineSegment" -> "abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.indicatortools.WoodwindFingering.WoodwindFingering";
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Accelerando
   Arpeggio
   ArrowLineSegment
   Articulation
   BarLine
   BendAfter
   BowContactPoint
   BowMotionTechnique
   BowPressure
   BreathMark
   Clef
   ColorFingering
   Dynamic
   Fermata
   KeyCluster
   KeySignature
   LaissezVibrer
   LilyPondCommand
   LilyPondComment
   LilyPondLiteral
   LineSegment
   MetricModulation
   MetronomeMark
   PageBreak
   RehearsalMark
   Repeat
   Ritardando
   Staccatissimo
   Staccato
   StaffChange
   StemTremolo
   StringContactPoint
   StringNumber
   SystemBreak
   TimeSignature
   Tremolo
   Tuning
   WoodwindFingering

.. autosummary::
   :nosignatures:

   Accelerando
   Arpeggio
   ArrowLineSegment
   Articulation
   BarLine
   BendAfter
   BowContactPoint
   BowMotionTechnique
   BowPressure
   BreathMark
   Clef
   ColorFingering
   Dynamic
   Fermata
   KeyCluster
   KeySignature
   LaissezVibrer
   LilyPondCommand
   LilyPondComment
   LilyPondLiteral
   LineSegment
   MetricModulation
   MetronomeMark
   PageBreak
   RehearsalMark
   Repeat
   Ritardando
   Staccatissimo
   Staccato
   StaffChange
   StemTremolo
   StringContactPoint
   StringNumber
   SystemBreak
   TimeSignature
   Tremolo
   Tuning
   WoodwindFingering

--------

Collections
-----------

.. toctree::
   :hidden:

   MetronomeMarkList
   TimeSignatureList

.. autosummary::
   :nosignatures:

   MetronomeMarkList
   TimeSignatureList
