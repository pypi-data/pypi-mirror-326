# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/face_geometry/proto/face_geometry_graph_options.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.vision.face_geometry.calculators import geometry_pipeline_calculator_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_face__geometry_dot_calculators_dot_geometry__pipeline__calculator__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nOmediapipe/tasks/cc/vision/face_geometry/proto/face_geometry_graph_options.proto\x12*mediapipe.tasks.vision.face_geometry.proto\x1a,mediapipe/framework/calculator_options.proto\x1aVmediapipe/tasks/cc/vision/face_geometry/calculators/geometry_pipeline_calculator.proto\"\xff\x01\n\x18\x46\x61\x63\x65GeometryGraphOptions\x12n\n\x19geometry_pipeline_options\x18\x01 \x01(\x0b\x32K.mediapipe.tasks.vision.face_geometry.FaceGeometryPipelineCalculatorOptions2s\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf2\xa1\xf5\xf5\x01 \x01(\x0b\x32\x44.mediapipe.tasks.vision.face_geometry.proto.FaceGeometryGraphOptionsBU\n4com.google.mediapipe.tasks.vision.facegeometry.protoB\x1d\x46\x61\x63\x65GeometryGraphOptionsProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.face_geometry.proto.face_geometry_graph_options_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n4com.google.mediapipe.tasks.vision.facegeometry.protoB\035FaceGeometryGraphOptionsProto'
  _globals['_FACEGEOMETRYGRAPHOPTIONS']._serialized_start=262
  _globals['_FACEGEOMETRYGRAPHOPTIONS']._serialized_end=517
# @@protoc_insertion_point(module_scope)
