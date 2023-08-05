.. currentmodule:: abjad.tools.systemtools

Signature
=========

.. autoclass:: Signature

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
              "abjad.tools.systemtools.Signature.Signature" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Signature</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.Signature.Signature";
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

      ~abjad.tools.systemtools.Signature.Signature.argument_list_callback
      ~abjad.tools.systemtools.Signature.Signature.is_operator
      ~abjad.tools.systemtools.Signature.Signature.markup_maker_callback
      ~abjad.tools.systemtools.Signature.Signature.method_name
      ~abjad.tools.systemtools.Signature.Signature.method_name_callback
      ~abjad.tools.systemtools.Signature.Signature.string_template_callback
      ~abjad.tools.systemtools.Signature.Signature.subscript
      ~abjad.tools.systemtools.Signature.Signature.superscript
      ~abjad.tools.systemtools.Signature.Signature.__call__
      ~abjad.tools.systemtools.Signature.Signature.__copy__
      ~abjad.tools.systemtools.Signature.Signature.__eq__
      ~abjad.tools.systemtools.Signature.Signature.__format__
      ~abjad.tools.systemtools.Signature.Signature.__hash__
      ~abjad.tools.systemtools.Signature.Signature.__ne__
      ~abjad.tools.systemtools.Signature.Signature.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.argument_list_callback

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.is_operator

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.markup_maker_callback

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.method_name

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.method_name_callback

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.string_template_callback

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.subscript

.. autoattribute:: abjad.tools.systemtools.Signature.Signature.superscript

Special methods
---------------

.. automethod:: abjad.tools.systemtools.Signature.Signature.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Signature.Signature.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Signature.Signature.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Signature.Signature.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Signature.Signature.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Signature.Signature.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Signature.Signature.__repr__
