.. currentmodule:: abjad.tools.selectortools

SelectorLibrary
===============

.. autoclass:: SelectorLibrary

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
          subgraph cluster_selectortools {
              graph [label=selectortools];
              "abjad.tools.selectortools.SelectorLibrary.SelectorLibrary" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>SelectorLibrary</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.selectortools.SelectorLibrary.SelectorLibrary";
      }

Bases
-----

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_first_logical_tie_in_pitched_runs
      ~abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_last_logical_tie_in_pitched_runs
      ~abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_nonfirst_logical_ties_in_pitched_runs
      ~abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_nonlast_logical_ties_in_pitched_runs
      ~abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_pitched_runs

Class & static methods
----------------------

.. automethod:: abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_first_logical_tie_in_pitched_runs

.. automethod:: abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_last_logical_tie_in_pitched_runs

.. automethod:: abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_nonfirst_logical_ties_in_pitched_runs

.. automethod:: abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_nonlast_logical_ties_in_pitched_runs

.. automethod:: abjad.tools.selectortools.SelectorLibrary.SelectorLibrary.select_pitched_runs
