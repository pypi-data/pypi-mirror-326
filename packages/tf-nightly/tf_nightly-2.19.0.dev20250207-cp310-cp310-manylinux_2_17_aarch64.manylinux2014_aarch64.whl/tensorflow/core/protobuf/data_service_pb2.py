# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/data_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+tensorflow/core/protobuf/data_service.proto\x12\x0ftensorflow.data\"\xb7\x01\n\x11ProcessingModeDef\x12J\n\x0fsharding_policy\x18\x01 \x01(\x0e\x32\x31.tensorflow.data.ProcessingModeDef.ShardingPolicy\"V\n\x0eShardingPolicy\x12\x07\n\x03OFF\x10\x00\x12\x0b\n\x07\x44YNAMIC\x10\x01\x12\x08\n\x04\x46ILE\x10\x02\x12\x08\n\x04\x44\x41TA\x10\x03\x12\x10\n\x0c\x46ILE_OR_DATA\x10\x04\x12\x08\n\x04HINT\x10\x05\"\x9a\x02\n\x13\x44\x61taServiceMetadata\x12\x16\n\x0c\x65lement_spec\x18\x01 \x01(\x0cH\x00\x12\x45\n\x0b\x63ompression\x18\x02 \x01(\x0e\x32\x30.tensorflow.data.DataServiceMetadata.Compression\x12\x13\n\x0b\x63\x61rdinality\x18\x03 \x01(\x03\"v\n\x0b\x43ompression\x12\x1b\n\x17\x43OMPRESSION_UNSPECIFIED\x10\x00\x12\x13\n\x0f\x43OMPRESSION_OFF\x10\x01\x12\x16\n\x12\x43OMPRESSION_SNAPPY\x10\x02\x12\x1d\n\x19\x43OMPRESSION_FORCED_SNAPPY\x10\x03\x42\x17\n\x15optional_element_spec\".\n\x18\x43rossTrainerCacheOptions\x12\x12\n\ntrainer_id\x18\x01 \x01(\t\"M\n\x11\x44\x61taServiceConfig\x12\x38\n\x0f\x64\x65ployment_mode\x18\x01 \x01(\x0e\x32\x1f.tensorflow.data.DeploymentMode*\x88\x01\n\x0e\x44\x65ploymentMode\x12\x1f\n\x1b\x44\x45PLOYMENT_MODE_UNSPECIFIED\x10\x00\x12\x1d\n\x19\x44\x45PLOYMENT_MODE_COLOCATED\x10\x01\x12\x1a\n\x16\x44\x45PLOYMENT_MODE_REMOTE\x10\x02\x12\x1a\n\x16\x44\x45PLOYMENT_MODE_HYBRID\x10\x03\x42WZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_protob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.protobuf.data_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto'
  _DEPLOYMENTMODE._serialized_start=663
  _DEPLOYMENTMODE._serialized_end=799
  _PROCESSINGMODEDEF._serialized_start=65
  _PROCESSINGMODEDEF._serialized_end=248
  _PROCESSINGMODEDEF_SHARDINGPOLICY._serialized_start=162
  _PROCESSINGMODEDEF_SHARDINGPOLICY._serialized_end=248
  _DATASERVICEMETADATA._serialized_start=251
  _DATASERVICEMETADATA._serialized_end=533
  _DATASERVICEMETADATA_COMPRESSION._serialized_start=390
  _DATASERVICEMETADATA_COMPRESSION._serialized_end=508
  _CROSSTRAINERCACHEOPTIONS._serialized_start=535
  _CROSSTRAINERCACHEOPTIONS._serialized_end=581
  _DATASERVICECONFIG._serialized_start=583
  _DATASERVICECONFIG._serialized_end=660
# @@protoc_insertion_point(module_scope)
