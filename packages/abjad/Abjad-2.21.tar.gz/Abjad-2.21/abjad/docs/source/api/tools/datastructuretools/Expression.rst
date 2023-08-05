.. currentmodule:: abjad.tools.datastructuretools

Expression
==========

.. autoclass:: Expression

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
              "abjad.tools.datastructuretools.Expression.Expression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Expression</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.datastructuretools.Expression.Expression";
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

      ~abjad.tools.datastructuretools.Expression.Expression.append_callback
      ~abjad.tools.datastructuretools.Expression.Expression.argument_count
      ~abjad.tools.datastructuretools.Expression.Expression.argument_values
      ~abjad.tools.datastructuretools.Expression.Expression.callbacks
      ~abjad.tools.datastructuretools.Expression.Expression.establish_equivalence
      ~abjad.tools.datastructuretools.Expression.Expression.evaluation_template
      ~abjad.tools.datastructuretools.Expression.Expression.force_return
      ~abjad.tools.datastructuretools.Expression.Expression.get_markup
      ~abjad.tools.datastructuretools.Expression.Expression.get_string
      ~abjad.tools.datastructuretools.Expression.Expression.has_parentheses
      ~abjad.tools.datastructuretools.Expression.Expression.is_composite
      ~abjad.tools.datastructuretools.Expression.Expression.is_initializer
      ~abjad.tools.datastructuretools.Expression.Expression.is_postfix
      ~abjad.tools.datastructuretools.Expression.Expression.iterate
      ~abjad.tools.datastructuretools.Expression.Expression.keywords
      ~abjad.tools.datastructuretools.Expression.Expression.label
      ~abjad.tools.datastructuretools.Expression.Expression.make_callback
      ~abjad.tools.datastructuretools.Expression.Expression.map_operand
      ~abjad.tools.datastructuretools.Expression.Expression.markup_maker_callback
      ~abjad.tools.datastructuretools.Expression.Expression.module_names
      ~abjad.tools.datastructuretools.Expression.Expression.name
      ~abjad.tools.datastructuretools.Expression.Expression.next_name
      ~abjad.tools.datastructuretools.Expression.Expression.pitch_class_segment
      ~abjad.tools.datastructuretools.Expression.Expression.precedence
      ~abjad.tools.datastructuretools.Expression.Expression.proxy_class
      ~abjad.tools.datastructuretools.Expression.Expression.qualified_method_name
      ~abjad.tools.datastructuretools.Expression.Expression.sequence
      ~abjad.tools.datastructuretools.Expression.Expression.string_template
      ~abjad.tools.datastructuretools.Expression.Expression.subclass_hook
      ~abjad.tools.datastructuretools.Expression.Expression.subexpressions
      ~abjad.tools.datastructuretools.Expression.Expression.wrap_in_list
      ~abjad.tools.datastructuretools.Expression.Expression.__add__
      ~abjad.tools.datastructuretools.Expression.Expression.__call__
      ~abjad.tools.datastructuretools.Expression.Expression.__copy__
      ~abjad.tools.datastructuretools.Expression.Expression.__eq__
      ~abjad.tools.datastructuretools.Expression.Expression.__format__
      ~abjad.tools.datastructuretools.Expression.Expression.__getattr__
      ~abjad.tools.datastructuretools.Expression.Expression.__getitem__
      ~abjad.tools.datastructuretools.Expression.Expression.__hash__
      ~abjad.tools.datastructuretools.Expression.Expression.__iadd__
      ~abjad.tools.datastructuretools.Expression.Expression.__ne__
      ~abjad.tools.datastructuretools.Expression.Expression.__radd__
      ~abjad.tools.datastructuretools.Expression.Expression.__repr__
      ~abjad.tools.datastructuretools.Expression.Expression.__setitem__
      ~abjad.tools.datastructuretools.Expression.Expression.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.argument_count

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.argument_values

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.callbacks

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.evaluation_template

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.force_return

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.has_parentheses

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.is_composite

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.is_initializer

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.is_postfix

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.keywords

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.map_operand

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.markup_maker_callback

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.module_names

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.name

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.next_name

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.precedence

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.proxy_class

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.qualified_method_name

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.string_template

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.subclass_hook

.. autoattribute:: abjad.tools.datastructuretools.Expression.Expression.subexpressions

Methods
-------

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.append_callback

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.establish_equivalence

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.get_markup

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.get_string

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.iterate

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.label

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.pitch_class_segment

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.sequence

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.wrap_in_list

Class & static methods
----------------------

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.make_callback

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__add__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Expression.Expression.__copy__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__eq__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__format__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__getattr__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__getitem__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__hash__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Expression.Expression.__ne__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__radd__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__repr__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__setitem__

.. automethod:: abjad.tools.datastructuretools.Expression.Expression.__str__
