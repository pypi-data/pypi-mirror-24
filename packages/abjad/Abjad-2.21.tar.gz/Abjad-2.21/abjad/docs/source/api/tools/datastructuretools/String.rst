.. currentmodule:: abjad.tools.datastructuretools

String
======

.. autoclass:: String

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.String.String" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>String</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
              "builtins.str" [color=1,
                  group=0,
                  label=str,
                  shape=box];
              "builtins.object" -> "builtins.str";
          }
          "builtins.str" -> "abjad.tools.datastructuretools.String.String";
      }

Bases
-----

- :py:class:`builtins.str`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.String.String.capitalize
      ~abjad.tools.datastructuretools.String.String.capitalize_start
      ~abjad.tools.datastructuretools.String.String.casefold
      ~abjad.tools.datastructuretools.String.String.center
      ~abjad.tools.datastructuretools.String.String.count
      ~abjad.tools.datastructuretools.String.String.delimit_words
      ~abjad.tools.datastructuretools.String.String.encode
      ~abjad.tools.datastructuretools.String.String.endswith
      ~abjad.tools.datastructuretools.String.String.expandtabs
      ~abjad.tools.datastructuretools.String.String.find
      ~abjad.tools.datastructuretools.String.String.format
      ~abjad.tools.datastructuretools.String.String.format_map
      ~abjad.tools.datastructuretools.String.String.index
      ~abjad.tools.datastructuretools.String.String.is_dash_case
      ~abjad.tools.datastructuretools.String.String.is_dash_case_file_name
      ~abjad.tools.datastructuretools.String.String.is_lower_camel_case
      ~abjad.tools.datastructuretools.String.String.is_snake_case
      ~abjad.tools.datastructuretools.String.String.is_snake_case_file_name
      ~abjad.tools.datastructuretools.String.String.is_snake_case_file_name_with_extension
      ~abjad.tools.datastructuretools.String.String.is_snake_case_package_name
      ~abjad.tools.datastructuretools.String.String.is_space_delimited_lowercase
      ~abjad.tools.datastructuretools.String.String.is_string
      ~abjad.tools.datastructuretools.String.String.is_upper_camel_case
      ~abjad.tools.datastructuretools.String.String.isalnum
      ~abjad.tools.datastructuretools.String.String.isalpha
      ~abjad.tools.datastructuretools.String.String.isdecimal
      ~abjad.tools.datastructuretools.String.String.isdigit
      ~abjad.tools.datastructuretools.String.String.isidentifier
      ~abjad.tools.datastructuretools.String.String.islower
      ~abjad.tools.datastructuretools.String.String.isnumeric
      ~abjad.tools.datastructuretools.String.String.isprintable
      ~abjad.tools.datastructuretools.String.String.isspace
      ~abjad.tools.datastructuretools.String.String.istitle
      ~abjad.tools.datastructuretools.String.String.isupper
      ~abjad.tools.datastructuretools.String.String.join
      ~abjad.tools.datastructuretools.String.String.ljust
      ~abjad.tools.datastructuretools.String.String.lower
      ~abjad.tools.datastructuretools.String.String.lstrip
      ~abjad.tools.datastructuretools.String.String.maketrans
      ~abjad.tools.datastructuretools.String.String.normalize
      ~abjad.tools.datastructuretools.String.String.partition
      ~abjad.tools.datastructuretools.String.String.pluralize
      ~abjad.tools.datastructuretools.String.String.replace
      ~abjad.tools.datastructuretools.String.String.rfind
      ~abjad.tools.datastructuretools.String.String.rindex
      ~abjad.tools.datastructuretools.String.String.rjust
      ~abjad.tools.datastructuretools.String.String.rpartition
      ~abjad.tools.datastructuretools.String.String.rsplit
      ~abjad.tools.datastructuretools.String.String.rstrip
      ~abjad.tools.datastructuretools.String.String.split
      ~abjad.tools.datastructuretools.String.String.splitlines
      ~abjad.tools.datastructuretools.String.String.startswith
      ~abjad.tools.datastructuretools.String.String.strip
      ~abjad.tools.datastructuretools.String.String.strip_diacritics
      ~abjad.tools.datastructuretools.String.String.swapcase
      ~abjad.tools.datastructuretools.String.String.title
      ~abjad.tools.datastructuretools.String.String.to_accent_free_snake_case
      ~abjad.tools.datastructuretools.String.String.to_bidirectional_direction_string
      ~abjad.tools.datastructuretools.String.String.to_bidirectional_lilypond_symbol
      ~abjad.tools.datastructuretools.String.String.to_dash_case
      ~abjad.tools.datastructuretools.String.String.to_lower_camel_case
      ~abjad.tools.datastructuretools.String.String.to_snake_case
      ~abjad.tools.datastructuretools.String.String.to_space_delimited_lowercase
      ~abjad.tools.datastructuretools.String.String.to_tridirectional_direction_string
      ~abjad.tools.datastructuretools.String.String.to_tridirectional_lilypond_symbol
      ~abjad.tools.datastructuretools.String.String.to_tridirectional_ordinal_constant
      ~abjad.tools.datastructuretools.String.String.to_upper_camel_case
      ~abjad.tools.datastructuretools.String.String.translate
      ~abjad.tools.datastructuretools.String.String.upper
      ~abjad.tools.datastructuretools.String.String.zfill
      ~abjad.tools.datastructuretools.String.String.__add__
      ~abjad.tools.datastructuretools.String.String.__contains__
      ~abjad.tools.datastructuretools.String.String.__eq__
      ~abjad.tools.datastructuretools.String.String.__format__
      ~abjad.tools.datastructuretools.String.String.__ge__
      ~abjad.tools.datastructuretools.String.String.__getitem__
      ~abjad.tools.datastructuretools.String.String.__gt__
      ~abjad.tools.datastructuretools.String.String.__hash__
      ~abjad.tools.datastructuretools.String.String.__iter__
      ~abjad.tools.datastructuretools.String.String.__le__
      ~abjad.tools.datastructuretools.String.String.__len__
      ~abjad.tools.datastructuretools.String.String.__lt__
      ~abjad.tools.datastructuretools.String.String.__mod__
      ~abjad.tools.datastructuretools.String.String.__mul__
      ~abjad.tools.datastructuretools.String.String.__ne__
      ~abjad.tools.datastructuretools.String.String.__new__
      ~abjad.tools.datastructuretools.String.String.__repr__
      ~abjad.tools.datastructuretools.String.String.__rmod__
      ~abjad.tools.datastructuretools.String.String.__rmul__
      ~abjad.tools.datastructuretools.String.String.__str__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.capitalize

.. automethod:: abjad.tools.datastructuretools.String.String.capitalize_start

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.casefold

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.center

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.count

.. automethod:: abjad.tools.datastructuretools.String.String.delimit_words

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.encode

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.endswith

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.expandtabs

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.find

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.format

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.format_map

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.index

.. automethod:: abjad.tools.datastructuretools.String.String.is_dash_case

.. automethod:: abjad.tools.datastructuretools.String.String.is_dash_case_file_name

.. automethod:: abjad.tools.datastructuretools.String.String.is_lower_camel_case

.. automethod:: abjad.tools.datastructuretools.String.String.is_snake_case

.. automethod:: abjad.tools.datastructuretools.String.String.is_snake_case_file_name

.. automethod:: abjad.tools.datastructuretools.String.String.is_snake_case_file_name_with_extension

.. automethod:: abjad.tools.datastructuretools.String.String.is_snake_case_package_name

.. automethod:: abjad.tools.datastructuretools.String.String.is_space_delimited_lowercase

.. automethod:: abjad.tools.datastructuretools.String.String.is_upper_camel_case

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isalnum

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isalpha

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isdecimal

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isdigit

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isidentifier

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.islower

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isnumeric

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isprintable

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isspace

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.istitle

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.isupper

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.join

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.ljust

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.lower

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.lstrip

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.partition

.. automethod:: abjad.tools.datastructuretools.String.String.pluralize

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.replace

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.rfind

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.rindex

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.rjust

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.rpartition

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.rsplit

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.rstrip

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.split

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.splitlines

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.startswith

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.strip

.. automethod:: abjad.tools.datastructuretools.String.String.strip_diacritics

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.swapcase

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.title

.. automethod:: abjad.tools.datastructuretools.String.String.to_accent_free_snake_case

.. automethod:: abjad.tools.datastructuretools.String.String.to_dash_case

.. automethod:: abjad.tools.datastructuretools.String.String.to_lower_camel_case

.. automethod:: abjad.tools.datastructuretools.String.String.to_snake_case

.. automethod:: abjad.tools.datastructuretools.String.String.to_space_delimited_lowercase

.. automethod:: abjad.tools.datastructuretools.String.String.to_upper_camel_case

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.translate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.upper

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.zfill

Class & static methods
----------------------

.. automethod:: abjad.tools.datastructuretools.String.String.is_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.maketrans

.. automethod:: abjad.tools.datastructuretools.String.String.normalize

.. automethod:: abjad.tools.datastructuretools.String.String.to_bidirectional_direction_string

.. automethod:: abjad.tools.datastructuretools.String.String.to_bidirectional_lilypond_symbol

.. automethod:: abjad.tools.datastructuretools.String.String.to_tridirectional_direction_string

.. automethod:: abjad.tools.datastructuretools.String.String.to_tridirectional_lilypond_symbol

.. automethod:: abjad.tools.datastructuretools.String.String.to_tridirectional_ordinal_constant

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__mod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__rmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.String.String.__str__
