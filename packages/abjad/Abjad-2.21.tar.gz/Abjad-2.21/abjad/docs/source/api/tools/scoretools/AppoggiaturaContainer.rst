.. currentmodule:: abjad.tools.scoretools

AppoggiaturaContainer
=====================

.. autoclass:: AppoggiaturaContainer

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
              "abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AppoggiaturaContainer</B>>,
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
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=3,
                  group=2,
                  label=GraceContainer,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.GraceContainer.GraceContainer";
              "abjad.tools.scoretools.GraceContainer.GraceContainer" -> "abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer";
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

- :py:class:`abjad.tools.scoretools.GraceContainer`

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.append
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.extend
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.index
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.insert
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.is_simultaneous
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.name
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.pop
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.remove
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.reverse
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__contains__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__copy__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__delitem__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__eq__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__format__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__getitem__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__graph__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__hash__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__illustrate__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__iter__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__len__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__mul__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__ne__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__repr__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__rmul__
      ~abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__setitem__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.reverse

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AppoggiaturaContainer.AppoggiaturaContainer.__setitem__
