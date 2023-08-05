.. currentmodule:: abjad.tools.abjadbooktools

LilyPondBlock
=============

.. autoclass:: LilyPondBlock

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
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>LilyPondBlock</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock";
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

      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.as_latex
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.from_latex_lilypond_block
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.image_layout_specifier
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.image_render_specifier
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.input_file_contents
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.interpret
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.options
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.output_proxies
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.starting_line_number
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__copy__
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__eq__
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__format__
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__hash__
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__ne__
      ~abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.image_layout_specifier

.. autoattribute:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.image_render_specifier

.. autoattribute:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.input_file_contents

.. autoattribute:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.options

.. autoattribute:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.output_proxies

.. autoattribute:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.starting_line_number

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.as_latex

.. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.interpret

Class & static methods
----------------------

.. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.from_latex_lilypond_block

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LilyPondBlock.LilyPondBlock.__repr__
