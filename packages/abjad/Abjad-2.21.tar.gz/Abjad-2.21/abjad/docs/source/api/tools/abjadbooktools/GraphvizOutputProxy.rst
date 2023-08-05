.. currentmodule:: abjad.tools.abjadbooktools

GraphvizOutputProxy
===================

.. autoclass:: GraphvizOutputProxy

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
              "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>GraphvizOutputProxy</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" [color=2,
                  group=1,
                  label=ImageOutputProxy,
                  shape=oval,
                  style=bold];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abjadbooktools.ImageOutputProxy`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.as_docutils
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.as_latex
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.file_name_prefix
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.file_name_without_extension
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.image_layout_specifier
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.image_render_specifier
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.layout
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.options
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.payload
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.render_for_latex
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__copy__
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__eq__
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__format__
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__hash__
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__ne__
      ~abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.file_name_prefix

.. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.file_name_without_extension

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.image_layout_specifier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.image_render_specifier

.. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.layout

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.payload

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.as_docutils

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.as_latex

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.render_for_latex

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy.__repr__
