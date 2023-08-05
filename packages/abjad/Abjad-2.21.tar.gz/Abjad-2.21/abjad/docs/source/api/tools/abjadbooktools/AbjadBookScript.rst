.. currentmodule:: abjad.tools.abjadbooktools

AbjadBookScript
===============

.. autoclass:: AbjadBookScript

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
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>AbjadBookScript</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_commandlinetools {
              graph [label=commandlinetools];
              "abjad.tools.commandlinetools.CommandlineScript.CommandlineScript" [color=4,
                  group=3,
                  label=CommandlineScript,
                  shape=oval,
                  style=bold];
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

- :py:class:`abjad.tools.commandlinetools.CommandlineScript`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.argument_parser
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_help
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_usage
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_version
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.list_commandline_script_classes
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.program_name
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__call__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__eq__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__format__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__hash__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__ne__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_version

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.program_name

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.list_commandline_script_classes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__repr__
