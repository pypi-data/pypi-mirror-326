# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/components/calculators/classification_aggregation_calculator.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nUmediapipe/tasks/cc/components/calculators/classification_aggregation_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xa6\x01\n*ClassificationAggregationCalculatorOptions\x12\x12\n\nhead_names\x18\x01 \x03(\t2d\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf8\x8e\xf5\xd5\x01 \x01(\x0b\x32\x35.mediapipe.ClassificationAggregationCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.components.calculators.classification_aggregation_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CLASSIFICATIONAGGREGATIONCALCULATOROPTIONS']._serialized_start=139
  _globals['_CLASSIFICATIONAGGREGATIONCALCULATOROPTIONS']._serialized_end=305
# @@protoc_insertion_point(module_scope)
