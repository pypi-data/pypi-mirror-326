# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_segmenter/proto/segmenter_options.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nGmediapipe/tasks/cc/vision/image_segmenter/proto/segmenter_options.proto\x12,mediapipe.tasks.vision.image_segmenter.proto\"\xd4\x02\n\x10SegmenterOptions\x12\x62\n\x0boutput_type\x18\x01 \x01(\x0e\x32I.mediapipe.tasks.vision.image_segmenter.proto.SegmenterOptions.OutputTypeB\x02\x18\x01\x12\x63\n\nactivation\x18\x02 \x01(\x0e\x32I.mediapipe.tasks.vision.image_segmenter.proto.SegmenterOptions.Activation:\x04NONE\"E\n\nOutputType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x11\n\rCATEGORY_MASK\x10\x01\x12\x13\n\x0f\x43ONFIDENCE_MASK\x10\x02\"0\n\nActivation\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07SIGMOID\x10\x01\x12\x0b\n\x07SOFTMAX\x10\x02\x42O\n6com.google.mediapipe.tasks.vision.imagesegmenter.protoB\x15SegmenterOptionsProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.image_segmenter.proto.segmenter_options_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n6com.google.mediapipe.tasks.vision.imagesegmenter.protoB\025SegmenterOptionsProto'
  _globals['_SEGMENTEROPTIONS'].fields_by_name['output_type']._options = None
  _globals['_SEGMENTEROPTIONS'].fields_by_name['output_type']._serialized_options = b'\030\001'
  _globals['_SEGMENTEROPTIONS']._serialized_start=122
  _globals['_SEGMENTEROPTIONS']._serialized_end=462
  _globals['_SEGMENTEROPTIONS_OUTPUTTYPE']._serialized_start=343
  _globals['_SEGMENTEROPTIONS_OUTPUTTYPE']._serialized_end=412
  _globals['_SEGMENTEROPTIONS_ACTIVATION']._serialized_start=414
  _globals['_SEGMENTEROPTIONS_ACTIVATION']._serialized_end=462
# @@protoc_insertion_point(module_scope)
