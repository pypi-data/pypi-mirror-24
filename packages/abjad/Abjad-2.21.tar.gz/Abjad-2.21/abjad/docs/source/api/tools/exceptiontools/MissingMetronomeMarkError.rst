.. currentmodule:: abjad.tools.exceptiontools

MissingMetronomeMarkError
=========================

.. autoclass:: MissingMetronomeMarkError

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
          subgraph cluster_exceptiontools {
              graph [label=exceptiontools];
              "abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>MissingMetronomeMarkError</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.BaseException" [color=1,
                  group=0,
                  label=BaseException,
                  shape=box];
              "builtins.Exception" [color=1,
                  group=0,
                  label=Exception,
                  shape=box];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
              "builtins.BaseException" -> "builtins.Exception";
              "builtins.object" -> "builtins.BaseException";
          }
          "builtins.Exception" -> "abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError";
      }

Bases
-----

- :py:class:`builtins.Exception`

- :py:class:`builtins.BaseException`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.with_traceback
      ~abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__delattr__
      ~abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__new__
      ~abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__repr__
      ~abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__setattr__
      ~abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__str__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.with_traceback

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__delattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__setattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingMetronomeMarkError.MissingMetronomeMarkError.__str__
