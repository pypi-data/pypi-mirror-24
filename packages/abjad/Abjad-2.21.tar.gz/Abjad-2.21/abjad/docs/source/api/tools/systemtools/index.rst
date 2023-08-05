systemtools
===========

.. automodule:: abjad.tools.systemtools

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
              "abjad.tools.abctools.ContextManager.ContextManager" [color=1,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=AbjadConfiguration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=BenchmarkScoreMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Configuration.Configuration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Configuration,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.systemtools.FilesystemState.FilesystemState" [color=black,
                  fontcolor=white,
                  group=2,
                  label=FilesystemState,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ForbidUpdate,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.FormatSpecification.FormatSpecification" [color=black,
                  fontcolor=white,
                  group=2,
                  label=FormatSpecification,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.IOManager.IOManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=IOManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.ImportManager.ImportManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ImportManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper" [color=black,
                  fontcolor=white,
                  group=2,
                  label=IndicatorWrapper,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondFormatBundle,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondFormatManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.NullContextManager.NullContextManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=NullContextManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ProgressIndicator,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams" [color=black,
                  fontcolor=white,
                  group=2,
                  label=RedirectedStreams,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Signature.Signature" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Signature,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.SlotContributions.SlotContributions" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SlotContributions,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=StorageFormatAgent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification" [color=black,
                  fontcolor=white,
                  group=2,
                  label=StorageFormatSpecification,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TemporaryDirectory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TemporaryDirectoryChange,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TestCase.TestCase" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TestCase,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TestManager.TestManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TestManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Timer.Timer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Timer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.UpdateManager.UpdateManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=UpdateManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.WellformednessManager.WellformednessManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=WellformednessManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Configuration.Configuration" -> "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          subgraph cluster_unittest {
              graph [label=unittest];
              "unittest.case.TestCase" [color=4,
                  group=3,
                  label=TestCase,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.Configuration.Configuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.IOManager.IOManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.ImportManager.ImportManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.SlotContributions.SlotContributions";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.TestManager.TestManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.UpdateManager.UpdateManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.WellformednessManager.WellformednessManager";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.FormatSpecification.FormatSpecification";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.IndicatorWrapper.IndicatorWrapper";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.Signature.Signature";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.systemtools.StorageFormatAgent.StorageFormatAgent";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.FilesystemState.FilesystemState";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.NullContextManager.NullContextManager";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.Timer.Timer";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "unittest.case.TestCase";
          "unittest.case.TestCase" -> "abjad.tools.systemtools.TestCase.TestCase";
      }

--------

Benchmarking
------------

.. toctree::
   :hidden:

   BenchmarkScoreMaker

.. autosummary::
   :nosignatures:

   BenchmarkScoreMaker

--------

Classes
-------

.. toctree::
   :hidden:

   Signature

.. autosummary::
   :nosignatures:

   Signature

--------

Context managers
----------------

.. toctree::
   :hidden:

   FilesystemState
   ForbidUpdate
   NullContextManager
   ProgressIndicator
   RedirectedStreams
   TemporaryDirectory
   TemporaryDirectoryChange
   Timer

.. autosummary::
   :nosignatures:

   FilesystemState
   ForbidUpdate
   NullContextManager
   ProgressIndicator
   RedirectedStreams
   TemporaryDirectory
   TemporaryDirectoryChange
   Timer

--------

Internals
---------

.. toctree::
   :hidden:

   IndicatorWrapper

.. autosummary::
   :nosignatures:

   IndicatorWrapper

--------

LilyPond formatting
-------------------

.. toctree::
   :hidden:

   LilyPondFormatBundle
   LilyPondFormatManager
   SlotContributions

.. autosummary::
   :nosignatures:

   LilyPondFormatBundle
   LilyPondFormatManager
   SlotContributions

--------

Managers
--------

.. toctree::
   :hidden:

   IOManager
   ImportManager
   TestManager
   UpdateManager
   WellformednessManager

.. autosummary::
   :nosignatures:

   IOManager
   ImportManager
   TestManager
   UpdateManager
   WellformednessManager

--------

Storage formatting
------------------

.. toctree::
   :hidden:

   FormatSpecification
   StorageFormatAgent
   StorageFormatSpecification

.. autosummary::
   :nosignatures:

   FormatSpecification
   StorageFormatAgent
   StorageFormatSpecification

--------

System configuration
--------------------

.. toctree::
   :hidden:

   AbjadConfiguration
   Configuration

.. autosummary::
   :nosignatures:

   AbjadConfiguration
   Configuration
