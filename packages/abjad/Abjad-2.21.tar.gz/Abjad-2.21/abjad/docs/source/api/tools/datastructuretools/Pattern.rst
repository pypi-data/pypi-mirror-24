.. currentmodule:: abjad.tools.datastructuretools

Pattern
=======

.. autoclass:: Pattern

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.Pattern.Pattern" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Pattern</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Pattern.Pattern";
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

      ~abjad.tools.datastructuretools.Pattern.Pattern.from_vector
      ~abjad.tools.datastructuretools.Pattern.Pattern.get_boolean_vector
      ~abjad.tools.datastructuretools.Pattern.Pattern.get_matching_items
      ~abjad.tools.datastructuretools.Pattern.Pattern.index
      ~abjad.tools.datastructuretools.Pattern.Pattern.index_all
      ~abjad.tools.datastructuretools.Pattern.Pattern.index_every
      ~abjad.tools.datastructuretools.Pattern.Pattern.index_first
      ~abjad.tools.datastructuretools.Pattern.Pattern.index_last
      ~abjad.tools.datastructuretools.Pattern.Pattern.indices
      ~abjad.tools.datastructuretools.Pattern.Pattern.inverted
      ~abjad.tools.datastructuretools.Pattern.Pattern.matches_index
      ~abjad.tools.datastructuretools.Pattern.Pattern.operator
      ~abjad.tools.datastructuretools.Pattern.Pattern.patterns
      ~abjad.tools.datastructuretools.Pattern.Pattern.payload
      ~abjad.tools.datastructuretools.Pattern.Pattern.period
      ~abjad.tools.datastructuretools.Pattern.Pattern.reverse
      ~abjad.tools.datastructuretools.Pattern.Pattern.rotate
      ~abjad.tools.datastructuretools.Pattern.Pattern.weight
      ~abjad.tools.datastructuretools.Pattern.Pattern.__and__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__copy__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__eq__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__format__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__hash__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__invert__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__len__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__ne__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__or__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__repr__
      ~abjad.tools.datastructuretools.Pattern.Pattern.__xor__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.indices

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.inverted

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.operator

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.patterns

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.payload

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.period

.. autoattribute:: abjad.tools.datastructuretools.Pattern.Pattern.weight

Methods
-------

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.get_boolean_vector

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.get_matching_items

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.matches_index

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.reverse

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.rotate

Class & static methods
----------------------

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.from_vector

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.index

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.index_all

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.index_every

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.index_first

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.index_last

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__hash__

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__invert__

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__ne__

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__repr__

.. automethod:: abjad.tools.datastructuretools.Pattern.Pattern.__xor__
