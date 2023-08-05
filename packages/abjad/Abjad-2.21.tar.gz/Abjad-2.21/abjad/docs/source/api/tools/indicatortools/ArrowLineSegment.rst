.. currentmodule:: abjad.tools.indicatortools

ArrowLineSegment
================

.. autoclass:: ArrowLineSegment

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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ArrowLineSegment</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LineSegment.LineSegment" [color=3,
                  group=2,
                  label=LineSegment,
                  shape=box];
              "abjad.tools.indicatortools.LineSegment.LineSegment" -> "abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LineSegment.LineSegment";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.indicatortools.LineSegment`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.arrow_width
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.dash_fraction
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.dash_period
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_broken_padding
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_broken_text
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_hspace
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_padding
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_stencil_align_direction_y
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_arrow
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_broken_arrow
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_broken_padding
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_padding
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_stencil_align_direction_y
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.style
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__copy__
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__eq__
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__format__
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__hash__
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__ne__
      ~abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.arrow_width

.. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.dash_fraction

.. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.dash_period

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_broken_padding

.. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_broken_text

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_hspace

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_padding

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.left_stencil_align_direction_y

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_arrow

.. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_broken_arrow

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_broken_padding

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_padding

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.right_stencil_align_direction_y

.. autoattribute:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.style

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ArrowLineSegment.ArrowLineSegment.__repr__
