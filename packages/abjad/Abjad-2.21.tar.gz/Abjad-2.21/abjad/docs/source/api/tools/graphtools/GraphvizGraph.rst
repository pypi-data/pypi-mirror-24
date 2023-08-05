.. currentmodule:: abjad.tools.graphtools

GraphvizGraph
=============

.. autoclass:: GraphvizGraph

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
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=3,
                  group=2,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_graphtools {
              graph [label=graphtools];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizGraph</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" [color=4,
                  group=3,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph" [color=4,
                  group=3,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.graphtools.GraphvizMixin`

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.append
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.attributes
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.canonical_name
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.children
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.depth
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.depthwise_inventory
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.edge_attributes
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.extend
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.graph_order
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.improper_parentage
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.index
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.insert
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.is_digraph
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.leaves
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.name
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.node_attributes
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.nodes
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.parent
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.pop
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.proper_parentage
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.remove
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.root
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.unflattened_graphviz_format
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__contains__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__copy__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__delitem__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__eq__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__format__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__getitem__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__graph__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__hash__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__iter__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__len__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__ne__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__repr__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__setitem__
      ~abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.attributes

.. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.canonical_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.depthwise_inventory

.. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.edge_attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.leaves

.. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.node_attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.root

.. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.unflattened_graphviz_format

Read/write properties
---------------------

.. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.is_digraph

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__contains__

.. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__getitem__

.. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__setitem__

.. automethod:: abjad.tools.graphtools.GraphvizGraph.GraphvizGraph.__str__
