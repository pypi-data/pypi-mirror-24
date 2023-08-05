.. currentmodule:: abjad.tools.systemtools

IndicatorWrapper
================

.. autoclass:: IndicatorWrapper

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>IndicatorWrapper</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper";
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

      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.component
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.indicator
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.is_annotation
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.is_piecewise
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.name
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.piecewise_spanner
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.scope
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.start_offset
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.synthetic_offset
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__copy__
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__eq__
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__format__
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__hash__
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__ne__
      ~abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.component

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.indicator

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.is_annotation

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.is_piecewise

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.name

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.piecewise_spanner

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.scope

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.start_offset

.. autoattribute:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.synthetic_offset

Special methods
---------------

.. automethod:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper.__repr__
