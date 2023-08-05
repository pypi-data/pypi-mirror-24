.. currentmodule:: abjad.tools.pitchtools

SetClass
========

.. autoclass:: SetClass

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
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.SetClass.SetClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SetClass</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.SetClass.SetClass";
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

      ~abjad.tools.pitchtools.SetClass.SetClass.cardinality
      ~abjad.tools.pitchtools.SetClass.SetClass.from_pitch_class_set
      ~abjad.tools.pitchtools.SetClass.SetClass.is_inversion_equivalent
      ~abjad.tools.pitchtools.SetClass.SetClass.lex_rank
      ~abjad.tools.pitchtools.SetClass.SetClass.list_set_classes
      ~abjad.tools.pitchtools.SetClass.SetClass.prime_form
      ~abjad.tools.pitchtools.SetClass.SetClass.rank
      ~abjad.tools.pitchtools.SetClass.SetClass.transposition_only
      ~abjad.tools.pitchtools.SetClass.SetClass.__copy__
      ~abjad.tools.pitchtools.SetClass.SetClass.__eq__
      ~abjad.tools.pitchtools.SetClass.SetClass.__format__
      ~abjad.tools.pitchtools.SetClass.SetClass.__hash__
      ~abjad.tools.pitchtools.SetClass.SetClass.__ne__
      ~abjad.tools.pitchtools.SetClass.SetClass.__repr__
      ~abjad.tools.pitchtools.SetClass.SetClass.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.SetClass.SetClass.cardinality

.. autoattribute:: abjad.tools.pitchtools.SetClass.SetClass.is_inversion_equivalent

.. autoattribute:: abjad.tools.pitchtools.SetClass.SetClass.lex_rank

.. autoattribute:: abjad.tools.pitchtools.SetClass.SetClass.prime_form

.. autoattribute:: abjad.tools.pitchtools.SetClass.SetClass.rank

.. autoattribute:: abjad.tools.pitchtools.SetClass.SetClass.transposition_only

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.SetClass.SetClass.from_pitch_class_set

.. automethod:: abjad.tools.pitchtools.SetClass.SetClass.list_set_classes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__repr__

.. automethod:: abjad.tools.pitchtools.SetClass.SetClass.__str__
