# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/function/trace_type/serialization_test.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow.core.function.trace_type import serialization_pb2 as tensorflow_dot_core_dot_function_dot_trace__type_dot_serialization__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<tensorflow/core/function/trace_type/serialization_test.proto\x12\x36tensorflow.core.function.trace_type.serialization_test\x1a\x37tensorflow/core/function/trace_type/serialization.proto\"5\n\x16MyCustomRepresentation\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"u\n\x19MyCompositeRepresentation\x12X\n\x08\x65lements\x18\x01 \x03(\x0b\x32\x46.tensorflow.core.function.trace_type.serialization.SerializedTraceType\"(\n\x1aMyMultiClassRepresentation\x12\n\n\x02id\x18\x01 \x01(\x05')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.function.trace_type.serialization_test_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MYCUSTOMREPRESENTATION._serialized_start=177
  _MYCUSTOMREPRESENTATION._serialized_end=230
  _MYCOMPOSITEREPRESENTATION._serialized_start=232
  _MYCOMPOSITEREPRESENTATION._serialized_end=349
  _MYMULTICLASSREPRESENTATION._serialized_start=351
  _MYMULTICLASSREPRESENTATION._serialized_end=391
# @@protoc_insertion_point(module_scope)
