# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/example/feature.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%tensorflow/core/example/feature.proto\x12\ntensorflow\"\x1a\n\tBytesList\x12\r\n\x05value\x18\x01 \x03(\x0c\"\x1e\n\tFloatList\x12\x11\n\x05value\x18\x01 \x03(\x02\x42\x02\x10\x01\" \n\tInt64List\x12\x13\n\x05value\x18\x01 \x03(\x03\x42\x04\x10\x01\x30\x01\"\x98\x01\n\x07\x46\x65\x61ture\x12+\n\nbytes_list\x18\x01 \x01(\x0b\x32\x15.tensorflow.BytesListH\x00\x12+\n\nfloat_list\x18\x02 \x01(\x0b\x32\x15.tensorflow.FloatListH\x00\x12+\n\nint64_list\x18\x03 \x01(\x0b\x32\x15.tensorflow.Int64ListH\x00\x42\x06\n\x04kind\"\x83\x01\n\x08\x46\x65\x61tures\x12\x32\n\x07\x66\x65\x61ture\x18\x01 \x03(\x0b\x32!.tensorflow.Features.FeatureEntry\x1a\x43\n\x0c\x46\x65\x61tureEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.tensorflow.Feature:\x02\x38\x01\"3\n\x0b\x46\x65\x61tureList\x12$\n\x07\x66\x65\x61ture\x18\x01 \x03(\x0b\x32\x13.tensorflow.Feature\"\x9c\x01\n\x0c\x46\x65\x61tureLists\x12?\n\x0c\x66\x65\x61ture_list\x18\x01 \x03(\x0b\x32).tensorflow.FeatureLists.FeatureListEntry\x1aK\n\x10\x46\x65\x61tureListEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.tensorflow.FeatureList:\x02\x38\x01\x42\x81\x01\n\x16org.tensorflow.exampleB\rFeatureProtosP\x01ZSgithub.com/tensorflow/tensorflow/tensorflow/go/core/example/example_protos_go_proto\xf8\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.example.feature_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026org.tensorflow.exampleB\rFeatureProtosP\001ZSgithub.com/tensorflow/tensorflow/tensorflow/go/core/example/example_protos_go_proto\370\001\001'
  _FLOATLIST.fields_by_name['value']._options = None
  _FLOATLIST.fields_by_name['value']._serialized_options = b'\020\001'
  _INT64LIST.fields_by_name['value']._options = None
  _INT64LIST.fields_by_name['value']._serialized_options = b'\020\0010\001'
  _FEATURES_FEATUREENTRY._options = None
  _FEATURES_FEATUREENTRY._serialized_options = b'8\001'
  _FEATURELISTS_FEATURELISTENTRY._options = None
  _FEATURELISTS_FEATURELISTENTRY._serialized_options = b'8\001'
  _BYTESLIST._serialized_start=53
  _BYTESLIST._serialized_end=79
  _FLOATLIST._serialized_start=81
  _FLOATLIST._serialized_end=111
  _INT64LIST._serialized_start=113
  _INT64LIST._serialized_end=145
  _FEATURE._serialized_start=148
  _FEATURE._serialized_end=300
  _FEATURES._serialized_start=303
  _FEATURES._serialized_end=434
  _FEATURES_FEATUREENTRY._serialized_start=367
  _FEATURES_FEATUREENTRY._serialized_end=434
  _FEATURELIST._serialized_start=436
  _FEATURELIST._serialized_end=487
  _FEATURELISTS._serialized_start=490
  _FEATURELISTS._serialized_end=646
  _FEATURELISTS_FEATURELISTENTRY._serialized_start=571
  _FEATURELISTS_FEATURELISTENTRY._serialized_end=646
# @@protoc_insertion_point(module_scope)
