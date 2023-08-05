.. currentmodule:: abjad.tools.tonalanalysistools

ScaleDegree
===========

.. autoclass:: ScaleDegree

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
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ScaleDegree</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree";
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

      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.accidental
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.from_accidental_and_number
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.name
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.number
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.roman_numeral_string
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.string
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.title_string
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__copy__
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__eq__
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__format__
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__hash__
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__ne__
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__repr__
      ~abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.accidental

.. autoattribute:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.name

.. autoattribute:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.number

.. autoattribute:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.roman_numeral_string

.. autoattribute:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.string

.. autoattribute:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.title_string

Class & static methods
----------------------

.. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.from_accidental_and_number

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__copy__

.. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__format__

.. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__repr__

.. automethod:: abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree.__str__
