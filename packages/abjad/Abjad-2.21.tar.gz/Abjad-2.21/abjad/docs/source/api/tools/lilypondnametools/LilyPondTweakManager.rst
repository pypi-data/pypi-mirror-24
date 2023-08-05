.. currentmodule:: abjad.tools.lilypondnametools

LilyPondTweakManager
====================

.. autoclass:: LilyPondTweakManager

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
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" [color=2,
                  group=1,
                  label=LilyPondNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>LilyPondTweakManager</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.lilypondnametools.LilyPondNameManager`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager.__eq__
      ~abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager.__hash__
      ~abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager.__repr__

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondTweakManager.LilyPondTweakManager.__repr__
