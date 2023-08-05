.. currentmodule:: abjad.tools.templatetools

GroupedStavesScoreTemplate
==========================

.. autoclass:: GroupedStavesScoreTemplate

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
          subgraph cluster_templatetools {
              graph [label=templatetools];
              "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>GroupedStavesScoreTemplate</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate";
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

      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.context_name_abbreviations
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.staff_count
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__call__
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__copy__
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__eq__
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__format__
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__hash__
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__ne__
      ~abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.context_name_abbreviations

.. autoattribute:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.staff_count

Special methods
---------------

.. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate.__repr__
