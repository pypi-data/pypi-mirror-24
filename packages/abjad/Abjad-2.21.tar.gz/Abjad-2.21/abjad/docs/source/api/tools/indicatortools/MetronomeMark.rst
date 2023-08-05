.. currentmodule:: abjad.tools.indicatortools

MetronomeMark
=============

.. autoclass:: MetronomeMark

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
              "abjad.tools.indicatortools.MetronomeMark.MetronomeMark" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MetronomeMark</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.MetronomeMark.MetronomeMark";
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

      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.custom_markup
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.default_scope
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.duration_to_milliseconds
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.is_imprecise
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.list_related_tempos
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.make_tempo_equation_markup
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.quarters_per_minute
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.reference_duration
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.rewrite_duration
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.textual_indication
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.units_per_minute
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__add__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__copy__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__div__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__eq__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__format__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__ge__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__gt__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__hash__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__le__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__lt__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__mul__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__ne__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__radd__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__repr__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__rmul__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__str__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__sub__
      ~abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__truediv__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.custom_markup

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.default_scope

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.is_imprecise

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.quarters_per_minute

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.reference_duration

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.textual_indication

.. autoattribute:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.units_per_minute

Methods
-------

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.duration_to_milliseconds

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.list_related_tempos

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.rewrite_duration

Class & static methods
----------------------

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.make_tempo_equation_markup

Special methods
---------------

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__copy__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__div__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__eq__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__format__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__ge__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__gt__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__hash__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__le__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__lt__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__ne__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__repr__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__rmul__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__str__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__sub__

.. automethod:: abjad.tools.indicatortools.MetronomeMark.MetronomeMark.__truediv__
