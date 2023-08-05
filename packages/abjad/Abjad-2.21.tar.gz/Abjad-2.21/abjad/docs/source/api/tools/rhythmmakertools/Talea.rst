.. currentmodule:: abjad.tools.rhythmmakertools

Talea
=====

.. autoclass:: Talea

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.Talea.Talea" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Talea</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.Talea.Talea";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmmakertools.Talea.Talea.counts
      ~abjad.tools.rhythmmakertools.Talea.Talea.denominator
      ~abjad.tools.rhythmmakertools.Talea.Talea.__copy__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__eq__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__format__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__getitem__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__hash__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__iter__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__len__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__ne__
      ~abjad.tools.rhythmmakertools.Talea.Talea.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.Talea.Talea.counts

.. autoattribute:: abjad.tools.rhythmmakertools.Talea.Talea.denominator

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__format__

.. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__hash__

.. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__iter__

.. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.Talea.Talea.__repr__
