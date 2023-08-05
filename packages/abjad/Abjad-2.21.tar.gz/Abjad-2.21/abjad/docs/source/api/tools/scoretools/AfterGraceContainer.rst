.. currentmodule:: abjad.tools.scoretools

AfterGraceContainer
===================

.. autoclass:: AfterGraceContainer

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AfterGraceContainer</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=3,
                  group=2,
                  label=Container,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.append
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.extend
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.index
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.insert
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.is_simultaneous
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.name
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.pop
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.remove
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.reverse
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__contains__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__copy__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__delitem__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__eq__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__format__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__getitem__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__graph__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__hash__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__illustrate__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__iter__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__len__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__mul__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__ne__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__repr__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__rmul__
      ~abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__setitem__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.reverse

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AfterGraceContainer.AfterGraceContainer.__setitem__
