.. currentmodule:: abjad.tools.commandlinetools

ManageMaterialScript
====================

.. autoclass:: ManageMaterialScript

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
              "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ManageMaterialScript</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" [color=3,
                  group=2,
                  label=ScorePackageScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript";
              "abjad.tools.commandlinetools.ScorePackageScript.ScorePackageScript" -> "abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript";
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

- :py:class:`abjad.tools.commandlinetools.ScorePackageScript`

- :py:class:`abjad.tools.commandlinetools.CommandlineScript`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.argument_parser
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.formatted_help
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.formatted_usage
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.formatted_version
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.list_commandline_script_classes
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.program_name
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__call__
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__eq__
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__format__
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__hash__
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__ne__
      ~abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.formatted_version

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.program_name

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.list_commandline_script_classes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.ManageMaterialScript.ManageMaterialScript.__repr__
