# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/flow_packager.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.util.tracking import motion_models_pb2 as mediapipe_dot_util_dot_tracking_dot_motion__models__pb2
from mediapipe.util.tracking import region_flow_pb2 as mediapipe_dot_util_dot_tracking_dot_region__flow__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+mediapipe/util/tracking/flow_packager.proto\x12\tmediapipe\x1a+mediapipe/util/tracking/motion_models.proto\x1a)mediapipe/util/tracking/region_flow.proto\"\xb1\x05\n\x0cTrackingData\x12\x16\n\x0b\x66rame_flags\x18\x01 \x01(\x05:\x01\x30\x12\x14\n\x0c\x64omain_width\x18\x02 \x01(\x05\x12\x15\n\rdomain_height\x18\x03 \x01(\x05\x12\x17\n\x0c\x66rame_aspect\x18\x06 \x01(\x02:\x01\x31\x12/\n\x10\x62\x61\x63kground_model\x18\x04 \x01(\x0b\x32\x15.mediapipe.Homography\x12\x37\n\x0bmotion_data\x18\x05 \x01(\x0b\x32\".mediapipe.TrackingData.MotionData\x12\x1c\n\x14global_feature_count\x18\x07 \x01(\r\x12 \n\x18\x61verage_motion_magnitude\x18\x08 \x01(\x02\x1a\xeb\x01\n\nMotionData\x12\x14\n\x0cnum_elements\x18\x01 \x01(\x05\x12\x17\n\x0bvector_data\x18\x02 \x03(\x02\x42\x02\x10\x01\x12\x14\n\x08track_id\x18\x03 \x03(\x05\x42\x02\x10\x01\x12\x17\n\x0brow_indices\x18\x04 \x03(\x05\x42\x02\x10\x01\x12\x16\n\ncol_starts\x18\x05 \x03(\x05\x42\x02\x10\x01\x12?\n\x13\x66\x65\x61ture_descriptors\x18\x06 \x03(\x0b\x32\".mediapipe.BinaryFeatureDescriptor\x12&\n\x1e\x61\x63tively_discarded_tracked_ids\x18\x07 \x03(\x05\"\xaa\x01\n\nFrameFlags\x12\x19\n\x15\x46LAG_PROFILE_BASELINE\x10\x00\x12\x15\n\x11\x46LAG_PROFILE_HIGH\x10\x01\x12\x1e\n\x1a\x46LAG_HIGH_FIDELITY_VECTORS\x10\x02\x12\x1c\n\x18\x46LAG_BACKGROUND_UNSTABLE\x10\x04\x12\x13\n\x0f\x46LAG_DUPLICATED\x10\x08\x12\x17\n\x13\x46LAG_CHUNK_BOUNDARY\x10\x10\"\xfb\x01\n\x11TrackingDataChunk\x12/\n\x04item\x18\x01 \x03(\x0b\x32!.mediapipe.TrackingDataChunk.Item\x12\x19\n\nlast_chunk\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x0b\x66irst_chunk\x18\x03 \x01(\x08:\x05\x66\x61lse\x1a~\n\x04Item\x12.\n\rtracking_data\x18\x01 \x01(\x0b\x32\x17.mediapipe.TrackingData\x12\x11\n\tframe_idx\x18\x02 \x01(\x05\x12\x16\n\x0etimestamp_usec\x18\x03 \x01(\x03\x12\x1b\n\x13prev_timestamp_usec\x18\x04 \x01(\x03\"\"\n\x12\x42inaryTrackingData\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x8a\x01\n\x08MetaData\x12\x12\n\nnum_frames\x18\x02 \x01(\x07\x12\x36\n\rtrack_offsets\x18\x03 \x03(\x0b\x32\x1f.mediapipe.MetaData.TrackOffset\x1a\x32\n\x0bTrackOffset\x12\x0c\n\x04msec\x18\x01 \x01(\x07\x12\x15\n\rstream_offset\x18\x02 \x01(\x07\"S\n\x11TrackingContainer\x12\x0e\n\x06header\x18\x01 \x01(\t\x12\x12\n\x07version\x18\x02 \x01(\x07:\x01\x31\x12\x0c\n\x04size\x18\x03 \x01(\x07\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\"\xad\x01\n\x17TrackingContainerFormat\x12/\n\tmeta_data\x18\x01 \x01(\x0b\x32\x1c.mediapipe.TrackingContainer\x12\x30\n\ntrack_data\x18\x02 \x03(\x0b\x32\x1c.mediapipe.TrackingContainer\x12/\n\tterm_data\x18\x03 \x01(\x0b\x32\x1c.mediapipe.TrackingContainer\"s\n\x16TrackingContainerProto\x12&\n\tmeta_data\x18\x01 \x01(\x0b\x32\x13.mediapipe.MetaData\x12\x31\n\ntrack_data\x18\x02 \x03(\x0b\x32\x1d.mediapipe.BinaryTrackingData\"\xc1\x02\n\x13\x46lowPackagerOptions\x12\x19\n\x0c\x64omain_width\x18\x01 \x01(\x05:\x03\x32\x35\x36\x12\x1a\n\rdomain_height\x18\x02 \x01(\x05:\x03\x31\x39\x32\x12*\n\x1c\x62inary_tracking_data_support\x18\x06 \x01(\x08:\x04true\x12\x1f\n\x10use_high_profile\x18\x03 \x01(\x08:\x05\x66\x61lse\x12(\n\x1ahigh_fidelity_16bit_encode\x18\x04 \x01(\x08:\x04true\x12)\n\x1chigh_profile_reuse_threshold\x18\x05 \x01(\x02:\x03\x30.5\"Q\n\x13HighProfileEncoding\x12\x11\n\x0c\x41\x44VANCE_FLAG\x10\x80\x01\x12\x17\n\x13\x44OUBLE_INDEX_ENCODE\x10@\x12\x0e\n\nINDEX_MASK\x10?')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.tracking.flow_packager_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['vector_data']._options = None
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['vector_data']._serialized_options = b'\020\001'
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['track_id']._options = None
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['track_id']._serialized_options = b'\020\001'
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['row_indices']._options = None
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['row_indices']._serialized_options = b'\020\001'
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['col_starts']._options = None
  _globals['_TRACKINGDATA_MOTIONDATA'].fields_by_name['col_starts']._serialized_options = b'\020\001'
  _globals['_TRACKINGDATA']._serialized_start=147
  _globals['_TRACKINGDATA']._serialized_end=836
  _globals['_TRACKINGDATA_MOTIONDATA']._serialized_start=428
  _globals['_TRACKINGDATA_MOTIONDATA']._serialized_end=663
  _globals['_TRACKINGDATA_FRAMEFLAGS']._serialized_start=666
  _globals['_TRACKINGDATA_FRAMEFLAGS']._serialized_end=836
  _globals['_TRACKINGDATACHUNK']._serialized_start=839
  _globals['_TRACKINGDATACHUNK']._serialized_end=1090
  _globals['_TRACKINGDATACHUNK_ITEM']._serialized_start=964
  _globals['_TRACKINGDATACHUNK_ITEM']._serialized_end=1090
  _globals['_BINARYTRACKINGDATA']._serialized_start=1092
  _globals['_BINARYTRACKINGDATA']._serialized_end=1126
  _globals['_METADATA']._serialized_start=1129
  _globals['_METADATA']._serialized_end=1267
  _globals['_METADATA_TRACKOFFSET']._serialized_start=1217
  _globals['_METADATA_TRACKOFFSET']._serialized_end=1267
  _globals['_TRACKINGCONTAINER']._serialized_start=1269
  _globals['_TRACKINGCONTAINER']._serialized_end=1352
  _globals['_TRACKINGCONTAINERFORMAT']._serialized_start=1355
  _globals['_TRACKINGCONTAINERFORMAT']._serialized_end=1528
  _globals['_TRACKINGCONTAINERPROTO']._serialized_start=1530
  _globals['_TRACKINGCONTAINERPROTO']._serialized_end=1645
  _globals['_FLOWPACKAGEROPTIONS']._serialized_start=1648
  _globals['_FLOWPACKAGEROPTIONS']._serialized_end=1969
  _globals['_FLOWPACKAGEROPTIONS_HIGHPROFILEENCODING']._serialized_start=1888
  _globals['_FLOWPACKAGEROPTIONS_HIGHPROFILEENCODING']._serialized_end=1969
# @@protoc_insertion_point(module_scope)
