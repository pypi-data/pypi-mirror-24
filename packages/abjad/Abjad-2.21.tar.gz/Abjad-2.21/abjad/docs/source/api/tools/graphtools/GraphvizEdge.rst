.. currentmodule:: abjad.tools.graphtools

GraphvizEdge
============

.. autoclass:: GraphvizEdge

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
          subgraph cluster_graphtools {
              graph [label=graphtools];
              "abjad.tools.graphtools.GraphvizEdge.GraphvizEdge" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>GraphvizEdge</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" [color=3,
                  group=2,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizEdge.GraphvizEdge";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.graphtools.GraphvizMixin`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.attach
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.attributes
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.detach
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.head
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.head_port_position
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.is_directed
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.tail
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.tail_port_position
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__eq__
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__format__
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__hash__
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__ne__
      ~abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.attributes

.. autoattribute:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.head

.. autoattribute:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.tail

Read/write properties
---------------------

.. autoattribute:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.head_port_position

.. autoattribute:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.is_directed

.. autoattribute:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.tail_port_position

Methods
-------

.. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.attach

.. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.detach

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizEdge.GraphvizEdge.__repr__
