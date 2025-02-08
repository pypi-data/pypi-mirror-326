# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/genai/inference/proto/transformer_params.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nAmediapipe/tasks/cc/genai/inference/proto/transformer_params.proto\x12\x10odml.infra.proto\"\x92\x13\n\x15TransformerParameters\x12\x12\n\nbatch_size\x18\x01 \x01(\x05\x12\x16\n\x0emax_seq_length\x18\x02 \x01(\x05\x12\x15\n\rembedding_dim\x18\x03 \x01(\x05\x12\x18\n\x10hidden_dimension\x18\x04 \x01(\x05\x12\x16\n\x0ehead_dimension\x18\x05 \x01(\x05\x12\x11\n\tnum_heads\x18\x06 \x01(\x05\x12\x12\n\nnum_stacks\x18\x07 \x01(\x05\x12\x14\n\x0cnum_kv_heads\x18\t \x01(\x05\x12^\n\x17\x66\x65\x65\x64_forward_parameters\x18\x0b \x01(\x0b\x32=.odml.infra.proto.TransformerParameters.FeedForwardParameters\x12`\n\x18\x66inal_project_parameters\x18\x0c \x01(\x0b\x32>.odml.infra.proto.TransformerParameters.FinalProjectParameters\x12>\n\x08pre_norm\x18\r \x01(\x0e\x32,.odml.infra.proto.TransformerParameters.Norm\x12?\n\tpost_norm\x18\x0e \x01(\x0e\x32,.odml.infra.proto.TransformerParameters.Norm\x12@\n\nfinal_norm\x18\x0f \x01(\x0e\x32,.odml.infra.proto.TransformerParameters.Norm\x12\x62\n\x19self_attention_parameters\x18\x10 \x01(\x0b\x32?.odml.infra.proto.TransformerParameters.SelfAttentionParameters\x12+\n#skip_absolute_positional_embeddings\x18\x12 \x01(\x08\x12k\n\x1bresidual_adapter_parameters\x18\x16 \x01(\x0b\x32\x41.odml.infra.proto.TransformerParameters.ResidualAdapterParametersH\x00\x88\x01\x01\x12!\n\x14query_rescale_factor\x18\x19 \x01(\x02H\x01\x88\x01\x01\x12\x19\n\x11vision_tokens_num\x18\x1a \x01(\x05\x12\x16\n\x0emax_num_images\x18\x1c \x01(\x05\x12\x18\n\x10num_extra_stacks\x18\x1b \x01(\x05\x12\x1a\n\x12\x61udio_vocab_offset\x18\x1d \x01(\x05\x12\x1d\n\x15\x61udio_vocab_extra_dim\x18\x1e \x01(\x05\x12!\n\x19\x61udio_input_embedding_dim\x18\x1f \x01(\x05\x1a\xf1\x01\n\x15\x46\x65\x65\x64\x46orwardParameters\x12\x0f\n\x07no_bias\x18\x01 \x01(\x08\x12\x46\n\nactivation\x18\x02 \x01(\x0e\x32\x32.odml.infra.proto.TransformerParameters.Activation\x12>\n\x08pre_norm\x18\x03 \x01(\x0e\x32,.odml.infra.proto.TransformerParameters.Norm\x12?\n\tpost_norm\x18\x04 \x01(\x0e\x32,.odml.infra.proto.TransformerParameters.Norm\x1a\x41\n\x16\x46inalProjectParameters\x12\x0f\n\x07no_bias\x18\x01 \x01(\x08\x12\x16\n\x0esoft_cap_value\x18\x02 \x01(\x02\x1a\xb7\x02\n\x17SelfAttentionParameters\x12\x13\n\x0bqkv_no_bias\x18\x01 \x01(\x08\x12\x19\n\x11post_proj_no_bias\x18\x02 \x01(\x08\x12V\n\x13\x61ttention_mask_type\x18\x03 \x01(\x0e\x32\x39.odml.infra.proto.TransformerParameters.AttentionMaskType\x12\x16\n\x0esoft_cap_value\x18\x04 \x01(\x02\x12]\n\x14\x61ttention_scale_type\x18\x05 \x01(\x0e\x32:.odml.infra.proto.TransformerParameters.AttentionScaleTypeH\x00\x88\x01\x01\x42\x17\n\x15_attention_scale_typeJ\x04\x08\x06\x10\x07\x1a\x91\x01\n\x19ResidualAdapterParameters\x12V\n\x13where_to_interleave\x18\x01 \x01(\x0e\x32\x39.odml.infra.proto.TransformerParameters.WhereToInterleave\x12\x1c\n\x14\x62ottleneck_dimension\x18\x02 \x01(\x05\"O\n\x11\x41ttentionMaskType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06\x43\x41USAL\x10\x01\x12\n\n\x06PREFIX\x10\x02\x12\x11\n\rBIDIRECTIONAL\x10\x03\"S\n\nActivation\x12\x1a\n\x16\x41\x43TIVATION_UNSPECIFIED\x10\x00\x12\x08\n\x04GELU\x10\x01\x12\x08\n\x04SILU\x10\x02\x12\x08\n\x04RELU\x10\x03\x12\x0b\n\x07RELU1P5\x10\x04\"G\n\x04Norm\x12\x14\n\x10NORM_UNSPECIFIED\x10\x00\x12\x0b\n\x07NO_NORM\x10\x01\x12\x0c\n\x08RMS_NORM\x10\x02\x12\x0e\n\nLAYER_NORM\x10\x03\"\xcb\x01\n\x12\x41ttentionScaleType\x12\x1a\n\x16SCALE_TYPE_UNSPECIFIED\x10\x00\x12\x1c\n\x18SCALE_TYPE_PER_DIM_SCALE\x10\x01\x12 \n\x1cSCALE_TYPE_INV_SQRT_HEAD_DIM\x10\x02\x12-\n)SCALE_TYPE_INV_SQRT_D_MODEL_DIV_NUM_HEADS\x10\x03\x12*\n&SCALE_TYPE_RESCALE_FACTOR_INV_HEAD_DIM\x10\x04\"K\n\x11WhereToInterleave\x12\x1a\n\x16INTERLEAVE_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41LL\x10\x01\x12\x11\n\rEVERY_OTHER_4\x10\x02\x42\x1e\n\x1c_residual_adapter_parametersB\x17\n\x15_query_rescale_factorJ\x04\x08\x08\x10\tJ\x04\x08\n\x10\x0bJ\x04\x08\x11\x10\x12J\x04\x08\x13\x10\x14J\x04\x08\x14\x10\x15J\x04\x08\x15\x10\x16J\x04\x08\x17\x10\x18J\x04\x08\x18\x10\x19\x42\x39\n\x1b\x63om.google.odml.infra.protoB\x1aTransformerParametersProtob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.genai.inference.proto.transformer_params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\033com.google.odml.infra.protoB\032TransformerParametersProto'
  _globals['_TRANSFORMERPARAMETERS']._serialized_start=88
  _globals['_TRANSFORMERPARAMETERS']._serialized_end=2538
  _globals['_TRANSFORMERPARAMETERS_FEEDFORWARDPARAMETERS']._serialized_start=1141
  _globals['_TRANSFORMERPARAMETERS_FEEDFORWARDPARAMETERS']._serialized_end=1382
  _globals['_TRANSFORMERPARAMETERS_FINALPROJECTPARAMETERS']._serialized_start=1384
  _globals['_TRANSFORMERPARAMETERS_FINALPROJECTPARAMETERS']._serialized_end=1449
  _globals['_TRANSFORMERPARAMETERS_SELFATTENTIONPARAMETERS']._serialized_start=1452
  _globals['_TRANSFORMERPARAMETERS_SELFATTENTIONPARAMETERS']._serialized_end=1763
  _globals['_TRANSFORMERPARAMETERS_RESIDUALADAPTERPARAMETERS']._serialized_start=1766
  _globals['_TRANSFORMERPARAMETERS_RESIDUALADAPTERPARAMETERS']._serialized_end=1911
  _globals['_TRANSFORMERPARAMETERS_ATTENTIONMASKTYPE']._serialized_start=1913
  _globals['_TRANSFORMERPARAMETERS_ATTENTIONMASKTYPE']._serialized_end=1992
  _globals['_TRANSFORMERPARAMETERS_ACTIVATION']._serialized_start=1994
  _globals['_TRANSFORMERPARAMETERS_ACTIVATION']._serialized_end=2077
  _globals['_TRANSFORMERPARAMETERS_NORM']._serialized_start=2079
  _globals['_TRANSFORMERPARAMETERS_NORM']._serialized_end=2150
  _globals['_TRANSFORMERPARAMETERS_ATTENTIONSCALETYPE']._serialized_start=2153
  _globals['_TRANSFORMERPARAMETERS_ATTENTIONSCALETYPE']._serialized_end=2356
  _globals['_TRANSFORMERPARAMETERS_WHERETOINTERLEAVE']._serialized_start=2358
  _globals['_TRANSFORMERPARAMETERS_WHERETOINTERLEAVE']._serialized_end=2433
# @@protoc_insertion_point(module_scope)
