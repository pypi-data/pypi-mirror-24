.. currentmodule:: abjad.tools.commandlinetools

CommandlineScript
=================

.. autoclass:: CommandlineScript

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
              "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript" [color=4,
                  group=3,
                  label=AbjDevScript,
                  shape=box];
              "abjad.tools.commandlinetools.BuildApiScript.BuildApiScript" [color=4,
                  group=3,
                  label=BuildApiScript,
                  shape=box];
              "abjad.tools.commandlinetools.CheckClassSections.CheckClassSections" [color=4,
                  group=3,
                  label=CheckClassSections,
                  shape=box];
              "abjad.tools.commandlinetools.CleanScript.CleanScript" [color=4,
                  group=3,
                  label=CleanScript,
                  shape=box];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>CommandlineScript</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.DoctestScript.DoctestScript" [color=4,
                  group=3,
                  label=DoctestScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript" [color=4,
                  group=3,
                  label=ManageBuildTargetScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript" [color=4,
                  group=3,
                  label=ManageMaterialScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript" [color=4,
                  group=3,
                  label=ManageScoreScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript" [color=4,
                  group=3,
                  label=ManageSegmentScript,
                  shape=box];
              "abjad.tools.commandlinetools.ReplaceScript.ReplaceScript" [color=4,
                  group=3,
                  label=ReplaceScript,
                  shape=box];
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" [color=4,
                  group=3,
                  label=ScorePackageScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.commandlinetools.StatsScript.StatsScript" [color=4,
                  group=3,
                  label=StatsScript,
                  shape=box];
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

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.argument_parser
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.formatted_help
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.formatted_usage
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.formatted_version
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.list_commandline_script_classes
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.program_name
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__call__
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__eq__
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__format__
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__hash__
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__ne__
      ~abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.argument_parser

.. autoattribute:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.formatted_help

.. autoattribute:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.formatted_usage

.. autoattribute:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.formatted_version

.. autoattribute:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.program_name

Class & static methods
----------------------

.. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.list_commandline_script_classes

Special methods
---------------

.. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.CommandlineScript.CommandlineScript.__repr__
