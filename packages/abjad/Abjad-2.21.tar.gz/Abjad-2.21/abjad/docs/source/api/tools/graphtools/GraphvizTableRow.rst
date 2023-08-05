.. currentmodule:: abjad.tools.graphtools

GraphvizTableRow
================

.. autoclass:: GraphvizTableRow

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
              "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizTableRow</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.append
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.children
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.depth
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.depthwise_inventory
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.extend
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.graph_order
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.improper_parentage
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.index
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.insert
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.leaves
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.name
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.nodes
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.parent
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.pop
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.proper_parentage
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.remove
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.root
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__contains__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__copy__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__delitem__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__eq__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__format__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__getitem__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__hash__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__iter__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__len__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__ne__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__repr__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__setitem__
      ~abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__setitem__

.. automethod:: abjad.tools.graphtools.GraphvizTableRow.GraphvizTableRow.__str__
