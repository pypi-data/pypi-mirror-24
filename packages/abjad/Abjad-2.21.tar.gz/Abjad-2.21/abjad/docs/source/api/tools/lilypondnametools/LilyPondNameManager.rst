.. currentmodule:: abjad.tools.lilypondnametools

LilyPondNameManager
===================

.. autoclass:: LilyPondNameManager

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
          subgraph cluster_lilypondnametools {
              graph [label=lilypondnametools];
              "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager" [color=2,
                  group=1,
                  label=LilyPondGrobNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>LilyPondNameManager</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager" [color=2,
                  group=1,
                  label=LilyPondSettingNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager" [color=2,
                  group=1,
                  label=LilyPondTweakManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager";
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager";
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager";
      }

Bases
-----

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__eq__
      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__hash__
      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__repr__

Special methods
---------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__eq__

.. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__hash__

.. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__repr__
