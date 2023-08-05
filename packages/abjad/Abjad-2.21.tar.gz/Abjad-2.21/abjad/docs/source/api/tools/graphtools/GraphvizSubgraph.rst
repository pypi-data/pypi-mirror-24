.. currentmodule:: abjad.tools.graphtools

GraphvizSubgraph
================

.. autoclass:: GraphvizSubgraph

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
              "abjad.tools.graphtools.GraphvizGraph.GraphvizGraph" [color=4,
                  group=3,
                  label=GraphvizGraph,
                  shape=box];
              "abjad.tools.graphtools.GraphvizMixin.GraphvizMixin" [color=4,
                  group=3,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizSubgraph</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.graphtools.GraphvizGraph`

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

      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.append
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.attributes
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.canonical_name
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.children
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.depth
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.depthwise_inventory
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.edge_attributes
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.edges
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.extend
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.graph_order
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.improper_parentage
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.index
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.insert
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.is_cluster
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.is_digraph
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.leaves
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.name
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.node_attributes
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.nodes
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.parent
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.pop
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.proper_parentage
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.remove
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.root
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.unflattened_graphviz_format
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__contains__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__copy__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__delitem__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__eq__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__format__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__getitem__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__graph__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__hash__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__iter__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__len__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__ne__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__repr__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__setitem__
      ~abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.attributes

.. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.canonical_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.edge_attributes

.. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.edges

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.node_attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.root

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.unflattened_graphviz_format

Read/write properties
---------------------

.. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.is_cluster

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.is_digraph

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizSubgraph.GraphvizSubgraph.__str__
