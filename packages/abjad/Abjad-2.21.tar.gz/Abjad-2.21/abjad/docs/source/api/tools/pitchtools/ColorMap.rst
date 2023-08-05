.. currentmodule:: abjad.tools.pitchtools

ColorMap
========

.. autoclass:: ColorMap

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
              "abjad.tools.pitchtools.ColorMap.ColorMap" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ColorMap</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.ColorMap.ColorMap";
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

      ~abjad.tools.pitchtools.ColorMap.ColorMap.colors
      ~abjad.tools.pitchtools.ColorMap.ColorMap.get
      ~abjad.tools.pitchtools.ColorMap.ColorMap.is_twelve_tone_complete
      ~abjad.tools.pitchtools.ColorMap.ColorMap.is_twenty_four_tone_complete
      ~abjad.tools.pitchtools.ColorMap.ColorMap.pairs
      ~abjad.tools.pitchtools.ColorMap.ColorMap.pitch_iterables
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__copy__
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__eq__
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__format__
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__getitem__
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__hash__
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__ne__
      ~abjad.tools.pitchtools.ColorMap.ColorMap.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.ColorMap.ColorMap.colors

.. autoattribute:: abjad.tools.pitchtools.ColorMap.ColorMap.is_twelve_tone_complete

.. autoattribute:: abjad.tools.pitchtools.ColorMap.ColorMap.is_twenty_four_tone_complete

.. autoattribute:: abjad.tools.pitchtools.ColorMap.ColorMap.pairs

.. autoattribute:: abjad.tools.pitchtools.ColorMap.ColorMap.pitch_iterables

Methods
-------

.. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.get

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__eq__

.. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__format__

.. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.ColorMap.ColorMap.__repr__
