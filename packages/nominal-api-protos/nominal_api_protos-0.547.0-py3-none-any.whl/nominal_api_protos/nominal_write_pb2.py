# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nominal_write.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13nominal_write.proto\x12\x1aio.nominal.scout.api.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"I\n\x13WriteRequestNominal\x12\x32\n\x06series\x18\x01 \x03(\x0b\x32\".io.nominal.scout.api.proto.Series\"\xdb\x01\n\x06Series\x12\x34\n\x07\x63hannel\x18\x01 \x01(\x0b\x32#.io.nominal.scout.api.proto.Channel\x12:\n\x04tags\x18\x02 \x03(\x0b\x32,.io.nominal.scout.api.proto.Series.TagsEntry\x12\x32\n\x06points\x18\x03 \x01(\x0b\x32\".io.nominal.scout.api.proto.Points\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x17\n\x07\x43hannel\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x9d\x01\n\x06Points\x12\x41\n\rdouble_points\x18\x01 \x01(\x0b\x32(.io.nominal.scout.api.proto.DoublePointsH\x00\x12\x41\n\rstring_points\x18\x02 \x01(\x0b\x32(.io.nominal.scout.api.proto.StringPointsH\x00\x42\r\n\x0bpoints_type\"G\n\x0c\x44oublePoints\x12\x37\n\x06points\x18\x01 \x03(\x0b\x32\'.io.nominal.scout.api.proto.DoublePoint\"G\n\x0cStringPoints\x12\x37\n\x06points\x18\x01 \x03(\x0b\x32\'.io.nominal.scout.api.proto.StringPoint\"K\n\x0b\x44oublePoint\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\x01\"K\n\x0bStringPoint\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\tB\x1e\n\x1aio.nominal.scout.api.protoP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nominal_write_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032io.nominal.scout.api.protoP\001'
  _SERIES_TAGSENTRY._options = None
  _SERIES_TAGSENTRY._serialized_options = b'8\001'
  _WRITEREQUESTNOMINAL._serialized_start=84
  _WRITEREQUESTNOMINAL._serialized_end=157
  _SERIES._serialized_start=160
  _SERIES._serialized_end=379
  _SERIES_TAGSENTRY._serialized_start=336
  _SERIES_TAGSENTRY._serialized_end=379
  _CHANNEL._serialized_start=381
  _CHANNEL._serialized_end=404
  _POINTS._serialized_start=407
  _POINTS._serialized_end=564
  _DOUBLEPOINTS._serialized_start=566
  _DOUBLEPOINTS._serialized_end=637
  _STRINGPOINTS._serialized_start=639
  _STRINGPOINTS._serialized_end=710
  _DOUBLEPOINT._serialized_start=712
  _DOUBLEPOINT._serialized_end=787
  _STRINGPOINT._serialized_start=789
  _STRINGPOINT._serialized_end=864
# @@protoc_insertion_point(module_scope)
