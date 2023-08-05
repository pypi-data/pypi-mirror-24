.. currentmodule:: abjad.tools.systemtools

StorageFormatAgent
==================

.. autoclass:: StorageFormatAgent

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>StorageFormatAgent</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent";
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

      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.client
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.format_specification
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_class_name_prefix
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_hash_values
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_import_statements
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_repr_format
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_repr_keyword_dict
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_repr_positional_values
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_root_package_name
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_storage_format
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_storage_format_keyword_dict
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_storage_format_positional_values
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_template_dict
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_tools_package_name
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.inspect_signature
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_accepts_args
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_accepts_kwargs
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_keyword_names
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_names
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_positional_names
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__copy__
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__eq__
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__format__
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__hash__
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__ne__
      ~abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.client

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.format_specification

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_accepts_args

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_accepts_kwargs

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_keyword_names

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_names

.. autoattribute:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.signature_positional_names

Methods
-------

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_class_name_prefix

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_hash_values

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_import_statements

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_repr_format

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_repr_keyword_dict

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_repr_positional_values

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_root_package_name

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_storage_format

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_storage_format_keyword_dict

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_storage_format_positional_values

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_template_dict

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.get_tools_package_name

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.inspect_signature

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent.__repr__
