# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_segmenter/calculators/tensors_to_segmentation_calculator.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.vision.image_segmenter.proto import segmenter_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__segmenter_dot_proto_dot_segmenter__options__pb2
from mediapipe.util import label_map_pb2 as mediapipe_dot_util_dot_label__map__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n^mediapipe/tasks/cc/vision/image_segmenter/calculators/tensors_to_segmentation_calculator.proto\x12\x0fmediapipe.tasks\x1a,mediapipe/framework/calculator_options.proto\x1aGmediapipe/tasks/cc/vision/image_segmenter/proto/segmenter_options.proto\x1a\x1emediapipe/util/label_map.proto\"\x95\x03\n&TensorsToSegmentationCalculatorOptions\x12Y\n\x11segmenter_options\x18\x01 \x01(\x0b\x32>.mediapipe.tasks.vision.image_segmenter.proto.SegmenterOptions\x12\\\n\x0blabel_items\x18\x02 \x03(\x0b\x32G.mediapipe.tasks.TensorsToSegmentationCalculatorOptions.LabelItemsEntry\x1aJ\n\x0fLabelItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.mediapipe.LabelMapItem:\x02\x38\x01\x32\x66\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x94\xc8\xb8\xda\x01 \x01(\x0b\x32\x37.mediapipe.tasks.TensorsToSegmentationCalculatorOptionsBI\n\x1a\x63om.google.mediapipe.tasksB+TensorsToSegmentationCalculatorOptionsProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.image_segmenter.calculators.tensors_to_segmentation_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\032com.google.mediapipe.tasksB+TensorsToSegmentationCalculatorOptionsProto'
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS_LABELITEMSENTRY']._options = None
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_options = b'8\001'
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS']._serialized_start=267
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS']._serialized_end=672
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_start=494
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_end=568
# @@protoc_insertion_point(module_scope)
