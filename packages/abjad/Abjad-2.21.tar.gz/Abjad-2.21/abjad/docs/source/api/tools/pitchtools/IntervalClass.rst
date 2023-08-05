.. currentmodule:: abjad.tools.pitchtools

IntervalClass
=============

.. autoclass:: IntervalClass

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
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>IntervalClass</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" [color=3,
                  group=2,
                  label=NamedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass" [color=3,
                  group=2,
                  label=NamedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" [color=3,
                  group=2,
                  label=NumberedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass" [color=3,
                  group=2,
                  label=NumberedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass";
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass";
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" -> "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass";
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" -> "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass";
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

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.number
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__abs__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__copy__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__eq__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__format__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__ge__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__gt__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__hash__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__le__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__lt__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__ne__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__repr__
      ~abjad.tools.pitchtools.IntervalClass.IntervalClass.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.IntervalClass.IntervalClass.number

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__abs__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__format__

.. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__ge__

.. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__hash__

.. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__le__

.. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__repr__

.. automethod:: abjad.tools.pitchtools.IntervalClass.IntervalClass.__str__
