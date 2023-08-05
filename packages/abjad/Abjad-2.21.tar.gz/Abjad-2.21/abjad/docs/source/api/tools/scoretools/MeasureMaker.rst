.. currentmodule:: abjad.tools.scoretools

MeasureMaker
============

.. autoclass:: MeasureMaker

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.MeasureMaker.MeasureMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MeasureMaker</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.scoretools.MeasureMaker.MeasureMaker";
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

      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.implicit_scaling
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__call__
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__copy__
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__eq__
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__format__
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__hash__
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__ne__
      ~abjad.tools.scoretools.MeasureMaker.MeasureMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.implicit_scaling

Special methods
---------------

.. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.MeasureMaker.MeasureMaker.__repr__
