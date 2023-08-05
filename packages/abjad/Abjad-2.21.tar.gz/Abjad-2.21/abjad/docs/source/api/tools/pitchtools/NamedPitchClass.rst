.. currentmodule:: abjad.tools.pitchtools

NamedPitchClass
===============

.. autoclass:: NamedPitchClass

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
              "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NamedPitchClass</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClass.PitchClass" [color=3,
                  group=2,
                  label=PitchClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.PitchClass.PitchClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.PitchClass`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.accidental
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.invert
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_diatonic_pitch_class_name
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_diatonic_pitch_class_number
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_pitch_class_name
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_pitch_class_number
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.multiply
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.name
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.number
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.pitch_class_label
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.transpose
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__add__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__copy__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__eq__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__float__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__format__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__ge__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__gt__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__hash__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__le__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__lt__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__ne__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__radd__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__repr__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__str__
      ~abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.accidental

.. autoattribute:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.name

.. autoattribute:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.number

.. autoattribute:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.pitch_class_label

Methods
-------

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.invert

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.multiply

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.transpose

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_diatonic_pitch_class_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_diatonic_pitch_class_number

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_pitch_class_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.is_pitch_class_number

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__add__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__copy__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__float__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__gt__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__le__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__ne__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__repr__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__str__

.. automethod:: abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass.__sub__
