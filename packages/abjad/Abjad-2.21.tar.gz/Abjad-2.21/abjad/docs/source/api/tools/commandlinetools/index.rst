commandlinetools
================

.. automodule:: abjad.tools.commandlinetools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=2,
                  group=1,
                  label=AbjadBookScript,
                  shape=box];
          }
          subgraph cluster_commandlinetools {
              graph [label=commandlinetools];
              "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AbjDevScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.BuildApiScript.BuildApiScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BuildApiScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.CheckClassSections.CheckClassSections" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CheckClassSections,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.CleanScript.CleanScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CleanScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CommandlineScript,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.DoctestScript.DoctestScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DoctestScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ManageBuildTargetScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ManageMaterialScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ManageScoreScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ManageSegmentScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ReplaceScript.ReplaceScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReplaceScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ScorePackageScript,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.StatsScript.StatsScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StatsScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.BuildApiScript.BuildApiScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.CheckClassSections.CheckClassSections";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.CleanScript.CleanScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.DoctestScript.DoctestScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.ReplaceScript.ReplaceScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript";
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.StatsScript.StatsScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript";
          "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   CommandlineScript
   ScorePackageScript

.. autosummary::
   :nosignatures:

   CommandlineScript
   ScorePackageScript

--------

Classes
-------

.. toctree::
   :hidden:

   AbjDevScript
   BuildApiScript
   CheckClassSections
   CleanScript
   DoctestScript
   ManageBuildTargetScript
   ManageMaterialScript
   ManageScoreScript
   ManageSegmentScript
   ReplaceScript
   StatsScript

.. autosummary::
   :nosignatures:

   AbjDevScript
   BuildApiScript
   CheckClassSections
   CleanScript
   DoctestScript
   ManageBuildTargetScript
   ManageMaterialScript
   ManageScoreScript
   ManageSegmentScript
   ReplaceScript
   StatsScript

--------

Functions
---------

.. toctree::
   :hidden:

   run_ajv

.. autosummary::
   :nosignatures:

   run_ajv
