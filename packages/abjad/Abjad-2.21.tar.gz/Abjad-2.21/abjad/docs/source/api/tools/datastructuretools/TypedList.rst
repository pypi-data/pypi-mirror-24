.. currentmodule:: abjad.tools.datastructuretools

TypedList
=========

.. autoclass:: TypedList

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
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TypedList</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.MetronomeMarkList.MetronomeMarkList" [color=4,
                  group=3,
                  label=MetronomeMarkList,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignatureList.TimeSignatureList" [color=4,
                  group=3,
                  label=TimeSignatureList,
                  shape=box];
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.ClefList.ClefList" [color=5,
                  group=4,
                  label=ClefList,
                  shape=box];
              "abjad.tools.instrumenttools.InstrumentList.InstrumentList" [color=5,
                  group=4,
                  label=InstrumentList,
                  shape=box];
              "abjad.tools.instrumenttools.PerformerList.PerformerList" [color=5,
                  group=4,
                  label=PerformerList,
                  shape=box];
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupList.MarkupList" [color=6,
                  group=5,
                  label=MarkupList,
                  shape=box];
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterList.MeterList" [color=7,
                  group=6,
                  label=MeterList,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchRangeList.PitchRangeList" [color=8,
                  group=7,
                  label=PitchRangeList,
                  shape=box];
              "abjad.tools.pitchtools.Registration.Registration" [color=8,
                  group=7,
                  label=Registration,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationList.RegistrationList" [color=8,
                  group=7,
                  label=RegistrationList,
                  shape=box];
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=9,
                  group=8,
                  label=NoteHeadList,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=1,
                  group=9,
                  label=CompoundInequality,
                  shape=box];
              "abjad.tools.timespantools.TimespanList.TimespanList" [color=1,
                  group=9,
                  label=TimespanList,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
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
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.TypedList.TypedList.append
      ~abjad.tools.datastructuretools.TypedList.TypedList.count
      ~abjad.tools.datastructuretools.TypedList.TypedList.extend
      ~abjad.tools.datastructuretools.TypedList.TypedList.index
      ~abjad.tools.datastructuretools.TypedList.TypedList.insert
      ~abjad.tools.datastructuretools.TypedList.TypedList.item_class
      ~abjad.tools.datastructuretools.TypedList.TypedList.items
      ~abjad.tools.datastructuretools.TypedList.TypedList.keep_sorted
      ~abjad.tools.datastructuretools.TypedList.TypedList.pop
      ~abjad.tools.datastructuretools.TypedList.TypedList.remove
      ~abjad.tools.datastructuretools.TypedList.TypedList.reverse
      ~abjad.tools.datastructuretools.TypedList.TypedList.sort
      ~abjad.tools.datastructuretools.TypedList.TypedList.__contains__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__delitem__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__eq__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__format__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__getitem__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__hash__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__iadd__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__iter__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__len__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__ne__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__repr__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__reversed__
      ~abjad.tools.datastructuretools.TypedList.TypedList.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedList.TypedList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedList.TypedList.items

Read/write properties
---------------------

.. autoattribute:: abjad.tools.datastructuretools.TypedList.TypedList.keep_sorted

Methods
-------

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.append

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.count

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.extend

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.index

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.insert

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.pop

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.remove

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.reverse

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__contains__

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__format__

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__hash__

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__repr__

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__reversed__

.. automethod:: abjad.tools.datastructuretools.TypedList.TypedList.__setitem__
