.. currentmodule:: abjad.tools.quantizationtools

ParallelJobHandlerWorker
========================

.. autoclass:: ParallelJobHandlerWorker

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ParallelJobHandlerWorker</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          subgraph cluster_multiprocessing {
              graph [label=multiprocessing];
              "multiprocessing.context.Process" [color=2,
                  group=1,
                  label=Process,
                  shape=box];
              "multiprocessing.process.BaseProcess" [color=2,
                  group=1,
                  label=BaseProcess,
                  shape=box];
              "multiprocessing.process.BaseProcess" -> "multiprocessing.context.Process";
          }
          "builtins.object" -> "multiprocessing.process.BaseProcess";
          "multiprocessing.context.Process" -> "abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker";
      }

Bases
-----

- :py:class:`multiprocessing.context.Process`

- :py:class:`multiprocessing.process.BaseProcess`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.authkey
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.daemon
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.exitcode
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.ident
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.is_alive
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.join
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.name
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.pid
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.run
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.sentinel
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.start
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.terminate
      ~abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.exitcode

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.ident

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.pid

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.sentinel

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.authkey

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.daemon

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.is_alive

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.join

.. automethod:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.run

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.start

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.terminate

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker.__repr__
