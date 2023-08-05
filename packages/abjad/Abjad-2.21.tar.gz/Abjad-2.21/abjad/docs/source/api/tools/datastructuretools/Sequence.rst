.. currentmodule:: abjad.tools.datastructuretools

Sequence
========

.. autoclass:: Sequence

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
              "abjad.tools.datastructuretools.Sequence.Sequence" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Sequence</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Sequence.Sequence";
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

      ~abjad.tools.datastructuretools.Sequence.Sequence.flatten
      ~abjad.tools.datastructuretools.Sequence.Sequence.group_by
      ~abjad.tools.datastructuretools.Sequence.Sequence.is_decreasing
      ~abjad.tools.datastructuretools.Sequence.Sequence.is_increasing
      ~abjad.tools.datastructuretools.Sequence.Sequence.is_permutation
      ~abjad.tools.datastructuretools.Sequence.Sequence.is_repetition_free
      ~abjad.tools.datastructuretools.Sequence.Sequence.items
      ~abjad.tools.datastructuretools.Sequence.Sequence.join
      ~abjad.tools.datastructuretools.Sequence.Sequence.map
      ~abjad.tools.datastructuretools.Sequence.Sequence.nwise
      ~abjad.tools.datastructuretools.Sequence.Sequence.partition_by_counts
      ~abjad.tools.datastructuretools.Sequence.Sequence.partition_by_ratio_of_lengths
      ~abjad.tools.datastructuretools.Sequence.Sequence.partition_by_ratio_of_weights
      ~abjad.tools.datastructuretools.Sequence.Sequence.partition_by_weights
      ~abjad.tools.datastructuretools.Sequence.Sequence.permute
      ~abjad.tools.datastructuretools.Sequence.Sequence.remove
      ~abjad.tools.datastructuretools.Sequence.Sequence.remove_repeats
      ~abjad.tools.datastructuretools.Sequence.Sequence.repeat
      ~abjad.tools.datastructuretools.Sequence.Sequence.repeat_to_length
      ~abjad.tools.datastructuretools.Sequence.Sequence.repeat_to_weight
      ~abjad.tools.datastructuretools.Sequence.Sequence.replace
      ~abjad.tools.datastructuretools.Sequence.Sequence.retain
      ~abjad.tools.datastructuretools.Sequence.Sequence.reverse
      ~abjad.tools.datastructuretools.Sequence.Sequence.rotate
      ~abjad.tools.datastructuretools.Sequence.Sequence.sort
      ~abjad.tools.datastructuretools.Sequence.Sequence.split
      ~abjad.tools.datastructuretools.Sequence.Sequence.sum
      ~abjad.tools.datastructuretools.Sequence.Sequence.sum_by_sign
      ~abjad.tools.datastructuretools.Sequence.Sequence.truncate
      ~abjad.tools.datastructuretools.Sequence.Sequence.zip
      ~abjad.tools.datastructuretools.Sequence.Sequence.__add__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__copy__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__eq__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__format__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__getitem__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__hash__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__len__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__ne__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__radd__
      ~abjad.tools.datastructuretools.Sequence.Sequence.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.Sequence.Sequence.items

Methods
-------

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.flatten

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.group_by

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.is_decreasing

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.is_increasing

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.is_permutation

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.is_repetition_free

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.join

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.map

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.nwise

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.partition_by_counts

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.partition_by_ratio_of_lengths

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.partition_by_ratio_of_weights

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.partition_by_weights

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.permute

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.remove

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.remove_repeats

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.repeat

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.repeat_to_length

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.repeat_to_weight

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.replace

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.retain

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.reverse

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.rotate

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.sort

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.split

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.sum

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.sum_by_sign

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.truncate

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.zip

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__copy__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__eq__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__format__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__getitem__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__hash__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__ne__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__radd__

.. automethod:: abjad.tools.datastructuretools.Sequence.Sequence.__repr__
