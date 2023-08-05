.. currentmodule:: abjad.tools.timespantools

TimespanList
============

.. autoclass:: TimespanList

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.TimespanList.TimespanList" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>TimespanList</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.TimespanList.TimespanList";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedList`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.timespantools.TimespanList.TimespanList.all_are_contiguous
      ~abjad.tools.timespantools.TimespanList.TimespanList.all_are_nonoverlapping
      ~abjad.tools.timespantools.TimespanList.TimespanList.all_are_well_formed
      ~abjad.tools.timespantools.TimespanList.TimespanList.append
      ~abjad.tools.timespantools.TimespanList.TimespanList.axis
      ~abjad.tools.timespantools.TimespanList.TimespanList.clip_timespan_durations
      ~abjad.tools.timespantools.TimespanList.TimespanList.compute_logical_and
      ~abjad.tools.timespantools.TimespanList.TimespanList.compute_logical_or
      ~abjad.tools.timespantools.TimespanList.TimespanList.compute_logical_xor
      ~abjad.tools.timespantools.TimespanList.TimespanList.compute_overlap_factor
      ~abjad.tools.timespantools.TimespanList.TimespanList.compute_overlap_factor_mapping
      ~abjad.tools.timespantools.TimespanList.TimespanList.count
      ~abjad.tools.timespantools.TimespanList.TimespanList.count_offsets
      ~abjad.tools.timespantools.TimespanList.TimespanList.duration
      ~abjad.tools.timespantools.TimespanList.TimespanList.explode
      ~abjad.tools.timespantools.TimespanList.TimespanList.extend
      ~abjad.tools.timespantools.TimespanList.TimespanList.get_timespan_that_satisfies_time_relation
      ~abjad.tools.timespantools.TimespanList.TimespanList.get_timespans_that_satisfy_time_relation
      ~abjad.tools.timespantools.TimespanList.TimespanList.has_timespan_that_satisfies_time_relation
      ~abjad.tools.timespantools.TimespanList.TimespanList.index
      ~abjad.tools.timespantools.TimespanList.TimespanList.insert
      ~abjad.tools.timespantools.TimespanList.TimespanList.is_sorted
      ~abjad.tools.timespantools.TimespanList.TimespanList.item_class
      ~abjad.tools.timespantools.TimespanList.TimespanList.items
      ~abjad.tools.timespantools.TimespanList.TimespanList.keep_sorted
      ~abjad.tools.timespantools.TimespanList.TimespanList.partition
      ~abjad.tools.timespantools.TimespanList.TimespanList.pop
      ~abjad.tools.timespantools.TimespanList.TimespanList.reflect
      ~abjad.tools.timespantools.TimespanList.TimespanList.remove
      ~abjad.tools.timespantools.TimespanList.TimespanList.remove_degenerate_timespans
      ~abjad.tools.timespantools.TimespanList.TimespanList.repeat_to_stop_offset
      ~abjad.tools.timespantools.TimespanList.TimespanList.reverse
      ~abjad.tools.timespantools.TimespanList.TimespanList.rotate
      ~abjad.tools.timespantools.TimespanList.TimespanList.round_offsets
      ~abjad.tools.timespantools.TimespanList.TimespanList.scale
      ~abjad.tools.timespantools.TimespanList.TimespanList.sort
      ~abjad.tools.timespantools.TimespanList.TimespanList.split_at_offset
      ~abjad.tools.timespantools.TimespanList.TimespanList.split_at_offsets
      ~abjad.tools.timespantools.TimespanList.TimespanList.start_offset
      ~abjad.tools.timespantools.TimespanList.TimespanList.stop_offset
      ~abjad.tools.timespantools.TimespanList.TimespanList.stretch
      ~abjad.tools.timespantools.TimespanList.TimespanList.timespan
      ~abjad.tools.timespantools.TimespanList.TimespanList.translate
      ~abjad.tools.timespantools.TimespanList.TimespanList.translate_offsets
      ~abjad.tools.timespantools.TimespanList.TimespanList.__and__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__contains__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__delitem__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__eq__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__format__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__getitem__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__hash__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__iadd__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__illustrate__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__invert__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__iter__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__len__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__ne__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__repr__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__reversed__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__setitem__
      ~abjad.tools.timespantools.TimespanList.TimespanList.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.all_are_contiguous

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.all_are_nonoverlapping

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.all_are_well_formed

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.axis

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.duration

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.is_sorted

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.items

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.start_offset

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.stop_offset

.. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.timespan

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanList.TimespanList.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.append

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.clip_timespan_durations

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.compute_logical_and

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.compute_logical_or

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.compute_logical_xor

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.compute_overlap_factor

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.compute_overlap_factor_mapping

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.count

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.count_offsets

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.explode

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.extend

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.get_timespan_that_satisfies_time_relation

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.get_timespans_that_satisfy_time_relation

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.has_timespan_that_satisfies_time_relation

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.insert

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.partition

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.pop

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.reflect

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.remove

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.remove_degenerate_timespans

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.repeat_to_stop_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.reverse

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.rotate

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.round_offsets

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.scale

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.sort

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.split_at_offset

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.split_at_offsets

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.stretch

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.translate

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.translate_offsets

Special methods
---------------

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__iadd__

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__illustrate__

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__invert__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__setitem__

.. automethod:: abjad.tools.timespantools.TimespanList.TimespanList.__sub__
