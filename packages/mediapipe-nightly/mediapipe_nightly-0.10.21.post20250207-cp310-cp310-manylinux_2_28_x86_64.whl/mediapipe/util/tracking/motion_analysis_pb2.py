# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/motion_analysis.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.util.tracking import motion_estimation_pb2 as mediapipe_dot_util_dot_tracking_dot_motion__estimation__pb2
from mediapipe.util.tracking import motion_saliency_pb2 as mediapipe_dot_util_dot_tracking_dot_motion__saliency__pb2
from mediapipe.util.tracking import region_flow_computation_pb2 as mediapipe_dot_util_dot_tracking_dot_region__flow__computation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-mediapipe/util/tracking/motion_analysis.proto\x12\tmediapipe\x1a/mediapipe/util/tracking/motion_estimation.proto\x1a-mediapipe/util/tracking/motion_saliency.proto\x1a\x35mediapipe/util/tracking/region_flow_computation.proto\"\xf8\n\n\x15MotionAnalysisOptions\x12`\n\x0f\x61nalysis_policy\x18\x0e \x01(\x0e\x32/.mediapipe.MotionAnalysisOptions.AnalysisPolicy:\x16\x41NALYSIS_POLICY_LEGACY\x12=\n\x0c\x66low_options\x18\x01 \x01(\x0b\x32\'.mediapipe.RegionFlowComputationOptions\x12:\n\x0emotion_options\x18\x02 \x01(\x0b\x32\".mediapipe.MotionEstimationOptions\x12:\n\x10saliency_options\x18\x03 \x01(\x0b\x32 .mediapipe.MotionSaliencyOptions\x12 \n\x14\x65stimation_clip_size\x18\x04 \x01(\x05:\x02\x31\x36\x12\x33\n$subtract_camera_motion_from_features\x18\x05 \x01(\x08:\x05\x66\x61lse\x12\x16\n\x0btrack_index\x18\x06 \x01(\x05:\x01\x30\x12&\n\x17\x63ompute_motion_saliency\x18\x07 \x01(\x08:\x05\x66\x61lse\x12%\n\x17select_saliency_inliers\x18\x08 \x01(\x08:\x04true\x12\x1d\n\x0f\x66ilter_saliency\x18\t \x01(\x08:\x04true\x12\"\n\x13post_irls_smoothing\x18\n \x01(\x08:\x05\x66\x61lse\x12)\n\x1drejection_transform_threshold\x18\r \x01(\x02:\x02\x32\x30\x12T\n\x15visualization_options\x18\x0b \x01(\x0b\x32\x35.mediapipe.MotionAnalysisOptions.VisualizationOptions\x12N\n\x12\x66oreground_options\x18\x0c \x01(\x0b\x32\x32.mediapipe.MotionAnalysisOptions.ForegroundOptions\x1a\xc5\x02\n\x14VisualizationOptions\x12,\n\x1evisualize_region_flow_features\x18\x01 \x01(\x08:\x04true\x12\'\n\x18visualize_salient_points\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x19\n\x0eline_thickness\x18\x05 \x01(\x05:\x01\x34\x12&\n\x17\x66oreground_jet_coloring\x18\x03 \x01(\x08:\x05\x66\x61lse\x12-\n\x1evisualize_blur_analysis_region\x18\x04 \x01(\x08:\x05\x66\x61lse\x12\x1d\n\x0fvisualize_stats\x18\x06 \x01(\x08:\x04true\x12!\n\x16min_long_feature_track\x18\x07 \x01(\x05:\x01\x30\x12\"\n\x17max_long_feature_points\x18\x08 \x01(\x05:\x01\x30\x1a}\n\x11\x46oregroundOptions\x12!\n\x14\x66oreground_threshold\x18\x01 \x01(\x02:\x03\x30.5\x12\x1b\n\x10\x66oreground_gamma\x18\x02 \x01(\x02:\x01\x31\x12(\n\x1athreshold_coverage_scaling\x18\x03 \x01(\x08:\x04true\"\xac\x01\n\x0e\x41nalysisPolicy\x12\x1a\n\x16\x41NALYSIS_POLICY_LEGACY\x10\x00\x12\x19\n\x15\x41NALYSIS_POLICY_VIDEO\x10\x01\x12 \n\x1c\x41NALYSIS_POLICY_VIDEO_MOBILE\x10\x02\x12!\n\x1d\x41NALYSIS_POLICY_CAMERA_MOBILE\x10\x03\x12\x1e\n\x1a\x41NALYSIS_POLICY_HYPERLAPSE\x10\x04')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.tracking.motion_analysis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MOTIONANALYSISOPTIONS']._serialized_start=212
  _globals['_MOTIONANALYSISOPTIONS']._serialized_end=1612
  _globals['_MOTIONANALYSISOPTIONS_VISUALIZATIONOPTIONS']._serialized_start=985
  _globals['_MOTIONANALYSISOPTIONS_VISUALIZATIONOPTIONS']._serialized_end=1310
  _globals['_MOTIONANALYSISOPTIONS_FOREGROUNDOPTIONS']._serialized_start=1312
  _globals['_MOTIONANALYSISOPTIONS_FOREGROUNDOPTIONS']._serialized_end=1437
  _globals['_MOTIONANALYSISOPTIONS_ANALYSISPOLICY']._serialized_start=1440
  _globals['_MOTIONANALYSISOPTIONS_ANALYSISPOLICY']._serialized_end=1612
# @@protoc_insertion_point(module_scope)
