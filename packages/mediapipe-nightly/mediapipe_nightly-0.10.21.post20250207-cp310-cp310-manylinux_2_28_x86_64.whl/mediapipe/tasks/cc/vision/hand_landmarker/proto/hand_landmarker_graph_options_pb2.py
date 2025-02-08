# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/hand_landmarker/proto/hand_landmarker_graph_options.proto
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
from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.core.proto import base_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2
from mediapipe.tasks.cc.vision.hand_detector.proto import hand_detector_graph_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_hand__detector_dot_proto_dot_hand__detector__graph__options__pb2
from mediapipe.tasks.cc.vision.hand_landmarker.proto import hand_landmarks_detector_graph_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_hand__landmarker_dot_proto_dot_hand__landmarks__detector__graph__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nSmediapipe/tasks/cc/vision/hand_landmarker/proto/hand_landmarker_graph_options.proto\x12,mediapipe.tasks.vision.hand_landmarker.proto\x1a$mediapipe/framework/calculator.proto\x1a,mediapipe/framework/calculator_options.proto\x1a\x30mediapipe/tasks/cc/core/proto/base_options.proto\x1aOmediapipe/tasks/cc/vision/hand_detector/proto/hand_detector_graph_options.proto\x1a[mediapipe/tasks/cc/vision/hand_landmarker/proto/hand_landmarks_detector_graph_options.proto\"\xe5\x03\n\x1aHandLandmarkerGraphOptions\x12=\n\x0c\x62\x61se_options\x18\x01 \x01(\x0b\x32\'.mediapipe.tasks.core.proto.BaseOptions\x12i\n\x1bhand_detector_graph_options\x18\x02 \x01(\x0b\x32\x44.mediapipe.tasks.vision.hand_detector.proto.HandDetectorGraphOptions\x12~\n%hand_landmarks_detector_graph_options\x18\x03 \x01(\x0b\x32O.mediapipe.tasks.vision.hand_landmarker.proto.HandLandmarksDetectorGraphOptions\x12$\n\x17min_tracking_confidence\x18\x04 \x01(\x02:\x03\x30.52w\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf2\xe2\xd1\xdc\x01 \x01(\x0b\x32H.mediapipe.tasks.vision.hand_landmarker.proto.HandLandmarkerGraphOptionsBY\n6com.google.mediapipe.tasks.vision.handlandmarker.protoB\x1fHandLandmarkerGraphOptionsProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.hand_landmarker.proto.hand_landmarker_graph_options_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n6com.google.mediapipe.tasks.vision.handlandmarker.protoB\037HandLandmarkerGraphOptionsProto'
  _globals['_HANDLANDMARKERGRAPHOPTIONS']._serialized_start=442
  _globals['_HANDLANDMARKERGRAPHOPTIONS']._serialized_end=927
# @@protoc_insertion_point(module_scope)
