.. currentmodule:: abjad.tools.commandlinetools

ScorePackageScript
==================

.. autoclass:: ScorePackageScript

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
          subgraph cluster_commandlinetools {
              graph [label=commandlinetools];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" [color=3,
                  group=2,
                  label=CommandlineScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript" [color=3,
                  group=2,
                  label=ManageBuildTargetScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript" [color=3,
                  group=2,
                  label=ManageMaterialScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript" [color=3,
                  group=2,
                  label=ManageScoreScript,
                  shape=box];
              "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript" [color=3,
                  group=2,
                  label=ManageSegmentScript,
                  shape=box];
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ScorePackageScript</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageBuildTargetScript.ManageBuildTargetScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageScoreScript.ManageScoreScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageSegmentScript.ManageSegmentScript";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.commandlinetools.CommandlineScript`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.argument_parser
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.formatted_help
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.formatted_usage
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.formatted_version
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.list_commandline_script_classes
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.program_name
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__call__
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__eq__
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__format__
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__hash__
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__ne__
      ~abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.formatted_version

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.program_name

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.list_commandline_script_classes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript.__repr__
