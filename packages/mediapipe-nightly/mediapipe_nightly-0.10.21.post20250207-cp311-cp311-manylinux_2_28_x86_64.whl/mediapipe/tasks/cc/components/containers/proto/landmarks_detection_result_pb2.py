# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/components/containers/proto/landmarks_detection_result.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework.formats import classification_pb2 as mediapipe_dot_framework_dot_formats_dot_classification__pb2
from mediapipe.framework.formats import landmark_pb2 as mediapipe_dot_framework_dot_formats_dot_landmark__pb2
from mediapipe.framework.formats import rect_pb2 as mediapipe_dot_framework_dot_formats_dot_rect__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nOmediapipe/tasks/cc/components/containers/proto/landmarks_detection_result.proto\x12 mediapipe.tasks.containers.proto\x1a\x30mediapipe/framework/formats/classification.proto\x1a*mediapipe/framework/formats/landmark.proto\x1a&mediapipe/framework/formats/rect.proto\"\xe3\x01\n\x18LandmarksDetectionResult\x12\x34\n\tlandmarks\x18\x01 \x01(\x0b\x32!.mediapipe.NormalizedLandmarkList\x12\x36\n\x0f\x63lassifications\x18\x02 \x01(\x0b\x32\x1d.mediapipe.ClassificationList\x12\x30\n\x0fworld_landmarks\x18\x03 \x01(\x0b\x32\x17.mediapipe.LandmarkList\x12\'\n\x04rect\x18\x04 \x01(\x0b\x32\x19.mediapipe.NormalizedRect\"\xe9\x01\n\x1dMultiLandmarksDetectionResult\x12\x34\n\tlandmarks\x18\x01 \x03(\x0b\x32!.mediapipe.NormalizedLandmarkList\x12\x36\n\x0f\x63lassifications\x18\x02 \x03(\x0b\x32\x1d.mediapipe.ClassificationList\x12\x30\n\x0fworld_landmarks\x18\x03 \x03(\x0b\x32\x17.mediapipe.LandmarkList\x12(\n\x05rects\x18\x04 \x03(\x0b\x32\x19.mediapipe.NormalizedRectBW\n6com.google.mediapipe.tasks.components.containers.protoB\x1dLandmarksDetectionResultProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.components.containers.proto.landmarks_detection_result_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n6com.google.mediapipe.tasks.components.containers.protoB\035LandmarksDetectionResultProto'
  _globals['_LANDMARKSDETECTIONRESULT']._serialized_start=252
  _globals['_LANDMARKSDETECTIONRESULT']._serialized_end=479
  _globals['_MULTILANDMARKSDETECTIONRESULT']._serialized_start=482
  _globals['_MULTILANDMARKSDETECTIONRESULT']._serialized_end=715
# @@protoc_insertion_point(module_scope)
