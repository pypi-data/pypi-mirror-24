.. currentmodule:: abjad.tools.instrumenttools

MezzoSopranoVoice
=================

.. autoclass:: MezzoSopranoVoice

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.Instrument.Instrument" [color=3,
                  group=2,
                  label=Instrument,
                  shape=box];
              "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MezzoSopranoVoice</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.instrumenttools.Instrument.Instrument";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.instrumenttools.Instrument`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.allowable_clefs
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.instrument_name
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.instrument_name_markup
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.pitch_range
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.short_instrument_name
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.short_instrument_name_markup
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.sounding_pitch_of_written_middle_c
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.transpose_from_sounding_pitch
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.transpose_from_written_pitch
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__copy__
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__eq__
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__format__
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__hash__
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__ne__
      ~abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.allowable_clefs

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.instrument_name

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.instrument_name_markup

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.pitch_range

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.short_instrument_name

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.short_instrument_name_markup

.. autoattribute:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.sounding_pitch_of_written_middle_c

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.transpose_from_sounding_pitch

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.transpose_from_written_pitch

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice.__repr__
