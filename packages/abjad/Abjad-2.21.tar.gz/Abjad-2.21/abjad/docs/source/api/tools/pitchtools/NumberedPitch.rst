.. currentmodule:: abjad.tools.pitchtools

NumberedPitch
=============

.. autoclass:: NumberedPitch

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
              "abjad.tools.pitchtools.NumberedPitch.NumberedPitch" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NumberedPitch</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=3,
                  group=2,
                  label=Pitch,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NumberedPitch.NumberedPitch";
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

      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.accidental
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.arrow
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.from_hertz
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.from_pitch_carrier
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.get_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.hertz
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.interpolate
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.invert
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.multiply
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.octave
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.transpose
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__add__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__copy__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__eq__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__float__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__format__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ge__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__gt__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__hash__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__illustrate__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__le__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__lt__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ne__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__neg__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__radd__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__repr__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__str__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.accidental

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.arrow

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.hertz

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.name

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.number

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.octave

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class

Methods
-------

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.get_name

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.interpolate

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.invert

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.multiply

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.transpose

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.from_hertz

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.from_pitch_carrier

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__le__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ne__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__neg__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__repr__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__str__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__sub__
