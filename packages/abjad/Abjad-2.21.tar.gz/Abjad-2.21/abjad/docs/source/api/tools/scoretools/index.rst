scoretools
==========

.. automodule:: abjad.tools.scoretools

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AcciaccaturaContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AfterGraceContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AppoggiaturaContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Chord.Chord" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Chord,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Cluster.Cluster" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Cluster,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Component,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Container.Container" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Container,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Context.Context" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Context,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DrumNoteHead,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraceContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Leaf.Leaf" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Leaf,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.scoretools.LeafMaker.LeafMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LeafMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Measure.Measure" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Measure,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.MeasureMaker.MeasureMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MeasureMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MultimeasureRest,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Note.Note" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Note,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteHead.NoteHead" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NoteHead,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NoteHeadList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteMaker.NoteMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NoteMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Rest.Rest" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Rest,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Score.Score" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Score,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Skip.Skip" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Skip,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Staff.Staff" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Staff,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StaffGroup,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Tuplet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Voice.Voice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Voice,
                  shape=box,
                  style="filled, rounded"];
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
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.NoteHead.NoteHead";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.LeafMaker.LeafMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.MeasureMaker.MeasureMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.NoteMaker.NoteMaker";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadList.NoteHeadList";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   Component
   Leaf

.. autosummary::
   :nosignatures:

   Component
   Leaf

--------

Containers
----------

.. toctree::
   :hidden:

   AcciaccaturaContainer
   AfterGraceContainer
   AppoggiaturaContainer
   Cluster
   Container
   GraceContainer
   Measure
   Tuplet

.. autosummary::
   :nosignatures:

   AcciaccaturaContainer
   AfterGraceContainer
   AppoggiaturaContainer
   Cluster
   Container
   GraceContainer
   Measure
   Tuplet

--------

Contexts
--------

.. toctree::
   :hidden:

   Context
   Score
   Staff
   StaffGroup
   Voice

.. autosummary::
   :nosignatures:

   Context
   Score
   Staff
   StaffGroup
   Voice

--------

Leaves
------

.. toctree::
   :hidden:

   Chord
   MultimeasureRest
   Note
   Rest
   Skip

.. autosummary::
   :nosignatures:

   Chord
   MultimeasureRest
   Note
   Rest
   Skip

--------

Makers
------

.. toctree::
   :hidden:

   LeafMaker
   MeasureMaker
   NoteMaker

.. autosummary::
   :nosignatures:

   LeafMaker
   MeasureMaker
   NoteMaker

--------

Note-heads
----------

.. toctree::
   :hidden:

   DrumNoteHead
   NoteHead
   NoteHeadList

.. autosummary::
   :nosignatures:

   DrumNoteHead
   NoteHead
   NoteHeadList
