.. currentmodule:: abjad.tools.pitchtools

NamedPitch
==========

.. autoclass:: NamedPitch

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
              "abjad.tools.pitchtools.NamedPitch.NamedPitch" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NamedPitch</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=3,
                  group=2,
                  label=Pitch,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NamedPitch.NamedPitch";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Pitch.Pitch";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.Pitch`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.accidental
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.arrow
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.from_hertz
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.from_pitch_carrier
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.from_pitch_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.get_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.hertz
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.invert
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.multiply
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.octave
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.to_staff_position
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.transpose
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.transpose_staff_position
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__add__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__copy__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__eq__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__float__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__format__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__ge__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__gt__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__hash__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__illustrate__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__le__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__lt__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__ne__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__radd__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__repr__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__str__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.accidental

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.arrow

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.hertz

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.name

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.number

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.octave

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class

Methods
-------

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.get_name

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.invert

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.multiply

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.to_staff_position

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.transpose

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.transpose_staff_position

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.from_hertz

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.from_pitch_carrier

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.from_pitch_number

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__add__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__copy__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__gt__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__le__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__ne__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__repr__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__str__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__sub__
