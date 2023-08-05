.. currentmodule:: abjad.tools.abctools

ContextManager
==============

.. autoclass:: ContextManager

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
              "abjad.tools.abctools.ContextManager.ContextManager" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>ContextManager</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.FilesystemState.FilesystemState" [color=3,
                  group=2,
                  label=FilesystemState,
                  shape=box];
              "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate" [color=3,
                  group=2,
                  label=ForbidUpdate,
                  shape=box];
              "abjad.tools.systemtools.NullContextManager.NullContextManager" [color=3,
                  group=2,
                  label=NullContextManager,
                  shape=box];
              "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator" [color=3,
                  group=2,
                  label=ProgressIndicator,
                  shape=box];
              "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams" [color=3,
                  group=2,
                  label=RedirectedStreams,
                  shape=box];
              "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory" [color=3,
                  group=2,
                  label=TemporaryDirectory,
                  shape=box];
              "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange" [color=3,
                  group=2,
                  label=TemporaryDirectoryChange,
                  shape=box];
              "abjad.tools.systemtools.Timer.Timer" [color=3,
                  group=2,
                  label=Timer,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.FilesystemState.FilesystemState";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.NullContextManager.NullContextManager";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.Timer.Timer";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abctools.ContextManager.ContextManager.__enter__
      ~abjad.tools.abctools.ContextManager.ContextManager.__eq__
      ~abjad.tools.abctools.ContextManager.ContextManager.__exit__
      ~abjad.tools.abctools.ContextManager.ContextManager.__format__
      ~abjad.tools.abctools.ContextManager.ContextManager.__hash__
      ~abjad.tools.abctools.ContextManager.ContextManager.__ne__
      ~abjad.tools.abctools.ContextManager.ContextManager.__repr__

Special methods
---------------

.. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__enter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__eq__

.. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__exit__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.ContextManager.ContextManager.__repr__
