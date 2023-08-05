.. currentmodule:: abjad.tools.scoretools

AcciaccaturaContainer
=====================

.. autoclass:: AcciaccaturaContainer

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
              "abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AcciaccaturaContainer</B>>,
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
              "abjad.tools.scoretools.GraceContainer.GraceContainer" -> "abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer";
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

      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.append
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.extend
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.index
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.insert
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.is_simultaneous
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.name
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.pop
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.remove
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.reverse
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__contains__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__copy__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__delitem__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__eq__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__format__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__getitem__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__graph__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__hash__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__illustrate__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__iter__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__len__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__mul__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__ne__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__repr__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__rmul__
      ~abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__setitem__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.reverse

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.AcciaccaturaContainer.AcciaccaturaContainer.__setitem__
