# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/video/tracked_detection_manager_calculator.proto
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
from mediapipe.util.tracking import tracked_detection_manager_config_pb2 as mediapipe_dot_util_dot_tracking_dot_tracked__detection__manager__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nFmediapipe/calculators/video/tracked_detection_manager_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a>mediapipe/util/tracking/tracked_detection_manager_config.proto\"\xe3\x01\n(TrackedDetectionManagerCalculatorOptions\x12S\n!tracked_detection_manager_options\x18\x01 \x01(\x0b\x32(.mediapipe.TrackedDetectionManagerConfig2b\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb6\xe6\xfe\x8f\x01 \x01(\x0b\x32\x33.mediapipe.TrackedDetectionManagerCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.video.tracked_detection_manager_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TRACKEDDETECTIONMANAGERCALCULATOROPTIONS']._serialized_start=188
  _globals['_TRACKEDDETECTIONMANAGERCALCULATOROPTIONS']._serialized_end=415
# @@protoc_insertion_point(module_scope)
