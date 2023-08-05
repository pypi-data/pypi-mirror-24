.. currentmodule:: abjad.tools.pitchtools

StaffPosition
=============

.. autoclass:: StaffPosition

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
              "abjad.tools.pitchtools.StaffPosition.StaffPosition" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>StaffPosition</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.StaffPosition.StaffPosition";
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

      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.number
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.to_pitch
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__copy__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__eq__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__format__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__ge__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__gt__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__hash__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__le__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__lt__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__ne__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__repr__
      ~abjad.tools.pitchtools.StaffPosition.StaffPosition.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.StaffPosition.StaffPosition.number

Methods
-------

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.to_pitch

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__copy__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__format__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__ge__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__gt__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__hash__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__le__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__repr__

.. automethod:: abjad.tools.pitchtools.StaffPosition.StaffPosition.__str__
