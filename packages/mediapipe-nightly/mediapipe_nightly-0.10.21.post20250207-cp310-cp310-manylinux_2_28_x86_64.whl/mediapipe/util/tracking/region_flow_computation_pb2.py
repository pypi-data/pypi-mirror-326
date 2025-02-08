# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/region_flow_computation.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.util.tracking import tone_estimation_pb2 as mediapipe_dot_util_dot_tracking_dot_tone__estimation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5mediapipe/util/tracking/region_flow_computation.proto\x12\tmediapipe\x1a-mediapipe/util/tracking/tone_estimation.proto\"\xb0\x10\n\x0fTrackingOptions\x12W\n\x1binternal_tracking_direction\x18\x13 \x01(\x0e\x32(.mediapipe.TrackingOptions.FlowDirection:\x08\x42\x41\x43KWARD\x12Q\n\x15output_flow_direction\x18\x14 \x01(\x0e\x32(.mediapipe.TrackingOptions.FlowDirection:\x08\x42\x41\x43KWARD\x12W\n\x0ftracking_policy\x18\x19 \x01(\x0e\x32).mediapipe.TrackingOptions.TrackingPolicy:\x13POLICY_SINGLE_FRAME\x12 \n\x15multi_frames_to_track\x18\x01 \x01(\x05:\x01\x31\x12#\n\x16long_tracks_max_frames\x18\x1a \x01(\x05:\x03\x33\x30\x30\x12\x1a\n\x0cmax_features\x18\x02 \x01(\x05:\x04\x32\x30\x30\x30\x12k\n\x18\x63orner_extraction_method\x18\x1b \x01(\x0e\x32\x31.mediapipe.TrackingOptions.CornerExtractionMethod:\x16\x45XTRACTION_MIN_EIG_VAL\x12T\n\x14min_eig_val_settings\x18\x1c \x01(\x0b\x32\x36.mediapipe.TrackingOptions.MinEigValExtractionSettings\x12L\n\x0fharris_settings\x18\x1d \x01(\x0b\x32\x33.mediapipe.TrackingOptions.HarrisExtractionSettings\x12H\n\rfast_settings\x18\x1f \x01(\x0b\x32\x31.mediapipe.TrackingOptions.FastExtractionSettings\x12 \n\x14tracking_window_size\x18\x04 \x01(\x05:\x02\x31\x30\x12\x1f\n\x13tracking_iterations\x18\x05 \x01(\x05:\x02\x31\x30\x12*\n\x1c\x66ractional_tracking_distance\x18\x06 \x01(\x02:\x04\x30.15\x12)\n\x1a\x61\x64\x61ptive_tracking_distance\x18\x18 \x01(\x08:\x05\x66\x61lse\x12\x1f\n\x14min_feature_distance\x18\x07 \x01(\x02:\x01\x37\x12%\n\x17\x64istance_downscale_sqrt\x18\x15 \x01(\x08:\x04true\x12-\n\x1f\x61\x64\x61ptive_good_features_to_track\x18\x08 \x01(\x08:\x04true\x12*\n\x1c\x61\x64\x61ptive_features_block_size\x18\t \x01(\x02:\x04\x30.26\x12#\n\x18\x61\x64\x61ptive_features_levels\x18\n \x01(\x05:\x01\x31\x12%\n\x1a\x61\x64\x61ptive_extraction_levels\x18\x16 \x01(\x05:\x01\x31\x12\x31\n&adaptive_extraction_levels_lowest_size\x18\x17 \x01(\x05:\x01\x30\x12-\n\x1fsynthetic_zero_motion_grid_step\x18\r \x01(\x02:\x04\x30.04\x12%\n\x16wide_baseline_matching\x18\x0e \x01(\x08:\x05\x66\x61lse\x12!\n\x14ratio_test_threshold\x18\x0f \x01(\x02:\x03\x30.8\x12+\n\x1crefine_wide_baseline_matches\x18\x10 \x01(\x08:\x05\x66\x61lse\x12,\n!reuse_features_max_frame_distance\x18\x11 \x01(\x05:\x01\x30\x12-\n reuse_features_min_survived_frac\x18\x12 \x01(\x02:\x03\x30.7\x12\x63\n\x1aklt_tracker_implementation\x18  \x01(\x0e\x32\x33.mediapipe.TrackingOptions.KltTrackerImplementation:\nKLT_OPENCV\x1ap\n\x1bMinEigValExtractionSettings\x12#\n\x15\x66\x65\x61ture_quality_level\x18\x01 \x01(\x02:\x04\x30.01\x12,\n\x1d\x61\x64\x61ptive_lowest_quality_level\x18\x02 \x01(\x02:\x05\x38\x65-05\x1a\x42\n\x18HarrisExtractionSettings\x12&\n\x15\x66\x65\x61ture_quality_level\x18\x01 \x01(\x02:\x07\x30.00025\x1a/\n\x16\x46\x61stExtractionSettings\x12\x15\n\tthreshold\x18\x01 \x01(\x05:\x02\x31\x30\"=\n\rFlowDirection\x12\x0b\n\x07\x46ORWARD\x10\x01\x12\x0c\n\x08\x42\x41\x43KWARD\x10\x02\x12\x11\n\rCONSECUTIVELY\x10\x03\"Y\n\x0eTrackingPolicy\x12\x17\n\x13POLICY_SINGLE_FRAME\x10\x01\x12\x16\n\x12POLICY_MULTI_FRAME\x10\x02\x12\x16\n\x12POLICY_LONG_TRACKS\x10\x03\"`\n\x16\x43ornerExtractionMethod\x12\x15\n\x11\x45XTRACTION_HARRIS\x10\x01\x12\x1a\n\x16\x45XTRACTION_MIN_EIG_VAL\x10\x02\x12\x13\n\x0f\x45XTRACTION_FAST\x10\x03\";\n\x18KltTrackerImplementation\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0e\n\nKLT_OPENCV\x10\x01*\x04\x08\x03\x10\x04*\x04\x08\x0b\x10\x0c*\x04\x08\x0c\x10\r*\x04\x08\x1e\x10\x1f\"\xe7\x1c\n\x1cRegionFlowComputationOptions\x12\x34\n\x10tracking_options\x18\x01 \x01(\x0b\x32\x1a.mediapipe.TrackingOptions\x12\x1e\n\x13min_feature_inliers\x18\x02 \x01(\x05:\x01\x33\x12)\n\x1crelative_min_feature_inliers\x18. \x01(\x02:\x03\x30.2\x12\x1b\n\x0epre_blur_sigma\x18! \x01(\x02:\x03\x30.8\x12$\n\x18ransac_rounds_per_region\x18\x03 \x01(\x05:\x02\x31\x35\x12*\n\x1f\x61\x62solute_inlier_error_threshold\x18\x04 \x01(\x02:\x01\x32\x12&\n\x1b\x66rac_inlier_error_threshold\x18\x34 \x01(\x02:\x01\x30\x12,\n\x1frelative_inlier_error_threshold\x18, \x01(\x02:\x03\x30.1\x12\x1a\n\x0ftop_inlier_sets\x18- \x01(\x05:\x01\x32\x12!\n\x12no_estimation_mode\x18( \x01(\x08:\x05\x66\x61lse\x12(\n\x1a\x66\x61st_estimation_block_size\x18\x06 \x01(\x02:\x04\x30.25\x12+\n\x1e\x66\x61st_estimation_min_block_size\x18\x19 \x01(\x05:\x03\x31\x30\x30\x12(\n\x1d\x66\x61st_estimation_overlap_grids\x18\x16 \x01(\x05:\x01\x33\x12*\n\x1dmax_magnitude_threshold_ratio\x18\x17 \x01(\x02:\x03\x30.2\x12\"\n\x17median_magnitude_bounds\x18\x33 \x01(\x02:\x01\x30\x12i\n\x13irls_initialization\x18\x31 \x01(\x0e\x32:.mediapipe.RegionFlowComputationOptions.IrlsInitialization:\x10INIT_CONSISTENCY\x12`\n\x0f\x64ownsample_mode\x18\x0b \x01(\x0e\x32\x36.mediapipe.RegionFlowComputationOptions.DownsampleMode:\x0f\x44OWNSAMPLE_NONE\x12\x1e\n\x11\x64ownsampling_size\x18\x0c \x01(\x05:\x03\x32\x35\x36\x12\x1c\n\x11\x64ownsample_factor\x18\x12 \x01(\x02:\x01\x32\x12&\n\x17round_downsample_factor\x18> \x01(\x08:\x05\x66\x61lse\x12W\n\x13\x64ownsample_schedule\x18\x13 \x01(\x0b\x32:.mediapipe.RegionFlowComputationOptions.DownSampleSchedule\x12#\n\x17min_feature_requirement\x18\r \x01(\x05:\x02\x32\x30\x12\x1f\n\x11min_feature_cover\x18\x0e \x01(\x02:\x04\x30.15\x12!\n\x16min_feature_cover_grid\x18\x14 \x01(\x05:\x01\x38\x12!\n\x12\x63ompute_blur_score\x18\x11 \x01(\x08:\x05\x66\x61lse\x12T\n\x12\x62lur_score_options\x18\x1f \x01(\x0b\x32\x38.mediapipe.RegionFlowComputationOptions.BlurScoreOptions\x12\x64\n\x1avisual_consistency_options\x18\x37 \x01(\x0b\x32@.mediapipe.RegionFlowComputationOptions.VisualConsistencyOptions\x12\"\n\x17patch_descriptor_radius\x18\x15 \x01(\x05:\x01\x33\x12\x1f\n\x14\x64istance_from_border\x18\x32 \x01(\x05:\x01\x33\x12#\n\x15\x63orner_response_scale\x18\x1a \x01(\x02:\x04\x31\x35\x30\x30\x12\x1e\n\x0fverify_features\x18\x1b \x01(\x08:\x05\x66\x61lse\x12\"\n\x15verification_distance\x18\x1c \x01(\x02:\x03\x30.5\x12\"\n\x14verify_long_features\x18\x35 \x01(\x08:\x04true\x12\x31\n#long_feature_verification_threshold\x18\x36 \x01(\x02:\x04\x30.04\x12(\n\x1dmax_long_feature_acceleration\x18\x38 \x01(\x02:\x01\x35\x12/\n verify_long_feature_acceleration\x18? \x01(\x08:\x05\x66\x61lse\x12,\n!verify_long_feature_trigger_ratio\x18@ \x01(\x02:\x01\x30\x12%\n\x16histogram_equalization\x18\x39 \x01(\x08:\x05\x66\x61lse\x12:\n+use_synthetic_zero_motion_tracks_all_frames\x18\" \x01(\x08:\x05\x66\x61lse\x12;\n,use_synthetic_zero_motion_tracks_first_frame\x18# \x01(\x08:\x05\x66\x61lse\x12\x1e\n\x0fgain_correction\x18$ \x01(\x08:\x05\x66\x61lse\x12#\n\x14\x66\x61st_gain_correction\x18= \x01(\x08:\x05\x66\x61lse\x12\x31\n#gain_correction_multiple_hypotheses\x18/ \x01(\x08:\x04true\x12\x34\n\'gain_correction_inlier_improvement_frac\x18\x30 \x01(\x02:\x03\x30.1\x12/\n gain_correction_bright_reference\x18; \x01(\x08:\x05\x66\x61lse\x12+\n gain_correction_triggering_ratio\x18< \x01(\x02:\x01\x30\x12#\n\x16\x66rac_gain_feature_size\x18% \x01(\x02:\x03\x30.3\x12\x1b\n\x0e\x66rac_gain_step\x18& \x01(\x02:\x03\x30.1\x12m\n\x11gain_correct_mode\x18) \x01(\x0e\x32\x37.mediapipe.RegionFlowComputationOptions.GainCorrectMode:\x19GAIN_CORRECT_DEFAULT_USER\x12I\n\x10gain_bias_bounds\x18\' \x01(\x0b\x32/.mediapipe.ToneEstimationOptions.GainBiasBounds\x12U\n\x0cimage_format\x18: \x01(\x0e\x32\x33.mediapipe.RegionFlowComputationOptions.ImageFormat:\nFORMAT_RGB\x12g\n\x19\x64\x65scriptor_extractor_type\x18\x41 \x01(\x0e\x32?.mediapipe.RegionFlowComputationOptions.DescriptorExtractorType:\x03ORB\x12+\n\x1d\x63ompute_derivative_in_pyramid\x18\x42 \x01(\x08:\x04true\x1a\xa1\x01\n\x12\x44ownSampleSchedule\x12!\n\x16\x64ownsample_factor_360p\x18\x01 \x01(\x02:\x01\x31\x12!\n\x16\x64ownsample_factor_480p\x18\x02 \x01(\x02:\x01\x31\x12!\n\x16\x64ownsample_factor_720p\x18\x03 \x01(\x02:\x01\x32\x12\"\n\x17\x64ownsample_factor_1080p\x18\x04 \x01(\x02:\x01\x32\x1a\xab\x01\n\x10\x42lurScoreOptions\x12\x1a\n\x0f\x62ox_filter_diam\x18\x01 \x01(\x05:\x01\x33\x12+\n\x1drelative_cornerness_threshold\x18\x02 \x01(\x02:\x04\x30.03\x12-\n\x1d\x61\x62solute_cornerness_threshold\x18\x03 \x01(\x02:\x06\x30.0001\x12\x1f\n\x11median_percentile\x18\x05 \x01(\x02:\x04\x30.85\x1a_\n\x18VisualConsistencyOptions\x12!\n\x13\x63ompute_consistency\x18\x01 \x01(\x08:\x04true\x12 \n\x14tiny_image_dimension\x18\x02 \x01(\x05:\x02\x32\x30\"<\n\x12IrlsInitialization\x12\x10\n\x0cINIT_UNIFORM\x10\x01\x12\x14\n\x10INIT_CONSISTENCY\x10\x02\"\xb1\x01\n\x0e\x44ownsampleMode\x12\x13\n\x0f\x44OWNSAMPLE_NONE\x10\x01\x12\x1a\n\x16\x44OWNSAMPLE_TO_MAX_SIZE\x10\x02\x12\x18\n\x14\x44OWNSAMPLE_BY_FACTOR\x10\x03\x12\x1a\n\x16\x44OWNSAMPLE_BY_SCHEDULE\x10\x04\x12\x1a\n\x16\x44OWNSAMPLE_TO_MIN_SIZE\x10\x05\x12\x1c\n\x18\x44OWNSAMPLE_TO_INPUT_SIZE\x10\x06\"|\n\x0fGainCorrectMode\x12\x1d\n\x19GAIN_CORRECT_DEFAULT_USER\x10\x01\x12\x16\n\x12GAIN_CORRECT_VIDEO\x10\x02\x12\x14\n\x10GAIN_CORRECT_HDR\x10\x03\x12\x1c\n\x18GAIN_CORRECT_PHOTO_BURST\x10\x04\"e\n\x0bImageFormat\x12\x14\n\x10\x46ORMAT_GRAYSCALE\x10\x01\x12\x0e\n\nFORMAT_RGB\x10\x02\x12\x0f\n\x0b\x46ORMAT_RGBA\x10\x03\x12\x0e\n\nFORMAT_BGR\x10\x04\x12\x0f\n\x0b\x46ORMAT_BGRA\x10\x05\"\"\n\x17\x44\x65scriptorExtractorType\x12\x07\n\x03ORB\x10\x00*\x04\x08\x05\x10\x06*\x04\x08\x07\x10\x08*\x04\x08\x08\x10\t*\x04\x08\t\x10\n*\x04\x08\n\x10\x0b*\x04\x08\x0f\x10\x10*\x04\x08\x10\x10\x11*\x04\x08\x18\x10\x19*\x04\x08\x1d\x10\x1e*\x04\x08\x1e\x10\x1f*\x04\x08 \x10!*\x04\x08*\x10+*\x04\x08+\x10,')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.tracking.region_flow_computation_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TRACKINGOPTIONS']._serialized_start=116
  _globals['_TRACKINGOPTIONS']._serialized_end=2212
  _globals['_TRACKINGOPTIONS_MINEIGVALEXTRACTIONSETTINGS']._serialized_start=1646
  _globals['_TRACKINGOPTIONS_MINEIGVALEXTRACTIONSETTINGS']._serialized_end=1758
  _globals['_TRACKINGOPTIONS_HARRISEXTRACTIONSETTINGS']._serialized_start=1760
  _globals['_TRACKINGOPTIONS_HARRISEXTRACTIONSETTINGS']._serialized_end=1826
  _globals['_TRACKINGOPTIONS_FASTEXTRACTIONSETTINGS']._serialized_start=1828
  _globals['_TRACKINGOPTIONS_FASTEXTRACTIONSETTINGS']._serialized_end=1875
  _globals['_TRACKINGOPTIONS_FLOWDIRECTION']._serialized_start=1877
  _globals['_TRACKINGOPTIONS_FLOWDIRECTION']._serialized_end=1938
  _globals['_TRACKINGOPTIONS_TRACKINGPOLICY']._serialized_start=1940
  _globals['_TRACKINGOPTIONS_TRACKINGPOLICY']._serialized_end=2029
  _globals['_TRACKINGOPTIONS_CORNEREXTRACTIONMETHOD']._serialized_start=2031
  _globals['_TRACKINGOPTIONS_CORNEREXTRACTIONMETHOD']._serialized_end=2127
  _globals['_TRACKINGOPTIONS_KLTTRACKERIMPLEMENTATION']._serialized_start=2129
  _globals['_TRACKINGOPTIONS_KLTTRACKERIMPLEMENTATION']._serialized_end=2188
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS']._serialized_start=2215
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS']._serialized_end=5902
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_DOWNSAMPLESCHEDULE']._serialized_start=4885
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_DOWNSAMPLESCHEDULE']._serialized_end=5046
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_BLURSCOREOPTIONS']._serialized_start=5049
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_BLURSCOREOPTIONS']._serialized_end=5220
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_VISUALCONSISTENCYOPTIONS']._serialized_start=5222
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_VISUALCONSISTENCYOPTIONS']._serialized_end=5317
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_IRLSINITIALIZATION']._serialized_start=5319
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_IRLSINITIALIZATION']._serialized_end=5379
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_DOWNSAMPLEMODE']._serialized_start=5382
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_DOWNSAMPLEMODE']._serialized_end=5559
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_GAINCORRECTMODE']._serialized_start=5561
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_GAINCORRECTMODE']._serialized_end=5685
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_IMAGEFORMAT']._serialized_start=5687
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_IMAGEFORMAT']._serialized_end=5788
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_DESCRIPTOREXTRACTORTYPE']._serialized_start=5790
  _globals['_REGIONFLOWCOMPUTATIONOPTIONS_DESCRIPTOREXTRACTORTYPE']._serialized_end=5824
# @@protoc_insertion_point(module_scope)
