.. currentmodule:: abjad.tools.systemtools

FormatSpecification
===================

.. autoclass:: FormatSpecification

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.FormatSpecification.FormatSpecification" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>FormatSpecification</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.FormatSpecification.FormatSpecification";
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

      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.client
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.coerce_for_equality
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_args_values
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_is_bracketed
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_is_indented
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_kwargs_names
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_text
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_args_values
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_includes_root_package
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_is_bracketed
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_is_indented
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_kwargs_names
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_text
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.template_names
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.__copy__
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.__eq__
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.__format__
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.__hash__
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.__ne__
      ~abjad.tools.systemtools.FormatSpecification.FormatSpecification.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.client

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.coerce_for_equality

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_args_values

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_is_bracketed

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_is_indented

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_kwargs_names

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.repr_text

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_args_values

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_includes_root_package

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_is_bracketed

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_is_indented

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_kwargs_names

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.storage_format_text

.. autoattribute:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.template_names

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.FormatSpecification.FormatSpecification.__repr__
