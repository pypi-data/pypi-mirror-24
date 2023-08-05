mathtools
=========

.. automodule:: abjad.tools.mathtools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=black,
                  fontcolor=white,
                  group=2,
                  label=BoundedObject,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Enumerator.Enumerator" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Enumerator,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Infinity.Infinity" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Infinity,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity" [color=black,
                  fontcolor=white,
                  group=2,
                  label=NegativeInfinity,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" [color=black,
                  fontcolor=white,
                  group=2,
                  label=NonreducedFraction,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" [color=black,
                  fontcolor=white,
                  group=2,
                  label=NonreducedRatio,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Ratio.Ratio" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Ratio,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Infinity.Infinity" -> "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity";
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" -> "abjad.tools.mathtools.Ratio.Ratio";
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=5,
                  group=4,
                  label=AnnotatedTimespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" [color=5,
                  group=4,
                  label=Timespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          subgraph cluster_quicktions {
              graph [label=quicktions];
              "quicktions.Fraction" [color=4,
                  group=3,
                  label=Fraction,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.Enumerator.Enumerator";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.Infinity.Infinity";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "quicktions.Fraction";
          "quicktions.Fraction" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   BoundedObject
   Enumerator
   Infinity
   NegativeInfinity
   NonreducedFraction
   NonreducedRatio
   Ratio

.. autosummary::
   :nosignatures:

   BoundedObject
   Enumerator
   Infinity
   NegativeInfinity
   NonreducedFraction
   NonreducedRatio
   Ratio

--------

Functions
---------

.. toctree::
   :hidden:

   all_are_equal
   all_are_integer_equivalent
   all_are_integer_equivalent_numbers
   all_are_nonnegative_integer_equivalent_numbers
   all_are_nonnegative_integer_powers_of_two
   all_are_nonnegative_integers
   all_are_pairs_of_types
   all_are_positive_integers
   are_relatively_prime
   arithmetic_mean
   binomial_coefficient
   cumulative_products
   cumulative_sums
   cumulative_sums_pairwise
   difference_series
   divisors
   factors
   fraction_to_proper_fraction
   greatest_common_divisor
   greatest_power_of_two_less_equal
   integer_equivalent_number_to_integer
   integer_to_base_k_tuple
   integer_to_binary_string
   is_assignable_integer
   is_integer_equivalent
   is_integer_equivalent_n_tuple
   is_integer_equivalent_number
   is_nonnegative_integer
   is_nonnegative_integer_equivalent_number
   is_nonnegative_integer_power_of_two
   is_positive_integer
   is_positive_integer_equivalent_number
   is_positive_integer_power_of_two
   least_common_multiple
   partition_integer_by_ratio
   partition_integer_into_canonic_parts
   sign
   weight
   yield_all_compositions_of_integer

.. autosummary::
   :nosignatures:

   all_are_equal
   all_are_integer_equivalent
   all_are_integer_equivalent_numbers
   all_are_nonnegative_integer_equivalent_numbers
   all_are_nonnegative_integer_powers_of_two
   all_are_nonnegative_integers
   all_are_pairs_of_types
   all_are_positive_integers
   are_relatively_prime
   arithmetic_mean
   binomial_coefficient
   cumulative_products
   cumulative_sums
   cumulative_sums_pairwise
   difference_series
   divisors
   factors
   fraction_to_proper_fraction
   greatest_common_divisor
   greatest_power_of_two_less_equal
   integer_equivalent_number_to_integer
   integer_to_base_k_tuple
   integer_to_binary_string
   is_assignable_integer
   is_integer_equivalent
   is_integer_equivalent_n_tuple
   is_integer_equivalent_number
   is_nonnegative_integer
   is_nonnegative_integer_equivalent_number
   is_nonnegative_integer_power_of_two
   is_positive_integer
   is_positive_integer_equivalent_number
   is_positive_integer_power_of_two
   least_common_multiple
   partition_integer_by_ratio
   partition_integer_into_canonic_parts
   sign
   weight
   yield_all_compositions_of_integer
