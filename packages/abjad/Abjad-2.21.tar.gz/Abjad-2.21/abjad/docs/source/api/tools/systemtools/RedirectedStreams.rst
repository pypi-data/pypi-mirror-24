.. currentmodule:: abjad.tools.systemtools

RedirectedStreams
=================

.. autoclass:: RedirectedStreams

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
              "abjad.tools.abctools.ContextManager.ContextManager" [color=1,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>RedirectedStreams</B>>,
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
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.ContextManager`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.stderr
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.stdout
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__enter__
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__eq__
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__exit__
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__format__
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__hash__
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__ne__
      ~abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.stderr

.. autoattribute:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.stdout

Special methods
---------------

.. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__enter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__eq__

.. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__exit__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__ne__

.. automethod:: abjad.tools.systemtools.RedirectedStreams.RedirectedStreams.__repr__
