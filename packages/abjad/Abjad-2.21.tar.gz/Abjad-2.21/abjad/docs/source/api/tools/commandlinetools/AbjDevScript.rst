.. currentmodule:: abjad.tools.commandlinetools

AbjDevScript
============

.. autoclass:: AbjDevScript

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
              "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AbjDevScript</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" [color=3,
                  group=2,
                  label=CommandlineScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" -> "abjad.tools.commandlinetools.AbjDevScript.AbjDevScript";
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

      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.argument_parser
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.commandline_script_aliases
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.commandline_script_classes
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.commandline_script_program_names
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.formatted_help
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.formatted_usage
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.formatted_version
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.list_commandline_script_classes
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.program_name
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__call__
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__eq__
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__format__
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__hash__
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__ne__
      ~abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.argument_parser

.. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.commandline_script_aliases

.. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.commandline_script_classes

.. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.commandline_script_program_names

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.formatted_version

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.program_name

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.list_commandline_script_classes

Special methods
---------------

.. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.commandlinetools.AbjDevScript.AbjDevScript.__repr__
