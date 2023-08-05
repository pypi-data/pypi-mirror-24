.. currentmodule:: abjad.tools.pitchtools

NamedIntervalClass
==================

.. autoclass:: NamedIntervalClass

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
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" [color=3,
                  group=2,
                  label=IntervalClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NamedIntervalClass</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass" [color=3,
                  group=2,
                  label=NamedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass";
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" -> "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.IntervalClass.IntervalClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.IntervalClass`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.direction_number
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.direction_string
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.direction_symbol
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.from_pitch_carriers
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.from_quality_and_number
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.name
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.number
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.quality_and_number_to_name
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.quality_string
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__abs__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__copy__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__eq__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__float__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__format__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__ge__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__gt__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__hash__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__le__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__lt__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__ne__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__repr__
      ~abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.direction_number

.. autoattribute:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.direction_string

.. autoattribute:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.direction_symbol

.. autoattribute:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.number

.. autoattribute:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.quality_string

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.from_pitch_carriers

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.from_quality_and_number

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.quality_and_number_to_name

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__abs__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__copy__

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__eq__

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__gt__

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__le__

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__repr__

.. automethod:: abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass.__str__
