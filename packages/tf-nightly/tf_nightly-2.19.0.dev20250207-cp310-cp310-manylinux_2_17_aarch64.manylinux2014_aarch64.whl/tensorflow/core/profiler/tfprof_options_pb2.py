# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/profiler/tfprof_options.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-tensorflow/core/profiler/tfprof_options.proto\x12\x11tensorflow.tfprof\"\x95\x04\n\x0cOptionsProto\x12\x11\n\tmax_depth\x18\x01 \x01(\x03\x12\x11\n\tmin_bytes\x18\x02 \x01(\x03\x12\x16\n\x0emin_peak_bytes\x18\x13 \x01(\x03\x12\x1a\n\x12min_residual_bytes\x18\x14 \x01(\x03\x12\x18\n\x10min_output_bytes\x18\x15 \x01(\x03\x12\x12\n\nmin_micros\x18\x03 \x01(\x03\x12\x1e\n\x16min_accelerator_micros\x18\x16 \x01(\x03\x12\x16\n\x0emin_cpu_micros\x18\x17 \x01(\x03\x12\x12\n\nmin_params\x18\x04 \x01(\x03\x12\x15\n\rmin_float_ops\x18\x05 \x01(\x03\x12\x16\n\x0emin_occurrence\x18\x11 \x01(\x03\x12\x0c\n\x04step\x18\x12 \x01(\x03\x12\x10\n\x08order_by\x18\x07 \x01(\t\x12\x1c\n\x14\x61\x63\x63ount_type_regexes\x18\x08 \x03(\t\x12\x1a\n\x12start_name_regexes\x18\t \x03(\t\x12\x19\n\x11trim_name_regexes\x18\n \x03(\t\x12\x19\n\x11show_name_regexes\x18\x0b \x03(\t\x12\x19\n\x11hide_name_regexes\x18\x0c \x03(\t\x12!\n\x19\x61\x63\x63ount_displayed_op_only\x18\r \x01(\x08\x12\x0e\n\x06select\x18\x0e \x03(\t\x12\x0e\n\x06output\x18\x0f \x01(\t\x12\x14\n\x0c\x64ump_to_file\x18\x10 \x01(\t\"\xda\x02\n\x13\x41\x64visorOptionsProto\x12\x46\n\x08\x63heckers\x18\x01 \x03(\x0b\x32\x34.tensorflow.tfprof.AdvisorOptionsProto.CheckersEntry\x1a\x65\n\rCheckersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x43\n\x05value\x18\x02 \x01(\x0b\x32\x34.tensorflow.tfprof.AdvisorOptionsProto.CheckerOption:\x02\x38\x01\x1a\x93\x01\n\rCheckerOption\x12R\n\x07options\x18\x01 \x03(\x0b\x32\x41.tensorflow.tfprof.AdvisorOptionsProto.CheckerOption.OptionsEntry\x1a.\n\x0cOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.profiler.tfprof_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ADVISOROPTIONSPROTO_CHECKERSENTRY._options = None
  _ADVISOROPTIONSPROTO_CHECKERSENTRY._serialized_options = b'8\001'
  _ADVISOROPTIONSPROTO_CHECKEROPTION_OPTIONSENTRY._options = None
  _ADVISOROPTIONSPROTO_CHECKEROPTION_OPTIONSENTRY._serialized_options = b'8\001'
  _OPTIONSPROTO._serialized_start=69
  _OPTIONSPROTO._serialized_end=602
  _ADVISOROPTIONSPROTO._serialized_start=605
  _ADVISOROPTIONSPROTO._serialized_end=951
  _ADVISOROPTIONSPROTO_CHECKERSENTRY._serialized_start=700
  _ADVISOROPTIONSPROTO_CHECKERSENTRY._serialized_end=801
  _ADVISOROPTIONSPROTO_CHECKEROPTION._serialized_start=804
  _ADVISOROPTIONSPROTO_CHECKEROPTION._serialized_end=951
  _ADVISOROPTIONSPROTO_CHECKEROPTION_OPTIONSENTRY._serialized_start=905
  _ADVISOROPTIONSPROTO_CHECKEROPTION_OPTIONSENTRY._serialized_end=951
# @@protoc_insertion_point(module_scope)
